---
name: skill-authoring
description: Create or update a Codex skill that packages reusable workflows, references, scripts, and assets for repeated tasks. Use when turning notebooks, tutorials, analyses, or domain procedures into a triggerable local skill for other agents.
---

# Skill Creator

Create skills that are short, reusable, and biased toward execution.

## Core Rules

1. Optimize for another agent using the skill, not for a human reading documentation.
2. Keep `SKILL.md` small. Put details into `references/`, deterministic logic into `scripts/`, and templates into `assets/`.
3. Put trigger conditions in frontmatter `description`, not in the body.
4. Prefer procedures and selection rules over long explanations.
5. Source-ground every interface-specific claim against real code, `help(...)`, or `-h/--help` before writing it into the skill.
6. Include only information another agent is unlikely to infer reliably from general knowledge.
7. Default to capability-first naming. Do not let a sample dataset, species, notebook title, or one published figure become the skill identity unless the workflow is truly specific to that artifact.
8. In generated skill documentation, prefer repo-relative paths or import paths. Do not bake local absolute source-code paths from one machine into `SKILL.md` or `references/`.
9. Keep reusable skill content environment-agnostic. Do not encode local environment names such as `omictest` into `SKILL.md` or `references/`; if local validation depends on them, keep that only in the review harness, acceptance harness, or calling prompt.
10. Treat local validation configuration as review-harness data, not as part of the reusable skill itself.

## Skill Shape

Each skill should follow this structure:

```text
skill-name/
├── SKILL.md
├── scripts/        # executable helpers for repeated or fragile steps
├── references/     # selectively loaded reference material
└── assets/         # templates, starter files, static resources
```

Use only the folders that are needed. Do not add extra docs like `README.md`, `CHANGELOG.md`, or process notes.

## What Belongs Where

### Put in `SKILL.md`

- Skill purpose
- Triggering scope
- The minimum workflow another agent should follow
- Selection rules for which reference or script to use
- Constraints, assumptions, and validation requirements

### Put in `references/`

- API notes
- domain conventions
- notebook-specific biological background
- long examples
- parameter tables

### Put in `scripts/`

- notebook extraction helpers
- format conversion
- deterministic preprocessing
- repeated analysis setup
- validation utilities

### Put in `assets/`

- starter notebooks
- report templates
- plotting styles
- canned config files

Do not treat reviewer-only local execution settings as normal skill content. Machine-specific interpreter paths, local cache locations, and one-user environment bootstrapping belong in the local review harness or the calling prompt, not in the reusable skill body.

## Writing Frontmatter

Frontmatter should contain only:

```yaml
---
name: skill-name
description: What the skill does and when to use it.
---
```

Write the description so the agent can trigger the skill correctly from user intent alone.

Good description properties:

- names the task
- names the artifacts involved
- names the situations that should trigger the skill
- includes common synonyms users may say

## Writing the Body

Use imperative instructions. Assume the reader is a capable coding agent with limited context.

Prefer this body structure:

```markdown
# Skill Name

## Goal

One short paragraph.

## Quick Workflow

1. Inspect the source artifacts.
2. Select the relevant reference or script.
3. Execute the transformation.
4. Validate the output.

## Resource Map

- Read `references/x.md` when ...
- Run `scripts/y.py` when ...

## Constraints

- Keep ...
- Avoid ...

## Validation

- Check ...
- Compare ...
```

## Notebook To Skill Workflow

Use this workflow when the source material is an `ipynb` tutorial.

### Step 1: Identify the reusable task

Extract the repeated capability behind the notebook, not the notebook itself.

Examples:

- "fit a vector field on dynamo tutorial data"
- "run Jacobian / acceleration / curvature analysis on a simulated motif"
- "preprocess AnnData and prepare layers for downstream dynamo analysis"

If a notebook mixes several capabilities, split them into separate skills or into one skill with clearly separated references.

### Step 1.5: Choose the right abstraction level

Before naming the skill, separate three layers explicitly:

- stable job or analysis family
- data modality or input contract
- worked example dataset, species, or notebook title

