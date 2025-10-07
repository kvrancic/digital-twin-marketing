"""
Interactive Podcast Orchestrator - User participates in multi-agent discussions.
Allows user to speak and choose who speaks next in real-time.
"""

from crewai import Crew, Process
from typing import Dict, List, Any, Optional
import sys
import os
import tempfile
import soundfile as sf
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.agents.philosopher import ZeitgeistPhilosopher
from src.agents.architect import CynicalContentArchitect
from src.agents.optimizer import BrutalistOptimizer
from src.tasks.podcast_tasks import PodcastTasks
from .tts import EdgeTTS
from .stt import WhisperSTT
from .audio_utils import AudioPlayer, AudioRecorder
from config import Config


class InteractivePodcast:
    """
    Interactive podcast where user participates in discussions.
    User chooses who speaks next and can contribute via voice.
    """

    def __init__(self, use_lite: bool = False):
        """
        Initialize interactive podcast.

        Args:
            use_lite: If True, use lite model for agents
        """
        # Set OpenAI API key for CrewAI
        os.environ['OPENAI_API_KEY'] = Config.OPENROUTER_API_KEY

        # Initialize agents in podcast mode (no tools, not verbose)
        self.philosopher = ZeitgeistPhilosopher().create(use_lite=use_lite)
        self.architect = CynicalContentArchitect().create(use_lite=use_lite)
        self.optimizer = BrutalistOptimizer().create(use_lite=use_lite, podcast_mode=True)

        # Set verbose=False for all agents
        self.philosopher.verbose = False
        self.architect.verbose = False
        self.optimizer.verbose = False

        # Task factory
        self.tasks = PodcastTasks()

        # Voice synthesis and recording
        try:
            self.tts = EdgeTTS()
            self.player = AudioPlayer()
            self.stt = WhisperSTT()
            self.recorder = AudioRecorder()
            self.voice_enabled = True
        except Exception as e:
            print(f"⚠️  Voice features not available: {e}")
            self.voice_enabled = False

        # Agent mapping
        self.agents = {
            '2': ('philosopher', self.philosopher, '🧐 Zeitgeist Philosopher'),
            '3': ('architect', self.architect, '✍️ Cynical Content Architect'),
            '4': ('optimizer', self.optimizer, '📊 Brutalist Optimizer'),
        }

    def speak_text(self, text: str, speaker: str, is_user: bool = False):
        """
        Synthesize and play speech.

        Args:
            text: Text to speak
            speaker: Name/role of speaker
            is_user: If True, this is user's contribution (don't synthesize)
        """
        print(f"\n{speaker}:")
        print(f"  {text}\n")

        if self.voice_enabled and not is_user:
            try:
                # Get agent name for voice mapping
                agent_name = None
                for _, (name, _, _) in self.agents.items():
                    if name in speaker.lower():
                        agent_name = name
                        break

                if agent_name:
                    # Synthesize speech
                    audio = self.tts.speak_as_agent(text, agent_name)
                    # Play audio
                    self.player.play(audio, blocking=True)

            except Exception as e:
                print(f"⚠️  Voice playback failed: {e}")

    def record_user_input(self) -> str:
        """
        Record user's voice input and transcribe.

        Returns:
            Transcribed text
        """
        if not self.voice_enabled:
            print("Voice not available. Enter text instead:")
            return input("> ")

        try:
            # Record audio with manual stop
            audio = self.recorder.record_manual()

            # Save to temp file for transcription
            fd, temp_path = tempfile.mkstemp(suffix='.wav')
            os.close(fd)
            sf.write(temp_path, audio, Config.AUDIO_SAMPLE_RATE)

            # Transcribe
            print("🔄 Transcribing...")
            text = self.stt.transcribe(temp_path)

            # Clean up
            os.remove(temp_path)

            return text

        except Exception as e:
            print(f"⚠️  Voice recording failed: {e}")
            print("Enter text instead:")
            return input("> ")

    def get_agent_response(self, agent, agent_name: str, topic: str, previous_text: str) -> str:
        """
        Get response from an agent.

        Args:
            agent: The CrewAI agent
            agent_name: Name of the agent
            topic: Discussion topic
            previous_text: What was just said

        Returns:
            Agent's response
        """
        # Create response task
        task = self.tasks.create_response_task(agent, topic, previous_text)

        # Execute with single-agent crew
        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=False
        )

        result = crew.kickoff()
        return str(result).strip()

    def run_interactive_discussion(self, topic: str) -> Dict[str, Any]:
        """
        Run an interactive podcast discussion.

        Args:
            topic: The topic to discuss

        Returns:
            Dictionary with discussion transcript
        """
        print(f"\n{'='*80}")
        print(f"🎙️  INTERACTIVE PODCAST: {topic}")
        print(f"{'='*80}\n")

        print("Welcome! You'll be participating in this discussion.")
        print("After each person speaks, you choose who speaks next.\n")

        transcript = []
        previous_text = f"Let's discuss: {topic}"

        # Main discussion loop
        while True:
            # Show menu
            print("\n" + "-" * 80)
            print("Who speaks next?")
            print("  [1] You (voice input)")
            print("  [2] 🧐 Zeitgeist Philosopher")
            print("  [3] ✍️ Cynical Content Architect")
            print("  [4] 📊 Brutalist Optimizer")
            print("  [5] End discussion")
            print("-" * 80)

            choice = input("Choose (1-5): ").strip()

            if choice == '5':
                print("\n✅ Discussion ended.\n")
                break

            elif choice == '1':
                # User speaks
                user_text = self.record_user_input()

                if user_text.strip():
                    self.speak_text(user_text, "👤 You (Karlo)", is_user=True)
                    transcript.append({
                        'speaker': 'user',
                        'text': user_text
                    })
                    previous_text = user_text
                else:
                    print("⚠️  No input received. Try again.")

            elif choice in ['2', '3', '4']:
                # Agent speaks
                agent_name, agent, display_name = self.agents[choice]

                print(f"\n⏳ {display_name} is thinking...\n")

                response = self.get_agent_response(agent, agent_name, topic, previous_text)

                self.speak_text(response, display_name)
                transcript.append({
                    'speaker': agent_name,
                    'text': response
                })
                previous_text = response

            else:
                print("⚠️  Invalid choice. Please enter 1-5.")

        return {
            'topic': topic,
            'transcript': transcript,
            'status': 'completed'
        }

    def save_transcript(self, discussion: Dict[str, Any], output_path: str = None):
        """
        Save discussion transcript to file.

        Args:
            discussion: Discussion result
            output_path: Path to save transcript
        """
        if output_path is None:
            topic_slug = discussion['topic'].replace(' ', '_').lower()
            output_path = f"outputs/interactive_podcast_{topic_slug}.md"

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'w') as f:
            f.write(f"# Interactive Podcast: {discussion['topic']}\n\n")
            f.write("---\n\n")

            speaker_names = {
                'user': '👤 You (Karlo)',
                'philosopher': '🧐 Zeitgeist Philosopher',
                'architect': '✍️ Cynical Content Architect',
                'optimizer': '📊 Brutalist Optimizer',
            }

            for i, entry in enumerate(discussion['transcript'], 1):
                speaker = speaker_names.get(entry['speaker'], entry['speaker'])
                f.write(f"## Turn {i}: {speaker}\n\n")
                f.write(f"{entry['text']}\n\n")

        print(f"✓ Transcript saved to {output_path}")
