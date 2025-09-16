"""
Marketing Crew Orchestration
Manages the three-agent crew for Karlo's digital twin.
"""

from crewai import Crew, Process
from typing import Dict, Any, Optional
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.agents.philosopher import ZeitgeistPhilosopher
from src.agents.architect import CynicalContentArchitect
from src.agents.optimizer import BrutalistOptimizer
from src.tasks.marketing_tasks import MarketingTasks
from config import Config
import os


class MarketingCrew:
    """
    Orchestrates the three-agent marketing crew.
    Implements hierarchical process: Philosopher → Architect → Optimizer
    """

    def __init__(self, use_lite: bool = False):
        """Initialize the marketing crew with all three agents.

        Args:
            use_lite: If True, use lite model for all agents (for simple tasks)
        """

        # Validate configuration
        Config.validate()

        # Store model preference
        self.use_lite = use_lite

        # Set environment variable for OpenAI API key (CrewAI fallback)
        # This prevents CrewAI from complaining about missing OpenAI key
        os.environ['OPENAI_API_KEY'] = Config.OPENROUTER_API_KEY

        # Create agents with appropriate model
        self.philosopher = ZeitgeistPhilosopher().create(use_lite=use_lite)
        self.architect = CynicalContentArchitect().create(use_lite=use_lite)
        self.optimizer = BrutalistOptimizer().create(use_lite=use_lite)

        # Task factory
        self.tasks = MarketingTasks()

        # Store crew instance
        self.crew = None

    def create_crew(self, tasks: list) -> Crew:
        """Create a crew with specific tasks."""

        self.crew = Crew(
            agents=[self.philosopher, self.architect, self.optimizer],
            tasks=tasks,
            process=Process.sequential,  # Sequential process to avoid hierarchical issues
            verbose=Config.CREW_VERBOSE,
            memory=True,  # Enable memory for better context
            cache=True,   # Cache results for efficiency
            max_rpm=30,   # Rate limiting for API calls
            share_crew=False
        )

        return self.crew

    def run_introduction(self, context: str = "the class") -> Dict[str, str]:
        """Have all agents introduce themselves."""

        results = {}

        # Create introduction tasks for each agent
        phil_task = self.tasks.create_introduction_task(self.philosopher, context)
        arch_task = self.tasks.create_introduction_task(self.architect, context)
        opt_task = self.tasks.create_introduction_task(self.optimizer, context)

        # Create crew with introduction tasks
        crew = self.create_crew([phil_task, arch_task, opt_task])

        # Execute introductions
        output = crew.kickoff()

        # Also get hardcoded introductions for backup
        results["philosopher"] = ZeitgeistPhilosopher().introduce_self()
        results["architect"] = CynicalContentArchitect().introduce_self()
        results["optimizer"] = BrutalistOptimizer().introduce_self()
        results["crew_output"] = str(output)

        return results

    def explain_background(self) -> str:
        """Explain Karlo's background in 3 sentences."""

        # Create task
        task = self.tasks.create_background_summary_task(self.philosopher)

        # Create crew with single task
        crew = self.create_crew([task])

        # Execute
        output = crew.kickoff()

        return str(output)

    def analyze_trend(self, topic: Optional[str] = None) -> Dict[str, Any]:
        """Run full marketing pipeline: analyze -> create -> optimize -> refine."""

        # Step 1: Philosopher analyzes trends
        trend_task = self.tasks.create_trend_analysis_task(self.philosopher, topic)

        # Step 2: Architect creates initial content based on analysis
        content_task = self.tasks.create_content_generation_task(self.architect, topic)
        content_task.context = [trend_task]  # Uses philosopher's analysis

        # Step 3: Optimizer analyzes the content and provides optimization recommendations
        optimize_task = self.tasks.create_optimization_task(self.optimizer)
        optimize_task.context = [content_task]  # Uses architect's content

        # Step 4: Architect creates FINAL content incorporating optimizer's feedback
        final_content_task = self.tasks.create_final_content_task(self.architect, topic)
        final_content_task.context = [trend_task, content_task, optimize_task]  # Uses ALL previous outputs

        # Create crew with full 4-step pipeline
        crew = self.create_crew([trend_task, content_task, optimize_task, final_content_task])

        # Execute pipeline
        output = crew.kickoff()

        return {
            "analysis": str(output),
            "topic": topic or "current trends",
            "status": "completed"
        }

    def generate_campaign(self, product: str) -> Dict[str, Any]:
        """Generate a complete marketing campaign using 4-step pipeline."""

        # Step 1: Philosopher analyzes cultural trends for the product
        trend_task = self.tasks.create_trend_analysis_task(
            self.philosopher,
            f"{product} - identify relevant cultural trends"
        )

        # Step 2: Architect creates initial content
        content_task = self.tasks.create_content_generation_task(
            self.architect,
            f"{product} campaign"
        )
        content_task.context = [trend_task]

        # Step 3: Optimizer provides recommendations
        optimize_task = self.tasks.create_optimization_task(self.optimizer)
        optimize_task.context = [content_task]

        # Step 4: Architect creates FINAL optimized content
        final_content_task = self.tasks.create_final_content_task(
            self.architect,
            f"{product} campaign"
        )
        final_content_task.context = [trend_task, content_task, optimize_task]

        # Create crew with full 4-step pipeline
        crew = self.create_crew([trend_task, content_task, optimize_task, final_content_task])

        # Execute campaign generation
        output = crew.kickoff()

        return {
            "campaign": str(output),
            "product": product,
            "status": "completed"
        }

    def quick_analysis(self, query: str) -> str:
        """Quick analysis without full pipeline."""

        # Single task for philosopher
        task = self.tasks.create_trend_analysis_task(self.philosopher, query)

        # Create minimal crew - use sequential for single agent
        crew = Crew(
            agents=[self.philosopher],
            tasks=[task],
            process=Process.sequential,
            verbose=Config.CREW_VERBOSE
        )

        # Execute
        output = crew.kickoff()

        return str(output)


class KarloDigitalTwin:
    """
    The complete digital twin of Karlo Vrančić.
    Combines all agents into a cohesive marketing intelligence system.
    Uses lite model for simple tasks and pro model for complex analysis.
    """

    def __init__(self):
        """Initialize the digital twin."""
        # Create two crews: one for lite tasks, one for pro tasks
        self.lite_crew = MarketingCrew(use_lite=True)  # For simple tasks
        self.pro_crew = MarketingCrew(use_lite=False)  # For complex tasks

        self.context = {
            "name": "Karlo Vrančić",
            "role": "Harvard/MIT MS Student & TeeWiz CEO",
            "philosophy": "Journey matters more than the destination",
            "expertise": ["AI", "Data Science", "Marketing", "Entrepreneurship"]
        }

    def introduce(self) -> Dict[str, str]:
        """Full introduction from all agents. Uses LITE model."""
        return self.lite_crew.run_introduction()

    def analyze(self, topic: Optional[str] = None) -> Dict[str, Any]:
        """Analyze trends and generate marketing insights. Uses PRO model."""
        return self.pro_crew.analyze_trend(topic)

    def campaign(self, product: str) -> Dict[str, Any]:
        """Generate full marketing campaign. Uses PRO model."""
        return self.pro_crew.generate_campaign(product)

    def about_me(self) -> str:
        """Explain Karlo's background. Uses LITE model."""
        return self.lite_crew.explain_background()

    def quick_take(self, query: str) -> str:
        """Get a quick take on something. Uses PRO model."""
        return self.pro_crew.quick_analysis(query)