# Create server parameters for sse connection
from mcp import ClientSession
from mcp.client.sse import sse_client

from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from llm_config import model
import os
import asyncio   
import sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(".env.dev"), override=True)

MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL")

async def talk_with_mcp(query: str):
    async with sse_client(MCP_SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(model, tools)

            # ----------------using the model directly----------------------------
            # agent = model.bind_tools(tools)
            # for message in agent.stream(query):
            #     response = message.content
            #     yield message
                # if (type(response) is list) and (response != []):
                #     yield response[0]['text'] if "text" in message.content[0].keys() else ""
            # --------------------------------------------------------------------
            
            async for message, _ in agent.astream({"messages": query}, stream_mode="messages"):
                if message.content:
                    if (message.type != 'tool_call_chunk') and (not hasattr(message, 'name') or not hasattr(message, 'tool_call_id')):
                        chunk = message.content[0]['text'] if "text" in message.content[0].keys() else ""

                        yield chunk



if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

async def main(query):
    async for msg in talk_with_mcp(query):
        print(msg, end="", flush=True)

if __name__ == "__main__":
    while True:
        query = input("Query: ")
        if query == "end":
            break
        else:
            asyncio.run(main(query))
            print("\n")