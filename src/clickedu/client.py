"""
Main ClickEdu API client.
"""

from typing import Optional
from .models import User
from .auth import get_user
from .query import QueryApi
from .exceptions import ClickEduError, AuthenticationError, APIError
from .utils.logger import setup_logger
from .config import Config


class ClickEduClient:
    """
    Main ClickEdu API client.
    
    This is the primary interface for interacting with the ClickEdu API.
    It provides a clean, high-level API for authentication and data retrieval.
    """
    
    def __init__(self, log_level: str = "WARNING"):
        """
        Initialize ClickEdu client.
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.config = Config(log_level=log_level)
        self.logger = setup_logger("clickedu.client", log_level)
        self._user: Optional[User] = None
        self._query_api: Optional[QueryApi] = None
    
    def authenticate(self, username: str, password: str) -> User:
        """
        Authenticate with ClickEdu.
        
        Args:
            username: Username for authentication
            password: Password for authentication
            
        Returns:
            Authenticated user object
            
        Raises:
            AuthenticationError: If authentication fails
            ClickEduError: If other errors occur
        """
        try:
            self.logger.info(f"Authenticating user {username} with domain {self.config.domain}")
            self._user = get_user(self.config.domain, username, password, self.config)
            
            if not self._user:
                raise AuthenticationError("Authentication failed")
            
            # Initialize query API
            self._query_api = QueryApi(self._user, self.config)
            
            self.logger.info("Authentication successful")
            return self._user
            
        except (AuthenticationError, APIError):
            # Re-raise known exceptions
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during authentication: {e}")
            raise ClickEduError(f"Unexpected error during authentication: {e}") from e
    
    @property
    def is_authenticated(self) -> bool:
        """Check if client is authenticated."""
        return self._user is not None and self._query_api is not None
    
    def _ensure_authenticated(self):
        """Ensure client is authenticated."""
        if not self.is_authenticated:
            raise AuthenticationError("Client not authenticated. Call authenticate() first.")
    
    def get_news(self, start_limit: int = 0, end_limit: int = 10):
        """
        Get news from ClickEdu.
        
        Args:
            start_limit: Starting index for news items
            end_limit: Ending index for news items
            
        Returns:
            NewsResponse object with news items
            
        Raises:
            AuthenticationError: If not authenticated
            APIError: If API request fails
        """
        self._ensure_authenticated()
        return self._query_api.get_news(start_limit, end_limit)
    
    def get_photo_albums(self, start_limit: int = 0, end_limit: int = 10):
        """
        Get photo albums from ClickEdu.
        
        Args:
            start_limit: Starting index for albums
            end_limit: Ending index for albums
            
        Returns:
            PhotoAlbumsResponse object with photo albums
            
        Raises:
            AuthenticationError: If not authenticated
            APIError: If API request fails
        """
        self._ensure_authenticated()
        return self._query_api.get_photo_albums(start_limit, end_limit)
    
    def get_album_photos(self, album_id: str):
        """
        Get photos from a specific album.
        
        Args:
            album_id: ID of the album
            
        Returns:
            GetAlbumByIdResponse object with photos
            
        Raises:
            AuthenticationError: If not authenticated
            APIError: If API request fails
        """
        self._ensure_authenticated()
        return self._query_api.get_album_by_id(album_id)
    
    def download_file(self, file_path: str, download_dir: str = "files"):
        """
        Download a file from ClickEdu.
        
        Args:
            file_path: Path to the file (from news item)
            download_dir: Directory to save the file
            
        Returns:
            Path to the downloaded file or None if failed
            
        Raises:
            AuthenticationError: If not authenticated
        """
        self._ensure_authenticated()
        return self._query_api.download_file(file_path, download_dir)
    
    def init(self):
        """
        Execute initialization query.
        
        Returns:
            InitQueryResponse object
            
        Raises:
            AuthenticationError: If not authenticated
            APIError: If API request fails
        """
        self._ensure_authenticated()
        return self._query_api.init()
    
    @property
    def user(self) -> Optional[User]:
        """Get the authenticated user object."""
        return self._user
