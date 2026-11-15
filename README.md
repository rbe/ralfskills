# ralfskills

Skills for [Microsoft APM](https://github.com/microsoft/apm). This repository is a [skill collection](https://microsoft.github.io/apm/reference/package-types/#skill-collection-skillsnameskillmd): each skill is `skills/<name>/SKILL.md`. There is no `SKILL.md` at the repository root, so APM does not treat the repository as one skill.

## Skills

| Skill | What it covers |
| --- | --- |
| [github-pipeline](skills/github-pipeline/SKILL.md) | Make is the interface, one GitHub workflow, versions from a `vMAJOR.MINOR.PATCH` tag |

The `name` in that skill's frontmatter is `github-pipeline`, the same as its directory.

## How APM loads them

`apm install` reads every `skills/<name>/` directory and copies it to that harness's `skills/<name>/` directory, including `sdlc.mk` and `templates/` inside the skill. A root `apm.yml` is optional. APM fills in metadata when the file is absent.

Install the collection:

```bash
apm install rbe/ralfskills
```

Install one skill. Repeat `--skill` to add another. The name is the directory under `skills/`.

```bash
apm install rbe/ralfskills --skill github-pipeline
```

The same choice in a project's `apm.yml`:

```yaml
dependencies:
  apm:
    - git: rbe/ralfskills
      skills:
        - github-pipeline
```

A later `apm install` keeps that selection. `apm install rbe/ralfskills --skill '*'` installs every skill again.
