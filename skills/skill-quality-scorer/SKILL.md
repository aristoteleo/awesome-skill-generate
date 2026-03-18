---
name: skill-quality-scorer
description: Evaluate the quality of a Codex skill from multiple dimensions and produce a structured score, verdict, and revision guidance. Use when reviewing a `SKILL.md`, scoring a skill folder, comparing two skills, performing cross-review on a newly created skill, or checking whether a skill is triggerable, executable, concise, and maintainable without loading unnecessary context.
---

# Skill Quality Scorer

## Goal

Score a skill on quality, not domain sophistication. Review whether another agent could trigger and use the skill reliably with minimal ambiguity and minimal context waste.

## Quick Workflow

1. Read the target `SKILL.md`.
2. If the skill documents a real callable or CLI, inspect the live interface before trusting notebook-derived claims.
3. For data workflows, try to follow the skill on representative data before final scoring.
4. Read only the referenced files needed to judge execution quality, resource partitioning, validation quality, source grounding, and empirical executability.
5. Score each required dimension using `references/rubric.md`.
6. Apply hard gates before computing the final verdict.
7. Return a compact scorecard plus the highest-signal revision guidance.
8. Write a human-readable Markdown score report to the current working directory instead of hiding it inside the generated skill folder.

## Scope

Use this skill to review:

- a skill folder
- a standalone `SKILL.md`
- a proposed skill diff
- two competing skill designs
- a notebook-derived skill after conversion

Do not score:

- the scientific correctness of the underlying domain unless the skill itself makes unsupported domain claims
- code quality outside the skill's own bundled scripts and instructions
- repository-wide documentation unrelated to the skill

## Review Rules

- Default to reading `SKILL.md` first.
- Read `references/` only when the main skill explicitly depends on them or when resource partitioning is being scored.
- Read `scripts/` only when the skill relies on them for core execution or validation.
- When the skill claims concrete function or CLI behavior, verify that behavior against source, `help(...)`, or `-h/--help` before treating the skill as complete.
- For notebook-derived data workflows, do not stop at interface inspection if representative data can be constructed or loaded reasonably.
- Treat missing branch coverage for `method`, `backend`, `mode`, `provider`, or similar parameters as a real usability risk, not a minor omission.
- Do not reward verbosity.
- Do not reward domain difficulty.
- Do not assume missing validation or compatibility notes are present elsewhere.
- Penalize trigger ambiguity, execution ambiguity, and hidden dependencies aggressively.

## Hard Gates

Apply these gates before issuing a passing verdict:

- `Trigger Precision` must be at least `3/5`.
- `Execution Clarity` must be at least `3/5`.
- `Validation Strength` must be at least `3/5`.
- For data workflows, `Empirical Executability` must be at least `3/5`.

If any hard-gate dimension is below `3`, the skill cannot receive a `pass` verdict even if the weighted score is otherwise high.

## Output Format

Return results in this order:

1. Overall verdict: `pass`, `revise`, or `fail`
2. Weighted score out of `100`
3. Dimension-by-dimension scores
4. Top issues blocking a higher score
5. Targeted revision actions

Also write a Markdown report file in the current working directory with a strict name like:

- `<skill-name>-score-report-YYYY-MM-DD.md`

Do not place this report inside the generated skill folder unless the user explicitly asks for that.
The filename pattern replaces older loose names such as `score-report.md`.

The report should include concrete evidence, not only the final score:

- files reviewed
- commands actually run
- test and validation outputs
- interface inspection evidence
- reviewer-run empirical execution evidence on real or synthetic data when applicable
- dimension-by-dimension scoring rationale
- residual risks

Keep the review concise. Prefer high-signal findings over a long narrative.

## Comparison Mode

When comparing two skills:

- score both using the same rubric
- keep the same standard across both reviews
- explain which one is more triggerable, more executable, or more maintainable
- identify whether one is shorter but underspecified or richer but too heavy

## Cross-Review Guidance

When reviewing a skill that was just created in the same repository:

- treat the scoring as independent evaluation
- do not import the creator's unstated intentions
- score only what is discoverable from the skill and its referenced resources
- if a needed behavior exists only in the source notebook or in the author's head, score that as missing
- if a notebook-derived skill documents only one observed `method` path but the source has more branches, score the missing branches as an execution and compatibility gap

## Resource Map

- Read `references/rubric.md` for scoring dimensions, weights, and verdict rules.
- Read `references/output-template.md` when you need a consistent review format.
- Read `references/source-grounding-audit.md` when judging whether a skill is grounded in real function signatures, docstrings, or branch behavior.
- Run `scripts/inspect_python_interface.py` when you need a quick source-grounded view of a Python callable before scoring completeness.
