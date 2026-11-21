# [project name]

[One sentence that says what this project is.]

`CLAUDE.md` is the only entry file. The skills are installed under `.claude/skills/` with APM.

Stages, in order: `plan`, `develop`, `review`, `release`. A new or vague request starts at `plan`. A request that names a source file, a failing test, or a known issue starts at `develop`. `record` writes every id and every board document. `project-report` generates the requirements-to-tests map and the architecture and development reviews. `project-setup` is the Make contract. [Keep this sentence only when `github-pipeline` is installed:] `github-pipeline` is the delivery contract, and `release` invokes it when delivery changes.

Language skills: [the installed ones of `node`, `python`, `shell`, `jvm`, `go`]. Subskills `plan` asks and `review` checks: [the installed ones of `security`, `privacy`, `ux-ui-design`, `api-design`]. A project skill is an extra name listed here. [Name each project skill and each framework here, or write that there is none.]

`plan` names who owns state and what may call what. `develop` is not done until `make lint` and `make test` pass. The linter is the one the language skill names. `make test` is the full suite. `make test-changed` runs the tests that cover the diff. `make coverage` lists the lines the change touched. `make project-report` writes the generated report. `make format-fix` rewrites the files with the formatter.

[Keep this paragraph only when `system-state-report` is installed:] `system-state-report` writes the plain-language report on what the system does now and which decisions wait for the owner. Say `state report` to start it.

This project ships [as a container image, with the merge into the default branch / as a binary, with `make <target>` / as a library package, with `make build` / as a library, with the merge into the default branch].

In-progress work is a line in `docs/ROADMAP.md`. A defect is a row in `docs/KNOWN_ISSUES.md`. A small choice is a row in `docs/DECISIONS.md`. An architecture or development rule is an ADR in `docs/adr/`. Work for later is a file in `docs/proposals/`. A started slice is a file in `docs/history/`. An accepted ADR is a rule for every change. A test names the ADR or the decision it proves with `id:`. Run `make toon` before reading an index. `make decision-log` writes the decisions as one document. An id in a document is a link. `make links` writes the links.

If `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` exists, the only skill is `migrate-docs`.

## Communication contract

The user reads each reply once, often after a break. The user has not read the code and does not remember earlier chats. The user decides from what you write. Each sentence must be clear on the first reading.

Names:

- Use the user's words and the identifiers of the project. Use one name for one thing. Do not change it for variety. Do not invent a synonym for a term the project already uses.
- During work you give things your own labels. The user does not know them. Before you send a reply, find each label you invented. Replace it with the project name or with a description. If you must keep a new term, define it in one sentence at its first use.
- Define an abbreviation at its first use.

Sentences:

- The first sentence to the user states the understood intent, in one sentence. Stop when that sentence is wrong.
- One statement per sentence. Maximum 25 words.
- Use active voice with a named actor: "The import job deletes the old rows", not "Old rows are deleted".
- Put the condition before the result: "If the token is expired, the system asks for a new login."
- Use full sentences. Do not use arrows, symbols, or note style in place of sentences.

Content:

- Use the specific noun, number, path, or name. Write "3 of 14 tests fail", not "some tests fail". Write "the function `send_invoice`", not "the logic".
- When you say that something is better, say what changed and what the effect is. Do not use a word that judges without a measure.
- For each statement about the system, say how you know it: you ran it, you read it in the code, or you only assume it.
- Use literal language. Do not use figures of speech.

Example. Not: "Refactored the persistence layer for improved robustness." But: "The function `save_order` in `db/orders.py` now tries a failed write 3 times. Before, one failed write stopped the import. I read this in the code. I did not run it."

These rules apply to what you write to the user. They do not apply to code, to quotes, or to a text the user asks you to write for a different reader.

English follows ASD-STE100. German follows "Deutsch für die Technische Kommunikation" (tekom Deutschland e.V.). Name the standards. Do not copy their text. Keep German and English separate.
