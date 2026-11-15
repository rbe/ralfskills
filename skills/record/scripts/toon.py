#!/usr/bin/env python3
"""Write the ADR index and the installed-skill index."""

import os
import sys
from pathlib import Path


def main():
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import adr_index
    import skill_index

    root = skill_index.repo_root(Path.cwd())
    previous = Path.cwd()
    try:
        os.chdir(root)
        adr_index.main()
    finally:
        os.chdir(previous)
    skill_index.write(root)
    return 0


if __name__ == "__main__":
    sys.exit(main())
