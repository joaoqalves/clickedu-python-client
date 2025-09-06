"""
File handling utilities for ClickEdu API client.
"""

import os
from urllib.parse import urlparse
from typing import Optional
from ..exceptions import FileDownloadError


class FileHandler:
    """Handles file download operations."""
    
    def __init__(self, session, base_url: str):
        """
        Initialize file handler.
        
        Args:
            session: Requests session object
            base_url: Base URL for file downloads
        """
        self.session = session
        self.base_url = base_url
    
    def download_file(self, file_path: str, download_dir: str = "files") -> Optional[str]:
        """
        Download a file from ClickEdu to the specified directory.
        
        Args:
            file_path: The file path from the news item (e.g., "../private/...")
            download_dir: Directory to save the file (default: "files")
            
        Returns:
            Path to the downloaded file or None if failed
            
        Raises:
            FileDownloadError: If download fails
        """
        try:
            # Create download directory if it doesn't exist
            os.makedirs(download_dir, exist_ok=True)
            
            # Construct the full URL for the file
            if file_path.startswith("../private/"):
                # Remove the "../private/" prefix and construct URL
                clean_path = file_path.replace("../private/", "")
                file_url = f"{self.base_url}/private/{clean_path}"
            else:
                # If it's already a full path, use it as is
                file_url = file_path
            
            # Extract filename from the path
            parsed_url = urlparse(file_url)
            filename = os.path.basename(parsed_url.path)
            
            # Full path where the file will be saved
            local_file_path = os.path.join(download_dir, filename)
            
            # Download the file
            response = self.session.get(file_url, stream=True)
            response.raise_for_status()
            
            # Save the file
            with open(local_file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            return local_file_path
            
        except Exception as e:
            raise FileDownloadError(f"Failed to download file {file_path}: {e}") from e