In almost all cases:

- use the stable job as the skill identity
- use the data modality as a constraint or scope note
- demote the worked example to `references/`, validation, or an example section

Prefer names like:

- `dynamo-conventional-rna-velocity`
- `dynamo-vector-field-analysis`
- `gene-id-conversion`

Avoid names like:

- `zebrafish-workflow`
- `figure-2-pipeline`
- `tutorial-200-skill`

Only keep the example dataset or species in the skill name when changing the example would materially break the workflow or invalidate the interpretation.

### Step 2: Separate stable logic from tutorial narration

Classify notebook content into four buckets:

- reusable procedure
- required biological or domain assumptions
- one-off exposition or teaching text
- display-only output

Only the first two usually belong in the skill.

### Step 3: Extract the execution spine

The skill should preserve the minimal sequence another agent must reproduce:

1. input assumptions
2. required imports and data shape expectations
3. preprocessing
4. core analysis calls
5. postprocessing or storage conventions
6. validation checks

Do not copy the notebook cell-by-cell unless the exact order is fragile and necessary.

### Step 3.5: Inspect the real callable interface before documenting it

If the notebook relies on concrete functions, methods, classes, or CLIs, inspect the live interface before writing the skill:

1. read the source or run `help(...)`
2. capture `inspect.signature(...)` and parameter defaults
3. extract parameter-level doc details when available
4. detect branch-like parameters such as `method`, `backend`, or `mode`
5. inspect `if` / `match` branches so notebook coverage does not hide unmentioned features

If the target is importable Python code, run `scripts/inspect_python_interface.py`.
If the target is a command-line tool, inspect `-h` or `--help`.

### Step 4: Move long notebook context out of `SKILL.md`

Use `references/` for:

- mathematical background
- motif-specific explanations
- differences between old and new APIs
- alternative branches in the tutorial
- expected figures and interpretation notes

Path rule:

- use repo-relative paths like `docs/tutorials/notebooks/200_zebrafish.ipynb`
- or import paths like `dynamo.preprocessing.Preprocessor`
- do not record machine-specific absolute paths like `/Users/alice/.../dynamo/preprocessing/Preprocessor.py` in generated skill docs
- if local review needs a concrete interpreter such as `python_path`, keep that in the local review harness, scorer workflow, or calling prompt rather than promoting it into the reusable skill
- if a repository-level acceptance harness needs a named environment, keep that requirement in the local harness rather than treating it as part of the reusable skill contract

Use `scripts/` for:

- notebook parsing
- dataset loading wrappers
- common plotting or metric generation
- compatibility shims for renamed APIs

### Step 5: Encode trigger language from how users actually ask

For notebook-derived skills, descriptions should include both the task and the artifact style.

Examples:

- "Use when converting a dynamo tutorial or analysis notebook into a reusable execution workflow."
- "Use when an agent needs to run the mixture-of-gaussian simulation, compute analytical Jacobian-derived quantities, or reconcile old tutorial API names with current dynamo code."

Default trigger-writing rule:

- lead with the capability
- include the data modality or artifact style only if it narrows execution meaningfully
- mention the source notebook or example dataset as adaptation context, not as the main trigger surface

Good:

- "Run or adapt a conventional spliced/unspliced RNA velocity workflow in dynamo. Use when analyzing conventional scRNA-seq `AnnData`, reproducing a related tutorial, or selecting between preprocessing, kinetics, vector-field, and fate stages."

Weak:

- "Run the zebrafish notebook."

Weak because it triggers on a worked example, not on the stable job another agent actually needs.

### Step 6: Add compatibility notes only when they unblock execution

Notebook-based skills often need a short compatibility section for drift such as:

- renamed functions
- removed parameters
- changed motif names
- old plotting keys
- old embedding slots

Keep this compact. Put full migration details into `references/compatibility.md`.

### Step 7: Validate against a fresh execution path

Before finalizing the skill, confirm that another agent could execute the workflow without relying on the original notebook narrative.

Validation should check:

