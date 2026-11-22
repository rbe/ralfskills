#!/usr/bin/env python3
"""Tests for the id check and the ADR index."""

import importlib.util
import os
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
links = load("links", HERE / "links.py")
requirements_index = load("requirements_index", HERE / "requirements_index.py")
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
        self.write("docs/ROADMAP.md", body)
        self.write("docs/proposals/P-1.md", "---\nid: D-1\nstatus: open\n---\n")
        errors = ids.check(self.root)
        self.assertTrue(any("D-1" in error for error in errors))

    def test_retired_id_still_in_use_fails(self):
        """id: R-13"""
        self.write("docs/ids.yaml", "retired:\n- D-1\n")
        self.write("docs/ROADMAP.md", "---\nid: D-1\nstatus: decided\n---\n")
        errors = ids.check(self.root)
        self.assertTrue(any("retired" in error for error in errors))

    def test_a_roadmap_row_is_a_live_id_and_a_roadmap_list_may_name_it(self):
        """id: R-13"""
        self.write(
            "docs/ROADMAP.md",
            "| Id | Kind | Title | Proposal |\n| --- | --- | --- | --- |\n"
            "| W-1 | defect | One. | |\n",
        )
        self.write("docs/history/H-1.md", "---\nid: H-1\nroadmap: [W-1]\n---\n")
        self.assertEqual(ids.check(self.root), [])
        self.assertEqual(
            ids.retire(self.root, "W-1"),
            ["W-1 is still in use: " + str(self.root / "docs" / "ROADMAP.md") + ":3"],
        )

    def test_retire_moves_an_unused_id(self):
        """id: R-13"""
        self.write("docs/ids.yaml", "retired: []\n")
        errors = ids.retire(self.root, "H-2026-11-15-old")
        self.assertEqual(errors, [])
        self.assertIn(
            "H-2026-11-15-old", ids.retired_ids(self.root / "docs" / "ids.yaml")
        )
        self.assertEqual(ids.check(self.root), [])

    def test_a_list_may_name_a_retired_id(self):
        """id: R-13"""
        self.write("docs/ids.yaml", "retired:\n- D-5\n")
        self.write(
            "docs/history/H-1.md",
            "---\nid: H-1\nadrs: []\ndecisions: [D-5]\n---\n",
        )
        self.assertEqual(ids.check(self.root), [])

    def test_a_list_that_names_an_unknown_id_fails(self):
        """id: R-13"""
        self.write(
            "docs/history/H-1.md",
            "---\nid: H-1\nadrs: []\ndecisions: [D-5]\n---\n",
        )
        errors = ids.check(self.root)
        self.assertTrue(
            any("D-5, which is neither live nor retired" in error for error in errors)
        )

    def test_a_list_that_is_text_or_has_no_brackets_fails(self):
        """id: R-13"""
        self.write(
            "docs/history/H-1.md",
            "---\nid: H-1\nadrs: none\ndecisions: [D-5, text]\nissues:\n---\n",
        )
        errors = ids.check(self.root)
        self.assertTrue(any("adrs is not a list" in error for error in errors))
        self.assertTrue(any("issues is not a list" in error for error in errors))
        self.assertTrue(any("text, which is not an id" in error for error in errors))

    def test_retire_with_into_writes_the_map_and_leaves_the_documents(self):
        """id: R-13"""
        row = '| <a id="r-28"></a>R-28 | Title | One sentence. |\n'
        self.write(
            "docs/REQUIREMENTS.md", "| Id | T | S |\n| --- | --- | --- |\n" + row
        )
        text = "---\nid: H-1\nadrs: []\ndecisions: [D-5, D-6]\n---\n\nBody D-5.\n"
        history = self.write("docs/history/H-1.md", text)
        self.assertEqual(ids.retire(self.root, "D-5", ["R-28"]), [])
        self.assertEqual(history.read_text(encoding="utf-8"), text)
        path = self.root / "docs" / "ids.yaml"
        self.assertEqual(ids.retired_ids(path), ["D-5"])
        self.assertEqual(ids.merged_ids(path), [("D-5", ["R-28"])])
        self.assertIn("merged:\n  D-5: [R-28]\n", path.read_text(encoding="utf-8"))

    def test_retire_without_into_writes_no_map_entry(self):
        """id: R-13"""
        self.assertEqual(ids.retire(self.root, "D-5"), [])
        path = self.root / "docs" / "ids.yaml"
        self.assertEqual(ids.retired_ids(path), ["D-5"])
        self.assertEqual(ids.merged_ids(path), [])
        self.assertNotIn("merged", path.read_text(encoding="utf-8"))

    def test_retire_of_a_surviving_id_hands_the_map_entry_on(self):
        """id: R-13"""
        rows = "".join(
            f'| <a id="r-{n}"></a>R-{n} | Title | One sentence. |\n' for n in (2, 3)
        )
        self.write(
            "docs/REQUIREMENTS.md", "| Id | T | S |\n| --- | --- | --- |\n" + rows
        )
        self.write("docs/ids.yaml", "retired:\n- D-5\nmerged:\n  D-5: [R-9]\n")
        self.assertEqual(ids.retire(self.root, "R-9", ["R-2", "R-3"]), [])
        path = self.root / "docs" / "ids.yaml"
        self.assertEqual(
            ids.merged_ids(path), [("D-5", ["R-2", "R-3"]), ("R-9", ["R-2", "R-3"])]
        )

    def test_the_map_names_a_retired_key_and_a_live_surviving_id(self):
        """id: R-13"""
        self.write(
            "docs/ids.yaml", "retired:\n- D-5\nmerged:\n  D-5: [R-9]\n  D-6: [R-2]\n"
        )
        errors = ids.check(self.root)
        self.assertTrue(
            any("D-5 names R-9, which is not a live id" in e for e in errors)
        )
        self.assertTrue(
            any("D-6, which is not on the retired list" in e for e in errors)
        )

    def test_retire_rejects_a_surviving_id_that_is_not_live(self):
        """id: R-13"""
        errors = ids.retire(self.root, "D-5", ["R-99"])
        self.assertTrue(any("R-99 is not a live id" in error for error in errors))
        self.assertFalse((self.root / "docs" / "ids.yaml").exists())

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
                "adrs: [ADR-0001]\nskills: [security, review]\nroadmap: [W-12]\n---\n\n# Body\n",
                encoding="utf-8",
            )
            text = adr_index.render(adr_index.rows(adr))
            self.assertIn("adr_index[1]{id,status,title,adrs,skills,roadmap}:", text)
            self.assertIn(
                "ADR-0004,Accepted,Listen on localhost,ADR-0001,security;review,W-12",
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
                "| Id | Title | Statement |\n| --- | --- | --- |\n"
                "| R-1 | One, two | The long statement. |\n",
                encoding="utf-8",
            )
            toon.write_indexes(root)
            text = (docs / "requirements-index.toon").read_text(encoding="utf-8")
            self.assertIn("requirements[1]{id,title,status}:", text)
            self.assertIn('R-1,"One, two",in force', text)
            self.assertNotIn("The long statement.", text)
            self.assertFalse((docs / "adr").exists())
            self.assertTrue((docs / "skill-index.toon").is_file())

    def test_the_index_shows_which_rows_are_planned(self):
        """id: R-6"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "REQUIREMENTS.md").write_text(
                "| Id | Title | Status | Statement |\n| --- | --- | --- | --- |\n"
                "| R-1 | One | in force | A statement. |\n"
                "| R-2 | Two | planned | Open work. |\n",
                encoding="utf-8",
            )
            toon.write_indexes(root)
            text = (docs / "requirements-index.toon").read_text(encoding="utf-8")
            self.assertIn("R-1,One,in force", text)
            self.assertIn("R-2,Two,planned", text)

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


skill_index = load("skill_index", HERE / "skill_index.py")


def write_file(root, relative, text):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class SkillNameTest(unittest.TestCase):
    def test_a_skill_name_that_differs_from_its_directory_is_an_error(self):
        """id: R-4"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_file(root, "skills/plan/SKILL.md", "---\nname: plan\n---\n")
            self.assertEqual(skill_index.name_errors(root), [])
            write_file(root, "skills/review/SKILL.md", "---\nname: check\n---\n")
            errors = skill_index.name_errors(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("review", errors[0])

    def test_make_toon_fails_when_a_skill_name_differs(self):
        """id: R-4"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            write_file(root, "skills/review/SKILL.md", "---\nname: check\n---\n")
            previous = Path.cwd()
            try:
                os.chdir(root)
                self.assertEqual(toon.main(), 1)
                write_file(root, "skills/review/SKILL.md", "---\nname: review\n---\n")
                self.assertEqual(toon.main(), 0)
            finally:
                os.chdir(previous)
            self.assertTrue((root / "docs" / "skill-index.toon").is_file())

    def test_a_description_with_a_colon_and_a_space_is_an_error(self):
        """id: R-65"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_file(
                root,
                "skills/plan/SKILL.md",
                "---\nname: plan\ndescription: Grill a change. Ask one question.\n---\n",
            )
            self.assertEqual(skill_index.yaml_errors(root), [])
            write_file(
                root,
                "skills/security/SKILL.md",
                '---\nname: security\ndescription: Write "security: not installed".\n---\n',
            )
            errors = skill_index.yaml_errors(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("security", errors[0])
            self.assertIn("description", errors[0])

    def test_every_skill_in_this_collection_has_yaml_frontmatter(self):
        """id: R-65"""
        self.assertEqual(skill_index.yaml_errors(HERE.parents[2]), [])

    def test_every_skill_in_this_collection_has_its_directory_name(self):
        """id: R-4"""
        self.assertEqual(skill_index.name_errors(HERE.parents[2]), [])


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

    def test_a_known_issue_row_is_a_live_id(self):
        """id: R-13"""
        self.write(
            "docs/ROADMAP.md",
            "| Id | Defect |\n| --- | --- |\n| W-1 | One. |\n",
        )
        self.assertEqual(ids.check(self.root), [])
        self.assertEqual(
            ids.retire(self.root, "W-1"),
            ["W-1 is still in use: " + str(self.root / "docs" / "ROADMAP.md") + ":3"],
        )
        self.write("docs/history/extra.md", "---\nid: W-1\n---\n")
        self.assertTrue(any("W-1" in error for error in ids.check(self.root)))

    def test_a_table_id_is_live_and_a_repeat_fails(self):
        """id: R-13"""
        self.write(
            "docs/REQUIREMENTS.md",
            "| Id | Statement |\n| --- | --- |\n| R-1 | One. |\n",
        )
        self.write(
            "docs/ROADMAP.md",
            "| Id | Kind | Title |\n| --- | --- | --- |\n| W-1 | Open | Later. |\n",
        )
        self.assertEqual(ids.check(self.root), [])
        self.write("docs/history/extra.md", "---\nid: R-1\n---\n")
        errors = ids.check(self.root)
        self.assertTrue(any("R-1" in error for error in errors))


ANCHORED = '| Id | Kind | Title |\n| --- | --- | --- |\n| <a id="w-9"></a>W-9 | feature | See R-1. |\n'


def tree(root, files):
    for relative, text in files.items():
        write_file(root, relative, text)


class LinkTest(unittest.TestCase):
    def test_a_link_in_a_code_span_or_a_code_block_is_an_example_and_stays(self):
        """id: R-69"""
        found = {"W-9": ("docs/ROADMAP.md", "w-9")}
        text = (
            "The form is `[W-9](../ROADMAP.md#w-9)`. See [W-9](wrong.md).\n"
            "```\n[W-9](example.md)\n```\n"
        )
        result = links.link_text(text, found, "docs/history")
        self.assertIn("`[W-9](../ROADMAP.md#w-9)`", result)
        self.assertIn("See [W-9](../ROADMAP.md#w-9).", result)
        self.assertIn("```\n[W-9](example.md)\n```", result)
        self.assertEqual(
            links.unlink("[W-9](x.md) and `[W-9](y.md)`"), "W-9 and `[W-9](y.md)`"
        )

    FOUND = {
        "W-9": ("docs/ROADMAP.md", "w-9"),
        "H-2026-11-20-go-skill": ("docs/history/H-2026-11-20-go-skill.md", ""),
    }

    def test_targets_cover_a_table_id_and_a_frontmatter_id_and_skip_a_retired_id(self):
        """id: R-69"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tree(
                root,
                {
                    "docs/ROADMAP.md": ANCHORED + "| W-1 | feature | Gone. |\n",
                    "docs/history/H-2026-11-20-go-skill.md": "---\nid: H-2026-11-20-go-skill\n---\n",
                    "docs/ids.yaml": "retired:\n- W-1\n",
                },
            )
            found = links.targets(root)
            self.assertEqual(found["W-9"], ("docs/ROADMAP.md", "w-9"))
            self.assertEqual(
                found["H-2026-11-20-go-skill"],
                ("docs/history/H-2026-11-20-go-skill.md", ""),
            )
            self.assertNotIn("W-1", found)

    def test_link_text_links_a_prose_id_with_a_relative_path(self):
        """id: R-69"""
        text = links.link_text(
            "See W-9 and H-2026-11-20-go-skill.", self.FOUND, "docs/history"
        )
        self.assertEqual(
            text,
            "See [W-9](../ROADMAP.md#w-9) and "
            "[H-2026-11-20-go-skill](H-2026-11-20-go-skill.md).",
        )
        self.assertEqual(
            links.link_text("W-9", self.FOUND, "build"),
            "[W-9](../docs/ROADMAP.md#w-9)",
        )
        self.assertEqual(
            links.link_text("W-9", self.FOUND, "docs", "docs/ROADMAP.md"),
            "[W-9](#w-9)",
        )

    def test_link_text_leaves_code_links_comments_frontmatter_headings_and_cells(self):
        """id: R-69"""
        cases = [
            "A `W-9` span.",
            "```\nW-9\n```",
            "A [see W-9](https://example.com/W-9) link.",
            "---\nid: W-9\ntitle: W-9\n---",
            "# Heading W-9",
            "<!-- W-9 -->",
            "<!--\nW-9\n-->",
            "| W-9 | text |",
            "| Id | W-9 |\n| W-9 | text |",
            "Path docs/history/W-9.md here.",
        ]
        for case in cases:
            with self.subTest(case=case):
                text = links.link_text(case, self.FOUND, "docs")
                self.assertEqual(
                    text.replace("| Id | [W-9](ROADMAP.md#w-9) |", "| Id | W-9 |"),
                    case,
                )

    def test_link_text_links_a_later_cell_and_leaves_an_unknown_id_plain(self):
        """id: R-69"""
        text = links.link_text("| R-2 | W-9 and W-77 |", self.FOUND, "docs")
        self.assertEqual(text, "| R-2 | [W-9](ROADMAP.md#w-9) and W-77 |")

    def test_unlink_restores_the_bare_id_and_keeps_other_links(self):
        """id: R-69"""
        text = "[W-9](../ROADMAP.md#w-9) and [docs](a.md) and [W-9 here](b.md)"
        self.assertEqual(
            links.unlink(text), "W-9 and [docs](a.md) and [W-9 here](b.md)"
        )
        linked = links.link_text(text, self.FOUND, "docs/history")
        self.assertEqual(links.unlink(linked), links.unlink(text))

    def test_anchor_rows_adds_the_anchor_once(self):
        """id: R-69"""
        row = "| W-9 | feature | One. |"
        once = links.anchor_rows(row)
        self.assertEqual(once, '| <a id="w-9"></a>W-9 | feature | One. |')
        self.assertEqual(links.anchor_rows(once), once)
        self.assertEqual(links.strip_anchor('<a id="w-9"></a>W-9 '), "W-9")
        self.assertEqual(links.anchor_rows("| Id | Status |"), "| Id | Status |")

    def sample(self, root):
        tree(
            root,
            {
                "docs/ROADMAP.md": "# Roadmap\n\n| Id | Kind | Title |\n| --- | --- | --- |\n"
                "| W-9 | feature | W-9 and R-1 and W-1. |\n",
                "docs/REQUIREMENTS.md": "| Id | Title | Statement |\n| --- | --- | --- |\n"
                "| R-1 | One | See W-9. |\n",
                "docs/history/H-2026-11-20-x.md": "---\nid: H-2026-11-20-x\n---\n\n# X\n\nSee W-9 and `R-1`.\n",
                "docs/ids.yaml": "retired:\n- W-1\n",
            },
        )

    def test_rewrite_changes_files_once_and_does_not_link_a_row_to_itself(self):
        """id: R-69"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.sample(root)
            changed = links.rewrite(root)
            self.assertEqual(
                changed,
                [
                    "docs/REQUIREMENTS.md",
                    "docs/ROADMAP.md",
                    "docs/history/H-2026-11-20-x.md",
                ],
            )
            roadmap = (root / "docs" / "ROADMAP.md").read_text(encoding="utf-8")
            self.assertIn(
                '| <a id="w-9"></a>W-9 | feature | W-9 and [R-1](REQUIREMENTS.md#r-1) and W-1. |',
                roadmap,
            )
            history = (root / "docs/history/H-2026-11-20-x.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("See [W-9](../ROADMAP.md#w-9) and `R-1`.", history)
            self.assertEqual(links.rewrite(root), [])

    def test_problems_report_an_unlinked_id_and_none_after_rewrite(self):
        """id: R-69"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.sample(root)
            errors = links.problems(root)
            self.assertIn("docs/history/H-2026-11-20-x.md: run make links", errors)
            self.assertTrue(any("without a link: W-9" in error for error in errors))
            links.rewrite(root)
            self.assertEqual(links.problems(root), [])

    def test_ids_check_finds_a_repeat_when_the_row_has_an_anchor(self):
        """id: R-69"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tree(
                root,
                {
                    "docs/ROADMAP.md": ANCHORED,
                    "docs/history/extra.md": "---\nid: W-9\n---\n",
                },
            )
            self.assertTrue(any("W-9" in error for error in ids.check(root)))


if __name__ == "__main__":
    unittest.main()
