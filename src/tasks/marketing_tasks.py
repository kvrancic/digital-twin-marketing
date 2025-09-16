"""
Marketing Tasks for the Digital Twin Crew
Defines specific tasks for each agent in the marketing pipeline.
"""

from crewai import Task
from typing import List, Dict, Any


class MarketingTasks:
    """Creates and manages tasks for the marketing crew."""

    @staticmethod
    def create_trend_analysis_task(agent, topic: str = None) -> Task:
        """Create a task for the Zeitgeist Philosopher to analyze trends."""

        description = f"""Analyze {'the topic: ' + topic if topic else 'current viral trends and cultural movements'}.

        Your analysis must:
        1. Identify surface-level trend observations
        2. Dig deeper to find the underlying psychological drivers
        3. Connect these drivers to consumer behavior patterns
        4. Identify specific opportunities for TeeWiz t-shirt designs
        5. Provide actionable insights with specific examples

        Use web search to find current trends, Reddit discussions, and viral content.
        Focus on trends that have merchandising potential.

        Remember: We're not just identifying trends, we're finding the human truths
        that make people buy t-shirts to express their identity."""

        expected_output = """A comprehensive trend analysis brief containing:

        1. TREND IDENTIFICATION
        - 3-5 current viral trends or cultural movements
        - Evidence from social media, search data, or news

        2. PSYCHOLOGICAL ANALYSIS
        - Deep psychological drivers behind each trend
        - Connection to fundamental human needs (belonging, status, rebellion, etc.)

        3. CONSUMER INSIGHTS
        - How these psychological drivers translate to purchasing behavior
        - Specific demographics most affected

        4. TEEWIZ OPPORTUNITIES
        - 5-10 specific VISUAL t-shirt concept angles (not just text)
        - Focus on imagery, symbols, visual metaphors that work on apparel
        - Consider meme formats, iconic imagery, visual jokes
        - Target audience for each concept
        - Viral potential assessment

        5. ACTIONABLE SUMMARY
        - Top 3 opportunities ranked by potential
        - Specific next steps for content creation"""

        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )

    @staticmethod
    def create_content_generation_task(agent, context: str = None) -> Task:
        """Create a task for the Cynical Content Architect to generate content."""

        description = f"""Based on the trend analysis insights from the previous task{' about: ' + context if context else ''},
        create multi-platform marketing content for TeeWiz that directly responds to the findings.

        You must produce:
        1. T-SHIRT CONCEPTS (10 ideas for FRONT-PRINT ONLY designs)
        - Focus on VISUAL/GRAPHIC designs, not just text
        - Include detailed visual descriptions (what images, illustrations, graphics)
        - Combine clever text WITH visual elements
        - Remember: DTG printing on front only, full-color capable
        - Target audience for each design
        - Think: album art parodies, meme formats, pop culture mashups, illustrated concepts

        2. SOCIAL MEDIA CONTENT
        - 5 Twitter/X posts (viral potential)
        - 3 Instagram captions with hashtags
        - 2 TikTok video concepts

        3. BLOG POST
        - SEO-optimized title (50-60 characters)
        - Compelling introduction (hook them immediately)
        - Full article outline with headers
        - Meta description (150-155 characters)
        - Target keywords naturally integrated

        Remember: Every piece of content should make people feel smart for getting it,
        and sharing it should make them look clever to their peers."""

        expected_output = """Complete marketing content package:

        T-SHIRT CONCEPTS:
        [10 detailed VISUAL designs with graphics, illustrations, and text combinations for front-print only]

        SOCIAL MEDIA POSTS:
        Twitter/X: [5 posts with engagement hooks]
        Instagram: [3 captions with strategic hashtags]
        TikTok: [2 video concepts with scripts]

        BLOG POST:
        Title: [SEO-optimized title]
        Meta Description: [Click-worthy description]
        Target Keywords: [Primary and secondary keywords]

        FULL OUTLINE:
        - Introduction (with hook)
        - Main sections with H2/H3 headers
        - Key points for each section
        - Conclusion with CTA

        CONTENT STRATEGY NOTES:
        - Viral potential assessment
        - Cross-promotion opportunities
        - Expected engagement metrics"""

        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )

    @staticmethod
    def create_optimization_task(agent, content: str = None) -> Task:
        """Create a task for the Brutalist Optimizer to optimize content."""

        description = f"""Analyze and optimize the marketing content created in the previous task for maximum
        search visibility and conversion potential.

        Your optimization must include:
        1. TECHNICAL SEO AUDIT
        - Title tag optimization
        - Meta descriptions with CTAs
        - Header hierarchy (H1, H2, H3)
        - Keyword density analysis
        - Internal linking opportunities

        2. CONVERSION OPTIMIZATION
        - CTA placement recommendations
        - Psychological triggers to implement
        - Urgency/scarcity elements
        - Social proof integration points

        3. PERFORMANCE METRICS
        - Estimated CTR for each piece
        - Conversion probability scoring
        - Ranking difficulty assessment
        - Time to first conversion estimate

        4. TECHNICAL IMPLEMENTATION
        - Schema markup recommendations
        - Page speed optimization tips
        - Mobile optimization requirements
        - Core Web Vitals considerations

        Provide specific, actionable recommendations with expected impact percentages."""

        expected_output = """Comprehensive optimization report:

        SEO OPTIMIZATION:
        - Title Tags: [Optimized versions with character counts]
        - Meta Descriptions: [Rewritten with CTAs, character counts]
        - Keyword Strategy: [Primary, secondary, LSI keywords]
        - Content Structure: [Optimal header hierarchy]

        CONVERSION OPTIMIZATION:
        - CTA Placements: [Specific locations with reasoning]
        - Psychological Triggers: [Which to use and where]
        - Urgency Elements: [Specific implementations]
        - A/B Test Recommendations: [What to test first]

        PERFORMANCE PROJECTIONS:
        - Expected CTR: [Percentage with reasoning]
        - Conversion Rate: [Baseline and optimized estimates]
        - Ranking Timeline: [Realistic expectations]
        - Revenue Impact: [Projected improvement]

        TECHNICAL REQUIREMENTS:
        - Schema Markup: [Specific types to implement]
        - Page Speed: [Target metrics and how to achieve]
        - Mobile Optimization: [Critical changes needed]

        PRIORITY ACTIONS:
        1. [Most impactful change - impact %]
        2. [Second priority - impact %]
        3. [Third priority - impact %]

        FINAL VERDICT:
        Overall optimization score: X/100
        Expected improvement: X%
        Implementation difficulty: Easy/Medium/Hard
        ROI Timeline: X weeks"""

        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )

    @staticmethod
    def create_introduction_task(agent, context: str = "the class") -> Task:
        """Create a task for agents to introduce themselves."""

        description = f"""Introduce yourself to {context} in character.

        Your introduction should:
        1. Explain your role in Karlo's digital twin system
        2. Showcase your unique personality and perspective
        3. Include a specific example of your expertise
        4. Reference Karlo's background appropriately
        5. Be memorable and true to your character

        Keep it concise but impactful - around 200-300 words."""

        expected_output = """A compelling self-introduction that:
        - Clearly explains your purpose
        - Demonstrates your unique personality
        - Shows how you contribute to the crew
        - Includes specific examples
        - Leaves a memorable impression"""

        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )

    @staticmethod
    def create_final_content_task(agent, context: str = None) -> Task:
        """Create a task for the Cynical Content Architect to generate FINAL optimized content."""

        description = f"""Based on ALL previous analysis:
        1. The trend analysis from the philosopher
        2. Your initial content creation
        3. The SEO/optimization recommendations from the optimizer

        Create the FINAL, OPTIMIZED version of the marketing content{' for: ' + context if context else ''}.

        You must produce the ULTIMATE version that incorporates:
        - All the deep insights from the trend analysis
        - Your creative content ideas
        - The SEO optimizations and conversion improvements suggested

        FINAL DELIVERABLES:
        1. T-SHIRT CONCEPTS (10 OPTIMIZED designs for FRONT-PRINT ONLY)
        - Visual/graphic designs with SEO-friendly names
        - Detailed visual descriptions optimized for searchability
        - Clear target audience and keywords for each design
        - Conversion-focused descriptions

        2. SOCIAL MEDIA CONTENT (OPTIMIZED)
        - 5 Twitter/X posts with viral hooks and trending hashtags
        - 3 Instagram captions with optimized hashtags and CTAs
        - 2 TikTok concepts with trending audio suggestions

        3. BLOG POST (FULLY OPTIMIZED)
        - SEO-perfect title (50-60 chars) with primary keyword
        - Compelling introduction with psychological triggers
        - Full article with optimal header hierarchy
        - Meta description that drives clicks (150-155 chars)
        - Natural keyword integration throughout
        - Strong CTAs placed strategically

        This is your FINAL output - make it perfect, actionable, and ready to convert."""

        expected_output = """FINAL OPTIMIZED MARKETING PACKAGE:

        T-SHIRT DESIGNS:
        [10 conversion-optimized visual designs with full details]

        SOCIAL MEDIA CONTENT:
        [Viral-optimized posts across all platforms]

        BLOG POST:
        [Complete SEO-optimized article ready to publish]

        CONVERSION METRICS:
        - Expected CTR improvements
        - Projected conversion rates
        - Key performance indicators"""

        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )

    @staticmethod
    def create_background_summary_task(agent) -> Task:
        """Create a task to explain Karlo's background in 3 sentences."""

        description = """Summarize Karlo Vrančić's background in exactly 3 sentences.

        Include:
        1. Academic achievements and current status
        2. TeeWiz startup and entrepreneurial vision
        3. Personal philosophy or unique characteristic

        Be concise, impressive, and authentic to how Karlo would want to be represented."""

        expected_output = """Three sentences that capture:
        - Sentence 1: Academic excellence and current Harvard/MIT status
        - Sentence 2: TeeWiz and entrepreneurial achievements
        - Sentence 3: Personal philosophy or distinguishing characteristic"""

        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )