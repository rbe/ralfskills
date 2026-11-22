# Id kinds

- Roadmap row (work to do): one table row, id `W-` plus a number, from `W-1`. One id form serves the three kinds `feature`, `defect`, and `question`, because the column `kind` already holds the kind. A row is not done. `record` deletes it and retires its id when the slice closes.
- Requirement row: one row of `docs/REQUIREMENTS.md`, id `R-` plus a number, from `R-1`. A repository with no `docs/adr/` gives the row a status: `planned` or `in force`.
- ADR: `docs/adr/<id>.md`, id `ADR-` plus four digits, from `ADR-0001`. The status is `Accepted` or `Superseded`.
- Proposal (the plan of one roadmap row): `docs/proposals/<id>.md`, id `P-` plus a number, from `P-1`. The status is `open`, `started`, or `done`.
- History file (a started slice): `docs/history/<id>.md`, id `H-` plus the day the file is created and a slug, as `H-2026-11-20-slugify`. The status is `started` or `closed`. The branch of the slice has the slug as its name.
