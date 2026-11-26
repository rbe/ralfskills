# Requirements of r-board-merge

The rows that the skill `r-board-merge` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-78"></a>R-78 | Board merge | in force | `r-board-merge` does what the owner chose by id in the report of [R-77](board-merge-report.md#r-77), and nothing else. It checks the finding again, and if the check fails it stops and says why. A merge keeps the surviving id, adds the unique sentences of the other row, deletes the other row, and changes each `id:` line of a test and each link to the surviving id. The skill edits no line of a history file. It deletes no test. A shorten or a cover edits the row only. A deletion of history takes only a closed file, moves a flagged reason first, and deletes the file. A fix edits the row to the corrected sentence after it checks the evidence again, and it never changes code. A question of the report waits for the owner's answer. Each finding is one Git commit, so that `git revert` undoes one. The gates run after each edit and before each commit, and if a gate fails the skill makes no commit. The skill reports the words before and after from `make board-numbers`. It invokes `r-record` for every id and every board write. This applies to this collection and to a product repository. |
