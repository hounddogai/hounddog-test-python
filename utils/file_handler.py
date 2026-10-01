import os
import uuid
from datetime import datetime

from streamlit.runtime.uploaded_file_manager import UploadedFile


class FileStorageError(Exception):
    """Raised when a medical file cannot be saved or read."""


class FileHandler:
    def __init__(self) -> None:
        """Initialize file handler with base storage directory."""
        self.base_dir = "medical_files"
        self.ensure_directory_exists(self.base_dir)

    def ensure_directory_exists(self, directory: str) -> None:
        """Create directory if it doesn't exist."""
        os.makedirs(directory, exist_ok=True)

    def save_file(self, uploaded_file: UploadedFile, patient_id: str, record_type: str) -> str:
        """
        Save uploaded file to storage directory.

        Args:
            uploaded_file: Streamlit uploaded file object
            patient_id: ID of the patient
            record_type: Type of medical record

        Returns:
            str: Path to saved file
        """
        try:
            # Create patient directory
            patient_dir = os.path.join(self.base_dir, f"patient_{patient_id}")
            self.ensure_directory_exists(patient_dir)

            # Generate unique filename
            file_extension = os.path.splitext(uploaded_file.name)[1]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = str(uuid.uuid4())[:8]

            filename = f"{record_type.replace(' ', '_')}_{timestamp}_{unique_id}{file_extension}"
            file_path = os.path.join(patient_dir, filename)

            # Save file
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            return file_path

        except OSError as e:
            raise FileStorageError(f"Failed to save file: {e}") from e

    def get_file(self, file_path: str) -> bytes:
        """
        Retrieve file content from storage.

        Args:
            file_path: Path to the file

        Returns:
            bytes: File content
        """
        try:
            with open(file_path, "rb") as f:
                return f.read()

        except OSError as e:
            raise FileStorageError(f"Failed to retrieve file: {e}") from e
