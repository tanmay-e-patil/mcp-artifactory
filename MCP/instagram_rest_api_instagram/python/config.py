"""API configuration for instagram."""
import os
from typing import Dict, Any


class APIConfig:
    """API configuration."""
    
    def __init__(
        self,
        base_url: str = "",
        bearer_token: str = "",
        api_key: str = "",
        basic_auth: str = "",
        port: str = ""
    ):
        self.base_url = base_url
        self.bearer_token = bearer_token
        self.api_key = api_key
        self.basic_auth = basic_auth
        self.port = port


def load_api_config() -> Dict[str, Any]:
    """
    Load API configuration from environment variables.
    
    Returns:
        Configuration dictionary
        
    Raises:
        ValueError: If required configuration is missing
    """
    # Check port environment variable
    port = os.getenv("PORT") or os.getenv("port", "")
    
    base_url = os.getenv("API_BASE_URL", "")
    
    # Check transport environment variable
    transport = os.getenv("TRANSPORT") or os.getenv("transport", "")
    
    # For STDIO mode (not HTTP/HTTPS), API_BASE_URL is required
    if transport not in ["http", "HTTP", "https", "HTTPS"] and not base_url:
        raise ValueError("API_BASE_URL environment variable not set")
    
    return {
        "base_url": base_url,
        "bearer_token": os.getenv("BEARER_TOKEN", ""),
        "api_key": os.getenv("API_KEY", ""),
        "basic_auth": os.getenv("BASIC_AUTH", ""),
        "port": port,
    }