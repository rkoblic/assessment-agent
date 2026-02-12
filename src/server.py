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
"""

from __future__ import annotations

import asyncio
import json
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sse_starlette.sse import EventSourceResponse

from src.agent import AssessmentAgent
from src.db import AssessmentDB
from src.domain_knowledge import MISCONCEPTIONS, PROGRESSION, STANDARDS
from src.evidence_report import EvidenceReport
from src.synthetic_learner import PERSONAS, SyntheticLearner
from src.types import AssessmentMode

app = FastAPI(
    title="Assessment Agent API",
    description="AI agent for conversational fractions assessment",
    version="0.1.0",
)

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
# Assessment endpoints
# ---------------------------------------------------------------------------


@app.post("/assess")
async def start_assessment(req: StartAssessmentRequest) -> EventSourceResponse:
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
async def submit_response(
    session_id: str, req: LearnerResponseRequest
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
async def list_assessments() -> list[dict]:
    db = AssessmentDB()
    return db.list_assessments()


@app.get("/assessments/{assessment_id}")
async def get_assessment(assessment_id: str) -> dict:
    db = AssessmentDB()
    result = db.get_assessment(assessment_id)
    if not result:
        raise HTTPException(status_code=404, detail="Assessment not found")
    return result


# ---------------------------------------------------------------------------
# Persona & domain endpoints
# ---------------------------------------------------------------------------


@app.get("/personas")
async def list_personas() -> list[dict]:
    return [
        {"name": p.name, "grade_level": p.grade_level}
        for p in PERSONAS.values()
    ]


@app.get("/domain/standards")
async def get_standards() -> list[dict]:
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
async def get_progressions() -> list[dict]:
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
async def get_misconceptions() -> list[dict]:
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
