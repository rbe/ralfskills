# Requirements of python

The rows that the skill `r-python` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-37"></a>R-37 | Python through Make | in force | `r-python` applies when it is installed and the files are Python. Its `files` are `py`. Do not run `python`, `python3`, `pip`, or a `.py` file on the host. `make test` runs the tests. `make setup` resolves dependencies. CI runs those same targets. A command variable that calls Python uses `=` and `$(PYTHON)`. `:=` expands too early. `TEST_CMD = $(PYTHON) -m unittest` is the shape. Public functions have type hints. A module does one job. The formatter and the linter are both Ruff. `make coverage` runs coverage.py. `PYTHON_IMAGE` is set before the include. When `CLAUDE.md` names a framework, read `references/frameworks.md` beside this skill and the file for that name. Django, Flask, and FastAPI have no reference file yet, and they do not get a second lifecycle. This applies to a product repository that installs `r-python`, and to this collection's own Python. `r-python` owns these rules. `r-project-setup` owns `$(PYTHON)`. |
