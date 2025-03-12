from pydantic_settings import BaseSettings

import os


class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "development")  # Default to development
    DEBUG: bool = ENV == "development"

    DATABASE_URL: str = os.getenv("DATABASE_URL")

    class Config:
        env_file = ".env"  # Load environment variables from .env file


settings = Settings()
