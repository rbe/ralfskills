---
id: H-2026-11-27-glossary
title: Glossary of terms for the user and the agents
status: started
adrs: [R-153]
skills: [record, project-setup, system-state-report]
roadmap: []
proposals: []
---

# Glossary of terms for the user and the agents

## Plan

The owner asked whether a glossary for the communication between the user and the agents exists. Only `r-system-state-report` built a table, inside one report. The owner approved a glossary file that `r-record` owns. `r-plan` was not invoked, because the owner approved the scope in the chat.

## Develop

`r-record` has the template `templates/glossary.md` and a rule for `docs/glossary.md`. The communication contract tells each agent to use the term of the glossary. `r-system-state-report` reads and extends the glossary and builds no own table. This collection has a first `docs/glossary.md` with 12 terms. The rule is [R-153](../requirements/record.md#r-153).

## Review

Not invoked yet.

## Release

Not invoked yet.
