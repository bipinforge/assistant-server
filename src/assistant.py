from dataclasses import dataclass
from langchain.chat_models import init_chat_model
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from langchain.tools import tool
from typing import Callable, List
from deepagents import create_deep_agent
from src.ingestion_service import query_embedding

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
        middleware=[configurable_model],
        context_schema=Context,
        tools=tools,
    )

#provide default model name and user message for testing
def run_agent(model_name: str = "openai:gpt-4o-mini", user_message: str = "Hello!"):
    result = agent.invoke(
        {"messages": [{"role": "user", "content": user_message}]},
        context=Context(model=model_name)
    )
    return result
