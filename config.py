import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    GEMINI_API_KEY: str = Field(..., validation_alias="GEMINI_API_KEY")
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        extra="ignore"
    )

try:
    settings = Settings()
except Exception:
    # Fallback to manual check to support seamless deployment environments
    if not os.environ.get("GEMINI_API_KEY"):
        raise ValueError("CRITICAL: GEMINI_API_KEY environment variable is missing.")
    settings = Settings(GEMINI_API_KEY=os.environ["GEMINI_API_KEY"])