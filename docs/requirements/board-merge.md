# Requirements of r-board-merge

The rows that the skill `r-board-merge` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-78"></a>R-78 | Board merge | in force | `r-board-merge` does what the owner chose by id in the report of [R-77](board-merge-report.md#r-77), and nothing else. It checks each finding again and makes one Git commit for each finding, so that `git revert` undoes one. It makes no commit when a gate fails. This applies to this collection and to a product repository, and `r-board-merge` owns the change. |
