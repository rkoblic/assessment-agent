"""FastAPI server with SSE streaming for the assessment agent.

Endpoints:
    POST /assess                      — Start an assessment (SSE stream)
    POST /assess/{session_id}/respond — Submit a learner response (SSE stream)
    GET  /assessments                 — List past assessments
    GET  /assessments/{id}            — Get a full assessment report
    GET  /personas                    — List synthetic learner personas
    GET  /domain/standards            — All fractions standards
    GET  /domain/progressions         — Learning progression
    GET  /domain/misconceptions       — All misconceptions
    GET  /demo                        — Pre-recorded demo assessment
    GET  /prompt                      — View the full assessment system prompt
"""

from __future__ import annotations

import asyncio
import json
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from sse_starlette.sse import EventSourceResponse

from src.agent import AssessmentAgent, SYSTEM_PROMPT
from src.config import MAX_TURNS
from src.db import AssessmentDB
from src.demo import DEMO_ASSESSMENT
from src.domain_knowledge import (
    MISCONCEPTIONS,
    PROGRESSION,
    STANDARDS,
    get_all_misconceptions_summary,
    get_all_standards_summary,
    get_progression_summary,
)
from src.evidence_report import EvidenceReport
from src.learner_model import LearnerModel
from src.synthetic_learner import PERSONAS, SyntheticLearner
from src.types import AssessmentMode

# ---------------------------------------------------------------------------
# Rate limiter
# ---------------------------------------------------------------------------

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Assessment Agent API",
    description="AI agent for conversational fractions assessment",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session store for active assessments
active_sessions: dict[str, AssessmentAgent] = {}
active_learners: dict[str, SyntheticLearner] = {}


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------


class StartAssessmentRequest(BaseModel):
    mode: str = "synthetic"
    persona_name: str | None = "mia"


class LearnerResponseRequest(BaseModel):
    message: str


# ---------------------------------------------------------------------------
# Assessment endpoints (rate-limited — these trigger LLM calls)
# ---------------------------------------------------------------------------


@app.post("/assess")
@limiter.limit("5/minute")
async def start_assessment(
    request: Request, req: StartAssessmentRequest
) -> EventSourceResponse:
    """Start an assessment session. Returns an SSE stream of events."""
    mode = AssessmentMode(req.mode)
    agent = AssessmentAgent(mode=mode, persona_name=req.persona_name)
    active_sessions[agent.session.session_id] = agent

    if mode == AssessmentMode.SYNTHETIC and req.persona_name:
        learner = SyntheticLearner(req.persona_name)
        active_learners[agent.session.session_id] = learner

    async def event_generator() -> AsyncGenerator[dict, None]:
        # Start the assessment
        events = await asyncio.to_thread(agent.start)
        for event in events:
            yield {
                "event": event["event"],
                "data": json.dumps(event.get("data", {})),
            }

        # In synthetic mode, run the full assessment loop
        if mode == AssessmentMode.SYNTHETIC:
            synth_learner = active_learners.get(agent.session.session_id)
            if synth_learner:
                while not agent.is_complete:
                    question = agent.pending_question
                    if not question:
                        break

                    response = await asyncio.to_thread(
                        synth_learner.respond, question
                    )
                    yield {
                        "event": "learner_response",
                        "data": json.dumps({"response": response}),
                    }

                    events = await asyncio.to_thread(
                        agent.submit_response, response
                    )
                    for event in events:
                        yield {
                            "event": event["event"],
                            "data": json.dumps(event.get("data", {})),
                        }

                # Save to DB
                db = AssessmentDB()
                db.save_assessment(agent.session, agent.learner_model)

                # Clean up
                active_sessions.pop(agent.session.session_id, None)
                active_learners.pop(agent.session.session_id, None)

    return EventSourceResponse(event_generator())


@app.post("/assess/{session_id}/respond")
@limiter.limit("10/minute")
async def submit_response(
    request: Request, session_id: str, req: LearnerResponseRequest
) -> EventSourceResponse:
    """Submit a learner response (real learner mode). Returns SSE stream."""
    agent = active_sessions.get(session_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Session not found")

    async def event_generator() -> AsyncGenerator[dict, None]:
        events = await asyncio.to_thread(
            agent.submit_response, req.message
        )
        for event in events:
            yield {
                "event": event["event"],
                "data": json.dumps(event.get("data", {})),
            }

        if agent.is_complete:
            db = AssessmentDB()
            db.save_assessment(agent.session, agent.learner_model)
            active_sessions.pop(session_id, None)

    return EventSourceResponse(event_generator())


@app.get("/assessments")
@limiter.limit("30/minute")
async def list_assessments(request: Request) -> list[dict]:
    db = AssessmentDB()
    return db.list_assessments()


@app.get("/assessments/{assessment_id}")
@limiter.limit("30/minute")
async def get_assessment(request: Request, assessment_id: str) -> dict:
    db = AssessmentDB()
    result = db.get_assessment(assessment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return result


# ---------------------------------------------------------------------------
# Demo endpoint
# ---------------------------------------------------------------------------


@app.get("/demo")
@limiter.limit("30/minute")
async def get_demo(request: Request) -> dict:
    """Return a pre-recorded demo assessment showing the full event stream.

    This lets users see what an assessment looks like without making any
    LLM API calls.
    """
    return DEMO_ASSESSMENT


# ---------------------------------------------------------------------------
# Prompt endpoint
# ---------------------------------------------------------------------------


@app.get("/prompt")
@limiter.limit("30/minute")
async def get_prompt(request: Request) -> PlainTextResponse:
    """Return the full rendered system prompt used by the assessment agent.

    The prompt is rendered with the actual domain knowledge (standards,
    misconceptions, progression) and a blank learner model, so viewers
    can see exactly what the agent sees at the start of an assessment.
    """
    rendered = SYSTEM_PROMPT.format(
        max_turns=MAX_TURNS,
        standards_summary=get_all_standards_summary(),
        misconceptions_summary=get_all_misconceptions_summary(),
        progression_summary=get_progression_summary(),
        learner_model_summary=LearnerModel().to_summary_string(),
    )
    return PlainTextResponse(rendered)


# ---------------------------------------------------------------------------
# Persona & domain endpoints
# ---------------------------------------------------------------------------


@app.get("/personas")
@limiter.limit("30/minute")
async def list_personas(request: Request) -> list[dict]:
    return [
        {"name": p.name, "grade_level": p.grade_level}
        for p in PERSONAS.values()
    ]


@app.get("/domain/standards")
@limiter.limit("30/minute")
async def get_standards(request: Request) -> list[dict]:
    return [
        {
            "code": s.code,
            "grade": s.grade,
            "description": s.description,
            "learning_components": [
                {"code": lc.code, "description": lc.description}
                for lc in s.learning_components
            ],
        }
        for s in STANDARDS.values()
    ]


@app.get("/domain/progressions")
@limiter.limit("30/minute")
async def get_progressions(request: Request) -> list[dict]:
    return [
        {
            "grade": p.grade,
            "label": p.label,
            "standards": p.standards,
            "prerequisites": p.prerequisites,
            "next_levels": p.next_levels,
        }
        for p in PROGRESSION
    ]


@app.get("/domain/misconceptions")
@limiter.limit("30/minute")
async def get_misconceptions(request: Request) -> list[dict]:
    return [
        {
            "id": m.id,
            "category": m.category,
            "description": m.description,
            "example": m.example,
            "related_standards": m.related_standards,
        }
        for m in MISCONCEPTIONS
    ]
