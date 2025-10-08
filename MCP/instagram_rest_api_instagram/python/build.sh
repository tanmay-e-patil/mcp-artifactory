#!/bin/bash

# Build script for Python MCP server binary
# Usage: ./build.sh

set -e

echo "Building Python MCP Server Binary..."

# Create bin directory if it doesn't exist
mkdir -p bin

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if PyInstaller is installed, if not install it
if ! command -v pyinstaller &> /dev/null; then
    echo "Installing PyInstaller..."
    pip install pyinstaller
fi

# Build the binary
pyinstaller --onefile --name mcp-server --distpath bin main.py

# Clean up build artifacts
rm -rf build/ *.spec

# Make binary executable
chmod +x bin/mcp-server

# Get current directory path
CURRENT_DIR=$(pwd)

# Update mcp-stdio.json with current directory
if [ -f "mcp-stdio.json" ]; then
    echo "Updating mcp-stdio.json with current directory: $CURRENT_DIR"
    sed -i.bak "s|\"/path/to/your/python/mcp/server/directory\"|\"$CURRENT_DIR\"|g" mcp-stdio.json
    sed -i.bak "s|\"python\"|\"$CURRENT_DIR/python\"|g" mcp-stdio.json
    sed -i.bak "s|\"main.py\"|\"$CURRENT_DIR/main.py\"|g" mcp-stdio.json
    rm -f mcp-stdio.json.bak
    echo "mcp-stdio.json updated successfully!"
else
    echo "mcp-stdio.json not found, creating with current directory: $CURRENT_DIR"
    cat > mcp-stdio.json << EOF
{
  "mcpServers": {
    "mcp-server-stdio": {
      "command": "python",
      "args": ["$CURRENT_DIR/main.py"],
      "env": {
        "API_BASE_URL": "https://your.api.url",
        "BEARER_TOKEN": "your-token-here"
      }
    }
  }
}
EOF
fi

echo "Binary built successfully!"
echo "Usage: ./bin/mcp-server or python main.py"
echo "MCP Config: mcp-stdio.json (updated with current directory)"
