# Requirements of review

The rows that the skill `r-review` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-48"></a>R-48 | Review findings | in force | `r-review` runs after implementation and before a ship. A finding follows the defect report form of [R-113](record.md#r-113), and a finding that waits becomes a roadmap row of the kind `defect` through `r-record`. A gate that did not run is reported as not run, and a step that is not `make <target>` is a finding. This applies to both, and `r-review` owns the findings. |
| <a id="r-143"></a>R-143 | Incident review | in force | After a suspected loss of data or a wrong number that users saw, `r-review` stops every write and copies the data folder. It reproduces the fault on the copy. It records impact, root cause, fix, and prevention. It tells the owner whether a re-import or a restore is needed. The reason is that a second write can destroy the evidence. This applies to a product repository that installs `r-review`, and `r-review` owns this rule. |
