# Requirements of review

The rows that the skill `r-review` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-48"></a>R-48 | Review findings | in force | `r-review` runs after implementation and before a ship. A finding follows the defect report form of [R-113](record.md#r-113), and a finding that waits becomes a roadmap row of the kind `defect` through `r-record`. A gate that did not run is reported as not run, and a step that is not `make <target>` is a finding. This applies to both, and `r-review` owns the findings. |
