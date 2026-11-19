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
        """id: R-13"""
        body = "---\nid: D-1\nstatus: open\n---\n\n# One\n"
        self.write("docs/DECISIONS.md", body)
        self.write("docs/proposals/P-1.md", "---\nid: D-1\nstatus: open\n---\n")
        errors = ids.check(self.root)
        self.assertTrue(any("D-1" in error for error in errors))

    def test_retired_id_still_in_use_fails(self):
        """id: R-13"""
        self.write("docs/ids.yaml", "retired:\n- D-1\n")
        self.write("docs/DECISIONS.md", "---\nid: D-1\nstatus: decided\n---\n")
        errors = ids.check(self.root)
        self.assertTrue(any("retired" in error for error in errors))

    def test_retire_moves_an_unused_id(self):
        """id: R-13"""
        self.write("docs/ids.yaml", "retired: []\n")
        errors = ids.retire(self.root, "H-2026-11-15-old")
        self.assertEqual(errors, [])
        self.assertIn(
            "H-2026-11-15-old", ids.retired_ids(self.root / "docs" / "ids.yaml")
        )
        self.assertEqual(ids.check(self.root), [])

    def test_retire_rejects_a_live_id(self):
        """id: R-13"""
        self.write("docs/history/H-1.md", "---\nid: H-1\n---\n")
        errors = ids.retire(self.root, "H-1")
        self.assertTrue(errors)


skill_index = load("skill_index", HERE / "skill_index.py")


class SkillIndexTest(unittest.TestCase):
    def test_rows_come_from_kind_and_installed_skills_win(self):
        """id: R-6"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bundled = root / "skills" / "jvm"
            bundled.mkdir(parents=True)
            (bundled / "SKILL.md").write_text(
                "---\nname: jvm\nkind: language\nfiles: [java]\n---\n", encoding="utf-8"
            )
            installed = root / ".claude" / "skills" / "node"
            installed.mkdir(parents=True)
            (installed / "SKILL.md").write_text(
                "---\nname: node\nkind: language\nfiles: [js, ts]\n---\n",
                encoding="utf-8",
            )
            check = root / ".claude" / "skills" / "security"
            check.mkdir(parents=True)
            (check / "SKILL.md").write_text(
                "---\nname: security\nkind: check\norder: 10\n---\n", encoding="utf-8"
            )
            plain = root / ".claude" / "skills" / "plan"
            plain.mkdir(parents=True)
            (plain / "SKILL.md").write_text(
                "---\nname: plan\ndescription: Grill.\n---\n", encoding="utf-8"
            )
            found = skill_index.rows(root)
            self.assertEqual([row["name"] for row in found], ["security", "node"])
            text = skill_index.render(found)
            self.assertIn("skill_index[2]{name,kind,order,files,names}:", text)
            self.assertIn("security,check,10,,", text)
            self.assertIn("node,language,,js;ts,", text)
            self.assertNotIn("jvm", text)
            self.assertNotIn("Grill", text)


class AdrIndexTest(unittest.TestCase):
    def test_index_lists_adr_links_and_not_skill_prose(self):
        """id: R-6"""
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
            self.assertIn(
                "ADR-0004,Accepted,Listen on localhost,ADR-0001,security;review,D-12",
                text,
            )
            self.assertNotIn("Body", text)


toon = load("toon", HERE / "toon.py")


class IndexTargetTest(unittest.TestCase):
    def test_a_requirements_list_is_indexed_without_an_adr_directory(self):
        """id: R-6"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "REQUIREMENTS.md").write_text(
                "| Id | Statement |\n| --- | --- |\n| R-1 | One, two. |\n",
                encoding="utf-8",
            )
            toon.write_indexes(root)
            text = (docs / "requirements-index.toon").read_text(encoding="utf-8")
            self.assertIn("requirements[1]{id,statement}:", text)
            self.assertIn('R-1,"One, two."', text)
            self.assertFalse((docs / "adr").exists())
            self.assertTrue((docs / "skill-index.toon").is_file())

    def test_a_product_repository_still_gets_an_adr_index(self):
        """id: R-6"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            toon.write_indexes(root)
            index = root / "docs" / "adr" / "index.toon"
            self.assertTrue(index.is_file())
            self.assertIn("adr_index[0]", index.read_text(encoding="utf-8"))
            self.assertFalse((root / "docs" / "requirements-index.toon").exists())

    def test_adr_files_keep_the_adr_index_when_a_requirements_list_is_also_present(
        self,
    ):
        """id: R-6"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            adr = root / "docs" / "adr"
            adr.mkdir(parents=True)
            (adr / "ADR-0004.md").write_text(
                "---\nid: ADR-0004\ntitle: Listen\nstatus: Accepted\n---\n",
                encoding="utf-8",
            )
            (root / "docs" / "REQUIREMENTS.md").write_text(
                "| Id | Statement |\n| --- | --- |\n| R-1 | One. |\n",
                encoding="utf-8",
            )
            toon.write_indexes(root)
            text = (adr / "index.toon").read_text(encoding="utf-8")
            self.assertIn("ADR-0004,Accepted,Listen,,,", text)
            self.assertFalse((root / "docs" / "requirements-index.toon").exists())


class TableIdTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "docs").mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, relative, text):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def test_a_table_id_is_live_and_a_repeat_fails(self):
        """id: R-13"""
        self.write(
            "docs/REQUIREMENTS.md",
            "| Id | Statement |\n| --- | --- |\n| R-1 | One. |\n",
        )
        self.write(
            "docs/DECISIONS.md",
            "| Id | Status | Choice |\n| --- | --- | --- |\n| D-1 | Open | Later. |\n",
        )
        self.assertEqual(ids.check(self.root), [])
        self.write("docs/history/extra.md", "---\nid: R-1\n---\n")
        errors = ids.check(self.root)
        self.assertTrue(any("R-1" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
