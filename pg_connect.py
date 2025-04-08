import os
import psycopg2
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env.dev file
# Override existing environment variables if they exist
load_dotenv(find_dotenv(".env.dev"), override=True)

# Retrieve database connection parameters from environment variables
# This approach keeps sensitive credentials out of the code
POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB_NAME = os.environ.get("POSTGRES_DB_NAME")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

# Database connection configuration dictionary
# Contains all necessary parameters to establish a PostgreSQL connection
DB_CONFIG = {
    "dbname": POSTGRES_DB_NAME,    # Name of the database
    "user": POSTGRES_USERNAME,     # PostgreSQL username
    "password": POSTGRES_PASSWORD, # PostgreSQL password
    "host": POSTGRES_HOST,         # Database host (localhost or IP address)
    "port": POSTGRES_PORT          # PostgreSQL port number
}

def establish_database_connection():
    """
    Establishes a connection to a PostgreSQL database.

    This function attempts to create a database connection using the 
    predefined DB_CONFIG parameters. It handles potential connection 
    errors and provides informative feedback.

    Returns:
        psycopg2.connection: An active database connection if successful
        None: If connection fails

    Raises:
        Exception: If there are any connection-related issues
    """
    conn = None
    try:
        # Attempt to connect to the PostgreSQL database
        conn = psycopg2.connect(**DB_CONFIG)
        print("Postgres connected successfully")
        return conn
    except Exception as e:
        # Catch and print any connection errors
        print("Postgres connection error: ", e)
        return None

# Usage Notes:
# 1. Ensure you have a .env.dev file with the following variables:
#    POSTGRES_USERNAME, POSTGRES_PASSWORD, POSTGRES_DB_NAME, 
#    POSTGRES_HOST, POSTGRES_PORT
#
# 2. Install required libraries:
#    pip install psycopg2 python-dotenv
#
# 3. Example of how to use this connection:
#    connection = establish_database_connection()
#    if connection:
#        # Perform database operations
#        cursor = connection.cursor()
#        # Execute queries, etc.
#        connection.close()