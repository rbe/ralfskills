---
name: record
description: Assign document ids and write the board. Use before creating or editing a roadmap line, a known issue, a decision, an ADR, a proposal, or a history file, and to close a task. Reject a duplicate id, including a retired one. Write the ADR index and the decision log. Other skills invoke this skill by name.
---

# Record

This skill is the only writer of ids and of the board. A stage that writes a document without this skill has failed its step.

## Steps

1. If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, stop. Name `migrate-docs`. Do not take a later step. `migrate-docs` is the one caller allowed to invoke this skill while those paths still exist.
2. This skill is `record`. Do not delegate the id check to another skill.
3. Do the work below for the document the caller named.
4. Reject a history file that is missing Plan, Develop, Review, or Release.

## Where a fact goes

| Kind | Home | Id |
| --- | --- | --- |
| In progress | `docs/ROADMAP.md` | Cites a history id and, when there is one, a proposal id. One line. No grill |
| Defect | `docs/KNOWN_ISSUES.md` | `id:` in the entry. Delete the entry when the fix lands, then retire the id |
| Small choice | `docs/DECISIONS.md` | Open, or Decided as one sentence |
| Architecture or development rule | `docs/adr/<id>.md` | `ADR-` plus four digits |
| Implement later | `docs/proposals/<id>.md` | `P-` plus a number. This is the backlog |
| Implement now | `docs/history/<id>.md` | `H-` plus the date and a slug |

A product repository keeps in-progress work in `docs/ROADMAP.md` and a rule in `docs/adr/`. This collection is not a product repository. Each requirement is one row in `docs/REQUIREMENTS.md`. An Open row in `docs/DECISIONS.md` is work that is not finished. A Decided row is a choice in force. This collection does not keep `docs/ROADMAP.md` or `docs/adr/`.

`plan` reads these before it asks. It does not ask a question an accepted ADR, a Decided entry, or an open proposal already answered.

## Links

Keys are the plural of the kind. A document names ids. It does not build a path to another document.

```yaml
id: ADR-0004
title: Listen on localhost
status: Accepted
adrs: [ADR-0001]
skills: [security, review]
decisions: [D-12]
proposals: []
issues: []
supersedes: []
```

A decision, a proposal, and a history file use the same keys.

## ADRs

In a product repository, when the owner answers a choice that is expensive to reverse, `plan` asks this skill for an ADR id. This skill writes `docs/adr/<id>.md` with the status `Accepted`. The Plan section cites that id. A choice that is cheap to reverse stays a Decided entry.

An ADR body has the section `## Rule` and the section `## Why`. Rule is what an agent must do or must not do, in sentences `review` can check. Why is the reason, and the options that were not chosen. An ADR that replaces a skill rule also has the section `## Divergence`. An ADR is short. It does not copy the grill.

This skill owns the ADR status. The values are `Accepted` and `Superseded`. A new ADR names the ADR it replaces in `supersedes`. This skill then sets the status of the replaced ADR to `Superseded`. `plan`, `develop`, and `review` follow only an accepted ADR. The project report does not list a superseded ADR as an id with no test.

`skills` names each skill whose work the ADR governs. `develop` and `review` open an accepted ADR when `skills` names a skill the slice uses. An ADR with an empty `skills` list has no reader.

An accepted ADR replaces a skill rule only when the ADR is a divergence. A divergence names the rule, what differs, and why. An ADR that differs from a skill rule and does not name these three is a finding in `review`. What `github-pipeline` says is not a divergence stays not allowed.

## Ids

Before writing an id, run `make ids`. It reads every `id:` under `docs/` and the retired list in `docs/ids.yaml`. A match exits non-zero. Do not write the document.

`docs/ids.yaml` is:

```yaml
retired: []
```

Deleting a document runs `make ids-retire ID=<id>`. A retired id is never issued again. The caller does not invent an id in prose.

## History

One file per task. `plan` creates it when implementation starts. `develop` asks for it when the request named a file or a failing test and `plan` did not run. Later skills extend that file. A deferred slice is a proposal and has no history file yet.

When a proposal is picked up, create the history file, set `proposals:` to that id, and set the proposal status to `started`. Add one roadmap line with both ids. Do not copy the grill into the roadmap.

Every history file has these sections. A missing heading is a failed step.

