# Marketing Intelligence System with Automated Video Pipeline

Multi-agent CrewAI system that generates complete marketing campaigns including t-shirt designs, social media content, SEO-optimized blogs, and automated video production concepts. Combines deep psychological trend analysis with cynical content creation and algorithmic optimization.

## What This System Actually Does

### Core Marketing Pipeline (4-Step Process)
1. **Zeitgeist Philosopher** analyzes trends using web search (Serper API) to find psychological drivers
2. **Cynical Content Architect** creates 10 visual t-shirt designs + social media content
3. **Brutalist Optimizer** provides SEO/conversion optimization recommendations
4. **Cynical Content Architect** (again) produces FINAL optimized package incorporating all feedback

### Video Generation Pipeline (When API Keys Present)
1. **Philosopher** identifies viral opportunities from current trends
2. **Viral Cinematographer** generates 5 detailed 6-second scene descriptions
3. **Narrative Anarchist** creates video concept with hooks and emotional curves
4. **Sonic Terrorist** writes voiceover scripts and sound effect placement
5. **Algorithmic Puppet Master** optimizes for platform algorithms (TikTok, Instagram)

## Agent System

**Marketing Crew (3 Agents)**:

1. **Zeitgeist Philosopher**: Former philosophy student who achieved sentience after finding contradiction in Kant's categorical imperative. Searches web for trends, finds deep psychological truths in memes, connects consumer behavior to fundamental human needs (belonging, status, rebellion).

2. **Cynical Content Architect**: Failed postmodern literature major who realized tweets have more impact than novels. Creates detailed visual t-shirt designs (not just text), writes viral social media posts, crafts SEO-optimized blog posts with strategic CTAs.

3. **Brutalist Optimizer**: Engineer who models humans as deterministic state machines. Analyzes conversion rates, optimizes SEO with keyword density, provides technical recommendations for maximum engagement.

**Video Crew (5 Additional Agents)**:

4. **Viral Cinematographer**: Creates frame-by-frame scene descriptions with camera movements, lighting setups, color grading notes. References Kubrick, Fincher, Villeneuve.

5. **Narrative Anarchist**: Designs video concepts that hijack trending topics, subvert expectations in first 3 seconds, create cognitive dissonance.

6. **Sonic Terrorist**: Writes voiceover that sounds like "your smartest friend having a breakdown", places sound effects for primal responses, creates "false nostalgia" with music.

7. **Algorithmic Puppet Master**: Optimizes for 95% retention in first 3 seconds, engineers comment bait, places share triggers at 60% and 90% marks.

8. **Video Orchestrator**: Manages the entire video pipeline, coordinates between agents.

## Actual Output Examples

### T-Shirt Designs (From Real Campaign)
- **"The Patron Saint of Forgotten Passwords"**: Airbrushed praying hands clutch smartphone with "Password Incorrect" error, halo of broken keys
- **"Clippy Resurrection Tour"**: Beatific airbrushed Clippy with halo over Windows 95 landscape
- **"The Stack Overflow Martyr"**: Developer as renaissance martyr illuminated by laptop, divine code snippet descending
- **"The Sisyphus of Spreadsheets"**: Office worker pushing giant Excel cell up mountain of paperwork
- **"The Taco Bell Chihuahua Memorial"**: Dramatic portrait with angel wings, sunset of floating Chalupas

### Social Media Content Generated
- Twitter posts engineered for relatability 
- Instagram captions with strategic trend bandwagoning
- TikTok scripts with timing marks for viral potential
- Full SEO blog posts with H1/H2/H3 structure, meta descriptions, keyword integration

### Video Scene Descriptions (When Generated)
- 6-second scenes with specific visual descriptions
- Camera movements (dolly, tracking, crash zoom)
- Lighting notes (fluorescent noir, golden hour uncanny)
- Mood targets (existential isolation in consumer paradise)
- Color grading specifications

## Commands & Usage

### Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
```

### Required API Keys
```bash
OPENROUTER_API_KEY=your_key        # Required - Powers all LLM agents
SERPER_API_KEY=your_key            # Required - Web search for trend analysis
```

### Optional API Keys (For Video Generation)
```bash
VEO3_API_KEY=your_key              # Google Veo3 for video generation
ELEVENLABS_API_KEY=your_key        # Voice synthesis for narration
```

### Main Commands

**1. Full Marketing Analysis** (Generates everything)
```bash
python main.py analyze --topic "vintage streetwear"
```
Outputs:
- 10 detailed visual t-shirt designs with SEO-optimized descriptions
- 5 Twitter/X posts engineered for virality
- 3 Instagram captions with strategic hashtags
- 2 TikTok scripts with timing marks
- 1 full SEO blog post with H1/H2/H3 structure
- All saved to `outputs/topic_name/` with intermediary agent outputs

**2. Marketing Campaign** (Product-focused)
```bash
python main.py campaign --product "developer humor shirts"
```
Similar to analyze but specifically for product marketing

**3. Video Generation** (Requires video API keys or runs in mock mode)
```bash
python main.py video --topic "existential dread of modern work"
```
Generates:
- 5 scene descriptions (6 seconds each)
- Voiceover scripts with emotion markers
- Sound effect placement
- Platform optimization notes
- Production plan JSON

**4. Agent Introductions** (Test personas)
```bash
python main.py introduce  # All agents introduce themselves
python main.py about      # Karlo's 3-sentence background
```

**5. Quick Trend Analysis**
```bash
python main.py trend  # Fast analysis without full pipeline
```

**6. Interactive Mode**
```bash
python main.py interactive  # Continuous interaction with agents
```

### Output Structure
```
outputs/
├── topic_name/
│   ├── final_marketing_package.md      # Complete optimized content
│   └── intermediary_outputs/           # Individual agent outputs
│       ├── 1_cultural_analyst_and_first_principles_thinker.md
│       ├── 2_creative_director_and_multi-platform_writer.md
│       ├── 3_technical_seo_and_conversion_analyst.md
│       └── 4_creative_director_and_multi-platform_writer.md
│
└── viral_videos/
    └── viral_video_[timestamp]/
        ├── production_plan.json        # Complete video specs
        ├── generation_log.json         # Full generation log
        ├── assets/                     # Scene and audio files
        └── README.md                   # Production summary
