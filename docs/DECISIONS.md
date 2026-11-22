# Decisions

One list. An Open row is work that is not finished. A Decided row is a choice in force.

| Id | Status | Choice |
| --- | --- | --- |
| <a id="d-3"></a>D-3 | Decided | This collection keeps one requirements list and records open work and choices in force in this list. |
| <a id="d-17"></a>D-17 | Decided | `sdlc.mk` has `make ci-status`, `make pull-request`, and `make pull-request-merge`, so `release` reads the CI result and merges through a pull request with no question to the owner. `tar` stays allowed as a tool of POSIX `sh`. `project-setup` keeps its new behaviour for an existing `CLAUDE.md`. A repository with `docs/REQUIREMENTS.md` and no `docs/adr/` reads the requirements index where a step names the ADR index. |
| <a id="d-18"></a>D-18 | Decided | Board cleanup is two skills. `board-merge-report` writes nothing and `board-merge` does what the owner chose by id, with one commit for each finding. A history file is deleted and never merged, and the numbers come from `make board-numbers`, as [R-77](REQUIREMENTS.md#r-77) and [R-78](REQUIREMENTS.md#r-78) say. |
