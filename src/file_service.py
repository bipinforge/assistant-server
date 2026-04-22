"""
File service - handles file storage and retrieval operations.
"""

from src.schemas.file_schema import FileSchema
from src.mongo_client import FileCRUD


def store_file_details(filename: str, filepath: str, status: str = "uploaded") -> str:
    """
    Store file details in MongoDB.
    
    Args:
        filename: Name of the file
        filepath: Path where the file is stored
        status: Status of the file (default: "uploaded")
        
    Returns:
        ID of the inserted file document
    """
    file_data = FileSchema.create(filename=filename, filepath=filepath, status=status)
    file_id = FileCRUD.create(file_data)
    return file_id


def get_all_files():
    """
    Retrieve all uploaded files.
    
    Returns:
        List of all file documents
    """
    return FileCRUD.read_all()


def get_file_by_id(file_id: str):
    """
    Retrieve a specific file by ID.
    
    Args:
        file_id: The file document ID
        
    Returns:
        File document or None if not found
    """
    return FileCRUD.read(file_id)


def get_file_by_filename(filename: str):
    """
    Retrieve a file by its filename.
    
    Args:
        filename: The name of the file
        
    Returns:
        File document or None if not found
    """
    return FileCRUD.read_by_filename(filename)


def update_file_status(file_id: str, status: str) -> bool:
    """
    Update the status of a file.
    
    Args:
        file_id: The file document ID
        status: New status value
        
    Returns:
        True if update was successful, False otherwise
    """
    return FileCRUD.update_status(file_id, status)


def delete_file(file_id: str) -> bool:
    """
    Delete a file document.
    
    Args:
        file_id: The file document ID
        
    Returns:
        True if deletion was successful, False otherwise
    """
    return FileCRUD.delete(file_id)
