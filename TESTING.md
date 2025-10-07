# Testing Guide - Voice-Enabled Digital Twin

This guide walks you through testing the voice capabilities of your Digital Twin system and recording a demo video for submission.

---

## Prerequisites

### 1. Install System Dependencies

**macOS:**
```bash
brew install portaudio
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install portaudio19-dev
```

**Windows:**
PortAudio is included with the Python package, but you may need to install additional audio drivers.

### 2. Install Python Dependencies

```bash
# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Install requirements
pip install -r requirements.txt
```

### 3. Configure API Keys

```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your API keys
nano .env  # or use any text editor
```

Add these keys to `.env`:
```
OPENROUTER_API_KEY=your_openrouter_key_here
OPENAI_API_KEY=your_openai_key_here
```

**Where to Get API Keys:**
- OpenRouter: https://openrouter.ai (for agent LLMs)
- OpenAI: https://platform.openai.com/api-keys (for Whisper STT)

---

## Testing Steps

### Step 1: Check Configuration

```bash
python main.py info
```

**Expected Output:**
- Shows all three agents
- Voice commands show `✓` (green checkmark)
- If you see `✗` (red X), check your dependencies

### Step 2: Test Microphone

```bash
python main.py test-mic
```

**What This Does:**
- Records 3 seconds of audio from your microphone
- Displays audio levels and duration
- Verifies microphone permissions are granted

**Expected Output:**
```
🎤 Microphone Test

Speak for 3 seconds...

Recorded 72000 samples
Duration: 3.00 seconds
Max amplitude: 0.1234

✓ Microphone working!
```

**Troubleshooting:**
- **"Max amplitude: 0.0001"** → Microphone not detected or muted
- **Permission error** → Grant microphone access in System Preferences (macOS)
- **No audio device found** → Check your microphone is plugged in

### Step 3: Test TTS Voices

```bash
python main.py test-voices
```

**What This Does:**
- Tests each agent's voice with a sample phrase
- Plays audio through your speakers
- Verifies Kokoro TTS is working

**Expected Output:**
```
🔊 Voice Test

Testing voices for each agent...

Zeitgeist Philosopher
  Text: Interesting. I've analyzed human speech patterns and found them absurdly predictable.
  Voice: af_sky
  ✓ Complete

Cynical Content Architect
  Text: Language is manipulation, and I'm ruthlessly effective at using it.
  Voice: am_adam
  ✓ Complete

Brutalist Optimizer
  Text: Your speech synthesis latency is acceptable. Optimization complete.
  Voice: bf_emma
  ✓ Complete

✓ All voice tests complete!
```

**Troubleshooting:**
- **No audio** → Check speaker volume, speaker connection
- **Kokoro import error** → Run `pip install kokoro-onnx`
- **Slow synthesis** → First time is slower, subsequent calls are faster

### Step 4: Test Voice Chat (Text Input)

Start with text input to test the podcast logic without voice:

```bash
python main.py voice-chat --topic "AI and creativity"
```

**What This Does:**
- Skips voice input (topic provided via CLI)
- Runs 2-round podcast discussion
- Each agent speaks their contribution aloud
- Saves transcript to `outputs/`

**Expected Flow:**
1. Shows "Starting podcast discussion..."
2. **Round 1:** Each agent gives opening statement (you hear 3 voices)
3. **Round 2:** Agents respond to each other (3 more contributions)
4. **Final Thoughts:** Each agent concludes (3 final statements)
5. Saves transcript

**Troubleshooting:**
- **OpenAI API error** → Check OPENAI_API_KEY in .env
- **OpenRouter API error** → Check OPENROUTER_API_KEY in .env
- **Agent timeout** → Network issue, try again

### Step 5: Test Voice Chat (Voice Input)

Now test the full voice pipeline:

```bash
python main.py voice-chat
```

**What This Does:**
- Prompts you to speak your topic
- Records via microphone (stops after 2 sec silence)
- Transcribes with Whisper
- Runs podcast discussion
- Each agent speaks in their voice

**Expected Flow:**
```
🎙️ Voice Chat Mode - Podcast Discussion

🎤 Listening... Speak your topic (will auto-stop after 2 seconds of silence)
Press Ctrl+C to cancel

[YOU SPEAK: "What is the future of AI agents?"]

🔄 Transcribing...

✓ You said: What is the future of AI agents?

Start podcast discussion on this topic? [Y/n]: y

[PODCAST DISCUSSION BEGINS]
```

**Tips for Best Results:**
- Speak clearly and at normal volume
- Wait 2 seconds of silence for auto-stop
- Use a quiet environment (minimize background noise)
- Good topics: "AI ethics", "Remote work trends", "Cryptocurrency regulation"

---

## Recording Your Demo Video

### Preparation

1. **Clean your terminal:**
```bash
clear
python main.py voice-chat
```

2. **Choose a good topic:**
   - Something your agents can discuss intelligently
   - Not too niche or technical
   - Examples: "AI replacing creative jobs", "Future of education", "Social media impact"

3. **Test your audio setup:**
   - Check microphone input level
   - Check speaker output volume
   - Close other applications to reduce lag

### Recording Options

**Option 1: QuickTime (macOS)**
```
1. Open QuickTime Player
2. File → New Screen Recording
3. Click Options → Choose microphone (to capture system audio + your voice)
4. Click Record → Select area to record
5. Run: python main.py voice-chat
6. Speak your topic
7. Let the podcast run
8. Stop recording when done
```

