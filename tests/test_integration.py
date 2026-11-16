#!/usr/bin/env python3
"""One integration entry: the Make contract and the language tools together."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class QualityContractTest(unittest.TestCase):
    def test_make_targets_use_the_existing_tools(self):
        """id: ADR-0009"""
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        project = (ROOT / "skills" / "project-setup" / "project.mk").read_text(
            encoding="utf-8"
        )
        review = (ROOT / "skills" / "review" / "SKILL.md").read_text(encoding="utf-8")
        editorconfig = (ROOT / ".editorconfig").read_text(encoding="utf-8")
        template = (
            ROOT / "skills" / "project-setup" / "templates" / "editorconfig"
        ).read_text(encoding="utf-8")
        self.assertEqual(editorconfig, template)
        for name in ("editorconfig:", "format:", "lint:", "integration:", "coverage:"):
            self.assertIn(name, project)
        for name in (
            "FORMAT_CMD",
            "LINT_CMD",
            "INTEGRATION_CMD",
            "COVERAGE_CMD",
            "RUFF_IMAGE",
        ):
            self.assertIn(name, makefile)
        self.assertIn("pattern Plan named", review)
        self.assertIn("build/coverage/diff.md", review)
