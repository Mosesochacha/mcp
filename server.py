"""
MiniMax MCP — SSE wrapper
Runs the official minimax-mcp server over SSE so Claude web can connect.
Set MINIMAX_API_KEY and MINIMAX_API_HOST before running.
"""
import os, sys

# Required env vars
if not os.getenv("MINIMAX_API_KEY"):
    print("ERROR: Set MINIMAX_API_KEY environment variable")
    sys.exit(1)
if not os.getenv("MINIMAX_API_HOST"):
    os.environ["MINIMAX_API_HOST"] = "https://api.minimax.io"
if not os.getenv("MINIMAX_MCP_BASE_PATH"):
    os.environ["MINIMAX_MCP_BASE_PATH"] = "/tmp/minimax-output"
    os.makedirs("/tmp/minimax-output", exist_ok=True)

# Import the official MiniMax MCP server and run it over SSE
from minimax_mcp.server import mcp

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🚀 MiniMax MCP SSE server starting on port {port}")
    print(f"   Connector URL: http://localhost:{port}/sse")
    mcp.run(transport="sse")
