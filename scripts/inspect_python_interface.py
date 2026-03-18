from __future__ import annotations

import argparse
import ast
import importlib
import inspect
import json
from pathlib import Path
from typing import Any


CAPABILITY_BRANCH_PARAMS = {
    "method",
    "recipe",
    "backend",
    "mode",
    "source",
    "task",
    "provider",
    "api_type",
    "model",
    "doublets_method",
    "correction_method",
    "prediction_mode",
    "classifier",
    "organism",
}

NON_CAPABILITY_BRANCH_PARAMS = {
    "name",
    "format",
    "key",
    "tag",
    "cmd",
    "kind",
    "platform",
    "cmap_name",
    "__name__",
    "file_type",
}

CAPABILITY_BRANCH_SUFFIXES = (
    "_method",
    "_backend",
    "_provider",
    "_source",
    "_classifier",
)

CAPABILITY_BRANCH_IMPORT_SUFFIXES = (
    "_mode",
    "_model",
    "_type",
    "_organism",
    "_task",
)
AST_MATCH = getattr(ast, "Match", None)


def is_branch_param_name(name: str) -> bool:
    lowered = name.lower()
    if lowered in NON_CAPABILITY_BRANCH_PARAMS:
        return False
    if lowered in CAPABILITY_BRANCH_PARAMS:
        return True
    if lowered.endswith(CAPABILITY_BRANCH_SUFFIXES):
        return True
    return lowered.endswith(CAPABILITY_BRANCH_IMPORT_SUFFIXES)


def resolve_target(target: str) -> Any:
    if ":" in target:
        module_name, qualname = target.split(":", 1)
        obj = importlib.import_module(module_name)
        for part in qualname.split("."):
            obj = getattr(obj, part)
        return obj

    parts = target.split(".")
    for index in range(len(parts), 0, -1):
        module_name = ".".join(parts[:index])
        try:
            obj = importlib.import_module(module_name)
        except Exception:
            continue
        for part in parts[index:]:
            obj = getattr(obj, part)
        return obj

    raise ValueError(f"Could not resolve target {target!r}")


def stringify_annotation(annotation: Any) -> str | None:
    if annotation is inspect.Signature.empty:
        return None
    if isinstance(annotation, type):
        return annotation.__name__
    return repr(annotation)


def stringify_default(default: Any) -> str | None:
    if default is inspect.Signature.empty:
        return None
    return repr(default)


