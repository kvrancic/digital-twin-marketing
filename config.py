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

    # Separate models for different task complexities
    LITE_MODEL: str = os.getenv("OPENROUTER_LITE_MODEL", "google/gemini-2.5-flash-lite")  # For simple tasks
    PRO_MODEL: str = os.getenv("OPENROUTER_PRO_MODEL", "google/gemini-2.5-pro")   # For complex tasks

    # Optional OpenRouter headers
    YOUR_SITE_URL: Optional[str] = os.getenv("YOUR_SITE_URL", "https://github.com/karlovrancic/digital-twin")
    YOUR_APP_NAME: Optional[str] = os.getenv("YOUR_APP_NAME", "KarloDigitalTwin")

    # CrewAI Configuration
    CREW_VERBOSE: bool = True
    ALLOW_DELEGATION: bool = False  # Agents work independently
    MAX_ITER: int = 5  # Maximum iterations for task completion

    # Output Configuration
    OUTPUT_DIR: str = "outputs"

    # Voice Configuration (HW4)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")  # For Whisper STT

    # Kokoro TTS Voice IDs for each agent
    KOKORO_VOICE_PHILOSOPHER: str = os.getenv("KOKORO_VOICE_PHILOSOPHER", "af_sky")
    KOKORO_VOICE_ARCHITECT: str = os.getenv("KOKORO_VOICE_ARCHITECT", "am_adam")
    KOKORO_VOICE_OPTIMIZER: str = os.getenv("KOKORO_VOICE_OPTIMIZER", "bf_emma")

    # Audio Configuration
    AUDIO_SAMPLE_RATE: int = 24000  # 24kHz for Kokoro
    AUDIO_CHANNELS: int = 1  # Mono
    RECORDING_SILENCE_THRESHOLD: float = 0.01  # Silence detection threshold
    RECORDING_SILENCE_DURATION: float = 2.0  # Seconds of silence to stop recording

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
    def get_llm_config(cls, use_lite: bool = False) -> dict:
        """
        Get LLM configuration for CrewAI agents.

        Args:
            use_lite: If True, use the lite model for simple tasks
        """
        model = cls.LITE_MODEL if use_lite else cls.PRO_MODEL

        return {
            "model": model,
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