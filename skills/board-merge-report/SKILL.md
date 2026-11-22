---
name: board-merge-report
description: Reports which board rows, Decided rows, ADRs, and closed history files can merge, shrink, or go, and writes nothing. Use when the owner asks to cut board duplicates, shorten the board, or review the board for repeated text.
---

The general rules in `CLAUDE.md` apply.

<purpose>
The report lists board text that says one fact twice. The owner reads it once and chooses by id what `board-merge` does. This skill writes no file, no row, and no id.
</purpose>

<inputs>
- The scope is the requirement rows of `docs/REQUIREMENTS.md`, the Decided rows of `docs/DECISIONS.md`, the ADRs in `docs/adr/`, and the files in `docs/history/`.
- Open decision rows, roadmap lines, known issues, and proposals are out of scope.
- If `docs/adr/` does not exist, the ADR part is empty. Say so in one line.
</inputs>

<steps>
1. Run `make toon` and `make board-numbers`. If a target fails, stop. Do not count words, tests, or links yourself. The target prints them for each unit.
2. Read each row, ADR, or history file that the index or the numbers make a candidate. Open a unit in full before you quote it.
3. List the candidates of the four kinds. Read `references/finding-kinds.md` for the test of each kind.
4. Try to refute each candidate. Compare the actor, the repository kind, and the stage of the rows. If one of the three differs, drop the merge. If two rows demand opposite results, report a contradiction and do not merge them.
5. For each finding that stays, take from the numbers the words now, the tests, and the links. Write the words after as about, because only `make board-numbers` measures the text that `board-merge` writes.
6. Write the report. Read `references/report-form.md` for the tables.
</steps>

<rules>
- A merge keeps the id that more tests name. If the tests tie, it keeps the id with more links, then the lower number.
- A merge lists the tests and the links that name the retired id. Those are the ones that `board-merge` rewrites. A frontmatter list that names the id counts as a link. A history file is not counted, because it keeps the retired id as plain text.
- A history file is never merged. It is deleted only when it is closed.
- If a closed history file holds the only copy of a reason, say so in the finding. The reason moves to a row before the file goes.
- A row that no test names is never a covered-by-code finding.
- Do not report an id of an Open row, a roadmap line, a known issue, or a proposal.
- Invent no id. Use only ids that `make board-numbers` printed.
</rules>

<output>
- One table for each finding kind that has findings: Merge, Shorten, Covered by code, Delete history. A kind with none gets one line that says none.
- One line for each contradiction, with the two ids and a short quote of each side.
- Each finding has a number, the ids, the repeated text as a short quote, the words now and after, and, for a merge, the tests and links to rewrite and the id that survives.
- The reply says which units you read in full and how many you did not read.
- The last lines say how to choose, by ids: `merge R-51 R-76`, `shorten R-12`, `cover R-40`, `delete H-2026-11-15-slug`.
</output>

<references>
- `references/finding-kinds.md`: the test of each finding kind and the refutation. Read it in step 3.
- `references/report-form.md`: the columns of each table and a sample. Read it in step 6.
</references>
