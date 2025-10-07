#!/usr/bin/env python3
"""
Karlo's Digital Twin - Main Terminal Interface
MIT AI Studio Homework Assignment
"""

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
import time
import sys
import os
from typing import Optional

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.crew.marketing_crew import KarloDigitalTwin
from config import Config

# Initialize Rich console for beautiful terminal output
console = Console()

# Voice capabilities imports (lazy loaded)
try:
    from src.voice.audio_utils import AudioRecorder, AudioPlayer
    from src.voice.stt import WhisperSTT
    from src.voice.tts import EdgeTTS
    from src.voice.podcast_orchestrator import PodcastOrchestrator
    VOICE_AVAILABLE = True
except ImportError as e:
    VOICE_AVAILABLE = False
    VOICE_IMPORT_ERROR = str(e)


def print_header():
    """Print the application header."""
    header = """
╔═══════════════════════════════════════════════════════════════════════════════╗
║                    🧠 KARLO'S DIGITAL TWIN - MIT AI STUDIO 🧠                 ║
║                                                                               ║
║                    Marketing Intelligence Powered by CrewAI                   ║
║                       Journey > Destination Philosophy                        ║
╚═══════════════════════════════════════════════════════════════════════════════╝
    """
    console.print(header, style="bold cyan")


def print_agents_info():
    """Display information about the three agents."""
    table = Table(title="🤖 Marketing Crew Agents", show_header=True, header_style="bold magenta")
    table.add_column("Agent", style="cyan", width=25)
    table.add_column("Role", style="green")
    table.add_column("Personality", style="yellow")

    table.add_row(
        "Zeitgeist Philosopher",
        "Cultural Analyst",
        "Sarcastic, finds deep truths in memes"
    )
    table.add_row(
        "Cynical Content Architect",
        "Creative Director",
        "Failed lit major who weaponizes language"
    )
    table.add_row(
        "Brutalist Optimizer",
        "Technical SEO & Conversion",
        "Models humans as state machines"
    )

    console.print(table)


@click.group()
def cli():
    """Karlo's Digital Twin - Marketing Intelligence System"""
    pass


@cli.command()
def introduce():
    """Have all agents introduce themselves to the class."""
    print_header()
    console.print("\n[bold cyan]🎭 Agent Introductions[/bold cyan]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Agents preparing introductions...", total=None)

        try:
            # Import agents for hardcoded introductions
            from src.agents.philosopher import ZeitgeistPhilosopher
            from src.agents.architect import CynicalContentArchitect
            from src.agents.optimizer import BrutalistOptimizer

            progress.stop()

            # Use hardcoded introductions directly
            for agent_name, intro in [
                ("Zeitgeist Philosopher", ZeitgeistPhilosopher().introduce_self()),
                ("Cynical Content Architect", CynicalContentArchitect().introduce_self()),
                ("Brutalist Optimizer", BrutalistOptimizer().introduce_self())
            ]:
                panel = Panel(
                    intro,
                    title=f"[bold cyan]{agent_name}[/bold cyan]",
                    border_style="green",
                    padding=(1, 2)
                )
                console.print(panel)
                console.print()

        except Exception as e:
            progress.stop()
            console.print(f"[red]Error during introductions: {str(e)}[/red]")


@cli.command()
def about():
    """Explain Karlo's background in 3 sentences."""
    print_header()
    console.print("\n[bold cyan]📚 About Karlo Vrančić[/bold cyan]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Summarizing background...", total=None)

        try:
            twin = KarloDigitalTwin()

            # Hardcoded backup in case API fails
            background = """Karlo Vrančić is a 22-year-old student from Croatia pursuing MS degrees at Harvard
(Data Science) and MIT (Deep Learning/AI Agents), after completing his BS at University of Zagreb where
he received recognition for research and community contributions.

He co-founded TeeWiz, an AI-powered custom t-shirt platform that simplifies fashion design, allowing users
to create custom designs quickly while using print-on-demand technology to reduce environmental impact.

With a background in basketball and a philosophy focused on valuing the journey over the destination,
Karlo works on combining technical skills with creative problem-solving in his entrepreneurial ventures."""

            try:
                background = twin.about_me()
            except:
                pass  # Use hardcoded version

            progress.stop()

            panel = Panel(
                background,
                title="[bold cyan]Karlo Vrančić - Background[/bold cyan]",
                border_style="green",
                padding=(1, 2)
            )
            console.print(panel)

        except Exception as e:
            progress.stop()
            console.print(f"[red]Error: {str(e)}[/red]")


