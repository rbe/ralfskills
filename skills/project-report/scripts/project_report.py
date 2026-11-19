#!/usr/bin/env python3
"""Write the project report. Hand-editing the file is a defect."""

import importlib.util
import sys
from pathlib import Path

ARCHITECTURE_CHECKS = (("plan", "## Work"), ("review", "## Work"))
DEVELOPMENT_CHECKS = (
    ("develop", "## Work"),
    ("review", "## Work"),
    ("release", "## Work"),
    ("project-setup", "## Quality targets"),
)


def sibling(name: str):
    loaded = sys.modules.get(f"_project_report_{name}")
    if loaded is not None:
        return loaded
    path = Path(__file__).resolve().parent / f"{name}.py"
    spec = importlib.util.spec_from_file_location(f"_project_report_{name}", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    if spec.loader is None:
        raise ImportError(f"cannot load {path}")
    spec.loader.exec_module(module)
    return module


def skill_text(root: Path, name: str) -> str | None:
    for base in (root / ".claude" / "skills", root / "skills"):
        path = base / name / "SKILL.md"
        if path.is_file():
            return path.read_text(encoding="utf-8")
    return None


def numbered_steps(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index + 1
            break
    if start is None:
        return []
    steps = []
    current = ""
    for line in lines[start:]:
        if line.startswith("#"):
            break
        match_indent = line.startswith((" ", "\t"))
        numbered = line[:1].isdigit() and ". " in line[:4]
        if numbered and not match_indent:
            if current:
                steps.append(current)
            current = line.strip()
            continue
        if current and match_indent and line.strip():
            current = f"{current} {line.strip()}"
            continue
        if current and not line.strip():
            steps.append(current)
            current = ""
    if current:
        steps.append(current)
    return steps


def content_lines(path: Path) -> list[str]:
    if not path.is_file():
        return []
    lines = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            stripped = stripped[2:].strip()
        lines.append(stripped)
    return lines


def cell(text: str) -> str:
    return text.replace("|", "/")


def tests_for(requirement_id: str, proofs_found) -> list[str]:
    return sorted(
        proof.qualified_name
        for proof in proofs_found
        if proof.requirement_id == requirement_id
    )


def format_requirement(item, proofs_found) -> str:
    proved = tests_for(item.id, proofs_found)
    names = "; ".join(proved) if proved else "no test"
    status = item.status or "unspecified"
    title = item.title or item.id
    return f"- {item.id}, {status}, {item.kind}. {title}. Proved by: {names}."


def append_requirements(lines: list[str], items, proofs_found, kind: str) -> None:
    chosen = [item for item in items if item.kind == kind]
    if not chosen:
        lines.append("None.")
        lines.append("")
        return
    for item in chosen:
        lines.append(format_requirement(item, proofs_found))
    lines.append("")


def append_lines(lines: list[str], entries: list[str]) -> None:
    if not entries:
        lines.append("None.")
    else:
        for entry in entries:
            lines.append(f"- {entry}")
    lines.append("")


def append_checks(lines: list[str], root: Path, checks) -> None:
    for name, heading in checks:
        lines.append(f"#### {name}")
        lines.append("")
        text = skill_text(root, name)
        if text is None:
            lines.append(f"{name}: not installed")
            lines.append("")
            continue
        steps = numbered_steps(text, heading)
        if not steps:
            lines.append("None.")
        else:
            for step in steps:
                lines.append(f"- {step}")
        lines.append("")


def append_proof_map(lines: list[str], requirements, proofs_found) -> None:
    lines.append("| Id | Kind | Status | Tests |")
    lines.append("| --- | --- | --- | --- |")
    for item in requirements:
        proved = tests_for(item.id, proofs_found)
        names = "; ".join(proved) if proved else "no test"
        lines.append(
            f"| {cell(item.id)} | {cell(item.kind)} | {cell(item.status)} | {cell(names)} |"
        )
    lines.append("")
    lines.append("### Ids with no test")
    lines.append("")
    gaps = [item for item in requirements if not tests_for(item.id, proofs_found)]
    if not gaps:
        lines.append("None.")
    else:
        for item in gaps:
            lines.append(f"- {item.id} ({item.kind})")
    lines.append("")
    lines.append("### Tests with no id")
    lines.append("")
    missing = [
        proof.qualified_name for proof in proofs_found if proof.requirement_id is None
    ]
    append_lines(lines, missing)
    lines.append("### Tests whose id is not a requirement")
    lines.append("")
    known = {item.id for item in requirements}
    unknown = [
        f"{proof.qualified_name} names {proof.requirement_id}"
        for proof in proofs_found
        if proof.requirement_id is not None and proof.requirement_id not in known
    ]
    append_lines(lines, unknown)


def render_product(root: Path, requirements, proofs_found) -> str:
    lines = [
        "# Project report",
        "",
        "Generated by `make project-report`. Hand-editing this file is a defect.",
        "",
        "## Requirements",
        "",
        "The id is a roadmap id, a known-issue id, an ADR id, or a decision id.",
        "The test names that id with `id:` in its header or metadata.",
        "",
    ]
    append_proof_map(lines, requirements, proofs_found)
    lines.append("## Architecture review")
    lines.append("")
    lines.append(
        "Drawn from the ADRs, the roadmap, known issues, and the checks in `plan` and `review`."
    )
    lines.append("")
    lines.append("### ADRs")
    lines.append("")
    append_requirements(lines, requirements, proofs_found, "adr")
    lines.append("### Roadmap")
    lines.append("")
    append_lines(lines, content_lines(root / "docs" / "ROADMAP.md"))
    lines.append("### Known issues")
    lines.append("")
    append_requirements(lines, requirements, proofs_found, "issue")
    lines.append("### Checks")
    lines.append("")
    append_checks(lines, root, ARCHITECTURE_CHECKS)
    lines.append("## Development review")
    lines.append("")
    lines.append(
        "Drawn from the ADRs, the decisions, the roadmap, known issues, "
        "and the checks in `develop`, `review`, `release`, and `project-setup`."
    )
    lines.append("")
    lines.append("### ADRs")
    lines.append("")
    append_requirements(lines, requirements, proofs_found, "adr")
    lines.append("### Decisions")
    lines.append("")
    append_requirements(lines, requirements, proofs_found, "decision")
    lines.append("### Roadmap")
    lines.append("")
    append_lines(lines, content_lines(root / "docs" / "ROADMAP.md"))
    lines.append("### Known issues")
    lines.append("")
    append_requirements(lines, requirements, proofs_found, "issue")
    lines.append("### Checks")
    lines.append("")
    append_checks(lines, root, DEVELOPMENT_CHECKS)
    return "\n".join(lines).rstrip() + "\n"


def render_requirements_list(root: Path, requirements, proofs_found) -> str:
    requirements_module = sibling("requirements")
    lines = [
        "# Project report",
        "",
        "Generated by `make project-report`. Hand-editing this file is a defect.",
        "",
        "## Requirements",
        "",
        "The id is a row in `docs/REQUIREMENTS.md`.",
        "The test names that id with `id:` in its header or metadata.",
        "",
    ]
    for item in requirements:
        lines.append(f"- {item.id}. {item.title}")
    lines.append("")
    append_proof_map(lines, requirements, proofs_found)
    lines.append("## Architecture review")
    lines.append("")
    lines.append(
        "This collection has no ADR directory and no roadmap. "
        "The checks in `plan` and `review` still apply."
    )
    lines.append("")
    lines.append("### Checks")
    lines.append("")
    append_checks(lines, root, ARCHITECTURE_CHECKS)
    lines.append("## Development review")
    lines.append("")
    lines.append(
        "This collection records choices in `docs/DECISIONS.md`. "
        "The checks in `develop`, `review`, `release`, and `project-setup` still apply."
    )
    lines.append("")
    lines.append("### Decisions")
    lines.append("")
    choices = requirements_module.decision_rows(root)
    if not choices:
        lines.append("None.")
        lines.append("")
    else:
        for choice in choices:
            text = choice.choice if choice.choice.endswith(".") else f"{choice.choice}."
            lines.append(f"- {choice.id}, {choice.status}. {text}")
        lines.append("")
    lines.append("### Checks")
    lines.append("")
    append_checks(lines, root, DEVELOPMENT_CHECKS)
    return "\n".join(lines).rstrip() + "\n"


def render(root: Path, requirements, proofs_found) -> str:
    requirements_module = sibling("requirements")
    if requirements_module.uses_requirements_list(root):
        return render_requirements_list(root, requirements, proofs_found)
    return render_product(root, requirements, proofs_found)


def build(root: Path) -> tuple[str, list[str]]:
    requirements_module = sibling("requirements")
    requirements = requirements_module.collect(root)
    proofs_found = requirements_module.proofs(root)
    text = render(root, requirements, proofs_found)
    return text, requirements_module.problems(requirements, proofs_found)


def main() -> int:
    requirements_module = sibling("requirements")
    root = requirements_module.repo_root(Path.cwd())
    text, errors = build(root)
    sys.stdout.write(text)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
