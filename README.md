# 🧠 Karlo's Digital Twin - MIT AI Studio CrewAI Homework

> **BUILD YOUR DIGITAL TWIN WITH CREWAI - A Multi-Agent Marketing System**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-Latest-green.svg)](https://github.com/crewAIInc/crewAI)
[![OpenRouter](https://img.shields.io/badge/LLM-OpenRouter-purple.svg)](https://openrouter.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Quick note: I also made another project with CrewAI: [Interview Analyzer & Archiver](https://github.com/kvrancic/interview-analyzer-archiver)

## 📚 HOMEWORK REQUIREMENTS MET

✅ **CrewAI Framework Used** - Agents, Tasks, Crews, Tools, Context Passing
✅ **Agents Defined** - 3 agents with roles, goals, backstories, and personas reflecting me
✅ **Tasks Created** - Marketing tasks with descriptions and expected outputs
✅ **Crews Orchestrated** - 4-step pipeline with proper agent collaboration
✅ **Test Prompts Working** - `introduce` and `about` commands fully functional
✅ **Web Search Tool** - Integrated Serper API for trend analysis
✅ **Documentation Complete** - Comprehensive README with learnings
✅ **Code Well-Commented** - Clean, modular architecture
✅ **GitHub Repository** - All code available and organized
✅ **ZIP File Ready** - Complete package for submission

## 🎯 Project Overview

This homework demonstrates advanced multi-agent orchestration using CrewAI as required by the MIT AI Studio assignment. The digital twin consists of three AI agents that reflect my personality and work together in a 4-step pipeline to generate marketing insights and visual t-shirt designs for TeeWiz, my custom t-shirt platform.

### 🔥 Key Features

- **4-Step Marketing Pipeline**: Philosopher → Architect → Optimizer → Architect (Final)
- **Visual T-Shirt Designs**: Generates detailed graphic designs for DTG front-print
- **Complete Marketing Package**: T-shirts, social media content, SEO-optimized blogs
- **Intelligent Context Passing**: Each agent builds on previous work
- **Structured Output**: Organized folders with final and intermediary outputs
- **Web Search Integration**: Uses Serper API for real-time trend analysis

## 🤖 The Marketing Crew

**NOTE: All of these agents are made to resemble me, my interests, and my personality in a very exaggerated way.**

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

## 💻 Usage - Homework Test Commands

### Required Test Prompts (from homework)

```bash
# HOMEWORK TEST 1: "introduce yourself to the class"
python main.py introduce
# Each agent introduces themselves with their unique persona

# HOMEWORK TEST 2: "explain my background in 3 sentences"
python main.py about
# Returns Karlo's background: Harvard/MIT student, TeeWiz co-founder, Croatian origin
```

### Full Pipeline Commands

```bash
# Run complete 4-step marketing analysis pipeline
python main.py analyze --topic "[any topic]"
# Generates: T-shirt designs, Justin Bieber, social content, SEO blog

# Create full marketing campaign
python main.py campaign --product "[product description]"
# Generates: Complete marketing strategy with all content

# Display system configuration and agent info
python main.py info
# Shows: Agent details, API configuration, system status
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

## 🎨 What Each Command Provides

### `python main.py introduce`
- All three agents introduce themselves sequentially
- Demonstrates agent personas and backstories
- Shows CrewAI agent implementation

### `python main.py about`
- Returns 3-sentence summary about Karlo
- Covers: Education (Harvard/MIT), Business (TeeWiz), Background (Croatia)
- Uses lightweight LLM for efficiency

### `python main.py analyze --topic "[topic]"`
- Executes full 4-step pipeline:
  1. Philosopher searches web and analyzes cultural significance
  2. Architect creates 10 visual t-shirt designs
  3. Optimizer provides SEO/conversion recommendations
  4. Architect produces FINAL optimized package
- Saves all outputs to `outputs/[topic]/` folder

### `python main.py campaign --product "[product]"`
- Similar to analyze but product-focused
- Creates complete marketing strategy
- Includes market positioning and competitive analysis

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

## 📊 Output Format Details

### Each Analysis Generates:

**T-SHIRT DESIGNS (10 concepts)**
- Detailed visual descriptions for DTG printing
- Front-print graphics with clever text
- Target audience specifications
- Mockup-ready descriptions

**SOCIAL MEDIA PACKAGE**
- 5 Twitter/X posts with engagement hooks
- 3 Instagram captions with hashtag strategy
- 2 TikTok video scripts with viral potential

**SEO BLOG POST**
- Title (50-60 characters)
- Meta description for search CTR
- Full article structure (H1/H2/H3)
- Keyword optimization
- Strategic CTA placement

## 🧪 Testing the Homework Requirements

### 1. **Verify CrewAI Installation**:
```bash
python main.py info
# Shows all agents and their configurations
```

### 2. **Test Required Prompts**:
```bash
# REQUIRED: "introduce yourself to the class"
python main.py introduce

# REQUIRED: "explain my background in 3 sentences"
python main.py about
```

### 3. **Test Full Agent Collaboration**:
```bash
python main.py analyze --topic "test run"
# Verifies all agents work together properly
```

## 📝 Documentation (Homework Requirement)

### ✅ What Worked
- **CrewAI Framework**: Successfully implemented agents with roles, goals, and backstories
- **Agent Personas**: Each agent reflects aspects of my personality (sarcasm, psychology insights, engineering mindset)
- **Task Orchestration**: 4-step pipeline with proper context passing between agents
- **Web Search Tool**: Integrated Serper API for real-time trend analysis
- **Test Prompts**: Both "introduce" and "about" commands work as required
- **Output Management**: Structured folder system with intermediary and final outputs

## 🎓 What I Learned (Homework Requirement)

1. **CrewAI Capabilities**:
   - Agents can have complex personas that affect output quality
   - Tasks need explicit context passing to share information
   - Crews orchestrate multi-step workflows effectively

2. **Agent Design Insights**:
   - Strong backstories create more consistent outputs
   - Personality traits must be reinforced in prompts
   - Tools (like web search) significantly enhance agent capabilities

3. **Technical Learnings**:
   - OpenRouter provides flexible LLM access without vendor lock-in
   - Hierarchical process flow creates better outputs than parallel execution
   - Saving intermediary outputs helps debug and understand agent thinking

4. **Practical Applications**:
   - This system can generate real marketing content for TeeWiz
   - Multi-agent systems excel at complex, multi-faceted tasks
   - Context passing is crucial for coherent multi-step outputs

## 📄 License

MIT License - Feel free to use this code for educational purposes.

## 🙏 Acknowledgments

- **CrewAI** for the powerful multi-agent framework
- **OpenRouter** for unified LLM access
- **Serper** for web search capabilities
- **MIT AI Studio** for the inspiring assignment
- **TeeWiz** for the real-world application context

---