from crewai import Crew, Task, Process
from typing import Dict, List, Optional
import json
import os
from datetime import datetime

from agents.video_agents import (
    create_viral_cinematographer,
    create_narrative_anarchist,
    create_sonic_terrorist,
    create_algorithmic_puppet_master,
    create_video_orchestrator
)
from src.agents.philosopher import ZeitgeistPhilosopher
from config import Config
from tools.video_tools import SceneDescriptionTool, StoryboardTool, VideoScriptTool
from integrations.veo3_client import Veo3Client
from integrations.elevenlabs_client import ElevenLabsClient
from integrations.ffmpeg_processor import FFmpegProcessor


class VideoGenerationCrew:
    """
    Orchestrates the complete video generation pipeline.
    Manages agents, tools, and integrations for viral video creation.
    """

    def __init__(self):
        self.veo3_client = Veo3Client()
        self.elevenlabs_client = ElevenLabsClient()
        self.ffmpeg_processor = FFmpegProcessor()

        self.scene_tool = SceneDescriptionTool()
        self.storyboard_tool = StoryboardTool()
        self.script_tool = VideoScriptTool()

        # Set environment variable for OpenAI API key (CrewAI fallback)
        os.environ['OPENAI_API_KEY'] = Config.OPENROUTER_API_KEY

        self.philosopher = ZeitgeistPhilosopher().create(use_lite=False)
        self.cinematographer = create_viral_cinematographer()
        self.narrative_anarchist = create_narrative_anarchist()
        self.sonic_terrorist = create_sonic_terrorist()
        self.algorithmic_puppet = create_algorithmic_puppet_master()
        self.orchestrator = create_video_orchestrator()

        self.output_dir = "outputs/viral_videos"
        os.makedirs(self.output_dir, exist_ok=True)

    def analyze_trends_task(self, topic: str = "") -> Task:
        """
        Task to analyze current trends and identify viral opportunities.
        """
        return Task(
            description=f"""
            Analyze current viral trends {f'related to {topic}' if topic else 'across all platforms'}.

            Your mission:
            1. Identify the most potent viral trends right now
            2. Find the psychological triggers that make content spread
            3. Spot gaps in the market where we can insert our chaos
            4. Predict what will trend in the next 48 hours

            Focus on trends that can sell t-shirts through existential crisis.
            Remember: We're not making content, we're engineering cultural moments.
            """,
            expected_output="""
            A comprehensive trend analysis containing:
            - Top 5 viral opportunities with engagement potential
            - Psychological hooks that bypass rational thought
            - Content gaps we can exploit
            - Predicted trend trajectories
            - Specific angles for t-shirt integration
            """,
            agent=self.philosopher,
            tools=[self.scene_tool]
        )

    def create_video_concept_task(self, trend_analysis: str) -> Task:
        """
        Task to create video concept based on trend analysis.
        """
        return Task(
            description=f"""
            Based on this trend analysis:
            {trend_analysis}

            Create a viral video concept that:
            1. Hijacks the trending topic for maximum reach
            2. Subverts expectations within first 3 seconds
            3. Creates cognitive dissonance that demands resolution
            4. Naturally integrates our product without feeling like an ad
            5. Triggers sharing through FOMO or superiority complex

            The video must feel like finding a $100 bill in a philosophy textbook.
            Make it impossible to scroll past.
            """,
            expected_output="""
            A complete video concept including:
            - Core hook and viral mechanism
            - Target emotional response curve
            - 30-second narrative arc
            - Product integration strategy
            - Platform-specific optimization notes
            """,
            agent=self.narrative_anarchist
        )

    def generate_scenes_task(self, video_concept: str) -> Task:
        """
        Task to generate detailed scene descriptions.
        """
        return Task(
            description=f"""
            Transform this concept into cinematic reality:
            {video_concept}

            Generate 5 scenes (6 seconds each) that:
            1. Open with visual cocaine - impossible to ignore
            2. Build tension through unexpected juxtaposition
            3. Create moments that become memes themselves
            4. Use visual language that transcends cultural barriers
            5. End with a call to action disguised as enlightenment

            Each frame should feel like Kubrick directed a TikTok.
            Make every second worth $1000 in attention currency.
            """,
            expected_output="""
            Detailed scene descriptions in JSON format with:
            - Shot composition and camera movements
            - Lighting and color grading specs
            - Visual effects and transitions
            - Mood and emotional targets
            - Technical requirements for Veo3
            """,
            agent=self.cinematographer,
            tools=[self.scene_tool, self.storyboard_tool]
        )

    def create_audio_script_task(self, scenes: str) -> Task:
        """
        Task to create audio script with voiceover and sound effects.
        """
        return Task(
            description=f"""
            Create sonic warfare for these scenes:
            {scenes}

            Design audio that:
            1. Voiceover that sounds like your smartest friend having a breakdown
            2. Sound effects that trigger primal responses
            3. Music that creates false nostalgia
            4. Dialogue that becomes quotable immediately
            5. Audio hooks that get stuck in the brain like malware

            The audio should make people feel something they can't name.
            Make silence feel wrong after watching.
            """,
            expected_output="""
            Complete audio script in JSON with:
            - Voiceover text with emotional delivery notes
            - Character dialogue with timing
            - Sound effect placement and descriptions
            - Music cues and transitions
            - ElevenLabs voice configuration
            """,
            agent=self.sonic_terrorist,
            tools=[self.script_tool]
        )

    def optimize_for_algorithm_task(self, video_plan: str) -> Task:
        """
        Task to optimize video for platform algorithms.
        """
        return Task(
            description=f"""
            Optimize this video for algorithmic domination:
            {video_plan}

            Engineering requirements:
            1. First 3 seconds must achieve 95% retention
            2. Comment bait without being obvious
            3. Share triggers at exactly 60% and 90% marks
            4. Platform-specific formatting (9:16, captions, etc)
            5. Metadata optimization for discovery

            Make the algorithm think this is its favorite child.
            Engineer virality like it's a science, because it is.
            """,
            expected_output="""
            Algorithm optimization package:
            - Platform-specific technical specs
            - Optimal posting times by timezone
            - Hashtag velocity calculations
            - Engagement prediction model
            - A/B testing recommendations
            """,
            agent=self.algorithmic_puppet
        )

    def orchestrate_production_task(self, all_inputs: Dict) -> Task:
        """
        Task to orchestrate the final video production.
        """
        return Task(
            description=f"""
            Orchestrate the chaos into viral gold:
            {json.dumps(all_inputs, indent=2)}

            Your mission:
            1. Synthesize all agent outputs into cohesive production plan
            2. Ensure technical compatibility across all elements
            3. Create backup plans for each potential failure point
            4. Generate final production timeline
            5. Output everything needed for actual video generation

            You're the adult supervision for genius children.
            Make their insanity executable.
            """,
            expected_output="""
            Complete production package:
            - Final scene descriptions for Veo3
            - Audio script for ElevenLabs
            - FFmpeg processing instructions
            - Platform optimization settings
            - Distribution strategy
            """,
            agent=self.orchestrator
        )

    def generate_video(self, topic: str = "", user_brief: str = "") -> Dict:
        """
        Execute the complete video generation pipeline.
        """
        print("\n🎬 === VIRAL VIDEO GENERATION PIPELINE === 🎬\n")

        if not topic and not user_brief:
            topic = "whatever will sell t-shirts today"

        crew = Crew(
            agents=[
                self.philosopher,
                self.cinematographer,
                self.narrative_anarchist,
                self.sonic_terrorist,
                self.algorithmic_puppet,
                self.orchestrator
            ],
            tasks=[
                self.analyze_trends_task(topic),
                self.create_video_concept_task("{task_1_output}"),
                self.generate_scenes_task("{task_2_output}"),
                self.create_audio_script_task("{task_3_output}"),
                self.optimize_for_algorithm_task("{task_2_output}\n{task_3_output}\n{task_4_output}"),
                self.orchestrate_production_task({
                    "scenes": "{task_3_output}",
                    "audio": "{task_4_output}",
                    "optimization": "{task_5_output}"
                })
            ],
            process=Process.sequential,
            verbose=True
        )

        print(f"🔍 Analyzing trends for: {topic or 'general virality'}")
        if user_brief:
            print(f"📝 User brief: {user_brief}")

        result = crew.kickoff()

        try:
            production_plan = json.loads(result)
        except:
            production_plan = {"raw_output": str(result)}

        print("\n📹 Generating video components...")
        video_output = self._execute_production(production_plan)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{self.output_dir}/viral_video_{timestamp}"
        os.makedirs(output_path, exist_ok=True)

        self._save_outputs(video_output, output_path)

        print(f"\n✅ Video generation complete!")
        print(f"📁 Outputs saved to: {output_path}")

        return video_output

    def _execute_production(self, plan: Dict) -> Dict:
        """
        Execute the production plan with actual API calls.
        """
        output = {
            "timestamp": datetime.now().isoformat(),
            "production_plan": plan,
            "generated_assets": {
                "videos": [],
                "audio": [],
                "final_output": None
            }
        }

        try:
            scenes_data = plan.get("scenes", {})
            if isinstance(scenes_data, str):
                scenes_data = json.loads(scenes_data)

            scenes = scenes_data.get("scenes", [])
            print(f"🎥 Generating {len(scenes)} video scenes...")

            video_results = self.veo3_client.generate_video_batch(scenes)
            output["generated_assets"]["videos"] = video_results

            audio_data = plan.get("audio", {})
            if isinstance(audio_data, str):
                audio_data = json.loads(audio_data)

            print("🎙️ Generating audio tracks...")
            audio_results = self.elevenlabs_client.process_full_script(audio_data)
            output["generated_assets"]["audio"] = audio_results

            print("🎬 Stitching final video...")

            video_files = [r.get("video_url", "") for r in video_results if r.get("status") in ["success", "mock_success"]]

            if video_files:
                temp_video = f"/tmp/video_{datetime.now().timestamp()}.mp4"
                stitch_result = self.ffmpeg_processor.stitch_scenes(video_files, temp_video)

                audio_layers = []
                for vo in audio_results.get("voiceover_tracks", []):
                    if vo.get("audio_data"):
                        temp_audio = f"/tmp/audio_{datetime.now().timestamp()}.mp3"
                        self.elevenlabs_client.save_audio_file(vo["audio_data"], temp_audio)
                        audio_layers.append({
                            "file": temp_audio,
                            "start_time": vo.get("time_range", "00:00").split("-")[0],
                            "volume": 100
                        })

                if audio_layers and stitch_result.get("status") in ["success", "mock_success"]:
                    final_output = f"/tmp/final_video_{datetime.now().timestamp()}.mp4"
                    mix_result = self.ffmpeg_processor.mix_audio_layers(
                        temp_video, audio_layers, final_output
                    )

                    platform = plan.get("optimization", {}).get("platform", "tiktok")
                    optimized_output = f"/tmp/optimized_{platform}_{datetime.now().timestamp()}.mp4"
                    optimize_result = self.ffmpeg_processor.optimize_for_platform(
                        final_output, platform, optimized_output
                    )

                    output["generated_assets"]["final_output"] = optimize_result

        except Exception as e:
            print(f"❌ Production execution error: {str(e)}")
            output["error"] = str(e)

        return output

    def _save_outputs(self, output: Dict, output_path: str) -> None:
        """
        Save all outputs to organized directory structure.
        """
        with open(f"{output_path}/production_plan.json", "w") as f:
            json.dump(output.get("production_plan", {}), f, indent=2)

        with open(f"{output_path}/generation_log.json", "w") as f:
            json.dump(output, f, indent=2)

        assets_dir = f"{output_path}/assets"
        os.makedirs(assets_dir, exist_ok=True)

        for idx, video in enumerate(output.get("generated_assets", {}).get("videos", [])):
            if video.get("metadata"):
                with open(f"{assets_dir}/scene_{idx+1}_metadata.json", "w") as f:
                    json.dump(video["metadata"], f, indent=2)

        audio_output = output.get("generated_assets", {}).get("audio", {})
        if audio_output:
            with open(f"{assets_dir}/audio_script.json", "w") as f:
                json.dump(audio_output, f, indent=2)

        readme_content = f"""# Viral Video Generation Output

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Production Summary

- **Scenes Generated**: {len(output.get('generated_assets', {}).get('videos', []))}
- **Audio Tracks**: {len(output.get('generated_assets', {}).get('audio', {}).get('voiceover_tracks', []))}
- **Sound Effects**: {len(output.get('generated_assets', {}).get('audio', {}).get('sound_effects', []))}

## Files

- `production_plan.json`: Complete production plan from AI agents
- `generation_log.json`: Full generation log with all outputs
- `assets/`: Individual scene and audio files

## Status

{"✅ Generation successful" if not output.get('error') else f"⚠️ Partial generation: {output.get('error')}"}

## Next Steps

1. Review generated content
2. Make any manual adjustments
3. Upload to target platforms
4. Monitor engagement metrics
5. Iterate based on performance

---

*Generated by Karlo's Digital Twin - Viral Video Pipeline*
"""

        with open(f"{output_path}/README.md", "w") as f:
            f.write(readme_content)

        print(f"📝 Saved README to {output_path}/README.md")