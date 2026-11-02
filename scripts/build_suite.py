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
SKILLS = ["planner", "tasker", "bugfixer", "auditor", "evolver", "explainer"]
DESCRIPTION_LIMIT = 1024
WORKBUDDY_TEXT_LIMITS = {"display_name_en": 60, "description_zh": 500, "description_en": 1000}
MAX_EXAMPLES = 3  # per language, examples_zh / examples_en

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


def examples_count(path: Path) -> dict[str, int]:
    """Count the list items under examples_zh / examples_en in the frontmatter."""
    counts: dict[str, int] = {}
    key = None
    text = path.read_text(encoding="utf-8").split("\n---", 1)[0]
    for line in text.splitlines():
        km = re.match(r"^([A-Za-z][\w-]*):", line)
        if km:
            key = km.group(1)
        elif key and re.match(r"^\s+- ", line):
            counts[key] = counts.get(key, 0) + 1
    return counts


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
    # WorkBuddy refuses a package whose SKILL.md lacks these.
    for field in ("display_name", "display_name_en", "description_zh", "description_en", "examples_zh", "examples_en"):
        if not fm.get(field):
            errors.append(f"suite frontmatter is missing {field}")
    # WorkBuddy limits, from upload errors and published skills' metadata.
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,39}", fm.get("name", "")):
        errors.append("name must match ^[a-z0-9][a-z0-9-]{0,39}$")
    for field, limit in WORKBUDDY_TEXT_LIMITS.items():
        if len(fm.get(field, "")) > limit:
            errors.append(f"{field} is {len(fm[field])} chars, WorkBuddy allows {limit}")
    examples = examples_count(SUITE_SRC / "SKILL.md")
    for field in ("examples_zh", "examples_en"):
        if not 1 <= examples.get(field, 0) <= MAX_EXAMPLES:
            errors.append(f"{field} has {examples.get(field, 0)} items, WorkBuddy allows 1-{MAX_EXAMPLES}")
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


# Platforms such as WorkBuddy accept at most root/second-level/file. Each sub-skill is
# flattened into one folder: references/x.md and scripts/y.py move up beside its
# SKILL.md, and the paths that point at them are rewritten to match.
DROP_DIRS = {"agents"}  # Codex UI metadata, not used by the suite entry
REWRITES: dict[str, list[tuple[str, str]]] = {}


def package_files() -> list[tuple[str, Path]]:
    """(path inside the package, source file), sorted. At most one folder level."""
    entries = [("SKILL.md", SUITE_SRC / "SKILL.md"), ("LICENSE", REPO / "LICENSE")]
    REWRITES.clear()
    for skill in SKILLS:
        root = REPO / skill
        seen: dict[str, Path] = {}
        rewrites: list[tuple[str, str]] = []
        for f in sorted(root.rglob("*")):
            inner = f.relative_to(root)
            if not f.is_file() or any(excluded(part) for part in inner.parts) or inner.parts[0] in DROP_DIRS:
                continue
            if len(inner.parts) > 2:
                raise SystemExit(f"{skill}/{inner.as_posix()}: nested deeper than one folder, cannot flatten")
            # WorkBuddy rejects a zip holding more than one SKILL.md as a multi-skill package,
            # so each sub-skill's entry file ships as <skill>/<skill>.md.
            name = f"{skill}.md" if inner.as_posix() == "SKILL.md" else inner.name
            if name in seen:
                raise SystemExit(f"{skill}: {inner.as_posix()} and {seen[name].as_posix()} collide when flattened")
            seen[name] = inner
            if len(inner.parts) == 2:
                rewrites.append((inner.as_posix(), name))
            entries.append((f"{skill}/{name}", f))
        rewrites.append(("SKILL.md", f"{skill}.md"))  # last, after the references/ rewrites
        REWRITES[skill] = rewrites
    for rel, _ in entries:
        if rel.count("/") > 1:
            raise SystemExit(f"{rel}: deeper than root/second-level/file")
    return sorted(entries)


def read_normalized(src: Path) -> bytes:
    data = src.read_bytes()
    if src.suffix in TEXT_SUFFIXES:
        data = data.replace(b"\r\n", b"\n")
    return data


def content(rel: str, src: Path) -> bytes:
    data = read_normalized(src)
    skill = rel.split("/", 1)[0] if "/" in rel else None
    if skill in REWRITES and src.suffix in TEXT_SUFFIXES:
        text = data.decode("utf-8")
        if rel == f"{skill}/{skill}.md":
            # drop the sub-skill frontmatter so nothing in the package looks like a second skill
            text = re.sub(r"\A---\n.*?\n---\n+", "", text, count=1, flags=re.S)
        for old, new in REWRITES[skill]:
            text = text.replace(old, new)
        data = text.encode("utf-8")
    return data


def validate_package(entries: list[tuple[str, Path]]) -> None:
    """The package must read as exactly one skill: one SKILL.md, at the root, and no other skill frontmatter."""
    errors = []
    skill_files = [rel for rel, _ in entries if rel.rsplit("/", 1)[-1].lower() == "skill.md"]
    if skill_files != ["SKILL.md"]:
        errors.append(f"package must hold exactly one SKILL.md at its root, found {skill_files}")
    for rel, src in entries:
        if src.read_bytes().startswith(b"\xef\xbb\xbf"):
            errors.append(f"{rel} starts with a UTF-8 BOM")
        if rel != "SKILL.md" and rel.endswith(".md"):
            if re.match(r"\A---\n(?:.*\n)*?name:", content(rel, src).decode("utf-8")):
                errors.append(f"{rel} still carries skill frontmatter")
    if errors:
        raise SystemExit("package check failed:\n  " + "\n  ".join(errors))


def make_zip(entries: list[tuple[str, Path]], prefix: str) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for rel, src in entries:
            info = zipfile.ZipInfo(prefix + rel, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, content(rel, src))
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
        dest.write_bytes(content(rel, src))
    flat = DIST / f"{NAME}-{version}-flat.zip"
    flat.write_bytes(make_zip(entries, ""))
    print(f"wrote {flat.relative_to(REPO).as_posix()} and dist/{NAME}/")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="validate only")
    args = ap.parse_args()
    version = validate()
    entries = package_files()
    validate_package(entries)
    if args.check:
        check_fresh(entries)
    else:
        build(version, entries)
    return 0


if __name__ == "__main__":
    sys.exit(main())
