# Instagram MCP Server

This MCP (Model Content Protocol) server provides access to Instagram API functionality through STDIO transport mode with FastMCP.

## Features

- FastMCP-based server with decorator pattern
- Automatic tool registration via @mcp.tool() decorators
- Type-safe parameter handling
- Comprehensive error handling and logging
- Easy configuration through environment variables

## Prerequisites

- Python 3.10 or later
- pip package manager

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
export API_BASE_URL="https://your-api-base-url"
export BEARER_TOKEN="your-bearer-token"
# Alternative authentication options (use only one):
# export API_KEY="your-api-key"
# export BASIC_AUTH="your-basic-auth-credentials"
```

## Running the MCP Server

### STDIO Mode (Default)

The server runs in STDIO mode by default, which is perfect for direct integration with AI assistants like Cursor:

```bash
python main.py
```

### Configuration for Cursor/Claude Desktop

Add this to your MCP configuration file (e.g., `~/Library/Application Support/Cursor/User/globalStorage/@anthropic/mcp-server-registry/mcp.json`):

```json
{
  "mcpServers": {
    "instagram-mcp-server": {
      "command": "python",
      "args": ["/path/to/your/project/main.py"],
      "env": {
        "API_BASE_URL": "https://your-api-base-url",
        "BEARER_TOKEN": "your-bearer-token"
      }
    }
  }
}
```

## Environment Variables

### Required
- `API_BASE_URL`: Base URL for the API endpoint

### Authentication (use one of the following)
- `BEARER_TOKEN`: Bearer token for OAuth2/Bearer authentication
- `API_KEY`: API key for API key authentication
- `BASIC_AUTH`: Basic authentication credentials (base64 encoded)

**Note**: At least one authentication variable should be provided unless the API explicitly doesn't require authentication.

## Development

For development with auto-reload:

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with Python
python main.py
```

## Project Structure

```
.
├── main.py              # Entry point with FastMCP server
├── config.py            # Configuration management
├── models.py            # Pydantic data models
├── tools/               # Auto-generated tools organized by category
│   ├── __init__.py
│   └── [category]/      # Tools grouped by API endpoint category
│       ├── __init__.py
│       └── *.py         # Individual tool implementations
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## How It Works

This MCP server is built using FastMCP with a decorator-based architecture:

1. **FastMCP Server**: Creates an MCP server instance in `main.py`
2. **Tool Decorators**: Each tool is decorated with `@mcp.tool()` for automatic registration
3. **Auto-Import**: Tools are automatically registered when their modules are imported
4. **Type Safety**: Uses Python type hints for parameter validation
5. **Error Handling**: Comprehensive error handling with JSON error responses

### Example Tool

```python
from main import mcp

@mcp.tool()
def get_users(search: str = None, page: int = None) -> str:
    """
    Get users from the API.
    
    Args:
        search: Search query for filtering users
        page: Page number for pagination
        
    Returns:
        JSON string with user data
    """
    # Tool implementation...
    return json.dumps(result, indent=2)
```

## Authentication Methods

The server supports multiple authentication methods:

### Bearer Token (OAuth2)
```bash
export BEARER_TOKEN="your-bearer-token"
```

### API Key
```bash
export API_KEY="your-api-key"
```

### Basic Authentication
```bash
export BASIC_AUTH="base64-encoded-credentials"
```

## Logging

The server includes comprehensive logging to stderr:
- INFO level: General operations, tool registration
- WARNING level: Skipped operations, missing parameters
- ERROR level: API errors, request failures

View logs in your MCP client's console or stderr output.

## Troubleshooting

### "Missing required parameter" errors
- Check that all required parameters are provided
- Verify parameter names match the tool definition

### Authentication errors
- Ensure the correct authentication environment variable is set
- Verify your credentials are valid and not expired
- Check that the API_BASE_URL is correct

### Import errors
- Run `pip install -r requirements.txt` to ensure all dependencies are installed
- Check that you're using Python 3.10 or later

### Tool not found
- Verify the tool name matches what's shown in your MCP client
- Check the tools directory structure
- Ensure all `__init__.py` files are present

## Generated Tools

This server was automatically generated from an OpenAPI specification. Each API endpoint is exposed as an MCP tool with:
- Automatic parameter extraction and validation
- Type-safe parameter handling  
- Comprehensive error handling
- JSON response formatting

Use your MCP client's tool listing feature to see all available tools.

## Contributing

This is a generated MCP server. To modify tool behavior:
1. Edit the tool implementation in `tools/[category]/[tool_name].py`
2. Maintain the `@mcp.tool()` decorator for registration
3. Keep the function signature for parameter validation
4. Test changes by running the server locally

## License

This generated MCP server follows the same license as the generator tool.