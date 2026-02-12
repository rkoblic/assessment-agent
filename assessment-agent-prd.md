# Assessment Agent — Product Requirements Document

## What This Is

An AI agent that conducts conversational assessments to determine evidence of learning. It talks to a learner (real human or synthetic), asks strategic questions, poses targeted mini-tasks, and builds a real-time model of the learner's understanding. The output is a structured evidence report mapping what the learner knows to standards, learning progressions, and specific misconceptions.

This is a **real agent** — it uses Claude's tool-use (function calling) to make autonomous decisions in a loop. Every question it asks is a strategic choice based on what it's learned so far. No two assessments follow the same path.

## Why This Matters

Traditional assessments are static: every student gets the same questions in the same order. A skilled human assessor works differently — they listen, probe, adapt, and build a picture of what the student actually understands (not just what they can recall). This agent does that, at scale.

The output isn't a score. It's an **evidence map**: here's what this learner demonstrably understands, here's what they can do, here's where they're stuck, and here's the specific evidence for each claim — all mapped to real standards and learning progressions.

## V1 Scope

### Domain: Fractions (Grades 3-5, CCSS-M)

V1 focuses exclusively on fractions. This is the richest domain for a first build because:
- Decades of research on common misconceptions
- Well-defined learning progression across grades 3-5
- Learning components available from the Knowledge Graph at granular level
- Universal — every educator immediately understands the domain

### Two Modes

1. **Real Learner Mode**: A human interacts with the agent via the web UI. The agent assesses them through conversation.
2. **Synthetic Learner Mode**: The agent talks to a synthetic learner persona (like from the Synthetic Learner Generator). Used for development, demos, and testing the agent's assessment capabilities.

The agent's behavior is identical in both modes — it doesn't know which kind of learner it's talking to. The only difference is whether the responses come from a human or an LLM.

---

## Architecture

### Stack
- **Python + FastAPI** on Railway (agent backend + API)
- **Next.js** on Vercel (dashboard/UI)
- **Anthropic SDK** (Claude with tool-use as the agent brain)
- **SQLite** for assessment result storage
- **Learning Commons Knowledge Graph** (via MCP) for standards and progressions

### Repo Structure
```
assessment-agent/           # Python backend — deployed on Railway
  src/
    main.py                 # CLI entry point
    agent.py                # Core agent loop
    tools.py                # Tool definitions (the agent's actions)
    learner_model.py        # Running model of learner understanding
    domain_knowledge.py     # Fractions domain: standards, progressions, misconceptions
    task_library.py         # Mini-task definitions
    synthetic_learner.py    # Synthetic learner personas for testing
    evidence_report.py      # Report generation
    server.py               # FastAPI server with SSE streaming
    db.py                   # SQLite storage
    config.py               # API client setup, constants
    types.py                # Data classes
```

A separate Next.js repo for the dashboard (same pattern as Synthetic Learner Agent).

---

## The Domain: Fractions

### Standards Covered (CCSS-M)

The agent assesses across the full fractions progression, grades 2-5:

**Prerequisite (Grade 2)**
- `2.G.A.3` — Partition circles and rectangles into two, three, or four equal shares; describe shares using halves, thirds, etc.
- `2.MD.A.2` — Measure length using different units; describe how measurements relate to unit size

**Grade 3 — Number and Operations: Fractions**
- `3.NF.A.1` — Understand 1/b as one part when a whole is partitioned into b equal parts; understand a/b as a parts of size 1/b
  - LC: Identify 1/b as the quantity formed by 1 part when a whole is partitioned into equal parts (b = 2,3,4,6,8)
  - LC: Identify a/b as the quantity formed by a parts of size 1/b (b = 2,3,4,6,8)
- `3.NF.A.2` — Understand a fraction as a number on the number line; represent fractions on a number line diagram
- `3.NF.A.3` — Explain equivalence of fractions in special cases, and compare fractions by reasoning about their size
  - LC: Explain why fractions are equivalent
  - LC: Compare fractions by reasoning about their size (denominators 2,3,4,6,8)

**Grade 4 — Number and Operations: Fractions**
- `4.NF.A.1` — Explain why a/b = (n×a)/(n×b) using visual fraction models
  - LC: Recognize equivalent fractions using the principle a/b = (n×a)/(n×b)
  - LC: Explain equivalence using visual fraction models
  - LC: Generate equivalent fractions using the principle