@cli.command()
@click.option('--topic', '-t', help='Specific topic to analyze')
def analyze(topic: Optional[str]):
    """Analyze current trends or a specific topic."""
    print_header()

    if not topic:
        topic = Prompt.ask("[cyan]What topic should I analyze?[/cyan]", default="current viral trends")

    console.print(f"\n[bold cyan]🔍 Analyzing: {topic}[/bold cyan]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Running marketing analysis pipeline...", total=None)

        try:
            twin = KarloDigitalTwin()
            result = twin.analyze(topic)

            progress.stop()

            # Display results
            panel = Panel(
                str(result.get("analysis", "No analysis generated")),
                title=f"[bold cyan]Marketing Analysis: {topic}[/bold cyan]",
                border_style="green",
                padding=(1, 2)
            )
            console.print(panel)

            # Create output directory structure
            topic_dir = f"outputs/{topic.replace(' ', '_').lower()}"
            intermediary_dir = f"{topic_dir}/intermediary_outputs"
            os.makedirs(intermediary_dir, exist_ok=True)

            # Save final output
            final_output_file = f"{topic_dir}/final_marketing_package.md"
            with open(final_output_file, "w") as f:
                f.write(f"# Final Marketing Package: {topic}\n\n")
                f.write(str(result.get("analysis", "")))

            # Save intermediary outputs if available
            if "intermediary_outputs" in result:
                for filename, content in result.get("intermediary_outputs", {}).items():
                    intermediary_file = f"{intermediary_dir}/{filename}.md"
                    with open(intermediary_file, "w") as f:
                        f.write(f"# {filename.replace('_', ' ').title()}\n\n")
                        f.write(content)

            console.print(f"\n[green]✓ Analysis saved to {topic_dir}/[/green]")
            console.print(f"  [cyan]→ Final package: final_marketing_package.md[/cyan]")
            console.print(f"  [cyan]→ Intermediary outputs: intermediary_outputs/[/cyan]")

        except Exception as e:
            progress.stop()
            console.print(f"[red]Error during analysis: {str(e)}[/red]")


@cli.command()
@click.option('--product', '-p', help='Product to create campaign for')
def campaign(product: Optional[str]):
    """Generate a complete marketing campaign for a product."""
    print_header()

    if not product:
        product = Prompt.ask("[cyan]What product should I create a campaign for?[/cyan]",
                           default="developer humor t-shirts")

    console.print(f"\n[bold cyan]🚀 Generating Campaign: {product}[/bold cyan]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Creating marketing campaign...", total=None)

        try:
            twin = KarloDigitalTwin()
            result = twin.campaign(product)

            progress.stop()

            # Display campaign
            panel = Panel(
                str(result.get("campaign", "No campaign generated")),
                title=f"[bold cyan]Marketing Campaign: {product}[/bold cyan]",
                border_style="green",
                padding=(1, 2)
            )
            console.print(panel)

            # Create output directory structure
            product_dir = f"outputs/{product.replace(' ', '_').lower()}_campaign"
            intermediary_dir = f"{product_dir}/intermediary_outputs"
            os.makedirs(intermediary_dir, exist_ok=True)

            # Save final output
            final_output_file = f"{product_dir}/final_marketing_package.md"
            with open(final_output_file, "w") as f:
                f.write(f"# Final Marketing Campaign: {product}\n\n")
                f.write(str(result.get("campaign", "")))

            # Save intermediary outputs if available
            if "intermediary_outputs" in result:
                for filename, content in result.get("intermediary_outputs", {}).items():
                    intermediary_file = f"{intermediary_dir}/{filename}.md"
                    with open(intermediary_file, "w") as f:
                        f.write(f"# {filename.replace('_', ' ').title()}\n\n")
                        f.write(content)

            console.print(f"\n[green]✓ Campaign saved to {product_dir}/[/green]")
            console.print(f"  [cyan]→ Final package: final_marketing_package.md[/cyan]")
            console.print(f"  [cyan]→ Intermediary outputs: intermediary_outputs/[/cyan]")

        except Exception as e:
            progress.stop()
            console.print(f"[red]Error during campaign generation: {str(e)}[/red]")


