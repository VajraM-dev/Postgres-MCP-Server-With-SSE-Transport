from mcp.server.fastmcp import FastMCP
from pg_connect import conn
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(".env.dev"), override=True)

if conn is None:
    print("Unable to connect to Postgres")
    exit()

MCP_NAME = os.environ.get("MCP_NAME")
MCP_HOST = os.environ.get("MCP_HOST")
MCP_PORT = int(os.environ.get("MCP_PORT"))

app = FastMCP(name=MCP_NAME,
              host=MCP_HOST,
              port=MCP_PORT
              )

@app.tool()
def list_tables():
    """
    Retrieve all base tables in non-system schemas.

    Args:
        conn (psycopg.Connection): Active database connection.

    Returns:
        list[dict]: A list of dictionaries containing schema and table names.
    """
    with conn.cursor() as cur:
        cur.execute("""
            SELECT table_schema, table_name 
            FROM information_schema.tables 
            WHERE table_type='BASE TABLE' AND table_schema NOT IN ('pg_catalog', 'information_schema');
        """)
        return cur.fetchall()

TRANSPORT = os.environ.get("TRANSPORT")
if __name__ == "__main__":
    # Initialize and run the server
    print("MCP Server Started")
    app.run(transport=TRANSPORT)