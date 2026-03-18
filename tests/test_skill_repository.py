from __future__ import annotations

import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import validate_skills
import run_skill_acceptance


class SkillRepositoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill_dirs = validate_skills.discover_skill_dirs()
        cls.skills = validate_skills.load_skills()
        cls.example_skill_dirs = validate_skills.discover_skill_dirs(
            root=validate_skills.EXAMPLE_GENERATED_SKILLS_DIR
        )
        cls.example_skills = validate_skills.load_skills(
            root=validate_skills.EXAMPLE_GENERATED_SKILLS_DIR
        )

    def test_skills_directory_is_not_empty(self) -> None:
        self.assertTrue(self.skill_dirs, "expected at least one skill directory under skills/")

    def test_each_skill_has_expected_frontmatter(self) -> None:
        for skill in self.skills:
            with self.subTest(skill=skill.folder.name):
                self.assertEqual(set(skill.frontmatter), {"name", "description"})
                self.assertEqual(skill.name, skill.folder.name)
                self.assertTrue(skill.description)
                self.assertIn("use when", skill.description.lower())

    def test_each_skill_has_only_allowed_top_level_entries(self) -> None:
        for skill in self.skills:
            with self.subTest(skill=skill.folder.name):
                names = {path.name for path in skill.folder.iterdir()}
                unexpected = names - validate_skills.ALLOWED_TOP_LEVEL_NAMES
                self.assertFalse(
                    unexpected,
                    f"unexpected top-level files or directories: {sorted(unexpected)}",
                )

    def test_all_internal_references_exist(self) -> None:
        for skill in self.skills:
            with self.subTest(skill=skill.folder.name):
                referenced_paths = validate_skills.collect_relative_paths(
                    skill.skill_md.read_text(encoding="utf-8")
                )
                for relative_path in sorted(referenced_paths):
                    self.assertTrue(
                        (skill.folder / relative_path).exists(),
                        f"missing referenced path: {relative_path}",
                    )

    def test_repository_validator_passes(self) -> None:
        self.assertEqual(validate_skills.validate_repository(), [])

    def test_repository_acceptance_passes(self) -> None:
        self.assertEqual(run_skill_acceptance.validate_repository_acceptance(), [])

    def test_example_generated_skills_exist(self) -> None:
        self.assertTrue(
            self.example_skill_dirs,
            "expected at least one generated example skill under examples/generated-skills/",
        )

    def test_example_generated_skills_validate(self) -> None:
        self.assertEqual(validate_skills.validate_example_generated_skills(), [])

    def test_example_generated_skill_acceptance_passes(self) -> None:
        self.assertEqual(run_skill_acceptance.validate_example_generated_skill_acceptance(), [])


if __name__ == "__main__":
    unittest.main()
