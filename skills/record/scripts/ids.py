#!/usr/bin/env python3
"""Reject a document id that is already used or retired."""

import re
import sys
from pathlib import Path

ID_LINE = re.compile(r"^id:\s*[\"']?([^\"'#\s]+)")
ROW_ID = re.compile(r"^\|\s*([A-Z]+-\d+)\s*\|")
RETIRED_ITEM = re.compile(r"^-\s*[\"']?([^\"'#\s]+)")
TABLE_FILES = ("REQUIREMENTS.md", "DECISIONS.md")


def repo_root(start):
    current = Path(start).resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "docs").is_dir():
            return candidate
    return current


def table_ids(docs):
    found = {}
    if not docs.is_dir():
        return found
    for name in TABLE_FILES:
        path = docs / name
        if not path.is_file():
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = ROW_ID.match(line.strip())
            if match:
                found.setdefault(match.group(1), []).append(f"{path}:{number}")
    return found


def live_ids(docs):
    found = table_ids(docs)
    if not docs.is_dir():
        return found
    for path in sorted(docs.rglob("*")):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".md", ".yaml", ".yml"}:
            continue
        if path.name == "ids.yaml":
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            match = ID_LINE.match(line.strip())
            if match:
                found.setdefault(match.group(1), []).append(f"{path}:{number}")
    return found


def retired_ids(path):
    if not path.is_file():
        return []
    retired = []
    in_list = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("retired:"):
            in_list = True
            inline = stripped.split(":", 1)[1].strip()
            if inline == "[]":
                return []
            if inline.startswith("[") and inline.endswith("]"):
                return [
                    item.strip().strip("'\"")
                    for item in inline[1:-1].split(",")
                    if item.strip()
                ]
            continue
        if not in_list:
            continue
        if stripped.startswith("-"):
            match = RETIRED_ITEM.match(stripped)
            if match:
                retired.append(match.group(1))
            continue
        if stripped and not stripped.startswith("#"):
            in_list = False
    return retired


def check(root):
    docs = root / "docs"
    live = live_ids(docs)
    retired = retired_ids(docs / "ids.yaml")
    errors = []
    for ident, places in sorted(live.items()):
        if len(places) > 1:
            errors.append(f"{ident} is used {len(places)} times: {', '.join(places)}")
        if ident in retired:
            errors.append(f"{ident} is retired and still in use")
    retired_seen = {}
    for ident in retired:
        retired_seen.setdefault(ident, 0)
        retired_seen[ident] += 1
    for ident, count in sorted(retired_seen.items()):
        if count > 1:
            errors.append(f"{ident} is on the retired list {count} times")
    return errors


def retire(root, ident):
    live = live_ids(root / "docs")
    if ident in live:
        return [f"{ident} is still in use: {', '.join(live[ident])}"]
    path = root / "docs" / "ids.yaml"
    retired = retired_ids(path) if path.is_file() else []
    if ident in retired:
        return [f"{ident} is already retired"]
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.is_file():
        path.write_text("retired:\n", encoding="utf-8")
    text = path.read_text(encoding="utf-8")
    if "retired:" not in text:
        text = "retired:\n" + text
    if text.rstrip().endswith("retired:") or "retired: []" in text:
        text = text.replace("retired: []", "retired:")
        if not text.endswith("\n"):
            text += "\n"
        text += f"- {ident}\n"
    else:
        if not text.endswith("\n"):
            text += "\n"
        text += f"- {ident}\n"
    path.write_text(text, encoding="utf-8")
    return []


def main(argv):
    root = repo_root(Path.cwd())
    if len(argv) >= 2 and argv[1] == "retire":
        if len(argv) != 3:
            print("usage: ids.py retire ID", file=sys.stderr)
            return 2
        errors = retire(root, argv[2])
    else:
        errors = check(root)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
