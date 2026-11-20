#!/usr/bin/env python3
"""Write the decision log. Hand-editing the file is a defect.

The log is the document a person reads. It lists the rules in force,
the choices in force, the open choices, and the rules that were replaced.
"""

import re
import sys
from pathlib import Path

ID_CELL = re.compile(r"^[A-Z]+-\d+$")
SECTIONS = ("Rule", "Why", "Divergence")
LOG = "build/decision-log.md"


def links_module():
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)
    import links

    return links


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "docs").is_dir():
            return candidate
    return current


def blocks(text: str) -> list[tuple[dict, str]]:
    """Split a file into frontmatter blocks, each with the body below it."""
    found = []
    front = None
    body: list[str] = []
    inside = False
    for line in text.splitlines():
        if line.strip() == "---":
            if inside:
                inside = False
                continue
            if front is not None:
                found.append((front, "\n".join(body).strip()))
            front = {}
            body = []
            inside = True
            continue
        if inside and front is not None:
            if ":" in line and not line.startswith((" ", "\t", "-")):
                key, value = line.split(":", 1)
                front[key.strip()] = value.strip().strip("'\"")
            continue
        body.append(line)
    if front is not None:
        found.append((front, "\n".join(body).strip()))
    return found


def listed(value: str) -> list[str]:
    inner = value.strip().strip("[]")
    return [item.strip().strip("'\"") for item in inner.split(",") if item.strip()]


def sections(body: str) -> dict[str, str]:
    found: dict[str, list[str]] = {}
    current = None
    for line in body.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            found[current] = []
            continue
        if current is not None:
            found[current].append(line)
    return {name: "\n".join(lines).strip() for name, lines in found.items()}


def without_title(body: str) -> str:
    lines = [line for line in body.splitlines() if not line.startswith("# ")]
    return "\n".join(lines).strip()


def table_rows(path: Path) -> list[list[str]]:
    if not path.is_file():
        return []
    found = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [part.strip() for part in stripped.strip("|").split("|")]
        if cells:
            cells[0] = links_module().strip_anchor(cells[0])
        if cells and ID_CELL.match(cells[0]):
            found.append(cells)
    return found


def adrs(root: Path) -> list[tuple[dict, str]]:
    directory = root / "docs" / "adr"
    if not directory.is_dir():
        return []
    found = []
    for path in sorted(directory.glob("*.md")):
        for front, body in blocks(path.read_text(encoding="utf-8")):
            if front.get("id"):
                found.append((front, body))
    return found


def decisions(root: Path) -> list[tuple[str, str, str]]:
    """Each decision as id, status, and sentence."""
    path = root / "docs" / "DECISIONS.md"
    found = []
    for cells in table_rows(path):
        if len(cells) >= 3:
            found.append((cells[0], cells[1], cells[2]))
    if path.is_file():
        for front, body in blocks(path.read_text(encoding="utf-8")):
            if not front.get("id"):
                continue
            parts = [front.get("title", ""), without_title(body)]
            sentence = " ".join(" ".join(part.split()) for part in parts if part)
            found.append((front["id"], front.get("status", ""), sentence))
    return found


def is_status(value: str, word: str) -> bool:
    return value.strip().lower() == word


def anchored(ident: str) -> str:
    return f'<a id="{ident.lower()}"></a>{ident}'


def heading(ident: str, title: str) -> str:
    unlink = links_module().unlink
    return f"### {anchored(ident)} {unlink(title)}".rstrip()


def append_adr(lines: list[str], front: dict, body: str, link) -> None:
    lines.append(heading(front["id"], front.get("title", "")))
    lines.append("")
    parts = sections(body)
    if "Rule" not in parts:
        text = without_title(body)
        if text:
            lines.append(link(text))
            lines.append("")
    for name in SECTIONS:
        if parts.get(name):
            lines.append(f"{name}: {link(parts[name])}")
            lines.append("")
    skills = listed(front.get("skills", ""))
    if skills:
        lines.append(f"Skills: {', '.join(skills)}")
        lines.append("")


def append_entries(lines: list[str], entries: list[str]) -> None:
    if not entries:
        lines.append("None.")
    else:
        lines.extend(f"- {entry}" for entry in entries)
    lines.append("")


def linker(root: Path, found: list, choices: list):
    """A function that links the ids in a text. An item of the log links to its anchor."""
    module = links_module()
    scope = dict(module.targets(root))
    local = [
        item[0]["id"]
        for item in found
        if item[0].get("status", "").lower() in ("accepted", "superseded")
    ]
    local += [
        ident
        for ident, status, _text in choices
        if status.lower() in ("decided", "open")
    ]
    if not found:
        local += [
            cells[0]
            for cells in table_rows(root / "docs" / "REQUIREMENTS.md")
            if len(cells) >= 2
        ]
    for ident in local:
        scope[ident] = (LOG, ident.lower())
    return lambda text: module.link_text(text, scope, "build", LOG)


def render(root: Path) -> str:
    found = adrs(root)
    choices = decisions(root)
    link = linker(root, found, choices)
    lines = [
        "# Decision log",
        "",
        "Generated by `make decision-log`. Hand-editing this file is a defect.",
        "",
    ]
    requirements = [
        cells
        for cells in table_rows(root / "docs" / "REQUIREMENTS.md")
        if len(cells) >= 2
    ]
    if requirements and not found:
        lines.append("## Requirements")
        lines.append("")
        for cells in requirements:
            lines.append(heading(cells[0], cells[1] if len(cells) > 2 else ""))
            lines.append("")
            lines.append(link(cells[-1]))
            lines.append("")
    lines.append("## Rules in force")
    lines.append("")
    accepted = [
        item for item in found if is_status(item[0].get("status", ""), "accepted")
    ]
    if not accepted:
        lines.append("None.")
        lines.append("")
    for front, body in accepted:
        append_adr(lines, front, body, link)
    lines.append("## Choices in force")
    lines.append("")
    append_entries(
        lines,
        [
            f"{anchored(ident)}. {link(text)}"
            for ident, status, text in choices
            if is_status(status, "decided")
        ],
    )
    lines.append("## Open choices")
    lines.append("")
    append_entries(
        lines,
        [
            f"{anchored(ident)}. {link(text)}"
            for ident, status, text in choices
            if is_status(status, "open")
        ],
    )
    lines.append("## Replaced rules")
    lines.append("")
    replaced_by = {}
    for front, _body in found:
        for old in listed(front.get("supersedes", "")):
            replaced_by[old] = front["id"]
    replaced = []
    for front, _body in found:
        if not is_status(front.get("status", ""), "superseded"):
            continue
        title = links_module().unlink(front.get("title", ""))
        entry = f"{anchored(front['id'])} {title}".rstrip() + "."
        if front["id"] in replaced_by:
            entry += f" Replaced by {link(replaced_by[front['id']])}."
        replaced.append(entry)
    append_entries(lines, replaced)
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    sys.stdout.write(render(repo_root(Path.cwd())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
