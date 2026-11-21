# Documents: layout, frontmatter, links

## Layout

- The scripts read a table row for a decision and for a known issue.
- The scripts read a frontmatter block for an ADR, a proposal, and a history file.
- Write a list in the frontmatter on one line, as `skills: [a, b]`.
- In the frontmatter and in the id cell of a table, an id is plain text. The scripts read it there.
- `docs/ids.yaml` holds the retired ids. Before the first retire it does not exist. An empty list is `retired: []`.

## Frontmatter

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

- The keys are the plural of the kind.
- A decision, a proposal, and a history file use the same keys.
- A history file may cite an id that was retired later.

## What `make links` writes

`make links` rewrites each document under `docs/`:

- A table row gets an anchor in its id cell, as `<a id="d-9"></a>D-9`. The anchor is the id in lowercase.
- An id of a table row becomes a link to that row, as `[D-9](../DECISIONS.md#d-9)`.
- An id of an ADR, a proposal, or a history file becomes a link to that file, as `[ADR-0001](../adr/ADR-0001.md)`.
- A retired id has no target and stays plain text.
- An id in a code span, a code block, or a heading stays plain text.

`make links-check` fails in 3 cases: an id in running text is not a link, a link is wrong, or a row has no anchor.

`make decision-log` and `make project-report` give each item an anchor and link each id in the generated document.