def _is_section_header(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    title = lines[index].strip()
    underline = lines[index + 1].strip()
    return bool(title) and underline and set(underline) == {"-"} and len(underline) >= 3


def extract_parameter_docs(docstring: str) -> dict[str, str]:
    lines = docstring.splitlines()
    params: dict[str, str] = {}
    start_index = None

    for index, line in enumerate(lines):
        if line.strip().lower() == "parameters" and _is_section_header(lines, index):
            start_index = index + 2
            break

    if start_index is None:
        return params

    index = start_index
    while index < len(lines):
        if _is_section_header(lines, index):
            break

        line = lines[index]
        stripped = line.strip()
        if not stripped:
            index += 1
            continue

        if line.startswith(" ") or ":" not in stripped:
            index += 1
            continue

        names_part, _, type_part = stripped.partition(":")
        names = [name.strip() for name in names_part.split(",") if name.strip()]
        description_lines: list[str] = []
        if type_part.strip():
            description_lines.append(f"type: {type_part.strip()}")

        index += 1
        while index < len(lines):
            next_line = lines[index]
            if _is_section_header(lines, index):
                break
            next_stripped = next_line.strip()
            if next_stripped and not next_line.startswith(" ") and ":" in next_stripped:
                break
            if next_stripped:
                description_lines.append(next_stripped)
            index += 1

        description = " ".join(description_lines).strip()
        for name in names:
            params[name] = description

    return params


def _literal_values(node: ast.AST) -> set[str]:
    if isinstance(node, ast.Constant):
        return {str(node.value)}
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        values: set[str] = set()
        for element in node.elts:
            values.update(_literal_values(element))
        return values
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        values = _literal_values(node.operand)
        return {f"-{value}" for value in values}
    return set()


def _name_ids(node: ast.AST) -> set[str]:
    return {child.id for child in ast.walk(node) if isinstance(child, ast.Name)}


def _collect_compare_branches(compare: ast.Compare, branch_params: set[str], found: dict[str, set[str]]) -> None:
    involved_params = {name for name in _name_ids(compare) if name in branch_params}
    if not involved_params:
        return

    literal_values = _literal_values(compare.left)
    for comparator in compare.comparators:
        literal_values.update(_literal_values(comparator))

    if not literal_values:
        return

    for param in involved_params:
        found.setdefault(param, set()).update(literal_values)


def _collect_match_branches(match_node: ast.Match, branch_params: set[str], found: dict[str, set[str]]) -> None:
    if not isinstance(match_node.subject, ast.Name):
        return
    if match_node.subject.id not in branch_params:
        return

    values: set[str] = set()
    for case in match_node.cases:
        values.update(_match_case_values(case.pattern))

    if values:
        found.setdefault(match_node.subject.id, set()).update(values)


def _match_case_values(pattern: ast.pattern) -> set[str]:
    if isinstance(pattern, ast.MatchValue):
        return _literal_values(pattern.value)
    if isinstance(pattern, ast.MatchSingleton):
        return {str(pattern.value)}
    if isinstance(pattern, ast.MatchOr):
        values: set[str] = set()
        for subpattern in pattern.patterns:
            values.update(_match_case_values(subpattern))
        return values
    return set()


def detect_branch_params(func: Any) -> dict[str, list[str]]:
    try:
        source = inspect.getsource(func)
    except (OSError, TypeError):
        return {}

    try:
        tree = ast.parse(source)
    except SyntaxError:
        return {}

    branch_params = {
        name
        for name in inspect.signature(func).parameters
        if is_branch_param_name(name)
    }
    found: dict[str, set[str]] = {}

    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            _collect_compare_branches(node, branch_params, found)
        elif AST_MATCH is not None and isinstance(node, AST_MATCH):
            _collect_match_branches(node, branch_params, found)

    return {name: sorted(values) for name, values in sorted(found.items())}


def inspect_callable(func: Any) -> dict[str, Any]:
    signature = inspect.signature(func)
    docstring = inspect.getdoc(func) or ""
    parameter_docs = extract_parameter_docs(docstring)
    branch_params = detect_branch_params(func)

    parameters = []
    for name, param in signature.parameters.items():
        parameters.append(
            {
                "name": name,
                "kind": str(param.kind),
                "annotation": stringify_annotation(param.annotation),
                "default": stringify_default(param.default),
                "is_branch_param": is_branch_param_name(name),
                "doc": parameter_docs.get(name),
                "detected_branch_values": branch_params.get(name, []),
            }
        )

    try:
        source_file = inspect.getsourcefile(func)
        source = inspect.getsource(func)
    except (OSError, TypeError):
        source_file = None
        source = None

    return {
        "module": getattr(func, "__module__", None),
        "qualname": getattr(func, "__qualname__", None),
        "signature": str(signature),
        "docstring": docstring,
        "parameter_docs": parameter_docs,
        "parameters": parameters,
        "branch_params": branch_params,
        "source_file": source_file,
        "source_available": source is not None,
    }


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Inspect a Python callable and emit a source-grounded summary of its signature, "
            "docstring-derived parameter docs, and branch-like method/backend/mode options."
        )
    )
    parser.add_argument("target", help="Import target in 'package.module:callable' or dotted form")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    target = resolve_target(args.target)
    if not callable(target):
        raise TypeError(f"Target {args.target!r} is not callable")

    payload = inspect_callable(target)
    indent = 2 if args.pretty else None
    print(json.dumps(payload, indent=indent, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
