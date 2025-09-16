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

            # Save to file
            output_file = f"outputs/analysis_{topic.replace(' ', '_')}.md"
            os.makedirs("outputs", exist_ok=True)
            with open(output_file, "w") as f:
                f.write(f"# Marketing Analysis: {topic}\n\n")
                f.write(str(result.get("analysis", "")))

            console.print(f"\n[green]✓ Analysis saved to {output_file}[/green]")

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

            # Save to file
            output_file = f"outputs/campaign_{product.replace(' ', '_')}.md"
            os.makedirs("outputs", exist_ok=True)
            with open(output_file, "w") as f:
                f.write(f"# Marketing Campaign: {product}\n\n")
                f.write(str(result.get("campaign", "")))

            console.print(f"\n[green]✓ Campaign saved to {output_file}[/green]")

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

    console.print("\n[bold cyan]🔧 Configuration:[/bold cyan]")
    console.print(f"  Lite Model (simple tasks): [yellow]{Config.LITE_MODEL}[/yellow]")
    console.print(f"  Pro Model (complex tasks): [yellow]{Config.PRO_MODEL}[/yellow]")
    console.print(f"  API: [yellow]OpenRouter[/yellow]")
    console.print(f"  Crew Mode: [yellow]Hierarchical (Philosopher leads)[/yellow]")

    console.print("\n[bold cyan]📊 Model Usage:[/bold cyan]")
    console.print(f"  [green]Lite Model[/green] → introduce, about")
    console.print(f"  [green]Pro Model[/green] → analyze, campaign, trend")


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