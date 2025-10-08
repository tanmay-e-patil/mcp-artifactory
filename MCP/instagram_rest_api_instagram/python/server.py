"""MCP Server instance."""
import logging
from mcp.server.fastmcp import FastMCP

logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("Instagram")