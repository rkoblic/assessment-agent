"""Fractions domain knowledge: CCSS-M standards, learning components,
misconceptions, and learning progression (Grades 2-5).

All data hardcoded from the Assessment Agent PRD. UUIDs from the
Learning Commons Knowledge Graph are included for future dynamic queries.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class LearningComponent:
    id: str  # Knowledge Graph UUID
    code: str  # e.g. "3.NF.A.1.a"
    description: str
    standard_code: str  # parent standard


@dataclass
class Standard:
    id: str  # Knowledge Graph UUID
    code: str  # e.g. "3.NF.A.1"
    grade: int
    description: str
    learning_components: list[LearningComponent] = field(default_factory=list)


@dataclass
class Misconception:
    id: str  # internal ID
    category: str  # foundational | equivalence | operations | conceptual
    description: str
    example: str
    related_standards: list[str] = field(default_factory=list)


@dataclass
class ProgressionLevel:
    grade: int
    label: str
    standards: list[str]
    prerequisites: list[str]
    next_levels: list[str]


# ---------------------------------------------------------------------------
# Standards (CCSS-M Fractions, Grades 2-5)
# ---------------------------------------------------------------------------

STANDARDS: dict[str, Standard] = {
    # --- Grade 2 Prerequisites ---
    "2.G.A.3": Standard(
        id="6b9e11e8-d7cc-11e8-824f-0242ac160002",
        code="2.G.A.3",
        grade=2,
        description=(
            "Partition circles and rectangles into two, three, or four equal "
            "shares; describe the shares using the words halves, thirds, half "
            "of, a third of, etc.; describe the whole as two halves, three "
            "thirds, four fourths. Recognize that equal shares of identical "
            "wholes need not have the same shape."
        ),
    ),
    "2.MD.A.2": Standard(
        id="6b9d2bdf-d7cc-11e8-824f-0242ac160002",
        code="2.MD.A.2",
        grade=2,
        description=(
            "Measure the length of an object twice, using length units of "
            "different lengths for the two measurements; describe how the two "
            "measurements relate to the size of the unit chosen."
        ),
    ),

    # --- Grade 3: Number and Operations — Fractions ---
    "3.NF.A.1": Standard(
        id="6b9bf846-d7cc-11e8-824f-0242ac160002",
        code="3.NF.A.1",
        grade=3,
        description=(
            "Understand a fraction 1/b as the quantity formed by 1 part when "
            "a whole is partitioned into b equal parts; understand a fraction "
            "a/b as the quantity formed by a parts of size 1/b."
        ),
        learning_components=[
            LearningComponent(
                id="188fe970-4e1d-52c4-9f18-5e2fade05494",
                code="3.NF.A.1.a",
                description=(
                    "Identify 1/b as the quantity formed by 1 part when a "
                    "whole is partitioned into equal parts (b = 2,3,4,6,8)"
                ),
                standard_code="3.NF.A.1",
            ),
            LearningComponent(
                id="0f80aa86-2c60-5a0f-bd85-7720345949d9",
                code="3.NF.A.1.b",
                description=(
                    "Identify a/b as the quantity formed by a parts of size "
                    "1/b (b = 2,3,4,6,8)"
                ),
                standard_code="3.NF.A.1",
            ),
        ],
    ),
    "3.NF.A.2": Standard(
        id="6b9d400d-d7cc-11e8-824f-0242ac160002",
        code="3.NF.A.2",
        grade=3,
        description=(
            "Understand a fraction as a number on the number line; represent "
            "fractions on a number line diagram."
        ),
    ),
    "3.NF.A.3": Standard(
        id="6b9e210d-d7cc-11e8-824f-0242ac160002",
        code="3.NF.A.3",
        grade=3,
        description=(
            "Explain equivalence of fractions in special cases, and compare "
            "fractions by reasoning about their size."
        ),
        learning_components=[
            LearningComponent(
                id="d20a384e-e8cc-5c06-acd5-9c829e5c9042",
                code="3.NF.A.3.a",
                description="Explain why fractions are equivalent",
                standard_code="3.NF.A.3",
            ),
            LearningComponent(
                id="2bfc7496-6e00-5c7d-9d81-1df05d4642c5",
                code="3.NF.A.3.b",
                description=(
                    "Compare fractions by reasoning about their size "
                    "(denominators 2,3,4,6,8)"
                ),
                standard_code="3.NF.A.3",
            ),
        ],
    ),

    # --- Grade 4: Number and Operations — Fractions ---
    "4.NF.A.1": Standard(
        id="6b9c09e2-d7cc-11e8-824f-0242ac160002",
        code="4.NF.A.1",
        grade=4,
        description=(
            "Explain why a fraction a/b is equivalent to a fraction "
            "(n×a)/(n×b) by using visual fraction models, with attention to "
            "how the number and size of the parts differ even though the two "
            "fractions themselves are the same size."
        ),
        learning_components=[
            LearningComponent(
                id="5f61cb2a-1c2e-5a6f-9f57-47629badf7c0",
                code="4.NF.A.1.a",
                description=(
                    "Recognize equivalent fractions using the principle "
                    "a/b = (n×a)/(n×b)"
                ),
                standard_code="4.NF.A.1",
            ),
            LearningComponent(
                id="74de8dae-331b-5d0a-8f64-a1e8c7c5c3be",
                code="4.NF.A.1.b",
                description="Explain equivalence using visual fraction models",
                standard_code="4.NF.A.1",
            ),
            LearningComponent(
                id="c3b684c1-9c44-51cd-8a52-d7812ec62951",
                code="4.NF.A.1.c",
                description="Generate equivalent fractions using the principle",
                standard_code="4.NF.A.1",
            ),
        ],
    ),
    "4.NF.A.2": Standard(
        id="6b9d4e66-d7cc-11e8-824f-0242ac160002",
        code="4.NF.A.2",
        grade=4,
        description=(
            "Compare two fractions with different numerators and different "
            "denominators, e.g., by creating common denominators or numerators, "
            "or by comparing to a benchmark fraction such as 1/2."
        ),
    ),
    "4.NF.B.3": Standard(
        id="6b9e2c7a-d7cc-11e8-824f-0242ac160002",
        code="4.NF.B.3",
        grade=4,
        description=(
            "Understand a fraction a/b with a > 1 as a sum of fractions 1/b. "
            "a. Understand addition and subtraction of fractions as joining "
            "and separating parts referring to the same whole. "
            "b. Decompose a fraction into a sum of fractions with the same "
            "denominator in more than one way. "
            "c. Add and subtract mixed numbers with like denominators."
        ),
    ),

    # --- Grade 5: Number and Operations — Fractions ---
    "5.NF.A.1": Standard(
        id="6b9c1a30-d7cc-11e8-824f-0242ac160002",
        code="5.NF.A.1",
        grade=5,
        description=(
            "Add and subtract fractions with unlike denominators (including "
            "mixed numbers) by replacing given fractions with equivalent "
            "fractions in such a way as to produce an equivalent sum or "
            "difference of fractions with like denominators."
        ),
        learning_components=[
            LearningComponent(
                id="d022d8d2-37f6-5ce9-bb02-e000d731aba0",
                code="5.NF.A.1.a",
                description=(
                    "Add fractions with different denominators by using "
                    "equivalent fractions"
                ),
                standard_code="5.NF.A.1",
            ),
            LearningComponent(
                id="089c550e-f3a4-5ea2-959a-34e267c3e374",
                code="5.NF.A.1.b",
                description=(
                    "Subtract fractions with different denominators by using "
                    "equivalent fractions"
                ),
                standard_code="5.NF.A.1",
            ),
            LearningComponent(
                id="d2565c2d-3930-54d3-864e-e532fd65cf6c",
                code="5.NF.A.1.c",
                description="Add mixed numbers with different denominators",
                standard_code="5.NF.A.1",
            ),
            LearningComponent(
                id="3f8f80e7-a5c3-56e5-bf2d-90c5bb5f4f08",
                code="5.NF.A.1.d",
                description="Subtract mixed numbers with different denominators",
                standard_code="5.NF.A.1",
            ),
        ],
    ),
    "5.NF.B.4": Standard(
        id="6b9edad5-d7cc-11e8-824f-0242ac160002",
        code="5.NF.B.4",
        grade=5,
        description="Apply and extend previous understandings of multiplication to multiply a fraction or whole number by a fraction.",
        learning_components=[
            LearningComponent(
                id="4aeee2dd-3e67-5d7e-b843-39650a018660",
                code="5.NF.B.4.a",
                description="Multiply a fraction or whole number by a fraction",
                standard_code="5.NF.B.4",
            ),
        ],
    ),
    "5.NF.B.7": Standard(
        id="6ba053e8-d7cc-11e8-824f-0242ac160002",
        code="5.NF.B.7",
        grade=5,
        description=(
            "Apply and extend previous understandings of division to divide "
            "unit fractions by whole numbers and whole numbers by unit fractions."
        ),
    ),
}


# ---------------------------------------------------------------------------
# Misconceptions
# ---------------------------------------------------------------------------

MISCONCEPTIONS: list[Misconception] = [
    # — Foundational —
    Misconception(
        id="foundational_bigger_denom",
        category="foundational",
        description="The bigger the denominator, the bigger the fraction",
        example="e.g., thinks 1/8 > 1/4 because 8 > 4",
        related_standards=["3.NF.A.1", "3.NF.A.3"],
    ),
    Misconception(
        id="foundational_separate_numbers",
        category="foundational",
        description=(
            "Treating numerator and denominator as separate whole numbers "
            "rather than a single value"
        ),
        example="e.g., sees 3/4 as 'a 3 and a 4' rather than one number",
        related_standards=["3.NF.A.1", "3.NF.A.2"],
    ),
    Misconception(
        id="foundational_unequal_parts",
        category="foundational",
        description=(
            "Not understanding that fractions represent equal parts "
            "(unequal partitioning seems fine)"
        ),
        example="e.g., accepts a circle split into unequal pieces as thirds",
        related_standards=["2.G.A.3", "3.NF.A.1"],
    ),
    Misconception(
        id="foundational_only_circles",
        category="foundational",
        description=(
            "Thinking fractions only apply to circles/pizzas, not number "
            "lines or other representations"
        ),
        example="e.g., can't place 3/4 on a number line even though they 'know' 3/4 of a pizza",
        related_standards=["3.NF.A.1", "3.NF.A.2"],
    ),

    # — Equivalence —
    Misconception(
        id="equivalence_different_looking",
        category="equivalence",
        description="Different-looking fractions can't be equal",
        example="e.g., insists 2/4 ≠ 1/2 because they look different",
        related_standards=["3.NF.A.3", "4.NF.A.1"],
    ),
    Misconception(
        id="equivalence_only_simplified",
        category="equivalence",
        description=(
            "Only recognizes equivalence in simplified form, not generating "
            "equivalent fractions"
        ),
        example="e.g., knows 1/2 is simplest but can't produce 3/6 as equivalent",
        related_standards=["4.NF.A.1"],
    ),
    Misconception(
        id="equivalence_no_why",
        category="equivalence",
        description=(
            "Treats equivalent fractions as 'the same fraction written "
            "differently' without understanding WHY they're equal"
        ),
        example="e.g., can multiply top and bottom by same number but can't explain with a model",
        related_standards=["4.NF.A.1"],
    ),

    # — Operations —
    Misconception(
        id="operations_add_both",
        category="operations",
        description=(
            "Adding fractions by adding numerators AND denominators separately"
        ),
        example="e.g., 1/2 + 1/3 = 2/5",
        related_standards=["4.NF.B.3", "5.NF.A.1"],
    ),
    Misconception(
        id="operations_common_denom_multiply",
        category="operations",
        description=(
            "You need common denominators to multiply "
            "(overgeneralizing from addition)"
        ),
        example="e.g., tries to find common denominator before multiplying 1/2 × 1/3",
        related_standards=["5.NF.B.4"],
    ),
    Misconception(
        id="operations_multiply_bigger",
        category="operations",
        description="Multiplying always makes bigger",
        example="e.g., expects 1/2 × 1/3 > 1/3 because 'multiplying makes things bigger'",
        related_standards=["5.NF.B.4"],
    ),
    Misconception(
        id="operations_division_smaller",
        category="operations",
        description="Division always makes smaller",
        example="e.g., expects 3 ÷ 1/2 < 3 because 'dividing makes things smaller'",
        related_standards=["5.NF.B.7"],
    ),

    # — Conceptual —
    Misconception(
        id="conceptual_always_less_than_1",
        category="conceptual",
        description="Fractions are always less than 1",
        example="e.g., says 5/4 'isn't a real fraction' or 'doesn't make sense'",
        related_standards=["4.NF.B.3", "3.NF.A.2"],
    ),
    Misconception(
        id="conceptual_two_numbers",
        category="conceptual",
        description="A fraction is 'two numbers' not 'one number'",
        example="e.g., can't place a fraction on a number line as a single point",
        related_standards=["3.NF.A.1", "3.NF.A.2"],
    ),
    Misconception(
        id="conceptual_number_line",
        category="conceptual",
        description="Difficulty placing fractions on a number line (especially between 0 and 1)",
        example="e.g., places 1/3 closer to 1 than 1/2 on the number line",
        related_standards=["3.NF.A.2", "3.NF.A.3"],
    ),
    Misconception(
        id="conceptual_cant_divide_smaller",
        category="conceptual",
        description="You can't divide a smaller number by a bigger number",
        example="e.g., says '1 ÷ 4 is impossible' or 'you can't do that'",
        related_standards=["3.NF.A.1", "5.NF.B.7"],
    ),
]


# ---------------------------------------------------------------------------
# Learning Progression
# ---------------------------------------------------------------------------

PROGRESSION: list[ProgressionLevel] = [
    ProgressionLevel(
        grade=2,
        label="Prerequisite: Partitioning & equal shares",
        standards=["2.G.A.3", "2.MD.A.2"],
        prerequisites=[],
        next_levels=["3.NF.A.1", "3.NF.A.2", "3.NF.A.3"],
    ),
    ProgressionLevel(
        grade=3,
        label="What IS a fraction? (unit fractions → general → number line → equivalence/comparison)",
        standards=["3.NF.A.1", "3.NF.A.2", "3.NF.A.3"],
        prerequisites=["2.G.A.3", "2.MD.A.2"],
        next_levels=["4.NF.A.1", "4.NF.A.2", "4.NF.B.3"],
    ),
    ProgressionLevel(
        grade=4,
        label="Equivalence & operations with like denominators",
        standards=["4.NF.A.1", "4.NF.A.2", "4.NF.B.3"],
        prerequisites=["3.NF.A.1", "3.NF.A.2", "3.NF.A.3"],
        next_levels=["5.NF.A.1", "5.NF.B.4", "5.NF.B.7"],
    ),
    ProgressionLevel(
        grade=5,
        label="Operations with unlike denominators & multiplication/division",
        standards=["5.NF.A.1", "5.NF.B.4", "5.NF.B.7"],
        prerequisites=["4.NF.A.1", "4.NF.A.2", "4.NF.B.3"],
        next_levels=[],
    ),
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_standard(code: str) -> Standard | None:
    return STANDARDS.get(code)


def get_misconceptions_for_standard(code: str) -> list[Misconception]:
    return [m for m in MISCONCEPTIONS if code in m.related_standards]


def get_progression_level(grade: int) -> ProgressionLevel | None:
    for level in PROGRESSION:
        if level.grade == grade:
            return level
    return None


def get_prerequisites(standard_code: str) -> list[str]:
    """Return standard codes that are prerequisites for the given standard."""
    for level in PROGRESSION:
        if standard_code in level.standards:
            return level.prerequisites
    return []


def get_next_standards(standard_code: str) -> list[str]:
    """Return standard codes in the next progression level."""
    for level in PROGRESSION:
        if standard_code in level.standards:
            return level.next_levels
    return []


def get_all_standards_summary() -> str:
    """Formatted summary of all standards for inclusion in the system prompt."""
    lines: list[str] = []
    current_grade = 0
    for code in sorted(STANDARDS, key=lambda c: (STANDARDS[c].grade, c)):
        std = STANDARDS[code]
        if std.grade != current_grade:
            current_grade = std.grade
            lines.append(f"\n**Grade {current_grade}**")
        lines.append(f"- `{std.code}`: {std.description}")
        for lc in std.learning_components:
            lines.append(f"  - LC `{lc.code}`: {lc.description}")
    return "\n".join(lines)


def get_all_misconceptions_summary() -> str:
    """Formatted summary of all misconceptions for the system prompt."""
    lines: list[str] = []
    current_category = ""
    for m in MISCONCEPTIONS:
        if m.category != current_category:
            current_category = m.category
            lines.append(f"\n**{current_category.title()}**")
        lines.append(f"- {m.description} ({m.example}) [standards: {', '.join(m.related_standards)}]")
    return "\n".join(lines)


def get_progression_summary() -> str:
    """Formatted summary of the learning progression for the system prompt."""
    lines: list[str] = []
    for level in PROGRESSION:
        standards_str = ", ".join(level.standards)
        lines.append(f"Grade {level.grade}: {level.label}")
        lines.append(f"  Standards: {standards_str}")
        if level.prerequisites:
            lines.append(f"  Prerequisites: {', '.join(level.prerequisites)}")
        if level.next_levels:
            lines.append(f"  Leads to: {', '.join(level.next_levels)}")
        lines.append("")
    return "\n".join(lines)
