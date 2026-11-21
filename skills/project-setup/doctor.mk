# make doctor checks the tools a machine needs before any other target
# runs. project.mk and the sdlc.mk of github-pipeline both include this
# file, and `make setup` runs it first. It changes nothing.
#
# Checks, each printed as ok or FAIL with the fix:
#   make    GNU Make 3.81 or newer
#   git     runs
#   podman  `podman info` works. On macOS a stopped Podman machine fails
#           that command: start it with `podman machine start`
#   origin  a remote named origin, when the project has a workflow
#   gh      the GitHub CLI, when the project has a workflow. A missing
#           gh is a warning, because only the cleanup targets need it
#
# Set DOCTOR_SKIP_PODMAN=1 for a project that does not use Podman.
# GNU Make 3.81. See project.mk for the rules of a recipe.

ifndef DOCTOR_MK
DOCTOR_MK := 1

DOCTOR_SKIP_PODMAN ?=

.PHONY: doctor

doctor: ## Check that this machine has the tools the targets need
	@set -u; \
	failed=0; \
	ok() { printf '  ok    %s\n' "$$1"; }; \
	bad() { printf '  FAIL  %s\n        %s\n' "$$1" "$$2"; failed=1; }; \
	warn() { printf '  warn  %s\n        %s\n' "$$1" "$$2"; }; \
	os=$$(uname -s); \
	printf '%s\n' "doctor: $$os"; \
	version=$$($(MAKE) --version 2>/dev/null | sed -n '1s/[^0-9]*\([0-9][0-9]*\)\.\([0-9][0-9]*\).*/\1 \2/p'); \
	major=$${version%% *}; minor=$${version##* }; \
	if [ -n "$$major" ] && { [ "$$major" -gt 3 ] || { [ "$$major" -eq 3 ] && [ "$$minor" -ge 81 ]; }; }; then \
	  ok "make $$major.$$minor"; \
	else \
	  bad "make is older than 3.81 or not GNU Make" "Install GNU Make 3.81 or newer."; \
	fi; \
	if git --version >/dev/null 2>&1; then ok "$$(git --version)"; \
	else bad "git does not run" "Install Git. On macOS: xcode-select --install"; fi; \
	if [ -n "$(DOCTOR_SKIP_PODMAN)" ]; then \
	  ok "podman skipped by DOCTOR_SKIP_PODMAN"; \
	elif ! command -v podman >/dev/null 2>&1; then \
	  if [ "$$os" = "Darwin" ]; then hint="Install Podman: brew install podman, then podman machine init and podman machine start."; \
	  else hint="Install Podman with the package manager of this system."; fi; \
	  bad "podman is not on PATH" "$$hint"; \
	elif podman info >/dev/null 2>&1; then \
	  ok "podman runs"; \
	else \
	  if [ "$$os" = "Darwin" ]; then hint="Run podman machine start. When no machine exists, run podman machine init first."; \
	  else hint="Run podman info and read the error."; fi; \
	  bad "podman info fails" "$$hint"; \
	fi; \
	if [ -d .github/workflows ]; then \
	  if git remote get-url origin >/dev/null 2>&1; then ok "git remote origin"; \
	  else bad "no git remote named origin" "Run git remote add origin <url>. The workflow and the image name read it."; fi; \
	  if command -v gh >/dev/null 2>&1; then ok "gh runs"; \
	  else warn "gh is not on PATH" "Only the cleanup targets need it. Install it with: brew install gh"; fi; \
	fi; \
	if [ "$$failed" -ne 0 ]; then printf '%s\n' "doctor: fix the FAIL lines, then run make doctor again." >&2; exit 1; fi; \
	printf '%s\n' "doctor: ready"

endif
