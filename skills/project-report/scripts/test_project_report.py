#!/usr/bin/env python3
"""The report, the requirement id, and test-changed."""

import importlib.util
import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


requirements = load("requirements", HERE / "requirements.py")
select_tests = load("select_tests", HERE / "select_tests.py")
project_report = load("project_report", HERE / "project_report.py")
changed_tests = load("changed_tests", HERE / "changed_tests.py")


def write(root, relative, text):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


class RequirementIdTest(unittest.TestCase):
    def test_a_missing_id_fails_the_check(self):
        """id: R-1"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(
                root,
                "docs/adr/ADR-0001.md",
                "---\nid: ADR-0001\ntitle: One\nstatus: Accepted\n---\n",
            )
            write(
                root,
                "tests/test_sample.py",
                "def test_runs():\n    assert True\n",
            )
            errors = requirements.problems(
                requirements.collect(root), requirements.proofs(root)
            )
            self.assertTrue(any("has no id" in error for error in errors))

    def test_a_path_does_not_name_the_requirement(self):
        """id: R-1"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(
                root,
                "docs/adr/ADR-0001.md",
                "---\nid: ADR-0001\ntitle: One\nstatus: Accepted\n---\n",
            )
            write(
                root,
                "tests/test_sample.py",
                'def test_runs():\n    """See docs/adr/ADR-0001.md"""\n    assert True\n',
            )
            errors = requirements.problems(
                requirements.collect(root), requirements.proofs(root)
            )
            self.assertTrue(any("has no id" in error for error in errors))

    def test_an_id_that_is_not_a_requirement_fails(self):
        """id: R-1"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(
                root,
                "docs/adr/ADR-0001.md",
                "---\nid: ADR-0001\ntitle: One\nstatus: Accepted\n---\n",
            )
            write(
                root,
                "tests/test_sample.py",
                'def test_runs():\n    """id: ADR-9999"""\n    assert True\n',
            )
            errors = requirements.problems(
                requirements.collect(root), requirements.proofs(root)
            )
            self.assertTrue(any("not a requirement" in error for error in errors))

    def test_review_fails_a_test_that_has_no_id(self):
        """id: R-1"""
        for name in ("develop", "review", "project-setup"):
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Stop when a test has no id.", text)
        record = (ROOT / "skills" / "record" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("`id:`", record)
        self.assertIn("does not build a path", record)

    def test_a_test_in_another_language_names_its_id_in_a_comment(self):
        """id: R-63"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(
                root,
                "docs/adr/ADR-0001.md",
                "---\nid: ADR-0001\ntitle: One\nstatus: Accepted\n---\n",
            )
            write(root, "src/a.test.ts", "// id: ADR-0001\ntest('a', () => {})\n")
            write(
                root,
                "src/test/java/PortTest.java",
                "/**\n * id: ADR-0001\n */\nclass PortTest {}\n",
            )
            write(root, "src/b.spec.js", "test('b', () => {})\n")
            found = requirements.proofs(root)
            named = {proof.path: proof.requirement_id for proof in found}
            self.assertEqual(named["src/a.test.ts"], "ADR-0001")
            self.assertEqual(named["src/test/java/PortTest.java"], "ADR-0001")
            self.assertIsNone(named["src/b.spec.js"])
            errors = requirements.problems(requirements.collect(root), found)
            self.assertEqual(errors, ["src/b.spec.js has no id"])

    def test_a_test_inside_an_installed_skill_is_not_a_project_test(self):
        """id: R-63"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(
                root,
                ".claude/skills/record/scripts/test_record.py",
                'def test_runs():\n    """id: R-13"""\n    assert True\n',
            )
            write(root, "node_modules/x/x.test.js", "test('x', () => {})\n")
            self.assertEqual(requirements.proofs(root), [])

    def test_every_test_in_this_repository_names_a_requirement(self):
        """id: R-1"""
        errors = requirements.problems(
            requirements.collect(ROOT), requirements.proofs(ROOT)
        )
        self.assertEqual(errors, [])


class ChangedTestsTest(unittest.TestCase):
    def test_coverage_of_a_file_selects_its_tests(self):
        """id: R-2"""
        covered = select_tests.merge_covered(
            {"pkg.Test.test_one": ["pkg/app.py"]},
            {
                "pkg.Test.test_one": ["docs/ROADMAP.md"],
                "pkg.Test.test_two": ["docs/ROADMAP.md"],
                "": ["pkg/ignored.py"],
            },
        )
        self.assertEqual(
            select_tests.select(["pkg/app.py"], covered), ["pkg.Test.test_one"]
        )
        self.assertEqual(
            select_tests.select(["docs/ROADMAP.md"], covered),
            ["pkg.Test.test_one", "pkg.Test.test_two"],
        )
        self.assertNotIn("", covered)
        script = (HERE / "changed_tests.py").read_text(encoding="utf-8")
        self.assertIn("covered.json", script)
        self.assertNotIn("SKILL.md", script)

    def test_a_missing_coverage_map_stops_test_changed(self):
        """id: R-2"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            error = io.StringIO()
            with redirect_stderr(error):
                code = changed_tests.run(root)
            self.assertEqual(code, 1)
            self.assertIn("make coverage", error.getvalue())

    def test_no_covering_test_still_names_the_full_suite(self):
        """id: R-2"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            coverage = root / "build" / "coverage"
            coverage.mkdir(parents=True)
            (coverage / "changed.txt").write_text("README.md\n", encoding="utf-8")
            (coverage / "covered.json").write_text("{}\n", encoding="utf-8")
            output = io.StringIO()
            with redirect_stdout(output):
                code = changed_tests.run(root)
            self.assertEqual(code, 0)
            self.assertIn("make test runs the full suite", output.getvalue())

    def test_ci_runs_the_full_suite(self):
        """id: R-2"""
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertIn("TEST_CHANGED_CMD", makefile)
        self.assertIn("cover_tests.py", makefile)
        self.assertIn("$(PYTHON) -m unittest $(UNIT_TESTS)", makefile)
        setup = ROOT / "skills" / "project-setup"
        fragment = (setup / "test-changed.mk").read_text(encoding="utf-8")
        self.assertIn("test-changed:", fragment)
        project = (setup / "project.mk").read_text(encoding="utf-8")
        self.assertIn("include $(PROJECT_MK_DIR)test-changed.mk", project)
        sdlc = (ROOT / "skills" / "github-pipeline" / "sdlc.mk").read_text(
            encoding="utf-8"
        )
        self.assertIn("project-setup/test-changed.mk", sdlc)
        ci_targets = [line for line in sdlc.splitlines() if line.startswith("SDLC_CI")]
        self.assertEqual(len(ci_targets), 1)
        self.assertNotIn("test-changed", ci_targets[0])
        for name in ("develop", "review", "project-setup"):
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("A green `test-changed` does not replace `make test`.", text)
        for name in ("ci.node.yml", "ci.gradle.yml"):
            workflow = (
                ROOT / "skills" / "github-pipeline" / "templates" / name
            ).read_text(encoding="utf-8")
            self.assertIn("\n      - run: make test\n", workflow)
            self.assertNotIn("test-changed", workflow)


class ProjectReportTest(unittest.TestCase):
    def sample(self, root):
        write(
            root,
            "docs/adr/ADR-0001.md",
            "---\nid: ADR-0001\ntitle: Listen on localhost\nstatus: Accepted\n---\n\n# Listen\n",
        )
        write(
            root,
            "docs/DECISIONS.md",
            "---\nid: D-1\ntitle: Keep the host make\nstatus: decided\n---\n\nKeep the host make.\n",
        )
        write(
            root,
            "skills/plan/SKILL.md",
            "# Plan\n\n## Work\n\n1. Name who owns state.\n",
        )
        write(
            root,
            "skills/develop/SKILL.md",
            "# Develop\n\n## Work\n\n1. Run `make lint` and `make test`.\n",
        )
        write(
            root,
            "tests/test_sample.py",
            'def test_listens_on_localhost():\n    """id: ADR-0001"""\n    assert True\n',
        )

    def test_the_report_names_the_tests_and_the_gaps(self):
        """id: R-3"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.sample(root)
            text, errors = project_report.build(root)
            self.assertEqual(errors, [])
            self.assertIn(
                "| ADR-0001 | adr | Accepted | tests.test_sample.test_listens_on_localhost |",
                text,
            )
            gap = text.split("### Ids with no test", 1)[1].split(
                "### Tests with no id", 1
            )[0]
            self.assertIn("D-1 (decision)", gap)
            self.assertNotIn("ADR-0001 (adr)", gap)
            self.assertIn("Hand-editing this file is a defect.", text)

    def test_a_superseded_adr_is_not_an_id_with_no_test(self):
        """id: R-56"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.sample(root)
            write(
                root,
                "docs/adr/ADR-0002.md",
                "---\nid: ADR-0002\ntitle: Listen on a socket\nstatus: Superseded\n---\n",
            )
            write(
                root,
                "docs/adr/ADR-0003.md",
                "---\nid: ADR-0003\ntitle: Listen on a port\nstatus: Accepted\n"
                "supersedes: [ADR-0002]\n---\n",
            )
            text, errors = project_report.build(root)
            self.assertEqual(errors, [])
            gap = text.split("### Ids with no test", 1)[1].split(
                "### Tests with no id", 1
            )[0]
            self.assertNotIn("ADR-0002 (adr)", gap)
            self.assertIn("ADR-0003 (adr)", gap)
            self.assertIn("| ADR-0002 | adr | Superseded | no test |", text)

    def test_a_requirements_list_is_the_map_when_there_is_no_adr_file(self):
        """id: R-3"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(
                root,
                "docs/REQUIREMENTS.md",
                "| Id | Statement |\n| --- | --- |\n| R-1 | A test names the requirement. |\n",
            )
            write(
                root,
                "tests/test_sample.py",
                'def test_names_it():\n    """id: R-1"""\n    assert True\n',
            )
            text, errors = project_report.build(root)
            self.assertEqual(errors, [])
            self.assertIn("| R-1 | requirement |", text)
            self.assertIn("The id is a row in `docs/REQUIREMENTS.md`.", text)
            self.assertNotIn("### ADRs", text)

    def test_an_adr_file_keeps_the_product_report(self):
        """id: R-3"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.sample(root)
            write(
                root,
                "docs/REQUIREMENTS.md",
                "| Id | Statement |\n| --- | --- |\n| R-9 | Other. |\n",
            )
            text, errors = project_report.build(root)
            self.assertEqual(errors, [])
            self.assertIn("| ADR-0001 | adr | Accepted |", text)
            self.assertIn("### ADRs", text)
            self.assertNotIn("R-9", text)

    def test_the_reviews_quote_the_stage_checks(self):
        """id: R-3"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.sample(root)
            text, _errors = project_report.build(root)
            architecture = text.split("## Architecture review", 1)[1].split(
                "## Development review", 1
            )[0]
            development = text.split("## Development review", 1)[1]
            self.assertIn("Listen on localhost", architecture)
            self.assertIn("Name who owns state.", architecture)
            self.assertIn("review: not installed", architecture)
            self.assertIn("Keep the host make", development)
            self.assertIn("Run `make lint` and `make test`.", development)
            self.assertIn("project-setup: not installed", development)

    def test_make_project_report_is_the_writer(self):
        """id: R-3"""
        for name in ("review", "project-setup", "project-report"):
            text = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("`make project-report`", text)
            self.assertIn("Hand-editing", text)
        project = (ROOT / "skills" / "project-setup" / "project.mk").read_text(
            encoding="utf-8"
        )
        self.assertIn("project-report:", project)

    def test_this_repository_report_maps_the_requirements_list(self):
        """id: R-3"""
        text, errors = project_report.build(ROOT)
        self.assertEqual(errors, [])
        self.assertIn("## Requirements", text)
        self.assertIn("## Architecture review", text)
        self.assertIn("## Development review", text)
        self.assertIn("| R-7 | requirement |", text)
        gap = text.split("### Ids with no test", 1)[1].split("### Tests with no id", 1)[
            0
        ]
        self.assertNotIn("(roadmap)", gap)
        architecture = text.split("## Architecture review", 1)[1].split(
            "## Development review", 1
        )[0]
        development = text.split("## Development review", 1)[1]
        self.assertIn("who owns state", architecture)
        self.assertIn("one integration entry", development)
        self.assertIn("### Decisions", development)
        self.assertIn(
            "D-3, Decided. This collection keeps one requirements list and records open work and choices in force in this list.",
            development,
        )
        self.assertNotIn("list..", development)


if __name__ == "__main__":
    unittest.main()
