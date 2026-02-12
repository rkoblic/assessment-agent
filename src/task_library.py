"""Mini-task templates for the assessment agent.

Pre-defined task templates the agent can draw from. The agent can also
compose tasks on the fly, but these ensure common assessment patterns
are available.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TaskTemplate:
    id: str
    task_type: str  # compare_fractions, order_fractions, etc.
    content: str  # The task text presented to the learner
    target_standard: str
    expected_answer: str
    common_errors: list[str] = field(default_factory=list)
    difficulty: str = "mid"  # entry | mid | advanced


# ---------------------------------------------------------------------------
# Task Library
# ---------------------------------------------------------------------------

TASK_LIBRARY: list[TaskTemplate] = [
    # --- Compare Fractions ---
    TaskTemplate(
        id="compare_01",
        task_type="compare_fractions",
        content="Which is bigger: 1/3 or 1/5? How do you know?",
        target_standard="3.NF.A.3",
        expected_answer=(
            "1/3 is bigger because when you divide something into fewer "
            "pieces, each piece is larger."
        ),
        common_errors=[
            "1/5 because 5 > 3 (bigger denominator = bigger fraction)",
        ],
        difficulty="entry",
    ),
    TaskTemplate(
        id="compare_02",
        task_type="compare_fractions",
        content="Which is bigger: 3/4 or 2/3? Explain your thinking.",
        target_standard="4.NF.A.2",
        expected_answer=(
            "3/4 is bigger. You can compare by finding common denominators: "
            "9/12 vs 8/12, or by reasoning that 3/4 is 1/4 away from 1 "
            "while 2/3 is 1/3 away from 1."
        ),
        common_errors=[
            "2/3 because 'both are missing one piece'",
            "They're equal because both are 'missing one piece'",
        ],
        difficulty="mid",
    ),
    TaskTemplate(
        id="compare_03",
        task_type="compare_fractions",
        content="Which is closer to 1: 3/4 or 5/6?",
        target_standard="4.NF.A.2",
        expected_answer=(
            "5/6 is closer to 1. 3/4 is 1/4 away from 1 and 5/6 is 1/6 "
            "away from 1. Since 1/6 < 1/4, 5/6 is closer."
        ),
        common_errors=[
            "3/4 because '4 is smaller than 6'",
            "They're the same because both are 'one piece away'",
        ],
        difficulty="advanced",
    ),

    # --- Order Fractions ---
    TaskTemplate(
        id="order_01",
        task_type="order_fractions",
        content="Put these in order from smallest to biggest: 1/2, 1/4, 3/4",
        target_standard="3.NF.A.3",
        expected_answer="1/4, 1/2, 3/4",
        common_errors=[
            "1/4, 3/4, 1/2 (comparing denominators only)",
            "3/4, 1/2, 1/4 (reversed — biggest first)",
        ],
        difficulty="entry",
    ),
    TaskTemplate(
        id="order_02",
        task_type="order_fractions",
        content="Put these in order from smallest to biggest: 2/3, 3/5, 1/2",
        target_standard="4.NF.A.2",
        expected_answer=(
            "1/2, 3/5, 2/3. Using common denominator 30: 15/30, 18/30, 20/30. "
            "Or using benchmark reasoning."
        ),
        common_errors=[
            "1/2, 2/3, 3/5 (comparing numerators or denominators independently)",
        ],
        difficulty="mid",
    ),

    # --- Find Equivalent ---
    TaskTemplate(
        id="equiv_01",
        task_type="find_equivalent",
        content="Can you give me a fraction that equals 1/2 but looks different?",
        target_standard="3.NF.A.3",
        expected_answer="Any valid equivalent: 2/4, 3/6, 4/8, 5/10, etc.",
        common_errors=[
            "2/3 or 1/3 (guessing a nearby fraction)",
            "Can't think of one (doesn't understand equivalence)",
        ],
        difficulty="entry",
    ),
    TaskTemplate(
        id="equiv_02",
        task_type="find_equivalent",
        content="Is 2/6 equal to 1/3? How could you prove it?",
        target_standard="4.NF.A.1",
        expected_answer=(
            "Yes, 2/6 = 1/3. You can simplify 2/6 by dividing both by 2, "
            "or show that 1/3 × 2/2 = 2/6, or use a visual model."
        ),
        common_errors=[
            "No, because 2 ≠ 1 and 6 ≠ 3 (comparing parts independently)",
            "Yes, but can't explain why",
        ],
        difficulty="mid",
    ),

    # --- Place on Number Line ---
    TaskTemplate(
        id="numline_01",
        task_type="place_on_number_line",
        content=(
            "If I drew a number line from 0 to 1, where would 3/4 go? "
            "What about 1/3?"
        ),
        target_standard="3.NF.A.2",
        expected_answer=(
            "3/4 goes three-quarters of the way from 0 to 1. "
            "1/3 goes one-third of the way, closer to 0."
        ),
        common_errors=[
            "Places 1/3 past 1/2 (confusion about fraction size)",
            "Can't relate fractions to a number line at all",
            "Places them 'at' 3 and 4 or 1 and 3",
        ],
        difficulty="entry",
    ),
    TaskTemplate(
        id="numline_02",
        task_type="place_on_number_line",
        content="Where does 5/4 go on a number line? Is that even possible?",
        target_standard="3.NF.A.2",
        expected_answer=(
            "5/4 goes past 1, one quarter beyond 1. It's between 1 and 2. "
            "Yes, fractions can be greater than 1."
        ),
        common_errors=[
            "It's impossible — fractions have to be less than 1",
            "It goes between 0 and 1 somewhere",
            "It goes at 5 and 4",
        ],
        difficulty="mid",
    ),

    # --- Compute ---
    TaskTemplate(
        id="compute_01",
        task_type="compute",
        content="What's 1/4 + 1/4?",
        target_standard="4.NF.B.3",
        expected_answer="2/4 or 1/2",
        common_errors=[
            "2/8 (adding both numerator and denominator)",
        ],
        difficulty="entry",
    ),
    TaskTemplate(
        id="compute_02",
        task_type="compute",
        content="What's 1/2 + 1/3?",
        target_standard="5.NF.A.1",
        expected_answer="5/6 (common denominator: 3/6 + 2/6 = 5/6)",
        common_errors=[
            "2/5 (adding numerators and denominators separately)",
            "1/5 (other incorrect operation)",
        ],
        difficulty="mid",
    ),
    TaskTemplate(
        id="compute_03",
        task_type="compute",
        content="What's 3 × 1/4?",
        target_standard="5.NF.B.4",
        expected_answer="3/4",
        common_errors=[
            "3/12 (multiplying denominator too)",
            "1/12 (confusion about the operation)",
        ],
        difficulty="mid",
    ),
    TaskTemplate(
        id="compute_04",
        task_type="compute",
        content=(
            "A recipe needs 2/3 cup of sugar. You want to make half the "
            "recipe. How much sugar do you need?"
        ),
        target_standard="5.NF.B.4",
        expected_answer="1/3 cup (1/2 × 2/3 = 2/6 = 1/3)",
        common_errors=[
            "1/3 cup but can't explain why",
            "2/6 without simplifying",
            "1/6 (dividing numerator and denominator by 2 separately)",
        ],
        difficulty="advanced",
    ),

    # --- Decompose ---
    TaskTemplate(
        id="decompose_01",
        task_type="decompose",
        content="Can you write 3/4 as a sum of smaller fractions?",
        target_standard="4.NF.B.3",
        expected_answer="1/4 + 1/4 + 1/4, or 1/4 + 2/4, or 1/2 + 1/4",
        common_errors=[
            "Can't think of a way (doesn't see fractions as sums)",
            "1/3 + 1/4 + 1/4 (incorrect decomposition)",
        ],
        difficulty="mid",
    ),
    TaskTemplate(
        id="decompose_02",
        task_type="decompose",
        content="How many 1/6 pieces make 2/3?",
        target_standard="4.NF.B.3",
        expected_answer="4 pieces (because 2/3 = 4/6)",
        common_errors=[
            "2 pieces (just using the numerator of 2/3)",
            "6 pieces (just using the denominator)",
        ],
        difficulty="mid",
    ),

    # --- Word Problems ---
    TaskTemplate(
        id="word_01",
        task_type="word_problem",
        content=(
            "You ate 2/8 of a pizza. Your friend ate 1/4. Who ate more?"
        ),
        target_standard="3.NF.A.3",
        expected_answer=(
            "They ate the same amount! 2/8 = 1/4. Both ate one quarter "
            "of the pizza."
        ),
        common_errors=[
            "You ate more because 2 > 1 and 8 > 4",
            "Your friend ate more because 1/4 'sounds bigger'",
        ],
        difficulty="mid",
    ),
    TaskTemplate(
        id="word_02",
        task_type="word_problem",
        content=(
            "You have 3/4 of a yard of ribbon. You use 1/3 of a yard. "
            "How much ribbon do you have left?"
        ),
        target_standard="5.NF.A.1",
        expected_answer="5/12 of a yard (3/4 - 1/3 = 9/12 - 4/12 = 5/12)",
        common_errors=[
            "2/1 or 2 (subtracting numerators and denominators separately)",
            "Doesn't know how to subtract with unlike denominators",
        ],
        difficulty="advanced",
    ),
]


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def get_tasks_for_standard(standard_code: str) -> list[TaskTemplate]:
    return [t for t in TASK_LIBRARY if t.target_standard == standard_code]


def get_tasks_by_type(task_type: str) -> list[TaskTemplate]:
    return [t for t in TASK_LIBRARY if t.task_type == task_type]


def get_tasks_by_difficulty(difficulty: str) -> list[TaskTemplate]:
    return [t for t in TASK_LIBRARY if t.difficulty == difficulty]
