from src.mongo_client import ConversationCRUD

def get_conversation_history():
    """
    Fetch conversation history for a given thread or user.
    
    This function can be extended to accept parameters like thread_id or user_id
    to filter the conversation history accordingly.
    
    Returns:
        A list of conversations with their messages and metadata.
    """
    # For demonstration, we will fetch all conversations. In a real implementation,
    # you would likely want to filter by thread_id or user_id.
    res = ConversationCRUD.read_all()  # You would need to implement this method
    conversations = []
    for record in res:
        conversations.append({ 
            "id": str(record["_id"]),
            "thread_id": record.get("thread_id", "N/A"),
            "name": record["messages"][0]["content"] if "messages" in record and len(record["messages"]) > 0 else "No conversation Name",
        }) 
    return conversations

def get_conversation_history_by_thread(thread_id: str):
    """
    Fetch conversation history for a specific thread ID.
    
    Args:
        thread_id: The thread ID to filter conversations
    Returns:
        A conversation with its messages and metadata, or None if not found.
    """
    print(f" ***** Fetching conversation history for thread_id: {thread_id}")
    conversation = ConversationCRUD.read_by_thread_id(thread_id)  # You would need to implement this method
    print(f" ***** Conversation fetched: {conversation}")
    if conversation:
        return {
            "id": str(conversation["_id"]),
            "thread_id": conversation.get("thread_id", "N/A"),
            "messages": conversation.get("messages", [])
        }
    return {}