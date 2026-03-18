from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import inspect_python_interface


def sample_dispatch(
    adata,
    method: str = "monocle",
    recipe: str = "default",
    backend: str = "cpu",
    kind: str = "scatter",
):
    """
    Example dispatcher.

    Parameters
    ----------
    adata : AnnData
        Input matrix.
    method : str, default "monocle"
        Processing method to use.
    recipe : str, default "default"
        Recipe name to use.
    backend : str, default "cpu"
        Execution backend.
    kind : str, default "scatter"
        Plot kind.
    """
    if method == "monocle":
        return "monocle"
    if method in {"pearson_residuals", "seurat"}:
        return "alt"
    if recipe in {"default", "strict"}:
        return recipe
    if backend == "cpu":
        return "cpu"
    if backend == "gpu":
        return "gpu"
    return kind


class InterfaceInspectionTests(unittest.TestCase):
    def test_extract_parameter_docs(self) -> None:
        docs = inspect_python_interface.extract_parameter_docs(inspect_python_interface.inspect_callable(sample_dispatch)["docstring"])
        self.assertIn("method", docs)
        self.assertIn("Processing method", docs["method"])
        self.assertIn("backend", docs)

    def test_detect_branch_params(self) -> None:
        branch_params = inspect_python_interface.detect_branch_params(sample_dispatch)
        self.assertEqual(branch_params["method"], ["monocle", "pearson_residuals", "seurat"])
        self.assertEqual(branch_params["recipe"], ["default", "strict"])
        self.assertEqual(branch_params["backend"], ["cpu", "gpu"])
        self.assertNotIn("kind", branch_params)

    def test_inspect_callable_marks_branch_params(self) -> None:
        payload = inspect_python_interface.inspect_callable(sample_dispatch)
        params = {entry["name"]: entry for entry in payload["parameters"]}
        self.assertTrue(params["method"]["is_branch_param"])
        self.assertTrue(params["recipe"]["is_branch_param"])
        self.assertTrue(params["backend"]["is_branch_param"])
        self.assertFalse(params["kind"]["is_branch_param"])
        self.assertEqual(params["method"]["detected_branch_values"], ["monocle", "pearson_residuals", "seurat"])
        self.assertEqual(params["recipe"]["detected_branch_values"], ["default", "strict"])
        self.assertIn("method", payload["signature"])
        self.assertIn("'monocle'", payload["signature"])
        self.assertIn("backend", payload["signature"])


if __name__ == "__main__":
    unittest.main()
