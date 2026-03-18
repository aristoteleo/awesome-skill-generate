# Source Grounding Audit

Use this reference when a skill documents real functions, methods, classes, or CLI entrypoints.

## Goal

Distinguish between:

- a skill that is grounded in the actual interface
- a skill that only paraphrases notebook usage or partial examples

## Audit Procedure

1. Identify the concrete callable or CLI that the skill depends on.
2. Inspect the real interface:
   - source code when available
   - `inspect.signature(...)`
   - `help(...)` / docstring
   - `-h` / `--help` for commands
3. Compare the actual interface against the skill text.
4. Check whether branch-like parameters such as `method`, `backend`, and `mode` were covered.
5. Downgrade the score when the skill overclaims completeness without source evidence.

## What To Reward

- signature and defaults agree with the live code
- parameter descriptions are more detailed than notebook examples because docstrings were consulted
- branch-like parameters include a nontrivial set of discovered values
- omitted branches are explicitly marked as not yet covered
- compatibility notes are based on real source drift, not speculation

## What To Penalize

- a notebook-derived skill that documents only the demonstrated branch
- parameter behavior inferred without checking source or help output
- silent omission of alternative `method` values
- missing mention of defaults that materially affect behavior
- unverified CLI flags copied from memory

## Suggested Evidence

When possible, cite or produce one of:

- output from `scripts/inspect_python_interface.py`
- a short source-derived branch table
- `help(...)` output summary
- command help output summary

If this evidence is absent, lower `Execution Clarity`, `Validation Strength`, and `Compatibility Robustness` unless the skill is clearly abstract and intentionally not interface-specific.
