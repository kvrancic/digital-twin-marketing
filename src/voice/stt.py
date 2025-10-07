"""
Speech-to-Text using OpenAI Whisper API.
Converts audio input to text transcription.
"""

from openai import OpenAI
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import Config


class WhisperSTT:
    """Speech-to-text using OpenAI's Whisper API."""

    def __init__(self, api_key: str = None):
        """
        Initialize Whisper STT client.

        Args:
            api_key: OpenAI API key (defaults to Config.OPENAI_API_KEY)
        """
        self.api_key = api_key or Config.OPENAI_API_KEY

        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found! "
                "Please set OPENAI_API_KEY in your .env file."
            )

        self.client = OpenAI(api_key=self.api_key)

    def transcribe(self, audio_file_path: str, language: str = "en") -> str:
        """
        Transcribe audio file to text.

        Args:
            audio_file_path: Path to audio file (mp3, mp4, wav, etc.)
            language: Language code (e.g., "en" for English)

        Returns:
            Transcribed text
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    response_format="text"
                )

            return transcript.strip()

        except Exception as e:
            raise RuntimeError(f"Whisper transcription failed: {str(e)}")

    def transcribe_with_timestamps(self, audio_file_path: str, language: str = "en") -> dict:
        """
        Transcribe audio with word-level timestamps.

        Args:
            audio_file_path: Path to audio file
            language: Language code

        Returns:
            Dictionary with text and timestamps
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language=language,
                    response_format="verbose_json",
                    timestamp_granularities=["word"]
                )

            return {
                "text": transcript.text,
                "duration": transcript.duration,
                "words": transcript.words if hasattr(transcript, 'words') else []
            }

        except Exception as e:
            raise RuntimeError(f"Whisper transcription failed: {str(e)}")

    @staticmethod
    def validate_config() -> bool:
        """
        Validate that OpenAI API key is configured.

        Returns:
            True if configured, raises ValueError otherwise
        """
        if not Config.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY not found! "
                "Please add it to your .env file for voice capabilities."
            )
        return True
