"""
Custom exceptions for ClickEdu API client.
"""


class ClickEduError(Exception):
    """Base exception for ClickEdu API errors."""
    pass


class AuthenticationError(ClickEduError):
    """Raised when authentication fails."""
    pass


class AuthorizationError(ClickEduError):
    """Raised when authorization fails."""
    pass


class APIError(ClickEduError):
    """Raised when API requests fail."""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data or {}


class ConfigurationError(ClickEduError):
    """Raised when configuration is invalid or missing."""
    pass


class FileDownloadError(ClickEduError):
    """Raised when file download fails."""
    pass


class ValidationError(ClickEduError):
    """Raised when data validation fails."""
    pass
