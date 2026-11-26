# Requirements of observability

The rows that the skill `observability` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-102"></a>R-102 | Observability questions | in force | `observability` applies when the change starts a program, prints a message, writes a log line, or can fail. `privacy` owns personal data in logs, and `api-design` owns the error body. `plan` asks four questions. What does the program print on start? Which failure can the user cause, and where does the user see it? Which unexpected failure needs its cause in the log? Which code path runs for each request, and does it log? `review` checks five things. On start, the program prints one line with the address it listens on and the data paths it uses. A message is short and says what to do. A hot path writes no log line for each request. A failure that the user can cause reaches the user as a visible error, not as a silent empty view. The program logs the cause of an unexpected failure once. This applies to both, when the skill is installed. `observability` owns the questions. |
