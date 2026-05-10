from dataclasses import dataclass
from langchain.chat_models import init_chat_model
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse, SummarizationMiddleware
from langgraph.checkpoint.redis import RedisSaver 
from langchain.tools import tool
from typing import Callable, List, Dict, Any
from deepagents import create_deep_agent
from src.ingestion_service import query_embedding
from src.mongo_client import ConversationCRUD
from datetime import datetime
import json


redis_saver = RedisSaver(
    redis_url="redis://localhost:6379"
)

redis_saver.setup()

agent = None


@dataclass
class Context:
    model: str

@wrap_model_call
def configurable_model(
    request: ModelRequest,
    handler: Callable[[ModelRequest], ModelResponse],
) -> ModelResponse:
    model_name = request.runtime.context.model

    # Optional: cache models to avoid re-init cost
    if not hasattr(configurable_model, "cache"):
        configurable_model.cache = {}

    if model_name not in configurable_model.cache:
        configurable_model.cache[model_name] = init_chat_model(model_name)

    model = configurable_model.cache[model_name]

    return handler(request.override(model=model))


@tool
def rag_retrieval_tool(query: str) -> str:
    """
    Fetches RAG (Retrieval-Augmented Generation) context from the vector store.
    Use this tool to retrieve relevant documents based on a user query.
    
    Args:
        query: The search query to retrieve relevant documents
        
    Returns:
        String containing the relevant documents/context from the vector store
    """
    try:
        print(f"Invoking RAG retrieval tool with query: {query}")
        results = query_embedding(query)
        
        # Format results for the agent
        if not results:
            return "No relevant documents found for the query."
        
        formatted_results = []
        for i, doc in enumerate(results, 1):
            if hasattr(doc, 'page_content'):
                formatted_results.append(f"Document {i}:\n{doc.page_content}")
            else:
                formatted_results.append(f"Document {i}:\n{str(doc)}")
        
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Error retrieving documents: {str(e)}"


def init_agent():
    global agent
    tools = [rag_retrieval_tool]
    
    agent = create_deep_agent(
        model="openai:gpt-4o-mini",  # default fallback
        middleware=[configurable_model, SummarizationMiddleware(max_tokens=500, model="openai:gpt-4o-mini")],
        context_schema=Context,
        tools=tools,
        checkpointer=redis_saver
    )


def _get_or_create_conversation(thread_id: str, user_id: str) -> str:
    """
    Fetch existing conversation by thread_id, or create a new one if it doesn't exist.
    
    Args:
        thread_id: The thread ID to look up or create
        user_id: The user ID for creating new conversation
        
    Returns:
        The conversation ID (document _id as string)
    """
    # Try to fetch existing conversation by thread_id
    existing_conversation = ConversationCRUD.read_by_thread_id(thread_id)
    
    if existing_conversation:
        return str(existing_conversation["_id"])
    
    # Create new conversation if it doesn't exist
    conversation_data = {
        "thread_id": thread_id,
        "user_id": user_id,
        "messages": [],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
    }
    
    conversation_id = ConversationCRUD.create(conversation_data)
    return conversation_id


def _build_message_history(conversation_id: str, user_message: str) -> List[Dict[str, str]]:
    """
    Build complete message history from database plus the new user message.
    
    Args:
        conversation_id: The conversation document ID
        user_message: The new user message to add
        
    Returns:
        List of message dictionaries with 'role' and 'content' keys
    """
    conversation = ConversationCRUD.read(conversation_id)
    
    # Start with previous messages
    messages = []
    if conversation and "messages" in conversation:
        messages = conversation["messages"].copy()
    
    # Add the new user message
    messages.append({
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().isoformat()
    })
    
    return messages


#provide default model name and user message for testing
def run_agent(thread_id: str, user_id: str, model_name: str = "openai:gpt-4o-mini", user_message: str = "Hello!"):
    """
    Run the agent with conversation history management.
    
    Args:
        thread_id: The conversation thread ID
        user_id: The user ID
        model_name: The model to use (default: openai:gpt-4o-mini)
        user_message: The user's message

    Returns:
        The agent's response and conversation ID
    """
    # Get or create conversation
    conversation_id = _get_or_create_conversation(thread_id, user_id)
    
    # Build complete message history
    messages = _build_message_history(conversation_id, user_message)
    
    # Invoke agent with complete message history
    assistant_response = ''
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    agent_state = agent.get_state(config)
    print(f"Agent state before call:", agent_state)
    for chunk in agent.stream({"messages": messages}, stream_mode='messages', context=Context(model=model_name), version="v2", config=config):
        # print(" \n\n *** RAW CHUNK:", chunk)
        try:
            chunk_type = chunk.get("type")
            ns = chunk.get("ns", ())
            message_chunk, metadata = chunk["data"]  # unpack the tuple

            # Only process main agent LLM tokens (skip subagent namespaces)
            if ns:
                continue

            if chunk_type == "messages" and metadata.get("langgraph_node") == "model":
                content = message_chunk.content

                # Standard text token
                if isinstance(content, str) and content:
                    assistant_response += content
                    yield content

                # Anthropic-style structured content blocks
                elif isinstance(content, list):
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text = block.get("text", "")
                            if text:
                                assistant_response += text
                                yield text

                # Tool call chunks — just track/log, don't yield
                if message_chunk.tool_call_chunks:
                    for tc in message_chunk.tool_call_chunks:
                        print(f"[tool call chunk] {tc}")


        # Subagent updates (non-empty namespace)
        except (KeyError, StopIteration):
            pass

    # Add user message to conversation
    user_msg_record = {
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().isoformat()
    }
    ConversationCRUD.add_message(conversation_id, user_msg_record)
    
    # Add assistant response to conversation
    assistant_msg_record = {
        "role": "assistant",
        "content": assistant_response,
        "timestamp": datetime.now().isoformat()
    }
    ConversationCRUD.add_message(conversation_id, assistant_msg_record)
