#!/usr/bin/env python3
"""Check docs/98_evolution/evolution-ledger.md: unique IDs, well-formed rows.

append_evolution_ledger.py rejects a duplicate ID only at append time. Two
branches can each append the same ID and the merge brings both in, so CI runs
this check on every push and pull request.

Usage: python3 scripts/check_ledger.py [path-to-ledger]
"""
from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

DEFAULT = Path(__file__).resolve().parent.parent / "docs" / "98_evolution" / "evolution-ledger.md"
ID_PATTERN = re.compile(r"EV-\d{8}-\d{3}")
COLUMNS = 8


def cells(row: str) -> list[str]:
    """Split a markdown table row on unescaped pipes."""
    inner = row.strip()[1:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", inner)]


def main() -> int:
    ledger = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    errors: list[str] = []
    ids: list[str] = []
    for n, line in enumerate(ledger.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("| EV-"):
            continue
        row = cells(line)
        if len(row) != COLUMNS:
            errors.append(f"line {n}: {len(row)} columns, expected {COLUMNS}")
        if not ID_PATTERN.fullmatch(row[0]):
            errors.append(f"line {n}: malformed ID {row[0]!r}")
        ids.append(row[0])
    for dup, count in Counter(ids).items():
        if count > 1:
            errors.append(f"duplicate ID {dup} appears {count} times")
    if errors:
        print("ledger check failed:\n  " + "\n  ".join(errors))
        return 1
    print(f"ok: {len(ids)} ledger rows, IDs unique")
    return 0


if __name__ == "__main__":
    sys.exit(main())
