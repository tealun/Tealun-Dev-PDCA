#!/usr/bin/env python3
"""Build the dev-pdca suite package: one skill folder that bundles all five skills.

Usage:
    python3 scripts/build_suite.py            # build into dist/
    python3 scripts/build_suite.py --check    # validate only, write nothing

Output:
    dist/dev-pdca/                 unpacked package (inspect before uploading)
    dist/dev-pdca-<version>.zip    the folder dev-pdca/ inside the zip
    dist/dev-pdca-<version>-flat.zip  SKILL.md at the zip root

Platforms differ on which zip layout they accept; try the first, fall back to -flat.
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SUITE_SRC = REPO / "suite" / "dev-pdca"
DIST = REPO / "dist"
NAME = "dev-pdca"
SKILLS = ["planner", "tasker", "bugfixer", "auditor", "evolver"]
DESCRIPTION_LIMIT = 1024

# Files that serve repository maintenance, not the agent at run time.
EXCLUDE_PATTERNS = [re.compile(p) for p in (r"^RELEASE_.*\.md$", r"^INTRO\.md$", r"^__pycache__$", r"\.pyc$", r"^\.DS_Store$")]


def frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        raise SystemExit(f"{path}: missing YAML frontmatter")
    fields: dict[str, str] = {}
    key = None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if km:
            key, value = km.group(1), km.group(2).strip()
            fields[key] = value
        elif key and line.startswith("  "):
            fields[key] = (fields[key] + " " + line.strip()).strip()
    for k, v in fields.items():
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            fields[k] = v[1:-1]
        elif v.startswith(">"):
            fields[k] = v[1:].strip()
    return fields


def validate() -> str:
    errors: list[str] = []
    fm = frontmatter(SUITE_SRC / "SKILL.md")
    if fm.get("name") != NAME:
        errors.append(f"suite name must be {NAME!r}, got {fm.get('name')!r}")
    desc = fm.get("description", "")
    if not desc:
        errors.append("suite description is empty")
    elif len(desc) > DESCRIPTION_LIMIT:
        errors.append(f"suite description is {len(desc)} chars, limit {DESCRIPTION_LIMIT}")
    version = fm.get("version", "")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        errors.append(f"suite version must be MAJOR.MINOR.PATCH, got {version!r}")
    body = (SUITE_SRC / "SKILL.md").read_text(encoding="utf-8")
    for skill in SKILLS:
        sk = REPO / skill / "SKILL.md"
        if not sk.is_file():
            errors.append(f"missing {skill}/SKILL.md")
            continue
        if frontmatter(sk).get("name") != skill:
            errors.append(f"{skill}/SKILL.md: name does not match folder")
        if f"`{skill}`" not in body:
            errors.append(f"suite SKILL.md does not route to {skill}")
    if errors:
        raise SystemExit("validation failed:\n  " + "\n  ".join(errors))
    print(f"ok: {NAME} {version}, description {len(desc)}/{DESCRIPTION_LIMIT} chars, {len(SKILLS)} sub-skills")
    return version


def excluded(name: str) -> bool:
    return any(p.search(name) for p in EXCLUDE_PATTERNS)


def build(version: str) -> None:
    out = DIST / NAME
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    shutil.copy2(SUITE_SRC / "SKILL.md", out / "SKILL.md")
    shutil.copy2(REPO / "LICENSE", out / "LICENSE")
    for skill in SKILLS:
        shutil.copytree(REPO / skill, out / skill, ignore=lambda _d, names: [n for n in names if excluded(n)])

    files = sorted(p for p in out.rglob("*") if p.is_file())
    for flat, zip_name in ((False, f"{NAME}-{version}.zip"), (True, f"{NAME}-{version}-flat.zip")):
        target = DIST / zip_name
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
            for f in files:
                rel = f.relative_to(out).as_posix()
                zf.write(f, rel if flat else f"{NAME}/{rel}")
        print(f"wrote {target.relative_to(REPO)} ({target.stat().st_size // 1024} KB, {len(files)} files)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="validate only")
    args = ap.parse_args()
    version = validate()
    if not args.check:
        build(version)
    return 0


if __name__ == "__main__":
    sys.exit(main())
