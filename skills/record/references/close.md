# Close mode

Do these steps in order after step 1 of close mode has passed.

1. Set the history status to `closed`.
2. Delete the roadmap line that cites this history id. After `make links` the line is a link, so match the id in the link text. Read `docs/ROADMAP.md` again and stop if a line still names the id.
3. If the slice started from a proposal, set the proposal status to `done`.
4. If the slice fixed a known issue, delete that row and retire its id. If a test still names that id, stop: the test must name a rule, as the test rules of `SKILL.md` say. Write that Decided row when there is none.
5. Leave each ADR and each Decided row. They stay in force.
6. In a repository that keeps `docs/REQUIREMENTS.md` and no `docs/ROADMAP.md`, delete the Open row for this task and retire its id.

A task whose work waits stays open. A slice that is done and waits only for the merge of the owner is closed on its branch.
