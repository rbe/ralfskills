#!/usr/bin/env python3
"""Tests for the id check and the ADR index."""

import importlib.util
import tempfile
import unittest
from pathlib import Path


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


HERE = Path(__file__).resolve().parent
ids = load("ids", HERE / "ids.py")
adr_index = load("adr_index", HERE / "adr_index.py")


class IdsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "docs" / "adr").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_duplicate_id_fails(self):
        body = "---\nid: D-1\nstatus: open\n---\n\n# One\n"
        self.write("docs/DECISIONS.md", body)
        self.write("docs/proposals/P-1.md", "---\nid: D-1\nstatus: open\n---\n")
        errors = ids.check(self.root)
        self.assertTrue(any("D-1" in error for error in errors))

    def test_retired_id_still_in_use_fails(self):
        self.write("docs/ids.yaml", "retired:\n- D-1\n")
        self.write("docs/DECISIONS.md", "---\nid: D-1\nstatus: decided\n---\n")
        errors = ids.check(self.root)
        self.assertTrue(any("retired" in error for error in errors))

    def test_retire_moves_an_unused_id(self):
        self.write("docs/ids.yaml", "retired: []\n")
        errors = ids.retire(self.root, "H-2026-11-15-old")
        self.assertEqual(errors, [])
        self.assertIn("H-2026-11-15-old", ids.retired_ids(self.root / "docs" / "ids.yaml"))
        self.assertEqual(ids.check(self.root), [])

    def test_retire_rejects_a_live_id(self):
        self.write("docs/history/H-1.md", "---\nid: H-1\n---\n")
        errors = ids.retire(self.root, "H-1")
        self.assertTrue(errors)


class AdrIndexTest(unittest.TestCase):
    def test_index_lists_adr_links_and_not_skill_prose(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            adr = root / "docs" / "adr"
            adr.mkdir(parents=True)
            (adr / "ADR-0004.md").write_text(
                "---\nid: ADR-0004\ntitle: Listen on localhost\nstatus: Accepted\n"
                "adrs: [ADR-0001]\nskills: [security, review]\ndecisions: [D-12]\n---\n\n# Body\n",
                encoding="utf-8",
            )
            text = adr_index.render(adr_index.rows(adr))
            self.assertIn("adr_index[1]{id,status,title,adrs,skills,decisions}:", text)
            self.assertIn("ADR-0004,Accepted,Listen on localhost,ADR-0001,security;review,D-12", text)
            self.assertNotIn("Body", text)


if __name__ == "__main__":
    unittest.main()
