"""
Configuration module for the Digital Twin project.
Centralized configuration for OpenRouter API and model selection.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Central configuration for the Digital Twin CrewAI project."""

    # OpenRouter API Configuration
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_API_BASE: str = os.getenv("OPENROUTER_API_BASE", "https://openrouter.ai/api/v1")

    # Model Configuration - EASILY CHANGEABLE HERE OR IN .env
    # Default to GPT-4 Turbo, but can use any OpenRouter model
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-4-turbo")

    # Optional OpenRouter headers
    YOUR_SITE_URL: Optional[str] = os.getenv("YOUR_SITE_URL", "https://github.com/karlovrancic/digital-twin")
    YOUR_APP_NAME: Optional[str] = os.getenv("YOUR_APP_NAME", "KarloDigitalTwin")

    # CrewAI Configuration
    CREW_VERBOSE: bool = True
    ALLOW_DELEGATION: bool = False  # Agents work independently
    MAX_ITER: int = 5  # Maximum iterations for task completion

    # Output Configuration
    OUTPUT_DIR: str = "outputs"

    @classmethod
    def validate(cls) -> bool:
        """Validate that required configuration is present."""
        if not cls.OPENROUTER_API_KEY:
            raise ValueError(
                "OPENROUTER_API_KEY not found! "
                "Please set it in your .env file. "
                "Copy .env.example to .env and add your API key."
            )
        return True

    @classmethod
    def get_llm_config(cls) -> dict:
        """Get LLM configuration for CrewAI agents."""
        return {
            "model": cls.OPENROUTER_MODEL,
            "api_key": cls.OPENROUTER_API_KEY,
            "base_url": cls.OPENROUTER_API_BASE,
            "default_headers": {
                "HTTP-Referer": cls.YOUR_SITE_URL,
                "X-Title": cls.YOUR_APP_NAME,
            } if cls.YOUR_SITE_URL else {}
        }


# Validate configuration on import
try:
    Config.validate()
except ValueError as e:
    print(f"⚠️  Configuration Error: {e}")
    print("📝 Copy .env.example to .env and add your OpenRouter API key")