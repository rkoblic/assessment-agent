"""Pre-recorded demo assessment for showcasing the system without API calls."""

from __future__ import annotations

DEMO_ASSESSMENT: dict = {
    "session_id": "demo-session-001",
    "persona": {"name": "Mia", "grade_level": 4},
    "events": [
        {
            "event": "session_started",
            "data": {"session_id": "demo-session-001"},
        },
        {
            "event": "agent_question",
            "data": {
                "question": (
                    "Hi there! I'm excited to chat with you about fractions today. "
                    "Let's start with something fun -- if you had a pizza and you "
                    "cut it into 4 equal pieces, and you ate 1 piece, what fraction "
                    "of the pizza did you eat?"
                ),
                "target_standard": "3.NF.A.1",
                "depth": "recall",
            },
        },
        {
            "event": "learner_response",
            "data": {"response": "That's 1/4 of the pizza!"},
        },
        {
            "event": "observation",
            "data": {
                "response_reveals": (
                    "Learner correctly identifies 1/4 as the fraction representing "
                    "1 out of 4 equal parts. Shows basic understanding of fraction "
                    "notation and part-whole relationships."
                ),
                "evidence_for": [
                    {"standard_code": "3.NF.A.1", "confidence": "medium"}
                ],
                "evidence_against": [],
                "misconceptions_detected": [],
                "misconceptions_ruled_out": [],
            },
        },
        {
            "event": "model_update",
            "data": {
                "summary": "Learner model updated. Position: Grade 3 foundational. Basic part-whole understanding confirmed.",
                "progression_position": "Grade 3 foundational",
                "standards_assessed": 1,
            },
        },
        {
            "event": "strategy_shift",
            "data": {
                "current_picture": "Learner shows basic fraction recognition.",
                "gaps_in_evidence": ["equivalent fractions", "fraction comparison", "number line placement"],
                "next_move": "Probe fraction comparison to see if learner understands relative size.",
                "progression_direction": "probe_forward",
            },
        },
        {
            "event": "agent_question",
            "data": {
                "question": (
                    "Nice job! Now here's a question that takes a little more "
                    "thinking: which fraction is bigger, 1/3 or 1/4? How do you know?"
                ),
                "target_standard": "3.NF.A.3",
                "depth": "conceptual",
            },
        },
        {
            "event": "learner_response",
            "data": {
                "response": (
                    "Hmm, I think 1/4 is bigger because 4 is bigger than 3."
                ),
            },
        },
        {
            "event": "observation",
            "data": {
                "response_reveals": (
                    "Learner exhibits the classic 'larger denominator means larger "
                    "fraction' misconception. They are comparing denominators as "
                    "whole numbers rather than understanding that larger denominators "
                    "mean smaller pieces."
                ),
                "evidence_for": [],
                "evidence_against": [
                    {"standard_code": "3.NF.A.3", "confidence": "high"}
                ],
                "misconceptions_detected": ["larger_denominator_larger_fraction"],
                "misconceptions_ruled_out": [],
            },
        },
        {
            "event": "model_update",
            "data": {
                "summary": "Learner model updated. Position: Grade 3 foundational with misconception. Holds larger-denominator misconception.",
                "progression_position": "Grade 3 foundational with misconception",
                "standards_assessed": 2,
            },
        },
        {
            "event": "strategy_shift",
            "data": {
                "current_picture": "Learner knows basic notation but has denominator misconception.",
                "gaps_in_evidence": ["equivalent fractions", "number line", "fraction addition"],
                "next_move": "Probe deeper on fraction comparison using a visual/contextual approach to understand the depth of the misconception.",
                "progression_direction": "probe_deeper",
            },
        },
        {
            "event": "agent_question",
            "data": {
                "question": (
                    "That's an interesting thought! Let me ask you this -- imagine "
                    "you have two identical chocolate bars. You share one bar equally "
                    "among 3 friends, and the other bar equally among 4 friends. "
                    "Which group of friends gets bigger pieces?"
                ),
                "target_standard": "3.NF.A.3",
                "depth": "application",
            },
        },
        {
            "event": "learner_response",
            "data": {
                "response": (
                    "Oh wait... the 3 friends would get bigger pieces because "
                    "the chocolate bar is split into less pieces! So 1/3 is "
                    "actually bigger than 1/4?"
                ),
            },
        },
        {
            "event": "observation",
            "data": {
                "response_reveals": (
                    "When given a concrete context, the learner self-corrects their "
                    "misconception. They now reason that fewer parts means each part "
                    "is larger. This suggests the misconception is not deeply rooted "
                    "and may be resolvable with contextual reasoning support."
                ),
                "evidence_for": [
                    {"standard_code": "3.NF.A.3", "confidence": "medium"}
                ],
                "evidence_against": [],
                "misconceptions_detected": [],
                "misconceptions_ruled_out": [],
            },
        },
        {
            "event": "model_update",
            "data": {
                "summary": "Learner model updated. Position: Grade 3 developing. Self-corrected with scaffolding.",
                "progression_position": "Grade 3 developing",
                "standards_assessed": 2,
            },
        },
        {
            "event": "strategy_shift",
            "data": {
                "current_picture": "Learner can reason about fraction size with concrete support but defaults to whole-number thinking abstractly.",
                "gaps_in_evidence": ["equivalent fractions", "number line", "fractions beyond unit fractions"],
                "next_move": "Probe equivalent fractions to assess Grade 3-4 boundary.",
                "progression_direction": "probe_forward",
            },
        },
        {
            "event": "agent_question",
            "data": {
                "question": (
                    "You're doing great thinking! Here's another one: can you "
                    "tell me a fraction that is the same amount as 1/2? "
                    "There might be more than one answer!"
                ),
                "target_standard": "3.NF.A.3",
                "depth": "conceptual",
            },
        },
        {
            "event": "learner_response",
            "data": {"response": "2/4 is the same as 1/2! And maybe 3/6?"},
        },
        {
            "event": "observation",
            "data": {
                "response_reveals": (
                    "Learner correctly identifies 2/4 and 3/6 as equivalent to 1/2. "
                    "Shows understanding of equivalent fractions, at least for "
                    "familiar benchmarks. This is a strong indicator for 3.NF.A.3."
                ),
                "evidence_for": [
                    {"standard_code": "3.NF.A.3", "confidence": "high"}
                ],
                "evidence_against": [],
                "misconceptions_detected": [],
                "misconceptions_ruled_out": ["no_concept_of_equivalence"],
            },
        },
        {
            "event": "model_update",
            "data": {
                "summary": "Learner model updated. Position: Grade 3 solid / Grade 4 emerging. Equivalent fractions understood for benchmarks.",
                "progression_position": "Grade 3 solid / Grade 4 emerging",
                "standards_assessed": 3,
            },
        },
        {
            "event": "strategy_shift",
            "data": {
                "current_picture": "Solid Grade 3 foundation with developing equivalence. Denominator misconception resolves with context.",
                "gaps_in_evidence": ["number line placement", "fraction addition", "mixed numbers"],
                "next_move": "Test number line understanding to assess Grade 3 standard 3.NF.A.2.",
                "progression_direction": "probe_lateral",
            },
        },
        {
            "event": "agent_task",
            "data": {
                "task_type": "place_on_number_line",
                "task_content": (
                    "Imagine a number line that goes from 0 to 1. If you had to "
                    "place the fraction 3/4 on that number line, where would it go? "
                    "Can you describe the spot?"
                ),
                "target_standard": "3.NF.A.2",
            },
        },
        {
            "event": "learner_response",
            "data": {
                "response": (
                    "It would go... between 1/2 and 1, closer to 1. Like if "
                    "you split the line into 4 parts, it would be at the third mark."
                ),
            },
        },
        {
            "event": "observation",
            "data": {
                "response_reveals": (
                    "Excellent understanding of number line placement. Learner "
                    "correctly identifies that 3/4 is between 1/2 and 1, closer "
                    "to 1, and connects it to partitioning the line into 4 equal "
                    "parts. Shows strong 3.NF.A.2 understanding."
                ),
                "evidence_for": [
                    {"standard_code": "3.NF.A.2", "confidence": "high"}
                ],
                "evidence_against": [],
                "misconceptions_detected": [],
                "misconceptions_ruled_out": ["fractions_not_numbers"],
            },
        },
        {
            "event": "model_update",
            "data": {
                "summary": "Learner model updated. Position: Solid Grade 3 / Grade 4 emerging. Strong number line and equivalence understanding.",
                "progression_position": "Solid Grade 3 / Grade 4 emerging",
                "standards_assessed": 4,
            },
        },
        {
            "event": "strategy_shift",
            "data": {
                "current_picture": "Strong Grade 3 foundation. Ready to probe Grade 4 skills.",
                "gaps_in_evidence": ["fraction addition", "mixed numbers", "decimal connection"],
                "next_move": "Probe fraction addition to test Grade 4 boundary.",
                "progression_direction": "probe_forward",
            },
        },
        {
            "event": "agent_question",
            "data": {
                "question": (
                    "You're really good at this! Let's try something a little "
                    "different. What do you get if you add 1/4 + 2/4?"
                ),
                "target_standard": "4.NF.B.3",
                "depth": "recall",
            },
        },
        {
            "event": "learner_response",
            "data": {"response": "3/4! Because 1 plus 2 is 3, and the bottom number stays the same."},
        },
        {
            "event": "observation",
            "data": {
                "response_reveals": (
                    "Learner correctly adds fractions with like denominators and "
                    "articulates the rule (add numerators, keep denominator). "
                    "Shows procedural fluency for same-denominator addition."
                ),
                "evidence_for": [
                    {"standard_code": "4.NF.B.3", "confidence": "medium"}
                ],
                "evidence_against": [],
                "misconceptions_detected": [],
                "misconceptions_ruled_out": ["add_both_num_and_denom"],
            },
        },
        {
            "event": "model_update",
            "data": {
                "summary": "Learner model updated. Position: Grade 4 emerging. Like-denominator addition understood.",
                "progression_position": "Grade 4 emerging",
                "standards_assessed": 5,
            },
        },
        {
            "event": "strategy_shift",
            "data": {
                "current_picture": "Solid through Grade 3. Grade 4 addition with like denominators works. Need to probe unlike denominators and mixed numbers.",
                "gaps_in_evidence": ["unlike denominator addition", "mixed numbers", "decimal fractions"],
                "next_move": "Probe unlike denominator addition to see Grade 4 ceiling.",
                "progression_direction": "probe_forward",
            },
        },
        {
            "event": "agent_question",
            "data": {
                "question": (
                    "Great job! Now here's a trickier one: what about 1/2 + 1/3? "
                    "Take your time with this one."
                ),
                "target_standard": "5.NF.A.1",
                "depth": "application",
            },
        },
        {
            "event": "learner_response",
            "data": {
                "response": "Hmm... is it 2/5? Because 1+1 is 2 and 2+3 is 5?",
            },
        },
        {
            "event": "observation",
            "data": {
                "response_reveals": (
                    "Learner adds both numerators and denominators separately, "
                    "which is the classic 'add across' misconception for unlike "
                    "denominators. They have not yet learned or internalized the "
                    "need for common denominators. This places their ceiling at "
                    "early Grade 4."
                ),
                "evidence_for": [],
                "evidence_against": [
                    {"standard_code": "5.NF.A.1", "confidence": "high"}
                ],
                "misconceptions_detected": ["add_numerators_and_denominators"],
                "misconceptions_ruled_out": [],
            },
        },
        {
            "event": "model_update",
            "data": {
                "summary": "Learner model updated. Position: Grade 4 emerging, ceiling identified. Cannot add unlike denominators.",
                "progression_position": "Grade 4 emerging, ceiling identified",
                "standards_assessed": 6,
            },
        },
        {
            "event": "strategy_shift",
            "data": {
                "current_picture": "Clear picture forming: solid Grade 3, emerging Grade 4 (like-denom addition), ceiling at unlike denominators (Grade 5).",
                "gaps_in_evidence": ["mixed numbers", "decimal fractions"],
                "next_move": "One more probe on mixed numbers, then conclude.",
                "progression_direction": "probe_lateral",
            },
        },
        {
            "event": "agent_question",
            "data": {
                "question": (
                    "No worries at all -- that's a tough one! Last question: "
                    "do you know what 5/4 means? Can you describe it in your own words?"
                ),
                "target_standard": "4.NF.B.3",
                "depth": "conceptual",
            },
        },
        {
            "event": "learner_response",
            "data": {
                "response": (
                    "5/4... that's more than 1 whole, right? Like 1 whole "
                    "pizza and 1/4 of another pizza. So it's 1 and 1/4!"
                ),
            },
        },
        {
            "event": "observation",
            "data": {
                "response_reveals": (
                    "Learner correctly interprets an improper fraction as a "
                    "mixed number and uses a concrete context to explain. "
                    "Strong evidence for understanding fractions greater than 1 "
                    "and mixed number conversion."
                ),
                "evidence_for": [
                    {"standard_code": "4.NF.B.3", "confidence": "high"}
                ],
                "evidence_against": [],
                "misconceptions_detected": [],
                "misconceptions_ruled_out": ["fractions_always_less_than_one"],
            },
        },
        {
            "event": "model_update",
            "data": {
                "summary": "Learner model updated. Position: Solid Grade 4 emerging. Mixed number understanding confirmed.",
                "progression_position": "Solid Grade 4 emerging",
                "standards_assessed": 7,
            },
        },
        {
            "event": "assessment_complete",
            "data": {
                "session_id": "demo-session-001",
                "report": {
                    "evidence_map": [
                        {
                            "standard_code": "3.NF.A.1",
                            "standard_description": "Understand a fraction 1/b as the quantity formed by 1 part when a whole is partitioned into b equal parts",
                            "status": "demonstrated",
                            "confidence": "high",
                            "evidence": [
                                "Correctly identified 1/4 of a pizza",
                                "Used part-whole language naturally",
                            ],
                        },
                        {
                            "standard_code": "3.NF.A.2",
                            "standard_description": "Understand a fraction as a number on the number line",
                            "status": "demonstrated",
                            "confidence": "high",
                            "evidence": [
                                "Correctly placed 3/4 on number line between 1/2 and 1",
                                "Connected placement to partitioning the line into equal parts",
                            ],
                        },
                        {
                            "standard_code": "3.NF.A.3",
                            "standard_description": "Explain equivalence of fractions and compare fractions by reasoning about their size",
                            "status": "partial",
                            "confidence": "high",
                            "evidence": [
                                "Correctly generated equivalent fractions for 1/2 (2/4, 3/6)",
                                "Initially showed larger-denominator misconception but self-corrected with context",
                            ],
                        },
                        {
                            "standard_code": "4.NF.B.3",
                            "standard_description": "Understand a fraction a/b with a > 1 as a sum of fractions 1/b",
                            "status": "demonstrated",
                            "confidence": "high",
                            "evidence": [
                                "Correctly added 1/4 + 2/4 = 3/4 with clear reasoning",
                                "Interpreted 5/4 as 1 and 1/4 using concrete context",
                            ],
                        },
                        {
                            "standard_code": "5.NF.A.1",
                            "standard_description": "Add and subtract fractions with unlike denominators",
                            "status": "not_demonstrated",
                            "confidence": "high",
                            "evidence": [
                                "Added 1/2 + 1/3 as 2/5 (added both numerators and denominators)",
                                "Has not learned common denominator strategy",
                            ],
                        },
                    ],
                    "progression_summary": (
                        "Mia is solidly in the Grade 3-4 range. She has a strong "
                        "foundation in fraction concepts (part-whole, number line, "
                        "equivalence) and is developing Grade 4 skills (like-denominator "
                        "addition, mixed numbers). Her ceiling is at unlike-denominator "
                        "operations, which is a Grade 5 skill."
                    ),
                    "misconception_report": [
                        {
                            "description": "Larger denominator means larger fraction",
                            "status": "suspected",
                            "evidence": "Initially said 1/4 > 1/3 but self-corrected with concrete context. May resurface with abstract problems.",
                        },
                        {
                            "description": "Add numerators and denominators separately",
                            "status": "confirmed",
                            "evidence": "Computed 1/2 + 1/3 = 2/5 by adding across.",
                        },
                    ],
                    "overall_narrative": (
                        "Mia demonstrates a solid understanding of foundational fraction "
                        "concepts at the Grade 3 level, including part-whole relationships, "
                        "number line placement, and basic equivalence. She can generate "
                        "equivalent fractions for benchmark values and correctly add fractions "
                        "with like denominators.\n\n"
                        "She is beginning to develop Grade 4 skills, successfully interpreting "
                        "improper fractions as mixed numbers and adding same-denominator fractions "
                        "with clear reasoning. However, she has not yet developed strategies for "
                        "adding fractions with unlike denominators, defaulting to the common "
                        "'add across' error.\n\n"
                        "A notable finding is her tendency toward whole-number thinking when "
                        "comparing fractions (believing 1/4 > 1/3 because 4 > 3), though she "
                        "can self-correct when given concrete contexts. This suggests the "
                        "misconception is accessible to instruction."
                    ),
                    "recommended_next_steps": [
                        "Reinforce fraction comparison using visual models (fraction strips, area models) to build intuition that larger denominators mean smaller pieces",
                        "Introduce the concept of common denominators through concrete materials before teaching the procedure",
                        "Build on her strong number line understanding to visualize why 1/2 + 1/3 cannot equal 2/5",
                        "Continue developing equivalent fraction fluency beyond benchmark fractions (1/2, 1/4)",
                        "She is ready for structured introduction to unlike-denominator addition with visual support",
                    ],
                    "stop_reason": "sufficient_evidence",
                },
            },
        },
    ],
}
