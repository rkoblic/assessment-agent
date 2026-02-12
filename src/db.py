"""SQLite storage for assessment results."""

from __future__ import annotations

import json
import sqlite3
from datetime import datetime, timezone
from typing import Any

from src.config import DB_PATH
from src.learner_model import LearnerModel
from src.types import AssessmentSession


class AssessmentDB:
    def __init__(self, db_path: str = DB_PATH) -> None:
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS assessments (
                id TEXT PRIMARY KEY,
                mode TEXT NOT NULL,
                persona_name TEXT,
                started_at TEXT NOT NULL,
                ended_at TEXT,
                turn_count INTEGER DEFAULT 0,
                report TEXT,
                learner_model TEXT,
                conversation TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
        conn.close()

    def save_assessment(
        self,
        session: AssessmentSession,
        learner_model: LearnerModel,
    ) -> None:
        conn = sqlite3.connect(self.db_path)
        conn.execute(
            """
            INSERT OR REPLACE INTO assessments
            (id, mode, persona_name, started_at, ended_at, turn_count,
             report, learner_model, conversation)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                session.session_id,
                session.mode.value,
                session.persona_name,
                session.started_at.isoformat(),
                (
                    session.ended_at.isoformat()
                    if session.ended_at
                    else datetime.now(timezone.utc).isoformat()
                ),
                session.turn_count,
                json.dumps(session.report) if session.report else None,
                json.dumps(learner_model.to_dict()),
                json.dumps(
                    [t.model_dump(mode="json") for t in session.conversation]
                ),
            ),
        )
        conn.commit()
        conn.close()

    def list_assessments(self) -> list[dict[str, Any]]:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT id, mode, persona_name, started_at, ended_at, turn_count
            FROM assessments ORDER BY created_at DESC
            """
        ).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def get_assessment(self, assessment_id: str) -> dict[str, Any] | None:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM assessments WHERE id = ?", (assessment_id,)
        ).fetchone()
        conn.close()
        if not row:
            return None
        result = dict(row)
        for json_field in ("report", "learner_model", "conversation"):
            if result.get(json_field):
                result[json_field] = json.loads(result[json_field])
        return result
