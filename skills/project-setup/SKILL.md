---
name: project-setup
description: Applies or checks the Make contract in setup mode or report mode. Use when adding a Makefile, CLAUDE.md, EditorConfig, or a standard target, or when moving a host tool into a target. A repository that does not publish through GitHub installs only this skill.
---

The general rules in `CLAUDE.md` apply.

<purpose>
This skill owns the Make contract: the Makefile, the standard targets, `CLAUDE.md`, and `.editorconfig`. Setup mode brings a project into line with the contract. Report mode shows the project against the contract.
</purpose>

<mode name="setup">
<steps>
1. Ask the owner how the project ships: as a binary, as a container image, as a library package, or with the merge only. A project that ships nothing answers with the merge only. Copy no template before the answer.
2. Write the Makefile.
   - If the project has no Makefile, ask which installed language skill the project uses. Write the Makefile from the template of that skill with the file tool: `templates/Makefile.python` in `python`, `templates/Makefile.node` in `node`, `templates/Makefile.gradle` in `jvm`, or `templates/Makefile.golang` in `go`. Write the other files that the comment at the top of the template names the same way.
   - For an existing Makefile, add only the lines of the template that it lacks.
   - The Makefile sets the variables, then includes `.claude/skills/project-setup/project.mk` before any target. If the Makefile includes `.claude/skills/github-pipeline/sdlc.mk`, leave this include out. That file provides `help` and the same targets.
3. Fill the command variables. Read `references/makefile.md` for the variables.
   - Set a variable only if it is empty and the toolchain is already in the project (`package.json`, Gradle, python, or tar). A value that the project set stays.
   - If the Makefile already has a recipe for a target, leave the recipe and leave the command variable empty. The report names that variable as missing.
   - If a recipe runs Gradle, npm, node, python, or go on the host, rewrite it to the command variable and keep what it does. The command of the template replaces a host recipe that runs the same tests or the same build. A target with no command variable, such as `run`, keeps its name and its place after the include. Its recipe uses `$(PYTHON)`, `$(NODE)`, `$(GRADLE)`, or `$(GO)`.
   - If the project has no dependency to resolve, no artifact to build, or no integration entry, set that command to `true`.
   - If the project ships a binary or a library package, set what the language skill names for it, such as `BIN` for Go, or set `BUILD_CMD`. Then `make build` writes the shipment from the first run.
   - If the repository renders docs, set `RENDER_DOCS` and `DOCS_CMD`. If an image is published, set `PUBLISH_IMAGE`.
4. If the Makefile came from a template in this run, or a file that the tooling target writes is missing, run the tooling target that the language skill names. The target creates the manifest, the config files, `.editorconfig`, and its `.gitignore` lines when they are missing, and it runs `make format-fix`. A file that is already in the project stays, so the target is safe to run again. A Python project with no dependency has no manifest.
5. Add each missing line to `.gitignore`: `build/`, `apm_modules/`, `docs/adr/index.toon`, `docs/skill-index.toon`, and the lines that the tooling reference of the language skill names.
6. Run `make toon`. Step 7 fills the brackets of the template from `docs/skill-index.toon`.
7. Write `CLAUDE.md`.
   - If the file is missing, copy `templates/CLAUDE.md` and fill each bracket from the project and from `docs/skill-index.toon`. The answer of step 1 is the ship sentence.
   - If the file exists, add each paragraph of the template that is missing. Keep its other text, except under the last bullet of this step.
   - If the file has no `<general_rules>` block, add the section `## General rules` of the template before `## Communication contract`. If the block differs from the template, replace the block.
   - After the block is in the file, delete each sentence outside the block that the block states. Name each deleted sentence in the reply.
8. Make each item of `<checks>` true, in order. Stop at the first item that cannot be made true.
   - If `.editorconfig` is missing, write it from `templates/editorconfig`.
   - Set `FORMAT_CMD`, `FORMAT_FIX_CMD`, `LINT_CMD`, and `INTEGRATION_CMD` as step 3 says. Leave an integration test out of `TEST_CMD`.
   - Set `DEFAULT_BRANCH` if that branch is not `main`.
   - If an existing test has no id, ask `record` for a Decided row that states the behaviour that the test proves, and name that row in the test. One row can serve several tests.
