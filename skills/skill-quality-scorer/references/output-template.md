# Output Template

Use this template when returning a scorecard.

```markdown
Verdict: pass | revise | fail
Weighted score: NN/100

Dimension scores:
- Trigger Precision: N/5
- Execution Clarity: N/5
- Validation Strength: N/5
- Empirical Executability: N/5
- Context Efficiency: N/5
- Reusability: N/5
- Resource Partitioning: N/5
- Compatibility Robustness: N/5
- Maintainability: N/5

Top issues:
- ...
- ...

Recommended revisions:
- ...
- ...
```

## Report File Template

Write a separate Markdown report in the current working directory, for example:

- `dynamo-preprocess-score-report-2026-03-18.md`

Suggested structure:

```markdown
# Skill Score Report: <skill-name>

- Verdict: pass | revise | fail
- Weighted score: NN/100
- Reviewed skill: <path>
- Report date: YYYY-MM-DD

## Dimension Scores

- Trigger Precision: N/5
- Execution Clarity: N/5
- Validation Strength: N/5
- Empirical Executability: N/5
- Context Efficiency: N/5
- Reusability: N/5
- Resource Partitioning: N/5
- Compatibility Robustness: N/5
- Maintainability: N/5

## Reviewed Files

- ...
- ...

## Commands Run

```bash
...
```

## Validation Results

- Command: ...
- Result: ...
- Key output: ...

## Interface Inspection Evidence

```text
...
```

## Scoring Rationale

- Trigger Precision: ...
- Execution Clarity: ...
- Validation Strength: ...
- Empirical Executability: ...
- Context Efficiency: ...
- Reusability: ...
- Resource Partitioning: ...
- Compatibility Robustness: ...
- Maintainability: ...

## Key Findings

- ...
- ...

## Recommended Revisions

- ...
- ...

## Residual Risks

- ...
- ...
```

## Comparison Template

Use this when scoring two skills.

```markdown
Skill A: NN/100, verdict
Skill B: NN/100, verdict

Why A is stronger:
- ...

Why B is stronger:
- ...

Most important next revision:
- Skill A: ...
- Skill B: ...
```

## Brevity Rule

Keep the review compact unless the user asks for a deep audit. Lead with the verdict and the few issues that most affect usability.
