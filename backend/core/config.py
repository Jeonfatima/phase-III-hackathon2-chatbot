import os
from typing import Optional
import logging

class Settings:
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")
    BETTER_AUTH_SECRET: Optional[str] = os.getenv("BETTER_AUTH_SECRET")
    BETTER_AUTH_URL: Optional[str] = os.getenv("BETTER_AUTH_URL")
    JWT_EXPIRATION: str = os.getenv("JWT_EXPIRATION", "24h")  # Default to 24 hours
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    @classmethod
    def validate(cls):
        """Validate that required settings are present"""
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required")

        if not cls.BETTER_AUTH_SECRET:
            raise ValueError("BETTER_AUTH_SECRET environment variable is required")

        # Validate DATABASE_URL format
        if not cls.DATABASE_URL.startswith(('postgresql://', 'postgresql+psycopg2://', 'sqlite:///')):
            logging.warning(f"Unusual DATABASE_URL format: {cls.DATABASE_URL}")

    @classmethod
    def validate_database_url(cls):
        """Specific validation for DATABASE_URL"""
        if not cls.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required")

        # More detailed validation
        if "localhost" in cls.DATABASE_URL or "127.0.0.1" in cls.DATABASE_URL:
            logging.info("Using local database for development")
        elif "postgres" in cls.DATABASE_URL:
            logging.info("Using PostgreSQL database")

settings = Settings()

__all__ = ["settings", "Settings"]