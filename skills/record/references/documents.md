# Documents: layout, frontmatter, links

## Layout

- The scripts read a table row for a roadmap row and for a requirement row.
- `docs/ROADMAP.md` has the columns Id, Kind, Title, and Proposal. The kind is `feature`, `defect`, or `question`. The proposal cell is a link or empty.
- `docs/REQUIREMENTS.md` has the columns Id, Title, and Statement. A repository with no `docs/adr/` has the columns Id, Title, Status, and Statement, and no `docs/ROADMAP.md`. The status is `planned` or `in force`. A planned row is open work, and its statement names the choices of an open question.
- The scripts read a frontmatter block for an ADR, a proposal, and a history file.
- Write a list in the frontmatter on one line, as `skills: [a, b]`.
- In the frontmatter and in the id cell of a table, an id is plain text. The scripts read it there.
- `docs/ids.yaml` holds the retired ids. Before the first retire it does not exist. An empty list is `retired: []`. A list with entries is `retired:` and one `- W-1` line per id.
- When a merge retired an id, `docs/ids.yaml` also has the key `merged:` and one line `  R-15: [R-24]` for each such id. The ids in the brackets are live. A retired id that no row took over has no line.

## Frontmatter

```yaml
id: ADR-0004
title: Listen on localhost
status: Accepted
adrs: [ADR-0001]
skills: [security, review]
roadmap: [W-12]
proposals: []
supersedes: []
```

- The keys are the plural of the kind.
- A proposal and a history file use the same keys.
- `decisions` and `issues` are read-only legacy keys of a file written before the roadmap table. A script that reads `roadmap` also reads these two. A new file does not use them.
- A list key other than `skills` holds ids only, written as `[a, b]` on one line. An empty list is `[]`. A list is never missing its brackets, never text, and never a bare id. A script can then read each list as a list of ids.
- Field rule: a list holds ids only, and each id is live or on the retired list. `make ids` fails on any other item. A document is not rewritten when an id retires later, a history file included.
- The id of a requirement row goes in `adrs`, where the repository keeps no `docs/adr/`. The id of a roadmap row goes in `roadmap`, and a proposal id in `proposals`.
- A text or an explanation does not go in a list. It goes in the body.
- When an id retires and other rows took over its content, `make ids-retire ID=<id> INTO="<id> <id>"` writes the map line in `docs/ids.yaml`. Without `INTO=`, a map line that names the retired id loses that id. A script follows the line from a retired id to the live ids.
- The text of a history file keeps a retired id as plain text.

## What `make links` writes

`make links` rewrites each document under `docs/`:

- A table row gets an anchor in its id cell, as `<a id="w-9"></a>W-9`. The anchor is the id in lowercase.
- An id of a table row becomes a link to that row, as `[W-9](../ROADMAP.md#w-9)`.
- An id of an ADR, a proposal, or a history file becomes a link to that file, as `[ADR-0001](../adr/ADR-0001.md)`.
- A retired id has no target and stays plain text.
- An id in a code span, a code block, or a heading stays plain text.

`make links-check` fails in 3 cases: an id in running text is not a link, a link is wrong, or a row has no anchor.

`make project-report` gives each item an anchor and links each id in the generated document.
