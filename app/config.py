from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application configuration loaded from .env file."""

    GROQ_API_KEY: str = ""
    
    # Storage paths
    UPLOAD_DIR: str = "uploads"
    MODELS_DIR: str = "models"
    
    # Risk thresholds
    HIGH_RISK_THRESHOLD: float = 0.4
    LOW_RISK_THRESHOLD: float = 0.65

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


@lru_cache()
def get_settings() -> Settings:
    return Settings()
