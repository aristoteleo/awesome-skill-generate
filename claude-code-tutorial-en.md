# Claude Code Tutorial

This tutorial is for people who want Claude Code to use `awesome-skill-generate` to turn a notebook into a reusable skill.

## Workflow

Claude Code should play a role very similar to Codex in this repository:

- Use `skill-authoring` to generate the skill
- Use `skill-quality-scorer` to review the skill
- Run representative data during scoring
- Produce a score report in the current directory

## What Your Task Description Should Include

Your task description should usually specify:

- The notebook path
- The output directory
- The Python environment
- Source-grounding requirements
- Branch coverage requirements
- Reviewer-side data validation requirements

## Recommended Prompt Template

```text
In this repository, use the two core meta-skills from awesome-skill-generate to do the following:

1. Use skill-authoring to convert /absolute/path/to/notebook.ipynb into a reusable skill
2. Write the output to examples/generated-skills/your-skill-name/
3. Check the real source code, inspect.signature, help, or CLI help
4. Inspect branch-heavy parameters such as method, recipe, backend, and mode
5. Use skill-quality-scorer to score the generated result
6. During scoring, do not rely on documentation only; use representative data to validate executability
7. Write the scoring report to the current directory as `<skill-name>-score-report-YYYY-MM-DD.md`
8. Finally run validate, acceptance, and tests
```

## Expected Outputs

An ideal Claude Code run should produce:

- A generated skill directory
- Reviewer-side execution evidence
- A score report in the current directory
- A short risk summary

## What You Should Review

- Is the skill actually triggerable?
- Is the skill actually executable?
- Did the scorer really run data?
- Does the score report include real commands and results?

## Claude Code Example

```text
Use the skill-authoring skill in this repository to convert /Users/fernandozeng/Desktop/analysis/dynamo-release/docs/tutorials/notebooks/100_tutorial_preprocess.ipynb into a reusable skill.

Please use the conda environment named omictest.

Requirements:
1. Write the output to examples/generated-skills/dynamo-preprocess/
2. Do not just summarize the notebook; extract an executable skill for another Agent
3. Check the real source code, inspect.signature, help, or -h/--help
4. Pay special attention to branch-heavy parameters such as method, recipe, backend, and mode
5. After generation, review the result with skill-quality-scorer
6. During scoring, use representative data to validate executability
7. Finally run validate and acceptance
```

## Useful Commands

```bash
python3 scripts/validate_skills.py --root all
python3 scripts/run_skill_acceptance.py --root all
python3 -m unittest discover -s tests -v
```
