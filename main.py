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
from crews.video_crew import VideoGenerationCrew
from config import Config

# Initialize Rich console for beautiful terminal output
console = Console()


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
        ("video", "Generate viral video with scenes and audio"),
        ("trend", "Quick trend analysis"),
        ("info", "Display this information"),
    ]

    for cmd, desc in commands:
        console.print(f"  [green]{cmd:12}[/green] - {desc}")

    console.print("\n[bold cyan]🔧 Configuration:[/bold cyan]")
    console.print(f"  Lite Model (simple tasks): [yellow]{Config.LITE_MODEL}[/yellow]")
    console.print(f"  Pro Model (complex tasks): [yellow]{Config.PRO_MODEL}[/yellow]")
    console.print(f"  API: [yellow]OpenRouter[/yellow]")
    console.print(f"  Crew Mode: [yellow]Sequential (Philosopher → Architect → Optimizer)[/yellow]")

    console.print("\n[bold cyan]📊 Model Usage:[/bold cyan]")
    console.print(f"  [green]Lite Model[/green] → introduce, about")
    console.print(f"  [green]Pro Model[/green] → analyze, campaign, trend")


@cli.command()
@click.option('--topic', '-t', help='Topic or trend for video')
@click.option('--brief', '-b', help='Custom brief for video generation')
@click.option('--style', '-s', type=click.Choice(['cinematic', 'funny', 'hybrid']), default='hybrid', help='Video style')
def video(topic: Optional[str], brief: Optional[str], style: str):
    """Generate a viral video campaign with scenes, audio, and production plan."""
    print_header()

    if not topic and not brief:
        console.print("\n[bold cyan]🎬 Viral Video Generation[/bold cyan]\n")
        topic = Prompt.ask(
            "[cyan]What should the video be about?[/cyan]",
            default="whatever will sell t-shirts today"
        )

    console.print(f"\n[bold cyan]🎬 Generating Viral Video Campaign[/bold cyan]")
    if topic:
        console.print(f"[cyan]Topic: {topic}[/cyan]")
    if brief:
        console.print(f"[cyan]Brief: {brief}[/cyan]")
    console.print(f"[cyan]Style: {style}[/cyan]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Orchestrating viral video generation...", total=None)

        try:
            video_crew = VideoGenerationCrew()

            # Update progress messages based on pipeline stages
            progress.update(task, description="[cyan]Analyzing viral trends...")
            time.sleep(1)

            progress.update(task, description="[cyan]Creating video concept...")
            time.sleep(1)

            progress.update(task, description="[cyan]Generating scene descriptions...")
            time.sleep(1)

            progress.update(task, description="[cyan]Writing audio script...")
            time.sleep(1)

            progress.update(task, description="[cyan]Optimizing for algorithms...")

            # Generate the video
            result = video_crew.generate_video(topic=topic or "", user_brief=brief or "")

            progress.stop()

            # Display production summary
            if result.get("generated_assets"):
                assets = result["generated_assets"]

                summary_table = Table(title="🎬 Video Production Summary", show_header=True, header_style="bold magenta")
                summary_table.add_column("Component", style="cyan")
                summary_table.add_column("Status", style="green")
                summary_table.add_column("Details", style="yellow")

                summary_table.add_row(
                    "Video Scenes",
                    f"{len(assets.get('videos', []))} generated",
                    "6 seconds each, Veo3 format"
                )

                audio_data = assets.get("audio", {})
                summary_table.add_row(
                    "Voiceover",
                    f"{len(audio_data.get('voiceover_tracks', []))} tracks",
                    "ElevenLabs synthesis"
                )

                summary_table.add_row(
                    "Sound Effects",
                    f"{len(audio_data.get('sound_effects', []))} effects",
                    "Timed and positioned"
                )

                if assets.get("final_output"):
                    summary_table.add_row(
                        "Final Video",
                        "✅ Complete",
                        f"Optimized for {result.get('production_plan', {}).get('optimization', {}).get('platform', 'TikTok')}"
                    )
                else:
                    summary_table.add_row(
                        "Final Video",
                        "⚠️ Mock Mode",
                        "Set API keys for actual generation"
                    )

                console.print(summary_table)

                # Display scene descriptions
                console.print("\n[bold cyan]🎬 Generated Scenes:[/bold cyan]")
                if "production_plan" in result and "scenes" in result["production_plan"]:
                    scenes_data = result["production_plan"]["scenes"]
                    if isinstance(scenes_data, str):
                        try:
                            import json
                            scenes_data = json.loads(scenes_data)
                        except:
                            pass

                    if isinstance(scenes_data, dict) and "scenes" in scenes_data:
                        for idx, scene in enumerate(scenes_data["scenes"][:3], 1):  # Show first 3 scenes
                            scene_panel = Panel(
                                f"[yellow]{scene.get('description', 'No description')}[/yellow]\n\n"
                                f"[dim]Type: {scene.get('type', 'unknown')} | "
                                f"Duration: {scene.get('duration', 6)}s | "
                                f"Camera: {scene.get('camera_movement', 'static')}[/dim]",
                                title=f"Scene {idx}",
                                border_style="green"
                            )
                            console.print(scene_panel)

                # Display voiceover script sample
                if audio_data.get("voiceover_tracks"):
                    console.print("\n[bold cyan]🎙️ Voiceover Sample:[/bold cyan]")
                    first_vo = audio_data["voiceover_tracks"][0]
                    vo_panel = Panel(
                        f"[yellow]{first_vo.get('text', 'No text')}[/yellow]\n\n"
                        f"[dim]Time: {first_vo.get('time_range', '00:00')} | "
                        f"Voice: {first_vo.get('voice_used', 'default')} | "
                        f"Emotion: {first_vo.get('emotion', 'neutral')}[/dim]",
                        title="Opening Voiceover",
                        border_style="cyan"
                    )
                    console.print(vo_panel)

                # Show output location
                if "timestamp" in result:
                    output_dir = f"outputs/viral_videos/viral_video_{result['timestamp'].replace(':', '').replace('-', '')[:15]}"
                    console.print(f"\n[green]✅ Video generation complete![/green]")
                    console.print(f"[cyan]📁 Outputs saved to: {output_dir}/[/cyan]")
                    console.print(f"[dim]   • production_plan.json - Complete production details[/dim]")
                    console.print(f"[dim]   • generation_log.json - Full generation log[/dim]")
                    console.print(f"[dim]   • assets/ - Individual scene and audio files[/dim]")
                    console.print(f"[dim]   • README.md - Production summary[/dim]")

            else:
                console.print("[yellow]⚠️ Video generation completed with limited output[/yellow]")
                console.print("[dim]Set VEO3_API_KEY and ELEVENLABS_API_KEY for full generation[/dim]")

        except Exception as e:
            progress.stop()
            console.print(f"[red]Error during video generation: {str(e)}[/red]")
            console.print("[dim]Check that all dependencies are installed and API keys are set[/dim]")


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
            console.print("  video     - Generate viral video")
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