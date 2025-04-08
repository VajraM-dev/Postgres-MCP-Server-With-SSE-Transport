"""
MCP Client with Server-Sent Events (SSE)

This script establishes a connection to an MCP (Machine Control Protocol) server using SSE,
allowing real-time communication with language models through LangChain and LangGraph.

Features:
- Connects to an MCP server via SSE for streaming responses
- Uses LangChain and LangGraph for agent creation and execution
- Supports streaming responses for better user experience
- Compatible with both Windows and non-Windows platforms

Requirements:
- mcp library for client sessions and SSE handling
- langchain_mcp_adapters for tool loading
- langgraph for agent creation
- dotenv for environment variable management
- asyncio for asynchronous operations

Usage:
1. Set up your .env.dev file with MCP_SERVER_URL
2. Run the script
3. Enter queries when prompted
4. Type "end" to exit
"""

from mcp import ClientSession
from mcp.client.sse import sse_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from llm_config import model  # Assumes you have a configuration file for your language model
import os
import asyncio   
import sys
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env.dev file
load_dotenv(find_dotenv(".env.dev"), override=True)

# Get the MCP server URL from environment variables
MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL")

async def talk_with_mcp(query: str):
    """
    Establishes a connection with the MCP server and streams responses for a given query.
    
    Args:
        query (str): The user's query to process
        
    Yields:
        str: Chunks of the model's response as they become available
    """
    # Create SSE client connection to the server
    async with sse_client(MCP_SERVER_URL) as (read, write):
        # Create a client session using the SSE connection
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get available tools from the MCP server
            tools = await load_mcp_tools(session)

            # Create a ReAct agent using the specified model and tools
            agent = create_react_agent(model, tools)
            
            # Alternative approach using direct model binding (commented out)
            # -----------------using the model directly----------------------------
            # agent = model.bind_tools(tools)
            # for message in agent.stream(query):
            #     response = message.content
            #     yield message
            #     # if (type(response) is list) and (response != []):
            #     #     yield response[0]['text'] if "text" in message.content[0].keys() else ""
            # --------------------------------------------------------------------
            
            # Stream the agent's responses
            async for message, _ in agent.astream({"messages": query}, stream_mode="messages"):
                if message.content:
                    # Filter out tool call chunks and only process text responses
                    if (message.type != 'tool_call_chunk') and (not hasattr(message, 'name') or not hasattr(message, 'tool_call_id')):
                        # Extract the text content from the message
                        chunk = message.content[0]['text'] if "text" in message.content[0].keys() else ""
                        yield chunk


# Fix for Windows event loop policy
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main(query):
    """
    Main function to process a query and print the streamed response.
    
    Args:
        query (str): The user's query to process
    """
    async for msg in talk_with_mcp(query):
        print(msg, end="", flush=True)  # Print each chunk without newlines, flushing output buffer

if __name__ == "__main__":
    print("=== MCP Client Interface ===")
    print("Type your queries and press Enter. Type 'end' to exit.")
    print("-" * 30)
    
    # Main interaction loop
    while True:
        query = input("Query: ")
        if query.lower() == "end":
            print("Exiting MCP client. Goodbye!")
            break
        else:
            asyncio.run(main(query))
            print("\n")  # Add spacing between responses