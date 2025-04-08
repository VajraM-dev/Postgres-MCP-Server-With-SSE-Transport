import os
from dotenv import load_dotenv, find_dotenv
from mcp.server.fastmcp import FastMCP
from pg_connect import conn  # Import database connection from another module

# Load environment variables from .env.dev file
# Override existing environment variables if they exist
load_dotenv(find_dotenv(".env.dev"), override=True)

# Validate database connection
if conn is None:
    print("Unable to connect to Postgres")
    exit()

# Retrieve MCP (Message Control Protocol) server configuration from environment variables
# This approach keeps configuration flexible and secure
MCP_NAME = os.environ.get("MCP_NAME")      # Name of the MCP server
MCP_HOST = os.environ.get("MCP_HOST")      # Host address for the MCP server
MCP_PORT = int(os.environ.get("MCP_PORT")) # Port number for the MCP server

def create_mcp_server():
    """
    Create and configure a FastMCP server instance.

    Initializes the MCP server with predefined configuration 
    from environment variables.

    Returns:
        FastMCP: Configured MCP server instance
    """
    return FastMCP(
        name=MCP_NAME,
        host=MCP_HOST,
        port=MCP_PORT
    )

# Initialize the MCP server
app = create_mcp_server()

@app.tool()
def list_tables():
    """
    Retrieve all base tables in non-system schemas from the PostgreSQL database.

    This tool provides a comprehensive list of user-created tables across 
    different schemas, excluding system-level schemas.

    Returns:
        list[tuple]: A list of tuples containing (schema_name, table_name)
    
    Notes:
        - Excludes tables from 'pg_catalog' and 'information_schema'
        - Uses an active database connection to query table information
    """
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_schema, table_name 
                FROM information_schema.tables 
                WHERE table_type='BASE TABLE' 
                AND table_schema NOT IN ('pg_catalog', 'information_schema');
            """)
            return cur.fetchall()
    except Exception as e:
        print(f"Error retrieving tables: {e}")
        return []

def main():
    """
    Main entry point for the MCP server application.

    Configures and starts the MCP server using the specified transport method.
    """
    # Retrieve transport method from environment variables
    TRANSPORT = os.environ.get("TRANSPORT")
    
    try:
        print("MCP Server Started")
        app.run(transport=TRANSPORT)
    except Exception as e:
        print(f"Failed to start MCP server: {e}")

# Ensure the main function is only called when the script is run directly
if __name__ == "__main__":
    main()

# Usage Notes:
# 1. Ensure you have a .env.dev file with the following variables:
#    - MCP_NAME: Name of the MCP server
#    - MCP_HOST: Host address for the server
#    - MCP_PORT: Port number for the server
#    - TRANSPORT: Communication transport method
#
# 2. Prerequisites:
#    - Properly configured database connection (pg_connect module)
#    - Required libraries installed (FastMCP, psycopg2, python-dotenv)
#
# 3. Configuration Tips:
#    - Keep sensitive information in .env files
#    - Use environment-specific configurations
#    - Implement proper error handling