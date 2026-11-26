# Requirements of r-board-merge-report

The rows that the skill `r-board-merge-report` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-77"></a>R-77 | Board merge report | in force | `r-board-merge-report` finds rows, ADRs, and closed history files that can merge, shrink, or go, and rows that contradict each other or the code. It writes nothing. The reason is that the owner chooses each change by id, from numbers that `make board-numbers` computes and not from the agent. This applies to this collection and to a product repository, and `r-board-merge-report` owns the report. |
| <a id="r-86"></a>R-86 | Test names in the output of `make board-numbers` | in force | `make board-numbers` names each test that carries an id, so the report quotes the tests without opening files. The output stays one line for each unit. This applies to this collection and to a product repository, and `r-board-merge-report` owns the target. |
