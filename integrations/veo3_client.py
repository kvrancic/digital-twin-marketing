import os
import json
import requests
from typing import Dict, List, Optional
from datetime import datetime
import time


class Veo3Client:
    """
    Google Veo3 Fast API client for video generation.
    Handles scene-by-scene video creation from text prompts.
    """

    def __init__(self):
        self.api_key = os.getenv("VEO3_API_KEY", "")
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "")
        self.base_url = "https://videogeneration.googleapis.com/v1"
        self.mock_mode = not bool(self.api_key)

        if self.mock_mode:
            print("⚠️  VEO3 API key not found. Running in mock mode.")
            print("   Set VEO3_API_KEY environment variable to enable actual generation.")

    def generate_scene(self, scene_description: Dict) -> Dict:
        """
        Generate a single video scene from description.
        Returns video URL or mock data.
        """
        if self.mock_mode:
            return self._mock_generation(scene_description)

        endpoint = f"{self.base_url}/projects/{self.project_id}/locations/us-central1/videos:generate"

        prompt = self._build_prompt(scene_description)

        payload = {
            "model": "veo-fast",
            "prompt": prompt,
            "duration": scene_description.get("duration", 6),
            "aspect_ratio": "9:16",
            "resolution": "1080p",
            "style_preset": self._get_style_preset(scene_description),
            "camera_motion": scene_description.get("camera_movement", "static"),
            "generation_config": {
                "temperature": 0.8,
                "top_p": 0.9,
                "guidance_scale": 7.5
            }
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(endpoint, json=payload, headers=headers)
            response.raise_for_status()
            result = response.json()

            return {
                "status": "success",
                "video_url": result.get("videoUrl"),
                "generation_id": result.get("generationId"),
                "scene_id": scene_description.get("scene_id"),
                "processing_time": result.get("processingTime"),
                "metadata": result.get("metadata", {})
            }
        except Exception as e:
            print(f"❌ Veo3 generation failed: {str(e)}")
            return self._mock_generation(scene_description)

    def _build_prompt(self, scene: Dict) -> str:
        """
        Build optimized prompt for Veo3 from scene description.
        """
        base_prompt = scene.get("description", "")

        style_modifiers = []
        if "cinematic" in scene.get("type", "").lower():
            style_modifiers.append("cinematic quality, film grain, anamorphic lens")
        if "funny" in scene.get("type", "").lower():
            style_modifiers.append("comedic timing, exaggerated expressions, vibrant colors")

        lighting = scene.get("lighting", "")
        if lighting:
            style_modifiers.append(f"lighting: {lighting}")

        mood = scene.get("mood", "")
        if mood:
            style_modifiers.append(f"mood: {mood}")

        color_grading = scene.get("color_grading", "")
        if color_grading:
            style_modifiers.append(f"color grading: {color_grading}")

        inspired_by = scene.get("inspired_by", "")
        if inspired_by:
            style_modifiers.append(f"visual style inspired by {inspired_by}")

        full_prompt = base_prompt
        if style_modifiers:
            full_prompt += f" | Style: {', '.join(style_modifiers)}"

        full_prompt += " | High quality, sharp focus, detailed, professional production"

        return full_prompt[:2000]

    def _get_style_preset(self, scene: Dict) -> str:
        """
        Map scene type to Veo3 style presets.
        """
        scene_type = scene.get("type", "").lower()

        style_map = {
            "establishing": "cinematic_wide",
            "character_moment": "portrait_dramatic",
            "action": "dynamic_motion",
            "revelation": "surreal_artistic",
            "climax": "epic_dramatic",
            "setup": "comedy_bright",
            "escalation": "chaotic_energy",
            "twist": "unexpected_surreal",
            "callback": "nostalgic_warm",
            "punchline": "absurdist_comedy"
        }

        return style_map.get(scene_type, "versatile_balanced")

    def _mock_generation(self, scene: Dict) -> Dict:
        """
        Generate mock response for testing without API.
        """
        scene_id = scene.get("scene_id", "unknown")
        mock_id = f"mock_gen_{int(time.time())}_{scene_id}"

        return {
            "status": "mock_success",
            "video_url": f"https://mock-veo3-output.com/videos/{mock_id}.mp4",
            "generation_id": mock_id,
            "scene_id": scene_id,
            "processing_time": "2.3s (mock)",
            "metadata": {
                "prompt_used": self._build_prompt(scene),
                "duration": scene.get("duration", 6),
                "resolution": "1920x1080",
                "fps": 24,
                "codec": "h264",
                "mock_mode": True,
                "actual_generation": "Would generate if API key was present",
                "scene_description": scene.get("description", "No description provided")
            }
        }

    def generate_video_batch(self, scenes: List[Dict]) -> List[Dict]:
        """
        Generate multiple video scenes in batch.
        """
        results = []
        for idx, scene in enumerate(scenes, 1):
            print(f"🎬 Generating scene {idx}/{len(scenes)}...")
            result = self.generate_scene(scene)
            results.append(result)

            if not self.mock_mode and idx < len(scenes):
                time.sleep(2)

        return results

    def check_generation_status(self, generation_id: str) -> Dict:
        """
        Check the status of a video generation job.
        """
        if self.mock_mode:
            return {
                "status": "completed",
                "generation_id": generation_id,
                "progress": 100,
                "estimated_time_remaining": 0
            }

        endpoint = f"{self.base_url}/generations/{generation_id}"

        headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

        try:
            response = requests.get(endpoint, headers=headers)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "generation_id": generation_id
            }

    def download_video(self, video_url: str, output_path: str) -> bool:
        """
        Download generated video to local file.
        """
        if "mock" in video_url:
            print(f"📦 Mock mode: Would download video to {output_path}")
            with open(output_path, "w") as f:
                f.write("MOCK_VIDEO_DATA")
            return True

        try:
            response = requests.get(video_url, stream=True)
            response.raise_for_status()

            with open(output_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"✅ Downloaded video to {output_path}")
            return True
        except Exception as e:
            print(f"❌ Failed to download video: {str(e)}")
            return False