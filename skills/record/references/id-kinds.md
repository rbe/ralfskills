# Id kinds

- Roadmap line (work in progress): `- H-2026-11-20-slugify`, or `- H-2026-11-20-slugify P-1` when the slice started from a proposal.
- Known issue (a defect): one table row, id `K-` plus a number, from `K-1`.
- Decision (a small choice): one table row, id `D-` plus a number, from `D-1`. The status is Open or Decided. A Decided row is one sentence.
- ADR: `docs/adr/<id>.md`, id `ADR-` plus four digits, from `ADR-0001`. The status is `Accepted` or `Superseded`.
- Proposal (work for later): `docs/proposals/<id>.md`, id `P-` plus a number, from `P-1`. The status is `open`, `started`, or `done`. The proposals are the backlog.
- History file (a started slice): `docs/history/<id>.md`, id `H-` plus the day the file is created and a slug, as `H-2026-11-20-slugify`. The status is `started` or `closed`. The branch of the slice has the slug as its name.
