# Multi-stage build for Python MCP Server
FROM python:3.11-alpine AS builder

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install PyInstaller
RUN pip install --no-cache-dir pyinstaller

# Copy source code
COPY . .

# Build the binary
RUN pyinstaller --onefile --name mcp-server main.py

# Final stage
FROM alpine:latest

# Install ca-certificates for HTTPS requests
RUN apk --no-cache add ca-certificates

# Create app directory
WORKDIR /app

# Copy binary from builder stage
COPY --from=builder /app/dist/mcp-server .

# Make binary executable
RUN chmod +x mcp-server

# Expose port (if running in HTTP mode)
EXPOSE 8080

# Set non-sensitive environment variables
ENV PORT="8080"
ENV TRANSPORT="http"

# Run the binary
CMD ["./mcp-server"]
