# Requirements of r-project-report

The rows that the skill `r-project-report` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-3"></a>R-3 | Generated project report | in force | `make project-report` writes `build/project-report.md` with the requirements-to-tests map, the architecture review, and the development review. `r-review` stops when the target fails, when a part is missing, or when the file was hand-edited. A test with no id, or with an id that is not a requirement id, fails the target. This applies to both, with the switch that a repository with `docs/requirements/` and no ADR file takes its ids from the requirement rows in force. `r-project-report` owns the target, and `r-review` runs it. |
| <a id="r-63"></a>R-63 | Test ids in every language | in force | A test names its requirement with an `id:` line in every language. The line is in the docstring for Python, and in a comment such as `// id: R-1` for the other languages. One reader of the line then serves all tests. A file under `.claude/`, `apm_modules/`, `node_modules/`, `build/`, `dist/`, `.gradle/`, or `.venv/` is not a project test. This applies to both, and `r-project-report` owns the reading. |
| <a id="r-64"></a>R-64 | Project report target in a product | in force | `report.mk` beside the `r-project-report` skill owns the `project-report` target when the skill is installed. Without the skill, `contract.mk` of `r-project-setup` runs `PROJECT_REPORT_CMD` when the project set it, and otherwise fails and names the variable. This applies to a product repository, and `r-project-report` owns `report.mk`. |
