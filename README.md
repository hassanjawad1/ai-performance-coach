# AI Performance Coach

An intelligent WhatsApp-based performance coaching agent that analyzes your Google Calendar and provides personalized daily training plans based on your schedule, goals, and current streak.

## Features

- **Smart Schedule Analysis**: Integrates with Google Calendar to understand your availability and commitments
- **Adaptive Planning**: Generates RECOVERY, MODERATE, or INTENSE plans based on your calendar load
- **Multi-Persona Coaching**: Adapts coaching style based on your goals:
  - **AI Engineer**: Focus on architecture, clean code, and technical logic
  - **Drill Sergeant**: Aggressive, brief, physical-limit-pushing workouts
  - **Habit Coach**: Discipline, consistency, and mental clarity focus
- **Streak Tracking**: SQLite-based persistence to track your consistency
- **Weekly Reports**: Automated summaries of your weekly activity
- **WhatsApp Integration**: Chat with your coach directly via WhatsApp (Twilio)

## Tech Stack

- **FastAPI**: Web framework for the webhook endpoint
- **LangGraph**: Agent workflow orchestration
- **LangChain + OpenRouter**: LLM integration (Gemini 2.5 Flash Lite)
- **Google Calendar API**: Schedule context ingestion
- **Twilio**: WhatsApp messaging
- **SQLite**: User stats and plan history persistence
- **Pydantic**: Data validation and state management

## AI Performance Coach Architecture

<img width="1264" height="842" alt="image Arch" src="https://github.com/user-attachments/assets/bc89b04a-8ecd-409b-9606-861980d74ae8" />


## Project Structure

```
ai-performance-coach/
├── app/
│   ├── agents/
│   │   ├── nodes.py          # LangGraph nodes (ingest, assess, plan)
│   │   └── prompts.py        # System prompts for LLM agents
│   ├── graph/
│   │   └── builder.py        # LangGraph workflow builder
│   ├── models/
│   │   └── state.py          # CoachState Pydantic model
│   ├── services/
│   │   ├── calender.py       # Google Calendar API integration
│   │   ├── database.py       # SQLite database operations
│   │   └── whatsapp.py       # Twilio WhatsApp service
│   ├── scripts/
│   │   └── weekly_reporter.py  # Weekly summary generator
│   └── main.py               # FastAPI application entry point
├── coach_memory.db           # SQLite database
├── credentials.json          # Google API credentials
├── token.json                # Google OAuth token
├── .env                      # Environment variables
└── requirements.txt          # Python dependencies
```

## Setup

### Prerequisites

- Python 3.8+
- Google Cloud project with Calendar API enabled
- Twilio account with WhatsApp sandbox
- OpenRouter API key

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env`:
   ```
   OPENAI_API_KEY=your_openrouter_api_key
   TWILIO_ACCOUNT_SID=your_twilio_sid
   TWILIO_AUTH_TOKEN=your_twilio_token
   TWILIO_PHONE_NUMBER=your_twilio_whatsapp_number
   ```

4. Set up Google Calendar API:
   - Download `credentials.json` from Google Cloud Console
   - Run the app once to authenticate and generate `token.json`

### Running the App

```bash
python app/main.py
```

The server will start on `http://0.0.0.0:8000`

## Usage

1. Configure your Twilio WhatsApp sandbox webhook URL to point to `https://your-domain.com/webhook`
2. Send a message to your WhatsApp number describing your goal (e.g., "tech", "gym", "be tough")
3. The coach will analyze your calendar and reply with a personalized daily plan

## Agent Workflow

```
User Message → Ingest Context → Assessment → Planning → WhatsApp Response
                  ↓                ↓            ↓
            Google Calendar    LLM (Status)   LLM (Plan)
```

1. **Context Ingestion**: Fetches today's events from Google Calendar
2. **Assessment**: LLM analyzes calendar load and assigns status (RECOVERY/MODERATE/INTENSE)
3. **Planning**: LLM generates plan based on status, persona, and streak

## License

MIT
