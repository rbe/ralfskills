# Requirements of python

The rows that the skill `r-python` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-37"></a>R-37 | Python through Make | in force | `r-python` applies the Python rules when it is installed and the files are Python. Python runs only through Make in Podman, so the host needs no Python. The formatter and the linter are both Ruff. This applies to a product repository that installs `r-python`, and to this collection's own Python. `r-python` owns these rules, and `r-project-setup` owns `$(PYTHON)`. |
