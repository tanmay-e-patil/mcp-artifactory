"""Instagram MCP Server.

Version: 1.0.0
"""
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)

# Import server instance first
from server import mcp

# Import all tools to register them via decorators
from tools import *

if __name__ == "__main__":
    logger.info(f"Starting Instagram MCP Server")
    mcp.run(transport="stdio")