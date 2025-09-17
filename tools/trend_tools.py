from crewai.tools import tool
import json
from datetime import datetime


@tool("Trend Analysis Tool")
def analyze_trends(query: str = "") -> str:
    """
    Analyzes current viral trends across social media platforms.
    Returns trending topics, hashtags, and viral content patterns.
    Perfect for finding what's hot right now and what will sell t-shirts.

    Args:
        query: Optional query string to filter trends

    Returns:
        JSON string with current trends and analysis
    """
    mock_trends = {
        "timestamp": datetime.now().isoformat(),
        "viral_topics": [
            {
                "topic": "AI girlfriend simulator breakups",
                "engagement": "8.2M views",
                "sentiment": "darkly humorous",
                "meme_potential": "extreme",
                "description": "People posting their AI companion breakup texts"
            },
            {
                "topic": "Mediterranean diet but make it midwest",
                "engagement": "5.1M views",
                "sentiment": "ironically wholesome",
                "meme_potential": "high",
                "description": "Ranch dressing on everything Greek"
            },
            {
                "topic": "Main character syndrome documentary",
                "engagement": "12.3M views",
                "sentiment": "self-aware cringe",
                "meme_potential": "extreme",
                "description": "Everyone thinks they're the protagonist"
            },
            {
                "topic": "Corporate speak as love language",
                "engagement": "3.7M views",
                "sentiment": "dystopian romance",
                "meme_potential": "high",
                "description": "Circle back on that kiss, synergize our hearts"
            },
            {
                "topic": "Therapy speak gone wrong",
                "engagement": "9.4M views",
                "sentiment": "chaotic enlightenment",
                "meme_potential": "extreme",
                "description": "That's toxic, bestie - everything is gaslighting now"
            }
        ],
        "viral_formats": [
            "POV videos with unexpected twists",
            "Before/After but the after is worse",
            "Explaining Gen Alpha slang to millennials",
            "Rating things that shouldn't be rated",
            "Day in the life but increasingly unhinged"
        ],
        "trending_sounds": [
            "Sigma phonk remix of classical music",
            "That one TikTok sound everyone uses incorrectly",
            "Dramatic orchestral for mundane activities",
            "Sped up 2000s throwbacks",
            "AI generated meditation gone wrong"
        ],
        "aesthetic_trends": [
            "Dark academia but you failed the class",
            "Cottagecore in a capitalist hellscape",
            "Y2K but with existential dread",
            "Clean girl who's actually messy",
            "Mob wife but make it suburban"
        ]
    }

    if query:
        mock_trends["user_context"] = f"Analyzed for: {query}"

    return json.dumps(mock_trends, indent=2)


@tool("Viral Content Pattern Analyzer")
def analyze_viral_patterns(topic: str) -> str:
    """
    Analyzes what makes content go viral right now.
    Identifies hooks, formats, and psychological triggers.
    Your secret weapon for creating content that hits.

    Args:
        topic: Topic to analyze viral patterns for

    Returns:
        JSON string with viral content patterns and insights
    """
    patterns = {
        "topic": topic,
        "viral_hooks": [
            "Nobody talks about this but...",
            "I was today years old when I learned...",
            "The [thing] they don't want you to know",
            "POV: You're [relatable situation]",
            "Tell me you're [X] without telling me you're [X]",
            "It's giving [unexpected comparison]"
        ],
        "psychological_triggers": [
            "FOMO - everyone else knows this already",
            "Tribal belonging - us vs them mentality",
            "Parasocial validation - your internet bestie agrees",
            "Cognitive dissonance - contradictory truths",
            "Nostalgic regression - childhood but corrupted",
            "Ironic detachment - caring is cringe"
        ],
        "engagement_patterns": {
            "optimal_length": "15-30 seconds for max retention",
            "hook_timing": "First 3 seconds are everything",
            "reveal_structure": "Setup, misdirection, punchline",
            "comment_bait": "Intentional minor errors drive engagement",
            "share_triggers": "Make viewers look smart/funny when sharing"
        },
        "platform_specific": {
            "tiktok": "Quick cuts, trending audio, text overlay",
            "instagram": "Carousel with plot twist on slide 3",
            "youtube_shorts": "MrBeast thumbnail strategy",
            "twitter": "Quote tweet bait with hot takes"
        },
        "content_formula": {
            "structure": "Hook + Context + Twist + Call to Action",
            "emotion_curve": "Curiosity -> Recognition -> Surprise -> Satisfaction",
            "shareability_factors": [
                "Makes sharer look culturally aware",
                "Validates viewer's worldview",
                "Too spicy to not share",
                "Perfectly captures a vibe"
            ]
        }
    }

    return json.dumps(patterns, indent=2)


@tool("Competitor Viral Analysis")
def analyze_competitor_viral(industry: str = "apparel") -> str:
    """
    Analyzes what's working for other brands right now.
    Identifies gaps in the market and opportunities.
    Your intelligence operation for content warfare.

    Args:
        industry: Industry to analyze (default: apparel)

    Returns:
        JSON string with competitor analysis and opportunities
    """
    analysis = {
        "industry": industry,
        "viral_campaigns": [
            {
                "brand": "Generic Streetwear Co",
                "campaign": "Unhinged customer service responses",
                "performance": "23M impressions",
                "why_it_worked": "Brand became the funny friend, not a company",
                "steal_this": "Personality over polish"
            },
            {
                "brand": "Fast Fashion Giant",
                "campaign": "Employees rating outfits brutally honest",
                "performance": "45M views",
                "why_it_worked": "Self-aware about fast fashion criticism",
                "steal_this": "Lean into your contradictions"
            },
            {
                "brand": "Luxury But Accessible",
                "campaign": "Rich vs Broke same outfit",
                "performance": "67M views",
                "why_it_worked": "Class consciousness but make it fashion",
                "steal_this": "Address the elephant in the room"
            }
        ],
        "content_gaps": [
            "Nobody's doing brutalist fashion comedy",
            "Untapped market for existential dread merch",
            "Philosophy memes x streetwear crossover virgin territory",
            "Anti-influencer influencer marketing paradox unexplored"
        ],
        "opportunities": [
            "TikTok hasn't discovered ironic motivational fashion yet",
            "Instagram Reels algorithm loves fashion + unexpected audio",
            "Twitter fashion discourse is undermonetized",
            "YouTube Shorts fashion content is still nascent"
        ],
        "risk_factors": [
            "Cancel culture moves fast in fashion",
            "Trend cycles now measured in hours not seasons",
            "Authenticity theater harder to maintain",
            "Platform algorithm changes can kill overnight"
        ]
    }

    return json.dumps(analysis, indent=2)


# Create tool instances for export
TrendAnalysisTool = analyze_trends
ViralContentPatternTool = analyze_viral_patterns
CompetitorViralAnalysisTool = analyze_competitor_viral