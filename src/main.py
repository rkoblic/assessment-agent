"""CLI entry point for the assessment agent.

Run assessments from the terminal with rich output.

Usage:
    python -m src.main --mode synthetic --persona mia
    python -m src.main --mode real
"""

from __future__ import annotations

import argparse
import sys

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from src.agent import AssessmentAgent
from src.evidence_report import EvidenceReport
from src.synthetic_learner import PERSONAS, SyntheticLearner
from src.types import AssessmentMode

console = Console()


def display_events(events: list[dict]) -> None:
    """Display SSE events in the terminal using rich formatting."""
    for event in events:
        event_type = event.get("event", "")
        data = event.get("data", {})

        if event_type == "session_started":
            console.print(
                f"[dim]Session started: {data.get('session_id', '')}[/]"
            )
        elif event_type == "agent_thinking":
            text = data.get("text", "")
            if text.strip():
                console.print(f"  [dim italic]{text}[/]")
        elif event_type == "agent_question":
            # Handled in the main loop (displayed as a panel)
            pass
        elif event_type == "agent_task":
            # Handled in the main loop (displayed as a panel)
            pass
        elif event_type == "observation":
            reveals = data.get("response_reveals", "")
            if reveals:
                console.print(f"  [yellow]Observation: {reveals}[/]")
        elif event_type == "model_update":
            summary = data.get("summary", "")
            assessed = data.get("standards_assessed", 0)
            console.print(
                f"  [cyan]Model updated ({assessed}/11 standards assessed)[/]"
            )
        elif event_type == "strategy_shift":
            direction = data.get("progression_direction", "")
            next_move = data.get("next_move", "")
            console.print(
                f"  [magenta]Strategy: {direction} — {next_move}[/]"
            )
        elif event_type == "assessment_complete":
            console.print()
            console.print(
                Panel("Assessment Complete", style="bold green", expand=False)
            )


def display_report(
    agent: AssessmentAgent,
) -> None:
    """Generate and display the evidence report."""
    if not agent.session.report:
        console.print("[red]No report data available.[/]")
        return

    report = EvidenceReport(
        session=agent.session,
        learner_model=agent.learner_model,
        conclusion_data=agent.session.report,
    )
    md = report.to_markdown()
    console.print()
    console.print(Markdown(md))


def run_synthetic_assessment(persona_name: str) -> None:
    """Run a full assessment with a synthetic learner."""
    config = PERSONAS[persona_name.lower()]
    console.print(
        Panel(
            f"Synthetic Assessment: {config.name} (Grade {config.grade_level})",
            style="bold blue",
            expand=False,
        )
    )
    console.print()

    agent = AssessmentAgent(
        mode=AssessmentMode.SYNTHETIC, persona_name=config.name
    )
    learner = SyntheticLearner(persona_name)

    # Start
    events = agent.start()
    display_events(events)

    # Loop until complete
    while not agent.is_complete:
        question = agent.pending_question
        if not question:
            console.print("[red]Agent did not produce a question. Ending.[/]")
            break

        console.print()
        console.print(Panel(question, title="Agent", border_style="blue"))

        response = learner.respond(question)
        console.print(Panel(response, title=config.name, border_style="green"))

        events = agent.submit_response(response)
        display_events(events)

    display_report(agent)


def run_real_assessment() -> None:
    """Run an assessment with a real human at the terminal."""
    console.print(
        Panel(
            "Real Learner Assessment",
            style="bold blue",
            expand=False,
        )
    )
    console.print(
        "[dim]Type your responses when prompted. "
        'Type "quit" to end early.[/]'
    )
    console.print()

    agent = AssessmentAgent(mode=AssessmentMode.REAL)

    events = agent.start()
    display_events(events)

    while not agent.is_complete:
        question = agent.pending_question
        if not question:
            console.print("[red]Agent did not produce a question. Ending.[/]")
            break

        console.print()
        console.print(Panel(question, title="Agent", border_style="blue"))

        response = console.input("[bold green]Your response: [/]")
        if response.strip().lower() == "quit":
            console.print("[dim]Assessment ended by learner.[/]")
            break

        events = agent.submit_response(response)
        display_events(events)

    display_report(agent)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Assessment Agent — conversational fractions assessment"
    )
    parser.add_argument(
        "--mode",
        choices=["real", "synthetic"],
        default="synthetic",
        help="Assessment mode (default: synthetic)",
    )
    parser.add_argument(
        "--persona",
        choices=list(PERSONAS.keys()),
        default="mia",
        help="Synthetic learner persona (default: mia)",
    )
    args = parser.parse_args()

    if args.mode == "synthetic":
        run_synthetic_assessment(args.persona)
    else:
        run_real_assessment()


if __name__ == "__main__":
    main()
