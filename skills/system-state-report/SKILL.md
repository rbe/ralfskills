---
name: system-state-report
description: Write a plain-language report on what an agent-built system does now, which decisions shaped it, and what the human must decide. Use for 'state report', 'what did we build', 'review the system'.
---

# System state report

## Purpose

A human and one or more agents built a system through many chats. The human can no longer see the full state. This report lets the human check the state and decide the direction. The report is successful if the human understands each sentence on the first reading and can make each open decision without a question back to you.

The reader knows the goal of the project. The reader did not read the code and does not remember the chats. Do not assume that the reader knows a name that an agent invented.

The communication contract in `CLAUDE.md` applies to the report in full. This skill adds the rules of a report below.

## Step 1: Collect the evidence

Read before you write. Do not describe a file that you did not open.

- The repository: structure, entry points, configuration, tests.
- The history: `git log`, and the diffs of the period the user asks about. If the user gives no period, use the full history or the time since the last report in `reports/`.
- The board: `docs/DECISIONS.md`, `docs/KNOWN_ISSUES.md`, `docs/REQUIREMENTS.md` when it exists, the ADRs in `docs/adr/`, and the history files in `docs/history/`. Run `make toon` before you read an index.
- The generated report, from `make project-report`, when `project-report` is installed.
- The current chat, and any transcripts or notes the user supplies.
- Run the tests through Make and start the system if you can do this without a change to data or to external systems. Record the real result.

If you cannot read or run something, write that down. It goes in the section "Not verified".

## Step 2: Build the glossary

Do this before you write the report.

1. List the things the report must name: components, data, actors, processes.
2. For each thing, select one name. Use this order of preference: the word the user uses, then the identifier in the code, then a plain descriptive phrase.
3. Find names that agents invented during the work (labels that appear in chat or commit messages, but not in the code and not in the user's own words). Replace each one with a name from item 2, or define it in one sentence.
4. Write the glossary as a table: name, what it is in one sentence, where it is in the project (path).

Use each name with one meaning only. Do not use a second word for the same thing.

## Step 3: Write the report

Write in the language the user writes in. Use these sections in this order. Omit a section only if it has no content, and then say so in one line.

1. **Summary.** Five sentences maximum. What the system does now, the largest difference from what was asked, and the number of decisions that wait for the human.
2. **What the system does now.** A list of behaviours that a person can observe. Form: "When [actor] does [action], the system does [result]." Not a list of files or modules.
3. **Differences from what was asked.** Each item: what was asked (with the source), what exists, the effect for the user.
4. **Decisions that were made.** A table: the decision, who made it (human, agent, or agent without a question to the human), the alternative that was rejected, the reason, and whether it is easy to reverse. Put decisions that an agent made without a question to the human first.
5. **Not verified.** What you could not run or read, and what is only claimed in chat.
6. **Risks and defects.** Only those you can point to. Each with the location and the effect.
7. **Decisions for you.** Each item is a question the human can answer with a selection. Give the options, the effect of each option, and your recommendation with one reason.
8. **Glossary.** The table from step 2.

### Evidence rule

Each statement in sections 2 to 6 has a source and a status.

- Source: `path/to/file:line`, a commit hash, a test name, or a chat passage (date or short quote).
- Status: **ran** (you executed it in this session and saw the result), **read** (you read it in the code, you did not execute it), or **said** (it is only stated in a chat or a commit message).

If you cannot give a source, delete the statement. Do not change **read** or **said** into **ran**.

### Rules of a report

These rules add to the communication contract. The contract has the rest.

- A sentence that tells the reader to do something has at most 20 words.
- Present tense for the current state. Past tense only for events.
- Use the glossary name each time. The glossary defines each abbreviation. Use no other abbreviation.
- No words that judge without a measure: robust, clean, seamless, simple, powerful, improved, optimized, comprehensive. Say what changed and what the effect is.
- Do not make noun chains of more than three nouns. In German, break long compounds with a hyphen or rewrite them.
- Lists for parallel items, tables for comparisons, sentences for cause and effect.

Bad: "Refactored the persistence layer for improved robustness and streamlined the sync path."

Good: "The function `save_order` in `db/orders.py` now tries a failed write 3 times. Before, one failed write stopped the import. Status: read. Source: commit `a1b2c3d`."

## Step 4: Cold-reader check

Do not skip this step. You cannot find your own unclear terms, because you know what they mean.

If you can start a subagent: give it only the report. Give it no code, no chat and no explanation. Ask it to return:

- each term that the report does not define and that is not a common word,
- each sentence that it can read in two ways,
- each statement without a source and status,
- each sentence that breaks the communication contract or a rule of a report,
- for each item in "Decisions for you": whether it can select an option with only the report.

Correct each finding. Run the check again if the first run had more than five findings.

If you cannot start a subagent: read the report sentence by sentence against the glossary and the rules, and tell the user that no independent reader checked the report.

## Step 5: Deliver

- Save the report as `reports/state-YYYY-MM-DD.md` in the project. Do not change other files, except the decision rows that `record` writes as described below.
- In the chat, give the summary and the list "Decisions for you". Do not repeat the full report.
- A decision of section 4 that `docs/DECISIONS.md` and `docs/adr/` do not contain is missing from the board. Ask `record` to add it: a small choice is a Decided row, and a rule is an ADR. Tell the user which rows you added.

## Decisions that nobody recorded

A report shows only the decisions that someone recorded. In this collection, `record` keeps them: a small choice is a row in `docs/DECISIONS.md`, and an architecture or development rule is an ADR. If the report finds an agent decision that has no row, say so in section 4, and name the missing rows in the chat. The entry file `CLAUDE.md` already tells each agent where a decision goes. Do not add a second instruction file.
