# The target `make python-tooling`

`make python-tooling` does these things, in this order:

1. If `.coveragerc` is missing, it writes `.coveragerc` from `templates/coveragerc` beside this skill. The coverage commands of `templates/Makefile.python` need that file.
2. If `.editorconfig` is missing, it writes `.editorconfig`.
3. It adds `build/`, `__pycache__/`, `*.pyc`, `.ruff_cache/`, and `.venv/` to `.gitignore`.
4. It runs `make format-fix`.

`templates/Makefile.python` holds each command variable, with Ruff, coverage.py, diff-cover, and the changed tests.
