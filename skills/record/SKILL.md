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
| In progress | `docs/ROADMAP.md` | One line: `- H-2026-11-20-slugify`, and the proposal id when there is one. No grill |
| Defect | `docs/KNOWN_ISSUES.md` | One table row. The id is `K-` plus a number, from `K-1`. Delete the row when the fix lands, then retire the id |
| Small choice | `docs/DECISIONS.md` | One table row. The id is `D-` plus a number, from `D-1`. The status is Open or Decided. A Decided row is one sentence |
| Architecture or development rule | `docs/adr/<id>.md` | `ADR-` plus four digits, from `ADR-0001` |
| Implement later | `docs/proposals/<id>.md` | `P-` plus a number, from `P-1`. This is the backlog |
| Implement now | `docs/history/<id>.md` | `H-` plus the date and a slug, as `H-2026-11-20-slugify`. The branch of the slice has the slug as its name |

A product repository keeps in-progress work in `docs/ROADMAP.md` and a rule in `docs/adr/`. This collection is not a product repository. Each requirement is one row in `docs/REQUIREMENTS.md`. An Open row in `docs/DECISIONS.md` is work that is not finished. A Decided row is a choice in force. This collection does not keep `docs/ROADMAP.md` or `docs/adr/`.

`templates/` beside this skill has one template for each document: `ROADMAP.md`, `KNOWN_ISSUES.md`, `DECISIONS.md`, `adr.md`, `proposal.md`, and `history.md`. Copy the template at the first write, and keep its layout. This skill has no tool that writes a document. The agent writes each document by hand from its template, and `make ids` checks the ids. The scripts read these layouts: a table row for a decision and a known issue, and a frontmatter block for an ADR, a proposal, and a history file. Write a list in the frontmatter on one line, as `skills: [a, b]`. `make ids-retire` creates `docs/ids.yaml` at the first retire. Do not write it by hand. The next number of a kind is one above the highest number of that kind in the documents and in `docs/ids.yaml`. The date in a history id is the day the file is created.

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

A decision, a proposal, and a history file use the same keys. In a history file, `skills` lists each skill the slice used: the stages, the language skills, and the subskills. A history file may still cite an id that was retired later.

The open history section is the section of the stage that runs: Plan, Develop, Review, or Release. A skill that adds one line adds it there, as `python: the language skill for the Python files.` or `security: no listener, no secret.` The same step adds the skill name to `skills` in the frontmatter. `decisions`, `adrs`, and `issues` list the ids the slice wrote, fixed, or proves with a test. `proposals` lists only the proposal the slice started from. A proposal the slice wrote for a later part is named in the Plan section.

## ADRs

In a product repository, when the owner answers a choice that is expensive to reverse, `plan` asks this skill for an ADR id. This skill writes `docs/adr/<id>.md` with the status `Accepted`. The Plan section cites that id. A choice that is cheap to reverse stays a Decided entry.

An ADR body has the section `## Rule` and the section `## Why`. Rule is what an agent must do or must not do, in sentences `review` can check. Why is the reason, and the options that were not chosen. An ADR that replaces a skill rule also has the section `## Divergence`. An ADR is short. It does not copy the grill.

This skill owns the ADR status. The values are `Accepted` and `Superseded`. A new ADR names the ADR it replaces in `supersedes`. This skill then sets the status of the replaced ADR to `Superseded`. `plan`, `develop`, and `review` follow only an accepted ADR. The project report does not list a superseded ADR as an id with no test.

`skills` names each skill whose work the ADR governs. Each name is an installed skill: a stage, a language skill, or a subskill. A rule for every change names `develop` and `review`, the two stages every slice uses, as `skills: [develop, review]`. A rule for one language names that language skill too, as `skills: [python, develop, review]`. `develop` and `review` open an accepted ADR when `skills` names a skill the slice uses. An ADR with an empty `skills` list has no reader.

