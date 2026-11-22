# The target `make python-tooling`

`make python-tooling` does these things, in this order:

1. If `.coveragerc` is missing, it writes `.coveragerc` from `templates/coveragerc` beside this skill. The coverage commands of `templates/Makefile.python` need that file.
2. It adds `build/`, `__pycache__/`, `*.pyc`, `.ruff_cache/`, and `.venv/` to `.gitignore`.
3. It runs `make format-fix`.

`templates/Makefile.python` holds each command variable, with Ruff, coverage.py, diff-cover, and the changed tests.

A Python project with no dependency has no manifest.
