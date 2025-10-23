# HW4: Multimodal Agent - Voice Capabilities

**Student:** Karlo Vrančić
**Course:** MIT AI Studio
**Date:** October 2025

---

## 1. Implementation Overview

This project extends my Digital Twin (HW1-HW3) with voice interaction capabilities, enabling speech-to-text input and text-to-speech output. The system supports two podcast-style modes where three AI agents (Zeitgeist Philosopher, Cynical Content Architect, and Brutalist Optimizer) engage in spoken conversations, each with their own unique voice.

### Key Features
- **Speech-to-Text:** OpenAI Whisper API for voice input transcription
- **Text-to-Speech:** Microsoft Edge TTS with 3 distinct neural voices
- **Automated Podcast:** Agents discuss topics among themselves
- **Interactive Podcast:** User participates via voice in agent discussions
- **Real-time Audio I/O:** Microphone recording with manual stop control (press Enter)

### Architecture
```
Voice System Pipeline:
Audio Input → Whisper STT → Agent Processing → Edge TTS → Audio Output

Components:
├── STT: OpenAI Whisper API (cloud-based transcription)
├── TTS: Microsoft Edge TTS (3 neural voices for agent differentiation)
├── Audio: sounddevice/soundfile (recording & playback)
├── Orchestration: PodcastOrchestrator (automated mode)
└── Interaction: InteractivePodcast (user participation mode)
```

---

## 2. Voice Implementation Details

### Speech-to-Text (Whisper)
**Library:** OpenAI Python SDK (`openai>=1.0.0`)

**Implementation:**
```python
# User speaks into microphone
audio_file = AudioRecorder().record_to_file()

# Whisper API transcribes to text
client = OpenAI(api_key=Config.OPENAI_API_KEY)
transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=open(audio_file, "rb")
)
```

**Why Whisper?** Industry-leading accuracy, handles accents/noise well, simple cloud API with no local model management.

### Text-to-Speech (Edge TTS)
**Library:** Microsoft Edge TTS (`edge-tts>=6.1.9`)

**Voice Assignment:**
- **Zeitgeist Philosopher** → `en-US-AvaNeural` (warm, conversational female)
- **Cynical Content Architect** → `en-US-GuyNeural` (casual, engaging male)
- **Brutalist Optimizer** → `en-GB-MaisieNeural` (analytical British female)

**Implementation:**
```python
async def speak_as_agent(text: str, agent_name: str):
    voice = AGENT_VOICES[agent_name]
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    AudioPlayer().play(output_file)
```

**Why Edge TTS?** Free cloud service (no API key needed), high-quality neural voices, multiple voice options for agent differentiation, works out-of-the-box.

### Audio Handling
**Libraries:**
- `sounddevice` - Microphone capture & speaker playback
- `soundfile` - Audio file I/O (WAV format)
- `numpy` - Audio sample processing
- Threading - Manual recording control (listen for Enter key while recording)

---

## 3. Example Run: Interactive Podcast Mode

**Command Used:**
```bash
python main.py voice-chat --interactive --topic "AI ethics"
```

### Input
User speaks or types the topic "AI ethics", then participates in a discussion by choosing speakers and contributing via voice.

### What Happened

**1. Topic Input**
```
🎙️  Speak your topic, or type it: AI ethics
Starting interactive podcast on: AI ethics
```

**2. Menu-Driven Conversation**
```
Who speaks next?
  [1] 👤 You (voice input)
  [2] 🧐 Zeitgeist Philosopher
  [3] ✍️ Cynical Content Architect
  [4] 📊 Brutalist Optimizer
  [5] 🔚 End discussion
```

**3. Philosopher Opens (User chooses 2)**
```
🧐 Zeitgeist Philosopher (voice plays):
  "Oh wonderful, another discussion about AI ethics. Let me guess - we'll debate
  whether machines can be 'moral' while ignoring that humans have been delegating
  moral responsibility to systems for centuries. The stock market is an algorithm
  that decides who eats. We've been living with algorithmic ethics forever; we
  just called it 'the economy.'"
```

**4. User Responds (chooses 1)**
```
🎙️  Recording... Press ENTER when done speaking.
[User speaks: "That's fair, but transparency is still important"]
✓ Recording stopped. Transcribing...

👤 You: "That's fair, but transparency is still important for accountability"
```

**5. Optimizer Responds (User chooses 4)**
```
📊 Brutalist Optimizer (voice plays):
  "Your accountability argument assumes transparency equals comprehensibility.
  False. Neural networks with billions of parameters are transparent in theory -
  all weights are accessible - yet incomprehensible in practice. What you want
  isn't transparency; it's interpretability. And interpretability has a cost:
  accuracy drops 12-15% when you constrain models to human-understandable
  decision trees."
```