| Section | When the stage ran | When it did not |
| --- | --- | --- |
| Plan | Questions and answers | One sentence. `plan` writes this section when it creates the file |
| Develop | What changed, and which language skill was used | `Not invoked yet.` while the task is open. When the task closes or waits, one sentence |
| Review | Gates, subskill checks, findings, what was left alone | The same pattern. A subskill that is not installed is one line: `security: not installed` |
| Release | What shipped | `Not invoked: this slice does not ship.` or `Not invoked yet.` |

An agent on another task opens a history file only when an id names it.

## Closing a task

`release` asks this skill to close the task, when the slice shipped and when it does not ship. A task that waits stays open.

1. Stop when a section of the history file is still `Not invoked yet.` Do not take a later step.
2. Set the history status to `closed`. The status of a history file is `started` or `closed`.
3. Delete the roadmap line that cites this history id.
4. When the slice started from a proposal, set the proposal status to `done`. The status of a proposal is `open`, `started`, or `done`.
5. When the slice fixed a known issue, delete that entry and retire its id.
6. An ADR and a Decided entry stay. They are in force after the task closes.
7. In a repository that keeps `docs/REQUIREMENTS.md` and does not keep `docs/ROADMAP.md`, delete the Open row for this task and retire its id.

## Tests

A test names the requirement it proves with `id:` in its header or metadata. That is the same line this skill matches. The id is a roadmap id, a known-issue id, an ADR id, or a decision id. When the repository keeps `docs/REQUIREMENTS.md` and does not keep `docs/adr/`, the id is a row in that list. The test name states what the system does when that requirement holds. The test does not build a path to the document.

## Indexes

`make toon` writes the ADR index and the skill index through `$(PYTHON)`. A repository that keeps `docs/REQUIREMENTS.md` and does not keep `docs/adr/` gets `docs/requirements-index.toon` from that list, and it still gets the skill index. `make toon` does not create `docs/adr/` there. When a repository has both an ADR file and `docs/REQUIREMENTS.md`, `make toon` writes the ADR index. `project.mk` and `sdlc.mk` include `.claude/skills/record/index.mk`, so a project Makefile that includes either of those already has the target. `make setup` runs `toon` first when that include is present.

Make is the interface. Python reads the frontmatter, because a makefile recipe is the wrong place for that parser. `toon` and `ids` call `$(PYTHON)` from `project-setup`. That is Podman on the machine where Make runs. The host does not need Python.

Run `make toon` after a skill is installed or removed, after ADR frontmatter changes, after the requirements list changes, and before `plan`, `develop`, or `review` reads an index. Hand-editing an index is a defect.

| File | Columns | What it lists |
| --- | --- | --- |
| `docs/adr/index.toon` | `id`, `status`, `title`, `adrs`, `skills`, `decisions` | ADR frontmatter. `plan` opens one ADR when the id matches |
| `docs/requirements-index.toon` | `id`, `title` | The requirements list, when that list is the board and `docs/adr/` has no ADR file. The list has the columns Id, Title, and Statement. An agent opens the list for the statement |
| `docs/skill-index.toon` | `name`, `kind`, `order`, `files`, `names` | Installed skills whose frontmatter `kind` is `language` or `check` |

The skill index is the installed set under `.claude/skills/`. In this collection, before install, it is `skills/`. It does not copy skill prose. The `name` in a skill's frontmatter matches its directory. `make toon` fails when a name differs. It also fails when a frontmatter value has a colon followed by a space, or a ` #`. APM reads the frontmatter as YAML and refuses to install such a skill. A language skill sets `files` to extensions and `names` to exact filenames such as `Makefile`. A check skill sets `order`. `plan` and `review` follow that order. `develop` invokes the language row whose `files` or `names` match the files in hand.

## Decision log

`make decision-log` writes `build/decision-log.md`. It is the document a person reads. It lists each accepted ADR with its rule and its reason, each Decided entry, each Open entry, and each superseded ADR with the ADR that replaced it. A repository that keeps `docs/REQUIREMENTS.md` and has no ADR file gets that list in the log. Hand-editing the log is a defect. A repository that renders docs uses this file as a source. The log does not replace the ADR an agent opens.

`make ids` is separate. It checks ids. It does not write a TOON file. It uses `$(PYTHON)`, the same Podman command as `make toon`.
