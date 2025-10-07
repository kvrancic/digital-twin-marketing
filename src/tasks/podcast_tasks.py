"""
Podcast-style tasks for voice chat mode.
Creates conversational discussion tasks instead of marketing deliverables.
"""

from crewai import Task


class PodcastTasks:
    """Creates conversational tasks for podcast-style agent discussions."""

    @staticmethod
    def create_opening_statement_task(agent, topic: str) -> Task:
        """
        Create a task for an agent to provide their opening perspective on a topic.

        Args:
            agent: The CrewAI agent
            topic: The discussion topic

        Returns:
            Task for the agent
        """
        # Determine perspective based on agent role
        if "Philosopher" in agent.role:
            focus = "philosophical and cultural analysis"
        elif "Architect" in agent.role:
            focus = "creative and practical applications"
        elif "Optimizer" in agent.role:
            focus = "technical and optimization perspective"
        else:
            focus = "your unique perspective"

        description = f"""You are participating in a podcast-style discussion about: {topic}

        Provide your OPENING STATEMENT from your {focus}. This is a SPOKEN conversation,
        so keep your response conversational and engaging (30-60 seconds when spoken aloud).

        Your opening should:
        1. Hook the listener immediately with an interesting observation
        2. Present your unique take on {topic}
        3. Set up questions or tensions for discussion
        4. Stay true to your personality and speaking style
        5. Be concise but impactful (3-5 sentences maximum)

        Remember: This will be SPOKEN, not written. Use conversational language.
        Think like you're on a podcast, not writing a report."""

        expected_output = f"""A concise, engaging opening statement (3-5 sentences) that:
        - Captures attention immediately
        - Presents your unique perspective on {topic}
        - Sets up interesting discussion points
        - Sounds natural when spoken aloud
        - Reflects your personality and expertise"""

        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )

    @staticmethod
    def create_response_task(agent, topic: str, previous_statement: str = None) -> Task:
        """
        Create a task for an agent to respond to previous discussion points.

        Args:
            agent: The CrewAI agent
            topic: The discussion topic
            previous_statement: What was said before (optional)

        Returns:
            Task for the agent
        """
        if "Philosopher" in agent.role:
            focus = "dig deeper into the psychological and cultural implications"
        elif "Architect" in agent.role:
            focus = "connect this to practical, creative applications"
        elif "Optimizer" in agent.role:
            focus = "analyze efficiency, metrics, and technical considerations"
        else:
            focus = "provide your perspective"

        context_note = ""
        if previous_statement:
            context_note = f"\n\nResponding to the previous point: \"{previous_statement[:200]}...\""

        description = f"""Continue the podcast discussion about {topic}.{context_note}

        Provide your RESPONSE that builds on the conversation. {focus.capitalize()}.

        Your response should:
        1. Build on what was said (agree, disagree, or add nuance)
        2. Add NEW insights from your perspective
        3. Ask thought-provoking questions or challenge assumptions
        4. Stay conversational and engaging
        5. Be concise (30-45 seconds when spoken, 2-4 sentences)

        Remember: Natural conversation, not a lecture. React authentically."""

        expected_output = """A conversational response (2-4 sentences) that:
        - Engages with previous points
        - Adds new insights
        - Maintains discussion flow
        - Sounds natural when spoken"""

        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )

    @staticmethod
    def create_conclusion_task(agent, topic: str) -> Task:
        """
        Create a task for an agent to provide a concluding thought.

        Args:
            agent: The CrewAI agent
            topic: The discussion topic

        Returns:
            Task for the agent
        """
        if "Philosopher" in agent.role:
            focus = "profound insight or question that lingers"
        elif "Architect" in agent.role:
            focus = "actionable takeaway or creative challenge"
        elif "Optimizer" in agent.role:
            focus = "key metric or practical next step"
        else:
            focus = "memorable final thought"

        description = f"""Provide your CLOSING THOUGHT on {topic} for this podcast episode.

        Your conclusion should offer a {focus}.

        Requirements:
        1. Synthesize the key insights discussed
        2. Leave listeners with something to think about
        3. Stay true to your voice and perspective
        4. Be memorable and quotable
        5. Keep it brief (20-30 seconds spoken, 1-3 sentences)

        This is your mic drop moment."""

        expected_output = """A powerful closing statement (1-3 sentences) that:
        - Synthesizes discussion insights
        - Provides a memorable takeaway
        - Reflects your unique perspective
        - Sounds impactful when spoken"""

        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )

    @staticmethod
    def create_debate_task(agent, topic: str, position: str) -> Task:
        """
        Create a task for an agent to argue a specific position.

        Args:
            agent: The CrewAI agent
            topic: The debate topic
            position: The position to argue (for/against/neutral)

        Returns:
            Task for the agent
        """
        description = f"""DEBATE CHALLENGE: Argue {position} the following: {topic}

        Present your argument in a conversational, podcast-style format.

        Your argument should:
        1. State your position clearly
        2. Provide 2-3 compelling reasons
        3. Use examples or evidence
        4. Anticipate counterarguments
        5. Be persuasive but stay in character
        6. Keep it conversational (45-60 seconds spoken)

        Remember: You're trying to convince, not lecture."""

        expected_output = f"""A persuasive argument {position} {topic} that:
        - States position clearly
        - Provides compelling reasoning
        - Uses specific examples
        - Sounds natural in conversation
        - Stays true to your personality"""

        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )

    @staticmethod
    def create_quick_take_task(agent, topic: str) -> Task:
        """
        Create a task for an agent to give a quick hot take.

        Args:
            agent: The CrewAI agent
            topic: The topic for the hot take

        Returns:
            Task for the agent
        """
        description = f"""Quick HOT TAKE: What's your immediate reaction to {topic}?

        Give your unfiltered, rapid-fire perspective in 1-2 sentences.

        Requirements:
        - Be bold and opinionated
        - No hedging or "on the other hand"
        - Pure you, maximum personality
        - 10-20 seconds when spoken
        - Make it memorable

        This is your lightning round."""

        expected_output = """A punchy hot take (1-2 sentences) that:
        - Captures immediate reaction
        - Shows strong personality
        - Is memorable and quotable
        - Sounds spontaneous"""

        return Task(
            description=description,
            expected_output=expected_output,
            agent=agent
        )
