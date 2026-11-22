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
MERGED_LINE = re.compile(r"^\s+([^\s:]+):\s*(.*)$")


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


def merged_ids(path):
    """The map of ids.yaml as (retired id, surviving ids) pairs, in file order.

    The map is the key `merged:` and one line `  D-5: [R-28]` for each pair.
    """
    if not path.is_file():
        return []
    pairs = []
    in_map = False
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("merged:"):
            in_map = True
            continue
        if not in_map:
            continue
        match = MERGED_LINE.match(line)
        if match:
            items = list_items(match.group(2).strip())
            pairs.append((match.group(1), items if items is not None else []))
        elif line.strip() and not line.strip().startswith("#"):
            in_map = False
    return pairs


def write_ids(path, retired, merged):
    """Write ids.yaml: the retired list, and the map when a merge made one."""
    lines = ["retired:", *[f"- {item}" for item in retired]]
    if not retired:
        lines = ["retired: []"]
    if merged:
        lines.append("merged:")
        lines.extend(f"  {key}: [{', '.join(items)}]" for key, items in merged)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


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


def list_errors(docs, live, retired):
    """A frontmatter list is [a, b], and [] when empty. Each item is a live or a retired id."""
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
                elif item not in live and item not in retired:
                    errors.append(
                        f"{place} {key} names {item}, which is neither live nor retired"
                    )
    return errors


def merged_errors(live, retired, pairs):
    """Each retired id of the map is on the retired list. Each surviving id is live."""
    errors = []
    seen = set()
    for key, items in pairs:
        if key in seen:
            errors.append(f"merged names {key} twice")
        seen.add(key)
        if key not in retired:
            errors.append(f"merged names {key}, which is not on the retired list")
        if not items:
            errors.append(f"merged: {key} has no surviving id")
        for item in items:
            if item not in live:
                errors.append(f"merged: {key} names {item}, which is not a live id")
    return errors


def check(root):
    docs = root / "docs"
    live = live_ids(docs)
    retired = retired_ids(docs / "ids.yaml")
    errors = list_errors(docs, live, retired)
    errors += merged_errors(live, retired, merged_ids(docs / "ids.yaml"))
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


def retire(root, ident, into=()):
    """Retire an id. When a merge retires it, the map names the ids that took its content.

    A document is not rewritten. A map entry that named ident now names the ids of into.
    """
    live = live_ids(root / "docs")
    if ident in live:
        return [f"{ident} is still in use: {', '.join(live[ident])}"]
    missing = [item for item in into if item not in live]
    if missing:
        return [f"{item} is not a live id" for item in missing]
    path = root / "docs" / "ids.yaml"
    retired = retired_ids(path)
    if ident in retired:
        return [f"{ident} is already retired"]
    merged = []
    for key, items in merged_ids(path):
        if ident in items:
            items = [item for item in items if item != ident]
            items += [item for item in into if item not in items]
        if items:
            merged.append((key, items))
    if into:
        merged.append((ident, list(into)))
    write_ids(path, [*retired, ident], merged)
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
