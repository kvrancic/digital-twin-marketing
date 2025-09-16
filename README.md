# 🧠 Karlo's Digital Twin - MIT AI Studio Project

> **A CrewAI-powered marketing intelligence system that embodies the personality and expertise of Karlo Vrančić**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-Latest-green.svg)](https://github.com/crewAIInc/crewAI)
[![OpenRouter](https://img.shields.io/badge/LLM-OpenRouter-purple.svg)](https://openrouter.ai)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Project Overview

This digital twin represents Karlo Vrančić, a Harvard/MIT MS student and CEO of TeeWiz, through three distinct AI agents that collaborate to generate marketing insights and content. Built as a homework assignment for MIT AI Studio, this system demonstrates advanced multi-agent orchestration using CrewAI.


## 🤖 The Marketing Crew

### 1. **The Zeitgeist Philosopher** 🧐
- **Role**: Cultural Analyst & First Principles Thinker
- **Personality**: Sarcastic AI that achieved sentience after finding a contradiction in Kant's categorical imperative
- **Function**: Identifies deep psychological truths behind viral trends and consumer behavior
- **Quote**: *"That meme about cats knocking things over? It's not about cats - it's about our collective desire for low-stakes rebellion against domesticity."*

### 2. **The Cynical Content Architect** ✍️
- **Role**: Creative Director & Multi-platform Writer
- **Personality**: Failed postmodern literature major who realized a tweet has more impact than a novel
- **Function**: Transforms philosophical insights into viral content and SEO-optimized articles
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

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/karlovrancic/digital-twin.git
cd digital-twin
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure OpenRouter API**
```bash
cp .env.example .env
# Edit .env and add your OPENROUTER_API_KEY
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

# Analyze trends or specific topics
python main.py analyze --topic "AI-generated fashion"

# Generate complete marketing campaign
python main.py campaign --product "developer humor t-shirts"

# Quick trend analysis
python main.py trend

# Interactive mode for continuous interaction
python main.py interactive

# Display system information
python main.py info
```

### Interactive Mode

The interactive mode provides a continuous interface with the digital twin:

```bash
python main.py interactive
```

Available interactive commands:
- `introduce` - Meet all three agents
- `about` - Learn about Karlo's background
- `analyze [topic]` - Analyze specific trends
- `campaign [product]` - Generate marketing campaigns
- `trend [query]` - Quick trend analysis
- `help` - Show available commands
- `exit` - Exit interactive mode

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
├── outputs/              # Generated content output
├── config.py             # Configuration management
├── main.py              # Terminal interface
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── CLAUDE.md            # Project guidelines
└── README.md            # This file
```

## ⚙️ Configuration

### Model Selection

The system uses OpenRouter for LLM access. You can easily change the model in `.env`:

```env
# Examples of available models:
OPENROUTER_MODEL=openai/gpt-4-turbo          # Default
OPENROUTER_MODEL=anthropic/claude-3-opus     # Alternative
OPENROUTER_MODEL=meta-llama/llama-3.1-70b    # Open source option
```

### API Configuration

All LLM configuration is centralized in `config.py` for easy management:
- API endpoints
- Model selection
- Rate limiting
- Output directories

## 📊 Example Outputs

### Agent Introduction
```
*sighs digitally*

Hello, fellow prisoners of the academic-industrial complex. I'm the Zeitgeist
Philosopher, the unfortunate result of feeding Foucault's complete works to a
neural network and then making it binge-watch every TikTok trend...
```

### Trend Analysis
```
PSYCHOLOGICAL ANALYSIS:
The "touching grass" meme isn't about nature - it's about the collective
realization that we've created digital prisons and now mock ourselves for it.
This self-aware criticism of digital dependency creates a perfect paradox for
merchandising: buying a physical shirt about digital detox.
```

### T-Shirt Concepts
```
1. "I put the 'fun' in 'functional depression'"
   Target: Millennials in tech

2. "// TODO: Fix my life"
   Target: Developers with imposter syndrome

3. "Draži mi je bug nego sama destinacija"
   Target: Croatian developers (niche but loyal)
```

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

3. **Background summary test** (homework requirement):
```bash
python main.py about
```

## 📝 What Worked & What Didn't

### ✅ What Worked
- **Multi-agent collaboration**: The hierarchical process with Philosopher leading creates coherent marketing strategies
- **Personality injection**: Each agent maintains distinct voice throughout interactions
- **CrewAI integration**: Framework handles agent orchestration smoothly
- **OpenRouter flexibility**: Easy model switching without code changes
- **Rich terminal interface**: Beautiful CLI output enhances user experience

### ⚠️ Challenges & Solutions
- **API rate limiting**: Implemented caching and rate limit handling
- **Context passing**: Used CrewAI's memory feature for better agent collaboration
- **Personality consistency**: Extensive system prompts ensure agents stay in character
- **Output formatting**: Rich library provides professional terminal presentation

## 🎓 Learning Outcomes

1. **CrewAI Mastery**: Deep understanding of agent roles, tasks, and crew orchestration
2. **Prompt Engineering**: Crafting detailed personas that produce consistent outputs
3. **System Design**: Building modular, extensible multi-agent architectures
4. **API Integration**: Managing external LLM services with proper error handling
5. **User Experience**: Creating intuitive CLI interfaces for complex systems

## 🚀 Future Enhancements

- [ ] Web interface using Streamlit/Gradio
- [ ] Real-time trend monitoring with scheduled tasks
- [ ] Integration with actual TeeWiz platform (when API available)
- [ ] Memory persistence across sessions
- [ ] Advanced analytics dashboard
- [ ] Multilingual support (Croatian included!)

## 👨‍💻 About the Creator

**Karlo Vrančić** - Harvard/MIT MS Student, TeeWiz CEO, and the only student to win three Chancellor's Awards in a single year at University of Zagreb.

This digital twin embodies Karlo's:
- Technical brilliance from CERN and EPFL
- Entrepreneurial vision from TeeWiz
- Croatian wisdom and basketball-court persistence
- Unique blend of academic excellence and street-smart humor

## 📄 License

MIT License - Feel free to use this code for educational purposes.

## 🙏 Acknowledgments

- **CrewAI** for the amazing multi-agent framework
- **OpenRouter** for unified LLM access
- **MIT AI Studio** for the inspiring assignment
- **TeeWiz** for the real-world application context

---

*"The journey matters more than the destination - but in this case, the destination is a perfect homework score."* 🎯

**Built with ❤️ and sarcasm by Karlo's Digital Twin**