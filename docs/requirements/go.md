# Requirements of go

The rows that the skill `r-go` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-68"></a>R-68 | Go | in force | `r-go` applies the Go rules when it is installed and the files are Go. Go runs only in Podman, so the host needs no Go toolchain. A Go test file carries its `id:` line as [R-63](project-report.md#r-63) says. This applies to a product repository that installs `r-go`, and `r-go` owns these rules. |
| <a id="r-118"></a>R-118 | Smoke check of a binary | in force | A project that ships a binary runs the built binary once, so a binary that does not start fails the build. A binary of another machine is not run. This applies to a product repository that installs `r-go`, and `r-go` owns this rule. |