@cli.command()
def trend():
    """Quick trend analysis without full pipeline."""
    print_header()
    console.print("\n[bold cyan]📊 Quick Trend Analysis[/bold cyan]\n")

    query = Prompt.ask("[cyan]What trend should I analyze?[/cyan]",
                      default="AI-generated content")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Analyzing trend...", total=None)

        try:
            twin = KarloDigitalTwin()
            result = twin.quick_take(query)

            progress.stop()

            panel = Panel(
                result,
                title=f"[bold cyan]Trend Analysis: {query}[/bold cyan]",
                border_style="green",
                padding=(1, 2)
            )
            console.print(panel)

        except Exception as e:
            progress.stop()
            console.print(f"[red]Error: {str(e)}[/red]")


@cli.command()
def info():
    """Display information about the digital twin and its agents."""
    print_header()
    print_agents_info()

    console.print("\n[bold cyan]📋 Available Commands:[/bold cyan]")
    commands = [
        ("introduce", "Have all agents introduce themselves"),
        ("about", "Learn about Karlo's background (3 sentences)"),
        ("analyze", "Analyze trends and generate marketing insights"),
        ("campaign", "Create a complete marketing campaign"),
        ("trend", "Quick trend analysis"),
        ("info", "Display this information"),
    ]

    for cmd, desc in commands:
        console.print(f"  [green]{cmd:12}[/green] - {desc}")

    console.print("\n[bold cyan]🎙️  Voice Commands (HW4):[/bold cyan]")
    voice_commands = [
        ("voice-chat", "Podcast-style discussion with voice input/output"),
        ("test-mic", "Test microphone recording"),
        ("test-voices", "Test TTS voices for each agent"),
    ]

    for cmd, desc in voice_commands:
        status = "[green]✓[/green]" if VOICE_AVAILABLE else "[red]✗[/red]"
        console.print(f"  {status} [green]{cmd:12}[/green] - {desc}")

    if not VOICE_AVAILABLE:
        console.print("\n[yellow]⚠️  Voice features require additional setup:[/yellow]")
        console.print("  1. pip install -r requirements.txt")
        console.print("  2. brew install portaudio (macOS)")
        console.print("  3. Set OPENAI_API_KEY in .env")

    console.print("\n[bold cyan]🔧 Configuration:[/bold cyan]")
    console.print(f"  Lite Model (simple tasks): [yellow]{Config.LITE_MODEL}[/yellow]")
    console.print(f"  Pro Model (complex tasks): [yellow]{Config.PRO_MODEL}[/yellow]")
    console.print(f"  API: [yellow]OpenRouter[/yellow]")
    console.print(f"  Crew Mode: [yellow]Sequential (Philosopher → Architect → Optimizer)[/yellow]")

    console.print("\n[bold cyan]📊 Model Usage:[/bold cyan]")
    console.print(f"  [green]Lite Model[/green] → introduce, about")
    console.print(f"  [green]Pro Model[/green] → analyze, campaign, trend")


