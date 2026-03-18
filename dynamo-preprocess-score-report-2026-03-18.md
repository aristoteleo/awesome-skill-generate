# Skill Score Report: dynamo-preprocess

- Verdict: pass
- Weighted score: 95/100
- Reviewed skill: `examples/generated-skills/dynamo-preprocess/`
- Report date: 2026-03-18

## Dimension Scores

- Trigger Precision: 5/5
- Execution Clarity: 5/5
- Validation Strength: 4/5
- Empirical Executability: 5/5
- Context Efficiency: 4/5
- Reusability: 5/5
- Resource Partitioning: 5/5
- Compatibility Robustness: 5/5
- Maintainability: 5/5

## Reviewed Files

- `examples/generated-skills/dynamo-preprocess/SKILL.md`
- `examples/generated-skills/dynamo-preprocess/references/recipe-selection.md`
- `examples/generated-skills/dynamo-preprocess/references/source-notebook-map.md`
- `examples/generated-skills/dynamo-preprocess/references/source-grounding.md`
- `examples/generated-skills/dynamo-preprocess/references/compatibility.md`
- `examples/generated-skills/dynamo-preprocess/assets/acceptance.json`
- `/Users/fernandozeng/Desktop/analysis/dynamo-release/docs/tutorials/notebooks/100_tutorial_preprocess.ipynb`
- `/Users/fernandozeng/Desktop/analysis/dynamo-release/dynamo/preprocessing/Preprocessor.py`

## Commands Run

```bash
python3 scripts/validate_skills.py --root examples
python3 scripts/run_skill_acceptance.py --root examples
python3 -m unittest discover -s tests -v
env MPLCONFIGDIR=/tmp/mpl NUMBA_CACHE_DIR=/tmp/numba /Users/fernandozeng/miniforge3/envs/omictest/bin/python - <<'PY'
import numpy as np
import anndata as ad
from dynamo.preprocessing import Preprocessor

X = np.random.poisson(2, (80, 200)).astype(float)
adata = ad.AnnData(X=X)
p = Preprocessor()
p.preprocess_adata(adata, recipe='pearson_residuals')
print('use_for_pca' in adata.var.columns)
print('X_pca' in adata.obsm.keys())
PY
env MPLCONFIGDIR=/tmp/mpl NUMBA_CACHE_DIR=/tmp/numba /Users/fernandozeng/miniforge3/envs/omictest/bin/python - <<'PY'
import dynamo as dyn
from dynamo.preprocessing import Preprocessor

adata = dyn.sample_data.zebrafish()
p = Preprocessor()
p.preprocess_adata(adata, recipe='monocle')
print('use_for_pca' in adata.var.columns)
print('X_pca' in adata.obsm.keys())
print('Size_Factor' in adata.obs.columns)
PY
env MPLCONFIGDIR=/tmp/mpl NUMBA_CACHE_DIR=/tmp/numba /Users/fernandozeng/miniforge3/envs/omictest/bin/python - <<'PY'
import dynamo as dyn
from dynamo.preprocessing import Preprocessor

adata = dyn.sample_data.zebrafish()
p = Preprocessor()
p.preprocess_adata(adata, recipe='pearson_residuals')
print('use_for_pca' in adata.var.columns)
print('X_pca' in adata.obsm.keys())
PY
env MPLCONFIGDIR=/tmp/mpl NUMBA_CACHE_DIR=/tmp/numba /Users/fernandozeng/miniforge3/envs/omictest/bin/python - <<'PY'
import inspect
from dynamo.preprocessing import Preprocessor
print('PREPROCESS_SIGNATURE', inspect.signature(Preprocessor.preprocess_adata))
for name in ['config_monocle_recipe','config_seurat_recipe','config_sctransform_recipe','config_pearson_residuals_recipe','config_monocle_pearson_residuals_recipe']:
    fn = getattr(Preprocessor, name)
    print(name, inspect.signature(fn))
PY
```

## Validation Results

- Command: `python3 scripts/validate_skills.py --root examples`
- Result: passed
- Key output: `Validated 1 generated example skill(s) successfully.`

- Command: `python3 scripts/run_skill_acceptance.py --root examples`
- Result: passed
- Key output: `All skill acceptance checks passed.`

- Command: `python3 -m unittest discover -s tests -v`
- Result: passed
- Key output:

```text
Ran 12 tests in 15.490s

OK
```

Relevant passing tests included:

- `test_example_generated_skill_acceptance_passes`
- `test_example_generated_skills_validate`
- `test_repository_acceptance_passes`
- `test_repository_validator_passes`

Empirical-executability results:

