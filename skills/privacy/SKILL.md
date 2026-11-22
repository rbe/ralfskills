---
name: privacy
description: Asks the privacy questions for plan and runs the privacy checks for review. Use before a slice is closed and after implementation, when the change stores, logs, exports, or shows personal data.
kind: check
order: 20
---

The general rules in `CLAUDE.md` apply.

<purpose>
The checks limit where a change stores, shows, logs, and exports personal data.
</purpose>

<questions>
1. What personal data is stored, shown, logged, or exported?
2. What remains if a log or a fixture is copied out of the machine?
3. Who asked for the export?
</questions>

<checks>
1. Logs, errors, and fixtures contain no personal data.
2. An export is one the user asked for in this slice.
3. Example data is marked as an example. Real data is not in the tree.
</checks>