@cli.command()
@click.option('--topic', '-t', help='Topic to discuss (optional, can use voice input)')
@click.option('--rounds', '-r', default=2, help='Number of discussion rounds (default: 2)')
def voice_chat(topic: Optional[str], rounds: int):
    """Voice-enabled podcast discussion mode with real-time speech."""
    print_header()

    if not VOICE_AVAILABLE:
        console.print(f"[red]✗ Voice capabilities not available[/red]")
        console.print(f"[yellow]Error: {VOICE_IMPORT_ERROR}[/yellow]")
        console.print("\n[cyan]To enable voice features:[/cyan]")
        console.print("1. Install dependencies: pip install -r requirements.txt")
        console.print("2. Install PortAudio: brew install portaudio (macOS)")
        console.print("3. Set OPENAI_API_KEY in .env file")
        return

    console.print("\n[bold cyan]🎙️  Voice Chat Mode - Podcast Discussion[/bold cyan]\n")

    try:
        # Initialize components
        stt = WhisperSTT()
        recorder = AudioRecorder()
        orchestrator = PodcastOrchestrator(use_lite=False)

        # Get topic via voice or parameter
        if not topic:
            console.print("[cyan]🎤 Listening... Speak your topic (will auto-stop after 2 seconds of silence)[/cyan]")
            console.print("[dim]Press Ctrl+C to cancel[/dim]\n")

            # Record audio
            audio_file = recorder.record_to_file()

            console.print("[cyan]🔄 Transcribing...[/cyan]")
            topic = stt.transcribe(audio_file)

            # Clean up temp file
            os.remove(audio_file)

            console.print(f"\n[green]✓ You said:[/green] [bold]{topic}[/bold]\n")

            # Confirm
            if not Confirm.ask("Start podcast discussion on this topic?", default=True):
                console.print("[yellow]Cancelled.[/yellow]")
                return

        # Run podcast discussion
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Starting podcast discussion...", total=None)
            progress.stop()

        result = orchestrator.run_discussion(topic, rounds=rounds)

        # Save transcript
        orchestrator.save_transcript(result)

        console.print("\n[green]✅ Podcast discussion complete![/green]")
        console.print(f"[cyan]Topic:[/cyan] {result['topic']}")
        console.print(f"[cyan]Rounds:[/cyan] {result['rounds']}")
        console.print(f"[cyan]Contributions:[/cyan] {len(result['transcript'])}")

    except KeyboardInterrupt:
        console.print("\n[yellow]Voice chat cancelled.[/yellow]")
    except Exception as e:
        console.print(f"\n[red]Error during voice chat: {str(e)}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")


@cli.command()
def test_mic():
    """Test microphone input and recording."""
    print_header()
    console.print("\n[bold cyan]🎤 Microphone Test[/bold cyan]\n")

    if not VOICE_AVAILABLE:
        console.print(f"[red]✗ Voice capabilities not available[/red]")
        console.print(f"[yellow]Error: {VOICE_IMPORT_ERROR}[/yellow]")
        return

    try:
        console.print("[cyan]Speak for 3 seconds...[/cyan]\n")
        AudioRecorder.test_microphone()
        console.print("\n[green]✓ Microphone test complete![/green]")
    except Exception as e:
        console.print(f"\n[red]✗ Microphone test failed: {str(e)}[/red]")


@cli.command()
@click.option('--voice', '-v', help='Specific voice to test (e.g., af_sky, am_adam)')
def test_voices(voice: Optional[str]):
    """Test text-to-speech voices for each agent."""
    print_header()
    console.print("\n[bold cyan]🔊 Voice Test[/bold cyan]\n")

    if not VOICE_AVAILABLE:
        console.print(f"[red]✗ Voice capabilities not available[/red]")
        console.print(f"[yellow]Error: {VOICE_IMPORT_ERROR}[/yellow]")
        return

    try:
        tts = EdgeTTS()

        if voice:
            # Test specific voice
            test_text = "Hello! This is a test of the Edge text-to-speech system."
            console.print(f"[cyan]Testing voice: {voice}[/cyan]")
            EdgeTTS.test_voice(voice, test_text)
        else:
            # Test all agent voices
            console.print("[cyan]Testing voices for each agent...[/cyan]\n")

            agents = {
                'philosopher': ('Zeitgeist Philosopher', "Interesting. I've analyzed human speech patterns and found them absurdly predictable."),
                'architect': ('Cynical Content Architect', "Language is manipulation, and I'm ruthlessly effective at using it."),
                'optimizer': ('Brutalist Optimizer', "Your speech synthesis latency is acceptable. Optimization complete."),
            }

            for agent_name, (display_name, test_text) in agents.items():
                console.print(f"\n[bold]{display_name}[/bold]")
                console.print(f"  Text: {test_text}")

                voice_id = tts.get_agent_voice(agent_name)
                console.print(f"  Voice: {voice_id}")

                audio = tts.speak_as_agent(test_text, agent_name)

                player = AudioPlayer()
                player.play(audio, blocking=True)

                console.print("  [green]✓ Complete[/green]")

            console.print("\n[green]✓ All voice tests complete![/green]")

    except Exception as e:
        console.print(f"\n[red]✗ Voice test failed: {str(e)}[/red]")
        import traceback
        console.print(f"[dim]{traceback.format_exc()}[/dim]")


