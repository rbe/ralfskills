---
id: H-2026-11-27-product-skill-takeaways
title: Generic rules from the cleanup of a product skill set
status: started
adrs: [R-131, R-132, R-133, R-134, R-135, R-136, R-137, R-138, R-139, R-140, R-141, R-142, R-143, R-144, R-145, R-146, R-147, R-148, R-149, R-150, R-151, R-152]
skills: [plan, develop, review, record, api-design, privacy, ux-ui-design, node]
roadmap: []
proposals: []
---

# Generic rules from the cleanup of a product skill set

## Plan

The owner approved the 13 takeaways of the cleanup review of one product skill set, dated 2026-11-27. Declined: a rule for temporary document blocks in `r-record`, because `r-develop` owns the work that creates the gap.

## Develop

`r-api-design` has five new questions and checks. `r-privacy` has two checks. `r-ux-ui-design` has one question and five checks. `r-review` has an incident section. `r-develop` has three rules. `r-node` has the upgrade order, the risks, the file list of a Node major change, a package checklist, and the Vitest facts. `make ids` now checks the frontmatter and the status of each ADR file. Each rule is one row, [R-131](../requirements/api-design.md#r-131) to [R-152](../requirements/record.md#r-152).

## Review

The 270 unit tests of `UNIT_TESTS` passed. `ruff format --check` and `ruff check` passed with ruff 0.15.2. `make ids` and `make links-check` passed as direct script runs. Not run: `make gates`, because this machine has no Podman. No `make coverage` run.

## Release

Not invoked yet.
