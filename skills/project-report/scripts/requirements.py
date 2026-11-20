#!/usr/bin/env python3
"""Requirement ids from the board, and the id a test names."""

import ast
import re
from dataclasses import dataclass
from pathlib import Path

ID_LINE = re.compile(r"^id:\s*[\"']?([^\"'#\s]+)")
ID_CELL = re.compile(r"^[A-Z]+-\d+$")
ROADMAP_ID = re.compile(
    r"(?<![A-Za-z0-9-])(?:ADR-\d+|D-\d+|P-\d+|H-[A-Za-z0-9-]+)(?![A-Za-z0-9-])"
)
SKIP = {
    ".git",
    ".claude",
    ".gradle",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "node_modules",
}
OTHER_TEST_FILE = re.compile(
    r"(?:\.(?:test|spec)\.(?:js|jsx|ts|tsx|mjs|cjs)"
    r"|(?:Test|Tests|Spec|IT)\.(?:java|groovy|kt))$"
)
COMMENT_ID = re.compile(r"^(?://+|/\*+|\*|#)\s*id:\s*[\"']?([^\"'#\s*]+)")


@dataclass(frozen=True)
class Requirement:
    id: str
    kind: str
    title: str
    status: str


@dataclass(frozen=True)
class DecisionRow:
    id: str
    status: str
    choice: str


@dataclass(frozen=True)
class TestProof:
    requirement_id: str | None
    qualified_name: str
    path: str


def adr_markdown(root: Path) -> list[Path]:
    adr_dir = root / "docs" / "adr"
    if not adr_dir.is_dir():
        return []
    return sorted(path for path in adr_dir.glob("*.md") if path.is_file())


def uses_requirements_list(root: Path) -> bool:
    listed = root / "docs" / "REQUIREMENTS.md"
    return listed.is_file() and not adr_markdown(root)


def table_rows(path: Path) -> list[list[str]]:
    if not path.is_file():
        return []
    found = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [part.strip() for part in stripped.strip("|").split("|")]
        if not cells or ID_CELL.match(cells[0]) is None:
            continue
        found.append(cells)
    return found


def decision_rows(root: Path) -> list[DecisionRow]:
    found = []
    for cells in table_rows(root / "docs" / "DECISIONS.md"):
        if len(cells) < 3:
            continue
        found.append(DecisionRow(cells[0], cells[1], cells[2]))
    return found


def collect_requirements_list(root: Path) -> list[Requirement]:
    found = []
    for cells in table_rows(root / "docs" / "REQUIREMENTS.md"):
        if len(cells) < 2:
            continue
        found.append(Requirement(cells[0], "requirement", cells[1], ""))
    return found


def repo_root(start: Path) -> Path:
    current = start.resolve()
    for candidate in [current, *current.parents]:
        if (candidate / "Makefile").is_file() and (
            (candidate / "skills").is_dir()
            or (candidate / ".claude" / "skills").is_dir()
        ):
            return candidate
    return current


def requirement_id(docstring: str | None) -> str | None:
    if not docstring:
        return None
    for line in docstring.splitlines():
        match = ID_LINE.match(line.strip())
        if match:
            return match.group(1)
    return None


def split_blocks(text: str) -> list[tuple[str, str]]:
    parts = text.split("---")
    if len(parts) < 3:
        return []
    blocks = []
    rest = parts[1:]
    index = 0
    while index < len(rest):
        front = rest[index]
        body = rest[index + 1] if index + 1 < len(rest) else ""
        blocks.append((front, body))
        index += 2
    return blocks


