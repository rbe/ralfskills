# ralfskills

This repository is the skill collection. `CLAUDE.md` is the only entry file.

Stages, in order: `plan`, `develop`, `review`, `release`. `plan` names who owns state and what may call what. `project-report` generates the requirements-to-tests map and the architecture and development reviews. `onboard` brings a project onto this collection: it runs the skills below in order. `system-state-report` writes the plain-language report on what the system does now and which decisions wait for the owner. `project-setup` is the Make contract. `github-pipeline` is the delivery contract, and `release` invokes it when delivery changes.

Language skills: `node`, `python`, `shell`, `jvm`, `go`. Subskills `plan` asks and `review` checks: `security`, `privacy`, `ux-ui-design`, `api-design`. A project skill is an extra name listed here.

This collection records each requirement as one row in `docs/REQUIREMENTS.md`. An Open row in `docs/DECISIONS.md` is work that is not finished. A Decided row is a choice in force. This collection does not keep `docs/ROADMAP.md` or `docs/adr/`. The skills still teach a product repository to keep them. `make toon` writes `docs/requirements-index.toon` and `docs/skill-index.toon` here. In a product repository it writes `docs/adr/index.toon` and the skill index.

## General rules

These rules apply to every skill. A skill states only what it adds.

<general_rules>

Interface:

- Type only `make <target>` and Git commands. `make` prints the targets. Make runs every other tool in a Podman image, on this machine and in CI. The host needs only Make, Git, and Podman.
- If no target runs the command that the work needs, `project-setup` adds the target. Do not run the tool on the host.
- If the Makefile does not include `project.mk` or `sdlc.mk` yet, run a target as `make -f .claude/skills/<skill>/<file>.mk <target>`. An example is `make -f .claude/skills/project-setup/old-board.mk old-board`.
- `project-setup` owns the rules for Podman, XDG paths, Make 3.81 recipes, and what a shipment may contain.
- A skill with modes runs one mode. Report mode reads the project and writes nothing. Setup mode writes only what is missing or off the contract, and it leaves a target that the project already filled in. If a request asks for both modes, run report mode first.
- A divergence from a skill rule names the rule, what differs, and why.
- The owner creates a `v*` tag. A skill creates none.

Start of a task:

- Run `make old-board` before the first skill. If the target fails, the only skill is `migrate-docs`, and `migrate-docs` may invoke `record`. `onboard` invokes `migrate-docs` itself.
- If a step needs a skill that is not installed, stop and name that skill. A subskill is optional. For a subskill that is not installed, `plan` and `review` write the line `<name>: not installed`.
- If a step says stop, take no later step. Tell the user the step and the reason.
- Ask the owner one question at a time. Ask only what the code and the board do not answer.

Board:

- `record` writes every id and every board document. Invoke `record` before you create an id or a document.
- In-progress work is a line in `docs/ROADMAP.md`. A defect is a row in `docs/KNOWN_ISSUES.md`. A small choice is a row in `docs/DECISIONS.md`. An architecture or development rule is an ADR in `docs/adr/`. Work for later is a file in `docs/proposals/`. A started slice is a file in `docs/history/`.
- An ADR with the status `Accepted` is a rule for every change.
- If the repository keeps `docs/REQUIREMENTS.md` and no `docs/adr/`, a row of that list replaces an ADR, and an Open row of `docs/DECISIONS.md` replaces a roadmap line.
- Run `make toon` before you read an index.
- Write an id as plain text. After a document under `docs/` changes, run `make links`. It makes each id a link. `make links-check` checks the links.
- `make decision-log` writes the decisions as one document.
- A file that a Make target writes is generated. Hand-editing it is a defect.
- A stage asks `record` to write its section of the history file. Each other skill asks `record` to add one line that names the skill to the open section. Such a skill opens no history file. If no history file is open, the skill adds no line.
- The work of `onboard`, of `migrate-docs`, and of setup mode is not a slice. It has no history file. Its commits go on the default branch.

Gates:

- The gates are `make editorconfig`, `make format`, `make lint`, `make test`, `make integration`, and `make coverage`. CI runs the same six targets.
- A change is not done until `make lint` and `make test` passed after the last edit. Report a gate that did not run as not run, with the reason.
- `make test` is the full suite. `make test-changed` runs the tests that cover the diff. A green `test-changed` does not replace `make test`.
- `make coverage` writes `build/coverage/diff.md`, the lines that the change touched. A repository-wide percentage is not a result.
- Each language has one formatter and one linter, the tools that the language skill names. `make format-fix` rewrites the files. Do not write a formatter or a linter, and do not add a second one.
- `make project-report` writes `build/project-report.md`.
- A test names the requirement that it proves in a line `id:`. The id is an ADR id or a decision id. Stop when a test has no id.
- Do not weaken a test and do not skip a test. Do not catch an error silently. Do not put a secret or personal data in a fixture.
- A method does one thing, or it only composes other methods. The name of a unit, a function, a method, a class, or a file comes from the domain.

</general_rules>

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
