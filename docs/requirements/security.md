# Requirements of security

The rows that the skill `r-security` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-31"></a>R-31 | Security questions | in force | `r-security` applies when the change listens, stores a secret, accepts input, or runs a command. `r-plan` asks what crosses a trust boundary, who can call it, what happens when the check says no, and what bounds each input. `r-review` checks that no secret is in the tree, a log, or an error. It checks that a listener, an input, and a command are the ones the slice named. This applies to both, when the skill is installed, and `r-security` owns the questions. |