- Synthetic data run with `recipe='pearson_residuals'`: passed
- Notebook-adjacent zebrafish run with `recipe='monocle'`: passed
- Notebook-adjacent zebrafish run with `recipe='pearson_residuals'`: passed

Observed output evidence included:

- `use_for_pca == True`
- `X_pca` present in `adata.obsm`
- `Size_Factor` present in `adata.obs` for the monocle path
- expected summary changes logged by dynamo for both wrapper paths

## Interface Inspection Evidence

Inspection runtime:

- `/Users/fernandozeng/miniforge3/envs/omictest/bin/python`

Inspection environment:

- `MPLCONFIGDIR=/tmp/mpl`
- `NUMBA_CACHE_DIR=/tmp/numba`

Observed signature output:

```text
PREPROCESS_SIGNATURE (self, adata: anndata._core.anndata.AnnData, recipe: Literal['monocle', 'seurat', 'sctransform', 'pearson_residuals', 'monocle_pearson_residuals'] = 'monocle', tkey: Optional[str] = None, experiment_type: Optional[str] = None) -> None
config_monocle_recipe (self, adata: anndata._core.anndata.AnnData, n_top_genes: int = 2000) -> None
config_seurat_recipe (self, adata: anndata._core.anndata.AnnData) -> None
config_sctransform_recipe (self, adata: anndata._core.anndata.AnnData) -> None
config_pearson_residuals_recipe (self, adata: anndata._core.anndata.AnnData) -> None
config_monocle_pearson_residuals_recipe (self, adata: anndata._core.anndata.AnnData) -> None
```

Source branch evidence taken from `dynamo/preprocessing/Preprocessor.py`:

- `if recipe == "monocle"`
- `elif recipe == "seurat"`
- `elif recipe == "sctransform"`
- `elif recipe == "pearson_residuals"`
- `elif recipe == "monocle_pearson_residuals"`

Interpretation:

- `recipe` is the critical capability selector for this workflow.
- The notebook explicitly demonstrates four branches, but the live source exposes five.
- The generated skill correctly includes `monocle_pearson_residuals` instead of treating the notebook coverage as exhaustive.

## Scoring Rationale

- Trigger Precision: 5/5
  The frontmatter names the task, artifact type, major API, and all relevant recipe branches clearly enough for realistic user requests.

- Execution Clarity: 5/5
  The skill gives a default path, a customization path, and a stepwise debugging path, all ordered and grounded in the current API.

- Validation Strength: 4/5
  Validation is concrete and acceptance exists, but the smoke test still checks interface usability rather than a full preprocessing run on a real or fixture dataset.

- Empirical Executability: 5/5
  During scoring, the reviewer ran a synthetic Pearson-residual path and two notebook-adjacent zebrafish paths (`monocle` and `pearson_residuals`) in `omictest`, and confirmed expected outputs such as `use_for_pca`, `X_pca`, and `Size_Factor`.

- Context Efficiency: 4/5
  Core instructions stay in `SKILL.md` and supporting detail is split into references, but the domain-specific skill is still moderately dense because it needs branch and validation detail.

- Reusability: 5/5
  The skill is framed around the stable job of dynamo preprocessing rather than around a single notebook transcript.

- Resource Partitioning: 5/5
  Workflow, notebook mapping, source-grounding, compatibility, and acceptance are separated cleanly.

- Compatibility Robustness: 5/5
  The skill explicitly calls out `KDEpy`, current `Preprocessor` preference, the extra live-source branch, and the `omictest` runtime used for validation.

- Maintainability: 5/5
  The notebook map and source-grounding note make future updates traceable when the notebook or source changes.

## Key Findings

- The generated skill is grounded in the live `Preprocessor` API rather than notebook prose alone.
- The main branch selector is `recipe`, and the generated skill covers `monocle`, `seurat`, `sctransform`, `pearson_residuals`, and `monocle_pearson_residuals`.
- The skill includes explicit source-grounding and compatibility references, which materially improve trustworthiness.
- The acceptance contract and `omictest`-based smoke command make the generated skill more defensible than a pure document-only artifact.
- Reviewer-run empirical checks now show that the documented workflow is executable on both synthetic and notebook-adjacent data, so the skill clears the data-backed scoring gate.

## Recommended Revisions

- Consider adding `monocle_pearson_residuals` as an explicit empirical reviewer check in future score runs, since it is source-grounded but not notebook-demonstrated.
- If this skill will be reused broadly, consider adding one deterministic helper script for environment setup or recipe inspection.

## Residual Risks

- The scorer verified executability for `monocle` and `pearson_residuals`, but not every documented branch.
- `sctransform` still depends on `KDEpy` and was not executed in this review run.
- Future source changes to `Preprocessor` could add or remove recipe branches, so `source-grounding.md` should be refreshed when the upstream API changes.