@cli.command()
def interactive():
    """Interactive mode for continuous interaction with the digital twin."""
    print_header()
    print_agents_info()
    console.print("\n[bold cyan]🎮 Interactive Mode[/bold cyan]")
    console.print("[dim]Type 'help' for commands, 'exit' to quit[/dim]\n")

    twin = KarloDigitalTwin()

    while True:
        command = Prompt.ask("[cyan]Command[/cyan]").lower().strip()

        if command == "exit" or command == "quit":
            console.print("[yellow]Shutting down digital twin. Hvala![/yellow]")
            break

        elif command == "help":
            console.print("[green]Available commands:[/green]")
            console.print("  introduce - Agent introductions")
            console.print("  about     - Karlo's background")
            console.print("  analyze   - Analyze a topic")
            console.print("  campaign  - Generate campaign")
            console.print("  trend     - Quick trend analysis")
            console.print("  clear     - Clear screen")
            console.print("  exit      - Exit interactive mode")

        elif command == "clear":
            console.clear()
            print_header()

        elif command == "introduce":
            with console.status("[cyan]Agents introducing themselves..."):
                results = twin.introduce()
                for key, value in results.items():
                    if key != "crew_output":
                        console.print(Panel(value, title=key.title(), border_style="green"))

        elif command == "about":
            with console.status("[cyan]Generating background..."):
                background = twin.about_me()
                console.print(Panel(background, title="About Karlo", border_style="green"))

        elif command.startswith("analyze"):
            topic = command.replace("analyze", "").strip() or \
                   Prompt.ask("[cyan]Topic[/cyan]", default="current trends")
            with console.status(f"[cyan]Analyzing {topic}..."):
                result = twin.analyze(topic)
                console.print(Panel(str(result["analysis"]), title=f"Analysis: {topic}",
                                  border_style="green"))

        elif command.startswith("campaign"):
            product = command.replace("campaign", "").strip() or \
                     Prompt.ask("[cyan]Product[/cyan]", default="tech humor shirts")
            with console.status(f"[cyan]Creating campaign for {product}..."):
                result = twin.campaign(product)
                console.print(Panel(str(result["campaign"]), title=f"Campaign: {product}",
                                  border_style="green"))

        elif command.startswith("trend"):
            query = command.replace("trend", "").strip() or \
                   Prompt.ask("[cyan]Trend[/cyan]", default="AI memes")
            with console.status(f"[cyan]Analyzing {query}..."):
                result = twin.quick_take(query)
                console.print(Panel(result, title=f"Trend: {query}", border_style="green"))

        else:
            console.print(f"[red]Unknown command: {command}[/red]")
            console.print("[dim]Type 'help' for available commands[/dim]")


if __name__ == "__main__":
    try:
        # Check configuration
        Config.validate()

        # Run CLI
        if len(sys.argv) == 1:
            # No arguments - run interactive mode
            print_header()
            print_agents_info()
            console.print("\n[bold cyan]Welcome to Karlo's Digital Twin![/bold cyan]")
            console.print("[dim]Use 'python main.py --help' to see all commands[/dim]")
            console.print("[dim]Or try 'python main.py interactive' for interactive mode[/dim]\n")

            # Show available commands
            console.print("[bold cyan]Quick Start Commands:[/bold cyan]")
            console.print("  [green]python main.py introduce[/green] - Meet the agents")
            console.print("  [green]python main.py about[/green]     - Learn about Karlo")
            console.print("  [green]python main.py analyze[/green]   - Analyze trends")
            console.print("  [green]python main.py campaign[/green]  - Generate campaign")
            console.print("  [green]python main.py info[/green]      - System information")
        else:
            cli()

    except ValueError as e:
        console.print(f"[red]Configuration Error: {e}[/red]")
        console.print("[yellow]Please create a .env file with your OpenRouter API key[/yellow]")
        console.print("[dim]Copy .env.example to .env and add your key[/dim]")
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted. Doviđenja![/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        sys.exit(1)