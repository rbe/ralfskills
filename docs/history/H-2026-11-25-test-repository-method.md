---
id: H-2026-11-25-test-repository-method
title: The test in a test repository is documented
status: closed
adrs: [R-100]
skills: [develop, review, record]
roadmap: []
proposals: []
---

# The test in a test repository is documented

## Plan

The owner merged PR 29, removed the two test branches of the repository rbe/gh-sweep, and asked to document how to use those branches again, so that a testing method exists. `plan` was not invoked.

The two branches were `claude/framework-test-base`, which stood for the default branch, and `claude/framework-test`, the work branch. The test put the skills on the work branch, ran `make old-board`, `migrate-docs` when it failed, the gates, a push, the GitHub Actions run, `make ci-status WAIT=1`, `make pull-request`, and `make pull-request-merge WAIT=1`. Its limits were: never push to or change `main`, never delete a release, a tag, or a package version for real, and work only on the two test branches.

## Develop

The README has a section "Test the collection in a test repository" after the Update section. It has five numbered steps: create the branches, install the branch of the collection, run the test, use the branches again, and remove them. [R-100](../requirements/collection.md#r-100) states the rule. One test in `skills/project-report/scripts/test_project_report.py` pins the heading, the two branch names, the three limits, and the command line of `make pull-request-merge`.

Facts read in the code: `DEFAULT_BRANCH` in `skills/project-setup/tools.mk` is set only when no value exists, so a value on the command line replaces it. `pull-request` and `pull-request-merge` in `skills/github-pipeline/sdlc.mk` read it for the base branch. The workflow template runs on a push to any branch. Its publish job runs only on the default branch of the repository. Its `setup` job deletes Actions artifacts that are one hour old.

Install trial in a local checkout of rbe/gh-sweep on `claude/framework-test`, with `ref: claude/dev-framework-review-7lu8tr` under the git line of `apm.yml`. `make skills-update DRY_RUN=1` printed the plan from the old commit 995e6b5 to 26b5d77. `make skills-update` refused: the checkout held skill files that APM did not manage. `make apm ARGS='install --force'` installed the branch and wrote `resolved_commit` 26b5d770 and `resolved_ref` of the branch into `apm.lock.yaml`. The checkout was restored with `git checkout -- .`. Nothing was committed or pushed there.

## Review

`make toon`, `make links`, `make ids`, `make links-check`, `make editorconfig`, `make format`, `make lint`, and `make test` ran after the last edit. The results are in the report of the commit.

security: the README names the one real deletion that the workflow does, the Actions artifacts of the test repository. No secret.

privacy, ux-ui-design, api-design: not touched.

Not run: `make integration` and `make coverage`, and the steps of the README on GitHub, which this slice did not push.

## Release

Not invoked: the owner pushes this slice.
