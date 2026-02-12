"""Evidence report generation.

Produces structured reports from the conclude_assessment tool output
merged with the accumulated LearnerModel data.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.learner_model import LearnerModel
from src.types import AssessmentSession


class EvidenceReport:
    def __init__(
        self,
        session: AssessmentSession,
        learner_model: LearnerModel,
        conclusion_data: dict[str, Any],
    ) -> None:
        self.session = session
        self.learner_model = learner_model
        self.conclusion = conclusion_data

    def to_dict(self) -> dict[str, Any]:
        """Full structured report as a dict for JSON storage/API response."""
        return {
            "session_id": self.session.session_id,
            "mode": self.session.mode.value,
            "persona_name": self.session.persona_name,
            "started_at": self.session.started_at.isoformat(),
            "ended_at": (
                self.session.ended_at.isoformat()
                if self.session.ended_at
                else datetime.now(timezone.utc).isoformat()
            ),
            "turn_count": self.session.turn_count,
            "progression_summary": self.conclusion.get(
                "progression_summary", ""
            ),
            "standards_evidence_map": self._build_standards_map(),
            "misconception_report": self.conclusion.get(
                "misconception_report", []
            ),
            "overall_narrative": self.conclusion.get("overall_narrative", ""),
            "recommended_next_steps": self.conclusion.get(
                "recommended_next_steps", []
            ),
            "stop_reason": self.conclusion.get("stop_reason", ""),
            "conversation_log": [
                turn.model_dump(mode="json")
                for turn in self.session.conversation
            ],
        }

    def _build_standards_map(self) -> list[dict[str, Any]]:
        """Merge conclusion evidence_map with learner model data."""
        # Prefer the agent's conclusion data (more complete final summary),
        # fall back to the accumulated learner model for anything not covered.
        conclusion_map = {
            entry["standard_code"]: entry
            for entry in self.conclusion.get("evidence_map", [])
        }

        result = []
        for code, se in self.learner_model.standards_evidence.items():
            if code in conclusion_map:
                entry = conclusion_map[code]
            else:
                entry = {
                    "standard_code": se.standard_code,
                    "standard_description": se.standard_description,
                    "status": se.status.value,
                    "confidence": se.confidence.value,
                    "evidence": se.evidence,
                    "learning_components": [
                        {
                            "code": lc.code,
                            "description": lc.description,
                            "status": lc.status.value,
                        }
                        for lc in se.learning_components
                    ],
                }
            result.append(entry)
        return result

    def to_markdown(self) -> str:
        """Render the report as readable Markdown."""
        report = self.to_dict()
        name = report.get("persona_name") or "Anonymous"
        date = report["started_at"][:10]
        turns = report["turn_count"]

        lines = [
            "# Evidence of Learning Report",
            "",
            f"**Learner**: {name}",
            f"**Date**: {date}",
            "**Domain**: Fractions (CCSS-M Grades 2-5)",
            f"**Assessment Duration**: {turns} turns",
            "",
            "---",
            "",
            "## Progression Summary",
            "",
            report.get("progression_summary", "Not available."),
            "",
            "---",
            "",
            "## Standards Evidence Map",
            "",
        ]

        for std in report.get("standards_evidence_map", []):
            code = std.get("standard_code", "")
            desc = std.get("standard_description", "")
            status = std.get("status", "not_assessed")
            confidence = std.get("confidence", "low")
            evidence_list = std.get("evidence", [])

            lines.append(f"### {code}: {desc}")
            lines.append(f"- **Status**: {status}")
            lines.append(f"- **Confidence**: {confidence}")
            if evidence_list:
                lines.append("- **Evidence**:")
                for e in evidence_list:
                    lines.append(f"  - {e}")

            lcs = std.get("learning_components", [])
            if lcs:
                lines.append("- **Learning Components**:")
                for lc in lcs:
                    lc_status = lc.get("status", "not_assessed")
                    lines.append(
                        f"  - {lc.get('code', '')}: {lc.get('description', '')} "
                        f"— {lc_status}"
                    )
            lines.append("")

        lines.extend(
            [
                "---",
                "",
                "## Misconception Report",
                "",
            ]
        )

        for m in report.get("misconception_report", []):
            lines.append(f"### {m.get('description', '')}")
            lines.append(f"- **Status**: {m.get('status', '')}")
            lines.append(f"- **Evidence**: {m.get('evidence', '')}")
            lines.append("")

        lines.extend(
            [
                "---",
                "",
                "## Overall Narrative",
                "",
                report.get("overall_narrative", "Not available."),
                "",
                "---",
                "",
                "## Recommended Next Steps",
                "",
            ]
        )

        for step in report.get("recommended_next_steps", []):
            lines.append(f"- {step}")

        return "\n".join(lines)
