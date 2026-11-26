# Requirements of r-system-state-report

The rows that the skill `r-system-state-report` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-74"></a>R-74 | System state report | in force | `r-system-state-report` writes a plain-language report on what an agent-built system does now, which decisions shaped it, and what the owner must decide. Each statement has a source and a status of ran, read, or said, so a reader who has only the report can check it. A decision that has no row and must hold goes to `r-record`, as [R-53](record.md#r-53) says. This applies to this collection and to a product repository. `r-system-state-report` owns the report, and `r-record` owns the rows. |
