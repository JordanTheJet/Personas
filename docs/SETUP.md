# Development Environment Setup

This guide will help you set up your development environment to start building the AI Agent Collective.

## Prerequisites

Before you begin, ensure you have:

- **Python 3.11+** installed
- **Docker** and **Docker Compose** installed
- **Git** installed
- A code editor (VS Code recommended)
- At least 8GB RAM and 20GB free disk space

## Quick Start

### 1. Clone and Enter Repository

```bash
cd Personas  # You're already here if you're reading this!
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate
# On Windows:
# venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your actual API keys
nano .env  # or use your preferred editor
```

**Required API Keys** (get these before proceeding):

1. **Anthropic** (Claude):
   - Sign up at https://console.anthropic.com/
   - Create API key
   - Add to `.env` as `ANTHROPIC_API_KEY`

2. **OpenAI** (GPT-4, DALL-E):
   - Sign up at https://platform.openai.com/
   - Create API key
   - Add to `.env` as `OPENAI_API_KEY`

3. **Twitter API** (for social media):
   - Apply for developer access at https://developer.twitter.com/
   - Create an app and get credentials
   - Add all Twitter keys to `.env`

*Note: You can start with just Anthropic key and add others as needed*

### 5. Start Infrastructure Services

```bash
# Start PostgreSQL, Redis, and RabbitMQ
docker-compose up -d

# Verify services are running
docker-compose ps

# You should see:
# - personas_db (PostgreSQL) - healthy
# - personas_redis (Redis) - healthy
# - personas_rabbitmq (RabbitMQ) - healthy
```

### 6. Initialize Database

```bash
# TODO: Create database initialization script
# This will create tables for:
# - Agents
# - Memory/context
# - Actions log
# - Metrics
```

### 7. Verify Installation

```bash
# Test that core imports work
python -c "from core.config import settings; print('✓ Config loaded')"
python -c "from core.agent_framework import BaseAgent; print('✓ Agent framework loaded')"
python -c "from core.personality_engine import Persona; print('✓ Personality engine loaded')"
```

If all three print checkmarks, you're ready to go!

## Development Workflow

### Running the Application

**Option A: Development Mode**
```bash
# Activate virtual environment
source venv/bin/activate

# Run main application (once created)
python main.py
```

**Option B: With Auto-reload**
```bash
# If using FastAPI for web interface
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Option C: With Docker** (later)
```bash
# Uncomment app service in docker-compose.yml
docker-compose up app
```

### Running Celery Workers

For scheduled tasks and background jobs:

```bash
# Terminal 1: Celery Worker
celery -A core.scheduler.celery_app worker --loglevel=info

# Terminal 2: Celery Beat (scheduler)
celery -A core.scheduler.celery_app beat --loglevel=info
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=core --cov=agents

# Run specific test file
pytest tests/test_agents.py

# Run with verbose output
pytest -v
```

### Code Formatting and Linting

```bash
# Format code with Black
black .

# Check code style with flake8
flake8 core/ agents/ tools/

# Type checking with mypy
mypy core/
```

## Project Structure Overview

```
Personas/
├── core/                    # Core infrastructure
│   ├── agent_framework/     # Base agent system ✓
│   ├── personality_engine/  # Persona definitions ✓
│   ├── memory_system/       # Memory & context (TODO)
│   └── scheduler/           # Task scheduling (TODO)
├── agents/                  # Individual agents
│   ├── jordanthejet/       # Self-augmentation (TODO)
│   ├── pixelphantom/       # Game dev agent (TODO)
│   └── luxeai/             # Content creator (TODO)
├── integrations/           # External services
│   ├── social_media/       # Twitter, Instagram, etc. (TODO)
│   ├── content_gen/        # Image/video generation (TODO)
│   └── code_gen/           # AI coding tools (TODO)
├── tools/                  # Shared utilities
├── tests/                  # Test suite
├── docs/                   # Documentation ✓
├── docker-compose.yml      # Infrastructure setup ✓
├── requirements.txt        # Python dependencies ✓
└── .env                    # Environment variables (your config)
```

## Common Development Tasks

### Create a New Agent

1. Create directory: `agents/your_agent_name/`
2. Create `__init__.py` and `agent.py`
3. Inherit from `BaseAgent`
4. Implement required methods:
   - `initialize()`
   - `perceive()`
   - `reason()`
   - `act()`
   - `reflect()`
5. Create persona definition in `core/personality_engine/persona.py`
6. Register with `AgentManager`

### Add a New Integration

1. Create directory: `integrations/service_name/`
2. Create client class
3. Implement authentication
4. Add methods for key operations
5. Add tests

### Monitor Agent Activity

```bash
# View logs
tail -f logs/app.log

# Check RabbitMQ management UI
open http://localhost:15672
# Login: personas / personas_dev_password

# Check Redis
docker exec -it personas_redis redis-cli
> KEYS *
> GET agent:jordanthejet:state

# Check PostgreSQL
docker exec -it personas_db psql -U personas -d personas
> \dt  -- List tables
> SELECT * FROM agents;
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Restart PostgreSQL
docker-compose restart postgres

# View logs
docker-compose logs postgres
```

### Redis Connection Issues

```bash
# Test Redis connection
docker exec -it personas_redis redis-cli ping
# Should return: PONG

# Restart Redis
docker-compose restart redis
```

### Module Import Errors

```bash
# Ensure virtual environment is activated
which python
# Should point to venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### API Key Issues

```bash
# Verify API keys are loaded
python -c "from core.config import settings; print(settings.anthropic_api_key[:10])"
# Should print first 10 chars of your key

# If empty, check .env file exists and is properly formatted
cat .env | grep ANTHROPIC
```

## Next Steps

Once your environment is set up:

1. **Review Documentation**:
   - Read `docs/architecture.md` for system design
   - Read `docs/personas.md` for agent personalities
   - Read `docs/roadmap.md` for implementation plan

2. **Start with Phase 1**:
   - Build JordanTheJet augmentation system
   - Implement Twitter integration
   - Test with shadow mode

3. **Join Development**:
   - Check `docs/roadmap.md` for current phase
   - Pick a task from the roadmap
   - Start building!

## Useful Commands Reference

```bash
# Virtual Environment
source venv/bin/activate                    # Activate
deactivate                                   # Deactivate

# Docker
docker-compose up -d                         # Start all services
docker-compose down                          # Stop all services
docker-compose logs -f [service]             # View logs
docker-compose restart [service]             # Restart service

# Development
python main.py                               # Run application
pytest                                       # Run tests
black .                                      # Format code

# Database
docker exec -it personas_db psql -U personas -d personas
docker exec -it personas_redis redis-cli

# Monitoring
docker stats                                 # Resource usage
docker-compose ps                            # Service status
```

## Getting Help

- **Documentation**: Check `docs/` directory
- **Issues**: This is a personal project, but document your blockers
- **Community**: Share your progress if building in public

## Security Notes

⚠️ **IMPORTANT**:
- Never commit `.env` file (it's in `.gitignore`)
- Never commit API keys
- Rotate keys if accidentally exposed
- Use strong passwords for production databases
- Enable 2FA on all service accounts

---

**You're all set!** 🚀

Start with the roadmap in `docs/roadmap.md` and begin building your AI agent collective.
