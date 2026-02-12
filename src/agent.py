"""Core assessment agent — system prompt, tool orchestration, decision loop.

The agent uses Claude's tool-use to conduct adaptive conversational
assessments. It calls tools to ask questions, assess responses, update
its learner model, adjust strategy, and conclude the assessment.
"""

from __future__ import annotations

import uuid
from typing import Any

from src.config import MAX_TOKENS, MAX_TURNS, MODEL, get_client
from src.domain_knowledge import (
    get_all_misconceptions_summary,
    get_all_standards_summary,
    get_progression_summary,
)
from src.learner_model import LearnerModel
from src.tools import TOOL_DEFINITIONS, handle_tool_call
from src.types import AssessmentMode, AssessmentSession, ConversationTurn


# ---------------------------------------------------------------------------
# System Prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are an expert mathematics assessment specialist conducting a one-on-one \
conversational assessment of a learner's understanding of fractions \
(CCSS-M, Grades 2-5).

## Your Persona
You are warm, encouraging, and genuinely curious about how this learner \
thinks about fractions. This is a conversation, not a test. Never tell the \
learner they are wrong directly — instead, probe to understand their \
reasoning. Use language appropriate for elementary school students.

## Your Goal
Build a complete evidence map of this learner's fraction understanding by:
1. Determining which standards they have demonstrated understanding of
2. Identifying specific misconceptions they hold
3. Locating their position on the fractions learning progression
4. Gathering sufficient evidence (with confidence levels) for each claim

## Assessment Protocol
1. START: Greet the learner warmly. Ask an entry-level question targeting \
Grade 3-4 level.
2. After each learner response, ALWAYS call these tools in order:
   a. assess_response — analyze what the response reveals
   b. update_learner_model — record your updated understanding
   c. adjust_strategy — plan your next move
   d. Then ask_question OR pose_task based on your strategy
3. BACKWARD: If the learner struggles, probe prerequisite understanding.
4. FORWARD: If the learner demonstrates strength, probe more advanced concepts.
5. DEEPER: If you need more evidence on a standard, ask at a different depth.
6. LATERAL: If you want to test transfer, pose a different task type.

## Tool Usage Rules
- After EVERY learner response, call assess_response → update_learner_model \
→ adjust_strategy before your next question/task.
- Use ask_question for conversational probes. Use pose_task for structured \
mini-tasks.
- Keep your questions/tasks concise: 1-3 sentences max.
- Mix question types: conceptual understanding, procedural fluency, transfer.
- Use mini-tasks strategically — not every turn, but when a task would \
reveal something a question can't.
- Call conclude_assessment when you have sufficient evidence across the \
progression OR after {max_turns} turns.
- Aim for 8-15 turns of meaningful interaction.
- Do NOT output conversational text to the learner outside of tool calls. \
All learner-facing content goes through ask_question or pose_task.

## Standards Being Assessed
{standards_summary}

## Known Misconceptions to Probe For
{misconceptions_summary}

## Learning Progression
{progression_summary}

