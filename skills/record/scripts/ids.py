#!/usr/bin/env python3
"""Reject a document id that is already used or retired."""

import re
import sys
from pathlib import Path

ID_LINE = re.compile(r"^id:\s*[\"']?([^\"'#\s]+)")
ROW_ID = re.compile(r'^\|\s*(?:<a id="[^"]*"></a>)?\s*([A-Z]+-\d+)\s*\|')
RETIRED_ITEM = re.compile(r"^-\s*[\"']?([^\"'#\s]+)")
TABLE_FILES = ("REQUIREMENTS.md", "DECISIONS.md", "KNOWN_ISSUES.md")
ID_FORM = re.compile(
    r"ADR-\d{4}|H-\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*|[A-Z]-\d+"
)
LIST_KEY = re.compile(r"^(adrs|decisions|issues|proposals|supersedes):(.*)$")
# The key of a frontmatter list that holds the ids of one kind. A requirement
# row takes the place of an ADR where the repository keeps no docs/adr/.
KIND_KEY = {
    "ADR": "adrs",
    "R": "adrs",
    "D": "decisions",
    "K": "issues",
    "P": "proposals",
}


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


def front_lists(lines):
    """Each list key of the frontmatter as (line index, key, text after the colon)."""
    if not lines or lines[0].strip() != "---":
        return []
    found = []
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            break
        match = LIST_KEY.match(lines[index])
        if match:
            found.append((index, match.group(1), match.group(2).strip()))
    return found


def list_items(text):
    """The items of a list written on one line, or None when it is not one."""
    if not (text.startswith("[") and text.endswith("]")):
        return None
    return [item.strip().strip("'\"") for item in text[1:-1].split(",") if item.strip()]


def list_errors(docs, retired):
    """A frontmatter list holds live ids only, written as [a, b], and [] when empty."""
    errors = []
    for path in sorted(docs.rglob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, key, text in front_lists(lines):
            place = f"{path}:{index + 1}"
            items = list_items(text)
            if items is None:
                errors.append(f"{place} {key} is not a list on one line: write []")
                continue
            for item in items:
                if not ID_FORM.fullmatch(item):
                    errors.append(f"{place} {key} holds {item}, which is not an id")
                elif item in retired:
                    errors.append(f"{place} {key} names the retired id {item}")
    return errors


def replace_in_lists(docs, ident, successors):
    """Take ident out of each frontmatter list. Add each successor to the list of its kind."""
    for path in sorted(docs.rglob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
        lists = {
            key: (index, list_items(text) or [])
            for index, key, text in front_lists([line.rstrip("\n") for line in lines])
        }
        if not any(ident in items for _, items in lists.values()):
            continue
        changed = set()
        for key, (index, items) in list(lists.items()):
            if ident in items:
                lists[key] = (index, [item for item in items if item != ident])
                changed.add(key)
        for successor in successors:
            key = KIND_KEY.get(successor.split("-", 1)[0])
            if key in lists and successor not in lists[key][1]:
                lists[key] = (lists[key][0], [*lists[key][1], successor])
                changed.add(key)
        for key in changed:
            index, items = lists[key]
            lines[index] = f"{key}: [{', '.join(items)}]\n"
        path.write_text("".join(lines), encoding="utf-8")


def check(root):
    docs = root / "docs"
    live = live_ids(docs)
    retired = retired_ids(docs / "ids.yaml")
    errors = list_errors(docs, retired)
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


def retire(root, ident, successors=()):
    """Retire an id. Each frontmatter list that named it names the successors."""
    live = live_ids(root / "docs")
    if ident in live:
        return [f"{ident} is still in use: {', '.join(live[ident])}"]
    missing = [item for item in successors if item not in live]
    if missing:
        return [f"{item} is not a live id" for item in missing]
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
    replace_in_lists(root / "docs", ident, successors)
    return []


def main(argv):
    root = repo_root(Path.cwd())
    if len(argv) >= 2 and argv[1] == "retire":
        if len(argv) < 3:
            print("usage: ids.py retire ID [SURVIVING-ID ...]", file=sys.stderr)
            return 2
        errors = retire(root, argv[2], argv[3:])
    else:
        errors = check(root)
    for error in errors:
        print(error, file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
