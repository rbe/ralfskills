# The target `make python-tooling`

`python.mk` beside this skill has the target `make python-tooling`. The Makefile includes it with `include .claude/skills/r-python/python.mk` after `project.mk` or `sdlc.mk`. The target does these things, in this order:

1. If `.coveragerc` is missing, it writes `.coveragerc` from `templates/coveragerc` beside this skill. The coverage commands of `templates/Makefile.python` need that file.
2. It adds `build/`, `__pycache__/`, `*.pyc`, `.ruff_cache/`, and `.venv/` to `.gitignore`.
3. It runs `make format-fix`.

`templates/Makefile.python` holds each command variable, with Ruff, coverage.py, diff-cover, and the changed tests.

A Python project with no dependency has no manifest.
