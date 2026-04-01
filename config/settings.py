from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import os
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Aura GPT"
    DEBUG: bool = False
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000

    # Model Settings
    HF_TOKEN: str = Field(default="", env="HF_TOKEN")
    GPT_MODEL_ID: str = "Qwen/Qwen2.5-3B-Instruct"
    EMOTION_MODEL_ID: str = "bhadresh-savani/distilbert-base-uncased-emotion"

    # Path Settings
    PERSONALITY_CONFIG_PATH: Path = BASE_DIR / "config" / "personality.json"
    MEMORY_DB_PATH: Path = BASE_DIR / "data" / "memory.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate settings
settings = Settings()
