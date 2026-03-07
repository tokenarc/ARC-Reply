"""
Configuration settings for ARC Reply.
Loads environment variables and provides centralized configuration.
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


class Settings:
    """Application settings loaded from environment variables."""

    # Telegram Configuration
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    BOT_ADMIN_ID: Optional[int] = (
        int(os.getenv("BOT_ADMIN_ID")) if os.getenv("BOT_ADMIN_ID") else None
    )

    # TwitterAPI.io Configuration
    TWITTER_API_KEY: str = os.getenv("TWITTER_API_KEY", "")
    TWITTER_API_BASE_URL: str = "https://api.twitter-api.io"
    TWITTER_API_BEARER_TOKEN: str = os.getenv("TWITTER_API_BEARER_TOKEN", "")

    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o")

    # Tesseract Configuration
    TESSERACT_PATH: Optional[str] = os.getenv("TESSERACT_PATH")

    # Bot Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    REQUEST_TIMEOUT: int = 30
    MAX_RETRIES: int = 3

    @classmethod
    def validate(cls) -> None:
        """Validate that all required settings are configured."""
        required_settings = [
            ("TELEGRAM_BOT_TOKEN", cls.TELEGRAM_BOT_TOKEN),
            ("TWITTER_API_KEY", cls.TWITTER_API_KEY),
            ("OPENAI_API_KEY", cls.OPENAI_API_KEY),
        ]

        missing = [name for name, value in required_settings if not value]
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )


# Export settings instance
settings = Settings()
