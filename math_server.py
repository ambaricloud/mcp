from mcp.server.fastmcp import FastMCP
import logging
import asyncio
from typing import Annotated, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Request
import uvicorn
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("math_server")

# Initialize FastAPI app
app = FastAPI(
    title="Math MCP Server",
    description="API for mathematical operations",
    version="0.1.0"
)

# Initialize FastMCP server with proper configuration for Streamable HTTP
mcp = FastMCP(
    name="MathServer",  # Server name
    description="Math MCP Server",  # Server description
    version="0.1.0",  # Server version
    stateless_http=True  # Enable stateless HTTP mode
)

# Mount the MCP server at /mcp endpoint
app.mount("/mcp", mcp.sse_app())

@mcp.tool()
def add(
    a: Annotated[int, "First number to add"],
    b: Annotated[int, "Second number to add"]
) -> int:
    """Add two numbers together."""
    try:
        result = a + b
        logger.info(f"add({a}, {b}) = {result}")
        return result
    except Exception as e:
        logger.error(f"Error in add operation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@mcp.tool()
def sub(
    a: Annotated[int, "Number to subtract from"],
    b: Annotated[int, "Number to subtract"]
) -> int:
    """Subtract second number from first number."""
    try:
        result = a - b
        logger.info(f"sub({a}, {b}) = {result}")
        return result
    except Exception as e:
        logger.error(f"Error in sub operation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@mcp.tool()
def multiply(
    a: Annotated[int, "First number to multiply"],
    b: Annotated[int, "Second number to multiply"]
) -> int:
    """Multiply two numbers together."""
    try:
        result = a * b
        logger.info(f"multiply({a}, {b}) = {result}")
        return result
    except Exception as e:
        logger.error(f"Error in multiply operation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@mcp.prompt()
def Add_Prompt(
    a: Annotated[int, "First number to add"],
    b: Annotated[int, "Second number to add"]
) -> str:
    """Prompt to add two numbers."""
    prompt = f"Add {a} and {b}."
    logger.info(f"Add_Prompt({a}, {b}) -> {prompt}")
    return prompt

@mcp.prompt()
def Sub_Prompt(
    a: Annotated[int, "Number to subtract from"],
    b: Annotated[int, "Number to subtract"]
) -> str:
    """Prompt to subtract two numbers."""
    prompt = f"Subtract {b} from {a}."
    logger.info(f"Sub_Prompt({a}, {b}) -> {prompt}")
    return prompt

@mcp.prompt()
def Multiply_Prompt(
    a: Annotated[int, "First number to multiply"],
    b: Annotated[int, "Second number to multiply"]
) -> str:
    """Prompt to multiply two numbers."""
    prompt = f"Multiply {a} and {b}."
    logger.info(f"Multiply_Prompt({a}, {b}) -> {prompt}")
    return prompt

async def print_registered_tools():
    """Print the list of registered tools asynchronously."""
    try:
        tools = await mcp.list_tools()
        print("Registered tools:", tools)
        return tools
    except Exception as e:
        logger.error(f"Error listing tools: {str(e)}")
        logger.error(traceback.format_exc())
        raise

if __name__ == "__main__":
    # Run the server with uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)