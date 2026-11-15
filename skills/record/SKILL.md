---
name: record
description: Assign document ids and write the board. Use before creating or editing a roadmap line, a known issue, a decision, an ADR, a proposal, or a history file. Reject a duplicate id, including a retired one. Write the ADR index. Other skills invoke this skill by name.
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
```

A decision, a proposal, and a history file use the same keys.

## Ids

Before writing an id, run `python3 .claude/skills/record/scripts/ids.py`. The script reads every `id:` under `docs/` and the retired list in `docs/ids.yaml`. A match exits non-zero. Do not write the document.

`docs/ids.yaml` is:

```yaml
retired: []
```

Deleting a document runs `python3 .claude/skills/record/scripts/ids.py retire <id>`. A retired id is never issued again. The caller does not invent an id in prose.

## History

One file per task. `plan` creates it when implementation starts. Later skills extend that file. A deferred slice is a proposal and has no history file yet.

When a proposal is picked up, create the history file, set `proposals:` to that id, and set the proposal status to `started`. Add one roadmap line with both ids. Do not copy the grill into the roadmap.

Every history file has these sections. A missing heading is a failed step.

| Section | When the stage ran | When it did not |
| --- | --- | --- |
| Plan | Questions and answers | One sentence. `plan` writes this section when it creates the file |
| Develop | What changed, and which language skill was used | `Not invoked yet.` while the task is open. When the task closes or waits, one sentence |
| Review | Gates, subskill checks, findings, what was left alone | The same pattern. A subskill that is not installed is one line: `security: not installed` |
| Release | What shipped | `Not invoked: this slice does not ship.` or `Not invoked yet.` |

An agent on another task opens a history file only when an id names it.

## ADR index

`python3 .claude/skills/record/scripts/adr_index.py` reads ADR frontmatter and writes `docs/adr/index.toon`. The columns are `id`, `status`, `title`, `adrs`, `skills`, and `decisions`. `plan` reads the index and opens one ADR when the id matches. The index is generated. Hand-editing it is a defect. The index does not list skills.

A project Makefile may add:

```make
adr-index: ## Write the ADR index
	python3 .claude/skills/record/scripts/adr_index.py

ids: ## Reject a repeated id
	python3 .claude/skills/record/scripts/ids.py
```
