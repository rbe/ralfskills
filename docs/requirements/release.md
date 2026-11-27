# Requirements of release

The rows that the skill `r-release` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-114"></a>R-114 | Stage only named files | in force | `r-release` states the rule: stage only the files of the change, by name. Never run `git add -A`, `git add .`, or `git commit -a`. A pathspec such as `git add -A <directory>` bounds the command, so it is no breach. A unit test checks that the rule stands in `r-release` only. This applies to both, and `r-release` owns the rule. |
| <a id="r-57"></a>R-57 | Release ships the slice | in force | `r-release` ships a reviewed slice on one branch. It stops when the Review section does not report all six gates as passed, when `build/gates.ok` does not match the working tree, or when a finding is neither fixed nor a roadmap row. It closes the task through `r-record` and commits the board documents on the same branch, so the board is correct after the merge. The owner creates a `v*` tag, and a skill creates none. This applies to a product repository, and to this collection without the publish, and `r-release` owns the steps. |
