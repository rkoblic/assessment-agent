"""Learner model — tracks evidence of understanding across standards.

Updated by the agent via the update_learner_model tool. This module
maintains the data structure; Claude makes the assessment decisions.
"""

from __future__ import annotations

from src.domain_knowledge import STANDARDS
from src.types import (
    Confidence,
    EvidenceStatus,
    LearningComponentEvidence,
    MisconceptionEvidence,
    MisconceptionStatus,
    StandardEvidence,
)


class LearnerModel:
    def __init__(self) -> None:
        # Evidence map for all standards
        self.standards_evidence: dict[str, StandardEvidence] = {}
        for code, std in STANDARDS.items():
            lcs = [
                LearningComponentEvidence(
                    code=lc.code,
                    description=lc.description,
                )
                for lc in std.learning_components
            ]
            self.standards_evidence[code] = StandardEvidence(
                standard_code=code,
                standard_description=std.description,
                learning_components=lcs,
            )

        # Misconceptions: populated as they are detected/probed
        self.misconceptions: dict[str, MisconceptionEvidence] = {}

        self.progression_position: str = "not_determined"
        self.overall_assessment: str = "Assessment not yet started"

    # ------------------------------------------------------------------
    # Serialization
    # ------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            "standards_evidence": {
                code: se.model_dump() for code, se in self.standards_evidence.items()
            },
            "misconceptions": {
                mid: me.model_dump() for mid, me in self.misconceptions.items()
            },
            "progression_position": self.progression_position,
            "overall_assessment": self.overall_assessment,
        }

    @classmethod
    def from_dict(cls, data: dict) -> LearnerModel:
        model = cls.__new__(cls)
        model.standards_evidence = {
            code: StandardEvidence(**se_data)
            for code, se_data in data.get("standards_evidence", {}).items()
        }
        model.misconceptions = {
            mid: MisconceptionEvidence(**me_data)
            for mid, me_data in data.get("misconceptions", {}).items()
        }
        model.progression_position = data.get("progression_position", "not_determined")
        model.overall_assessment = data.get("overall_assessment", "")
        return model

    # ------------------------------------------------------------------
    # Queries
    # ------------------------------------------------------------------

    def get_unassessed_standards(self) -> list[str]:
        return [
            code
            for code, se in self.standards_evidence.items()
            if se.status == EvidenceStatus.NOT_ASSESSED
        ]

    def get_gaps(self) -> list[str]:
        """Standards with partial or not_demonstrated evidence."""
        return [
            code
            for code, se in self.standards_evidence.items()
            if se.status in (EvidenceStatus.PARTIAL, EvidenceStatus.NOT_DEMONSTRATED)
        ]

    def get_strengths(self) -> list[str]:
        """Standards demonstrated with medium or high confidence."""
        return [
            code
            for code, se in self.standards_evidence.items()
            if se.status == EvidenceStatus.DEMONSTRATED
            and se.confidence in (Confidence.MEDIUM, Confidence.HIGH)
        ]

    # ------------------------------------------------------------------
    # Updates (called by tool handlers)
    # ------------------------------------------------------------------

    def update_standard(
        self,
        standard_code: str,
        status: str,
        confidence: str,
        evidence_summary: str,
    ) -> None:
        if standard_code not in self.standards_evidence:
            return
        se = self.standards_evidence[standard_code]
        se.status = EvidenceStatus(status)
        se.confidence = Confidence(confidence)
        if evidence_summary:
            se.evidence.append(evidence_summary)

    def add_misconception(
        self,
        misconception_id: str,
        description: str,
        status: str = "suspected",
        evidence: str = "",
    ) -> None:
        if misconception_id in self.misconceptions:
            me = self.misconceptions[misconception_id]
            me.status = MisconceptionStatus(status)
            if evidence:
                me.evidence.append(evidence)
        else:
            self.misconceptions[misconception_id] = MisconceptionEvidence(
                misconception_id=misconception_id,
                description=description,
                status=MisconceptionStatus(status),
                evidence=[evidence] if evidence else [],
            )

    def clear_misconception(self, misconception_id: str) -> None:
        if misconception_id in self.misconceptions:
            self.misconceptions[misconception_id].status = MisconceptionStatus.CLEARED

    # ------------------------------------------------------------------
    # Summary for system prompt
    # ------------------------------------------------------------------

    def to_summary_string(self) -> str:
        lines: list[str] = []

        lines.append(f"Progression position: {self.progression_position}")
        lines.append(f"Overall: {self.overall_assessment}")
        lines.append("")

        # Standards
        lines.append("Standards Evidence:")
        for code, se in self.standards_evidence.items():
            status_str = se.status.value
            conf_str = se.confidence.value
            lines.append(f"  {code}: {status_str} (confidence: {conf_str})")
            if se.evidence:
                for e in se.evidence[-2:]:  # last 2 evidence items
                    lines.append(f"    - {e}")
            for lc in se.learning_components:
                if lc.status != EvidenceStatus.NOT_ASSESSED:
                    lines.append(f"    LC {lc.code}: {lc.status.value}")

        # Misconceptions
        if self.misconceptions:
            lines.append("")
            lines.append("Misconceptions:")
            for mid, me in self.misconceptions.items():
                lines.append(f"  {me.description}: {me.status.value}")
                if me.evidence:
                    lines.append(f"    Evidence: {me.evidence[-1]}")

        return "\n".join(lines)
