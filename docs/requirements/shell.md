# Requirements of shell

The rows that the skill `r-shell` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-38"></a>R-38 | POSIX shell in Make | in force | `r-shell` applies when it is installed and the change is a recipe or a shell command. Its `files` are `sh` and its `names` include `Makefile`. The shell is POSIX `sh`. A bash feature needs `CLAUDE.md` to name bash, and that choice is a requirement row through `r-record`. The formatter is shfmt. The linter is shellcheck. They read `.sh` files. A project whose only shell is in Make recipes adds no shell formatter and no shell linter. Recipe rules stay in `r-project-setup`, as [R-44](project-setup.md#r-44) says. `set -eu` starts a recipe that can fail. This applies to both. `r-shell` owns these rules. |
