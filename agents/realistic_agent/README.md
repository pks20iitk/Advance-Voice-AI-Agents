# Realistic Office Caller Agent

This agent simulates a professional office assistant with realistic background sounds and typing effects when "thinking". It creates a more immersive and engaging experience for users.

## Features

- **Professional voice**: Uses Deepgram's "Aura Asteria" voice
- **Office ambient sounds**: Background office noises provide realism
- **Typing sounds during thinking**: Keyboard typing sounds play when processing
- **Professional assistant capabilities**:
  - Schedule meetings
  - Check calendar availability
  - Take messages
  - Provide company information
  - Find personnel

## Environment Variables

Make sure to set up your `.env` file with the necessary API keys and configuration:

```
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your_api_key
LIVEKIT_API_SECRET=your_api_secret
GOOGLE_API_KEY=AIzaSyAlPK3CIow-Bx4TMRpDbl4_21C4GYOO5IQ
DEEPGRAM_API_KEY=your_deepgram_key
```

## Running Locally

1. Install dependencies:
   ```bash
   pip install -r ../../requirements.txt
   ```

2. Run the agent:
   ```bash
   python agent.py
   ```

## Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t voice-ai-realistic-agent -f Dockerfile ../..
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file ../../.env voice-ai-realistic-agent
   ```

## Agent Configuration

The realistic agent is configured with:
- Google Gemini 1.5 Flash LLM for enhanced capabilities
- Deepgram Nova-3 for accurate speech recognition
- Deepgram Aura Asteria voice for a professional sound
- Silero VAD (Voice Activity Detection) for improved interaction