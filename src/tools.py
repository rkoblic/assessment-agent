"""Tool definitions and handlers for the assessment agent.

Defines the 6 tools in Anthropic tool-use JSON format and the handler
functions that execute when the agent calls each tool.

Most tools are "cognitive" — they structure the agent's thinking and
update internal state. ask_question and pose_task produce output shown
to the learner. conclude_assessment triggers report generation.
"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.learner_model import LearnerModel
    from src.types import AssessmentSession


# ---------------------------------------------------------------------------
# Tool Definitions (Anthropic tool-use JSON format)
# ---------------------------------------------------------------------------

TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "name": "ask_question",
        "description": (
            "Ask the learner a conversational question to probe their "
            "understanding of fractions. Only the 'question' text will be "
            "shown to the learner. The 'intent' field is your strategic "
            "reasoning — logged but not shown to the learner."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": (
                        "The question to ask the learner. Should be "
                        "conversational and encouraging."
                    ),
                },
                "target_standard": {
                    "type": "string",
                    "description": (
                        "Which CCSS-M standard this question probes, "
                        "e.g. '3.NF.A.1'"
                    ),
                },
                "target_learning_component": {
                    "type": "string",
                    "description": (
                        "Specific learning component being assessed, if applicable"
                    ),
                },
                "depth": {
                    "type": "string",
                    "enum": ["recall", "conceptual", "application", "transfer"],
                    "description": "The depth of understanding this question probes",
                },
                "intent": {
                    "type": "string",
                    "description": (
                        "Strategic reasoning for why you're asking this "
                        "question now. Not shown to learner."
                    ),
                },
            },
            "required": ["question", "target_standard", "depth", "intent"],
        },
    },
    {
        "name": "pose_task",
        "description": (
            "Present a structured mini-task to the learner. The 'task_content' "
            "will be shown to the learner. Include expected_answer and "
            "common_errors to help you evaluate the response later."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "task_type": {
                    "type": "string",
                    "enum": [
                        "compare_fractions",
                        "order_fractions",
                        "find_equivalent",
                        "place_on_number_line",
                        "compute",
                        "decompose",
                        "word_problem",
                    ],
                    "description": "The type of mini-task",
                },
                "task_content": {
                    "type": "string",
                    "description": "The specific task presented to the learner",
                },
                "target_standard": {
                    "type": "string",
                    "description": "Which CCSS-M standard this task assesses",
                },
                "expected_answer": {
                    "type": "string",
                    "description": "What a correct response looks like",
                },
                "common_errors": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Errors that would indicate specific misconceptions"
                    ),
                },
                "intent": {
                    "type": "string",
                    "description": "Strategic reasoning for this task",
                },
            },
            "required": [
                "task_type",
                "task_content",
                "target_standard",
                "expected_answer",
                "common_errors",
                "intent",
            ],
        },
    },
    {
        "name": "assess_response",
        "description": (
            "After each learner response, analyze what it reveals about "
            "their understanding. You MUST call this after every learner "
            "response before doing anything else."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "response_reveals": {
                    "type": "string",
                    "description": (
                        "What this response tells us about the learner's "
                        "understanding"
                    ),
                },
                "evidence_for": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "standard_code": {"type": "string"},
                            "learning_component": {"type": "string"},
                            "confidence": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                            },
                        },
                        "required": ["standard_code", "confidence"],
                    },
                    "description": (
                        "Standards/LCs this provides POSITIVE evidence for"
                    ),
                },
                "evidence_against": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "standard_code": {"type": "string"},
                            "learning_component": {"type": "string"},
                            "confidence": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                            },
                        },
                        "required": ["standard_code", "confidence"],
                    },
                    "description": (
                        "Standards/LCs this provides NEGATIVE evidence for"
                    ),
                },
                "misconceptions_detected": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Specific misconceptions surfaced",
                },
                "misconceptions_ruled_out": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Misconceptions we can now eliminate",
                },
                "notes": {
                    "type": "string",
                    "description": "Your reasoning about this response",
                },
            },
            "required": [
                "response_reveals",
                "evidence_for",
                "evidence_against",
                "misconceptions_detected",
                "misconceptions_ruled_out",
                "notes",
            ],
        },
    },
    {
        "name": "update_learner_model",
        "description": (
            "Update the running model of the learner's knowledge state. "
            "Call this after assess_response to record your updated "
            "understanding of the learner."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "standards_status": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "standard_code": {"type": "string"},
                            "status": {
                                "type": "string",
                                "enum": [
                                    "demonstrated",
                                    "partial",
                                    "not_demonstrated",
                                    "not_assessed",
                                ],
                            },
                            "confidence": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                            },
                            "evidence_summary": {"type": "string"},
                        },
                        "required": [
                            "standard_code",
                            "status",
                            "confidence",
                            "evidence_summary",
                        ],
                    },
                    "description": (
                        "For each standard assessed so far: current status "
                        "and evidence summary"
                    ),
                },
                "progression_position": {
                    "type": "string",
                    "description": (
                        "Where the learner sits on the fractions progression"
                    ),
                },
                "active_misconceptions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Misconception IDs currently held by learner",
                },
                "cleared_misconceptions": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Misconception IDs ruled out by evidence",
                },
                "overall_assessment": {
                    "type": "string",
                    "description": "Current holistic picture of the learner",
                },
            },
            "required": [
                "standards_status",
                "progression_position",
                "active_misconceptions",
                "cleared_misconceptions",
                "overall_assessment",
            ],
        },
    },
    {
        "name": "adjust_strategy",
        "description": (
            "Plan your next assessment move based on what you've learned. "
            "Call this after update_learner_model to decide what to probe next."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "current_picture": {
                    "type": "string",
                    "description": "What we know so far about the learner",
                },
                "gaps_in_evidence": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "What we still need to assess",
                },
                "next_move": {
                    "type": "string",
                    "description": "What to probe next and why",
                },
                "progression_direction": {
                    "type": "string",
                    "enum": [
                        "probe_backward",
                        "probe_forward",
                        "probe_deeper",
                        "probe_lateral",
                    ],
                    "description": (
                        "Direction to move on the learning progression"
                    ),
                },
            },
            "required": [
                "current_picture",
                "gaps_in_evidence",
                "next_move",
                "progression_direction",
            ],
        },
    },
    {
        "name": "conclude_assessment",
        "description": (
            "End the assessment and produce the final evidence report. "
            "Call this when you have gathered sufficient evidence across "
            "the progression, or when the maximum number of turns has been "
            "reached. This must be your FINAL tool call."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "evidence_map": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "standard_code": {"type": "string"},
                            "standard_description": {"type": "string"},
                            "status": {
                                "type": "string",
                                "enum": [
                                    "demonstrated",
                                    "partial",
                                    "not_demonstrated",
                                    "not_assessed",
                                ],
                            },
                            "confidence": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                            },
                            "evidence": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                            "learning_components": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "code": {"type": "string"},
                                        "description": {"type": "string"},
                                        "status": {"type": "string"},
                                    },
                                },
                            },
                        },
                        "required": [
                            "standard_code",
                            "standard_description",
                            "status",
                            "confidence",
                            "evidence",
                        ],
                    },
                    "description": "Per-standard evidence with status and confidence",
                },
                "progression_summary": {
                    "type": "string",
                    "description": (
                        "Where the learner is on the fractions progression "
                        "and what that means"
                    ),
                },
                "misconception_report": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "description": {"type": "string"},
                            "status": {
                                "type": "string",
                                "enum": ["confirmed", "suspected", "cleared"],
                            },
                            "evidence": {"type": "string"},
                        },
                        "required": ["description", "status", "evidence"],
                    },
                    "description": (
                        "Each misconception probed with status and evidence"
                    ),
                },
                "overall_narrative": {
                    "type": "string",
                    "description": (
                        "A 2-3 paragraph teacher-readable summary of this "
                        "learner's understanding"
                    ),
                },
                "recommended_next_steps": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Specific, actionable recommendations for instruction"
                    ),
                },
                "stop_reason": {
                    "type": "string",
                    "enum": [
                        "sufficient_evidence",
                        "max_turns",
                        "learner_disengaged",
                    ],
                    "description": "Why the assessment ended",
                },
            },
            "required": [
                "evidence_map",
                "progression_summary",
                "misconception_report",
                "overall_narrative",
                "recommended_next_steps",
                "stop_reason",
            ],
        },
    },
]


# ---------------------------------------------------------------------------
# Tool Handlers
# ---------------------------------------------------------------------------

def handle_tool_call(
    tool_name: str,
    tool_input: dict[str, Any],
    session: AssessmentSession,
    learner_model: LearnerModel,
) -> tuple[str, dict[str, Any] | None]:
    """Execute a tool call and return (result_text, event_to_emit).

    The event_to_emit is a dict with "event" and "data" keys for SSE,
    or None if no event should be emitted.
    """
    handlers = {
        "ask_question": _handle_ask_question,
        "pose_task": _handle_pose_task,
        "assess_response": _handle_assess_response,
        "update_learner_model": _handle_update_learner_model,
        "adjust_strategy": _handle_adjust_strategy,
        "conclude_assessment": _handle_conclude_assessment,
    }
    handler = handlers.get(tool_name)
    if handler is None:
        return f"Unknown tool: {tool_name}", None
    return handler(tool_input, session, learner_model)


# -- ask_question ----------------------------------------------------------

def _handle_ask_question(
    inp: dict[str, Any],
    session: AssessmentSession,
    _learner_model: LearnerModel,
) -> tuple[str, dict[str, Any] | None]:
    from src.types import ConversationTurn

    question = inp.get("question", "")
    session.conversation.append(
        ConversationTurn(
            turn_number=session.turn_count,
            role="agent",
            content=question,
            tool_calls=[{"tool": "ask_question", "input": inp}],
        )
    )
    event = {
        "event": "agent_question",
        "data": {
            "question": question,
            "target_standard": inp.get("target_standard", ""),
            "depth": inp.get("depth", ""),
        },
    }
    return "Question presented to learner. Awaiting their response.", event


# -- pose_task -------------------------------------------------------------

def _handle_pose_task(
    inp: dict[str, Any],
    session: AssessmentSession,
    _learner_model: LearnerModel,
) -> tuple[str, dict[str, Any] | None]:
    from src.types import ConversationTurn

    task_content = inp.get("task_content", "")
    session.conversation.append(
        ConversationTurn(
            turn_number=session.turn_count,
            role="agent",
            content=task_content,
            tool_calls=[{"tool": "pose_task", "input": inp}],
        )
    )
    event = {
        "event": "agent_task",
        "data": {
            "task_type": inp.get("task_type", ""),
            "task_content": task_content,
            "target_standard": inp.get("target_standard", ""),
        },
    }
    return "Task presented to learner. Awaiting their response.", event


# -- assess_response -------------------------------------------------------

def _handle_assess_response(
    inp: dict[str, Any],
    session: AssessmentSession,
    _learner_model: LearnerModel,
) -> tuple[str, dict[str, Any] | None]:
    evidence_for = inp.get("evidence_for", [])
    evidence_against = inp.get("evidence_against", [])
    misconceptions = inp.get("misconceptions_detected", [])
    ruled_out = inp.get("misconceptions_ruled_out", [])

    summary_parts = [f"Assessment recorded."]
    if evidence_for:
        codes = [e.get("standard_code", "?") for e in evidence_for]
        summary_parts.append(f"Evidence FOR: {', '.join(codes)}.")
    if evidence_against:
        codes = [e.get("standard_code", "?") for e in evidence_against]
        summary_parts.append(f"Evidence AGAINST: {', '.join(codes)}.")
    if misconceptions:
        summary_parts.append(f"Misconceptions detected: {', '.join(misconceptions)}.")
    if ruled_out:
        summary_parts.append(f"Misconceptions ruled out: {', '.join(ruled_out)}.")

    result_text = " ".join(summary_parts)

    event = {
        "event": "observation",
        "data": {
            "response_reveals": inp.get("response_reveals", ""),
            "evidence_for": evidence_for,
            "evidence_against": evidence_against,
            "misconceptions_detected": misconceptions,
            "misconceptions_ruled_out": ruled_out,
        },
    }
    return result_text, event


# -- update_learner_model --------------------------------------------------

def _handle_update_learner_model(
    inp: dict[str, Any],
    session: AssessmentSession,
    learner_model: LearnerModel,
) -> tuple[str, dict[str, Any] | None]:
    # Update standards
    for status_entry in inp.get("standards_status", []):
        learner_model.update_standard(
            standard_code=status_entry.get("standard_code", ""),
            status=status_entry.get("status", "not_assessed"),
            confidence=status_entry.get("confidence", "low"),
            evidence_summary=status_entry.get("evidence_summary", ""),
        )

    # Update misconceptions
    for mid in inp.get("active_misconceptions", []):
        # Add or update as suspected/confirmed
        learner_model.add_misconception(
            misconception_id=mid,
            description=mid,  # agent may use descriptive IDs
            status="suspected",
        )

    for mid in inp.get("cleared_misconceptions", []):
        learner_model.clear_misconception(mid)

    # Update progression and overall
    learner_model.progression_position = inp.get(
        "progression_position", learner_model.progression_position
    )
    learner_model.overall_assessment = inp.get(
        "overall_assessment", learner_model.overall_assessment
    )

    summary = (
        f"Learner model updated. Position: {learner_model.progression_position}. "
        f"{learner_model.overall_assessment}"
    )
    event = {
        "event": "model_update",
        "data": {
            "summary": summary,
            "progression_position": learner_model.progression_position,
            "standards_assessed": len(
                [
                    s
                    for s in learner_model.standards_evidence.values()
                    if s.status.value != "not_assessed"
                ]
            ),
        },
    }
    return summary, event


# -- adjust_strategy -------------------------------------------------------

def _handle_adjust_strategy(
    inp: dict[str, Any],
    _session: AssessmentSession,
    _learner_model: LearnerModel,
) -> tuple[str, dict[str, Any] | None]:
    next_move = inp.get("next_move", "")
    direction = inp.get("progression_direction", "")
    result_text = f"Strategy adjusted. Next move: {next_move} (direction: {direction})"

    event = {
        "event": "strategy_shift",
        "data": {
            "current_picture": inp.get("current_picture", ""),
            "gaps_in_evidence": inp.get("gaps_in_evidence", []),
            "next_move": next_move,
            "progression_direction": direction,
        },
    }
    return result_text, event


# -- conclude_assessment ---------------------------------------------------

def _handle_conclude_assessment(
    inp: dict[str, Any],
    session: AssessmentSession,
    learner_model: LearnerModel,
) -> tuple[str, dict[str, Any] | None]:
    from datetime import datetime, timezone

    # Store the conclusion data on the session
    session.report = inp
    session.ended_at = datetime.now(timezone.utc)
    session.learner_model = learner_model.to_dict()

    result_text = (
        f"Assessment concluded. Stop reason: {inp.get('stop_reason', 'unknown')}. "
        f"Report generated with {len(inp.get('evidence_map', []))} standards assessed."
    )

    event = {
        "event": "assessment_complete",
        "data": {
            "report": inp,
            "session_id": session.session_id,
        },
    }
    return result_text, event