- the skill can be triggered from a realistic user request
- the core workflow can be followed without opening the full notebook unless necessary
- references are actually sufficient
- scripts run or are at least structurally correct
- output names and storage locations are explicit
- function signatures, defaults, doc-derived constraints, and branch options were checked against the live interface
- the skill still makes sense if the original example dataset or species name is removed from the user request
- the reusable skill is not secretly coupled to one reviewer's local interpreter path or machine setup

### Step 7.5: Run an anti-overfitting check

Before shipping the skill, ask these questions:

- If the user asked for the workflow without naming the tutorial dataset, would this skill still trigger?
- If the example dataset were replaced with another compatible dataset, would most of `SKILL.md` still hold?
- Are dataset-specific grouping columns, lineage labels, or plotting genes presented as defaults only because the notebook used them?

If any answer is "no", the skill is probably overfit to the notebook. Move the example-specific material into:

- `references/source-notebook-map.md`
- `references/compatibility.md`
- a worked example section
- acceptance smoke commands

For local validation settings, move them even further out:

- the calling prompt
- the local scorer or reviewer workflow
- a repository-level harness that is explicitly marked as local-only

## Design Heuristics For `ipynb`-Derived Skills

Prefer one skill per stable job. Do not build a single skill that tries to cover every notebook in a project.

Good candidates for one skill:

- a repeated simulation workflow
- one analysis family
- one plotting/reporting pipeline
- one data ingestion pattern
- one stable modality-constrained workflow with multiple example datasets

Bad candidates:

- an entire tutorial collection with unrelated goals
- a notebook whose value is mostly pedagogy rather than reusable execution
- a workflow that depends heavily on interactive interpretation at every step
- a skill whose name and trigger language are mostly the name of one sample dataset

## Recommended Deliverables For Notebook Conversion

When converting a notebook into a skill, aim for:

1. `SKILL.md` with the distilled workflow
2. `references/source-notebook-map.md` mapping notebook sections to skill resources
3. `references/source-grounding.md` summarizing signature/docstring/source inspection for critical interfaces
4. `references/compatibility.md` for API drift, if needed
5. `scripts/` helpers for repeated extraction or setup, if needed
6. `assets/acceptance.json` with sample requests, required sections, required terms, and optional smoke commands
7. optional additional `assets/` templates only if they save substantial repeated effort

## Resource Map

- Read `references/source-grounding.md` when the skill documents concrete function signatures, defaults, docstrings, or CLI flags.
- Run `scripts/inspect_python_interface.py` when a notebook depends on importable Python callables and branch-like parameters may hide unexercised behavior.

## Review Checklist

Before finishing, check the skill against this list:

- Frontmatter uses only `name` and `description`
- Description is strong enough to trigger correctly
- `SKILL.md` is procedural and not tutorial-heavy
- Large details moved to `references/`
- Repeated code moved to `scripts/`
- Critical function and CLI behavior was checked against source, `help(...)`, or `-h/--help`
- Branch-like parameters such as `method` or `backend` were audited for unmentioned options
- The skill name and description describe the stable capability, not just the notebook example
- Example dataset, species, and notebook-title details were demoted out of the main trigger surface unless they are execution-critical
- A counterfactual request without the notebook's proper nouns would still trigger the skill correctly
- `SKILL.md` and `references/` do not depend on machine-specific absolute source paths
- `assets/acceptance.json` prefers environment names such as `conda_env` over machine-specific interpreter paths
- reviewer-only local validation configuration is not presented as if it were part of the reusable skill contract
- Old notebook API drift is captured where necessary
- Validation steps are explicit
- `assets/acceptance.json` encodes concrete acceptance checks beyond scoring
- No extra documentation files were added

## Editing Existing Skills

When updating an existing skill:

1. Keep the existing trigger surface unless there is a clear triggering bug.
2. Remove duplicated explanations before adding new content.
3. Prefer tightening the workflow over expanding prose.
4. If the source notebook changed, update compatibility notes and resource mapping first.
5. Re-check whether the current `description` still matches what the skill actually does.
