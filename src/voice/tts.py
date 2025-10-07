"""
Text-to-Speech using Edge TTS (Microsoft).
Converts text to speech with different voice options.
"""

import asyncio
import edge_tts
import numpy as np
import soundfile as sf
import tempfile
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import Config


class EdgeTTS:
    """Text-to-speech using Microsoft Edge TTS with multiple voice options."""

    # Available voices in Edge TTS (English only for simplicity)
    AVAILABLE_VOICES = {
        'af_sky': 'en-US-AvaNeural',  # Warm, conversational female
        'af_bella': 'en-US-JennyNeural',  # Clear, analytical female
        'af_sarah': 'en-GB-SoniaNeural',  # British female
        'am_adam': 'en-US-GuyNeural',  # Conversational male
        'am_michael': 'en-US-DavisNeural',  # Professional male
        'bf_emma': 'en-GB-MaisieNeural',  # British female (child-like but clear)
        'bf_isabella': 'en-GB-LibbyNeural',  # Expressive British female
        'bm_george': 'en-GB-RyanNeural',  # British male
        'bm_lewis': 'en-GB-ThomasNeural',  # British male
    }

    # Reverse mapping for voice descriptions
    VOICE_DESCRIPTIONS = {
        'af_sky': 'Warm conversational female voice',
        'af_bella': 'Clear analytical female voice',
        'af_sarah': 'British female voice',
        'am_adam': 'Conversational male voice',
        'am_michael': 'Professional male voice',
        'bf_emma': 'British female voice',
        'bf_isabella': 'Expressive British female voice',
        'bm_george': 'British male voice',
        'bm_lewis': 'British male voice',
    }

    def __init__(self):
        """Initialize Edge TTS engine."""
        self.sample_rate = Config.AUDIO_SAMPLE_RATE

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
            # Map to Edge TTS voice
            edge_voice = self.AVAILABLE_VOICES[voice]

            # Generate audio using Edge TTS (async)
            audio_file = self._synthesize_sync(text, edge_voice, speed)

            # Load audio file
            audio, sr = sf.read(audio_file)

            # Clean up temp file
            os.remove(audio_file)

            # Resample if needed (Edge TTS outputs at different rates)
            if sr != self.sample_rate:
                import scipy.signal as sps
                num_samples = int(len(audio) * self.sample_rate / sr)
                audio = sps.resample(audio, num_samples)

            return audio

        except Exception as e:
            raise RuntimeError(f"Edge TTS synthesis failed: {str(e)}")

    def _synthesize_sync(self, text: str, voice: str, rate: float) -> str:
        """
        Synchronous wrapper for async Edge TTS synthesis.

        Args:
            text: Text to synthesize
            voice: Edge TTS voice name
            rate: Speech rate (1.0 = normal)

        Returns:
            Path to temporary audio file
        """
        # Create temp file
        fd, temp_path = tempfile.mkstemp(suffix='.mp3')
        os.close(fd)

        # Convert rate to Edge TTS format (+/- percentage)
        rate_str = f"+{int((rate - 1.0) * 100)}%" if rate >= 1.0 else f"{int((rate - 1.0) * 100)}%"

        # Run async synthesis in sync context
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.run_until_complete(self._async_synthesize(text, voice, rate_str, temp_path))

        return temp_path

    async def _async_synthesize(self, text: str, voice: str, rate: str, output_path: str):
        """Async Edge TTS synthesis."""
        communicate = edge_tts.Communicate(text, voice, rate=rate)
        await communicate.save(output_path)

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
        print("Available Edge TTS Voices:")
        print("-" * 50)
        for voice_id, description in EdgeTTS.VOICE_DESCRIPTIONS.items():
            edge_voice = EdgeTTS.AVAILABLE_VOICES[voice_id]
            print(f"  {voice_id:20} - {description:35} ({edge_voice})")

    @staticmethod
    def test_voice(voice: str = 'af_sky', text: str = None):
        """
        Test a specific voice.

        Args:
            voice: Voice ID to test
            text: Text to speak (default: agent introduction)
        """
        if text is None:
            text = "Hello! This is a test of the Edge text-to-speech system."

        print(f"Testing voice: {voice}")
        print(f"Text: {text}")

        try:
            tts = EdgeTTS()
            audio = tts.synthesize(text, voice)

            # Play audio
            from .audio_utils import AudioPlayer
            player = AudioPlayer()
            player.play(audio, blocking=True)

            print(f"✓ Voice test complete for {voice}")

        except Exception as e:
            print(f"✗ Voice test failed: {str(e)}")
