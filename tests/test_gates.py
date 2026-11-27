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

    def push_hook(self):
        return run(["sh", "scripts/pre-push.sh"], self.root, check=False)


class PrePushTest(unittest.TestCase):
    def test_refuses_without_stamp(self):
        """id: R-127"""
        result = GateRepository(self).push_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("make gates", result.stderr)

    def test_refuses_stale_stamp(self):
        """id: R-127"""
        repo = GateRepository(self)
        repo.stamp()
        repo.edit("work.txt", "two\n")
        result = repo.push_hook()
        self.assertEqual(result.returncode, 1)
        self.assertIn("make gates", result.stderr)

    def test_refuses_stale_stamp_after_new_file(self):
        """id: R-127"""
        repo = GateRepository(self)
        repo.stamp()
        repo.edit("extra.txt", "new\n")
        self.assertEqual(repo.push_hook().returncode, 1)

    def test_passes_with_matching_stamp(self):
        """id: R-127"""
        repo = GateRepository(self)
        repo.stamp()
        self.assertEqual(repo.push_hook().returncode, 0)

    def test_stamp_survives_commit_of_the_same_content(self):
        """id: R-127"""
        repo = GateRepository(self)
        repo.stamp()
        run(["git", "add", "work.txt", ".gitignore", "scripts"], repo.root)
        run(["git", "commit", "-q", "-m", "work"], repo.root)
        self.assertEqual(repo.push_hook().returncode, 0)

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
        run(["make", "git-hooks"], repo.root)
        self.assertIn("r-project-setup pre-push", hook.read_text(encoding="utf-8"))
        self.assertEqual(run(["sh", str(hook)], repo.root, check=False).returncode, 1)


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
