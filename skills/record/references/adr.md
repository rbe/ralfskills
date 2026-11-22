# ADRs

## When

- `plan` says when a choice is an ADR. `record` writes `docs/adr/<id>.md` with the status `Accepted`. The Plan section of the history file cites that id.

## Body

- `## Rule`: what an agent must do or must not do, in sentences that `review` can check.
- `## Why`: the reason, and the options that were not chosen.
- `## Divergence`: only in an ADR that replaces a skill rule.
- Keep the ADR short. Do not copy the grill.

## Status

- `record` owns the status.
- A new ADR names the ADR it replaces in `supersedes`. `record` then sets the status of the replaced ADR to `Superseded`.
- The project report does not list a superseded ADR as an id with no test.

## `skills`

- `skills` names each skill whose work the ADR governs. Each name is an installed skill: a stage, a language skill, or a subskill.
- A rule for every change names the two stages that every slice uses: `skills: [develop, review]`.
- A rule for one language names that language skill too: `skills: [python, develop, review]`.
- `develop` and `review` open an accepted ADR when `skills` names a skill the slice uses.
- An ADR with an empty `skills` list has no reader. Do not write one.
