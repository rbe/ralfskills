---
name: record
description: Assigns ids and writes the board documents, the indexes, and the decision log. Use before creating or editing a roadmap line, a known issue, a decision, an ADR, a proposal, or a history file, and to close a task. Rejects a duplicate or retired id.
---

The general rules in `CLAUDE.md` apply.

<purpose>
The agent writes each document by hand from a template in `templates/` beside this skill, and `make ids` checks the ids.
</purpose>

<mode name="write">
<steps>
1. Run `make ids`. If it exits non-zero, an id is a duplicate: stop and do not write the document. Before the Makefile includes `project.mk` or `sdlc.mk`, run `make -f .claude/skills/record/index.mk <target>`, with `PYTHON_IMAGE=<image>` on that line to replace the default image.
2. For a new item, take the next id of its kind from the rules below.
3. If the document does not exist, copy its template: `ROADMAP.md`, `KNOWN_ISSUES.md`, `DECISIONS.md`, `adr.md`, `proposal.md`, or `history.md`. Keep the layout. Before you write frontmatter or a table row for the first time in a task, read `references/documents.md`.
4. If the document is an ADR, read `references/adr.md` and follow it.
5. If the caller asks for a new history file, read `references/history.md`. Write the file from `templates/history.md` and add one roadmap line with the history id.
6. If a stage asks for its section, write it in sentences: what the stage did, each gate with its result, and what the stage left alone. Replace `Not invoked yet.` and keep the heading. Update the frontmatter lists.
7. If another skill asks for its line, add the line to the section of the stage that runs, as `python: the language skill for the Python files.` or `security: no listener, no secret.` Add the skill name to `skills` in the frontmatter.
8. If a document or a table row is deleted, retire its id.
9. If ADR frontmatter, the requirements list, or the set of installed skills changed, run `make toon`. If `make toon` fails, read `references/indexes.md`.
</steps>
</mode>

<mode name="close">
<steps>
1. If the Plan, the Develop, or the Review section of the history file is still `Not invoked yet.`, stop.
2. Set the history status to `closed`.
3. Delete the roadmap line that cites this history id.
4. If the slice started from a proposal, set the proposal status to `done`.
5. If the slice fixed a known issue, delete that row and retire its id. If a test still names that id, stop: the test must name a rule, as the Tests rules say. Write that Decided row when there is none.
6. Leave each ADR and each Decided row. They stay in force.
7. In a repository that keeps `docs/REQUIREMENTS.md` and no `docs/ROADMAP.md`, delete the Open row for this task and retire its id.
</steps>
<rules>
- A task whose work waits stays open. A slice that is done and waits only for the merge of the owner is closed on its branch.
</rules>
</mode>

<rules>
Ids:
- Do the id check in this skill. Do not delegate it, and do not accept an id that the caller invented in prose.
- The next number of a kind is one above the highest number of that kind in the documents and in `docs/ids.yaml`.
- Write an id as plain text. After a document under `docs/` changes, run `make links`. It makes each id a link.
- To retire an id, run `make ids-retire ID=<id>`, then `make links`. A retired id is never issued again. `make ids-retire` creates `docs/ids.yaml` at the first retire.
- Roadmap line (work in progress): `- H-2026-11-20-slugify`, or `- H-2026-11-20-slugify P-1` when the slice started from a proposal.
- Known issue (a defect): one table row, id `K-` plus a number, from `K-1`.
- Decision (a small choice): one table row, id `D-` plus a number, from `D-1`. The status is Open or Decided. A Decided row is one sentence.
- ADR: `docs/adr/<id>.md`, id `ADR-` plus four digits, from `ADR-0001`. The status is `Accepted` or `Superseded`.
- Proposal (work for later): `docs/proposals/<id>.md`, id `P-` plus a number, from `P-1`. The status is `open`, `started`, or `done`. The proposals are the backlog.
- History file (a started slice): `docs/history/<id>.md`, id `H-` plus the day the file is created and a slug, as `H-2026-11-20-slugify`. The status is `started` or `closed`. The branch of the slice has the slug as its name.

History:
- One task has one history file.
- A deferred slice is a proposal and has no history file.
- If a proposal is picked up, set `proposals:` in the new history file to that id, set the proposal status to `started`, and write both ids in the roadmap line.
- Reject a history file that is missing the heading Plan, Develop, Review, or Release.
- Frontmatter lists of a history file: `skills` lists each skill the slice used, which are the stages, the language skills, and the subskills. `decisions`, `adrs`, and `issues` list the ids the slice wrote, fixed, or proves with a test. `proposals` lists only the proposal the slice started from. A proposal that the slice wrote for a later part is named in the Plan section.
- While the task is open, a Develop, Review, or Release section whose stage did not run keeps `Not invoked yet.` When the task closes or waits, that section is one sentence that says why the stage was not invoked, as `Not invoked: this slice does not ship.`
- A subskill that is not installed is one line in the Review section.
- An agent on another task opens a history file only when an id names it.
- A skill that is not a stage asks `record` to add one line that names the skill to the open section. That skill opens no history file. If no history file is open, it adds no line.

Tests:
- `make ids` matches the `id:` line in the header or the metadata of a test.
- A roadmap line and a known issue are work, not rules, and their ids are retired. A test does not name them.
- A test for a fixed known issue names the ADR or the Decided row that states the fixed behaviour.
- The test name states what the system does when the requirement holds. The test does not build a path to the document.
- In a Python test the line is the docstring: `"""id: D-1"""`. In a JavaScript, TypeScript, Java, Groovy, Kotlin, or Go test file the line is a comment: `// id: D-1`. One file may have one line for each id it proves.
</rules>

<references>
- `references/documents.md`: the layouts the scripts read, the frontmatter keys, and what `make links` writes. Read it before the first write of frontmatter or of a table row in a task, and when `make links-check` fails.
- `references/adr.md`: the sections of an ADR, its status, and `skills`. Read it before you write or supersede an ADR.
- `references/history.md`: the content of each history section. Read it before you create a history file, and when you are not sure what a section holds.
- `references/indexes.md`: the files `make toon` and `make decision-log` write, their columns, and why `make toon` fails. Read it when `make toon` fails or when a question is about an index or the decision log.
</references>
