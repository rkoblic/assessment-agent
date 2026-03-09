# Assessment Agent Backend

AI agent that conducts adaptive conversational assessments of learner understanding in fractions (CCSS-M, Grades 2-5).

## Architecture

- **Framework**: FastAPI with SSE streaming (sse-starlette)
- **AI**: Anthropic Claude API with tool-use for autonomous agent loop
- **Database**: SQLite for assessment storage
- **Rate limiting**: slowapi (per-IP)
- **Deployment**: Railway (auto-deploys from `main` branch)

## Key files

- `src/agent.py` — Core agent loop + system prompt. The agent autonomously decides what to ask, how to interpret responses, and when to conclude.
- `src/tools.py` — 6 tool definitions (ask_question, pose_task, assess_response, update_learner_model, adjust_strategy, conclude_assessment) in Anthropic tool-use format + handlers.
- `src/server.py` — FastAPI endpoints. Rate-limited. Includes `/demo` (pre-recorded assessment) and `/prompt` (rendered system prompt viewer).
- `src/demo.py` — Pre-recorded 8-turn demo assessment fixture (Mia, Grade 4).
- `src/domain_knowledge.py` — CCSS-M standards, learning components, misconceptions, learning progression (hardcoded from PRD).
- `src/synthetic_learner.py` — AI-powered synthetic learner personas (Mia, Derek, Priya) for testing.
- `src/learner_model.py` — Running model of learner knowledge state.
- `src/config.py` — Env-based config (API key, model, max turns, DB path).
- `src/db.py` — SQLite storage for completed assessments.

## Running locally

```bash
pip install -e .
# Set ANTHROPIC_API_KEY in .env
uvicorn src.server:app --reload
# or CLI mode:
python -m src.main --mode synthetic --persona mia
```

## Companion repo

Frontend dashboard: `rkoblic/assessment-agent-dashboard` (Next.js, deployed on Vercel or similar). Lives at `/Users/rachelkoblic/assessment-agent-dashboard` locally.
