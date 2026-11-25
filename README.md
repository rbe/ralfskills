# ralfskills

Skills for [Microsoft APM](https://github.com/microsoft/apm). This repository is a [skill collection](https://microsoft.github.io/apm/reference/package-types/#skill-collection-skillsnameskillmd): each skill is `skills/<name>/SKILL.md`. There is no `SKILL.md` at the repository root, so APM does not treat the repository as one skill.

Install so the files land in `.claude/skills/`. That is the APM target `claude`. Make includes `project.mk` from that path, or `sdlc.mk` when `github-pipeline` is installed. `CLAUDE.md` is the only entry file in a project that uses these skills.

## Skills

| Skill | What it covers |
| --- | --- |
| [plan](skills/plan/SKILL.md) | Grill. Ask one question at a time. Write a history file to start now, or a roadmap row with a proposal to implement later |
| [develop](skills/develop/SKILL.md) | Implement the slice with the installed language skill |
| [review](skills/review/SKILL.md) | Gates and the installed subskills, after the change |
| [release](skills/release/SKILL.md) | Commit, push, merge when CI passed, and close the task. Invokes `github-pipeline` when delivery changes |
| [record](skills/record/SKILL.md) | Ids, the board, the history file, the ADRs and their status, the ADR index, and this collection's requirements index |
| [onboard](skills/onboard/SKILL.md) | The order of the other skills for a project that adopts this collection. Say `report and integrate` |
| [system-state-report](skills/system-state-report/SKILL.md) | A plain-language report on what the system does now, the decisions that shaped it, and the decisions that wait for the owner. Say `state report` |
| [board-merge-report](skills/board-merge-report/SKILL.md) | Reports which board rows, ADRs, and closed history files repeat text and can merge, shrink, or go. Writes nothing. Numbers come from `make board-numbers` |
| [board-merge](skills/board-merge/SKILL.md) | Does what the owner chose by id from that report. One commit for each finding |
| [project-report](skills/project-report/SKILL.md) | Generated requirements map, architecture review, and development review |
| [migrate-docs](skills/migrate-docs/SKILL.md) | The only skill that reads an old board. Other skills stop until it has deleted those files |
| [project-setup](skills/project-setup/SKILL.md) | Writes `CLAUDE.md` from its template when the file is missing. Make is the only interface. `help` is the default goal. EditorConfig, one formatter, one linter, unit tests, one integration entry, and a diff-cover report are targets |
| [github-pipeline](skills/github-pipeline/SKILL.md) | One GitHub workflow. Versions from a `vMAJOR.MINOR.PATCH` tag plus the run number |
| [security](skills/security/SKILL.md) | Questions before a slice, checks after |
| [privacy](skills/privacy/SKILL.md) | Personal data, before and after |
| [ux-ui-design](skills/ux-ui-design/SKILL.md) | Interaction. Product tokens stay in a project skill |
| [api-design](skills/api-design/SKILL.md) | HTTP, and the public API of a module or a library. The route list stays in a project skill |
| [node](skills/node/SKILL.md) | JavaScript and TypeScript |
| [python](skills/python/SKILL.md) | Python |
| [shell](skills/shell/SKILL.md) | POSIX shell inside a recipe |
| [jvm](skills/jvm/SKILL.md) | Java, Groovy, Grails, and Gradle |
| [go](skills/go/SKILL.md) | Go |

The `name` in each skill's frontmatter matches its directory. A project installs the stages, `record`, `project-setup`, `project-report`, the language skills it uses, and the subskills it wants. It installs `github-pipeline` when it publishes through GitHub. It installs `migrate-docs` when the old board is still present, and it runs that skill before the others.

`project-setup` and `github-pipeline` each have setup mode and report mode, written in the skill. Setup mode changes only what is missing or off the contract. Report mode names what matches and what is missing, and it changes nothing.

The rules that hold for every skill stand once, in the `<general_rules>` block of `CLAUDE.md`: the interface, the start of a task, the board, and the gates. Each `SKILL.md` starts with the line ``The general rules in `CLAUDE.md` apply.`` and states only what the skill adds. The body is XML tags: `purpose`, `steps`, `rules`, `output`, and `references`, with `mode` for a skill that has modes, and `questions` and `checks` for a subskill. A table, a sample, or a rule for one condition is in `references/` beside the skill. The agent reads such a file only when a step names it.

`make toon` writes the ADR index and the skill index for a product repository. In this collection it writes `docs/requirements-index.toon`, with the file and the owner of each row, and the skill index, and it does not create `docs/adr/`. `project.mk` and `sdlc.mk` include these targets from `record` when the skill is installed, and `make setup` runs `make toon` after `make doctor`. Every Python command, including a one-off `make py ARGS='...'`, runs in Podman on the machine where Make runs. Set `PYTHON_IMAGE` before the include to pick the version. The host does not need Python.

## The cycle

A request goes through `plan`, `develop`, `review`, and `release`. A new or vague request starts at `plan`. A fix that names a source file, a failing test, or a roadmap defect starts at `develop`. `release` commits the slice on one branch, pushes it, merges it into the default branch when CI passed, and asks `record` to close the task. With `github-pipeline` installed, that merge publishes.

`record` writes every board document. Each document has one job:

| Document | Holds |
| --- | --- |
| `docs/ROADMAP.md` | The things to do, one row each: id, kind (feature, defect, or question), title, and proposal. A row is not done. `record` deletes it when the slice closes |
| `docs/proposals/<id>.md` | The detailed plan of one roadmap row |
| `docs/adr/` and `docs/requirements/` | The rules in force. A product repository keeps ADRs and may keep requirement rows. This collection keeps only `docs/requirements/`, one file `<skill>.md` for each skill that owns rows, and `collection.md` for the rows with no owning skill. A row is `planned` (open work) or `in force`. `make req ID=R-45` prints one row, and `make req Q=<word>` finds rows |
| `docs/history/<id>.md` | The report of one slice. It is complete at any time and holds nothing that waits for a decision or for work |
| Code and tests | The current state. A test names the rule it proves with `id:` |

A choice that must hold becomes a requirement row, a sentence in an ADR, or a new ADR, as `record` decides. `develop` and `review` open each accepted ADR that names a skill the slice uses, so an agent follows the rules of this one project. Each id in a document is a link to its item, written by `make links`.

## Start

The host needs GNU Make 3.81 or newer, Git, and Podman. It needs no other tool: no APM, no Python, no GitHub CLI, and no Homebrew. Every other tool runs in a Podman image behind a Make target.

1. Add the `apm.yml` below. Then run this one line in the root of the project. It runs APM in a Podman image and installs the skills. The project has no Makefile before the skills are on the machine, so this line is the only command that is not `make` or `git`.

   ```sh
   podman run --rm -v "$PWD":/work:Z -w /work docker.io/library/python:3.13 sh -c 'pip install -q --root-user-action=ignore apm-cli==0.36.1 && apm install'
   ```

   Behind a proxy with its own CA, add `-v <CA file>:/ca.crt:ro -e GIT_SSL_CAINFO=/ca.crt -e SSL_CERT_FILE=/ca.crt` to the `podman run` arguments. For a private repository, add `-e GITHUB_APM_PAT`. These flags change only that one line. `PODMAN_NET_ARGS` holds the same arguments for the Make targets.

2. Tell the agent: `report and integrate`. The [onboard](skills/onboard/SKILL.md) skill carries the order, for a new project and for an existing one.

`onboard` does these steps, and each one is a skill that you can also start alone:

1. It checks that Make, Git, and Podman run on the machine, with `make -f .claude/skills/project-setup/doctor.mk doctor`. Once the Makefile has the include, `make doctor` is the same check, and `make setup` runs it first.
2. It reads the project: the language, the old board, the remote, and the tests. It asks you only what the files do not tell, such as how the project ships.
3. It runs `migrate-docs` when `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/DECISIONS.md`, `docs/KNOWN_ISSUES.md`, or their directories, or `AGENTS.md` exist, and commits the new board. `make old-board` tests those eight paths and a `docs/ROADMAP.md` in the old line form, which has a line that starts with `- `. It fails when one of these nine checks finds something. In a project with an old board, `make old-board` fails first, as designed, and the only skill is then `migrate-docs`.
4. It runs `project-setup` in report mode, then in setup mode. Setup mode asks how the project ships, copies the Makefile template of the language, and runs the tooling target of that language: `make node-tooling`, `make python-tooling`, `make jvm-tooling`, or `make go-tooling`. It writes `CLAUDE.md`, `.editorconfig`, and `.gitignore`, and commits with `.claude/skills/`, `apm.yml`, and `apm.lock.yaml`.
5. When the project publishes through GitHub, it runs `github-pipeline`: one workflow, a `Containerfile`, and the targets of the pipeline.
6. It records each rule the project already follows as an ADR or a requirement row, and gives each existing test the `id:` of the row it proves.
7. It runs every gate. It stops when one fails.

Then the first slice starts with `plan`. From here on, a person and the agent type only `make <target>` and Git commands. A typed tool of POSIX `sh`, such as `tail` or `grep`, may only shorten or search output, and writes no file.

## Update

This collection has tags named `vMAJOR.MINOR.PATCH`. A project that wants a fixed version sets `ref: v0.1.0` under the `git:` line of `apm.yml`. Without `ref`, APM follows the default branch and prints a warning.

To take a newer version:

1. Change `ref` to the new tag. Skip this step when the project has no `ref`.
2. Run `make skills-update`. `make skills-update DRY_RUN=1` shows the plan and changes nothing. The target runs `apm update --yes` in Podman, so it asks no question. `APM_VERSION` and `APM_IMAGE` in `tools.mk` of `project-setup` pin APM. `apm install --update` is deprecated in APM 0.36.1.
3. Run `make toon` and `make links`, because a new skill can add rows to the indexes and the links.
4. Run the gates of `CLAUDE.md`, and `make ci` when the project has a workflow.
5. Commit `.claude/skills/`, `apm.yml`, and `apm.lock.yaml` together, on the default branch.

APM 0.36.1 does not overwrite a skill file that a person changed in `.claude/skills/`. If such a file exists, `make skills-update` fails and names the file. Restore the file with `git restore <file>`, then run the target again. The target can also refuse when `.claude/skills/` holds files that APM did not install. APM calls them unmanaged. Run `make apm ARGS='install --force'`. That overwrites those files with the files of the collection. Keep project rules in a project skill or in `CLAUDE.md`, not in an installed file. A new Makefile template does not change the `Makefile` of the project. Run `project-setup` in report mode to see what a new version adds.

A project may hold documents with ids above the counters of `docs/ids.yaml`. Then `make ids` fails. Raise the counter of each such kind with `make id-raise KIND=<kind> TO=<n>`, where `<n>` is the highest number that a document uses.

## Test the collection in a test repository

The owner runs this test before a version tag of the collection. It runs the skills of a branch of this collection in a real project, in a repository that the owner may change. The Update section describes how a project takes a tagged version. This section describes how to try an untagged branch first.

Two branches of the test repository carry the test:

- `claude/framework-test-base` stands for the default branch. The pull request of the test merges into it.
- `claude/framework-test` is the work branch. The skills are installed on it, and every commit of the test goes on it.

The limits hold for every step:

- Never push to or change the default branch (`main`) of the test repository.
- Never delete a release, a tag, or a package version for real. Run a cleanup target only with `DRY_RUN=1`.
- Work only on the two test branches.

The workflow of `github-pipeline` runs on a push to any branch. Its `setup` job runs `make cleanup-actions-artifacts`, which deletes the Actions artifacts that are one hour old or older, except the artifacts `report` and `docs`. Its publish job runs only on the default branch of the repository, so neither test branch publishes. Do not dispatch `publish-container` on a test branch.

1. Create the branches. Run this in a clone of the test repository. `origin/main` is the default branch. The commands create two new branches and do not change `main`.

   ```sh
   git fetch origin
   git switch -c claude/framework-test-base origin/main
   git push -u origin claude/framework-test-base
   git switch -c claude/framework-test
   git push -u origin claude/framework-test
   ```

2. Install the branch of the collection on the work branch. APM reads the branch from GitHub, so push that branch of the collection first. Set `ref: <branch of the collection>` under the `git: rbe/ralfskills` line of `apm.yml`. Then run:

   ```sh
   make skills-update DRY_RUN=1
   make skills-update
   ```

   The dry run prints the plan with the old and the new commit. If `make skills-update` refuses and names a file in `.claude/skills/` that APM does not manage, run `make apm ARGS='install --force'`, as the Update section says. The files of the branch then replace such files. `apm.lock.yaml` then holds the commit of the branch as `resolved_commit`. Run `make toon` and `make links`. Commit `apm.yml`, `apm.lock.yaml`, and `.claude/skills/` on `claude/framework-test`.

3. Run the test on the work branch. The pull request targets read the base branch from `DEFAULT_BRANCH`. Without it, they use the default branch of the repository and would open the pull request into `main`. A value on the command line replaces the value that Make finds. Set `GH_TOKEN` or `GITHUB_TOKEN` in the environment.

   ```sh
   make old-board
   make editorconfig
   make format
   make lint
   make test
   make integration
   make coverage
   git push origin claude/framework-test
   make ci-status WAIT=1
   make pull-request DEFAULT_BRANCH=claude/framework-test-base
   make pull-request-merge WAIT=1 DEFAULT_BRANCH=claude/framework-test-base
   ```

   If `make old-board` fails, run the skill `migrate-docs` first, as `CLAUDE.md` says. `make ci-status WAIT=1` fails unless the run of the pushed commit passed. `make pull-request-merge` merges only when every check of the pull request passed. The merge is a push to the base branch, so it starts a second run. Pass `DEFAULT_BRANCH=claude/framework-test-base` to `make coverage` and `make test-changed` too when you want them to compare with the base branch.

4. Use the branches again for the next test:

   ```sh
   git fetch origin
   git switch claude/framework-test-base
   git merge origin/main
   git push origin claude/framework-test-base
   git switch claude/framework-test
   git merge claude/framework-test-base
   ```

   The first merge brings the base branch up to the default branch. The second merge brings the work branch up to the base branch. Install the newer collection as in step 2, run step 3 again, and commit before the push. The old pull request is closed after its merge, and `make pull-request` looks only for an open one, so it opens a new pull request.

5. Remove the branches when the test is over:

   ```sh
   git switch main
   git push origin --delete claude/framework-test claude/framework-test-base
   git branch -D claude/framework-test claude/framework-test-base
   ```

## How APM loads them

The `apm.yml` of a project needs `name` and `version`. APM refuses the file without them. `apm install` reads every `skills/<name>/` directory and copies it to `.claude/skills/<name>/`, including makefiles, `references/`, `scripts/`, and `templates/` inside the skills. That was tested with APM 0.36.1: nine skills installed into a sample project, and `make toon`, `make ids`, and `make project-report` ran there. This collection itself has no root `apm.yml`. APM does not need one in a skill collection.

```yaml
name: my-project
version: 0.1.0
targets:
  - claude
dependencies:
  apm:
    - git: rbe/ralfskills
      # ref: <tag or commit>   pins the version
      skills:
        - plan
        - develop
        - review
        - release
        - record
        - project-report
        - project-setup
        - onboard
        - system-state-report   # the plain-language report for the owner
        - board-merge-report    # finds repeated board text
        - board-merge           # applies the findings the owner chose
        - github-pipeline   # when the project publishes through GitHub
        - migrate-docs      # when the old board is still present
        - node              # or python, jvm, go: the language skills the project uses
        - shell
        - security
```

A Make-only repository leaves `github-pipeline` out. A repository that still has `docs/BUGS.md`, `docs/WAVES.md`, `docs/FEATURES.md`, `docs/DECISIONS.md`, `docs/KNOWN_ISSUES.md`, `docs/bugs/`, `docs/waves/`, or `docs/features/` adds `migrate-docs` and runs it first.

`apm install` does not write `CLAUDE.md`. `apm compile` for the target `claude` keeps a `CLAUDE.md` that a person wrote and prints a warning. That was tested with APM 0.36.1. `project-setup` owns the entry file. APM adds `apm_modules/` to `.gitignore`. It also creates `.apm-local/`, which has its own `.gitignore`.

`make skills-install` installs the skills that `apm.yml` names. `make apm ARGS='...'` is a one-off APM command in Podman. Install one skill with `make apm ARGS='install rbe/ralfskills --skill go'`. Repeat the flag to add another. `make apm ARGS="install rbe/ralfskills --skill '*'"` installs every skill again.
