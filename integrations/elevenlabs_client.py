import os
import json
import requests
from typing import Dict, List, Optional, Union
from datetime import datetime
import time
import base64


class ElevenLabsClient:
    """
    ElevenLabs API client for voice synthesis and sound effects.
    Handles voiceover generation, dialogue, and sound design.
    """

    def __init__(self):
        self.api_key = os.getenv("ELEVENLABS_API_KEY", "")
        self.base_url = "https://api.elevenlabs.io/v1"
        self.mock_mode = not bool(self.api_key)

        if self.mock_mode:
            print("⚠️  ElevenLabs API key not found. Running in mock mode.")
            print("   Set ELEVENLABS_API_KEY environment variable to enable actual generation.")

        self.voice_map = {
            "existential_narrator": "21m00Tcm4TlvDq8ikWAM",
            "gen_z_entrepreneur": "AZnzlk1XvdvUeBnXmlld",
            "confused_millennial": "EXAVITQu4vr4xnSDxMaL",
            "corporate_overlord": "ErXwobaYiN019PkySvjV",
            "therapy_voice": "MF3mGyEYCl7XYWbV9V6O",
            "hype_beast": "TxGEqnHWrfWFTfGW9XjX",
            "philosophy_bro": "VR6AewLTigWG4xSOukaG",
            "karen_energy": "pNInz6obpgDQGcFmaJgB",
            "zoomer_chaos": "yoZ06aMxZJJ28mfd3POQ"
        }

    def generate_voiceover(self, text: str, voice: str = "existential_narrator",
                          emotion: str = "neutral") -> Dict:
        """
        Generate voiceover from text using specified voice and emotion.
        """
        if self.mock_mode:
            return self._mock_voiceover(text, voice, emotion)

        voice_id = self.voice_map.get(voice, voice)

        endpoint = f"{self.base_url}/text-to-speech/{voice_id}"

        payload = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": self._get_stability(emotion),
                "similarity_boost": 0.85,
                "style": self._get_style(emotion),
                "use_speaker_boost": True
            }
        }

        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()

            audio_data = response.content

            timestamp = int(time.time())
            filename = f"voiceover_{voice}_{timestamp}.mp3"

            return {
                "status": "success",
                "audio_data": base64.b64encode(audio_data).decode(),
                "filename": filename,
                "duration": self._estimate_duration(text),
                "voice_used": voice,
                "emotion": emotion,
                "text": text
            }
        except Exception as e:
            print(f"❌ ElevenLabs generation failed: {str(e)}")
            return self._mock_voiceover(text, voice, emotion)

    def generate_dialogue(self, dialogue_entries: List[Dict]) -> List[Dict]:
        """
        Generate multiple dialogue clips with different voices.
        """
        results = []

        for entry in dialogue_entries:
            character = entry.get("character", "narrator")
            text = entry.get("text", "")
            delivery = entry.get("delivery", "neutral")

            voice = self._map_character_to_voice(character)

            result = self.generate_voiceover(text, voice, delivery)
            result["character"] = character
            result["time_marker"] = entry.get("time", "00:00")

            results.append(result)

            if not self.mock_mode:
                time.sleep(0.5)

        return results

    def generate_sound_effects(self, description: str, duration: float = 2.0) -> Dict:
        """
        Generate sound effects using ElevenLabs sound generation.
        """
        if self.mock_mode:
            return self._mock_sound_effect(description, duration)

        endpoint = f"{self.base_url}/sound-generation"

        payload = {
            "text": description,
            "duration_seconds": duration
        }

        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()

            result = response.json()

            return {
                "status": "success",
                "audio_url": result.get("audio_url"),
                "effect_id": result.get("effect_id"),
                "description": description,
                "duration": duration
            }
        except Exception as e:
            print(f"❌ Sound effect generation failed: {str(e)}")
            return self._mock_sound_effect(description, duration)

    def process_full_script(self, script: Dict) -> Dict:
        """
        Process a complete video script with all audio elements.
        """
        output = {
            "timestamp": datetime.now().isoformat(),
            "script_title": script.get("title", "Untitled"),
            "voiceover_tracks": [],
            "dialogue_tracks": [],
            "sound_effects": [],
            "processing_log": []
        }

        print("🎙️ Processing voiceover tracks...")
        for vo in script.get("voiceover_track", []):
            result = self.generate_voiceover(
                vo.get("text", ""),
                vo.get("voice", "existential_narrator"),
                vo.get("emotion", "neutral")
            )
            result["time_range"] = vo.get("time", "00:00")
            output["voiceover_tracks"].append(result)
            output["processing_log"].append(f"Generated voiceover for {vo.get('time', 'unknown')}")

        print("💬 Processing dialogue tracks...")
        dialogue_results = self.generate_dialogue(script.get("dialogue_track", []))
        output["dialogue_tracks"] = dialogue_results

        print("🔊 Processing sound effects...")
        for sfx in script.get("sound_effects", []):
            result = self.generate_sound_effects(
                sfx.get("effect", "generic sound"),
                duration=2.0
            )
            result["time_marker"] = sfx.get("time", "00:00")
            result["volume"] = sfx.get("volume", 50)
            output["sound_effects"].append(result)
            output["processing_log"].append(f"Generated SFX: {sfx.get('effect', 'unknown')}")

        output["summary"] = {
            "total_voiceover_clips": len(output["voiceover_tracks"]),
            "total_dialogue_clips": len(output["dialogue_tracks"]),
            "total_sound_effects": len(output["sound_effects"]),
            "processing_status": "complete" if not self.mock_mode else "mock_complete"
        }

        return output

    def _get_stability(self, emotion: str) -> float:
        """
        Map emotion to voice stability parameter.
        """
        emotion_stability = {
            "neutral": 0.75,
            "excited": 0.5,
            "calm": 0.9,
            "chaotic": 0.3,
            "dramatic": 0.6,
            "deadpan": 0.95,
            "manic": 0.2,
            "resigned": 0.8
        }
        return emotion_stability.get(emotion.lower(), 0.75)

    def _get_style(self, emotion: str) -> str:
        """
        Map emotion to voice style.
        """
        emotion_style = {
            "neutral": "news",
            "excited": "entertainment",
            "calm": "meditation",
            "chaotic": "sports_commentary",
            "dramatic": "documentary",
            "deadpan": "news",
            "manic": "advertisement",
            "resigned": "audiobook"
        }
        return emotion_style.get(emotion.lower(), "news")

    def _map_character_to_voice(self, character: str) -> str:
        """
        Map character names to voice IDs.
        """
        character_lower = character.lower()

        if "person 1" in character_lower or "background" in character_lower:
            return "confused_millennial"
        elif "person 2" in character_lower:
            return "gen_z_entrepreneur"
        elif "child" in character_lower:
            return "zoomer_chaos"
        elif "mother" in character_lower or "parent" in character_lower:
            return "karen_energy"
        elif "narrator" in character_lower:
            return "existential_narrator"
        else:
            return "philosophy_bro"

    def _estimate_duration(self, text: str) -> float:
        """
        Estimate audio duration based on text length.
        Assumes ~150 words per minute speaking rate.
        """
        words = len(text.split())
        minutes = words / 150
        return round(minutes * 60, 1)

    def _mock_voiceover(self, text: str, voice: str, emotion: str) -> Dict:
        """
        Generate mock voiceover response for testing.
        """
        mock_id = f"mock_vo_{int(time.time())}"

        return {
            "status": "mock_success",
            "audio_data": base64.b64encode(f"MOCK_AUDIO_{text[:20]}".encode()).decode(),
            "filename": f"mock_{voice}_{mock_id}.mp3",
            "duration": self._estimate_duration(text),
            "voice_used": voice,
            "emotion": emotion,
            "text": text,
            "mock_mode": True,
            "actual_generation": "Would generate audio if API key was present"
        }

    def _mock_sound_effect(self, description: str, duration: float) -> Dict:
        """
        Generate mock sound effect response.
        """
        mock_id = f"mock_sfx_{int(time.time())}"

        return {
            "status": "mock_success",
            "audio_url": f"https://mock-elevenlabs.com/sfx/{mock_id}.mp3",
            "effect_id": mock_id,
            "description": description,
            "duration": duration,
            "mock_mode": True,
            "actual_generation": f"Would generate {description} sound for {duration}s"
        }

    def save_audio_file(self, audio_data: str, filepath: str) -> bool:
        """
        Save base64 audio data to file.
        """
        try:
            audio_bytes = base64.b64decode(audio_data)
            with open(filepath, "wb") as f:
                f.write(audio_bytes)
            print(f"✅ Saved audio to {filepath}")
            return True
        except Exception as e:
            print(f"❌ Failed to save audio: {str(e)}")
            return False