"""
Core configuration settings for the application.
Uses pydantic-settings for environment variable management.
"""
import os
from functools import lru_cache
from typing import Literal

class Settings:
    """Application settings loaded from environment variables"""
    
    # Environment
    ENVIRONMENT: Literal["development", "production"] = os.getenv("ENVIRONMENT", "development")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    # API
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "OOP Resource Hub API"
    
    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://your-frontend-domain.vercel.app",
    ]
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 100
    MAX_PAGE_SIZE: int = 1000
    
    def __init__(self):
        # Require DATABASE_URL in production
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable is required!")
            
        # Convert postgres:// to postgresql:// for SQLAlchemy 2.0
        if self.DATABASE_URL.startswith("postgres://"):
            self.DATABASE_URL = self.DATABASE_URL.replace("postgres://", "postgresql://", 1)

@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance.
    Use this function to get settings throughout the app.
    """
    return Settings()
