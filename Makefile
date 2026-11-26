# Collection checks. Python runs in Podman on this machine.
# `make` prints help. `make test` runs the full suite.
# `make test-changed` runs the tests that cover the diff.
# `make project-report` writes the generated report.
# Ruff is the formatter and the linter. editorconfig-checker reads
# .editorconfig. diff-cover writes the lines this change touched.

# No install step. Ruff and editorconfig-checker are container images.
SETUP_CMD = true
BUILD_CMD = true
UNIT_TESTS = skills/r-record/scripts/test_record.py skills/r-project-report/scripts/test_project_report.py skills/r-board-merge-report/scripts/test_board_numbers.py skills/r-project-setup/scripts/test_check_docs.py
TEST_CMD = $(PYTHON) -m unittest $(UNIT_TESTS)
TEST_CHANGED_CMD = $(PYTHON) skills/r-project-report/scripts/changed_tests.py
PROJECT_REPORT_CMD = $(PYTHON) skills/r-project-report/scripts/project_report.py
FORMAT_CMD = podman run --rm -v "$(CURDIR)":/io:Z -w /io $(RUFF_IMAGE) format --check
FORMAT_FIX_CMD = podman run --rm -v "$(CURDIR)":/io:Z -w /io $(RUFF_IMAGE) format
LINT_CMD = podman run --rm -v "$(CURDIR)":/io:Z -w /io $(RUFF_IMAGE) check
# No integration entry. The unit tests cover the scripts.
INTEGRATION_CMD = true
COVERAGE_CMD = set -eu; \
	podman run --rm -e HOME=/tmp -e PYTHONDONTWRITEBYTECODE=1 $(PODMAN_NET_ARGS) -v "$(CURDIR)":/work:Z -w /work $(PYTHON_IMAGE) sh -c 'set -eu; pip install --disable-pip-version-check --root-user-action=ignore -q --target /tmp/py "coverage==$(COVERAGE_VERSION)"; PYTHONPATH=/tmp/py python3 skills/r-project-report/scripts/cover_tests.py $(UNIT_TESTS)'; \
	REPORT=build/coverage/coverage.xml $(DIFF_COVER)

include skills/r-project-setup/project.mk
# This collection is not installed under .claude/skills, so the index
# target is included from the skill source. A product Makefile includes
# project.mk, which includes the installed copy.
include skills/r-record/index.mk
include skills/r-board-merge-report/merge-report.mk

.DEFAULT_GOAL := help
