---
name: system-state-report
description: Writes a plain-language report on what an agent-built system does now, which decisions shaped it, and what the human must decide. Use for 'state report', 'what did we build', 'review the system'.
---

The general rules in `CLAUDE.md` apply.

<purpose>
The report lets a human check the state of a system that agents built through many chats, and decide the direction.
The report is successful if the reader understands each sentence on the first reading and can make each open decision without a question back.
</purpose>

<steps>
1. Collect the evidence. Read before you write. Write down each thing that you cannot read or run. It goes in the section "Not verified".
   - The repository: structure, entry points, configuration, tests.
   - The history: `git log`, and the diffs of the period that the user names. If the user names no period, use the time since the last report in `reports/`, or the full history.
   - The board: `docs/DECISIONS.md`, `docs/KNOWN_ISSUES.md`, `docs/REQUIREMENTS.md`, the ADRs in `docs/adr/`, and the history files in `docs/history/`, each when it exists.
   - `build/project-report.md`, after you run `make project-report`, when `project-report` is installed.
   - The current chat, and the transcripts or notes that the user supplies.
   - The result of `make test`, and of the Make target that starts the system. Run each only if it changes no data and no external system. Record the real result.
2. Build the glossary before you write the report.
   - List the things that the report must name: components, data, actors, processes.
   - Select one name for each thing. Prefer the word of the user, then the identifier in the code, then a plain descriptive phrase.
   - Find each label that appears in a chat or a commit message, but not in the code and not in the words of the user. Replace it with a selected name, or define it in one sentence.
   - Write a table: the name, what it is in one sentence, and its path in the project.
3. Write the report in the language of the user. Use these sections in this order. If a section has no content, say so in one line.
   1. Summary. Maximum 5 sentences: what the system does now, the largest difference from what was asked, and the number of decisions that wait for the human.
   2. What the system does now. A list of behaviours that a person can observe, in the form "When [actor] does [action], the system does [result]." Do not list files or modules.
   3. Differences from what was asked. Each item: what was asked, with the source; what exists; the effect for the user.
   4. Decisions that were made. A table: the decision; who made it (human, agent, or agent without a question to the human); the rejected alternative; the reason; whether it is easy to reverse. Put the decisions that an agent made without a question first. Mark each decision that has no row in `docs/DECISIONS.md` and no ADR.
   5. Not verified. What you could not run or read, and what only a chat claims.
   6. Risks and defects. Only those that you can point to, each with the location and the effect.
   7. Decisions for you. Each item is a question that the human answers with a selection. Give the options, the effect of each option, and your recommendation with one reason.
   8. Glossary. The table from step 2.
4. Run the cold-reader check, because you cannot find your own unclear terms. Give a subagent only the report: no code, no chat, no explanation. Ask it to return the items below. Correct each finding. If the first run had more than 5 findings, run the check again.
   - Each term that the report does not define and that is not a common word.
   - Each sentence that it can read in two ways.
   - Each statement without a source and a status.
   - Each sentence that breaks the communication contract or a rule of this skill.
   - For each item in "Decisions for you": whether it can select an option with only the report.
   If you cannot start a subagent, read the report sentence by sentence against the glossary and the rules. Tell the user that no independent reader checked the report.
5. Save the report as `reports/state-YYYY-MM-DD.md`.
6. Ask `record` to add each decision that step 3 marked as missing from the board. A row that `record` adds has the status Decided.
7. In the chat, give the summary, the list "Decisions for you", and the rows that `record` added. Do not repeat the full report.
</steps>

<rules>
- Do not describe a file that you did not open.
- Each statement in sections 2 to 6 has a source and a status. If a statement has no source, delete it.
- A source is `path/to/file:line`, a commit hash, a test name, or a chat passage with a date or a short quote.
- A status is one of three words. "ran": you executed it in this session and saw the result. "read": you read it in the code and did not execute it. "said": only a chat or a commit message states it. Do not change "read" or "said" into "ran".
- The communication contract in `CLAUDE.md` applies to the report. The rules below add to it.
- A sentence that tells the reader to do something has at most 20 words.
- Use present tense for the current state. Use past tense only for events.
- The glossary defines each abbreviation. Use no other abbreviation.
- Do not use these judging words: robust, clean, seamless, simple, powerful, improved, optimized, comprehensive.
- A noun chain has at most 3 nouns. In German, break a long compound with a hyphen or rewrite it.
- Use a list for parallel items, a table for a comparison, and sentences for cause and effect.
- Change no file other than the report and the rows that `record` writes. Do not add a second instruction file: `CLAUDE.md` tells each agent where a decision goes.
</rules>

<example>
The import job tries a failed write 3 times. Status: read. Source: `db/orders.py:41`.
</example>
