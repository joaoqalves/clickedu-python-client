"""
Configuration management for ClickEdu API client.
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv
from .exceptions import ConfigurationError

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for ClickEdu API client."""
    
    def __init__(self, domain: Optional[str] = None, log_level: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            domain: ClickEdu domain (overrides environment variable)
            log_level: Logging level (overrides environment variable)
        """
        self.domain = domain or os.getenv("CLICKEDU_DOMAIN")
        self.cons_key = os.getenv("CLICKEDU_CONS_KEY", "xxx")
        self.cons_secret = os.getenv("CLICKEDU_CONS_SECRET", "xxx")
        self.api_key = os.getenv("CLICKEDU_API_KEY", "xxx")
        self.client_secret = os.getenv("CLICKEDU_CLIENT_SECRET", "xxx")
        self.default_language = os.getenv("DEFAULT_LANGUAGE", "ca")

        # Set up logging
        log_level_str = log_level or os.getenv("LOG_LEVEL", "WARNING")
        self.log_level = getattr(logging, log_level_str.upper(), logging.WARNING)
        
        # Validate required configuration
        if not self.domain:
            raise ConfigurationError("ClickEdu domain is required. Set CLICKEDU_DOMAIN environment variable or pass domain parameter.")
    
    @property
    def base_url(self) -> str:
        """Get the base URL for the ClickEdu instance."""
        return f"https://{self.domain}"
    
    @property
    def api_base_url(self) -> str:
        """Get the API base URL."""
        return "https://api.clickedu.eu"
    
    def get_user_agent(self) -> str:
        """Get the User-Agent string for requests."""
        return "ClickEdu/Python"
    
    def get_default_headers(self) -> dict:
        """Get default headers for requests."""
        return {
            "User-Agent": self.get_user_agent(),
            "content-type": "application/x-www-form-urlencoded"
        }
    
    def get_api_headers(self) -> dict:
        """Get headers for API requests."""
        return {
            "x-api-key": self.api_key,
            "domain": self.domain,
            "User-Agent": self.get_user_agent()
        }
