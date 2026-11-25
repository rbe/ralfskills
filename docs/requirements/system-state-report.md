# Requirements of system-state-report

The rows that the skill `system-state-report` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-74"></a>R-74 | System state report | in force | `system-state-report` writes a plain-language report on what an agent-built system does now, which decisions shaped it, and what the owner must decide. It collects the evidence first, builds a glossary, writes eight sections, and gives each statement in sections 2 to 6 a source and a status of ran, read, or said. A reader that has only the report checks it. The report is `reports/state-YYYY-MM-DD.md`. A decision the report finds that has no row and must hold goes to `record`, which decides where it goes, as [R-53](record.md#r-53) says. The skill keeps only the rules of a report that the communication contract of [R-51](collection.md#r-51) lacks. This applies to this collection and to a product repository. `system-state-report` owns the report. `record` owns the rows. |
