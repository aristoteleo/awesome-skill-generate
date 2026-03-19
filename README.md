<div align="center">

<img src="https://raw.githubusercontent.com/Starlitnightly/ImageStore/main/omicverse_img/Gemini_Generated_Image_9hq7de9hq7de9hq7.png" >


# awesome-skill-generate


### Turn notebook knowledge into reusable agent work.

**The manifesto for making agent-generated skills actually usable.**

Turn notebooks, tutorials, and one-off workflows into reusable, source-grounded, reviewable agent skills.

[![GitHub stars](https://img.shields.io/github/stars/aristoteleo/awesome-skill-generate?style=flat-square)](https://github.com/aristoteleo/awesome-skill-generate/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/aristoteleo/awesome-skill-generate?style=flat-square)](https://github.com/aristoteleo/awesome-skill-generate/commits/main)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-unittest-green?style=flat-square)](./tests)
[![Meta Skills](https://img.shields.io/badge/meta--skills-2-orange?style=flat-square)](./skills)
[![Notebook to Skill](https://img.shields.io/badge/notebook-%3E-skill-7c3aed?style=flat-square)](./README.md)
[![Source Grounded](https://img.shields.io/badge/source-grounded-0f766e?style=flat-square)](./skills/skill-authoring/SKILL.md)
[![Empirical Scoring](https://img.shields.io/badge/empirical-scoring-b45309?style=flat-square)](./skills/skill-quality-scorer/SKILL.md)
[![README](https://img.shields.io/badge/readme-English%20default-blueviolet?style=flat-square)](./README.md)

[Get Started](#quick-start) · [View Example](./examples/generated-skills/dynamo-preprocess/SKILL.md) · [Read Score Report](./dynamo-preprocess-score-report-2026-03-18.md) · [Codex Tutorial](./codex-tutorial-en.md) · [Claude Code Tutorial](./claude-code-tutorial-en.md) · [中文 README](./README.zh.md)

[Quick Start](#quick-start) · [Tutorials](#tutorials) · [At A Glance](#at-a-glance) · [Benchmark Snapshot](#benchmark-snapshot) · [Repository Layout](#repository-layout) · [Example](#example) · [Contributing](#contributing)

</div>

---

> [!WARNING]
> Default agents can already generate skills. Most of those skills are not reusable. This repository exists to change that.

## Why Builders Use This

If you are turning domain knowledge into AI products, internal automations, or reusable agent workflows, this repo gives you a path from:

- notebook
- prompt
- transcript
- one-off demo

to:

- reusable skill
- reviewable artifact
- scored deliverable
- standardizable unit of agent work

## The Problem We Are Solving

Most agent-generated skills fail in predictable ways:

- they summarize notebook prose instead of extracting a stable job
- they document only the branch that happened to run once
- they skip live checks against source code, signatures, help text, or CLI flags
- they have weak validation and no reviewer-side execution evidence
- they are hard to maintain because workflow, references, and evidence are all mixed together

`awesome-skill-generate` is designed to fix those failure modes.

## What Makes This Repo Different

<table>
  <tr>
    <td width="33%"><strong>Source-Grounded</strong><br/><br/>The generator pushes the agent to inspect real source code, <code>inspect.signature(...)</code>, <code>help(...)</code>, and <code>-h/--help</code> before documenting behavior.</td>
    <td width="33%"><strong>Branch-Aware</strong><br/><br/>It checks branch-heavy selectors such as <code>method</code>, <code>recipe</code>, <code>backend</code>, and <code>mode</code> so one notebook path is not mistaken for the whole interface.</td>
    <td width="33%"><strong>Evidence-Backed</strong><br/><br/>It does not stop at text quality. Skills are reviewed with validation rules, acceptance contracts, and reviewer-side empirical checks when the workflow is data-sensitive.</td>
  </tr>
</table>

<table>
  <tr>
    <td width="33%"><strong>Structured Artifacts</strong><br/><br/>The output is split into <code>SKILL.md</code>, <code>references/</code>, <code>assets/</code>, and optionally <code>scripts/</code> instead of dumping everything into one bloated file.</td>
    <td width="33%"><strong>Human-Visible Reports</strong><br/><br/>The scorer produces a readable report with commands, evidence, weighted scores, and residual risks.</td>
    <td width="33%"><strong>Standard-Driven</strong><br/><br/>This repo is trying to make skill generation auditable, comparable, and eventually standardizable.</td>
  </tr>
</table>


## Quick Start

> [!TIP]
> If you want the fastest path to value, start from one notebook with a clear stable task, generate one skill, score it, and inspect the report before scaling out.


1. Open this repository in Codex or Claude Code.
2. Pick a notebook you want to convert.
3. Ask the agent to use `skill-authoring` and write to `examples/generated-skills/<skill-name>/`.
4. Ask it to review the result with `skill-quality-scorer`.
5. Run validation and acceptance.

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

## Tutorials

**English**

- [Codex Tutorial](./codex-tutorial-en.md)
- [Claude Code Tutorial](./claude-code-tutorial-en.md)

**中文**

- [Codex 中文教程](./codex-tutorial-zh.md)
- [Claude Code 中文教程](./claude-code-tutorial-zh.md)
- [中文 README](./README.zh.md)

## At A Glance

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

## Default Agent Output vs. This Repo

| Dimension | Typical default agent output | `awesome-skill-generate` |
| --- | --- | --- |
| Goal | Summarize the notebook | Build a reusable skill |
| API handling | Uses what the notebook happened to show | Checks live source, signatures, help, and branches |
| Validation | Light or missing | Explicit validation and acceptance |
| Data workflows | Often text-only review | Reviewer-side empirical execution when needed |
| Artifact shape | One big document | `SKILL.md` + `references/` + `assets/` + optional `scripts/` |
| Human trust | Implicit | Report-backed |
| Maintenance | Drift-prone | Traceable and updateable |

## Benchmark Snapshot

Measured example in this repository:

<div align="center">

[![Weighted Score](https://img.shields.io/badge/weighted%20score-95%2F100-111827?style=for-the-badge)](./dynamo-preprocess-score-report-2026-03-18.md)
[![Verdict](https://img.shields.io/badge/verdict-pass-15803d?style=for-the-badge)](./dynamo-preprocess-score-report-2026-03-18.md)
[![Execution Clarity](https://img.shields.io/badge/execution%20clarity-5%2F5-1d4ed8?style=for-the-badge)](./dynamo-preprocess-score-report-2026-03-18.md)
[![Empirical Executability](https://img.shields.io/badge/empirical%20executability-5%2F5-b45309?style=for-the-badge)](./dynamo-preprocess-score-report-2026-03-18.md)

[![Source Grounded](https://img.shields.io/badge/source-grounded-0f766e?style=flat-square)](./skills/skill-authoring/SKILL.md)
[![Branch Aware](https://img.shields.io/badge/branch-aware-7c2d12?style=flat-square)](./examples/generated-skills/dynamo-preprocess/references/source-grounding.md)
[![Report Backed](https://img.shields.io/badge/report-backed-7e22ce?style=flat-square)](./dynamo-preprocess-score-report-2026-03-18.md)

</div>

> [!NOTE]
> The benchmark shown here is based on the repository's current `dynamo-preprocess` example skill and its linked score report.

- generated skill: [`examples/generated-skills/dynamo-preprocess/`](./examples/generated-skills/dynamo-preprocess/SKILL.md)
- score report: [`dynamo-preprocess-score-report-2026-03-18.md`](./dynamo-preprocess-score-report-2026-03-18.md)
- weighted score: `95/100`
- verdict: `pass`

> [!IMPORTANT]
> The default-agent baseline below is an illustrative rubric-based profile, not a separately versioned benchmark artifact. It is meant to show the failure modes this repository is trying to eliminate.

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

### What Those Gains Actually Mean

The gains are not aesthetic. They come from four concrete upgrades:

- source-grounding against live APIs instead of notebook memory
- branch coverage for `method` / `recipe` / `backend` style selectors
- reviewer-side empirical execution checks for data workflows
- a structured artifact layout that remains maintainable as upstream code changes

## The Standard We Want To Set

This repository is not just a prompt collection. It is trying to make skill generation auditable, comparable, and standardizable.

The standard is simple:

1. A skill must define a stable job, not mirror a tutorial title.
2. A skill must include a trigger contract, execution spine, and validation contract.
3. Concrete API or CLI claims should be grounded in live source, signatures, help text, or CLI help.
4. Branch-heavy parameters must be checked for coverage, not inferred from a single notebook path.
5. Data workflows should be reviewable with reviewer-side execution evidence when needed.
6. The artifact layout should be explicit: `SKILL.md`, `references/`, `assets/`, and optionally `scripts/`.
7. A score report should be visible to humans and should include commands, evidence, and residual risks.
8. Quality should be measured with a rubric, not with vibes.

If enough generated skills follow these rules, skill generation stops being ad hoc prompt craft and starts looking like an engineering discipline.


## Core Meta-Skills

- [`skills/skill-authoring/`](./skills/skill-authoring/SKILL.md)
  Converts a notebook into a reusable skill.
- [`skills/skill-quality-scorer/`](./skills/skill-quality-scorer/SKILL.md)
  Reviews and scores the generated skill, with reviewer-side empirical validation when appropriate.


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

## Contributing

Contributions of all types are more than welcome. Whether it is publishing skills, improving the generator, refining the scorer, tightening the benchmark story, or contributing code, feel free to check out our GitHub Issues and start building.

## License

This project is [BSD 2-Clause](./LICENSE) licensed.

## Copyright

Copyright © 2026 [Qiu Lab](https://www.devo-evo.com).
