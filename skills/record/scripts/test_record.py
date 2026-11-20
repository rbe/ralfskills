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
                "| Id | Title | Statement |\n| --- | --- | --- |\n"
                "| R-1 | One, two | The long statement. |\n",
                encoding="utf-8",
            )
            toon.write_indexes(root)
            text = (docs / "requirements-index.toon").read_text(encoding="utf-8")
            self.assertIn("requirements[1]{id,title}:", text)
            self.assertIn('R-1,"One, two"', text)
            self.assertNotIn("The long statement.", text)
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


skill_index = load("skill_index", HERE / "skill_index.py")
decision_log = load("decision_log", HERE / "decision_log.py")


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


class DecisionLogTest(unittest.TestCase):
    def test_the_log_lists_rules_choices_and_replaced_rules(self):
        """id: R-62"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_file(
                root,
                "docs/adr/ADR-0002.md",
                "---\nid: ADR-0002\ntitle: Listen on a socket\nstatus: Superseded\n---\n",
            )
            write_file(
                root,
                "docs/adr/ADR-0003.md",
                "---\nid: ADR-0003\ntitle: Listen on localhost\nstatus: Accepted\n"
                "skills: [security, review]\nsupersedes: [ADR-0002]\n---\n\n"
                "# Listen on localhost\n\n## Rule\n\nThe server binds 127.0.0.1.\n\n"
                "## Why\n\nNo other host needs it.\n",
            )
            write_file(
                root,
                "docs/DECISIONS.md",
                "---\nid: D-1\nstatus: decided\n---\n\nKeep the host make.\n\n"
                "---\nid: D-2\nstatus: open\n---\n\nWhich port.\n",
            )
            text = decision_log.render(root)
            rules = text.split("## Rules in force", 1)[1].split("## Choices", 1)[0]
            self.assertIn(
                '### <a id="adr-0003"></a>ADR-0003 Listen on localhost', rules
            )
            self.assertIn("Rule: The server binds 127.0.0.1.", rules)
            self.assertIn("Why: No other host needs it.", rules)
            self.assertIn("Skills: security, review", rules)
            self.assertNotIn("ADR-0002", rules)
            self.assertIn('- <a id="d-1"></a>D-1. Keep the host make.', text)
            open_choices = text.split("## Open choices", 1)[1]
            self.assertIn('- <a id="d-2"></a>D-2. Which port.', open_choices)
            self.assertIn(
                '- <a id="adr-0002"></a>ADR-0002 Listen on a socket. '
                "Replaced by [ADR-0003](#adr-0003).",
                text,
            )
            self.assertIn("Hand-editing this file is a defect.", text)

    def test_the_log_has_the_title_and_the_sentence_of_a_decision_block(self):
        """id: R-62"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_file(
                root,
                "docs/DECISIONS.md",
                "---\nid: D-1\ntitle: Slug format\nstatus: decided\n---\n\n"
                "A slug has lowercase letters,\ndigits, and hyphens.\n",
            )
            text = decision_log.render(root)
            self.assertIn(
                '- <a id="d-1"></a>D-1. Slug format A slug has lowercase letters, digits, and hyphens.',
                text,
            )

    def test_a_requirements_list_is_in_the_log_when_there_is_no_adr_file(self):
        """id: R-62"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_file(
                root,
                "docs/REQUIREMENTS.md",
                "| Id | Title | Statement |\n| --- | --- | --- |\n"
                "| R-1 | Tests name a requirement | A test names its id. |\n",
            )
            write_file(
                root,
                "docs/DECISIONS.md",
                "| Id | Status | Choice |\n| --- | --- | --- |\n"
                "| D-3 | Decided | One list. |\n",
            )
            text = decision_log.render(root)
            self.assertIn('### <a id="r-1"></a>R-1 Tests name a requirement', text)
            self.assertIn("A test names its id.", text)
            self.assertIn('- <a id="d-3"></a>D-3. One list.', text)


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
            "docs/KNOWN_ISSUES.md",
            "| Id | Defect |\n| --- | --- |\n| K-1 | One. |\n",
        )
        self.assertEqual(ids.check(self.root), [])
        self.assertEqual(
            ids.retire(self.root, "K-1"),
            [
                "K-1 is still in use: "
                + str(self.root / "docs" / "KNOWN_ISSUES.md")
                + ":3"
            ],
        )
        self.write("docs/history/extra.md", "---\nid: K-1\n---\n")
        self.assertTrue(any("K-1" in error for error in ids.check(self.root)))

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


ANCHORED = '| Id | Status | Choice |\n| --- | --- | --- |\n| <a id="d-9"></a>D-9 | Decided | See R-1. |\n'


def tree(root, files):
    for relative, text in files.items():
        write_file(root, relative, text)


class LinkTest(unittest.TestCase):
    def test_a_link_in_a_code_span_or_a_code_block_is_an_example_and_stays(self):
        """id: R-69"""
        found = {"D-9": ("docs/DECISIONS.md", "d-9")}
        text = (
            "The form is `[D-9](../DECISIONS.md#d-9)`. See [D-9](wrong.md).\n"
            "```\n[D-9](example.md)\n```\n"
        )
        result = links.link_text(text, found, "docs/history")
        self.assertIn("`[D-9](../DECISIONS.md#d-9)`", result)
        self.assertIn("See [D-9](../DECISIONS.md#d-9).", result)
        self.assertIn("```\n[D-9](example.md)\n```", result)
        self.assertEqual(
            links.unlink("[D-9](x.md) and `[D-9](y.md)`"), "D-9 and `[D-9](y.md)`"
        )

    FOUND = {
        "D-9": ("docs/DECISIONS.md", "d-9"),
        "H-2026-11-20-go-skill": ("docs/history/H-2026-11-20-go-skill.md", ""),
    }

    def test_targets_cover_a_table_id_and_a_frontmatter_id_and_skip_a_retired_id(self):
        """id: R-69"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tree(
                root,
                {
                    "docs/DECISIONS.md": ANCHORED + "| D-1 | Decided | Gone. |\n",
                    "docs/history/H-2026-11-20-go-skill.md": "---\nid: H-2026-11-20-go-skill\n---\n",
                    "docs/ids.yaml": "retired:\n- D-1\n",
                },
            )
            found = links.targets(root)
            self.assertEqual(found["D-9"], ("docs/DECISIONS.md", "d-9"))
            self.assertEqual(
                found["H-2026-11-20-go-skill"],
                ("docs/history/H-2026-11-20-go-skill.md", ""),
            )
            self.assertNotIn("D-1", found)

    def test_link_text_links_a_prose_id_with_a_relative_path(self):
        """id: R-69"""
        text = links.link_text(
            "See D-9 and H-2026-11-20-go-skill.", self.FOUND, "docs/history"
        )
        self.assertEqual(
            text,
            "See [D-9](../DECISIONS.md#d-9) and "
            "[H-2026-11-20-go-skill](H-2026-11-20-go-skill.md).",
        )
        self.assertEqual(
            links.link_text("D-9", self.FOUND, "build"),
            "[D-9](../docs/DECISIONS.md#d-9)",
        )
        self.assertEqual(
            links.link_text("D-9", self.FOUND, "docs", "docs/DECISIONS.md"),
            "[D-9](#d-9)",
        )

    def test_link_text_leaves_code_links_comments_frontmatter_headings_and_cells(self):
        """id: R-69"""
        cases = [
            "A `D-9` span.",
            "```\nD-9\n```",
            "A [see D-9](https://example.com/D-9) link.",
            "---\nid: D-9\ntitle: D-9\n---",
            "# Heading D-9",
            "<!-- D-9 -->",
            "<!--\nD-9\n-->",
            "| D-9 | text |",
            "| Id | D-9 |\n| D-9 | text |",
            "Path docs/history/D-9.md here.",
        ]
        for case in cases:
            with self.subTest(case=case):
                text = links.link_text(case, self.FOUND, "docs")
                self.assertEqual(
                    text.replace("| Id | [D-9](DECISIONS.md#d-9) |", "| Id | D-9 |"),
                    case,
                )

    def test_link_text_links_a_later_cell_and_leaves_an_unknown_id_plain(self):
        """id: R-69"""
        text = links.link_text("| R-2 | D-9 and D-77 |", self.FOUND, "docs")
        self.assertEqual(text, "| R-2 | [D-9](DECISIONS.md#d-9) and D-77 |")

    def test_unlink_restores_the_bare_id_and_keeps_other_links(self):
        """id: R-69"""
        text = "[D-9](../DECISIONS.md#d-9) and [docs](a.md) and [D-9 here](b.md)"
        self.assertEqual(
            links.unlink(text), "D-9 and [docs](a.md) and [D-9 here](b.md)"
        )
        linked = links.link_text(text, self.FOUND, "docs/history")
        self.assertEqual(links.unlink(linked), links.unlink(text))

    def test_anchor_rows_adds_the_anchor_once(self):
        """id: R-69"""
        row = "| D-9 | Decided | One. |"
        once = links.anchor_rows(row)
        self.assertEqual(once, '| <a id="d-9"></a>D-9 | Decided | One. |')
        self.assertEqual(links.anchor_rows(once), once)
        self.assertEqual(links.strip_anchor('<a id="d-9"></a>D-9 '), "D-9")
        self.assertEqual(links.anchor_rows("| Id | Status |"), "| Id | Status |")

    def sample(self, root):
        tree(
            root,
            {
                "docs/DECISIONS.md": "# Decisions\n\n| Id | Status | Choice |\n| --- | --- | --- |\n"
                "| D-9 | Decided | D-9 and R-1 and D-1. |\n",
                "docs/REQUIREMENTS.md": "| Id | Title | Statement |\n| --- | --- | --- |\n"
                "| R-1 | One | See D-9. |\n",
                "docs/history/H-2026-11-20-x.md": "---\nid: H-2026-11-20-x\n---\n\n# X\n\nSee D-9 and `R-1`.\n",
                "docs/ids.yaml": "retired:\n- D-1\n",
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
                    "docs/DECISIONS.md",
                    "docs/REQUIREMENTS.md",
                    "docs/history/H-2026-11-20-x.md",
                ],
            )
            decisions = (root / "docs" / "DECISIONS.md").read_text(encoding="utf-8")
            self.assertIn(
                '| <a id="d-9"></a>D-9 | Decided | D-9 and [R-1](REQUIREMENTS.md#r-1) and D-1. |',
                decisions,
            )
            history = (root / "docs/history/H-2026-11-20-x.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("See [D-9](../DECISIONS.md#d-9) and `R-1`.", history)
            self.assertEqual(links.rewrite(root), [])

    def test_problems_report_an_unlinked_id_and_none_after_rewrite(self):
        """id: R-69"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.sample(root)
            errors = links.problems(root)
            self.assertIn("docs/history/H-2026-11-20-x.md: run make links", errors)
            self.assertTrue(any("without a link: D-9" in error for error in errors))
            links.rewrite(root)
            self.assertEqual(links.problems(root), [])

    def test_ids_check_finds_a_repeat_when_the_row_has_an_anchor(self):
        """id: R-69"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tree(
                root,
                {
                    "docs/DECISIONS.md": ANCHORED,
                    "docs/history/extra.md": "---\nid: D-9\n---\n",
                },
            )
            self.assertTrue(any("D-9" in error for error in ids.check(root)))

    def test_the_index_and_the_log_read_an_anchored_row(self):
        """id: R-69"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tree(
                root,
                {
                    "docs/REQUIREMENTS.md": "| Id | Title | Statement |\n| --- | --- | --- |\n"
                    '| <a id="r-1"></a>R-1 | One | See D-9. |\n',
                    "docs/DECISIONS.md": ANCHORED,
                },
            )
            found = requirements_index.rows(root / "docs" / "REQUIREMENTS.md")
            self.assertEqual(found, [("R-1", "One")])
            text = decision_log.render(root)
            self.assertIn('### <a id="r-1"></a>R-1 One', text)
            self.assertIn("See [D-9](#d-9).", text)
            self.assertIn('- <a id="d-9"></a>D-9. See [R-1](#r-1).', text)

    def test_the_log_links_an_item_that_is_not_in_the_log_to_its_source(self):
        """id: R-69"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tree(
                root,
                {
                    "docs/DECISIONS.md": "| Id | Status | Choice |\n| --- | --- | --- |\n"
                    "| D-9 | Decided | After [H-2026-11-20-x](../h.md). |\n",
                    "docs/history/H-2026-11-20-x.md": "---\nid: H-2026-11-20-x\n---\n",
                },
            )
            text = decision_log.render(root)
            self.assertIn(
                "After [H-2026-11-20-x](../docs/history/H-2026-11-20-x.md).", text
            )


if __name__ == "__main__":
    unittest.main()
