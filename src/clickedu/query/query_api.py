"""
Query API for ClickEdu.
"""

import requests
from typing import Dict, Any, Optional, List
from ..models import (
    User, InitQueryResponse, NewsResponse, NewsItem,
    PhotoAlbumsResponse, PhotoAlbum, GetAlbumByIdResponse, Photo
)
from ..exceptions import APIError
from ..utils.logger import setup_logger
from ..utils.file_handler import FileHandler


class QueryApi:
    """QueryApi class for handling ClickEdu query operations."""
    
    def __init__(self, user: User, config):
        """
        Initialize QueryApi.
        
        Args:
            user: Authenticated user object
            config: Configuration object
        """
        self.user = user
        self.config = config
        self.cons_key = config.cons_key
        self.cons_secret = config.cons_secret
        self.session = requests.Session()
        self.logger = setup_logger("clickedu.query")
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': self.config.get_user_agent()
        })
        
        # Initialize file handler
        self.file_handler = FileHandler(self.session, f"https://{self.user.base_url}")
    
    def _get_url_and_default_params(self) -> tuple[str, Dict[str, str]]:
        """Get URL and default parameters for queries."""
        url = f"https://{self.user.base_url}/ws/app_clickedu_query.php"
        
        default_params = {
            "auth_token": self.user.auth_token,
            "auth_secret": self.user.secret_token,
            "cons_key": self.cons_key,
            "cons_secret": self.cons_secret,
            "id_fill": self.user.child_id,
        }
        
        return url, default_params
    
    def _default_query(self, query: str, params: Dict[str, str | int] = None) -> Optional[Dict[str, Any]]:
        """Execute a default query with common parameters."""
        try:
            url, default_params = self._get_url_and_default_params()
            
            # Merge default params with provided params
            query_params = {**default_params, **(params or {}), "query": query}
            
            self.logger.info(f"Executing query: {query}")
            response = self.session.get(url, params=query_params)
            response.raise_for_status()
            
            result = response.json()
            self.logger.info(f"Query {query} successful!")
            return result
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error executing query {query}: {e}")
            if hasattr(e, 'response') and e.response is not None:
                self.logger.error(f"Response status: {e.response.status_code}")
                self.logger.error(f"Response content: {e.response.text}")
            raise APIError(f"Failed to execute query {query}: {e}", e.response.status_code if hasattr(e, 'response') and e.response else None) from e
    
    def init(self) -> Optional[InitQueryResponse]:
        """Execute /init query."""
        result = self._default_query("/init")
        if result:
            return InitQueryResponse()
        return None
    
    def get_news(self, start_limit: int = 0, end_limit: int = 10) -> Optional[NewsResponse]:
        """Get news from ClickEdu."""
        params = {
            "startLimit": start_limit,
            "endLimit": end_limit,
            "lan": "ca"  # Using Catalan as requested
        }
        
        result = self._default_query("/news", params)
        if result:
            # Parse news items from result
            news_data = result.get("news", [])
            news_items = []
            for news_item_data in news_data:
                news_item = NewsItem(
                    title=news_item_data.get("title", ""),
                    subtitle=news_item_data.get("subtitle"),
                    body=news_item_data.get("body"),
                    imagePath=news_item_data.get("imagePath"),
                    imageText=news_item_data.get("imageText"),
                    filePath=news_item_data.get("filePath")
                )
                news_items.append(news_item)
            
            return NewsResponse(
                total=result.get("total", 0),
                news=news_items
            )
        return None
    
    def get_photo_albums(self, start_limit: int = 0, end_limit: int = 10) -> Optional[PhotoAlbumsResponse]:
        """Get photo albums from ClickEdu."""
        params = {
            "startLimit": start_limit,
            "endLimit": end_limit,
            "lan": "ca"  # Using Catalan as requested
        }
        
        result = self._default_query("/photo_albums", params)
        if result:
            # Parse albums from result
            albums_data = result.get("albums", [])
            albums = []
            for album_data in albums_data:
                album = PhotoAlbum(
                    id=album_data.get("id", ""),
                    name=album_data.get("name", ""),
                    coverImageLarge=album_data.get("coverImageLarge"),
                    coverImageSmall=album_data.get("coverImageSmall")
                )
                albums.append(album)
            
            # Fix image URLs
            albums = self._fix_images_urls(albums, ["coverImageLarge", "coverImageSmall"])
            
            return PhotoAlbumsResponse(albums=albums)
        return None
    
    def get_album_by_id(self, album_id: str) -> Optional[GetAlbumByIdResponse]:
        """Get photos from a specific album."""
        params = {
            "albumId": album_id,
            "lan": "ca"  # Using Catalan as requested
        }
        
        result = self._default_query("/pictures", params)
        if result:
            # Parse photos from result
            photos_data = result.get("photos", [])
            photos = []
            for photo_data in photos_data:
                photo = Photo(
                    id=photo_data.get("id", ""),
                    pathLarge=photo_data.get("pathLarge"),
                    pathSmall=photo_data.get("pathSmall")
                )
                photos.append(photo)
            
            # Fix image URLs
            photos = self._fix_images_urls(photos, ["pathLarge", "pathSmall"])
            
            return GetAlbumByIdResponse(photos=photos)
        return None
    
    def _fix_images_urls(self, items: List, image_fields: List[str]) -> List:
        """Fix image URLs by adding the base URL."""
        base_url = self._get_photo_base_url()
        
        fixed_items = []
        for item in items:
            # Create a copy of the item
            if hasattr(item, '__dict__'):
                # For dataclass objects
                fixed_item = type(item)(**item.__dict__)
            else:
                # For dict objects
                fixed_item = {**item}
            
            # Fix each image field
            for field in image_fields:
                if hasattr(fixed_item, field):
                    current_value = getattr(fixed_item, field)
                    if current_value:
                        new_path = base_url + current_value.replace("../private/", "")
                        setattr(fixed_item, field, new_path)
                elif isinstance(fixed_item, dict) and field in fixed_item:
                    current_value = fixed_item[field]
                    if current_value:
                        new_path = base_url + current_value.replace("../private/", "")
                        fixed_item[field] = new_path
            
            fixed_items.append(fixed_item)
        
        return fixed_items
    
    def _get_photo_base_url(self) -> str:
        """Get the base URL for photos."""
        return f"https://{self.user.base_url}/private/app-{self.cons_key}-{self.cons_secret}-{self.user.auth_token}-{self.user.secret_token}/"
    
    def download_file(self, file_path: str, download_dir: str = "files") -> Optional[str]:
        """
        Download a file from ClickEdu to the specified directory.
        
        Args:
            file_path: The file path from the news item (e.g., "../private/...")
            download_dir: Directory to save the file (default: "files")
            
        Returns:
            Path to the downloaded file or None if failed
        """
        try:
            return self.file_handler.download_file(file_path, download_dir)
        except Exception as e:
            self.logger.error(f"Error downloading file {file_path}: {e}")
            return None