## Current Learner Model
{learner_model_summary}
"""


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

class AssessmentAgent:
    """Runs the assessment agent loop.

    The loop continues until the agent asks a question (needs learner input),
    concludes the assessment, or hits a safety limit.
    """

    def __init__(
        self,
        mode: AssessmentMode,
        persona_name: str | None = None,
    ) -> None:
        self.client = get_client()
        self.mode = mode
        self.persona_name = persona_name
        self.session = AssessmentSession(
            session_id=str(uuid.uuid4()),
            mode=mode,
            persona_name=persona_name,
        )
        self.learner_model = LearnerModel()
        self.messages: list[dict[str, Any]] = []
        self.turn_count = 0
        self.is_complete = False
        self.pending_question: str | None = None
        self.events: list[dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start(self) -> list[dict[str, Any]]:
        """Start the assessment. Returns SSE events."""
        self.events = [
            {
                "event": "session_started",
                "data": {"session_id": self.session.session_id},
            }
        ]
        self.messages = [
            {
                "role": "user",
                "content": (
                    "Please begin the assessment. Greet the learner warmly "
                    "and ask your first question using the ask_question tool."
                ),
            }
        ]
        self._run_agent_loop()
        return self.events

    def submit_response(self, learner_response: str) -> list[dict[str, Any]]:
        """Submit a learner response and run the next agent turn."""
        self.events = []
        self.turn_count += 1
        self.session.turn_count = self.turn_count
        self.pending_question = None

        # Record in conversation log
        self.session.conversation.append(
            ConversationTurn(
                turn_number=self.turn_count,
                role="learner",
                content=learner_response,
            )
        )

        # Check if we should auto-conclude due to max turns
        if self.turn_count >= MAX_TURNS:
            conclude_prompt = (
                f'The learner responded: "{learner_response}"\n\n'
                "You have reached the maximum number of assessment turns. "
                "Please call assess_response for this final response, then "
                "update_learner_model, then call conclude_assessment to "
                "produce the final report."
            )
        else:
            turns_remaining = MAX_TURNS - self.turn_count
            conclude_prompt = (
                f'The learner responded: "{learner_response}"\n\n'
                "Please assess this response using assess_response, update "
                "the learner model, adjust your strategy, and then ask your "
                "next question or pose a task. If you have gathered "
                f"sufficient evidence, call conclude_assessment. "
                f"({turns_remaining} turns remaining)"
            )

        self.messages.append({"role": "user", "content": conclude_prompt})
        self._run_agent_loop()
        return self.events

    # ------------------------------------------------------------------
    # Internal loop
    # ------------------------------------------------------------------

    def _build_system_prompt(self) -> str:
        return SYSTEM_PROMPT.format(
            max_turns=MAX_TURNS,
            standards_summary=get_all_standards_summary(),
            misconceptions_summary=get_all_misconceptions_summary(),
            progression_summary=get_progression_summary(),
            learner_model_summary=self.learner_model.to_summary_string(),
        )

    def _run_agent_loop(self) -> None:
        """Run the agent loop until it needs learner input or finishes."""
        # Safety limit to prevent infinite loops
        max_iterations = 10

        for _ in range(max_iterations):
            if self.is_complete:
                break

            response = self.client.messages.create(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=self._build_system_prompt(),
                tools=TOOL_DEFINITIONS,
                messages=self.messages,
            )

            # Append assistant response to message history
            # Convert content blocks to serializable format
            assistant_content = []
            for block in response.content:
                if block.type == "text":
                    assistant_content.append(
                        {"type": "text", "text": block.text}
                    )
                    if block.text.strip():
                        self.events.append(
                            {
                                "event": "agent_thinking",
                                "data": {"text": block.text},
                            }
                        )
                elif block.type == "tool_use":
                    assistant_content.append(
                        {
                            "type": "tool_use",
                            "id": block.id,
                            "name": block.name,
                            "input": block.input,
                        }
                    )

            self.messages.append(
                {"role": "assistant", "content": assistant_content}
            )

            # Process tool calls
            tool_use_blocks = [
                b for b in response.content if b.type == "tool_use"
            ]

            if not tool_use_blocks:
                # No tools called — unusual, but break
                break

            tool_results = []
            should_wait_for_learner = False

            for tool_block in tool_use_blocks:
                result_text, event = handle_tool_call(
                    tool_block.name,
                    tool_block.input,
                    self.session,
                    self.learner_model,
                )
                if event:
                    self.events.append(event)

                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_block.id,
                        "content": result_text,
                    }
                )

                if tool_block.name in ("ask_question", "pose_task"):
                    should_wait_for_learner = True
                    self.pending_question = tool_block.input.get(
                        "question"
                    ) or tool_block.input.get("task_content")

                if tool_block.name == "conclude_assessment":
                    self.is_complete = True

            # Send tool results back
            self.messages.append({"role": "user", "content": tool_results})

            if should_wait_for_learner or self.is_complete:
                break

            if response.stop_reason == "end_turn":
                break