- `4.NF.A.2` — Compare fractions with different numerators and denominators using common denominators, common numerators, or benchmark fractions
- `4.NF.B.3` — Understand a/b with a > 1 as a sum of fractions 1/b
  - `4.NF.B.3.a` — Understand addition/subtraction of fractions as joining/separating parts of the same whole
  - `4.NF.B.3.b` — Decompose a fraction into a sum of fractions with same denominator
  - `4.NF.B.3.c` — Add and subtract mixed numbers with like denominators

**Grade 5 — Number and Operations: Fractions**
- `5.NF.A.1` — Add and subtract fractions with unlike denominators using equivalent fractions
  - LC: Add fractions with different denominators by using equivalent fractions
  - LC: Subtract fractions with different denominators by using equivalent fractions
  - LC: Add mixed numbers with different denominators
  - LC: Subtract mixed numbers with different denominators
- `5.NF.B.4` — Multiply a fraction or whole number by a fraction
  - LC: Multiply a fraction or whole number by a fraction
- `5.NF.B.7` — Divide unit fractions by whole numbers and whole numbers by unit fractions

### Known Misconceptions (Research-Based)

The agent should be aware of and probe for these common fraction misconceptions:

**Foundational**
- "The bigger the denominator, the bigger the fraction" (e.g., 1/8 > 1/4 because 8 > 4)
- Treating numerator and denominator as separate whole numbers rather than a single value
- Not understanding that fractions represent equal parts (unequal partitioning seems fine)
- Thinking fractions only apply to circles/pizzas, not number lines or other representations

**Equivalence**
- "Different-looking fractions can't be equal" (2/4 ≠ 1/2 because they look different)
- Only recognizing equivalence in simplified form, not generating equivalent fractions
- Treating equivalent fractions as "the same fraction written differently" without understanding WHY they're equal

