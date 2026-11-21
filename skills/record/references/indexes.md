# Indexes and the decision log

## `make toon`

| File | Columns | What it lists |
| --- | --- | --- |
| `docs/adr/index.toon` | `id`, `status`, `title`, `adrs`, `skills`, `decisions` | ADR frontmatter. `plan` opens one ADR when the id matches |
| `docs/requirements-index.toon` | `id`, `title` | The requirements list, when that list is the board and `docs/adr/` has no ADR file. The list has the columns Id, Title, and Statement. An agent opens the list for the statement |
| `docs/skill-index.toon` | `name`, `kind`, `order`, `files`, `names` | Installed skills whose frontmatter `kind` is `language` or `check` |

- A repository that keeps `docs/REQUIREMENTS.md` and no `docs/adr/` gets `docs/requirements-index.toon` and the skill index. `make toon` does not create `docs/adr/` there.
- If a repository has an ADR file and `docs/REQUIREMENTS.md`, `make toon` writes the ADR index.
- `project.mk` and `sdlc.mk` include `.claude/skills/record/index.mk`. A Makefile that includes one of them has the targets `toon`, `ids`, `ids-retire`, `links`, `links-check`, and `decision-log`.
- `make setup` runs `toon` first when that include is present.
- `toon` and `ids` call `$(PYTHON)` from `project-setup`. `make ids` checks ids and writes no index.

## Skill index

- The skill index lists the installed set under `.claude/skills/`. In the skill collection, before install, it lists `skills/`.
- The index does not copy skill prose.
- A language skill sets `files` to extensions and `names` to exact filenames such as `Makefile`. `develop` invokes the language row whose `files` or `names` match the files in hand.
- A check skill sets `order`. `plan` and `review` follow that order.

## Why `make toon` fails

- The `name` in the frontmatter of a skill differs from its directory.
- A frontmatter value has a colon followed by a space, or a space followed by `#`. APM reads the frontmatter as YAML and refuses to install such a skill.

## `make decision-log`

- `make decision-log` writes `build/decision-log.md`. A person reads this document.
- It lists each accepted ADR with its rule and its reason, each Decided row, each Open row, and each superseded ADR with the ADR that replaced it.
- A repository that keeps `docs/REQUIREMENTS.md` and has no ADR file gets that list in the log.
- A repository that renders docs uses this file as a source.
- The log does not replace the ADR that an agent opens.
