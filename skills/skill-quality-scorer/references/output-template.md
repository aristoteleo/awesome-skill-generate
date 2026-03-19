# Output Template

Use this template when returning a scorecard.

```markdown
Verdict: pass | revise | fail
Weighted score: NN/100

Dimension scores:
- Trigger Precision: N/5
  Reason: ...
- Execution Clarity: N/5
  Reason: ...
- Validation Strength: N/5
  Reason: ...
- Empirical Executability: N/5
  Reason: ...
- Context Efficiency: N/5
  Reason: ...
- Reusability: N/5
  Reason: ...
- Resource Partitioning: N/5
  Reason: ...
- Compatibility Robustness: N/5
  Reason: ...
- Maintainability: N/5
  Reason: ...

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
  Reason: ...
- Execution Clarity: N/5
  Reason: ...
- Validation Strength: N/5
  Reason: ...
- Empirical Executability: N/5
  Reason: ...
- Context Efficiency: N/5
  Reason: ...
- Reusability: N/5
  Reason: ...
- Resource Partitioning: N/5
  Reason: ...
- Compatibility Robustness: N/5
  Reason: ...
- Maintainability: N/5
  Reason: ...

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

## Rationale Rule

Do not separate raw scores from their explanations. In both the inline scorecard and the Markdown report, each dimension must be immediately followed by its reason.