**Option 2: OBS Studio (All Platforms)**
```
1. Install OBS Studio (free)
2. Add source → Display Capture
3. Add source → Audio Input (your mic)
4. Add source → Audio Output (system audio)
5. Start Recording
6. Run: python main.py voice-chat
7. Stop Recording when done
```

**Option 3: Built-in Screen Recording (macOS)**
```
1. Press Cmd + Shift + 5
2. Choose "Record Entire Screen" or "Record Selected Portion"
3. Click Options → Select microphone
4. Click Record
5. Run: python main.py voice-chat
6. Stop in menu bar when done
```

### What to Include in Video

**Duration:** 2-3 minutes is perfect

**Suggested Script:**
1. **Introduction (15 seconds)**
   - "Hi, this is Karlo's Digital Twin with voice capabilities"
   - "I'll demonstrate the podcast discussion mode"

2. **Show the command (5 seconds)**
   ```bash
   python main.py voice-chat
   ```

3. **Speak your topic (5 seconds)**
   - Clearly state your topic when prompted
   - Example: "What are the current trends in artificial intelligence?"

4. **Let it run (90-120 seconds)**
   - Show the transcription of your speech
   - Let at least 2-3 agent contributions play
   - Show different voices speaking
   - You can narrate: "Now the Philosopher is speaking... now the Architect..."

5. **Show the output (10 seconds)**
   - Show the saved transcript file
   - `ls outputs/`
   - `cat outputs/podcast_*.md` (optional)

**Pro Tips:**
- **Don't speed up the video** - show the voices in real-time
- **Include your face/voice** if comfortable (but not required)
- **Show terminal output** clearly (increase font size if needed)
- **Caption key moments** if your editing tool allows it

### Upload to YouTube

1. Go to https://youtube.com/upload
2. Select your video file
3. Title: "AI Studio HW4 - Voice-Enabled Digital Twin - [Your Name]"
4. Description:
   ```
   Demonstration of voice-enabled multimodal agent system for MIT AI Studio HW4.

   Features:
   - Speech-to-text input (OpenAI Whisper)
   - Multi-agent podcast discussion (CrewAI)
   - Text-to-speech output (Kokoro TTS)
   - Three distinct agent voices

   GitHub: [your repo URL]
   ```
5. Set visibility to **Unlisted**
6. Click Publish
7. Copy the video URL for homework submission

---

## Troubleshooting Common Issues

### Voice Input Not Working

**Issue:** Recording captures no audio

**Solutions:**
- Grant microphone permissions: System Preferences → Security & Privacy → Microphone
- Check microphone is not muted
- Test with `python main.py test-mic`
- Try different microphone (built-in vs external)

### Whisper Transcription Fails

**Issue:** "Whisper transcription failed" error

**Solutions:**
- Check OPENAI_API_KEY is set correctly in .env
- Verify API key has credits: https://platform.openai.com/account/usage
- Check internet connection
- Audio file might be too short (speak longer)

### TTS Synthesis Fails

**Issue:** "Kokoro synthesis failed" error

**Solutions:**
- Reinstall: `pip uninstall kokoro-onnx && pip install kokoro-onnx`
- Check disk space (models need ~500MB)
- Try different voice: `python main.py test-voices --voice af_bella`

### Agent Responses are Slow

**Issue:** Long pauses between agents

**Solutions:**
- This is normal - agents are thinking (LLM inference)
- Use faster model: Edit .env → `OPENROUTER_PRO_MODEL=google/gemini-2.5-flash-lite`
- Check OpenRouter API status

### Audio Playback Issues

**Issue:** No sound from speakers

**Solutions:**
- Check system volume
- Check default audio output device
- Try: `python -c "import sounddevice as sd; sd.play([0.3]*24000, 24000); sd.wait()"`
- Restart terminal and try again

---

## Example Topics for Testing

**Good Topics (Agents Will Discuss Well):**
- "The impact of AI on creative industries"
- "Remote work vs office culture"
- "Social media and mental health"
- "The future of education"
- "Cryptocurrency and financial systems"
- "Climate change solutions"
- "The role of government in tech regulation"

**Topics to Avoid:**
- Too specific: "Explain the Transformer architecture" (too technical for podcast)
- Too broad: "Life" (agents need direction)
- Requires current data: "Who won yesterday's game?" (agents don't have real-time info)

---

## Expected Output Files

After running voice-chat, you should have:

```
outputs/
└── podcast_[your_topic_slug].md
```

**Example:**
```
outputs/podcast_ai_and_creative_industries.md
```

This file contains the full transcript with:
- Topic name
- Number of rounds
- Each agent's contributions
- Formatted with headers and speaker labels

---

## Manual Testing Checklist

Before recording your final video, verify:

- [ ] `python main.py info` shows voice features enabled
- [ ] `python main.py test-mic` detects your microphone
- [ ] `python main.py test-voices` plays all three voices
- [ ] `python main.py voice-chat --topic "test"` completes successfully
- [ ] `python main.py voice-chat` (no topic) accepts voice input
- [ ] Transcript file is created in `outputs/`
- [ ] Audio quality is clear (no distortion/static)
- [ ] All three voices are distinct and audible

If all items are checked, you're ready to record your demo! 🎉

---

## Need Help?

If you encounter issues not covered here:

1. Check the error message carefully
2. Review HOMEWORK.md for architecture details
3. Check GitHub Issues: https://github.com/karlovrancic/digital-twin/issues
4. Verify all dependencies installed: `pip list | grep -E "openai|kokoro|sounddevice"`

Good luck with your demo! 🎙️
