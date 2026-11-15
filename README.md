# ralfskills

Skills for [Microsoft APM](https://github.com/microsoft/apm). This repository is a [skill collection](https://microsoft.github.io/apm/reference/package-types/#skill-collection-skillsnameskillmd): each skill is `skills/<name>/SKILL.md`. There is no `SKILL.md` at the repository root, so APM does not treat the repository as one skill.

## Skills

| Skill | What it covers |
| --- | --- |
| [project-setup](skills/project-setup/SKILL.md) | Make is the only interface. `help` is the default goal. A target does the same thing locally and in CI |
| [github-pipeline](skills/github-pipeline/SKILL.md) | One GitHub workflow. Versions from a `vMAJOR.MINOR.PATCH` tag plus the run number |

The `name` in each skill's frontmatter matches its directory. `github-pipeline` depends on `project-setup` because a workflow calls `make` and each job name is a target from that contract. A Make-only repository installs `project-setup` only.

## How APM loads them

`apm install` reads every `skills/<name>/` directory and copies it to that harness's `skills/<name>/` directory, including `project.mk`, `sdlc.mk`, and `templates/` inside the skills. A root `apm.yml` is optional. APM fills in metadata when the file is absent.

Install the collection:

```bash
apm install rbe/ralfskills
```

Install one skill. Repeat `--skill` to add another. The name is the directory under `skills/`.

A repository that uses Make and does not publish through GitHub:

```bash
apm install rbe/ralfskills --skill project-setup
```

A repository that also runs the GitHub workflow:

```bash
apm install rbe/ralfskills --skill project-setup --skill github-pipeline
```

The same choice in a project's `apm.yml`:

```yaml
dependencies:
  apm:
    - git: rbe/ralfskills
      skills:
        - project-setup
        - github-pipeline
```

A Make-only repository lists `project-setup` and leaves `github-pipeline` out.

A later `apm install` keeps that selection. `apm install rbe/ralfskills --skill '*'` installs every skill again.
