# Requirements of r-skills-review

The rows that the skill `r-skills-review` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-107"></a>R-107 | Skills review | in force | `r-skills-review` has report mode only and writes nothing. It reads each `SKILL.md` and each file under `references/` of the installed skills, which are `skills/r-*/` in this collection and `.claude/skills/*/` in a project, with the project skills, and it reads the general rules and the communication contract of `CLAUDE.md`. It reports three kinds of finding: the same rule in two places, the same action in two skills, and two statements that contradict. A pointer is not an overlap. Each finding has a number, the kind, each place as `path:line`, a quote, and the proposed owner. The owner of a rule of the general rules is `CLAUDE.md` alone. Any other rule belongs to the skill whose purpose names the subject, and the other places keep a pointer. `r-skills-review` covers skill files, and `r-board-merge-report` covers the documents in `docs/`, as [R-77](board-merge-report.md#r-77) says. This applies to this collection and to a project. `r-skills-review` owns the report. |
