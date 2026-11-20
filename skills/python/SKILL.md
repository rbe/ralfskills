---
name: python
description: Python. Use when python is installed and the files in hand are Python. Tests run through make. Type hints are on public signatures. The stage skill still applies. A framework named in CLAUDE.md is not a reason to skip this skill.
kind: language
files: [py]
---

# Python

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step.
2. Invoke `record` before creating an id or a document. A write that skips `record` fails this step.
3. Do the work below. `develop` invokes this skill for Python files.
4. Ask `record` to add one line under Develop naming `python`. Do not open a second history file.

## Work

1. Do not run `python`, `python3`, `pip`, or a `.py` file on the host. An agent runs Python on this machine through Make. `make py ARGS='...'` is a one-off command. `make test` runs the tests. `make setup` resolves dependencies. CI runs those same targets. The container is Podman on the machine where Make is running.
2. A command variable that calls Python uses `=` and `$(PYTHON)`, so it expands after `podman-python.mk` is included. `TEST_CMD = $(PYTHON) -m unittest` is the shape. `:=` expands too early.
3. Public functions have type hints. A change adds the hints to each public function it touches. A module does one job.
4. `templates/Makefile.python` beside this skill is the Makefile of a Python project: each command variable, with Ruff, coverage.py, diff-cover, and the changed tests. `templates/coveragerc` is the `.coveragerc` those commands need. `project-setup` copies them to `Makefile` and `.coveragerc`. Do not write these commands again from memory. Ruff does not read `.claude/`, `apm_modules/`, or `docs/`. `.gitignore` has the lines `__pycache__/` and `*.pyc`. `UNIT_TESTS` in the template is every file `tests/test_*.py`. A new test file runs with no change to the Makefile. A test names its requirement in the docstring of the test: `"""id: D-1"""`. A test file has no `if __name__ == "__main__":` block. `make test` runs it, and the diff report counts each line of a test file. A target the project already has, such as `run`, keeps its name and uses `$(PYTHON)`.
5. The formatter is Ruff (`ruff format`). The linter is Ruff (`ruff check`). Do not write a linter. Do not add a second formatter or a second linter.
6. `make coverage` runs coverage.py and then diff-cover. The report is the lines this change touched. Do not use a repository-wide percentage.
7. A framework named in `CLAUDE.md` is read as a project skill. It does not replace this skill.
8. `PYTHON_IMAGE` is set before the include. The default is in `project-setup`. XDG paths and what a shipment may contain are `project-setup`.
