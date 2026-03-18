# awesome-skill-generate

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-unittest-green)](./tests)
[![Skills](https://img.shields.io/badge/meta--skills-2-orange)](./skills)
[![Language](https://img.shields.io/badge/readme-English%20default-blueviolet)](./README.md)

Turn notebooks, tutorials, and domain workflows into reusable agent skills.

This repository is built for `notebook -> executable skill`, not `notebook -> summary`.

中文说明见 [README.zh.md](./README.zh.md).

## Why This Repo Exists

Most agent-generated skills fail in predictable ways:

- they restate notebook prose instead of extracting a stable job
- they document only the branch that happened to run in the notebook
- they skip live interface checks against source code, `inspect.signature(...)`, `help(...)`, or `-h/--help`
- they have weak validation and no reviewer-side execution evidence
- they are hard to maintain because notebook facts, source facts, and validation facts are mixed together

`awesome-skill-generate` is designed to fix those failure modes.

## Why It Is "Awesome"

This repository pushes an agent to produce a skill that is:

- Triggerable
- Executable
- Verifiable
- Reviewable
- Source-grounded
- Branch-aware
- Scored with explicit evidence

In practice, that means the generator is expected to:

- extract a stable task from a notebook
- inspect real source code, `inspect.signature(...)`, `help(...)`, and `-h/--help`
- check branch-heavy parameters such as `method`, `recipe`, `backend`, and `mode`
- generate a reusable skill directory with `SKILL.md`, `references/`, and `assets/acceptance.json`
- review the generated skill with empirical scorer-side checks when needed
- emit a user-visible score report instead of a vague pass/fail claim

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

## Benchmark Snapshot

Measured example in this repository:

- generated skill: [`examples/generated-skills/dynamo-preprocess/`](./examples/generated-skills/dynamo-preprocess/SKILL.md)
- score report: [`dynamo-preprocess-score-report-2026-03-18.md`](./dynamo-preprocess-score-report-2026-03-18.md)
- weighted score: `95/100`
- verdict: `pass`

Comparison baseline used below:

- a typical default agent output that mostly summarizes a notebook
- does not do full source-grounding or reviewer-side empirical validation
- this baseline is an illustrative rubric-based profile, not a separately versioned benchmark artifact

### Weighted Score Comparison

```text
Typical default agent skill      38/100  [########------------]
awesome-skill-generate example   95/100  [###################-]
```

### Dimension Breakdown

```text
Dimension                  Default Agent   This Repo Example
Trigger Precision          3/5  ###--      5/5  #####
Execution Clarity          2/5  ##---      5/5  #####
Validation Strength        1/5  #----      4/5  ####-
Empirical Executability    1/5  #----      5/5  #####
Context Efficiency         3/5  ###--      4/5  ####-
Reusability                2/5  ##---      5/5  #####
Resource Partitioning      2/5  ##---      5/5  #####
Compatibility Robustness   1/5  #----      5/5  #####
Maintainability            2/5  ##---      5/5  #####
```

### What The Comparison Is Saying

The biggest practical gains are not cosmetic. They come from four things that default agent output usually misses:

- source-grounding against live APIs instead of notebook memory
- branch coverage for `method` / `recipe` / `backend` style selectors
- reviewer-side empirical execution checks for data workflows
- a structured artifact layout that stays maintainable as upstream code changes

## Toward An Industry Standard For Skill Generation

This repository is not just a prompt collection. It is trying to make skill generation auditable and standardizable.

The standard we are trying to establish is:

1. A skill must define a stable job, not just mirror a tutorial title.
2. A skill must include a trigger contract, execution spine, and validation contract.
3. Any concrete API or CLI claim should be grounded in live source, signatures, help text, or CLI help.
4. Branch-heavy parameters must be checked for coverage, not inferred from one notebook path.
5. Data workflows should be reviewable with reviewer-side execution evidence when needed.
6. The artifact layout should be explicit: `SKILL.md`, `references/`, `assets/`, and optionally `scripts/`.
7. A score report should be visible to humans and should include commands, evidence, and residual risks.
8. Quality should be measured with a rubric, not with vibes.

If enough generated skills follow these rules, skill generation stops being ad hoc prompt craft and starts looking like an engineering discipline.

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
