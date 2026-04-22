from datetime import datetime
from typing import Optional


class FileSchema:
    """
    Schema for file documents in MongoDB.
    Defines the structure for storing file metadata.
    """

    @staticmethod
    def create(
        filename: str,
        filepath: str,
        status: str = "uploaded",
        uploaded_at: Optional[datetime] = None
    ) -> dict:
        """
        Create a file document.
        
        Args:
            filename: Name of the file
            filepath: Path where the file is stored
            status: Status of the file (e.g., 'uploaded', 'processed', 'failed')
            uploaded_at: Timestamp when file was uploaded
            
        Returns:
            Dictionary representing the file document
        """
        return {
            "filename": filename,
            "filepath": filepath,
            "status": status,
            "uploaded_at": uploaded_at or datetime.now()
        }
