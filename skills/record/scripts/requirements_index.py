#!/usr/bin/env python3
"""Write docs/requirements-index.toon from the requirements list."""

import re
import sys
from pathlib import Path

COLUMNS = ("id", "title", "status")
ID_CELL = re.compile(r"^[A-Z]+-\d+$")
IN_FORCE = "in force"


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "docs").is_dir():
            return candidate
    return current


def strip_anchor(cell: str) -> str:
    here = str(Path(__file__).resolve().parent)
    if here not in sys.path:
        sys.path.insert(0, here)
    import links

    return links.strip_anchor(cell)


def rows(path: Path) -> list[tuple[str, str, str]]:
    """Each row as id, title, and status.

    A table with a column Status gives the status. A row of a table with no
    such column is in force.
    """
    found = []
    if not path.is_file():
        return found
    status_at = None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [part.strip() for part in stripped.strip("|").split("|")]
        ident = strip_anchor(cells[0]) if cells else ""
        if ident == "Id":
            lowered = [cell.lower() for cell in cells]
            status_at = lowered.index("status") if "status" in lowered else None
            continue
        if len(cells) < 2 or ID_CELL.match(ident) is None:
            continue
        status = cells[status_at] if status_at and status_at < len(cells) else ""
        found.append((ident, cells[1], status or IN_FORCE))
    return found


def cell(value: str) -> str:
    if any(character in value for character in ',"\n'):
        return '"' + value.replace('"', '""') + '"'
    return value


def render(found: list[tuple[str, str, str]]) -> str:
    lines = [f"requirements[{len(found)}]{{{','.join(COLUMNS)}}}:"]
    for row in found:
        lines.append("  " + ",".join(cell(value) for value in row))
    return "\n".join(lines) + "\n"


def write(root: Path) -> Path:
    text = render(rows(root / "docs" / "REQUIREMENTS.md"))
    destination = root / "docs" / "requirements-index.toon"
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(text, encoding="utf-8")
    return destination


def main() -> int:
    write(repo_root(Path.cwd()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
