"""
Audio utilities for recording and playback.
Handles microphone input and speaker output.
"""

import sounddevice as sd
import soundfile as sf
import numpy as np
from typing import Optional
import tempfile
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from config import Config


class AudioRecorder:
    """Records audio from microphone with automatic silence detection."""

    def __init__(self,
                 sample_rate: int = Config.AUDIO_SAMPLE_RATE,
                 channels: int = Config.AUDIO_CHANNELS,
                 silence_threshold: float = Config.RECORDING_SILENCE_THRESHOLD,
                 silence_duration: float = Config.RECORDING_SILENCE_DURATION):
        """
        Initialize audio recorder.

        Args:
            sample_rate: Audio sample rate in Hz
            channels: Number of audio channels (1=mono, 2=stereo)
            silence_threshold: RMS threshold below which audio is considered silence
            silence_duration: Seconds of silence before stopping recording
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.silence_threshold = silence_threshold
        self.silence_duration = silence_duration
        self.is_recording = False
        self.audio_data = []

    def record(self, duration: Optional[float] = None, auto_stop: bool = True) -> np.ndarray:
        """
        Record audio from microphone.

        Args:
            duration: Maximum recording duration in seconds (None = unlimited)
            auto_stop: Automatically stop on silence detection

        Returns:
            Numpy array of recorded audio samples
        """
        self.audio_data = []
        self.is_recording = True
        silence_counter = 0

        def callback(indata, frames, time, status):
            if status:
                print(f"Recording status: {status}")

            # Store audio data
            self.audio_data.append(indata.copy())

            # Silence detection
            if auto_stop:
                rms = np.sqrt(np.mean(indata**2))
                if rms < self.silence_threshold:
                    nonlocal silence_counter
                    silence_counter += frames / self.sample_rate
                else:
                    silence_counter = 0

                # Stop if enough silence detected
                if silence_counter >= self.silence_duration:
                    raise sd.CallbackStop()

        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                callback=callback,
                dtype='float32'
            ):
                if duration:
                    sd.sleep(int(duration * 1000))
                else:
                    # Wait until stopped by silence or user interrupt
                    while self.is_recording:
                        sd.sleep(100)

        except (KeyboardInterrupt, sd.CallbackStop):
            pass
        finally:
            self.is_recording = False

        # Concatenate all recorded chunks
        if self.audio_data:
            return np.concatenate(self.audio_data, axis=0)
        else:
            return np.array([])

    def record_to_file(self, output_path: Optional[str] = None, **kwargs) -> str:
        """
        Record audio and save to file.

        Args:
            output_path: Path to save audio file (None = temp file)
            **kwargs: Arguments passed to record()

        Returns:
            Path to saved audio file
        """
        audio = self.record(**kwargs)

        # Create temp file if no path specified
        if output_path is None:
            fd, output_path = tempfile.mkstemp(suffix='.wav')
            os.close(fd)

        # Save audio to file
        sf.write(output_path, audio, self.sample_rate)

        return output_path

    def stop(self):
        """Stop recording."""
        self.is_recording = False

    @staticmethod
    def test_microphone():
        """Test microphone by recording and playing back a short sample."""
        print("Testing microphone... Speak for 3 seconds.")
        recorder = AudioRecorder()
        audio = recorder.record(duration=3, auto_stop=False)

        print(f"Recorded {len(audio)} samples")
        print(f"Duration: {len(audio) / Config.AUDIO_SAMPLE_RATE:.2f} seconds")
        print(f"Max amplitude: {np.max(np.abs(audio)):.4f}")

        if np.max(np.abs(audio)) < 0.001:
            print("⚠️ WARNING: Audio levels very low. Check microphone permissions.")
        else:
            print("✓ Microphone working!")

        return audio


class AudioPlayer:
    """Plays audio through speakers."""

    def __init__(self, sample_rate: int = Config.AUDIO_SAMPLE_RATE):
        """
        Initialize audio player.

        Args:
            sample_rate: Audio sample rate in Hz
        """
        self.sample_rate = sample_rate

    def play(self, audio: np.ndarray, blocking: bool = True):
        """
        Play audio through speakers.

        Args:
            audio: Numpy array of audio samples
            blocking: If True, wait for playback to finish
        """
        sd.play(audio, self.sample_rate)
        if blocking:
            sd.wait()

    def play_file(self, file_path: str, blocking: bool = True):
        """
        Play audio from file.

        Args:
            file_path: Path to audio file
            blocking: If True, wait for playback to finish
        """
        audio, sample_rate = sf.read(file_path)
        sd.play(audio, sample_rate)
        if blocking:
            sd.wait()

    def stop(self):
        """Stop audio playback."""
        sd.stop()

    @staticmethod
    def test_speaker():
        """Test speaker by playing a tone."""
        print("Testing speaker... You should hear a tone.")
        sample_rate = 24000
        duration = 1  # seconds
        frequency = 440  # Hz (A4 note)

        # Generate sine wave
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = 0.3 * np.sin(2 * np.pi * frequency * t)

        player = AudioPlayer(sample_rate)
        player.play(audio, blocking=True)

        print("✓ Speaker test complete!")
