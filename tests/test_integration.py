#!/usr/bin/env python3
"""One integration entry: each requirement is still said by a skill."""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"


def requirement_rows(text):
    found = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [part.strip() for part in stripped.strip("|").split("|")]
        if len(cells) < 2 or not cells[0].startswith("R-"):
            continue
        if not cells[0][2:].isdigit():
            continue
        found.append((cells[0], cells[1]))
    return found


class RequirementWordingTest(unittest.TestCase):
    def test_a_skill_still_says_each_requirement(self):
        """id: R-1"""
        rows = requirement_rows(
            (ROOT / "docs" / "REQUIREMENTS.md").read_text(encoding="utf-8")
        )
        self.assertGreaterEqual(len(rows), 15)
        blob = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SKILLS.rglob("*")
            if path.suffix in {".md", ".mk"}
        )
        missing = [ident for ident, statement in rows if statement not in blob]
        self.assertEqual(missing, [])
