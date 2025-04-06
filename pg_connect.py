import os
import psycopg2

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(".env.dev"), override=True)

POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB_NAME = os.environ.get("POSTGRES_DB_NAME")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")

# Database connection parameters
DB_CONFIG = {
    "dbname": POSTGRES_DB_NAME,
    "user": POSTGRES_USERNAME,
    "password": POSTGRES_PASSWORD,
    "host": POSTGRES_HOST,  # e.g., "localhost" or "127.0.0.1"
    "port": POSTGRES_PORT  # Change if using a different port
}

conn = None
try:
    conn = psycopg2.connect(**DB_CONFIG)
    print("Postgres connected successfully")
except Exception as e:
    print("Postgres connection error: ", e)