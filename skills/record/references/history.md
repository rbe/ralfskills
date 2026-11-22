# History file

## Sections

Every history file has these 4 headings.

| Section | When the stage ran | When it did not |
| --- | --- | --- |
| Plan | Questions and answers | One sentence. `plan` writes this section when it creates the file |
| Develop | What changed, and which language skill was used | `Not invoked yet.` while the task is open. When the task closes or waits, one sentence |
| Review | Gates, subskill checks, findings, what was left alone | The same pattern as Develop. |
| Release | What shipped | `Not invoked: this slice does not ship.` or `Not invoked yet.` |

## Rules

- If a proposal is picked up, set `proposals:` in the new history file to that id, set the proposal status to `started`, and write both ids in the roadmap line.
- A history file is complete at every stage end. It holds no open question, no sentence that waits for the owner, and no item to decide. Write open work to an Open row of `docs/DECISIONS.md`, to a known issue, or to a proposal, and name that id in the section.
- A question that the owner answered stays in Plan with its answer.
- Reject a history file that is missing the heading Plan, Develop, Review, or Release.
- Frontmatter lists: `skills` lists each skill the slice used, which are the stages, the language skills, and the subskills. `decisions`, `adrs`, and `issues` list the ids the slice wrote, fixed, or proves with a test. `proposals` lists only the proposal the slice started from. A proposal that the slice wrote for a later part is named in the Plan section.
