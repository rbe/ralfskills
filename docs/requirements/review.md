# Requirements of review

The rows that the skill `review` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-48"></a>R-48 | Review findings | in force | `review` runs after implementation and before a ship. A finding has a location, the mechanism, the evidence, whether it predates this change, and the check that proves the fix. A finding that is fixed stays in this change. A finding that waits becomes a roadmap row of the kind defect through `record`. `review` writes what this change deliberately left alone. A gate that did not run is reported as not run, with the reason. Do not weaken a test. CI runs the six gate targets that the test job of [R-93](github-pipeline.md#r-93) lists. A step that is not `make <target>` is a finding. This applies to both. `review` owns the findings. |
