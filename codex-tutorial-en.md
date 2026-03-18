# Codex Tutorial

This tutorial is for people who want Codex to use `awesome-skill-generate` to turn a notebook into a reusable skill.

## What To Prepare

Prepare at least three things:

1. The notebook path
2. The source code or runnable environment
3. The output directory

Recommended output directory:

- `examples/generated-skills/<skill-name>/`

Do not write the result to:

- `skills/<skill-name>/`

because `skills/` stores the repository's own meta-skills.

## Minimal Prompt

```text
Use the skill-authoring skill in this repository to convert /absolute/path/to/your.ipynb into a reusable skill.

Requirements:
1. Write the output to examples/generated-skills/<skill-name>/
2. Do not just summarize the notebook; extract an executable skill for another Agent
3. Check the real source code, inspect.signature, help, or -h/--help
4. Pay special attention to branch-heavy parameters such as method, recipe, backend, and mode
5. After generation, review the result with skill-quality-scorer
6. During scoring, try to use data to validate executability instead of relying on documentation only
7. Finally run validate and acceptance
```

## Recommended Prompt

```text
In this repository, use awesome-skill-generate to convert the following notebook into a reusable skill:

Input notebook:
/absolute/path/to/your-notebook.ipynb

Output directory:
examples/generated-skills/your-skill-name/

Requirements:
1. Use the skill-authoring workflow to generate the skill
2. Do not place the result under the repository's own skills/ directory
3. Extract a stable task from the notebook instead of copying the notebook title
4. Check the real interface first, including source code, inspect.signature, help, or CLI -h/--help
5. Inspect branching parameters such as method, recipe, backend, mode, provider, and *_method
6. The generated skill should include at least:
   - SKILL.md
   - references/source-notebook-map.md
   - references/source-grounding.md when concrete functions, parameters, or commands are documented
   - assets/acceptance.json
7. Review the generated skill with skill-quality-scorer
8. During scoring, run representative data instead of reviewing text only
9. Write the score report into the current directory as `<skill-name>-score-report-YYYY-MM-DD.md`
10. Finally run:
   - python3 scripts/validate_skills.py --root examples
   - python3 scripts/run_skill_acceptance.py --root examples
   - python3 -m unittest discover -s tests -v
```

## What Codex Should Do

A solid Codex run should include:

1. Read the notebook
2. Read the relevant source code
3. Identify the stable task
4. Build the skill directory structure
5. Write `SKILL.md`
6. Write `references/`
7. Write `assets/acceptance.json`
8. Review the result with the scorer
9. Run representative data from the scorer's perspective
10. Generate a score report

## How To Review The Result

Check these points:

- Is it only retelling the notebook?
- Did it inspect the real interface?
- Did it inspect branching parameters?
- Did it write to the correct output directory?
- Did the scorer actually run data?
- Did it create a score report in the current directory?

## Real Example

```text
Use the skill-authoring skill in this repository to convert /Users/fernandozeng/Desktop/analysis/dynamo-release/docs/tutorials/notebooks/100_tutorial_preprocess.ipynb into a reusable skill.

Please use the conda environment named omictest.

Requirements:
1. Write the output to examples/generated-skills/dynamo-preprocess/
2. Do not just summarize the notebook; extract an executable skill for another Agent
3. Check the real source code, inspect.signature, help, or -h/--help
4. Pay special attention to branch-heavy parameters such as method, recipe, backend, and mode
5. After generation, review the result with skill-quality-scorer
6. During scoring, use synthetic data or notebook-adjacent data to validate executability
7. Finally run validate and acceptance
```

## Useful Commands

```bash
python3 scripts/validate_skills.py --root examples
python3 scripts/run_skill_acceptance.py --root examples
python3 -m unittest discover -s tests -v
```
