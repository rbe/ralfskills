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
        """id: R-4"""
        found = list(SKILLS.glob("*/SKILL.md"))
        self.assertGreaterEqual(len(found), 16)
        for path in found:
            data = frontmatter(path.read_text(encoding="utf-8"))
            self.assertEqual(data["name"], path.parent.name)
            self.assertLessEqual(len(data["description"]), 1024)
            self.assertGreater(len(data["description"]), 40)

    def test_github_pipeline_does_not_require_the_old_board(self):
        """id: R-5"""
        text = (SKILLS / "github-pipeline" / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("Required files", text)
        self.assertNotIn("are the backlog", text)
        self.assertNotIn("AGENTS.md", text)
        for name in OLD:
            self.assertEqual(text.count(name), 1)

    def test_only_migrate_docs_tells_the_agent_to_read_the_old_board(self):
        """id: R-5"""
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
        """id: R-6"""
        index = (SKILLS / "record" / "index.mk").read_text(encoding="utf-8")
        self.assertIn("toon:", index)
        self.assertIn("$(PYTHON)", index)
        runner = (SKILLS / "project-setup" / "podman-python.mk").read_text(
            encoding="utf-8"
        )
        self.assertIn("podman run", runner)
        self.assertIn("PYTHON_IMAGE", runner)
        gradle = (
            SKILLS / "github-pipeline" / "templates" / "Makefile.gradle"
        ).read_text(encoding="utf-8")
        self.assertIn("$(PYTHON) scripts/render-docs.py", gradle)
        self.assertNotIn("python3 scripts/render-docs.py", gradle)
        for makefile in (
            SKILLS / "project-setup" / "project.mk",
            SKILLS / "github-pipeline" / "sdlc.mk",
        ):
            self.assertIn(
                "-include .claude/skills/record/index.mk",
                makefile.read_text(encoding="utf-8"),
            )
        record = (SKILLS / "record" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn(
            "`make toon` writes the ADR index and the skill index through `$(PYTHON)`.",
            record,
        )
        self.assertIn("docs/adr/index.toon", record)
        self.assertIn("docs/requirements-index.toon", record)
        self.assertIn("does not create `docs/adr/`", record)

    def test_plan_names_the_boundary_and_the_pattern(self):
        """id: R-7"""
        text = (SKILLS / "plan" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("who owns state", text)
        self.assertIn("what may call what", text)
        review = (SKILLS / "review" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("pattern Plan named", review)

    def test_plan_waits_when_a_choice_is_expensive_to_reverse(self):
        """id: R-14"""
        text = (SKILLS / "plan" / "SKILL.md").read_text(encoding="utf-8")
        step = (
            "Evaluate architecture, scalability, and code quality against the "
            "constraints of this system. Prefer the smallest design that stays "
            "operable and maintainable. When a choice is expensive to reverse, "
            "name the options, recommend one, and wait. Otherwise implement it "
            "in small modules."
        )
        work = text.split("## Work", 1)[1]
        lines = [
            line
            for line in work.splitlines()
            if line[:1].isdigit() and ". " in line[:4]
        ]
        boundary = next(
            index for index, line in enumerate(lines) if "who owns state" in line
        )
        self.assertEqual(text.count(step), 1)
        self.assertIn(step, lines[boundary + 1])

    def test_develop_stops_until_lint_and_test_pass(self):
        """id: R-8"""
        text = (SKILLS / "develop" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("`make lint` and `make test`", text)
        self.assertIn("Do not write a linter.", text)
        self.assertIn("one integration entry", text)

    def test_linters_are_existing_tools(self):
        """id: R-9"""
        node = (SKILLS / "node" / "SKILL.md").read_text(encoding="utf-8")
        python = (SKILLS / "python" / "SKILL.md").read_text(encoding="utf-8")
        shell = (SKILLS / "shell" / "SKILL.md").read_text(encoding="utf-8")
        java = (SKILLS / "jvm" / "references" / "java.md").read_text(encoding="utf-8")
        self.assertIn("ESLint", node)
        self.assertIn("Prettier", node)
        self.assertIn("Ruff", python)
        self.assertIn("shellcheck", shell)
        self.assertIn("shfmt", shell)
        self.assertIn("Checkstyle", java)
        self.assertIn("google-java-format", java)
        self.assertFalse((SKILLS / "project-setup" / "scripts").exists())

    def test_api_design_covers_a_module_export(self):
        """id: R-10"""
        text = (SKILLS / "api-design" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("What is exported?", text)
        self.assertIn("What stays internal?", text)
        self.assertIn(
            "What is the resource, the verb, and the status on success?", text
        )

    def test_make_with_no_arguments_is_help(self):
        """id: R-11"""
        files = [
            ROOT / "Makefile",
            SKILLS / "project-setup" / "project.mk",
            SKILLS / "project-setup" / "podman-python.mk",
            SKILLS / "project-setup" / "tools.mk",
            SKILLS / "github-pipeline" / "sdlc.mk",
            SKILLS / "record" / "index.mk",
        ]
        for path in files:
            text = path.read_text(encoding="utf-8")
            self.assertIn(".DEFAULT_GOAL := help", text)
            self.assertNotIn(".DEFAULT_GOAL := test", text)

    def test_coverage_is_the_diff_report(self):
        """id: R-12"""
        text = (SKILLS / "project-setup" / "SKILL.md").read_text(encoding="utf-8")
        tools = (SKILLS / "project-setup" / "tools.mk").read_text(encoding="utf-8")
        self.assertIn("diff-cover", text)
        self.assertIn("repository-wide percentage", text)
        self.assertIn("diff-cover==", tools)
        self.assertIn("editorconfig-checker", tools)
        review = (SKILLS / "review" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("build/coverage/diff.md", review)

    def test_a_product_repository_keeps_a_roadmap_and_adrs(self):
        """id: R-15"""
        record = (SKILLS / "record" / "SKILL.md").read_text(encoding="utf-8")
        plan = (SKILLS / "plan" / "SKILL.md").read_text(encoding="utf-8")
        migrate = (SKILLS / "migrate-docs" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("docs/ROADMAP.md", record)
        self.assertIn("docs/adr/", record)
        self.assertIn("docs/DECISIONS.md", record)
        self.assertIn("docs/ROADMAP.md", plan)
        self.assertIn("docs/adr/index.toon", plan)
        self.assertIn("`docs/adr/`", migrate)
        self.assertIn("`docs/ROADMAP.md`", migrate)


if __name__ == "__main__":
    unittest.main()
