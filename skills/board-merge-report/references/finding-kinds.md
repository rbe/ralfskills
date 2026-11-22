# Finding kinds

## Merge

- Two or more rows state the same obligation: the same actor, the same repository kind, the same stage, the same condition, and the same result.
- A Decided row whose choice a requirement row or an ADR states in full goes with no addition. A Decided row with a unique sentence is a merge only when that sentence moves into the surviving row. List the sentence in the finding.
- The requirement or the ADR survives when it has the same number of tests or more.
- A sentence that only one row states is not repeated text. Do not list it.

## Shorten

- The rows stay. A sentence that another row already states goes from this row. A sentence that the same row states twice also goes. Name that row as `same row`.
- Name the row that keeps the sentence. Quote the sentence that goes.
- A sentence with a number, a name, or a condition that the other row lacks stays.

## Covered by code

- The row has at least one test with an `id:` line for it.
- Read each such test. Every fact of the row must be pinned by an assertion: each name, number, list, path, and string.
- The row then shrinks to its intent and its reason.
- Keep what code cannot state: the reason, the rejected alternative, and a rule that crosses files.
- A fact that no assertion pins stays in the row. If one fact stays, say which.

## Delete history

- The file has the status `closed`. A file with the status `started` is never a finding.
- Read the Plan, Develop, and Review sections. A sentence that gives a reason or a rejected alternative is a reason.
- If no row, ADR, or Decided row that the file names states that reason, the file holds the only copy. Flag the file, quote the reason, and name the row that receives it. The words after are the words of that one sentence.
- A living document that links to the history id keeps a dead link. Count those in the links column. `board-merge` edits each out.

## Refutation

- Read both units in full.
- Same subject but another actor, another repository kind (this collection, a product repository, both), or another stage means no merge.
- A sentence that starts with `This applies to` names the repository kind.
- A contradiction is not a duplicate. Report it as its own line with the two ids.
