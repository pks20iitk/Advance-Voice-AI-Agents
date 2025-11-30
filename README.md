# Voice AI Agents

This project contains voice AI agent implementations using the LiveKit Agents framework.

## Project Structure

```
├── agents/                     # Agent implementations
│   ├── realistic_agent/        # Agent with background audio effects
│   └── standard_agent/         # Agent without background audio
├── backend/                    # Flask token server for LiveKit authentication
├── frontend/                   # React web application
├── requirements.txt            # Python dependencies
└── docker-compose.yml          # Docker orchestration
```

## Setup Instructions

### Environment Setup

1. Clone this repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file using the provided `.env.example` and add your API keys

### Running the Agents

#### Realistic Agent

```bash
cd agents/realistic_agent
python agent.py
```

#### Standard Agent

```bash
cd agents/standard_agent
python agent.py
```

### Running the Frontend

```bash
cd frontend
npm install
npm start
```

For detailed instructions, refer to the README files in each component directory.

## Docker Deployment

Each component can be containerized using Docker:

### Realistic Agent

```bash
docker build -t voice-ai-realistic-agent -f agents/realistic_agent/Dockerfile .
docker run -p 8000:8000 --env-file .env voice-ai-realistic-agent
```

### Standard Agent

```bash
docker build -t voice-ai-standard-agent -f agents/standard_agent/Dockerfile .
docker run -p 8001:8000 --env-file .env voice-ai-standard-agent
```

### Frontend

```bash
docker build -t voice-ai-frontend -f frontend/Dockerfile frontend/
docker run -p 3000:80 voice-ai-frontend
```