**Conversation continues** with user directing flow by choosing speakers, contributing thoughts via voice, and hearing agents respond until choosing option 5 to end.

### Output
- **Audio:** Each agent speaks in their unique neural voice (heard in real-time)
- **Transcript:** Complete conversation saved to `outputs/interactive_podcast_ai_ethics.md` with all user and agent contributions, timestamps, and formatted markdown

### Insights Observed

1. **Voice Differentiation Works:** Three distinct voices make it easy to follow multi-agent discussions without visual cues
2. **Interactive > Passive:** User participation transforms listening into active dialogue - you can challenge agents, steer conversation, and add your own ideas
3. **Personalities Shine Through Voice:** Same text sounds different in different voices - TTS enhances agent character (Philosopher's warmth, Architect's cynicism, Optimizer's precision)
4. **Manual Control Beats Auto-Detection:** Enter key recording control is more reliable than silence detection for interactive discussions
5. **Context Matters:** Agents build on previous statements rather than repeating ideas, creating genuine conversation flow
6. **Accessibility Impact:** Voice I/O makes AI more accessible - hands-free operation enables multitasking and serves different learning styles

---

## 4. Technical Challenges & Solutions

**Challenge 1: TTS Library Selection**
Initial implementation used Kokoro TTS (required manual model downloads). **Solution:** Switched to Edge TTS for cloud-based, zero-config setup.

**Challenge 2: Recording Control**
Silence detection was unreliable for interactive mode. **Solution:** Manual control with Enter key using threading to listen for input while recording.

**Challenge 3: Agent Output Clarity**
Brutalist Optimizer showed internal reasoning in podcast mode. **Solution:** Added `podcast_mode` parameter to disable tools and verbose output for clean spoken responses.

---

## 5. Libraries & APIs Used

### Core Voice Libraries
- **OpenAI Python SDK** (`openai>=1.0.0`) - Whisper STT API
- **Edge TTS** (`edge-tts>=6.1.9`) - Microsoft neural TTS (free, cloud-based)
- **sounddevice** (`sounddevice>=0.4.6`) - Audio I/O
- **soundfile** (`soundfile>=0.12.1`) - Audio file handling
- **numpy** (`numpy>=1.24.0`) - Audio processing

### Agent Framework
- **CrewAI** - Multi-agent orchestration (from HW1-HW3)

---

## 6. Key Learnings

**Technical:**
- Cloud STT/TTS services (Whisper, Edge TTS) provide better UX than local models due to simplicity and quality
- Audio processing harder than expected - sample rates must match, threading required for simultaneous recording/listening
- Voice personality matching matters - distinct voices prevent confusion, personality should match agent character

**Design:**
- Podcast format (multi-agent discussion) more engaging than monologue
- Interactive mode > passive listening - users want control over conversation flow
- Manual control feels more reliable than "magical" auto-detection interfaces
- Voice reveals personality - same text sounds different in different voices, enhancing agent differentiation

**Impact:**
- Voice I/O makes AI more accessible (hands-free, multitasking-friendly)
- Interactive discussion enables genuine two-way interaction vs one-way synthesis
- Users connect more with "speaking" agents - feels conversational and collaborative

---

## 7. Repository & Testing

**GitHub:** [https://github.com/karlovrancic/digital-twin](https://github.com/karlovrancic/digital-twin)

**Demo Video:** [REPLACE WITH YOUR YOUTUBE LINK]

**Quick Test:**
```bash
# Setup
git clone https://github.com/karlovrancic/digital-twin.git
cd digital-twin
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
brew install portaudio  # macOS

# Configure .env with OPENAI_API_KEY and OPENROUTER_API_KEY

# Test
python main.py test-mic        # Test microphone
python main.py test-voices     # Test TTS voices
python main.py voice-chat --interactive  # Run interactive podcast
```

**For comprehensive testing guide, see [TESTING.md](TESTING.md)**

---

## Conclusion

This project successfully extended the Digital Twin with multimodal voice capabilities using OpenAI Whisper (STT) and Microsoft Edge TTS (multi-voice synthesis). The **interactive podcast mode** proved especially valuable, transforming passive listening into active discussion where users contribute ideas, challenge agents, and steer conversations via voice input.

Key technical decisions - choosing cloud services over local models, implementing manual recording control, and assigning personality-matched voices - significantly improved user experience. The result is a system where voice enhances agent interactions beyond novelty, creating genuinely engaging and accessible AI experiences that feel conversational and collaborative.
