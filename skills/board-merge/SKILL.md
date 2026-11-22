---
name: board-merge
description: Applies the findings that the owner chose by id from the board merge report. Merges rows, shortens a row, shrinks a row that tests cover, or deletes a closed history file. Makes one commit for each finding.
---

The general rules in `CLAUDE.md` apply.

<purpose>
The owner chooses findings from the report of `board-merge-report`. This skill does exactly that and nothing else. One Git commit holds one finding, so that `git revert` undoes one.
</purpose>

<inputs>
- An action and ids, as `merge R-51 R-76`, `shorten R-12`, `cover R-40`, or `delete H-2026-11-15-slug`.
- Several lines make several findings.
</inputs>

<steps>
1. Run `make toon` and `make board-numbers IDS="<ids>"`. Keep the output as the words before. If an id is not a unit, stop.
2. Check the finding again, because the report can be old. Read `references/recheck.md`. If a check fails, stop and tell the user the id and the reason.
3. Invoke `record` before each board write. Edit the row text with the file edit tool. Do the action as the rules say.
4. Run `make links`, `make toon`, `make ids`, and `make links-check`.
5. Run the gates of `CLAUDE.md`. If a gate fails, stop without a commit. Leave the edit in the working tree, name the gate, and say that a fix or `git checkout -- <files>` is the next step.
6. Run `make board-numbers IDS="<the surviving or receiving id>"`. Its words are the words after. A deletion with no moved reason has 0.
7. Stage only the files of the finding and commit with Git. The message names the action, the ids, and the words before and after. Then start the next finding at step 1.
</steps>

<rules>
- Merge: the surviving row keeps its id and takes the unique sentences of the other row. The other id is retired with `make ids-retire ID=<id>`.
- Merge: each test line `id:` that names the retired id names the surviving id. No test is deleted.
- Merge: each running-text mention and each frontmatter list item of the retired id becomes the surviving id before the retire. After the retire, `make links` rewrites the links. Do not edit a history file. It keeps the retired id as plain text.
- Merge: if a Decided row that states a reason goes into a requirement or an ADR, one sentence of that reason stays in the surviving row.
- Shorten and cover: edit the row only. The row keeps its id and its tests.
- Cover: the row keeps its intent, its reason, and each fact that no test pins.
- Delete history: only a closed file. If the finding flags a reason, copy it into the named row as one sentence first. That sentence counts in the words after. Remove each mention of the history id from other documents that are not history files, delete the file, and retire the id.
- Do not weaken a test, and do not delete one.
- Touch no id outside the finding.
</rules>

<output>
- For each finding: the action, the ids, the commit, the gates and their results, and the words before and after from `make board-numbers`.
- A finding that stopped: the id, the step, and the reason.
</output>

<references>
- `references/recheck.md`: what to check again for each action. Read it in step 2.
</references>
