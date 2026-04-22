from datetime import datetime
from typing import Optional, List


class ConversationSchema:
    """
    Schema for conversation documents in MongoDB.
    Defines the structure for storing chat conversations and messages.
    """

    @staticmethod
    def create(
        thread_id: str,
        user_id: str,
        messages: Optional[List[dict]] = None,
        status: str = "active",
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ) -> dict:
        """
        Create a conversation document.
        
        Args:
            thread_id: Unique identifier for the conversation thread
            user_id: ID of the user who owns this conversation
            messages: List of message objects in the conversation
            status: Status of the conversation (e.g., 'active', 'archived', 'closed')
            created_at: Timestamp when conversation was created
            updated_at: Timestamp when conversation was last updated
            
        Returns:
            Dictionary representing the conversation document
        """
        now = datetime.now()
        return {
            "thread_id": thread_id,
            "user_id": user_id,
            "messages": messages or [],
            "status": status,
            "created_at": created_at or now,
            "updated_at": updated_at or now
        }
