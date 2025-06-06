from mcp.server.fastmcp import FastMCP
import logging
from typing import Annotated, Dict, Any, Optional


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("math_server")


# Initialize FastMCP server with proper configuration for Streamable HTTP
mcp = FastMCP("Math2Server", port=8003)


@mcp.tool()
def multiply(x: float, y: float) -> float:
    return x * y

if __name__ == "__main__":
    mcp.run(transport="sse")