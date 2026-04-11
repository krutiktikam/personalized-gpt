from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Aura GPT"
    DEBUG: bool = False
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8000

    # JWT Settings
    SECRET_KEY: str = "your-secret-key-here-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database Settings
    PSQL_USER: str = "aura_user"
    PSQL_PASSWORD: str = "aura_password"
    PSQL_HOST: str = "localhost"
    PSQL_PORT: int = 5432
    PSQL_DB: str = "aura_db"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.PSQL_USER}:{self.PSQL_PASSWORD}@{self.PSQL_HOST}:{self.PSQL_PORT}/{self.PSQL_DB}"

    # Model Settings
    HF_TOKEN: str = Field(default="", validation_alias="HF_TOKEN")
    GPT_MODEL_ID: str = "qwen2.5:1.5b" 
    EMOTION_MODEL_ID: str = "bhadresh-savani/distilbert-base-uncased-emotion"
    OLLAMA_HOST: str = "http://localhost:11434"

    # Path Settings
    PERSONALITY_CONFIG_PATH: Path = BASE_DIR / "config" / "personality.json"
    MEMORY_DB_PATH: Path = BASE_DIR / "data" / "memory.db"
    LOG_FILE: Path = BASE_DIR / "logs" / "aura.log"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate settings
settings = Settings()

print(f"DEBUG: Loaded settings from {__file__}")
print(f"DEBUG: OLLAMA_HOST is {settings.OLLAMA_HOST}")
print(f"DEBUG: GPT_MODEL_ID is {settings.GPT_MODEL_ID}")
print(f"DEBUG: API_PORT is {settings.API_PORT}")
