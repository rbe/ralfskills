#!/usr/bin/env python3
"""The guard hooks: each script refuses its command and lets the rest pass."""

import json
import subprocess
import unittest
from pathlib import Path

HOOKS = Path(__file__).resolve().parents[1] / "hooks"
SCRIPTS = HOOKS / "scripts"


def run_hook(script, hook_input):
    """Run one hook script with the hook input on stdin."""
    return subprocess.run(
        ["sh", str(SCRIPTS / script)],
        input=hook_input,
        capture_output=True,
        text=True,
        check=False,
    )


def bash_input(command):
    """The PreToolUse input of the Bash tool for one command."""
    return json.dumps(
        {
            "hook_event_name": "PreToolUse",
            "tool_name": "Bash",
            "tool_input": {"command": command, "description": "a step"},
        }
    )


class GuardTest(unittest.TestCase):
    script = ""

    def decision(self, command):
        result = run_hook(self.script, bash_input(command))
        self.assertEqual(result.returncode, 0, result.stderr)
        if not result.stdout.strip():
            return "allow"
        return json.loads(result.stdout)["hookSpecificOutput"]["permissionDecision"]

    def assert_denied(self, *commands):
        for command in commands:
            with self.subTest(command=command):
                self.assertEqual(self.decision(command), "deny")

    def assert_allowed(self, *commands):
        for command in commands:
            with self.subTest(command=command):
                self.assertEqual(self.decision(command), "allow")


class BareGitAddTest(GuardTest):
    script = "block-bare-git-add.sh"

    def test_a_command_that_stages_the_whole_working_copy_is_refused(self):
        """id: R-124"""
        self.assert_denied(
            "git add -A",
            "git add .",
            "git add --all",
            "git add -u",
            "git add :/",
            "git add -A .",
            "sudo git add -A",
            "git -C repo add .",
            "cd repo && git add -A && git commit -m 'x'",
            "echo start\ngit add .",
            'git commit -am "fix"',
            "git commit -a -m fix",
            "git commit --all",
        )

    def test_a_command_that_names_its_files_passes(self):
        """id: R-124"""
        self.assert_allowed(
            "git add src/ tests/",
            "git add -A src/ tests/",
            "git add -u docs/",
            "git add README.md",
            'git commit -m "add -A to the docs"',
            "git commit --amend --no-edit",
            "git status",
            "ls -a",
        )

    def test_the_refusal_names_the_staging_rule(self):
        """id: R-124"""
        result = run_hook(self.script, bash_input("git add -A"))
        reason = json.loads(result.stdout)["hookSpecificOutput"]
        self.assertIn("R-114", reason["permissionDecisionReason"])


class PythonFileWriteTest(GuardTest):
    script = "block-python-file-write.sh"

    def test_an_inline_python_script_that_writes_a_project_file_is_refused(self):
        """id: R-124"""
        self.assert_denied(
            'python3 - <<EOF\nfrom pathlib import Path\np = Path("src/app.py")\n'
            'p.write_text(p.read_text().replace("a", "b"))\nEOF',
            "python -c \"open('docs/x.md', 'w').write('x')\"",
            "uv run python -c \"open('./tests/t.py', 'a').write('x')\"",
            "make py ARGS=\"-c \\\"open('skills/r-x/SKILL.md', 'w').write('x')\\\"\"",
        )

    def test_a_reading_script_and_a_script_that_writes_build_output_pass(self):
        """id: R-124"""
        self.assert_allowed(
            "python3 -c \"print(open('src/app.py').read())\"",
            "python3 -c \"import sys; sys.stdout.write(open('src/app.py').read())\"",
            "python3 -c \"open('build/report.txt', 'w').write('x')\"",
            "python3 -c \"open('/tmp/x.txt', 'w').write('x')\"",
            "sed -n 1,5p src/app.py",
            "echo write_text src/app.py",
        )


class HookInputTest(unittest.TestCase):
    def test_a_hook_input_without_a_command_blocks_with_a_message(self):
        """id: R-124"""
        for script in ("block-bare-git-add.sh", "block-python-file-write.sh"):
            with self.subTest(script=script):
                result = run_hook(script, '{"tool_input": {"cmd": "ls"}}')
                self.assertEqual(result.returncode, 2)
                self.assertIn("tool_input.command", result.stderr)

    def test_a_command_in_the_description_does_not_count(self):
        """id: R-124"""
        hook_input = json.dumps(
            {"tool_input": {"description": "git add -A", "command": "ls"}}
        )
        result = run_hook("block-bare-git-add.sh", hook_input)
        self.assertEqual((result.returncode, result.stdout), (0, ""))

    def test_the_hook_file_runs_both_scripts_before_each_bash_command(self):
        """id: R-124"""
        hooks = json.loads((HOOKS / "r-guards.json").read_text(encoding="utf-8"))
        (group,) = hooks["hooks"]["PreToolUse"]
        self.assertEqual(group["matcher"], "Bash")
        commands = [hook["command"] for hook in group["hooks"]]
        for script in ("block-bare-git-add.sh", "block-python-file-write.sh"):
            self.assertIn(
                f'sh "${{CLAUDE_PLUGIN_ROOT}}/hooks/scripts/{script}"', commands
            )


if __name__ == "__main__":
    unittest.main()
