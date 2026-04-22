"""
MongoDB client and CRUD operations for ingestion server.
Centralizes all database operations for files and conversations.
"""

from pymongo import MongoClient
from datetime import datetime
from typing import Optional, List, Dict, Any
import os
from bson.objectid import ObjectId

# --- DB CONFIG ---
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")

client = MongoClient(MONGO_URL)
db = client["ingestion_db"]

# Collections
files_collection = db["files"]
conversations_collection = db["conversations"]


# ============================================================================
# FILE CRUD OPERATIONS
# ============================================================================

class FileCRUD:
    """Centralized CRUD operations for files collection."""

    @staticmethod
    def create(file_data: dict) -> str:
        """
        Insert a new file document.
        
        Args:
            file_data: Dictionary containing file information
            
        Returns:
            String representation of the inserted document ID
        """
        result = files_collection.insert_one(file_data)
        return str(result.inserted_id)

    @staticmethod
    def read(file_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a file by ID.
        
        Args:
            file_id: The file document ID
            
        Returns:
            File document or None if not found
        """
        try:
            return files_collection.find_one({"_id": ObjectId(file_id)})
        except:
            return None

    @staticmethod
    def read_all() -> List[Dict[str, Any]]:
        """
        Retrieve all files.
        
        Returns:
            List of file documents
        """
        return list(files_collection.find({}, {"_id": 0}))

    @staticmethod
    def read_by_filename(filename: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a file by filename.
        
        Args:
            filename: The name of the file
            
        Returns:
            File document or None if not found
        """
        return files_collection.find_one({"filename": filename})

    @staticmethod
    def update(file_id: str, update_data: dict) -> bool:
        """
        Update a file document.
        
        Args:
            file_id: The file document ID
            update_data: Dictionary of fields to update
            
        Returns:
            True if document was updated, False otherwise
        """
        try:
            update_data["updated_at"] = datetime.now()
            result = files_collection.update_one(
                {"_id": ObjectId(file_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except:
            return False

    @staticmethod
    def delete(file_id: str) -> bool:
        """
        Delete a file document.
        
        Args:
            file_id: The file document ID
            
        Returns:
            True if document was deleted, False otherwise
        """
        try:
            result = files_collection.delete_one({"_id": ObjectId(file_id)})
            return result.deleted_count > 0
        except:
            return False

    @staticmethod
    def update_status(file_id: str, status: str) -> bool:
        """
        Update the status of a file.
        
        Args:
            file_id: The file document ID
            status: New status value
            
        Returns:
            True if status was updated, False otherwise
        """
        return FileCRUD.update(file_id, {"status": status})


# ============================================================================
# CONVERSATION CRUD OPERATIONS
# ============================================================================

class ConversationCRUD:
    """Centralized CRUD operations for conversations collection."""

    @staticmethod
    def create(conversation_data: dict) -> str:
        """
        Insert a new conversation document.
        
        Args:
            conversation_data: Dictionary containing conversation information
            
        Returns:
            String representation of the inserted document ID
        """
        result = conversations_collection.insert_one(conversation_data)
        return str(result.inserted_id)

    @staticmethod
    def read(conversation_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a conversation by ID.
        
        Args:
            conversation_id: The conversation document ID
            
        Returns:
            Conversation document or None if not found
        """
        try:
            return conversations_collection.find_one({"_id": ObjectId(conversation_id)})
        except:
            return None

    @staticmethod
    def read_by_thread_id(thread_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a conversation by thread ID.
        
        Args:
            thread_id: The conversation thread ID
            
        Returns:
            Conversation document or None if not found
        """
        return conversations_collection.find_one({"thread_id": thread_id})

    @staticmethod
    def read_by_user_id(user_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all conversations for a specific user.
        
        Args:
            user_id: The user ID
            
        Returns:
            List of conversation documents
        """
        return list(conversations_collection.find({"user_id": user_id}))

    @staticmethod
    def read_all() -> List[Dict[str, Any]]:
        """
        Retrieve all conversations.
        
        Returns:
            List of conversation documents
        """
        return list(conversations_collection.find({}))

    @staticmethod
    def update(conversation_id: str, update_data: dict) -> bool:
        """
        Update a conversation document.
        
        Args:
            conversation_id: The conversation document ID
            update_data: Dictionary of fields to update
            
        Returns:
            True if document was updated, False otherwise
        """
        try:
            update_data["updated_at"] = datetime.now()
            result = conversations_collection.update_one(
                {"_id": ObjectId(conversation_id)},
                {"$set": update_data}
            )
            return result.modified_count > 0
        except:
            return False

    @staticmethod
    def add_message(conversation_id: str, message: dict) -> bool:
        """
        Add a message to a conversation.
        
        Args:
            conversation_id: The conversation document ID
            message: Message object to add
            
        Returns:
            True if message was added, False otherwise
        """
        try:
            result = conversations_collection.update_one(
                {"_id": ObjectId(conversation_id)},
                {
                    "$push": {"messages": message},
                    "$set": {"updated_at": datetime.now()}
                }
            )
            return result.modified_count > 0
        except:
            return False

    @staticmethod
    def delete(conversation_id: str) -> bool:
        """
        Delete a conversation document.
        
        Args:
            conversation_id: The conversation document ID
            
        Returns:
            True if document was deleted, False otherwise
        """
        try:
            result = conversations_collection.delete_one({"_id": ObjectId(conversation_id)})
            return result.deleted_count > 0
        except:
            return False

    @staticmethod
    def update_status(conversation_id: str, status: str) -> bool:
        """
        Update the status of a conversation.
        
        Args:
            conversation_id: The conversation document ID
            status: New status value
            
        Returns:
            True if status was updated, False otherwise
        """
        return ConversationCRUD.update(conversation_id, {"status": status})
