"""
Text-to-Speech using Kokoro TTS.
Converts text to speech with different voice options.
"""

import numpy as np
import tempfile
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import Config

try:
    from kokoro_onnx import Kokoro
except ImportError:
    Kokoro = None


class KokoroTTS:
    """Text-to-speech using Kokoro TTS with multiple voice options."""

    # Available voices in Kokoro
    AVAILABLE_VOICES = {
        'af_sky': 'Deep contemplative female voice',
        'af_bella': 'Analytical female voice',
        'af_sarah': 'Clear female voice',
        'am_adam': 'Dry sardonic male voice',
        'am_michael': 'Professional male voice',
        'bf_emma': 'British female voice',
        'bf_isabella': 'Expressive British female voice',
        'bm_george': 'British male voice',
        'bm_lewis': 'British male voice',
    }

    def __init__(self):
        """Initialize Kokoro TTS engine."""
        if Kokoro is None:
            raise ImportError(
                "Kokoro TTS not installed! "
                "Install with: pip install kokoro-onnx"
            )

        try:
            # Initialize Kokoro model
            self.engine = Kokoro()
            self.sample_rate = Config.AUDIO_SAMPLE_RATE
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Kokoro TTS: {str(e)}")

    def synthesize(self, text: str, voice: str = 'af_sky', speed: float = 1.0) -> np.ndarray:
        """
        Convert text to speech audio.

        Args:
            text: Text to synthesize
            voice: Voice ID (see AVAILABLE_VOICES)
            speed: Speech speed multiplier (1.0 = normal)

        Returns:
            Numpy array of audio samples
        """
        if voice not in self.AVAILABLE_VOICES:
            raise ValueError(
                f"Invalid voice: {voice}. "
                f"Available voices: {list(self.AVAILABLE_VOICES.keys())}"
            )

        try:
            # Generate audio using Kokoro
            audio, _ = self.engine.create(
                text=text,
                voice=voice,
                speed=speed,
                lang='en-us'
            )

            return audio

        except Exception as e:
            raise RuntimeError(f"Kokoro synthesis failed: {str(e)}")

    def synthesize_to_file(self, text: str, voice: str = 'af_sky',
                          output_path: str = None, speed: float = 1.0) -> str:
        """
        Convert text to speech and save to file.

        Args:
            text: Text to synthesize
            voice: Voice ID
            output_path: Output file path (None = temp file)
            speed: Speech speed multiplier

        Returns:
            Path to audio file
        """
        audio = self.synthesize(text, voice, speed)

        # Create temp file if no path specified
        if output_path is None:
            fd, output_path = tempfile.mkstemp(suffix='.wav')
            os.close(fd)

        # Save audio to file
        import soundfile as sf
        sf.write(output_path, audio, self.sample_rate)

        return output_path

    def get_agent_voice(self, agent_name: str) -> str:
        """
        Get the configured voice for a specific agent.

        Args:
            agent_name: Agent name (philosopher, architect, optimizer)

        Returns:
            Voice ID for the agent
        """
        voice_map = {
            'philosopher': Config.KOKORO_VOICE_PHILOSOPHER,
            'architect': Config.KOKORO_VOICE_ARCHITECT,
            'optimizer': Config.KOKORO_VOICE_OPTIMIZER,
        }

        return voice_map.get(agent_name.lower(), 'af_sky')

    def speak_as_agent(self, text: str, agent_name: str, speed: float = 1.0) -> np.ndarray:
        """
        Synthesize speech for a specific agent using their configured voice.

        Args:
            text: Text to speak
            agent_name: Agent name (philosopher, architect, optimizer)
            speed: Speech speed multiplier

        Returns:
            Audio array
        """
        voice = self.get_agent_voice(agent_name)
        return self.synthesize(text, voice, speed)

    @staticmethod
    def list_voices():
        """Print available voices with descriptions."""
        print("Available Kokoro TTS Voices:")
        print("-" * 50)
        for voice_id, description in KokoroTTS.AVAILABLE_VOICES.items():
            print(f"  {voice_id:20} - {description}")

    @staticmethod
    def test_voice(voice: str = 'af_sky', text: str = None):
        """
        Test a specific voice.

        Args:
            voice: Voice ID to test
            text: Text to speak (default: agent introduction)
        """
        if text is None:
            text = "Hello! This is a test of the Kokoro text-to-speech system."

        print(f"Testing voice: {voice}")
        print(f"Text: {text}")

        try:
            tts = KokoroTTS()
            audio = tts.synthesize(text, voice)

            # Play audio
            from .audio_utils import AudioPlayer
            player = AudioPlayer()
            player.play(audio, blocking=True)

            print(f"✓ Voice test complete for {voice}")

        except Exception as e:
            print(f"✗ Voice test failed: {str(e)}")
