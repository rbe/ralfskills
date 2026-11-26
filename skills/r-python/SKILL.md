---
name: r-python
description: Python. Applies the Python rules to a change. Use when r-python is installed and the files in hand are Python. A framework named in CLAUDE.md is a reference file beside this skill. The stage skill still applies.
kind: language
files: [py]
---

The general rules in `CLAUDE.md` apply.

<purpose>
This skill gives the Make targets and the code rules for Python files.
</purpose>

<steps>
1. If the project is new or `.coveragerc` is missing, read `references/tooling.md`, then run `make python-tooling`.
2. If `CLAUDE.md` names a framework, read `references/frameworks.md` and the file in `references/` that has the name of the framework.
3. Edit the Python files by the rules below.
4. If a one-off Python command is necessary, run `make py ARGS='...'`.
</steps>

<rules>
- In a recipe, `$(PYTHON)` runs Python in Podman. `make setup` resolves the dependencies.
- The formatter is Ruff (`ruff format`). The linter is Ruff (`ruff check`). Ruff does not read `.claude/`, `apm_modules/`, or `docs/`.
- `make coverage` runs coverage.py and then diff-cover.
- `UNIT_TESTS` in the template is every file `tests/test_*.py` and `tests/*/test_*.py`, so `make test` runs a new test file with no change to the Makefile.
- A test file has no `if __name__ == "__main__":` block, because the diff report counts each line of a test file.
- A public function has type hints. A change adds the hints to each public function that it touches.
- A module has one job.
- A framework file does not replace this skill or the stage skill.
</rules>

<references>
- `references/tooling.md`: read it before `make python-tooling` runs.
- `references/frameworks.md` and a file named by a framework: read them when `CLAUDE.md` names that framework.
- `references/makefile.md`: read it when the change touches a command variable, `PYTHON_IMAGE`, a target of the Makefile, or a `src/` layout.
</references>
