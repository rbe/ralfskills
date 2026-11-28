# The Makefile of a Python project

Command variables:

- A command variable that calls Python uses `=` and `$(PYTHON)`. The variable then expands after `podman-python.mk` is included.
- The shape is `TEST_CMD = $(PYTHON) -m unittest`.
- `:=` expands before the include, and `$(PYTHON)` is then empty.

pytest:

- If the tests are pytest functions, `unittest` does not collect them. `pytest_cover.py` of `r-project-report` then replaces `cover_tests.py` and `changed_tests.py`.
- `COVERAGE_CMD` runs `$(PYTHON) .claude/skills/r-project-report/scripts/pytest_cover.py cover`, then diff-cover. `TEST_CHANGED_CMD` runs `pytest_cover.py changed`.
- Arguments after `cover` or `changed` go to pytest. The image needs pytest and coverage.py.

Image:

- Set `PYTHON_IMAGE` before the include. `r-project-setup` gives the default.

Targets:

- A target that the project already has, such as `run`, keeps its name and uses `$(PYTHON)`.

A `src/` layout:

- A project with a `src/` layout needs no change to the Makefile.
- `$(PYTHON)` sets `PYTHONPATH=/work/src`.
- `make coverage` puts `src/` on the path of the test run.
- Python imports the package from `src/` with no install step.
