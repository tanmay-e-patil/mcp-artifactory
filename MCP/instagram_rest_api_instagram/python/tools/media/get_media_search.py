"""GetMediaSearch tool implementation."""
import json
import logging
from typing import Any
import requests
from server import mcp

logger = logging.getLogger(__name__)


@mcp.tool()
def getmediasearch(
    lat: str = None,
    lng: str = None,
    min_timestamp: str = None,
    max_timestamp: str = None,
    distance: str = None
) -> str:
    """
    Search for media in a given area.
    
    Args:
        lat: Latitude of the center search coordinate. If used, `lng` is required.
        lng: Longitude of the center search coordinate. If used, `lat` is required.
        min_timestamp: Return media after this UNIX timestamp.
        max_timestamp: Return media before this UNIX timestamp.
        distance: Default is 1000m (distance=1000), max distance is 5000.
        
    Returns:
        JSON string result
    """
    from config import load_api_config
    config = load_api_config()
    # Build query parameters
    query_params = {}
    if lat is not None:
        query_params["lat"] = lat
    if lng is not None:
        query_params["lng"] = lng
    if min_timestamp is not None:
        query_params["min_timestamp"] = min_timestamp
    if max_timestamp is not None:
        query_params["max_timestamp"] = max_timestamp
    if distance is not None:
        query_params["distance"] = distance
    
    # Build URL
    url = f"{config['base_url']}/media/search"
    
    # Build headers
    headers = {
        "Accept": "application/json",
        "X-Request-Source": "Codeglide-MCP-generator",
    }
    # No specific authentication - add fallback
    if config.get("bearer_token"):
        headers["Authorization"] = f"Bearer {config['bearer_token']}"
    elif config.get("api_key"):
        headers["Authorization"] = f"Bearer {config['api_key']}"
    elif config.get("basic_auth"):
        headers["Authorization"] = f"Basic {config['basic_auth']}"
    
    # Add custom headers
    
    try:
        # Make API request
        response = requests.request(
            method="GET",
            url=url,
            params=query_params,
            headers=headers,
            timeout=30
        )
        
        if response.status_code >= 400:
            return json.dumps({
                "error": f"API error ({response.status_code})",
                "message": response.text
            })
        
        # Parse response
        try:
            result = response.json()
            return json.dumps(result, indent=2)
        except json.JSONDecodeError:
            return response.text
            
    except requests.RequestException as e:
        logger.error(f"Request failed: {e}")
        return json.dumps({"error": f"Request failed: {str(e)}"})
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return json.dumps({"error": f"Error: {str(e)}"})