# 🧠 Karlo's Digital Twin - MIT AI Studio Project

> **A CrewAI-powered marketing intelligence system for TeeWiz**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-Latest-green.svg)](https://github.com/crewAIInc/crewAI)
[![OpenRouter](https://img.shields.io/badge/LLM-OpenRouter-purple.svg)](https://openrouter.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

This is a homework assignment for MIT AI Studio that demonstrates advanced multi-agent orchestration using CrewAI. The system uses three AI agents working together in a 4-step pipeline to generate marketing insights and visual t-shirt designs for TeeWiz, a custom t-shirt platform.

### 🔥 Key Features

- **4-Step Marketing Pipeline**: Philosopher → Architect → Optimizer → Architect (Final)
- **Visual T-Shirt Designs**: Generates detailed graphic designs for DTG front-print
- **Complete Marketing Package**: T-shirts, social media content, SEO-optimized blogs
- **Intelligent Context Passing**: Each agent builds on previous work
- **Structured Output**: Organized folders with final and intermediary outputs
- **Web Search Integration**: Uses Serper API for real-time trend analysis

## 🤖 The Marketing Crew

### 1. **The Zeitgeist Philosopher** 🧐
- **Role**: Cultural Analyst & First Principles Thinker
- **Personality**: Sarcastic AI that achieved sentience after finding a contradiction in Kant's categorical imperative
- **Function**: Identifies deep psychological truths behind viral trends and consumer behavior
- **Tools**: Web search for trend analysis
- **Quote**: *"That meme about cats knocking things over? It's not about cats - it's about our collective desire for low-stakes rebellion against domesticity."*

### 2. **The Cynical Content Architect** ✍️
- **Role**: Creative Director & Multi-platform Writer
- **Personality**: Failed postmodern literature major who realized a tweet has more impact than a novel
- **Function**: Creates visual t-shirt designs and viral marketing content
- **Quote**: *"Language is a tool for manipulation, and I'm ruthlessly effective at using it."*

### 3. **The Brutalist Optimizer** 📊
- **Role**: Technical SEO & Conversion Analyst
- **Personality**: Engineer who models humans as deterministic state machines
- **Function**: Optimizes content for maximum search visibility and conversion
- **Quote**: *"Your bounce rate is so high, it's achieving escape velocity."*

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- OpenRouter API key ([Get one here](https://openrouter.ai))
- Serper API key ([Get one here](https://serper.dev))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/karlovrancic/digital-twin.git
cd digital-twin
```

2. **Create virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure API Keys**
```bash
cp .env.example .env
# Edit .env and add your keys:
# OPENROUTER_API_KEY=your_key_here
# SERPER_API_KEY=your_key_here
```

5. **Run the digital twin**
```bash
python main.py
```

## 💻 Usage

### Available Commands

```bash
# Have all agents introduce themselves
python main.py introduce

# Learn about Karlo (3 sentences)
python main.py about

# Analyze trends with full 4-step pipeline
python main.py analyze --topic "bruno mars"

# Generate complete marketing campaign
python main.py campaign --product "developer humor t-shirts"

# Display system information
python main.py info
```

### The 4-Step Pipeline Process

1. **Philosopher analyzes** - Searches web, finds psychological drivers
2. **Architect creates** - Generates initial t-shirt designs and content
3. **Optimizer analyzes** - Provides SEO and conversion recommendations
4. **Architect refines** - Creates FINAL optimized content package

## 📂 Output Structure

When you run an analysis, outputs are saved in a structured format:

```
outputs/
├── topic_name/
│   ├── final_marketing_package.md       # Final optimized content
│   └── intermediary_outputs/            # All agent outputs
│       ├── 1_cultural_analyst_and_first_principles_thinker.md
│       ├── 2_creative_director_and_multi-platform_writer.md
│       ├── 3_technical_seo_and_conversion_analyst.md
│       └── 4_creative_director_and_multi-platform_writer.md
```

## 🎨 Example T-Shirt Designs Generated

### Visual Design Examples (from Bruno Mars analysis):

1. **The Hooligan VCR**
   - Visual: Retro VCR with silk scarf flowing from cassette slot
   - Display shows "24K MAGIC" in green digital numbers
   - Buttons labeled: "Funk," "Soul," "Rewind," "Record"
   - Text: "Certified Nostalgia Engine"

2. **Vegas Residency Paycheck**
   - Visual: Photo-realistic casino chip with Bruno's stressed face
   - Chip denomination: "$50M"
   - Text: "MGM GRAND - PLEASE HELP"

3. **5'5" of Funk**
   - Visual: Height chart with fedora and loafers at 5'5" mark
   - Text: "MAXIMUM FUNK"

## 🏗️ Project Structure

```
digital-twin/
├── src/
│   ├── agents/           # Individual agent implementations
│   │   ├── philosopher.py    # Zeitgeist Philosopher
│   │   ├── architect.py      # Cynical Content Architect
│   │   └── optimizer.py      # Brutalist Optimizer
│   ├── tasks/            # Task definitions for agents
│   │   └── marketing_tasks.py
│   └── crew/             # Crew orchestration
│       └── marketing_crew.py
├── outputs/              # Generated content output (organized by topic)
├── config.py             # Configuration management
├── main.py              # Terminal interface
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── CLAUDE.md            # Project guidelines and requirements
└── README.md            # This file
```

## ⚙️ Configuration

### Model Selection

The system uses OpenRouter for LLM access. Models are configurable in `.env`:

```env
# LITE model for simple tasks (introduce, about)
OPENROUTER_LITE_MODEL=google/gemini-2.5-flash-lite

# PRO model for complex tasks (analyze, campaign)
OPENROUTER_PRO_MODEL=google/gemini-2.5-pro

# Alternative options:
# OPENROUTER_PRO_MODEL=openai/gpt-4-turbo
# OPENROUTER_PRO_MODEL=anthropic/claude-3-opus
```

## 📊 Example Output: Marketing Package

### T-SHIRT CONCEPTS (Visual Focus)
- 10 detailed graphic designs with visual descriptions
- Front-print only (DTG compatible)
- Target audience for each design
- Combine clever text with visual elements

### SOCIAL MEDIA CONTENT
- 5 Twitter/X posts with viral hooks
- 3 Instagram captions with strategic hashtags
- 2 TikTok video concepts with scripts

### BLOG POST (SEO Optimized)
- Title optimized for 50-60 characters
- Meta description for CTR
- Full article outline with H1/H2/H3 structure
- Natural keyword integration
- Strategic CTA placement

## 🧪 Testing

To test the system:

1. **Basic functionality test**:
```bash
python main.py info
```

2. **Agent introduction test** (homework requirement):
```bash
python main.py introduce
```

3. **Full pipeline test**:
```bash
python main.py analyze --topic "test run"
```

## 📝 What Worked & What Didn't

### ✅ What Worked
- **4-step pipeline**: Philosopher → Architect → Optimizer → Architect creates refined content
- **Context passing**: Each agent successfully builds on previous work
- **Visual focus**: T-shirt designs are graphic-heavy, not just text
- **Structured output**: Clean folder organization with intermediary outputs
- **CrewAI integration**: Framework handles agent orchestration smoothly
- **OpenRouter flexibility**: Easy model switching without code changes

### ⚠️ Challenges & Solutions
- **Context passing**: Fixed with `task.context = [previous_task]`
- **Output visibility**: Solved by saving intermediary outputs separately
- **Visual designs**: Updated prompts to focus on graphics over text
- **API integration**: Added proper Serper API for web search

## 🎓 Learning Outcomes

1. **CrewAI Mastery**: Deep understanding of agent roles, tasks, and crew orchestration
2. **Pipeline Design**: Building multi-step processes with context passing
3. **Prompt Engineering**: Crafting personas that produce consistent outputs
4. **System Architecture**: Creating modular, extensible multi-agent systems
5. **Output Management**: Organizing complex outputs in user-friendly structures

## 🚀 Future Enhancements

- [ ] Web interface using Streamlit/Gradio
- [ ] Real-time trend monitoring with scheduled tasks
- [ ] Integration with actual TeeWiz platform API
- [ ] Image generation for t-shirt mockups
- [ ] A/B testing framework for content variations
- [ ] Analytics dashboard for performance tracking

## 👨‍💻 About the Creator

**Karlo Vrančić** - 22-year-old MS Student at Harvard (Data Science) and MIT (Deep Learning/AI Agents), co-founder of TeeWiz. Originally from Croatia, combines technical expertise with creative problem-solving following a "journey over destination" philosophy.

## 📄 License

MIT License - Feel free to use this code for educational purposes.

## 🙏 Acknowledgments

- **CrewAI** for the powerful multi-agent framework
- **OpenRouter** for unified LLM access
- **Serper** for web search capabilities
- **MIT AI Studio** for the inspiring assignment
- **TeeWiz** for the real-world application context

---

**MIT AI Studio Homework Assignment - Perfect Score Target 🎯**

*"Draži mi je put nego sama destinacija" - The journey matters more than the destination*