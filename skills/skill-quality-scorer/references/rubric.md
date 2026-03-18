# Skill Quality Rubric

Use a 1-5 scale for each dimension.

## Scale

- `1`: seriously inadequate
- `2`: partially present but unreliable
- `3`: usable with notable gaps
- `4`: strong and reliable
- `5`: excellent and low-ambiguity

## Dimensions And Weights

### 1. Trigger Precision (`15`)

Question:

- Will the skill trigger for the right requests and avoid obvious false positives?

Look for:

- a clear task description
- explicit use cases
- concrete artifacts or scenarios
- recognizable user-language synonyms

Penalize:

- vague descriptions like "help with data"
- missing trigger situations
- domain names without task names

### 2. Execution Clarity (`15`)

Question:

- Can another agent follow the workflow and act without guessing major steps?

Look for:

- ordered workflow
- minimal execution spine
- clear selection rules
- explicit assumptions and prerequisites
- source-grounded interface details when the skill documents concrete functions, methods, or CLI flags
- coverage of branch-like parameters such as `method`, `backend`, or `mode` when they control materially different behavior

Penalize:

- tutorial prose without procedure
- missing order of operations
- implicit prerequisites
- parameter descriptions copied from notebook usage without checking live signatures or defaults
- unmentioned conditional branches that another agent would need in real use

### 3. Validation Strength (`15`)

Question:

- Does the skill explain how to tell whether the output is correct?

Look for:

- concrete checks
- expected keys, files, outputs, or postconditions
- smoke tests or verification steps
- evidence that interface claims were checked against source, `help(...)`, or `-h/--help`

Penalize:

- no validation section
- "works if no error" as the only check
- validation hidden in an unrelated file
- no way to tell whether documented parameter choices are exhaustive or just notebook-local

### 4. Empirical Executability (`10`)

Question:

- Can the reviewer use representative data to follow the skill and verify that a documented core path actually works?

Look for:

- reviewer-run execution on representative data
- a synthetic-data spot check when real data is unnecessary
- a notebook-adjacent or fixture dataset run when the workflow is data-sensitive
- explicit checks for expected outputs after execution
- evidence gathered during scoring, not only evidence bundled by the generated skill itself

Penalize:

- no reviewer-run data-backed execution evidence
- interface import checks presented as if they were full execution proof
- scorer conclusions based only on text, references, or method presence for a data workflow
- inability to follow the skill on representative data because key instructions are missing or wrong

Scoring guidance:

- `1/5`: no empirical execution attempt at all
- `2/5`: import or interface smoke only
- `3/5`: reviewer ran one synthetic or minimal data execution path
- `4/5`: reviewer ran one realistic or notebook-adjacent data path with output checks
- `5/5`: reviewer ran multiple meaningful paths or strong fixture coverage with output checks

### 5. Context Efficiency (`10`)

Question:

- Does the skill minimize context usage while remaining complete?

Look for:

- short `SKILL.md`
- details delegated to `references/`
- little duplication

Penalize:

- bloated `SKILL.md`
- copied tutorial text
- repeated examples with no new information

### 6. Reusability (`10`)

Question:

- Is the skill built around a stable job rather than a one-off artifact?

Look for:

- reusable task framing
- clear abstraction from source material
- applicability beyond one notebook run

Penalize:

- skill is mostly a transcript of one tutorial
- no abstraction from source artifact

### 7. Resource Partitioning (`10`)

Question:

- Are `SKILL.md`, `references/`, `scripts/`, and `assets/` used appropriately?

Look for:

- core workflow in `SKILL.md`
- long details in `references/`
- repeated deterministic logic in `scripts/`

Penalize:

- all content stuffed into one file
- references that are required but never mentioned
- scripts that are essential but not surfaced

### 8. Compatibility Robustness (`10`)

Question:

- Does the skill identify version drift, dependency constraints, or known incompatibilities when they matter?

Look for:

- renamed APIs
- removed parameters
- extra dependencies
- environment assumptions
- source-verified branch options and defaults when notebook examples are incomplete

Penalize:

- silent dependency traps
- old API examples presented as current
- compatibility issues only discoverable by failure
- hidden `method`/`backend` branches that would only be discovered by reading code later

### 9. Maintainability (`5`)

Question:

- Can the skill be updated without large rewrites when the source changes?

Look for:

- good decomposition
- source-to-skill mapping
- compact structure

Penalize:

- tightly coupled prose
- no indication where content came from
- difficult-to-update monoliths

## Weighted Score

Compute:

- `sum(dimension_score / 5 * weight)`

This yields a score out of `100`.

## Verdict Rules

### `pass`

All hard-gate dimensions are at least `3`, and weighted score is at least `75`.

For skills whose main job is running a data workflow, analysis pipeline, preprocessing pipeline, simulation, or model execution, `Empirical Executability` must also be at least `3/5`.

### `revise`

Hard-gate dimensions pass but weighted score is below `75`, or the skill is usable but has clear structural weaknesses.

Also use `revise` when the structure is strong but reviewer-run data-backed execution evidence is too weak for a reliable `pass`.

### `fail`

Any hard-gate dimension is below `3`, or the skill is too ambiguous to use reliably.

## Severity Guidance

When summarizing issues:

- call out hard-gate failures first
- then call out the few changes that would raise the score the most
- avoid listing minor polish items before structural problems
