# Requirements of onboard

The rows that the skill `r-onboard` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-70"></a>R-70 | Onboard | in force | `r-onboard` brings a project onto this collection when the owner says `report and integrate`, for a new project and for an existing one. It is the order of the other skills and does no work that they own. It checks that Make, Git, and Podman run, reads the language, the old board, and the remote, and asks only what the files do not tell, such as how the project ships. If `CLAUDE.md` is missing or has no general rules, it reads the entry-file template first. It runs `r-migrate-docs` first when the old board or `AGENTS.md` exists, then `r-project-setup` in report mode and in setup mode, then `r-github-pipeline` when the project publishes through GitHub, then `r-record` for the rules the project already follows, then every gate. It takes the owner and the name from the remote. If the project has no remote `origin`, it says so, pushes nothing, and asks the owner for the owner and the name only when `r-github-pipeline` runs. It stops when a gate fails. It writes no feature and opens no history file. It pushes only to the remote the project already has. This applies to a product repository. `r-onboard` owns the order. |
