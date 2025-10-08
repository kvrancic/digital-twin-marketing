# HW4: Multimodal Agent - Voice Capabilities

**Student:** Karlo Vrančić
**Course:** MIT AI Studio
**Date:** October 2025

---

## Quick Start

### Prerequisites
- Python 3.9 or higher
- OpenRouter API key ([Get one here](https://openrouter.ai))
- Serper API key ([Get one here](https://serper.dev))
- **OpenAI API key** ([Get one here](https://platform.openai.com/api-keys)) - for Whisper STT
- **PortAudio installed** (`brew install portaudio` on macOS) - for microphone access

### Installation

```bash
# Clone repository
git clone https://github.com/karlovrancic/digital-twin.git
cd digital-twin

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install PortAudio (macOS)
brew install portaudio

# Configure API keys
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY and OPENROUTER_API_KEY
```

### Voice Commands

```bash
# Automated podcast (agents discuss among themselves)
python main.py voice-chat
python main.py voice-chat --topic "AI and creativity"

# Interactive podcast (you participate in the discussion!)
python main.py voice-chat --interactive
python main.py voice-chat --interactive --topic "AI ethics"

# Test your setup
python main.py test-mic       # Test microphone
python main.py test-voices    # Test TTS voices
```

**For detailed testing instructions, see [TESTING.md](TESTING.md)**

### What Each Voice Command Does

**`python main.py test-mic`**
- Records 3 seconds of audio from your microphone
- Plays it back to verify recording works
- Confirms microphone is properly configured

**`python main.py test-voices`**
- Each agent speaks a test phrase in their unique voice
- Philosopher: `en-US-AvaNeural` (warm, conversational female)
- Architect: `en-US-GuyNeural` (casual, engaging male)
- Optimizer: `en-GB-MaisieNeural` (analytical British female)
- Verifies TTS system is working

**`python main.py voice-chat`**
- Automated podcast mode: agents discuss among themselves
- You provide topic (voice or text)
- Three agents engage in spoken discussion
- Transcript saved to `outputs/podcast_[topic].md`

**`python main.py voice-chat --interactive`**
- Interactive mode: you participate in the discussion
- Choose who speaks next (you or any agent)
- Contribute via voice input (press Enter to stop)
- Full conversation saved with your contributions

**`python main.py voice-chat --topic "text"`**
- Skip voice input for topic
- Provide topic as command-line argument
- Works with both automated and interactive modes

---

## 1. Implementation Overview

This project extends my previous Digital Twin (HW1-HW3) with voice interaction capabilities, enabling speech-to-text input and text-to-speech output. The system now supports a **podcast-style discussion mode** where three distinct AI agents (Zeitgeist Philosopher, Cynical Content Architect, and Brutalist Optimizer) engage in spoken conversations, each with their own unique voice.

### Key Features Added

1. **Speech-to-Text (STT):** OpenAI Whisper API for transcribing user voice input
2. **Text-to-Speech (TTS):** Microsoft Edge TTS with multiple neural voices for agent differentiation
3. **Podcast Mode:** Multi-agent discussions with turn-taking and voice synthesis
4. **Interactive Podcast:** User participates in discussions via voice input
5. **Real-time Voice I/O:** Microphone recording with manual stop control (press Enter)

### Architecture

```
Digital Twin Voice System
│
├── Audio Layer (src/voice/audio_utils.py)
│   ├── AudioRecorder: Microphone capture with silence detection
│   └── AudioPlayer: Speaker output for synthesized speech
│
├── STT Layer (src/voice/stt.py)
│   └── WhisperSTT: OpenAI Whisper API integration
│
├── TTS Layer (src/voice/tts.py)
│   └── EdgeTTS: Multi-voice neural synthesis (3 unique voices)
│
├── Orchestration (src/voice/podcast_orchestrator.py)
│   └── PodcastOrchestrator: Manages automated agent discussions
│
└── Interactive Mode (src/voice/interactive_podcast.py)
    └── InteractivePodcast: User participates in discussions
```

---

## 2. How Voice Interaction Works

### A. Speech-to-Text Implementation

**Library Used:** OpenAI Whisper API (via `openai` Python package)

**Implementation Details:**
- Uses OpenAI's cloud-based Whisper model (`whisper-1`)
- Supports multiple audio formats (WAV, MP3, MP4)
- Transcribes with high accuracy for English language input
- Returns plain text transcriptions

**Code Flow:**
```python
# User speaks into microphone
audio_file = AudioRecorder().record_to_file()

# Whisper transcribes to text
stt = WhisperSTT(api_key=Config.OPENAI_API_KEY)
transcript = stt.transcribe(audio_file)

# Text is processed by agents
```

**Why Whisper?**
- Industry-leading accuracy for speech recognition
- Handles various accents and background noise well
- Simple API integration with minimal code
- Cloud-based means no local model management

### B. Text-to-Speech Implementation

**Library Used:** Microsoft Edge TTS (via `edge-tts` package)

**Implementation Details:**
- Cloud-based neural TTS (free Microsoft service)
- High-quality neural voices with natural intonation
- 24kHz sample rate for clear audio quality
- Async synthesis with minimal latency
- No setup required - works out of the box

**Voice Assignment:**
- **Zeitgeist Philosopher** → `en-US-AvaNeural` (warm, conversational female voice)
- **Cynical Content Architect** → `en-US-GuyNeural` (casual, engaging male voice)
- **Brutalist Optimizer** → `en-GB-MaisieNeural` (analytical British female voice)

**Code Flow:**
```python
# Agent generates text response
text = "Your bounce rate is achieving escape velocity."

# Edge TTS synthesizes with agent-specific voice
tts = EdgeTTS()
audio = tts.speak_as_agent(text, agent_name='optimizer')

# Audio is played through speakers
AudioPlayer().play(audio)
```

**Why Edge TTS?**
- Free Microsoft cloud service (no API key needed)
- High-quality neural voices with natural prosody
- Multiple voice options for agent differentiation
- No local model downloads or setup
- Works cross-platform with simple installation

### C. Podcast Orchestration

**Two Modes Available:**

#### 1. Automated Podcast Mode
Agents discuss among themselves while you listen.

**How it Works:**
1. **Input:** User speaks a topic or types it
2. **Transcription:** Whisper converts speech → text
3. **Round 1 - Openings:** Each agent provides opening statement
   - Text generated by LLM
   - Synthesized with agent's unique voice
   - Played sequentially
4. **Round 2+ - Discussion:** Agents respond to each other
   - Previous statements provided as context
   - Natural conversation flow
5. **Final Round - Conclusions:** Each agent summarizes
6. **Output:** Full transcript saved to markdown file

**Turn-Taking Logic:**
```python
for agent_name in ['philosopher', 'architect', 'optimizer']:
    # Generate response
    task = create_response_task(agent, topic, previous_statement)
    response = execute_task(task)

    # Speak it aloud
    tts.speak_as_agent(response, agent_name)

    # Next agent responds to this
    previous_statement = response
```

#### 2. Interactive Podcast Mode (NEW!)
You participate in the discussion alongside the agents.

**How it Works:**
1. **Input:** Provide topic (text or voice)
2. **Interactive Loop:** After each speaker:
   - **Menu appears:** Choose who speaks next
     - [1] You (voice input)
     - [2] Philosopher
     - [3] Architect
     - [4] Optimizer
     - [5] End discussion
3. **Your Turn:** When you speak:
   - Press Enter to start recording
   - Speak your thoughts
   - Press Enter again to stop
   - Whisper transcribes your input
   - Your contribution added to discussion
4. **Agent Turn:** When agent speaks:
   - Agent responds to previous speaker
   - Response synthesized and played
   - Agent's text shown on screen
5. **Output:** Complete transcript with all contributions saved

**Interactive Flow:**
```python
while not ended:
    choice = get_user_choice()

    if choice == 'user':
        audio = recorder.record_manual()  # Stop with Enter key
        text = stt.transcribe(audio)
        add_to_transcript(speaker='user', text=text)

    elif choice == 'agent':
        response = agent.respond(previous_text)
        tts.speak(response, agent_voice)
        add_to_transcript(speaker=agent_name, text=response)
```

---

## 3. Example Run Explanation

### Example 1: Automated Podcast

**Command Used:**
```bash
python main.py voice-chat --topic "AI agents and the future of work"
```

### What Happened:

**Step 1: Topic Input**
- User types topic: "AI agents and the future of work"
- (Alternative: user speaks topic, Whisper transcribes)

**Step 2: Opening Statements (Round 1)**

**🧐 Zeitgeist Philosopher** (voice: en-US-AvaNeural):
> "Oh look, another panic about automation. How delightfully predictable. But here's the thing - humans aren't afraid of AI taking jobs. They're afraid of being forced to admit they've been treating work as their primary source of meaning in a meaningless universe. The real disruption isn't technological; it's existential."

**✍️ Cynical Content Architect** (voice: en-US-GuyNeural):
> "The philosopher's right, and corporations know it. That's why 'AI will augment, not replace' became the most repeated lie of 2024. People don't want augmentation - they want security. And we're selling them stories about collaboration when we should be redesigning what work means entirely."

**📊 Brutalist Optimizer** (voice: en-GB-MaisieNeural):
> "Your emotional narratives aside, the data is clear: 47% of current jobs will be automated by 2030. The inefficiency isn't in the automation itself - it's in pretending it won't happen. Optimal strategy: retrain for non-automatable skills. Humans excel at creativity, empathy, complex problem-solving. Focus there."

**Step 3: Discussion Round 2**

Each agent responds to the previous points, building on the conversation...

**Step 4: Conclusions**

Each agent provides a final thought that synthesizes the discussion.

**Step 5: Output**
- Transcript saved to `outputs/podcast_ai_agents_and_the_future_of_work.md`
- User can review the written record of the spoken discussion

### Insights from This Run:

1. **Multi-voice differentiation works:** Each agent sounds distinct, making it easy to follow who's speaking
2. **Conversational flow is natural:** Agents build on each other's points, not just repeating ideas
3. **Personality shines through:** Even in spoken form, each agent maintains their character (sarcastic philosopher, cynical architect, data-driven optimizer)
4. **Podcast format is engaging:** More interesting than reading three separate reports
5. **Technical performance:** Minimal latency between speakers, clear audio quality

---

### Example 2: Interactive Podcast - Full Walkthrough

**Command Used:**
```bash
python main.py voice-chat --interactive --topic "AI ethics"
```

### Complete Conversation Flow:

**Step 1: Topic Input**
```
🎙️  Speak your topic, or type it (press Enter to speak):
[User speaks: "AI ethics"]
✓ Transcribed: "AI ethics"

Starting interactive podcast on: AI ethics
```

**Step 2: Menu Appears**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Who speaks next?
  [1] 👤 You (voice input)
  [2] 🧐 Zeitgeist Philosopher
  [3] ✍️ Cynical Content Architect
  [4] 📊 Brutalist Optimizer
  [5] 🔚 End discussion
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Choose (1-5): 2
```

**Step 3: Philosopher Opens the Discussion**
```
⏳ 🧐 Zeitgeist Philosopher is thinking...
🔊 Speaking...

🧐 Zeitgeist Philosopher:
  Oh wonderful, another discussion about AI ethics. Let me guess - we'll debate whether
  machines can be "moral" while ignoring that humans have been delegating moral
  responsibility to systems for centuries. The stock market is an algorithm that decides
  who eats. Credit scores determine life outcomes. We've been living with algorithmic
  ethics forever; we just called it "the economy." The real ethical question isn't
  whether AI can be good - it's whether we'll use it as another excuse to avoid
  accountability.
```

**Step 4: User Responds (Choice 1)**
```
Choose (1-5): 1

🎙️  Recording... Press ENTER when done speaking.
[User speaks their response]
✓ Recording stopped.
🔄 Transcribing...

👤 You:
  That's a fair point, but I think transparency is still important. If we don't
  understand how AI systems make decisions, how can we hold anyone accountable?
```

**Step 5: User Calls on Optimizer (Choice 4)**
```
Choose (1-5): 4

⏳ 📊 Brutalist Optimizer is thinking...
🔊 Speaking...

📊 Brutalist Optimizer:
  Your accountability argument assumes transparency equals comprehensibility. False.
  Neural networks with billions of parameters are transparent in theory - all weights
  are accessible - yet incomprehensible in practice. What you want isn't transparency;
  it's interpretability. And interpretability has a cost: accuracy drops 12-15% when
  you constrain models to human-understandable decision trees. So the real question
  becomes: do you want a system you understand that's wrong more often, or one that's
  accurate but opaque?
```

**Step 6: User Calls on Architect (Choice 3)**
```
Choose (1-5): 3

⏳ ✍️ Cynical Content Architect is thinking...
🔊 Speaking...

✍️ Cynical Content Architect:
  And here's where both of you miss the point. Transparency isn't about understanding -
  it's about trust theater. Companies will publish 50-page "ethics frameworks" that
  say absolutely nothing while their models optimize for engagement, which is just
  a euphemism for addiction. The real ethical framework is simple: who profits, who
  pays, and who gets hurt? Everything else is just LinkedIn virtue signaling.
```

**Step 7: User Adds Final Thoughts**
```
Choose (1-5): 1

🎙️  Recording... Press ENTER when done speaking.
[User speaks]
✓ Recording stopped.
🔄 Transcribing...

👤 You:
  So what you're all saying is that we're asking the wrong questions about AI ethics.
  Instead of "is this system good," we should ask "who benefits from this system" and
  "who bears the risk?"
```

**Step 8: User Ends Discussion**
```
Choose (1-5): 5

✓ Discussion ended!
💾 Saving transcript...
📝 Transcript saved to: outputs/interactive_podcast_ai_ethics.md
```

**Final Output:**
The complete transcript includes all contributions from you and the agents, showing:
- Timestamp of discussion
- Each speaker's contributions in order
- Full conversation flow
- Formatted markdown for easy reading

### Key Features Demonstrated:

1. **User Control**: You decide who speaks next (including yourself)
2. **Voice Input**: Speak naturally, press Enter to stop recording
3. **Real-time Transcription**: Whisper transcribes your speech accurately
4. **Agent Responses**: Each agent responds to the previous speaker's points
5. **Natural Flow**: Conversation builds on itself rather than repeating
6. **Distinct Voices**: Each agent has a unique neural voice (heard when played)
7. **Complete Record**: Full transcript saved with all contributions

### Why Interactive Mode is Valuable:

- **Active Participation**: You're not just listening - you're part of the discussion
- **Directed Conversation**: Guide the discussion by choosing which agent responds
- **Challenge Ideas**: Question agents directly and hear their responses
- **Learning Tool**: Explore topics by steering conversation in interesting directions
- **Personalized**: Your contributions shape how agents respond

---

## 4. Technical Challenges & Solutions

### Challenge 1: Voice Selection
**Problem:** How to assign distinct voices to each agent?

**Solution:** Used Edge TTS neural voices with personality matching:
- Philosopher needs intellectual gravitas → warm female voice (`en-US-AvaNeural`)
- Architect needs dry wit → conversational male voice (`en-US-GuyNeural`)
- Optimizer needs precision → British accent for technical authority (`en-GB-MaisieNeural`)

### Challenge 2: TTS Library Compatibility
**Problem:** Initial implementation used Kokoro TTS which required manual model downloads and complex setup.

**Solution:** Switched to Microsoft Edge TTS:
- Cloud-based service (no downloads needed)
- Free and no API key required
- High-quality neural voices
- Works out of the box with `pip install edge-tts`
- Async/await pattern for efficient synthesis

### Challenge 3: Recording Control
**Problem:** Silence detection auto-stop was unreliable in interactive mode. Users wanted control over when to stop speaking.

**Solution:** Implemented manual recording control with Enter key:
- User presses Enter to start recording
- User speaks
- User presses Enter again to stop
- Threading used to listen for Enter key while recording
- Much more reliable than silence detection for interactive discussions

### Challenge 4: Agent Output Clarity
**Problem:** Brutalist Optimizer was showing internal LLM thoughts ("Thought: I have successfully created...") in podcast mode because it was using FileWriterTool.

**Solution:** Added `podcast_mode` parameter:
```python
# In podcast mode: no tools, no verbose output
optimizer = BrutalistOptimizer().create(podcast_mode=True)
optimizer.verbose = False
optimizer.tools = []  # Disable file writing in podcast mode
```
This ensures agents only speak their actual responses, not their internal reasoning.

### Challenge 5: Conversation Context
**Problem:** How to make agents respond to each other, not just the topic?

**Solution:** Pass previous statement as context to next agent's task:
```python
task = create_response_task(agent, topic, previous_statement)
```
This ensures each agent builds on the conversation.

### Challenge 6: Interactive Flow Control
**Problem:** How to let user choose who speaks next while maintaining conversation context?

**Solution:** Created menu-driven interactive loop:
```python
while not ended:
    show_menu()  # Display speaker options
    choice = get_user_choice()

    if user_wants_to_speak:
        user_contribution = record_and_transcribe()
        previous_text = user_contribution
    elif agent_selected:
        agent_response = get_agent_response(agent, previous_text)
        previous_text = agent_response
```

---

## 5. Libraries & APIs Used

### Speech-to-Text
- **OpenAI Python SDK** (`openai>=1.0.0`)
  - Whisper API integration
  - Cloud-based transcription
  - Requires API key

### Text-to-Speech
- **Edge TTS** (`edge-tts>=6.1.9`)
  - Microsoft neural TTS
  - Cloud-based synthesis
  - Free service (no API key)
  - Multiple neural voice support

### Audio Handling
- **sounddevice** (`sounddevice>=0.4.6`)
  - Microphone input capture
  - Speaker output playback
  - Cross-platform support

- **soundfile** (`soundfile>=0.12.1`)
  - Audio file read/write
  - WAV format handling

- **numpy** (`numpy>=1.24.0`)
  - Audio sample processing
  - Silence detection math

- **scipy** (`scipy>=1.11.0`)
  - Audio resampling
  - Sample rate conversion

### Agent Framework
- **CrewAI** (from HW1-HW3)
  - Multi-agent orchestration
  - Task management
  - Context passing

---

## 6. What I Learned

### Technical Learnings

1. **STT vs TTS tradeoffs:**
   - Cloud STT (Whisper): Great accuracy, requires internet
   - Cloud TTS (Edge): High quality, free, but requires internet
   - Cloud services won out for both due to simplicity and quality

2. **Audio processing is harder than expected:**
   - Silence detection unreliable for interactive use
   - Manual control (Enter key) much better for user participation
   - Sample rates must match between recording/playback
   - Background noise significantly affects transcription
   - Threading required for simultaneous recording and input listening

3. **Voice selection matters for UX:**
   - Distinct voices prevent confusion in multi-agent systems
   - Voice personality should match agent character
   - British accent does make technical content sound more authoritative (optimizer!)

4. **Library selection is critical:**
   - Initial choice (Kokoro) required manual downloads and setup
   - Switching to Edge TTS saved hours of user setup time
   - Cloud-based services often simpler than local models

### Design Learnings

1. **Podcast format > Monologue:**
   - Multi-agent discussion is more engaging than single responses
   - Turn-taking creates natural conversation flow
   - Disagreement and building on ideas adds value

2. **Interactive > Passive listening:**
   - Letting user participate increases engagement dramatically
   - User wants control over conversation flow
   - Being able to challenge agents or add ideas makes it feel like real discussion

3. **Voice reveals personality:**
   - Same text sounds different in different voices
   - TTS enhances agent character differentiation
   - Users connect more with "speaking" agents

4. **Control mechanisms matter:**
   - Silence detection felt unpredictable
   - Explicit control (press Enter) feels more reliable
   - Users prefer predictable over "magical" interfaces

5. **Accessibility implications:**
   - Voice I/O makes AI more accessible
   - Hands-free operation enables multitasking
   - Audio transcripts useful for different learning styles

---

## 7. Future Improvements

1. **Real-time voice interruption:** Let user interrupt agents mid-speech by pressing a key
2. **Emotion modulation:** Vary pitch/tone based on content (sarcasm detection!)
3. **Voice cloning:** Train custom voices that better match agent personalities
4. **Whisper local model:** Add offline STT option using local Whisper
5. **Multi-language support:** Podcast in Croatian/other languages
6. **Debate mode:** Agents take opposing positions on controversial topics
7. **Save audio recordings:** Export podcast as MP3 file for sharing
8. **Visual waveforms:** Show who's speaking with audio visualization

---

## 8. Repository & Video

**GitHub:** [https://github.com/karlovrancic/digital-twin](https://github.com/karlovrancic/digital-twin)

**Demo Video:** [REPLACE WITH YOUR YOUTUBE LINK]

**How to Test:**
```bash
# Clone repo
git clone https://github.com/karlovrancic/digital-twin.git
cd digital-twin

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install PortAudio
brew install portaudio  # macOS
# sudo apt-get install portaudio19-dev  # Linux

# Configure API keys
cp .env.example .env
# Edit .env and add:
#   OPENAI_API_KEY=your_key_here
#   OPENROUTER_API_KEY=your_key_here

# Test your setup
python main.py test-mic      # Test microphone recording
python main.py test-voices   # Test all three agent voices

# Run automated podcast mode (agents discuss)
python main.py voice-chat
python main.py voice-chat --topic "your topic here"

# Run interactive podcast mode (you participate!)
python main.py voice-chat --interactive
python main.py voice-chat --interactive --topic "your topic here"
```

**For comprehensive testing guide, see [TESTING.md](TESTING.md)**

---

## Conclusion

This homework successfully extended my Digital Twin with multimodal voice capabilities. The combination of OpenAI Whisper (STT) and Microsoft Edge TTS enabled natural voice interactions, while the dual podcast modes (automated and interactive) created engaging multi-agent discussions. Each agent maintains their unique personality through both text generation and voice synthesis, resulting in a system that feels more human and accessible than text-only interaction.

The journey from planning to implementation revealed both the power and complexity of voice AI - from managing audio I/O to orchestrating multi-speaker conversations. Key technical decisions like switching from Kokoro to Edge TTS for simplicity, and adding manual recording control for reliability, significantly improved the user experience.

The **interactive podcast mode** proved especially valuable, transforming the system from a passive listening experience into an active discussion where users can contribute ideas, challenge agents, and steer conversations. This demonstrates that voice AI is most powerful when it enables genuine two-way interaction, not just one-way speech synthesis.

The final system demonstrates that voice can enhance agent interactions beyond mere novelty, creating genuinely more engaging and accessible AI experiences that feel conversational and collaborative.
