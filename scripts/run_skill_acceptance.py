from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path

import validate_skills


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_acceptance_case(skill: validate_skills.Skill) -> dict:
    acceptance_path = skill.folder / "assets" / "acceptance.json"
    if not acceptance_path.exists():
        raise ValueError(f"{skill.folder.name}: missing assets/acceptance.json")
    with acceptance_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def _lower_items(items: list[str]) -> list[str]:
    return [item.lower() for item in items]


def validate_acceptance_case(skill: validate_skills.Skill, case: dict) -> list[str]:
    errors: list[str] = []
    skill_text = skill.skill_md.read_text(encoding="utf-8")
    body_lower = skill.body.lower()
    description_lower = skill.description.lower()

    if case.get("version") != 1:
        errors.append(f"{skill.folder.name}: acceptance version must be 1")

    if case.get("skill") != skill.folder.name:
        errors.append(
            f"{skill.folder.name}: acceptance skill value {case.get('skill')!r} does not match folder name"
        )

    sample_requests = case.get("sample_requests")
    if not isinstance(sample_requests, list) or not sample_requests:
        errors.append(f"{skill.folder.name}: acceptance file must include non-empty sample_requests")

    for term in _lower_items(case.get("required_description_terms", [])):
        if term not in description_lower:
            errors.append(f"{skill.folder.name}: description is missing required term {term!r}")

    for section in case.get("required_sections", []):
        if section not in skill_text:
            errors.append(f"{skill.folder.name}: SKILL.md is missing required section {section!r}")

    for term in _lower_items(case.get("required_body_terms", [])):
        if term not in body_lower:
            errors.append(f"{skill.folder.name}: body is missing required term {term!r}")

    for relative_path in case.get("required_paths", []):
        if not (skill.folder / relative_path).exists():
            errors.append(f"{skill.folder.name}: acceptance required path does not exist: {relative_path}")

    return errors


def run_smoke_commands(skill: validate_skills.Skill, case: dict) -> list[str]:
    errors: list[str] = []
    for smoke in case.get("smoke_commands", []):
        name = smoke.get("name", "unnamed-smoke")
        command = smoke.get("command")
        if not command:
            errors.append(f"{skill.folder.name}: smoke command {name!r} is missing a command")
            continue

        env_prefix = ""
        smoke_env = smoke.get("env", {})
        if smoke_env:
            assignments = " ".join(
                f"{key}={shlex.quote(str(value))}" for key, value in sorted(smoke_env.items())
            )
            env_prefix = f"env {assignments} "

        python_path = smoke.get("python_path")
        conda_env = smoke.get("conda_env")
        if python_path:
            command = command.replace("${PYTHON}", shlex.quote(str(python_path)))
            command = f"{env_prefix}{command}"
        elif conda_env:
            command = command.replace("${PYTHON}", "python")
            command = f"{env_prefix}conda run -n {shlex.quote(str(conda_env))} {command}"
        else:
            command = command.replace("${PYTHON}", sys.executable)
            command = f"{env_prefix}{command}"

        completed = subprocess.run(
            ["/bin/zsh", "-lc", command],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=smoke.get("timeout_seconds", 60),
        )
        stdout = completed.stdout
        stderr = completed.stderr
        combined = stdout + "\n" + stderr

        if completed.returncode != 0:
            errors.append(
                f"{skill.folder.name}: smoke command {name!r} failed with exit code {completed.returncode}\n"
                f"{combined.strip()}"
            )
            continue

        for needle in smoke.get("expect_stdout_contains", []):
            if needle not in stdout:
                errors.append(
                    f"{skill.folder.name}: smoke command {name!r} missing expected stdout fragment {needle!r}"
                )

        for needle in smoke.get("expect_stderr_contains", []):
            if needle not in stderr:
                errors.append(
                    f"{skill.folder.name}: smoke command {name!r} missing expected stderr fragment {needle!r}"
                )

    return errors


def validate_skill_root_acceptance(root: Path) -> list[str]:
    errors: list[str] = []
    for skill in validate_skills.load_skills(root=root):
        try:
            case = load_acceptance_case(skill)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        errors.extend(validate_acceptance_case(skill, case))
        if not errors or not any(error.startswith(f"{skill.folder.name}:") for error in errors):
            errors.extend(run_smoke_commands(skill, case))

    return errors


def validate_repository_acceptance() -> list[str]:
    return validate_skill_root_acceptance(validate_skills.PACKAGE_SKILLS_DIR)


def validate_example_generated_skill_acceptance() -> list[str]:
    return validate_skill_root_acceptance(validate_skills.EXAMPLE_GENERATED_SKILLS_DIR)


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run acceptance checks for package skills and generated examples.")
    parser.add_argument(
        "--root",
        choices=("package", "examples", "all"),
        default="package",
        help="Which skill tree to validate.",
    )
    return parser


def main() -> int:
    args = build_argument_parser().parse_args()
    if args.root == "package":
        errors = validate_repository_acceptance()
    elif args.root == "examples":
        errors = validate_example_generated_skill_acceptance()
    else:
        errors = validate_repository_acceptance() + validate_example_generated_skill_acceptance()

    if errors:
        print("Skill acceptance failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("All skill acceptance checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
