#!/usr/bin/env python3
"""Write docs/requirements-index.toon from the requirements list."""

import re
import sys
from pathlib import Path

COLUMNS = ("id", "statement")
ID_CELL = re.compile(r"^[A-Z]+-\d+$")


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "docs").is_dir():
            return candidate
    return current


def rows(path: Path) -> list[tuple[str, str]]:
    found = []
    if not path.is_file():
        return found
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [part.strip() for part in stripped.strip("|").split("|")]
        if len(cells) < 2 or ID_CELL.match(cells[0]) is None:
            continue
        found.append((cells[0], cells[1]))
    return found


def cell(value: str) -> str:
    if any(character in value for character in ',"\n'):
        return '"' + value.replace('"', '""') + '"'
    return value


def render(found: list[tuple[str, str]]) -> str:
    lines = [f"requirements[{len(found)}]{{{','.join(COLUMNS)}}}:"]
    for ident, statement in found:
        lines.append("  " + ",".join((cell(ident), cell(statement))))
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
