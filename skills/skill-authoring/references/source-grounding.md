# Source Grounding

Use this reference when a notebook-derived skill documents Python callables, methods, CLI commands, or recipe-like parameters.

## Rule

Do not describe a function interface from notebook usage alone.

Before writing parameter behavior into the skill, inspect the real interface from at least one of:

- source code
- `inspect.signature(...)`
- `help(...)` or docstring extraction
- `-h` / `--help` for CLI entrypoints

If you cannot inspect the real interface, mark the skill as incomplete and avoid pretending that notebook examples are exhaustive.

## Required Output For Python Callables

For each important callable or method, capture:

- full callable path
- signature
- parameter defaults
- parameter-level doc details when available
- branch-like parameters such as `method`, `backend`, `mode`, `provider`, `task`, or `*_method`
- detected branch values from source-level conditionals

Use `scripts/inspect_python_interface.py` when the target is importable Python code.
If the interface only exists in a specific runtime, run the inspection and smoke checks in a local compatible environment, but do not treat that environment name as part of the reusable skill content. Keep local environment naming in the review harness or calling prompt.

## Branch Coverage Requirement

Notebook examples often exercise only one branch, such as `method="monocle"`.

Before finalizing the skill:

1. detect branch-like parameters from signature names
2. inspect the source for `if` or `match` branches keyed on those parameters
3. list the discovered options in a reference file or table
4. call out branches that were not exercised in the notebook
5. avoid collapsing all behavior into the single notebook path

This is especially important for:

- `method`
- `backend`
- `mode`
- `provider`
- `source`
- `task`
- any parameter ending in `_method`, `_backend`, `_provider`, `_mode`, `_task`, `_type`, or `_model`

## OmicVerse-Style Heuristic

Model the branch scan after the capability-oriented naming heuristic used in `omicverse/_registry.py`:

- treat names like `method`, `backend`, and `mode` as likely capability selectors
- do not over-index on cosmetic names like `name`, `format`, or `kind`
- if source conditionals compare a branch-like parameter against literals, preserve those literals in the skill

## Failure Modes

Common failure cases that should block a "complete" skill:

- parameter list copied from a notebook without defaults
- docstring ignored even though it contains stronger constraints than the notebook
- `method` branches omitted because the notebook only used one option
- CLI flags undocumented because only the happy-path command was copied
- current function behavior inferred from stale tutorial prose instead of the live code
- inspection performed in the wrong Python environment, so the documented interface does not match the environment users actually run
