# Decisions

One list. An Open row is work that is not finished. A Decided row is a choice in force.

| Id | Status | Choice |
| --- | --- | --- |
| <a id="d-3"></a>D-3 | Decided | This collection keeps one requirements list and records open work and choices in force in this list. |
| <a id="d-5"></a>D-5 | Decided | This collection keeps no test on skill wording. The unit tests cover the scripts. |
| <a id="d-6"></a>D-6 | Decided | `project-setup` has the one template of the entry file. A product repository gets the communication contract from that template. |
| <a id="d-8"></a>D-8 | Decided | For Vitest, `make test-changed` uses `vitest related`. That selection is the module graph of Vitest, not coverage. |
| <a id="d-9"></a>D-9 | Decided | A test names an ADR or a decision. It does not name a roadmap line or a known issue, because those ids are retired when the work ends. |
| <a id="d-10"></a>D-10 | Decided | Setup mode asks how the project ships before it copies a Makefile template. A project that ships a binary sets its build command in that step. |
| <a id="d-11"></a>D-11 | Decided | An agent runs a Go program with `make run`, in the container. The file in `build/` is a Linux binary, and `GOOS` and `GOARCH` give the binary of another machine. |
| <a id="d-12"></a>D-12 | Decided | An id in running text is a link, and a tool writes it. This replaces the rule that a document does not build a path to another document. |
| <a id="d-13"></a>D-13 | Decided | `sdlc.mk` includes the contract targets of `project-setup`, so the switch from `project.mk` loses no target. A makefile with its own recipes for them sets `SDLC_OWN_CONTRACT = 1`. |
| <a id="d-14"></a>D-14 | Decided | The talking rules of the owner are the communication contract in `CLAUDE.md` and in its template, and replace the shorter text there. `system-state-report` keeps only the rules that the contract lacks, and sends a missing decision to `record`. |
| <a id="d-15"></a>D-15 | Decided | The general rules stand once in `CLAUDE.md` and in its template, a person and an agent type only `make <target>` and Git commands while every other tool runs in a Podman image, the first start is one `podman run` line in the README, and each `SKILL.md` is steps and rules in XML tags with the rest in reference files, as [R-75](REQUIREMENTS.md#r-75) and [R-76](REQUIREMENTS.md#r-76) say. |
| <a id="d-16"></a>D-16 | Decided | `make jvm-tooling` counts `build.gradle.kts` and `settings.gradle.kts` as present, so a project with a Kotlin build file gets no second build file, as [R-66](REQUIREMENTS.md#r-66) says. A test reads the recipe in `skills/jvm/templates/Makefile.gradle`. |
| <a id="d-17"></a>D-17 | Decided | `sdlc.mk` has `make ci-status`, `make pull-request`, and `make pull-request-merge`, so `release` reads the CI result and merges through a pull request with no question to the owner. `tar` stays allowed as a tool of POSIX `sh`. `project-setup` keeps its new behaviour for an existing `CLAUDE.md`. A repository with `docs/REQUIREMENTS.md` and no `docs/adr/` reads the requirements index where a step names the ADR index. |
