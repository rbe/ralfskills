# [project name]

[One sentence that says what this project is.]

`CLAUDE.md` is the only entry file. The skills are installed under `.claude/skills/` with APM.

Stages, in order: `plan`, `develop`, `review`, `release`. A new or vague request starts at `plan`. A request that names a source file, a failing test, or a known issue starts at `develop`. Other skills: `record`, `project-report`, `project-setup`[, `github-pipeline`, `system-state-report`: keep each only when installed].

Language skills: [the installed ones of `node`, `python`, `shell`, `jvm`, `go`]. Subskills `plan` asks and `review` checks: [the installed ones of `security`, `privacy`, `ux-ui-design`, `api-design`]. A project skill is an extra name listed here. [Name each project skill and framework here, or write none.]

This project ships [as a binary, with `make <target>` / as a container image, with the merge into the default branch / as a library package, with `make build` / with the merge only].

## General rules

These rules apply to every skill. A skill states only what it adds.

<general_rules>

Interface:

- Type only `make <target>` and Git commands. Make runs every other tool in a Podman image, on this machine and in CI. The host needs only Make, Git, and Podman.
- If no target runs a command that the work needs, `project-setup` adds the target. Do not run the tool on the host.
- If the Makefile lacks the include of `project.mk` or `sdlc.mk`, run `make -f .claude/skills/<skill>/<file>.mk <target>`.

Start of a task:

- Run `make old-board` before the first skill. If the target fails, the only skill is `migrate-docs`, which may invoke `record`.
- If a step says stop, or needs a skill that is not installed, take no later step. Tell the user the step and the reason, and name the skill that is missing.

Board:

- `record` writes every id and every board document. Invoke `record` before you create one.
- An ADR in `docs/adr/` is an architecture or development rule, and an ADR with the status `Accepted` is a rule for every change.
- If the repository keeps `docs/REQUIREMENTS.md` and no `docs/adr/`, a row of that list replaces an ADR, and an Open row of `docs/DECISIONS.md` replaces a roadmap line. Where a step names `docs/adr/index.toon`, read `docs/requirements-index.toon` in such a repository and open each row that names a part that the change touches.
- Run `make toon` before you read an index. A file that a Make target writes is generated. Hand-editing it is a defect.
- `onboard`, `migrate-docs`, and setup mode open no history file, and their commits go on the default branch.

Gates:

- The gates are `make editorconfig`, `make format`, `make lint`, `make test`, `make integration`, and `make coverage`.
- A change is done when `make lint` and `make test` passed after the last edit. Report a gate that did not run as not run, with the reason.
- A test names the ADR id or the decision id that it proves in a line `id:`. Stop when a test has no id.
- Do not weaken a test, skip a test, catch an error silently, or put a secret or personal data in a fixture.
- A method does one thing or only composes other methods. Each unit, function, method, class, and file takes its name from the domain.

</general_rules>

## Communication contract

The user reads each reply once, often after a break, has not read the code, and does not remember earlier chats. The user decides from what you write, so make each sentence clear on first reading.

Names:

- Use the user's words and the identifiers of the project, one name for one thing. Invent no synonym for a term the project uses.
- Before you send a reply, replace each label you invented with the project name or a description, or define it in one sentence at its first use.
- Define an abbreviation at its first use.

Sentences:

- The first sentence states the understood intent, in one sentence. Stop when that sentence is wrong.
- One statement per sentence. Maximum 25 words.
- Use active voice with a named actor: "The import job deletes the old rows", not "Old rows are deleted".
- Put the condition before the result: "If the token is expired, the system asks for a new login."
- Use full sentences, not arrows, symbols, or note style.

Content:

- Use the specific noun, number, path, or name: "3 of 14 tests fail", not "some tests fail".
- For "better", say what changed and what the effect is. Use no judging word without a measure.
- For each statement about the system, say how you know it: you ran it, you read it in the code, or you only assume it.
- Use literal language, not figures of speech.

Example. Not: "Improved the persistence layer." But: "`save_order` in `db/orders.py` now tries a failed write 3 times. Before, one failed write stopped the import. I read this in the code. I did not run it."

These rules apply to what you write to the user, not to code, to quotes, or to a text the user asks you to write for a different reader.

English follows ASD-STE100. German follows "Deutsch für die Technische Kommunikation" (tekom Deutschland e.V.). Name the standards. Copy no text of them. Keep German and English separate.
