# Requirements of security

The rows that the skill `security` owns. `collection.md` says what the status means.

| Id | Title | Status | Statement |
| --- | --- | --- | --- |
| <a id="r-31"></a>R-31 | Security questions | in force | `security` applies when the change listens, stores a secret, accepts input, or runs a command. `plan` asks four questions. What crosses a trust boundary: a listener, a file, a secret, or a command? Who can call it? What happens when the check says no? What is the bound on the size and on the type of each input? `review` checks four things. A secret is not in the tree, a log, an error, or a fixture. A listener is the one the accepted ADR names. Input has a bound on size and on type. A command the program runs is the one the slice named. Podman, XDG paths, and shipment contents stay in `project-setup`. This skill does not restate them. This applies to both, when the skill is installed. `security` owns the questions. |
