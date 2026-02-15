# Assessment Agent

An AI-powered adaptive assessment agent that conducts conversational assessments of learner understanding in fractions (CCSS-M, Grades 2-5). Built with Claude's tool-use capability.

## How It Works

The agent uses 6 tools in an autonomous loop to conduct adaptive assessments:

1. **ask_question** / **pose_task** — Present questions or structured tasks to the learner
2. **assess_response** — Analyze what a response reveals about understanding
3. **update_learner_model** — Record evidence against 11 CCSS-M standards
4. **adjust_strategy** — Decide what to probe next (backward, forward, deeper, lateral)
5. **conclude_assessment** — Generate a structured evidence report

The agent adapts in real-time: if a learner struggles, it probes prerequisites; if they demonstrate strength, it probes more advanced concepts.

## Modes

- **Real** — A real learner answers via chat. The agent asks questions and waits for responses.
- **Synthetic** — A simulated learner persona (Mia, Derek, or Priya) responds automatically. Useful for demos and testing.

### Synthetic Personas

| Persona | Grade | Profile |
|---------|-------|---------|
| Mia | 3 | Fragmented understanding. Knows unit fractions as pizza slices. Thinks bigger denominator = bigger fraction. |
| Derek | 4 | Procedural but not conceptual. Can find equivalent fractions mechanically but can't explain why. Adds unlike denominators incorrectly. |
| Priya | 5 | Strong overall with specific gaps. Thinks multiplying always makes bigger. Can't explain fraction division conceptually. |

## Setup

```bash
# Clone
git clone git@github.com:rkoblic/assessment-agent.git
cd assessment-agent

# Install dependencies
pip install -e .

# Configure
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Usage

### CLI

```bash
# Run synthetic assessment with a persona
python -m src.main --mode synthetic --persona Mia

# Run real (interactive) assessment
python -m src.main --mode real
```

### API Server

```bash
uvicorn src.server:app --host 0.0.0.0 --port 8000
```

#### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/assess` | Start assessment (SSE stream) |
| POST | `/assess/{id}/respond` | Submit learner response (SSE stream) |
| GET | `/assessments` | List past assessments |
| GET | `/assessments/{id}` | Get assessment detail + report |
| GET | `/personas` | List available personas |
| GET | `/domain/standards` | CCSS-M standards being assessed |
| GET | `/domain/progressions` | Learning progression levels |
| GET | `/domain/misconceptions` | Known misconceptions |

All assessment endpoints stream Server-Sent Events (SSE) with event types: `session_started`, `agent_thinking`, `agent_question`, `agent_task`, `learner_response`, `observation`, `model_update`, `strategy_shift`, `assessment_complete`.

## Deployment

Deployed on Railway. See `Dockerfile` and `railway.toml` for configuration.

**Production URL:** https://assessment-agent-production.up.railway.app

## Architecture

```
src/
├── agent.py              # Core agent loop + system prompt
├── config.py             # API client, model config
├── db.py                 # SQLite storage
├── domain_knowledge.py   # 11 CCSS-M standards, misconceptions, progressions
├── evidence_report.py    # Structured report generation
├── learner_model.py      # Tracks evidence per standard
├── main.py               # CLI entry point
├── server.py             # FastAPI + SSE endpoints
├── synthetic_learner.py  # 3 simulated learner personas
├── task_library.py       # 17 mini-task templates
├── tools.py              # 6 tool definitions + handlers
└── types.py              # Pydantic models + enums
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `ANTHROPIC_API_KEY` | Yes | — | Claude API key |
| `MODEL` | No | `claude-sonnet-4-20250514` | Claude model to use |
| `MAX_TURNS` | No | `20` | Maximum assessment turns |
| `DB_PATH` | No | `assessments.db` | SQLite database path |
| `PORT` | No | `8000` | Server port |
