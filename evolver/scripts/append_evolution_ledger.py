#!/usr/bin/env python3
"""Append one validated row to a project's evolution ledger."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


HEADER = (
    "| ID | Trigger/Evidence | Root Cause | Local Fix | Systemic Action | "
    "Guard Verification | Closure Level | Next Planning Input |\n"
    "|---|---|---|---|---|---|---|---|\n"
)
LEVELS = {"Corrected", "Guarded", "Institutionalized", "Fed forward"}


def resolve_project_root(root: Path) -> tuple[Path, bool]:
    """Return the Git top level when available, else the given root as-is."""
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError):
        return root, False
    return Path(result.stdout.strip()).resolve(), True


def cell(value: str) -> str:
    return " ".join(value.splitlines()).replace("|", "\\|").strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--id", required=True)
    parser.add_argument("--trigger", required=True)
    parser.add_argument("--root-cause", required=True)
    parser.add_argument("--local-fix", required=True)
    parser.add_argument("--systemic-action", required=True)
    parser.add_argument("--guard-verification", required=True)
    parser.add_argument("--closure-level", required=True, choices=sorted(LEVELS))
    parser.add_argument("--next-planning-input", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root, in_git = resolve_project_root(args.root.resolve())
    if not root.is_dir():
        raise SystemExit(f"Project root does not exist: {root}")
    ledger = args.ledger or Path("docs/98_evolution/evolution-ledger.md")
    ledger = (root / ledger).resolve() if not ledger.is_absolute() else ledger.resolve()

    if ledger.exists():
        content = ledger.read_text(encoding="utf-8")
        if not content.startswith(HEADER):
            raise SystemExit(f"Existing ledger has an unsupported schema: {ledger}")
    else:
        ledger.parent.mkdir(parents=True, exist_ok=True)
        content = HEADER

    entry_id = cell(args.id)
    if not entry_id:
        raise SystemExit("Ledger ID cannot be empty")
    if any(line.startswith(f"| {entry_id} |") for line in content.splitlines()):
        raise SystemExit(f"Duplicate ledger ID: {entry_id}")

    values = [
        entry_id,
        cell(args.trigger),
        cell(args.root_cause),
        cell(args.local_fix),
        cell(args.systemic_action),
        cell(args.guard_verification),
        cell(args.closure_level),
        cell(args.next_planning_input),
    ]
    row = "| " + " | ".join(values) + " |"
    ledger.write_text(content.rstrip() + "\n" + row + "\n", encoding="utf-8", newline="\n")

    if row not in ledger.read_text(encoding="utf-8"):
        raise SystemExit(f"Ledger read-back failed: {ledger}")

    print(f"ledger={ledger}")
    print(f"git={'yes' if in_git else 'unavailable'}")
    print(f"id={entry_id}")
    print("status=appended-and-verified")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
