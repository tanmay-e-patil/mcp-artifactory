"""GetGeographiesGeoIdMediaRecent tool implementation."""
import json
import logging
from typing import Any
import requests
from server import mcp

logger = logging.getLogger(__name__)


@mcp.tool()
def getgeographiesgeoidmediarecent(
    geo_id: str,
    count: str = None,
    min_id: str = None
) -> str:
    """
    Get recent media from a custom geo-id.
    
    Args:
        count: Max number of media to return.
        min_id: Return media before this `min_id`.
        geo_id: The geography ID.
        
    Returns:
        JSON string result
    """
    from config import load_api_config
    config = load_api_config()
    # Validate required path parameters
    if not geo_id:
        return json.dumps({"error": "Missing required path parameter: geo-id"})
    # Build query parameters
    query_params = {}
    if count is not None:
        query_params["count"] = count
    if min_id is not None:
        query_params["min_id"] = min_id
    
    # Build URL
    url = f"{config['base_url']}/geographies/{geo-id}/media/recent"
    
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