def scalars(front: str) -> dict[str, str]:
    data = {}
    for line in front.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or line[:1] in (" ", "\t", "-"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("'\"")
    return data


def first_sentence(body: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        return stripped.lstrip("-").strip()
    return ""


def requirements_in_markdown(path: Path, kind: str) -> list[Requirement]:
    text = path.read_text(encoding="utf-8")
    found = []
    seen = set()
    for front, body in split_blocks(text):
        data = scalars(front)
        ident = data.get("id", "")
        if not ident or ident in seen:
            continue
        seen.add(ident)
        title = data.get("title") or first_sentence(body) or ident
        found.append(Requirement(ident, kind, title, data.get("status", "")))
    for line in text.splitlines():
        match = ID_LINE.match(line.strip())
        if match and match.group(1) not in seen:
            seen.add(match.group(1))
            found.append(Requirement(match.group(1), kind, match.group(1), ""))
    return found


def roadmap_requirements(path: Path, existing: set[str]) -> list[Requirement]:
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    found = []
    seen = set(existing)
    for line in text.splitlines():
        title = line.strip().lstrip("-").strip()
        for ident in ROADMAP_ID.findall(line):
            if ident in seen:
                continue
            seen.add(ident)
            found.append(Requirement(ident, "roadmap", title or ident, "in progress"))
        match = ID_LINE.match(line.strip())
        if match and match.group(1) not in seen:
            seen.add(match.group(1))
            found.append(
                Requirement(
                    match.group(1), "roadmap", title or match.group(1), "in progress"
                )
            )
    return found


def collect_board(root: Path) -> list[Requirement]:
    docs = root / "docs"
    found = []
    adr_dir = docs / "adr"
    if adr_dir.is_dir():
        for path in sorted(adr_dir.glob("*.md")):
            found.extend(requirements_in_markdown(path, "adr"))
    for name, kind in (("DECISIONS.md", "decision"), ("KNOWN_ISSUES.md", "issue")):
        path = docs / name
        if path.is_file():
            found.extend(requirements_in_markdown(path, kind))
    found.extend(roadmap_requirements(docs / "ROADMAP.md", {item.id for item in found}))
    unique = []
    seen = set()
    for item in found:
        if item.id in seen:
            continue
        seen.add(item.id)
        unique.append(item)
    return sorted(unique, key=lambda item: item.id)


def collect(root: Path) -> list[Requirement]:
    if uses_requirements_list(root):
        return collect_requirements_list(root)
    return collect_board(root)


def parents_of(tree: ast.AST) -> dict[ast.AST, ast.AST]:
    found = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            found[child] = parent
    return found


def is_test(node: ast.AST, parents: dict[ast.AST, ast.AST]) -> bool:
    if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
        return False
    if not node.name.startswith("test"):
        return False
    parent = parents.get(node)
    if isinstance(parent, ast.Module):
        return True
    return isinstance(parent, ast.ClassDef) and isinstance(
        parents.get(parent), ast.Module
    )


def proofs_in(path: Path, root: Path) -> list[TestProof]:
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=str(path))
    relative = path.relative_to(root).as_posix()
    module = (
        relative[: -len(".py")].replace("/", ".")
        if relative.endswith(".py")
        else relative
    )
    found = []
    parents = parents_of(tree)
    for node in ast.walk(tree):
        if not is_test(node, parents):
            continue
        parent = parents.get(node)
        if isinstance(parent, ast.ClassDef):
            qualified = f"{module}.{parent.name}.{node.name}"
        else:
            qualified = f"{module}.{node.name}"
        docstring = ast.get_docstring(node, clean=True)
        found.append(TestProof(requirement_id(docstring), qualified, relative))
    return found


def test_files(root: Path) -> list[Path]:
    found = []
    for path in sorted(root.rglob("*.py")):
        if any(part in SKIP for part in path.parts):
            continue
        if path.name.startswith("test_") or path.name.endswith("_test.py"):
            found.append(path)
    return found


def other_test_files(root: Path) -> list[Path]:
    found = []
    for path in sorted(root.rglob("*")):
        if any(part in SKIP for part in path.parts):
            continue
        if path.is_file() and OTHER_TEST_FILE.search(path.name):
            found.append(path)
    return found


def proofs_in_comments(path: Path, root: Path) -> list[TestProof]:
    relative = path.relative_to(root).as_posix()
    found = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = COMMENT_ID.match(line.strip())
        if match:
            found.append(TestProof(match.group(1), relative, relative))
    if not found:
        found.append(TestProof(None, relative, relative))
    return found


def proofs(root: Path) -> list[TestProof]:
    found = []
    for path in test_files(root):
        found.extend(proofs_in(path, root))
    for path in other_test_files(root):
        found.extend(proofs_in_comments(path, root))
    return found


def problems(
    requirements: list[Requirement], proofs_found: list[TestProof]
) -> list[str]:
    known = {item.id for item in requirements}
    errors = []
    for proof in proofs_found:
        if proof.requirement_id is None:
            errors.append(f"{proof.qualified_name} has no id")
        elif proof.requirement_id not in known:
            errors.append(
                f"{proof.qualified_name} names {proof.requirement_id}, which is not a requirement"
            )
    return errors