9. If each required command variable is set, or the Makefile defines that target, run `make setup`. Otherwise leave the run for later and name the empty variable.
10. Commit every file that this mode wrote, and each of these that exists: the manifest and its lockfile, `.claude/skills/`, `apm.yml`, and `apm.lock.yaml`. Push when the project has a remote `origin`. The Makefile includes files from `.claude/skills/`, so a clone needs them.
</steps>
<rules>
- Do not define `setup`, `build`, or `test` again after the include.
- Do not add `sdlc.mk` or a workflow. Version tags, GHCR, and cleanup are `github-pipeline`.
- If a `project.mk` is at the repository root, leave its bytes and name it in the report.
</rules>
</mode>

<mode name="report">
<steps>
1. Read `templates/contract-report.md`, `project.mk`, and `references/fail-list.md` in this skill. Read the `Makefile` and `CLAUDE.md` of the project.
2. If there is no `Makefile`, mark every row that needs one as `missing`. Otherwise read which target `.DEFAULT_GOAL` names in the `Makefile` and in the makefile that it includes.
3. Fill a copy of the skeleton in the reply, as the skeleton says.
</steps>
<rules>
- Do not run `make setup`, `make build`, `make test`, `make docs`, or `make login`.
</rules>
</mode>

<checks>
1. `editorconfig` runs editorconfig-checker, and `.editorconfig` exists.
2. `format` and `format-fix` run the one formatter that the language skill names, and `format-fix` rewrites the files. Do not write a formatter or add a second one. The formatter does not format `.claude/`, `apm_modules/`, `build/`, or `docs/`, because the scripts of `record` read the board line by line.
3. `lint` runs the one linter that the language skill names.
4. `test` runs the unit tests and no integration test.
5. `integration` is the one integration entry. No second integration target exists.
6. `coverage` writes its report through diff-cover, and `COVERAGE_CMD` also writes the coverage map. The language skill names the coverage tool. The diff is the branch against `DEFAULT_BRANCH`. `coverage` and `test-changed` fail until the first unit test exists.
7. `test-changed` selects the tests from the coverage of the files in the diff, not from a hand-kept list.
8. The `id:` line of each test names an id, not a path.
9. When `project-report` is installed, `make project-report` writes its file.
</checks>

<rules>
- Run one mode. Report mode reads the project and writes nothing. Setup mode writes only what is missing or off the contract, and it leaves a target that the project already filled in. If a request asks for both modes, run report mode first.
- `help` is the default goal. A project Makefile sets `.DEFAULT_GOAL` to no other target. A `##` comment on the target line is the text that `help` prints.
- The standard targets are `doctor`, `setup`, `build`, `test`, `editorconfig`, `format`, `format-fix`, `lint`, `integration`, `coverage`, `test-changed`, `old-board`, `skills-install`, `skills-update`, and `apm`. `project-report` exists when that skill is installed. `docs` exists only when the repository renders docs. `login` exists only when an image is published.
- A target does the same thing on a laptop and in CI. A command that only makes sense on a laptop gets its own name, such as `dev` or `verify`.
- A target is filled in when its command variable has a non-empty value, or when the Makefile of the project gives that target a recipe. `true` is a filled-in value.
- A target that the project adds after the include is the project's. A target repeated there with a recipe replaces the included recipe.
- The project includes the installed `project.mk`. Do not keep a copy at the repository root or elsewhere.
- Podman: `make build` and `make test` call Podman. `make run` exists only where a language template defines it. Docker is not a second engine. A recipe calls `git`, `podman`, and the tools of POSIX `sh`, such as `sed`, `awk`, `grep`, `find`, and `tar`. The agent types none of them. `setup` runs `make doctor`, then `SETUP_CMD`.
- XDG paths: config, data, state, and cache use `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_STATE_HOME`, and `XDG_CACHE_HOME` on macOS and Linux. If a variable is unset, the paths are `~/.config`, `~/.local/share`, `~/.local/state`, and `~/.cache`.
- Shipment: `github-pipeline` says what a shipment may contain. A Make-only repository that ships a binary ships the binary, and example data only from `examples/` when the path and the name say that it is an example.
- Make 3.81 recipes: the system `make` stays GNU Make 3.81, also on macOS. Use no `.ONESHELL` and no Make 4 function (`$(file ...)`, `$(guile ...)`, `!=`). Each recipe line is one POSIX shell, joined with backslashes. The recipe is the command; add no shell-script wrapper.
- A shell `$` in a command is `$$`.
</rules>

<references>
- `references/makefile.md`: the meaning of each target, each variable and its default, a sample Makefile, and what each makefile of this skill provides. Read it before you set a variable, when a target fails, or when `make doctor` prints `FAIL`.
- `references/fail-list.md`: the conditions under which a repository fails this contract. Read it in report mode, and when `review` checks a change to the Makefile or to a workflow.
</references>
