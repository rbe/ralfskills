# Glossary

Each row is one term that the user and the agents use for one thing. `r-record` writes each row. The communication contract says when an agent reads this file.

| Term | Meaning | Path |
| --- | --- | --- |
| ADR | An architecture decision record: one architecture or development rule of a product repository. | `docs/adr/` in a product repository |
| board | The documents under `docs/` that hold the work, the rules, the plans, and the history. | `docs/` |
| gate | One of the six Make targets that must pass before a change is done. | `skills/r-project-setup/rules.md` |
| glossary | This file: one row for each term that the user and the agents use. | `docs/glossary.md` |
| history file | The report of one started slice, with the sections Plan, Develop, Review, and Release. | `docs/history/` |
| owner | The human who decides the direction and answers the questions of a project. | none |
| proposal | The plan of one roadmap row, for work that waits. | `docs/proposals/` in a product repository |
| requirement row | One rule or one piece of open work of this collection, with the status `in force` or `planned`. | `docs/requirements/` |
| roadmap row | One piece of work, one defect, or one open question of a product repository. | `docs/ROADMAP.md` in a product repository |
| skill | One directory `skills/r-<name>/` with a `SKILL.md` that an agent loads for one kind of work. | `skills/` |
| slice | One change that ships on its own, from plan to release. | none |
| stage | One of the four skills `r-plan`, `r-develop`, `r-review`, and `r-release`, run in this order. | `skills/` |
