---
name: migrate-docs
description: Move an old board onto the roadmap, known issues, decisions, ADRs, and proposals, then delete the old files. The only skill that reads docs/BUGS.md, docs/WAVES.md, docs/FEATURES.md, docs/bugs/, docs/waves/, or docs/features/. Run it before any other skill when those paths exist.
---

# Migrate docs

This is the only skill that reads the old board. Every other skill stops while any of those paths exists.

## Steps

1. Test each of `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, and `docs/features/` with `ls -d`. An empty directory exists too, and Git does not list it. If none exists, stop. There is nothing to migrate.
2. Invoke `record` for every new id. `record`'s own stop does not apply to this caller.
3. Move each still-true fact once, using the table below. Then delete the old paths in the same change. Delete an empty directory with `rmdir`. Run `ls -d` on the six paths again. None may exist before any other skill runs.
4. Where `AGENTS.md` exists, fold a constraint that is still true into `CLAUDE.md` and remove `AGENTS.md`. `CLAUDE.md` is the only entry file. When `CLAUDE.md` does not exist yet, write it with the project title, the one sentence of the `README.md` that says what the project is, and the constraints. `project-setup` adds the paragraphs of its template after that text and leaves the text as it is.
5. Ask `record` to retire every old label that was used as an id. A retired id is never issued again. The new row or file names the old label in its text, so a person can still find it. A label whose text was not copied is retired too.
6. `record` needs `make ids` and `make ids-retire`. In a project whose Makefile has no include yet, run `make -f .claude/skills/record/index.mk ids` and `make -f .claude/skills/record/index.mk ids-retire ID=<id>`. `project-setup` writes the include after this skill has deleted the old paths.
7. Commit the new board on the default branch and push. The onboarding of a project is not a slice.

## Where the old text goes

| Old content | New home |
| --- | --- |
| Open bug or open audit finding | `docs/KNOWN_ISSUES.md` |
| Work that is already in progress | `docs/ROADMAP.md`, ids only |
| A feature or wave that is a plan for later | `docs/proposals/`. The old text is the slice sentence. `Out of scope` and the questions say that `plan` asks them when the proposal is picked up |
| Open choice | `docs/DECISIONS.md`, Open |
| Small choice still in force | `docs/DECISIONS.md`, Decided, one sentence |
| Architecture or development rule | `docs/adr/`, with `adrs:` and `skills:` |
| Fixed bug, shipped feature, wave narrative | Not copied. A sentence that is still a rule becomes an ADR or a Decided line |

Do not leave the old files in place beside the new board. Do not create `docs/BUGS.md`, `docs/WAVES.md`, or `docs/FEATURES.md`.
