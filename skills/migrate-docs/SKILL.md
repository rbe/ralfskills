---
name: migrate-docs
description: Moves an old board onto the roadmap, known issues, decisions, ADRs, and proposals, then deletes the old files. Use when `make old-board` fails or AGENTS.md exists.
---

The general rules in `CLAUDE.md` apply.

<purpose>
This skill moves each still-true fact of the old board to the new board and deletes the old board. The old board is the six paths `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, and `docs/features/`.
</purpose>

<steps>
1. Run `make old-board`, or `make -f .claude/skills/project-setup/old-board.mk old-board` when the Makefile has no include. The target prints each of the six paths that exists, an empty directory too, and fails when one exists. If the target passes and `AGENTS.md` does not exist, stop. There is nothing to migrate.
2. Move each still-true fact once. The rules below name the new place.
3. Ask `record` to retire every old label that was used as an id, also a label whose text you did not copy. Name the old label in the text of the new row or file, so that a person can still find it.
4. If `AGENTS.md` exists, move each constraint that is still true into `CLAUDE.md` and run `git rm AGENTS.md`. If `CLAUDE.md` does not exist, write it with the project title, the one sentence of `README.md` that says what the project is, and the constraints.
5. Run `make old-board-delete` in the same change, or `make -f .claude/skills/migrate-docs/migrate.mk old-board-delete` when the Makefile has no include. The target deletes the six paths and then runs `make old-board`. Run no other skill until it passes.
6. Commit the files that this skill wrote or deleted. Push when the project has a remote `origin`.
</steps>

<rules>
- An open bug or an open audit finding goes to `docs/KNOWN_ISSUES.md`.
- Work that is already in progress goes to `docs/ROADMAP.md`, as ids only.
- A feature or a wave that is a plan for later goes to `docs/proposals/`. The old text is the slice sentence. In `Out of scope` and in the questions, write that `plan` asks them when the proposal is picked up.
- An open choice goes to `docs/DECISIONS.md` as an Open row.
- A small choice that is still in force goes to `docs/DECISIONS.md` as a Decided row of one sentence.
- An architecture or development rule goes to `docs/adr/`, with `adrs:` and `skills:`.
- Do not copy a fixed bug, a shipped feature, or a wave narrative. If one of its sentences is still a rule, that sentence becomes an ADR or a Decided row.
- `project-setup` writes the include of `migrate.mk` after step 5.
</rules>
