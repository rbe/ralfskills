# Requirements of observability

The rows that the skill `r-observability` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-102"></a>R-102 | Observability questions | in force | `r-observability` applies when the change starts a program, prints a message, writes a log line, or can fail. `r-plan` asks what the program prints on start, which failure the user can cause, and which unexpected failure needs its cause in the log. `r-review` checks that the user sees each failure and that the log holds each cause once. This applies to both, when the skill is installed, and `r-observability` owns the questions. |
