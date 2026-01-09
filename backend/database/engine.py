from sqlmodel import create_engine
import os
from typing import Generator
from sqlalchemy import text
from sqlalchemy.pool import QueuePool

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todoapp.db")

# Create the database engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=True,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300
)

def get_engine():
    return engine

def validate_database_connection():
    """Validate that the database connection is working"""
    try:
        with engine.connect() as connection:
            # Test the connection with a simple query
            result = connection.execute(text("SELECT 1"))
            return True
    except Exception as e:
        print(f"Database connection validation failed: {e}")
        return False

__all__ = ["engine", "get_engine", "validate_database_connection"]