An accepted ADR replaces a skill rule only when the ADR is a divergence. A divergence names the rule, what differs, and why. An ADR that differs from a skill rule and does not name these three is a finding in `review`. What `github-pipeline` says is not a divergence stays not allowed.

## Ids

Before writing an id, run `make ids`. It reads every `id:` and every table id under `docs/`, and the retired list in `docs/ids.yaml`. A match exits non-zero. Do not write the document. When the Makefile does not include `project.mk` or `sdlc.mk` yet, run `make -f .claude/skills/record/index.mk ids`. The retire command has the same form: `make -f .claude/skills/record/index.mk ids-retire ID=<id>`. Set `PYTHON_IMAGE=<image>` on that command line when the default image is not the one to use. `migrate-docs` needs these forms in an existing project.

`docs/ids.yaml` is:

```yaml
retired: []
```

Deleting a document runs `make ids-retire ID=<id>`. A retired id is never issued again. The caller does not invent an id in prose.

## History

One file per task. `plan` creates it when implementation starts. `develop` asks for it when the request named a source file, a failing test, or a known issue and `plan` did not run. The stage that asks creates the branch of the slice first. This skill writes the file from `templates/history.md` and adds one roadmap line with the history id. Later skills extend that file. A deferred slice is a proposal and has no history file yet.

When a proposal is picked up, create the history file, set `proposals:` to that id, and set the proposal status to `started`. Add one roadmap line with both ids. Do not copy the grill into the roadmap.

A stage writes its section in sentences: what it did, each gate with its result, and what it left alone. It replaces `Not invoked yet.` and keeps the heading.

Every history file has these sections. A missing heading is a failed step.

| Section | When the stage ran | When it did not |
| --- | --- | --- |
| Plan | Questions and answers | One sentence. `plan` writes this section when it creates the file |
| Develop | What changed, and which language skill was used | `Not invoked yet.` while the task is open. When the task closes or waits, one sentence |
| Review | Gates, subskill checks, findings, what was left alone | The same pattern. A subskill that is not installed is one line: `security: not installed` |
| Release | What shipped | `Not invoked: this slice does not ship.` or `Not invoked yet.` |

An agent on another task opens a history file only when an id names it.

## Closing a task

`release` asks this skill to close the task, when the slice shipped and when it does not ship. A task whose work waits stays open. A slice that is done and waits only for the merge of the owner is closed on its branch.

1. Stop when the Plan, the Develop, or the Review section of the history file is still `Not invoked yet.` Do not take a later step. `release` writes the Release section before it asks for the close.
2. Set the history status to `closed`. The status of a history file is `started` or `closed`.
3. Delete the roadmap line that cites this history id.
4. When the slice started from a proposal, set the proposal status to `done`. The status of a proposal is `open`, `started`, or `done`.
5. When the slice fixed a known issue, delete that row and retire its id. Stop when a test still names that id. The test names the ADR or the Decided row that states the fixed behaviour. Write that Decided row when there is none.
6. An ADR and a Decided entry stay. They are in force after the task closes.
7. In a repository that keeps `docs/REQUIREMENTS.md` and does not keep `docs/ROADMAP.md`, delete the Open row for this task and retire its id.

## Tests

A test names the requirement it proves with `id:` in its header or metadata. That is the same line this skill matches. The id is an ADR id or a decision id. A roadmap line and a known issue are work, not rules. Their ids are retired when the work ends, so a test does not name them. A test for a fixed known issue names the ADR or the Decided entry that states the fixed behaviour. `record` writes that Decided entry when there is none. When the repository keeps `docs/REQUIREMENTS.md` and does not keep `docs/adr/`, the id is a row in that list. The test name states what the system does when that requirement holds. The test does not build a path to the document. In a Python test the line is the docstring of the test: `"""id: D-1"""`. In a JavaScript, TypeScript, Java, Groovy, Kotlin, or Go test file the line is a comment: `// id: D-1`. One file may have several such lines, one for each id it proves.

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
