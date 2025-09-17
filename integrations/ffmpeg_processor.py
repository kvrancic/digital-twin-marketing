import os
import json
import subprocess
from typing import Dict, List, Optional
from datetime import datetime
import tempfile
import shutil


class FFmpegProcessor:
    """
    FFmpeg wrapper for video processing and stitching.
    Handles scene compilation, audio mixing, and final output.
    """

    def __init__(self):
        self.ffmpeg_path = self._find_ffmpeg()
        self.mock_mode = not bool(self.ffmpeg_path)

        if self.mock_mode:
            print("⚠️  FFmpeg not found. Running in mock mode.")
            print("   Install FFmpeg: brew install ffmpeg")

    def _find_ffmpeg(self) -> Optional[str]:
        """
        Find FFmpeg executable on the system.
        """
        try:
            result = subprocess.run(
                ["which", "ffmpeg"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass

        common_paths = [
            "/usr/local/bin/ffmpeg",
            "/usr/bin/ffmpeg",
            "/opt/homebrew/bin/ffmpeg"
        ]

        for path in common_paths:
            if os.path.exists(path):
                return path

        return None

    def stitch_scenes(self, video_files: List[str], output_path: str,
                     transition: str = "fade") -> Dict:
        """
        Stitch multiple video scenes together with transitions.
        """
        if self.mock_mode:
            return self._mock_stitch(video_files, output_path)

        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                for video in video_files:
                    f.write(f"file '{video}'\n")
                concat_file = f.name

            cmd = [
                self.ffmpeg_path,
                "-f", "concat",
                "-safe", "0",
                "-i", concat_file,
                "-c", "copy",
                "-y",
                output_path
            ]

            if transition == "fade":
                cmd = self._add_fade_transitions(video_files, output_path)

            result = subprocess.run(cmd, capture_output=True, text=True)

            os.unlink(concat_file)

            if result.returncode == 0:
                return {
                    "status": "success",
                    "output_file": output_path,
                    "duration": self._get_duration(output_path),
                    "file_size": os.path.getsize(output_path)
                }
            else:
                return {
                    "status": "error",
                    "error": result.stderr
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def add_audio_track(self, video_file: str, audio_file: str,
                       output_path: str, audio_level: float = 0.8) -> Dict:
        """
        Add audio track to video file.
        """
        if self.mock_mode:
            return self._mock_audio_add(video_file, audio_file, output_path)

        try:
            cmd = [
                self.ffmpeg_path,
                "-i", video_file,
                "-i", audio_file,
                "-c:v", "copy",
                "-c:a", "aac",
                "-filter_complex",
                f"[1:a]volume={audio_level}[a1];[0:a][a1]amix=inputs=2:duration=first",
                "-y",
                output_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                return {
                    "status": "success",
                    "output_file": output_path,
                    "audio_added": audio_file
                }
            else:
                return {
                    "status": "error",
                    "error": result.stderr
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def mix_audio_layers(self, base_video: str, audio_layers: List[Dict],
                        output_path: str) -> Dict:
        """
        Mix multiple audio layers (voiceover, sfx, music) onto video.
        """
        if self.mock_mode:
            return self._mock_audio_mix(base_video, audio_layers, output_path)

        try:
            inputs = ["-i", base_video]
            filter_parts = []
            audio_inputs = []

            for idx, layer in enumerate(audio_layers, 1):
                inputs.extend(["-i", layer["file"]])
                volume = layer.get("volume", 100) / 100
                delay = self._time_to_ms(layer.get("start_time", "00:00"))

                if delay > 0:
                    filter_parts.append(f"[{idx}:a]adelay={delay}|{delay}[a{idx}]")
                    audio_inputs.append(f"[a{idx}]")
                else:
                    audio_inputs.append(f"[{idx}:a]")

            if len(audio_inputs) > 0:
                filter_complex = ";".join(filter_parts) if filter_parts else ""
                if filter_complex:
                    filter_complex += ";"
                filter_complex += f"{''.join(audio_inputs)}amix=inputs={len(audio_inputs)}:duration=first[aout]"

                cmd = [
                    self.ffmpeg_path,
                    *inputs,
                    "-filter_complex", filter_complex,
                    "-map", "0:v",
                    "-map", "[aout]",
                    "-c:v", "copy",
                    "-c:a", "aac",
                    "-y",
                    output_path
                ]

                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode == 0:
                    return {
                        "status": "success",
                        "output_file": output_path,
                        "audio_layers_mixed": len(audio_layers)
                    }
                else:
                    return {
                        "status": "error",
                        "error": result.stderr
                    }
            else:
                shutil.copy(base_video, output_path)
                return {
                    "status": "success",
                    "output_file": output_path,
                    "note": "No audio layers to mix"
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def add_text_overlay(self, video_file: str, text: str, position: str,
                        output_path: str, font_size: int = 48) -> Dict:
        """
        Add text overlay to video.
        """
        if self.mock_mode:
            return self._mock_text_overlay(video_file, text, output_path)

        position_map = {
            "top": "x=(w-text_w)/2:y=50",
            "center": "x=(w-text_w)/2:y=(h-text_h)/2",
            "bottom": "x=(w-text_w)/2:y=h-text_h-50",
            "top_left": "x=50:y=50",
            "top_right": "x=w-text_w-50:y=50",
            "bottom_left": "x=50:y=h-text_h-50",
            "bottom_right": "x=w-text_w-50:y=h-text_h-50"
        }

        pos = position_map.get(position, position_map["center"])

        try:
            cmd = [
                self.ffmpeg_path,
                "-i", video_file,
                "-vf", f"drawtext=text='{text}':fontsize={font_size}:fontcolor=white:box=1:boxcolor=black@0.5:boxborderw=5:{pos}",
                "-codec:a", "copy",
                "-y",
                output_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                return {
                    "status": "success",
                    "output_file": output_path,
                    "text_added": text
                }
            else:
                return {
                    "status": "error",
                    "error": result.stderr
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def optimize_for_platform(self, video_file: str, platform: str,
                             output_path: str) -> Dict:
        """
        Optimize video for specific platform requirements.
        """
        if self.mock_mode:
            return self._mock_optimize(video_file, platform, output_path)

        platform_settings = {
            "tiktok": {
                "resolution": "1080x1920",
                "fps": "30",
                "bitrate": "4M",
                "max_size": 287,
                "format": "mp4"
            },
            "instagram_reels": {
                "resolution": "1080x1920",
                "fps": "30",
                "bitrate": "3.5M",
                "max_size": 100,
                "format": "mp4"
            },
            "youtube_shorts": {
                "resolution": "1080x1920",
                "fps": "30",
                "bitrate": "5M",
                "max_size": 100,
                "format": "mp4"
            },
            "twitter": {
                "resolution": "1280x720",
                "fps": "30",
                "bitrate": "2M",
                "max_size": 512,
                "format": "mp4"
            }
        }

        settings = platform_settings.get(platform, platform_settings["tiktok"])

        try:
            cmd = [
                self.ffmpeg_path,
                "-i", video_file,
                "-vf", f"scale={settings['resolution']}:force_original_aspect_ratio=decrease,pad={settings['resolution']}:(ow-iw)/2:(oh-ih)/2",
                "-r", settings["fps"],
                "-b:v", settings["bitrate"],
                "-c:a", "aac",
                "-b:a", "128k",
                "-movflags", "+faststart",
                "-y",
                output_path
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                file_size_mb = os.path.getsize(output_path) / (1024 * 1024)

                return {
                    "status": "success",
                    "output_file": output_path,
                    "platform": platform,
                    "file_size_mb": round(file_size_mb, 2),
                    "within_limit": file_size_mb <= settings["max_size"]
                }
            else:
                return {
                    "status": "error",
                    "error": result.stderr
                }

        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

    def _add_fade_transitions(self, video_files: List[str], output_path: str) -> List[str]:
        """
        Build FFmpeg command for fade transitions.
        """
        filter_complex = []
        stream_labels = []

        for i, video in enumerate(video_files):
            if i == 0:
                filter_complex.append(f"[0:v]fade=out:d=0.5:alpha=1[v0]")
            elif i == len(video_files) - 1:
                filter_complex.append(f"[{i}:v]fade=in:d=0.5:alpha=1[v{i}]")
            else:
                filter_complex.append(f"[{i}:v]fade=in:d=0.5:alpha=1,fade=out:d=0.5:alpha=1[v{i}]")
            stream_labels.append(f"[v{i}]")

        filter_complex.append(f"{''.join(stream_labels)}concat=n={len(video_files)}:v=1:a=0[outv]")

        cmd = [self.ffmpeg_path]
        for video in video_files:
            cmd.extend(["-i", video])
        cmd.extend([
            "-filter_complex", ";".join(filter_complex),
            "-map", "[outv]",
            "-c:v", "libx264",
            "-preset", "fast",
            "-y",
            output_path
        ])

        return cmd

    def _get_duration(self, video_file: str) -> float:
        """
        Get duration of video file in seconds.
        """
        try:
            cmd = [
                self.ffmpeg_path,
                "-i", video_file,
                "-f", "null",
                "-"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, stderr=subprocess.PIPE)
            for line in result.stderr.split('\n'):
                if "Duration" in line:
                    duration_str = line.split("Duration:")[1].split(",")[0].strip()
                    parts = duration_str.split(":")
                    hours = int(parts[0])
                    minutes = int(parts[1])
                    seconds = float(parts[2])
                    return hours * 3600 + minutes * 60 + seconds
        except:
            pass
        return 0.0

    def _time_to_ms(self, time_str: str) -> int:
        """
        Convert time string (MM:SS) to milliseconds.
        """
        try:
            if ":" in time_str:
                parts = time_str.split(":")
                if len(parts) == 2:
                    minutes = int(parts[0])
                    seconds = int(parts[1])
                    return (minutes * 60 + seconds) * 1000
            return int(time_str) * 1000
        except:
            return 0

    def _mock_stitch(self, video_files: List[str], output_path: str) -> Dict:
        """Mock response for stitching."""
        return {
            "status": "mock_success",
            "output_file": output_path,
            "duration": len(video_files) * 6,
            "file_size": 50000000,
            "mock_mode": True,
            "actual_operation": f"Would stitch {len(video_files)} videos"
        }

    def _mock_audio_add(self, video_file: str, audio_file: str, output_path: str) -> Dict:
        """Mock response for audio addition."""
        return {
            "status": "mock_success",
            "output_file": output_path,
            "audio_added": audio_file,
            "mock_mode": True
        }

    def _mock_audio_mix(self, base_video: str, audio_layers: List[Dict], output_path: str) -> Dict:
        """Mock response for audio mixing."""
        return {
            "status": "mock_success",
            "output_file": output_path,
            "audio_layers_mixed": len(audio_layers),
            "mock_mode": True
        }

    def _mock_text_overlay(self, video_file: str, text: str, output_path: str) -> Dict:
        """Mock response for text overlay."""
        return {
            "status": "mock_success",
            "output_file": output_path,
            "text_added": text,
            "mock_mode": True
        }

    def _mock_optimize(self, video_file: str, platform: str, output_path: str) -> Dict:
        """Mock response for optimization."""
        return {
            "status": "mock_success",
            "output_file": output_path,
            "platform": platform,
            "file_size_mb": 45.2,
            "within_limit": True,
            "mock_mode": True
        }