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
