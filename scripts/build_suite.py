#!/usr/bin/env python3
"""Build the dev-pdca suite package: one skill folder that bundles all five skills.

Usage:
    python3 scripts/build_suite.py            # rebuild dev-pdca.zip and dist/
    python3 scripts/build_suite.py --check    # validate, and fail if dev-pdca.zip is stale

Output:
    dev-pdca.zip                   committed at the repository root; folder dev-pdca/ inside
    dist/dev-pdca/                 unpacked package (inspect before uploading)
    dist/dev-pdca-<version>-flat.zip  SKILL.md at the zip root, for platforms that need it

The build is deterministic (sorted entries, fixed timestamps, LF line endings), so
--check can compare the committed zip byte for byte with a fresh build.
"""
from __future__ import annotations

import argparse
import io
import re
import shutil
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SUITE_SRC = REPO / "suite" / "dev-pdca"
DIST = REPO / "dist"
ROOT_ZIP = REPO / "dev-pdca.zip"
TEXT_SUFFIXES = {".md", ".py", ".yaml", ".yml", ".json", ".txt", ""}
FIXED_TIME = (2020, 1, 1, 0, 0, 0)
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


def package_files() -> list[tuple[str, Path]]:
    """(path inside the package, source file), sorted."""
    entries = [("SKILL.md", SUITE_SRC / "SKILL.md"), ("LICENSE", REPO / "LICENSE")]
    for skill in SKILLS:
        for f in (REPO / skill).rglob("*"):
            rel = f.relative_to(REPO)
            if f.is_file() and not any(excluded(part) for part in rel.parts):
                entries.append((rel.as_posix(), f))
    return sorted(entries)


def read_normalized(src: Path) -> bytes:
    data = src.read_bytes()
    if src.suffix in TEXT_SUFFIXES:
        data = data.replace(b"\r\n", b"\n")
    return data


def make_zip(entries: list[tuple[str, Path]], prefix: str) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel, src in entries:
            info = zipfile.ZipInfo(prefix + rel, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, read_normalized(src))
    return buf.getvalue()


def check_fresh(entries: list[tuple[str, Path]]) -> None:
    if not ROOT_ZIP.is_file():
        raise SystemExit("dev-pdca.zip is missing: run python3 scripts/build_suite.py and commit it")
    if ROOT_ZIP.read_bytes() != make_zip(entries, f"{NAME}/"):
        raise SystemExit("dev-pdca.zip is stale: run python3 scripts/build_suite.py and commit it")
    print("ok: dev-pdca.zip matches the sources")


def build(version: str, entries: list[tuple[str, Path]]) -> None:
    ROOT_ZIP.write_bytes(make_zip(entries, f"{NAME}/"))
    print(f"wrote dev-pdca.zip ({ROOT_ZIP.stat().st_size // 1024} KB, {len(entries)} files, version {version})")

    out = DIST / NAME
    if out.exists():
        shutil.rmtree(out)
    for rel, src in entries:
        dest = out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(read_normalized(src))
    flat = DIST / f"{NAME}-{version}-flat.zip"
    flat.write_bytes(make_zip(entries, ""))
    print(f"wrote {flat.relative_to(REPO).as_posix()} and dist/{NAME}/")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="validate only")
    args = ap.parse_args()
    version = validate()
    entries = package_files()
    if args.check:
        check_fresh(entries)
    else:
        build(version, entries)
    return 0


if __name__ == "__main__":
    sys.exit(main())
