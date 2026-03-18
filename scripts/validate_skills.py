from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_SKILLS_DIR = REPO_ROOT / "skills"
EXAMPLE_GENERATED_SKILLS_DIR = REPO_ROOT / "examples" / "generated-skills"
ALLOWED_TOP_LEVEL_NAMES = {"SKILL.md", "references", "scripts", "assets"}
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
RELATIVE_PATH_RE = re.compile(
    r"`((?:references|scripts|assets)/[^`\s]+(?:\.[^`\s]+)?)`",
    re.IGNORECASE,
)
RESOURCE_LINE_RE = re.compile(r"^(?:- )?(?:Read|Run)\b", re.IGNORECASE)


@dataclass(frozen=True)
class Skill:
    folder: Path
    skill_md: Path
    frontmatter: dict[str, str]
    body: str

    @property
    def name(self) -> str:
        return self.frontmatter["name"]

    @property
    def description(self) -> str:
        return self.frontmatter["description"]


def discover_skill_dirs(root: Path | None = None) -> list[Path]:
    skill_root = PACKAGE_SKILLS_DIR if root is None else root
    if not skill_root.exists():
        return []
    return sorted(path for path in skill_root.iterdir() if path.is_dir())


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise ValueError("missing YAML frontmatter block")

    raw_frontmatter = match.group(1)
    frontmatter: dict[str, str] = {}
    for raw_line in raw_frontmatter.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {raw_line!r}")
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = value.strip()

    body = text[match.end() :].lstrip("\n")
    return frontmatter, body


def load_skill(skill_dir: Path) -> Skill:
    skill_md = skill_dir / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    return Skill(folder=skill_dir, skill_md=skill_md, frontmatter=frontmatter, body=body)


def load_skills(root: Path | None = None) -> list[Skill]:
    return [load_skill(skill_dir) for skill_dir in discover_skill_dirs(root=root)]


def strip_fenced_code_blocks(markdown_text: str) -> str:
    lines: list[str] = []
    in_fence = False
    for line in markdown_text.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            lines.append(line)
    return "\n".join(lines)


def collect_relative_paths(markdown_text: str) -> set[str]:
    stripped_text = strip_fenced_code_blocks(markdown_text)
    referenced_paths: set[str] = set()
    for line in stripped_text.splitlines():
        if not RESOURCE_LINE_RE.match(line.strip()):
            continue
        referenced_paths.update(match.group(1) for match in RELATIVE_PATH_RE.finditer(line))
    return referenced_paths


def validate_skill(skill: Skill) -> list[str]:
    errors: list[str] = []
    expected_name = skill.folder.name
    actual_keys = set(skill.frontmatter)

    if actual_keys != {"name", "description"}:
        errors.append(
            f"{skill.folder.name}: frontmatter keys must be exactly "
            f"['description', 'name'], found {sorted(actual_keys)}"
        )

    if skill.name != expected_name:
        errors.append(
            f"{skill.folder.name}: frontmatter name {skill.name!r} does not match folder name {expected_name!r}"
        )

    if not skill.description:
        errors.append(f"{skill.folder.name}: description must not be empty")
    elif "use when" not in skill.description.lower():
        errors.append(f"{skill.folder.name}: description should include trigger language such as 'Use when'")

    if not skill.body.strip():
        errors.append(f"{skill.folder.name}: SKILL.md body must not be empty")

    top_level_names = {path.name for path in skill.folder.iterdir()}
    disallowed_names = sorted(name for name in top_level_names if name not in ALLOWED_TOP_LEVEL_NAMES)
    if disallowed_names:
        errors.append(
            f"{skill.folder.name}: unexpected top-level files or directories: {', '.join(disallowed_names)}"
        )

    referenced_paths = collect_relative_paths(skill.skill_md.read_text(encoding="utf-8"))
    for relative_path in sorted(referenced_paths):
        if not (skill.folder / relative_path).exists():
            errors.append(f"{skill.folder.name}: referenced path does not exist: {relative_path}")

    return errors


def validate_skill_root(root: Path, *, label: str) -> list[str]:
    errors: list[str] = []
    skill_dirs = discover_skill_dirs(root=root)

    if not skill_dirs:
        return [f"{label}: no skill directories found under {root.relative_to(REPO_ROOT)}/"]

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"{skill_dir.name}: missing SKILL.md")
            continue
        try:
            skill = load_skill(skill_dir)
        except ValueError as exc:
            errors.append(f"{skill_dir.name}: {exc}")
            continue
        errors.extend(validate_skill(skill))

    return errors


def validate_repository() -> list[str]:
    return validate_skill_root(PACKAGE_SKILLS_DIR, label="package-skills")


def validate_example_generated_skills() -> list[str]:
    return validate_skill_root(EXAMPLE_GENERATED_SKILLS_DIR, label="generated-skill-examples")


def build_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate package skills and generated skill examples.")
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
        errors = validate_repository()
        count = len(discover_skill_dirs())
        label = "package skill"
    elif args.root == "examples":
        errors = validate_example_generated_skills()
        count = len(discover_skill_dirs(root=EXAMPLE_GENERATED_SKILLS_DIR))
        label = "generated example skill"
    else:
        errors = validate_repository() + validate_example_generated_skills()
        count = len(discover_skill_dirs()) + len(discover_skill_dirs(root=EXAMPLE_GENERATED_SKILLS_DIR))
        label = "skill"

    if errors:
        print("Skill validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {count} {label}(s) successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
