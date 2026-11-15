#!/usr/bin/env python3
"""Collection checks: names, descriptions, and the old board stays out of delivery."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
OLD = ("BUGS.md", "WAVES.md", "FEATURES.md")


def frontmatter(text):
    if not text.startswith("---"):
        raise AssertionError("missing frontmatter")
    end = text.find("\n---", 3)
    block = text[3:end]
    data = {}
    for line in block.splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


class SkillCollectionTest(unittest.TestCase):
    def test_every_skill_has_a_matching_name_and_a_short_description(self):
        found = list(SKILLS.glob("*/SKILL.md"))
        self.assertGreaterEqual(len(found), 16)
        for path in found:
            data = frontmatter(path.read_text(encoding="utf-8"))
            self.assertEqual(data["name"], path.parent.name)
            self.assertLessEqual(len(data["description"]), 1024)
            self.assertGreater(len(data["description"]), 40)

    def test_github_pipeline_does_not_require_the_old_board(self):
        text = (SKILLS / "github-pipeline" / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("Required files", text)
        self.assertNotIn("are the backlog", text)
        self.assertNotIn("AGENTS.md", text)
        for name in OLD:
            self.assertEqual(text.count(name), 1)

    def test_only_migrate_docs_tells_the_agent_to_read_the_old_board(self):
        migrate = (SKILLS / "migrate-docs" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("only skill that reads", migrate)
        for path in SKILLS.glob("*/SKILL.md"):
            if path.parent.name == "migrate-docs":
                continue
            text = path.read_text(encoding="utf-8")
            self.assertIn("Name `migrate-docs`", text)
            if path.parent.name != "record":
                self.assertIn("Invoke `record`", text)
            self.assertNotIn("Cursor", text)
            self.assertNotIn(".agents/", text)

    def test_make_reaches_the_toon_target(self):
        index = (SKILLS / "record" / "index.mk").read_text(encoding="utf-8")
        self.assertIn("toon:", index)
        self.assertIn("$(PYTHON)", index)
        runner = (SKILLS / "project-setup" / "podman-python.mk").read_text(encoding="utf-8")
        self.assertIn("podman run", runner)
        self.assertIn("PYTHON_IMAGE", runner)
        gradle = (SKILLS / "github-pipeline" / "templates" / "Makefile.gradle").read_text(encoding="utf-8")
        self.assertIn("$(PYTHON) scripts/render-docs.py", gradle)
        self.assertNotIn("python3 scripts/render-docs.py", gradle)
        for makefile in (
            SKILLS / "project-setup" / "project.mk",
            SKILLS / "github-pipeline" / "sdlc.mk",
        ):
            self.assertIn("-include .claude/skills/record/index.mk", makefile.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
