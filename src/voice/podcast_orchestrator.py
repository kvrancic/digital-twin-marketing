"""
Podcast Orchestrator - Manages multi-agent voice discussions.
Coordinates agent responses and synthesizes speech for each contribution.
"""

from crewai import Crew, Process
from typing import Dict, List, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.agents.philosopher import ZeitgeistPhilosopher
from src.agents.architect import CynicalContentArchitect
from src.agents.optimizer import BrutalistOptimizer
from src.tasks.podcast_tasks import PodcastTasks
from .tts import KokoroTTS
from .audio_utils import AudioPlayer
from config import Config


class PodcastOrchestrator:
    """
    Orchestrates podcast-style discussions between agents.
    Each agent speaks their contributions in their unique voice.
    """

    def __init__(self, use_lite: bool = False):
        """
        Initialize podcast orchestrator.

        Args:
            use_lite: If True, use lite model for agents
        """
        # Set OpenAI API key for CrewAI
        os.environ['OPENAI_API_KEY'] = Config.OPENROUTER_API_KEY

        # Initialize agents
        self.philosopher = ZeitgeistPhilosopher().create(use_lite=use_lite)
        self.architect = CynicalContentArchitect().create(use_lite=use_lite)
        self.optimizer = BrutalistOptimizer().create(use_lite=use_lite)

        # Task factory
        self.tasks = PodcastTasks()

        # Voice synthesis
        try:
            self.tts = KokoroTTS()
            self.player = AudioPlayer()
            self.voice_enabled = True
        except Exception as e:
            print(f"⚠️  Voice synthesis not available: {e}")
            self.voice_enabled = False

        # Agent-to-name mapping
        self.agent_names = {
            id(self.philosopher): 'philosopher',
            id(self.architect): 'architect',
            id(self.optimizer): 'optimizer',
        }

        # Agent-to-display-name mapping
        self.display_names = {
            'philosopher': '🧐 Zeitgeist Philosopher',
            'architect': '✍️ Cynical Content Architect',
            'optimizer': '📊 Brutalist Optimizer',
        }

    def speak_text(self, text: str, agent_name: str, show_text: bool = True):
        """
        Synthesize and play speech for an agent.

        Args:
            text: Text to speak
            agent_name: Name of the agent speaking
            show_text: If True, print the text as well
        """
        display_name = self.display_names.get(agent_name, agent_name)

        if show_text:
            print(f"\n{display_name}:")
            print(f"  {text}\n")

        if self.voice_enabled:
            try:
                # Synthesize speech
                audio = self.tts.speak_as_agent(text, agent_name)

                # Play audio
                self.player.play(audio, blocking=True)

            except Exception as e:
                print(f"⚠️  Voice playback failed: {e}")
        else:
            print("  (Voice synthesis not available - showing text only)")

    def run_discussion(self, topic: str, rounds: int = 3) -> Dict[str, Any]:
        """
        Run a podcast-style discussion about a topic.

        Args:
            topic: The topic to discuss
            rounds: Number of discussion rounds

        Returns:
            Dictionary with discussion transcript and metadata
        """
        print(f"\n{'='*80}")
        print(f"🎙️  PODCAST MODE: {topic}")
        print(f"{'='*80}\n")

        transcript = []

        # Round 1: Opening statements
        print("\n🎬 ROUND 1: Opening Statements\n")
        print("-" * 80)

        for agent, agent_name in [(self.philosopher, 'philosopher'),
                                   (self.architect, 'architect'),
                                   (self.optimizer, 'optimizer')]:
            # Create task
            task = self.tasks.create_opening_statement_task(agent, topic)

            # Execute with single-agent crew
            crew = Crew(
                agents=[agent],
                tasks=[task],
                process=Process.sequential,
                verbose=False
            )

            result = crew.kickoff()
            statement = str(result).strip()

            # Speak and record
            self.speak_text(statement, agent_name)
            transcript.append({
                'agent': agent_name,
                'round': 1,
                'type': 'opening',
                'text': statement
            })

        # Round 2-N: Responses and discussion
        for round_num in range(2, rounds + 1):
            print(f"\n🔄 ROUND {round_num}: Discussion\n")
            print("-" * 80)

            # Get previous statements for context
            previous_statement = transcript[-1]['text'] if transcript else None

            for agent, agent_name in [(self.philosopher, 'philosopher'),
                                       (self.architect, 'architect'),
                                       (self.optimizer, 'optimizer')]:
                # Create response task
                task = self.tasks.create_response_task(agent, topic, previous_statement)

                # Execute
                crew = Crew(
                    agents=[agent],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=False
                )

                result = crew.kickoff()
                response = str(result).strip()

                # Speak and record
                self.speak_text(response, agent_name)
                transcript.append({
                    'agent': agent_name,
                    'round': round_num,
                    'type': 'response',
                    'text': response
                })

                # Update previous statement for next agent
                previous_statement = response

        # Final round: Conclusions
        print("\n🎯 FINAL THOUGHTS: Conclusions\n")
        print("-" * 80)

        for agent, agent_name in [(self.philosopher, 'philosopher'),
                                   (self.architect, 'architect'),
                                   (self.optimizer, 'optimizer')]:
            # Create conclusion task
            task = self.tasks.create_conclusion_task(agent, topic)

            # Execute
            crew = Crew(
                agents=[agent],
                tasks=[task],
                process=Process.sequential,
                verbose=False
            )

            result = crew.kickoff()
            conclusion = str(result).strip()

            # Speak and record
            self.speak_text(conclusion, agent_name)
            transcript.append({
                'agent': agent_name,
                'round': 'final',
                'type': 'conclusion',
                'text': conclusion
            })

        print(f"\n{'='*80}")
        print("✅ Podcast discussion complete!")
        print(f"{'='*80}\n")

        return {
            'topic': topic,
            'transcript': transcript,
            'rounds': rounds,
            'status': 'completed'
        }

    def quick_takes(self, topic: str) -> Dict[str, str]:
        """
        Get quick hot takes from all agents.

        Args:
            topic: Topic for hot takes

        Returns:
            Dictionary of agent hot takes
        """
        print(f"\n{'='*80}")
        print(f"⚡ QUICK TAKES: {topic}")
        print(f"{'='*80}\n")

        hot_takes = {}

        for agent, agent_name in [(self.philosopher, 'philosopher'),
                                   (self.architect, 'architect'),
                                   (self.optimizer, 'optimizer')]:
            # Create hot take task
            task = self.tasks.create_quick_take_task(agent, topic)

            # Execute
            crew = Crew(
                agents=[agent],
                tasks=[task],
                process=Process.sequential,
                verbose=False
            )

            result = crew.kickoff()
            hot_take = str(result).strip()

            # Speak and record
            self.speak_text(hot_take, agent_name)
            hot_takes[agent_name] = hot_take

        print(f"\n{'='*80}\n")

        return hot_takes

    def save_transcript(self, discussion: Dict[str, Any], output_path: str = None):
        """
        Save discussion transcript to file.

        Args:
            discussion: Discussion result from run_discussion()
            output_path: Path to save transcript
        """
        if output_path is None:
            topic_slug = discussion['topic'].replace(' ', '_').lower()
            output_path = f"outputs/podcast_{topic_slug}.md"

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w') as f:
            f.write(f"# Podcast Discussion: {discussion['topic']}\n\n")
            f.write(f"**Rounds:** {discussion['rounds']}\n\n")
            f.write("---\n\n")

            current_round = None
            for entry in discussion['transcript']:
                # Write round headers
                if entry['round'] != current_round:
                    current_round = entry['round']
                    if current_round == 'final':
                        f.write("## Final Thoughts\n\n")
                    else:
                        f.write(f"## Round {current_round}\n\n")

                # Write speaker and text
                display_name = self.display_names[entry['agent']]
                f.write(f"### {display_name}\n\n")
                f.write(f"{entry['text']}\n\n")

        print(f"✓ Transcript saved to {output_path}")