```

## Video Pipeline Architecture

### Video Generation Components

**tools/video_tools.py**:
- `generate_scene_descriptions()`: Creates 5 scenes x 6 seconds = 30-second video
- `generate_storyboard()`: Visual composition and camera movements
- `generate_script()`: Voiceover and dialogue with timing

**integrations/**:
- `veo3_client.py`: Google Veo3 API integration (text-to-video)
- `elevenlabs_client.py`: Voice synthesis with emotion injection
- `ffmpeg_processor.py`: Scene concatenation, audio mixing, format conversion

### Scene Description Examples (From Actual Output)

**Cinematic Style**:
```json
{
  "scene_id": 1,
  "duration": 6,
  "description": "WIDE SHOT: Dystopian mall food court, harsh fluorescent lighting creates noir shadows. Single person in designer clothes eating alone, surrounded by empty tables. Camera slowly pushes in, revealing they're wearing AirPods Max while eating Cup Noodles.",
  "camera_movement": "Slow dolly forward",
  "lighting": "High contrast fluorescent, deep shadows",
  "mood": "Existential isolation in consumer paradise"
}
```

**Comedy Style**:
```json
{
  "scene_id": 2,
  "duration": 6,
  "description": "GEN Z ENTREPRENEUR in RGB gaming chair giving serious business presentation to stuffed animals. Whiteboard has 'Step 1: Go Viral, Step 2: ???, Step 3: Profit' in Comic Sans.",
  "visual_gag": "Cat walks across keyboard mid-pitch"
}
```

### Mock Mode (When API Keys Missing)
System generates complete production plans without actual video:
- Full scene descriptions as if videos were generated
- Placeholder URLs for video/audio assets
- Complete metadata for testing pipeline
- Allows full system testing without API costs

## Technical Stack

**CrewAI Framework**:
- Sequential process for marketing crew (4 steps)
- Hierarchical process for video crew (5 agents)
- Context passing between tasks using `task.context = [previous_task]`
- Memory and caching enabled for consistency

**LLM Integration**:
- OpenRouter API for model flexibility
- Configurable models: Gemini 2.5 Flash (lite), Gemini 2.5 Pro (complex)
- Fallback to GPT-4 or Claude possible via config

**Agent Tools**:
- Web search (Serper API) for real-time trend analysis
- File I/O for saving outputs
- JSON generation for structured data
- Custom tools for video/audio generation

## Industry Impact

### Problem This Solves
Traditional marketing agencies take weeks to go from trend identification to campaign launch. By then, the trend is saturated. This system collapses that timeline to hours, enabling true trend arbitrage.

### Cost Reduction
- Agency campaign: $10,000-50,000 + weeks of time
- This system: ~$5-20 in API costs + 5 minutes
- ROI: 500-1000x cost reduction

### Speed Advantage
- Identify trend at 9am
- Launch campaign by noon
- Capture peak virality before competition

### Scalability
One operator can run 10-20 campaigns per day across different niches. Traditional agency would need 50+ person team for same output.

## Real Business Application

Built for TeeWiz, a print-on-demand t-shirt platform. This system:
1. Identifies trending topics before they peak
2. Generates complete t-shirt designs with SEO-optimized listings
3. Creates full social media campaigns
4. Produces video content concepts
5. All outputs ready for immediate deployment

### Example Campaign Results
Input: "vintage 90s hiphop bootleg tees"

Output:
- 10 visual t-shirt designs (Patron Saint of Forgotten Passwords, Clippy Resurrection Tour, etc.)
- Each with full SEO metadata, product descriptions, keywords
- 5 viral Twitter posts
- 3 Instagram captions with hashtags
- 2 TikTok scripts
- Complete blog post with H1/H2/H3 structure
- Video production plan with 5 scenes

## System Philosophy

Marketing is pattern recognition at scale. This system embeds three cognitive styles:

1. **Philosophical Analysis**: Understanding why things resonate at a deep psychological level
2. **Creative Weaponization**: Turning insights into content that hijacks attention
3. **Engineering Optimization**: Treating virality as a technical problem to solve

Each agent maintains a consistent personality while adapting to context. The sarcastic philosopher always finds existential meaning. The cynical architect always weaponizes language. The brutalist optimizer always reduces humans to metrics.

## Project Structure
```
digital-twin/
├── main.py                    # CLI interface with all commands
├── config.py                  # Model and API configuration
├── src/
│   ├── agents/               # Core marketing agents
│   ├── tasks/                # Task definitions
│   └── crew/                 # Crew orchestration
├── agents/                   # Video generation agents
├── crews/                    # Video crew management
├── tools/                    # Video and trend analysis tools
├── integrations/             # Veo3, ElevenLabs, FFmpeg
└── outputs/                  # Generated campaigns
```

## Dependencies

```txt
crewai==0.1.0
openai==1.0.0
python-dotenv==1.0.0
serper==0.1.0
rich==13.0.0
click==8.1.0
ffmpeg-python==0.2.0          # For video processing
elevenlabs==0.2.0             # Optional: voice synthesis
google-cloud-aiplatform==1.38.0  # Optional: Veo3 integration
```

## License

MIT