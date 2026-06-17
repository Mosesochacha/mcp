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

import uvicorn
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import Response

PORT = int(os.environ.get("PORT", 8000))

sse = SseServerTransport("/messages/")

async def handle_sse(request):
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await mcp._mcp_server.run(
            streams[0], streams[1],
            mcp._mcp_server.create_initialization_options()
        )
    return Response()

starlette_app = Starlette(routes=[
    Route("/sse", endpoint=handle_sse),
    Mount("/messages/", app=sse.handle_post_message),
])

if __name__ == "__main__":
    print(f"🚀 MiniMax MCP SSE server starting on port {PORT}")
    print(f"   Connector URL: https://YOUR_APP.onrender.com/sse")
    uvicorn.run(starlette_app, host="0.0.0.0", port=PORT)
