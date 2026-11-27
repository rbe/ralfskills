#!/usr/bin/env python3
"""The gate stamp, the pre-push hook, and the warning-free Make contract."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SETUP = ROOT / "skills" / "r-project-setup"
SCRIPTS = SETUP / "scripts"


def run(args, cwd, check=True):
    """Run one command in a directory with a fixed git identity and home."""
    env = dict(os.environ, HOME=str(cwd))
    env.update(GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t")
    env.update(GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    return subprocess.run(
        args, cwd=cwd, env=env, capture_output=True, text=True, check=check
    )


class GateRepository:
    """A temporary git repository with the scripts of r-project-setup."""

    def __init__(self, test):
        self.root = Path(tempfile.mkdtemp())
        test.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        run(["git", "init", "-q"], self.root)
        shutil.copytree(SCRIPTS, self.root / "scripts")
        (self.root / ".gitignore").write_text("build/\n", encoding="utf-8")
        self.edit("work.txt", "one\n")

    def edit(self, name, text):
        (self.root / name).write_text(text, encoding="utf-8")

    def stamp(self):
        return run(["sh", "scripts/gates-stamp.sh", "write"], self.root)

    def commit(self, *paths):
        """Commit the named paths and return the commit id."""
        run(["git", "add", "--", *paths], self.root)
        run(["git", "commit", "-q", "-m", "work"], self.root)
        return run(["git", "rev-parse", "HEAD"], self.root).stdout.strip()

    def push_hook(self, sha=None, remote_ref="refs/heads/topic", env=None):
        """Run the hook as git does: one line for the pushed ref on stdin."""
        sha = sha or run(["git", "rev-parse", "HEAD"], self.root).stdout.strip()
        line = f"refs/heads/topic {sha} {remote_ref} {'0' * 40}\n"
        return subprocess.run(
            ["sh", "scripts/pre-push.sh"],
            cwd=self.root,
            input=line,
            env=dict(os.environ, **(env or {})),
            capture_output=True,
            text=True,
            check=False,
        )

    def commit_all(self):
        return self.commit("work.txt", ".gitignore", "scripts")


class PrePushTest(unittest.TestCase):
    def test_refuses_without_stamp(self):
        """id: R-127"""
        repo = GateRepository(self)
        repo.commit_all()
        result = repo.push_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("make gates", result.stderr)

    def test_passes_when_the_pushed_commit_is_the_checked_content(self):
        """id: R-127"""
        repo = GateRepository(self)
        repo.stamp()
        repo.commit_all()
        self.assertEqual(repo.push_hook().returncode, 0)

    def test_refuses_a_commit_of_part_of_the_checked_content(self):
        """id: R-127"""
        repo = GateRepository(self)
        repo.edit("extra.txt", "new\n")
        repo.stamp()
        repo.commit_all()
        result = repo.push_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("extra.txt", result.stderr)

    def test_refuses_a_commit_edited_after_the_gates(self):
        """id: R-127"""
        repo = GateRepository(self)
        repo.stamp()
        repo.edit("work.txt", "two\n")
        repo.commit_all()
        result = repo.push_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("work.txt", result.stderr)

    def test_an_edit_after_the_commit_does_not_change_the_result(self):
        """id: R-127"""
        repo = GateRepository(self)
        repo.stamp()
        repo.commit_all()
        repo.edit("work.txt", "an edit that is not pushed\n")
        self.assertEqual(repo.push_hook().returncode, 0)

    def test_passes_a_close_commit_that_changes_only_board_files(self):
        """id: R-127"""
        repo = GateRepository(self)
        (repo.root / "docs" / "history").mkdir(parents=True)
        repo.edit("docs/history/H-1.md", "open\n")
        repo.stamp()
        repo.commit_all()
        repo.commit("docs/history/H-1.md")
        repo.edit("docs/history/H-1.md", "closed\n")
        repo.edit("docs/ROADMAP.md", "| Id |\n")
        sha = repo.commit("docs/history/H-1.md", "docs/ROADMAP.md")
        self.assertEqual(repo.push_hook(sha).returncode, 0)
        result = repo.push_hook(sha, env={"BOARD_FILES": "docs/proposals/"})
        self.assertEqual(result.returncode, 1)

    def test_a_deleted_ref_and_a_tag_that_is_no_version_pass(self):
        """id: R-127"""
        repo = GateRepository(self)
        repo.commit_all()
        self.assertEqual(repo.push_hook("0" * 40).returncode, 0)
        self.assertEqual(repo.push_hook(remote_ref="refs/tags/note").returncode, 0)

    def test_a_version_tag_runs_check_tag_when_make_has_the_target(self):
        """id: R-120"""
        repo = GateRepository(self)
        repo.commit_all()
        self.assertEqual(repo.push_hook(remote_ref="refs/tags/v1.0.0").returncode, 0)
        repo.edit("Makefile", 'check-tag:\n\t@test "$(TAG)" = v1.0.0\n')
        self.assertEqual(repo.push_hook(remote_ref="refs/tags/v1.0.0").returncode, 0)
        result = repo.push_hook(remote_ref="refs/tags/v2.0.0")
        self.assertEqual(result.returncode, 1)
        self.assertIn("check-tag refused the tag v2.0.0", result.stderr)

    def test_stamp_survives_commit_of_the_same_content(self):
        """id: R-127"""
        repo = GateRepository(self)
        repo.stamp()
        repo.commit_all()
        self.assertEqual(
            run(["sh", "scripts/gates-stamp.sh", "check"], repo.root).returncode, 0
        )

    def test_hash_leaves_the_index_alone(self):
        """id: R-127"""
        repo = GateRepository(self)
        repo.stamp()
        staged = run(["git", "diff", "--cached", "--name-only"], repo.root)
        self.assertEqual(staged.stdout, "")


class GatesTargetTest(unittest.TestCase):
    def test_contract_runs_the_six_gates_in_order_then_stamps(self):
        """id: R-127"""
        text = (SETUP / "contract.mk").read_text(encoding="utf-8")
        recipe = text.split("\ngates: ", 1)[1].split("\n\n", 1)[0]
        lines = [line.strip() for line in recipe.splitlines()[1:]]
        gates = [line.split()[-1] for line in lines if line.startswith("$(THIS_MAKE)")]
        self.assertEqual(
            gates,
            ["editorconfig", "format", "lint", "test", "integration", "coverage"],
        )
        self.assertTrue(lines[-1].endswith("gates-stamp.sh write"))

    def test_setup_installs_the_hook_and_keeps_a_foreign_hook(self):
        """id: R-127"""
        repo = GateRepository(self)
        mk = repo.root / ".claude" / "skills" / "r-project-setup"
        shutil.copytree(SETUP, mk)
        repo.edit("Makefile", "include .claude/skills/r-project-setup/contract.mk\n")
        hook = repo.root / ".git" / "hooks" / "pre-push"
        hook.parent.mkdir(exist_ok=True)
        hook.write_text("#!/bin/sh\necho mine\n", encoding="utf-8")
        run(["make", "git-hooks"], repo.root)
        self.assertEqual(hook.read_text(encoding="utf-8"), "#!/bin/sh\necho mine\n")
        hook.unlink()
        run(
            ["make", "git-hooks", "BOARD_FILES=docs/history/ docs/ROADMAP.md"],
            repo.root,
        )
        text = hook.read_text(encoding="utf-8")
        self.assertIn("r-project-setup pre-push", text)
        self.assertIn('BOARD_FILES="docs/history/ docs/ROADMAP.md"', text)
        sha = repo.commit_all()
        result = subprocess.run(
            ["sh", str(hook)],
            cwd=repo.root,
            input=f"refs/heads/x {sha} refs/heads/x {'0' * 40}\n",
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        again = run(
            ["make", "git-hooks", "BOARD_FILES=docs/history/ docs/ROADMAP.md"],
            repo.root,
        )
        self.assertNotIn("installed", again.stdout)

    def test_the_gate_targets_install_the_hook(self):
        """id: R-127"""
        text = (SETUP / "contract.mk").read_text(encoding="utf-8")
        for target in ("setup", "gates", "test-changed"):
            self.assertIn(f"\n{target}: git-hooks\n", text)


class HostModeTest(unittest.TestCase):
    def dry_run(self, tools):
        """The commands of the gate targets under make -n, in one mode."""
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        skills = root / ".claude" / "skills"
        for name in ("r-project-setup", "r-node", "r-go", "r-jvm"):
            shutil.copytree(ROOT / "skills" / name, skills / name)
        (root / "Makefile").write_text(
            "TEST_CMD = $(PYTHON) -m unittest\n"
            "FORMAT_CMD = $(RUFF) format --check\nLINT_CMD = $(RUFF) check\n"
            "INTEGRATION_CMD = $(NODE) npm test && $(GO) test ./...\n"
            "BUILD_CMD = $(GRADLE_RUN) $(JDK_IMAGE) ./gradlew assemble\n"
            "COVERAGE_CMD = $(COVERAGE_PYTHON) cover.py && REPORT=x $(DIFF_COVER)\n"
            "include .claude/skills/r-project-setup/project.mk\n"
            "include .claude/skills/r-node/node.mk\n"
            "include .claude/skills/r-go/go.mk\n"
            "include .claude/skills/r-jvm/jvm.mk\n",
            encoding="utf-8",
        )
        env = dict(os.environ, HOME=str(root), TOOLS=tools)
        targets = ["editorconfig", "format", "lint", "test", "integration"]
        result = subprocess.run(
            ["make", "-n", *targets, "build", "coverage"],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_host_mode_runs_the_gate_tools_from_path(self):
        """id: R-129"""
        host = self.dry_run("host")
        self.assertNotIn("podman", host)
        for command in (
            "editorconfig-checker",
            "ruff format --check",
            "python3 -m unittest",
            "env npm_config_update_notifier=false npm test",
            "env GOFLAGS=-buildvcs=false go test",
            'exec "$@" \' gradle-host docker.io/library/eclipse-temurin',
            "diff-cover",
        ):
            self.assertIn(command, host)
        self.assertIn("podman run", self.dry_run("podman"))

    def test_host_tools_installs_the_pinned_versions(self):
        """id: R-129"""
        text = (SETUP / "tools.mk").read_text(encoding="utf-8")
        recipe = text.split("\nhost-tools: ## ", 1)[1].split("\n\n", 1)[0]
        for pin in (
            '"ruff==$(RUFF_VERSION)"',
            '"coverage==$(COVERAGE_VERSION)"',
            '"diff-cover==$(DIFF_COVER_VERSION)"',
            '"apm-cli==$(APM_VERSION)"',
            "editorconfig-checker@v$(EDITORCONFIG_VERSION)",
        ):
            self.assertIn(pin, recipe)
        self.assertIn("ifeq ($(TOOLS),host)", text)
        self.assertIn("setup: host-tools", text)


class UndefinedVariableTest(unittest.TestCase):
    def test_contract_targets_warn_about_no_undefined_variable(self):
        """id: R-71"""
        root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        skills = root / ".claude" / "skills"
        shutil.copytree(SETUP, skills / "r-project-setup")
        for name in ("r-project-report/report.mk", "r-record/index.mk"):
            target = skills / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(ROOT / "skills" / name, target)
        (root / "Makefile").write_text(
            "RENDER_DOCS = 1\ninclude .claude/skills/r-project-setup/project.mk\n",
            encoding="utf-8",
        )
        # doctor runs under -n, so a stub podman stands in for the host one.
        stub = root / "stub"
        stub.mkdir()
        (stub / "podman").write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        (stub / "podman").chmod(0o755)
        env = dict(os.environ, HOME=str(root), PATH=f"{stub}:{os.environ['PATH']}")
        result = subprocess.run(
            [
                "make",
                "--warn-undefined-variables",
                "-n",
                "setup",
                "build",
                "test",
                "docs",
                "project-report",
                "gates",
            ],
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertNotIn("undefined variable", result.stderr)


if __name__ == "__main__":
    unittest.main()
