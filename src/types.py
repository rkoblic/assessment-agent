"""Shared data types for the assessment agent."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class AssessmentMode(str, Enum):
    REAL = "real"
    SYNTHETIC = "synthetic"


class EvidenceStatus(str, Enum):
    DEMONSTRATED = "demonstrated"
    PARTIAL = "partial"
    NOT_DEMONSTRATED = "not_demonstrated"
    NOT_ASSESSED = "not_assessed"


class Confidence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class MisconceptionStatus(str, Enum):
    CONFIRMED = "confirmed"
    SUSPECTED = "suspected"
    CLEARED = "cleared"


class DepthLevel(str, Enum):
    RECALL = "recall"
    CONCEPTUAL = "conceptual"
    APPLICATION = "application"
    TRANSFER = "transfer"


class TaskType(str, Enum):
    COMPARE_FRACTIONS = "compare_fractions"
    ORDER_FRACTIONS = "order_fractions"
    FIND_EQUIVALENT = "find_equivalent"
    PLACE_ON_NUMBER_LINE = "place_on_number_line"
    COMPUTE = "compute"
    DECOMPOSE = "decompose"
    WORD_PROBLEM = "word_problem"


class ProgressionDirection(str, Enum):
    PROBE_BACKWARD = "probe_backward"
    PROBE_FORWARD = "probe_forward"
    PROBE_DEEPER = "probe_deeper"
    PROBE_LATERAL = "probe_lateral"


class StopReason(str, Enum):
    SUFFICIENT_EVIDENCE = "sufficient_evidence"
    MAX_TURNS = "max_turns"
    LEARNER_DISENGAGED = "learner_disengaged"


# ---------------------------------------------------------------------------
# Evidence structures
# ---------------------------------------------------------------------------

class LearningComponentEvidence(BaseModel):
    code: str
    description: str
    status: EvidenceStatus = EvidenceStatus.NOT_ASSESSED
    evidence: list[str] = Field(default_factory=list)


class StandardEvidence(BaseModel):
    standard_code: str
    standard_description: str
    status: EvidenceStatus = EvidenceStatus.NOT_ASSESSED
    confidence: Confidence = Confidence.LOW
    evidence: list[str] = Field(default_factory=list)
    learning_components: list[LearningComponentEvidence] = Field(
        default_factory=list
    )


class MisconceptionEvidence(BaseModel):
    misconception_id: str
    description: str
    status: MisconceptionStatus = MisconceptionStatus.SUSPECTED
    evidence: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Session structures
# ---------------------------------------------------------------------------

class ConversationTurn(BaseModel):
    turn_number: int
    role: str  # "agent" or "learner"
    content: str
    tool_calls: list[dict] = Field(default_factory=list)
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class AssessmentSession(BaseModel):
    session_id: str
    mode: AssessmentMode
    persona_name: Optional[str] = None
    started_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    ended_at: Optional[datetime] = None
    conversation: list[ConversationTurn] = Field(default_factory=list)
    learner_model: Optional[dict] = None
    report: Optional[dict] = None
    turn_count: int = 0