**Operations**
- Adding fractions by adding numerators AND denominators separately (1/2 + 1/3 = 2/5)
- "You need common denominators to multiply" (overgeneralizing from addition)
- "Multiplying always makes bigger" (doesn't hold for fractions less than 1)
- "Division always makes smaller" (doesn't hold for fractions less than 1)

**Conceptual**
- Fractions are always less than 1 (no understanding of improper fractions)
- A fraction is "two numbers" not "one number"
- Difficulty placing fractions on a number line (especially between 0 and 1)
- "You can't divide a smaller number by a bigger number"

### Learning Progression

The agent uses this progression to decide where to probe. If a learner shows weakness at one level, the agent goes backward to find where understanding breaks down. If they show strength, it moves forward.

```
Grade 2 prerequisites (partitioning, equal shares)
  ↓
Grade 3: What IS a fraction? (unit fractions → general fractions → number line → equivalence/comparison)
  ↓
Grade 4: Equivalence & operations with like denominators (equivalent fractions → comparing → adding/subtracting same denominator → mixed numbers)
  ↓
Grade 5: Operations with unlike denominators & multiplication/division (unlike denominators → multiplication → division)
```

---

## Agent Design

### The Agent Loop

```
1. START        → Greet learner, establish rapport, ask an entry-level question
2. OBSERVE      → Analyze the learner's response for evidence of understanding
3. UPDATE MODEL → Update the internal learner model (what they know, what's uncertain)
4. PLAN         → Decide what to assess next based on gaps in the model
5. ACT          → Ask a question OR pose a mini-task (tool call)
6. REPEAT 2-5   → Until sufficient evidence gathered or max turns reached
7. REPORT       → Produce the evidence map
```

### Agent System Prompt Requirements

The agent should:
- Be warm, encouraging, and curious — this is a conversation, not an interrogation
- Never tell the learner they're wrong directly — probe to understand their thinking
- Start with a mid-level question (grade 3-4) and adjust based on the response
- Go BACKWARD in the progression when it detects gaps (find where understanding breaks down)
- Go FORWARD when it detects strength (find where understanding tops out)
- Mix question types: conceptual understanding, procedural fluency, and transfer
- Use mini-tasks strategically — not every turn, but when a task would reveal something a question can't
- Keep responses concise and conversational (2-3 sentences + a question or task)
- Track which standards and learning components it has evidence for and which it still needs

### Tools

**`ask_question`**
The agent asks a conversational question to probe understanding.
- `question` (string): The question to ask
- `target_standard` (string): Which standard this is probing (e.g., "3.NF.A.1")
- `target_learning_component` (string, optional): Specific LC being assessed
- `depth` (enum): "recall", "conceptual", "application", "transfer"
- `intent` (string): Strategic reasoning — why this question now (logged, not shown to learner)

**`pose_task`**
The agent presents a structured mini-task.
- `task_type` (enum): "compare_fractions", "order_fractions", "find_equivalent", "place_on_number_line", "compute", "decompose", "word_problem"
- `task_content` (string): The specific task presented to the learner
- `target_standard` (string): Which standard this assesses
- `expected_answer` (string): What a correct response looks like
- `common_errors` (list[string]): Errors that would indicate specific misconceptions
- `intent` (string): Strategic reasoning

**`assess_response`**
After each learner response, the agent analyzes what it reveals.
- `response_reveals` (string): What this response tells us about the learner's understanding
- `evidence_for` (list[object]): Standards/LCs this provides POSITIVE evidence for, with confidence (low/medium/high)
- `evidence_against` (list[object]): Standards/LCs this provides NEGATIVE evidence for, with confidence
- `misconceptions_detected` (list[string]): Specific misconceptions surfaced
- `misconceptions_ruled_out` (list[string]): Misconceptions we can now eliminate
- `notes` (string): Agent's reasoning

**`update_learner_model`**
Updates the running model of the learner's knowledge state.
- `standards_status` (list[object]): For each standard assessed so far: status (demonstrated / partial / not_demonstrated / not_assessed), confidence (low/medium/high), evidence summary
- `progression_position` (string): Where the learner currently sits on the fractions progression
- `active_misconceptions` (list[string]): Misconceptions currently held (with confidence)
- `cleared_misconceptions` (list[string]): Misconceptions ruled out by evidence
- `overall_assessment` (string): Current holistic picture

**`adjust_strategy`**
Agent pivots its assessment approach.
- `current_picture` (string): What we know so far
- `gaps_in_evidence` (list[string]): What we still need to assess
- `next_move` (string): What to probe next and why
- `progression_direction` (enum): "probe_backward", "probe_forward", "probe_deeper", "probe_lateral"

**`conclude_assessment`**
Ends the assessment and produces the final report.
- `evidence_map` (list[object]): Per-standard evidence with: standard code, standard description, status, confidence, evidence (specific moments from conversation), learning components assessed
- `progression_summary` (string): Where the learner is on the fractions progression and what that means
- `misconception_report` (list[object]): Each misconception: description, status (confirmed/suspected/cleared), evidence
- `overall_narrative` (string): A teacher-readable summary of this learner's understanding
- `recommended_next_steps` (list[string]): What a teacher should focus on next with this learner
- `stop_reason` (string): "sufficient_evidence", "max_turns", "learner_disengaged"

### Mini-Task Library

Pre-defined task templates the agent can draw from. These are NOT the only tasks — the agent can also compose tasks on the fly — but these ensure common assessment patterns are available:

**Compare Fractions**
- "Which is bigger: 1/3 or 1/5? How do you know?"
- "Which is bigger: 3/4 or 2/3? Explain your thinking."
- "Which is closer to 1: 3/4 or 5/6?"

**Order Fractions**
- "Put these in order from smallest to biggest: 1/2, 1/4, 3/4"
- "Put these in order: 2/3, 3/5, 1/2"

**Find Equivalent**
- "Can you give me a fraction that equals 1/2 but looks different?"
- "Is 2/6 equal to 1/3? How could you prove it?"

**Place on Number Line**
- "If I drew a number line from 0 to 1, where would 3/4 go? What about 1/3?"
- "Where does 5/4 go on a number line? Is that even possible?"

**Compute**
- "What's 1/4 + 1/4?"
- "What's 1/2 + 1/3?"
- "What's 3 × 1/4?"
- "A recipe needs 2/3 cup of sugar. You want to make half the recipe. How much sugar?"

**Decompose**
- "Can you write 3/4 as a sum of smaller fractions?"
- "How many 1/6 pieces make 2/3?"

**Word Problems**
- "You ate 2/8 of a pizza. Your friend ate 1/4. Who ate more?"
- "You have 3/4 of a yard of ribbon. You use 1/3 of it. How much did you use?"

### Synthetic Learner Personas (for Testing Mode)

Three personas at different points on the progression:

**Mia — Grade 3 level, fragmented understanding**
- Gets unit fractions (1/2, 1/3, 1/4) but struggles with non-unit fractions
- Can partition shapes but can't connect that to number line
- Holds misconception: bigger denominator = bigger fraction
- Engagement: eager, asks "is that right?" a lot

**Derek — Grade 4 level, procedural but not conceptual**
- Can find equivalent fractions mechanically but can't explain WHY they're equal
- Can add fractions with like denominators
- Holds misconception: adds unlike fractions by adding numerators and denominators
- Engagement: confident, wants to get to the answer quickly

**Priya — Grade 5 level, strong with specific gaps**
- Solid on most fraction concepts through grade 4
- Can add/subtract unlike denominators
- Holds misconception: multiplication always makes bigger
- Struggles with division of fractions (no conceptual understanding, may have a memorized procedure)
- Engagement: thoughtful, asks "why" questions

---

## The Evidence Report

The final deliverable. This is what a teacher would see.

### Structure

```
EVIDENCE OF LEARNING REPORT
============================

Learner: [name or "Anonymous"]
Date: [timestamp]
Domain: Fractions (CCSS-M Grades 3-5)
Assessment Duration: [X turns]

PROGRESSION SUMMARY
Where this learner is on the fractions learning progression,
written in plain language a teacher can act on.

STANDARDS EVIDENCE MAP
For each standard assessed:
  - Standard code + description
  - Status: Demonstrated | Partial | Not Demonstrated | Not Assessed
  - Confidence: High | Medium | Low
  - Evidence: Specific moments from the conversation
  - Learning Components: Which sub-skills were assessed and their status

MISCONCEPTION REPORT
For each misconception probed:
  - Description
  - Status: Confirmed | Suspected | Cleared
  - Evidence: What the learner said/did that supports this

OVERALL NARRATIVE
A 2-3 paragraph teacher-readable summary.

RECOMMENDED NEXT STEPS
Specific, actionable recommendations for instruction.
```

---

## API Endpoints

### Assessment Endpoints

**`POST /assess`** — Start an assessment session
- Body: `{ mode: "real" | "synthetic", persona_name?: string }`
- Returns: SSE stream of assessment events
- Events: `session_started`, `agent_thinking`, `agent_question`, `agent_task`, `learner_response` (synthetic mode only), `observation`, `model_update`, `strategy_shift`, `assessment_complete`

**`POST /assess/{session_id}/respond`** — Submit a learner response (real learner mode)
- Body: `{ message: string }`
- Returns: SSE stream of the agent's next actions

**`GET /assessments`** — List past assessments
**`GET /assessments/{id}`** — Get a full assessment report
**`GET /personas`** — List available synthetic learner personas

### Domain Endpoints

**`GET /domain/standards`** — List all fractions standards with learning components
**`GET /domain/progressions`** — Get the fractions learning progression
**`GET /domain/misconceptions`** — List all known misconceptions

---

## Dashboard Pages

### `/` — Launch
- Choose mode: "Assess a Real Learner" or "Run with Synthetic Learner"
- If synthetic: pick a persona (Mia, Derek, or Priya)
- Brief explanation of what will happen
- "Start Assessment" button

### `/assess` — Live Assessment (Real Learner Mode)
- Chat interface — learner types responses
- Agent's questions and tasks appear as messages
- Behind the scenes (not shown to learner): agent's observations, model updates, strategy shifts
- "End Assessment" button available
- On completion: redirect to report

### `/assess/demo` — Live Assessment (Synthetic Learner Mode)
- Same as above but responses are generated automatically
- Agent thinking, observations, and strategy ARE visible (this is the demo view)
- Shows the learner model updating in real-time (sidebar or panel)

### `/report/{id}` — Evidence Report
- Full rendered report: progression summary, standards evidence map, misconception report, narrative, recommendations
- Conversation log available as expandable section
- Downloadable as PDF or Markdown

### `/assessments` — Past Assessments
- List of all past assessments with summary info
- Filter by mode (real/synthetic), persona, date

---

## Development Sequence

1. **Domain knowledge module** — Hardcode the fractions standards, progressions, misconceptions, and task library from the data in this PRD. Include the Knowledge Graph UUIDs so we can query dynamically later.
2. **Types and learner model** — Define all data structures, especially the learner model that tracks understanding across standards.
3. **Tools** — Define all 6 tools in Anthropic tool-use format.
4. **Agent loop** — The core: system prompt + tool orchestration + decision loop. Start with synthetic learner mode only.
5. **Synthetic learner personas** — Mia, Derek, Priya.
6. **CLI entry point** — Run an assessment from the terminal with rich output.
7. **Evidence report generation** — Structured output from the conclude_assessment tool.
8. **FastAPI server** — API with SSE streaming, session management for real learner mode.
9. **SQLite storage** — Save assessment results.
10. **Dashboard** — Next.js frontend (separate repo).

---

## Knowledge Graph Integration

The fractions domain data in this PRD was pulled from the Learning Commons Knowledge Graph. The UUIDs are included so the agent can query the KG dynamically in future versions.

### Standard UUIDs (for KG queries)
- `3.NF.A.1` → `6b9bf846-d7cc-11e8-824f-0242ac160002`
- `3.NF.A.2` → `6b9d400d-d7cc-11e8-824f-0242ac160002`
- `3.NF.A.3` → `6b9e210d-d7cc-11e8-824f-0242ac160002`
- `4.NF.A.1` → `6b9c09e2-d7cc-11e8-824f-0242ac160002`
- `4.NF.A.2` → `6b9d4e66-d7cc-11e8-824f-0242ac160002`
- `4.NF.B.3` → `6b9e2c7a-d7cc-11e8-824f-0242ac160002`
- `5.NF.A.1` → `6b9c1a30-d7cc-11e8-824f-0242ac160002`
- `5.NF.B.4` → `6b9edad5-d7cc-11e8-824f-0242ac160002`
- `5.NF.B.7` → `6ba053e8-d7cc-11e8-824f-0242ac160002`

### Learning Component UUIDs
- 3.NF.A.1 LC: Identify 1/b → `188fe970-4e1d-52c4-9f18-5e2fade05494`
- 3.NF.A.1 LC: Identify a/b → `0f80aa86-2c60-5a0f-bd85-7720345949d9`
- 3.NF.A.3 LC: Compare fractions → `2bfc7496-6e00-5c7d-9d81-1df05d4642c5`
- 3.NF.A.3 LC: Explain equivalence → `d20a384e-e8cc-5c06-acd5-9c829e5c9042`
- 4.NF.A.1 LC: Recognize equivalent → `5f61cb2a-1c2e-5a6f-9f57-47629badf7c0`
- 4.NF.A.1 LC: Explain with models → `74de8dae-331b-5d0a-8f64-a1e8c7c5c3be`
- 4.NF.A.1 LC: Generate equivalent → `c3b684c1-9c44-51cd-8a52-d7812ec62951`
- 5.NF.A.1 LC: Add unlike denominators → `d022d8d2-37f6-5ce9-bb02-e000d731aba0`
- 5.NF.A.1 LC: Subtract unlike denominators → `089c550e-f3a4-5ea2-959a-34e267c3e374`
- 5.NF.A.1 LC: Add mixed numbers → `d2565c2d-3930-54d3-864e-e532fd65cf6c`
- 5.NF.A.1 LC: Subtract mixed numbers → `3f8f80e7-a5c3-56e5-bf2d-90c5bb5f4f08`
- 5.NF.B.4 LC: Multiply fraction × fraction → `4aeee2dd-3e67-5d7e-b843-39650a018660`

### Prerequisite Standards (from backward progression)
- `2.G.A.3` → `6b9e11e8-d7cc-11e8-824f-0242ac160002` (partition shapes into equal shares)
- `2.MD.A.2` → `6b9d2bdf-d7cc-11e8-824f-0242ac160002` (measure with different units)

### Forward Progression from 3.NF.A.1
- → `3.NF.A.3` (equivalence and comparison)
- → `3.G.A.2` (partition shapes, express as unit fractions)
- → `4.NF.B.3.a` (addition/subtraction as joining/separating)
- → `4.NF.B.3.b` (decompose fractions)
- → `4.NF.B.3.c` (mixed numbers with like denominators)
- → `4.NF.B.4.a` (fraction as multiple of unit fraction)
- → `5.NF.B.7` (divide unit fractions and whole numbers)
