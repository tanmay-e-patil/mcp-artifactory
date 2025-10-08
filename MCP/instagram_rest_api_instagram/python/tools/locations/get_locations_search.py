"""GetLocationsSearch tool implementation."""
import json
import logging
from typing import Any
import requests
from server import mcp

logger = logging.getLogger(__name__)


@mcp.tool()
def getlocationssearch(
    distance: str = None,
    facebook_places_id: str = None,
    foursquare_id: str = None,
    lat: str = None,
    lng: str = None,
    foursquare_v2_id: str = None
) -> str:
    """
    Search for a location by geographic coordinate.
    
    Args:
        distance: Default is 1000m (distance=1000), max distance is 5000.
        facebook_places_id: Returns a location mapped off of a Facebook places id. If used, a Foursquare id and `lat`, `lng` are not required.
        foursquare_id: Returns a location mapped off of a foursquare v1 api location id. If used, you are not required to use\n`lat` and `lng`. Note that this method is deprecated; you should use the new foursquare IDs with V2 of their API.\n
        lat: Latitude of the center search coordinate. If used, `lng` is required.
        lng: Longitude of the center search coordinate. If used, `lat` is required.
        foursquare_v2_id: Returns a location mapped off of a foursquare v2 api location id. If used, you are not required to use\n`lat` and `lng`.\n
        
    Returns:
        JSON string result
    """
    from config import load_api_config
    config = load_api_config()
    # Build query parameters
    query_params = {}
    if distance is not None:
        query_params["distance"] = distance
    if facebook_places_id is not None:
        query_params["facebook_places_id"] = facebook_places_id
    if foursquare_id is not None:
        query_params["foursquare_id"] = foursquare_id
    if lat is not None:
        query_params["lat"] = lat
    if lng is not None:
        query_params["lng"] = lng
    if foursquare_v2_id is not None:
        query_params["foursquare_v2_id"] = foursquare_v2_id
    
    # Build URL
    url = f"{config['base_url']}/locations/search"
    
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