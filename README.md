# awesome-skill-generate

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-unittest-green)](./tests)
[![Skills](https://img.shields.io/badge/meta--skills-2-orange)](./skills)
[![Language](https://img.shields.io/badge/readme-English%20default-blueviolet)](./README.md)

Turn notebooks, tutorials, and domain workflows into reusable agent skills.

This repository is built for `notebook -> executable skill`, not `notebook -> summary`.

中文说明见 [README.zh.md](./README.zh.md).

## Why This Repo

`awesome-skill-generate` helps an agent convert a notebook into a skill that is:

- Triggerable
- Executable
- Verifiable
- Reviewable

It pushes the agent to:

- extract a stable task from a notebook
- inspect real source code, `inspect.signature(...)`, `help(...)`, and `-h/--help`
- check branch-heavy parameters such as `method`, `recipe`, `backend`, and `mode`
- generate a reusable skill directory with `SKILL.md`, `references/`, and `assets/acceptance.json`
- score the generated skill with reviewer-side empirical checks

## Overview

```text
Notebook / Tutorial / Workflow
            |
            v
   skill-authoring
            |
            v
Generated Skill Directory
(SKILL.md + references + acceptance)
            |
            v
 skill-quality-scorer
            |
            v
Score Report + Validation + Acceptance
```

## Quick Start

1. Open this repository in Codex or Claude Code.
2. Pick a notebook you want to convert.
3. Ask the agent to use `skill-authoring` and output to `examples/generated-skills/<skill-name>/`.
4. Ask it to review the result with `skill-quality-scorer`.
5. Run validation and acceptance checks.

Example request:

```text
Use the skill-authoring skill in this repository to convert /absolute/path/to/notebook.ipynb into a reusable skill.

Requirements:
1. Write the output to examples/generated-skills/<skill-name>/
2. Do not just summarize the notebook
3. Check real source code, inspect.signature, help, or -h/--help
4. Inspect branch-heavy parameters such as method, recipe, backend, and mode
5. Review the generated result with skill-quality-scorer
6. Write a score report in the current directory
7. Run validate and acceptance
```

## Core Meta-Skills

- [`skills/skill-authoring/`](./skills/skill-authoring/SKILL.md)
  Converts a notebook into a reusable skill.
- [`skills/skill-quality-scorer/`](./skills/skill-quality-scorer/SKILL.md)
  Reviews and scores the generated skill, with reviewer-side empirical validation when appropriate.

## Tutorials

English:

- [Codex Tutorial](./codex-tutorial-en.md)
- [Claude Code Tutorial](./claude-code-tutorial-en.md)

中文：

- [Codex 中文教程](./codex-tutorial-zh.md)
- [Claude Code 中文教程](./claude-code-tutorial-zh.md)
- [中文 README](./README.zh.md)

## Repository Layout

```text
awesome-skill-generate/
├── README.md
├── README.zh.md
├── codex-tutorial-en.md
├── codex-tutorial-zh.md
├── claude-code-tutorial-en.md
├── claude-code-tutorial-zh.md
├── skills/
│   ├── skill-authoring/
│   └── skill-quality-scorer/
├── examples/
│   └── generated-skills/
├── scripts/
└── tests/
```

## Example

This repository includes a notebook-derived example skill:

- [`examples/generated-skills/dynamo-preprocess/`](./examples/generated-skills/dynamo-preprocess/SKILL.md)

Source notebook:

- `/Users/fernandozeng/Desktop/analysis/dynamo-release/docs/tutorials/notebooks/100_tutorial_preprocess.ipynb`

Example score report:

- [`dynamo-preprocess-score-report-2026-03-18.md`](./dynamo-preprocess-score-report-2026-03-18.md)

## Common Commands

Validate skills:

```bash
python3 scripts/validate_skills.py --root all
```

Run acceptance:

```bash
python3 scripts/run_skill_acceptance.py --root all
```

Run tests:

```bash
python3 -m unittest discover -s tests -v
```

Inspect a Python interface:

```bash
python3 scripts/inspect_python_interface.py dynamo.preprocessing:Preprocessor --pretty
```

## Principles

- A skill is not a notebook summary
- Source code is more authoritative than tutorial memory
- Branch-heavy parameters must be checked for coverage
- Scoring should not rely on text alone when empirical execution is needed

## License

No explicit license file is included yet.
