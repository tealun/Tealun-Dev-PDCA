#!/usr/bin/env python3
"""Check and build the Claude plugin package tealun-dev-pdca-<version>.plugin.

The repository root is itself the plugin (.claude-plugin/plugin.json lists the
six skill folders). This script packs a copy laid out the standard way:

    .claude-plugin/plugin.json   skills rewritten to ./skills/<name>
    skills/<name>/...            each skill folder, minus release notes and agents/
    assets/<icon>                the icon plugin.json points at
    README.md, LICENSE

Output goes to dist/ only and is never committed. The zip is reproducible:
sorted entries, fixed timestamps, LF line endings.

Usage:
    python3 scripts/build_plugin.py                  check, then build
    python3 scripts/build_plugin.py --check          checks only
      [--tag vX.Y.Z]      the tag must equal v + plugin.json version
      [--since <tag>]     if skill folders changed since <tag>, version must be higher
Decisions: docs/88_planning/plugin-release-20261104.md and the plan it cites.
"""
from __future__ import annotations

import argparse
import importlib.util
import io
import json
import re
import shutil
import tarfile
import subprocess
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PLUGIN_JSON = REPO / ".claude-plugin" / "plugin.json"
DIST = REPO / "dist"
# Package and release name. It carries the brand and differs from the plugin name in
# plugin.json (dev-pdca), which is the short invocation prefix. See
# docs/88_planning/rename-dev-pdca-20261105.md R2 and R4.
NAME = "tealun-dev-pdca"
EXTRA_FILES = ["README.md", "LICENSE"]
DROP_DIRS = {"agents"}  # Codex UI metadata
VERSION_PATTERN = re.compile(r"\d+\.\d+\.\d+")
REFERENCE_PATTERN = re.compile(r"[(`]((?:references|scripts|templates)/[\w./-]+?)[)`]")

# Claude plugin directory rules (docs/claude-directory-rules.md). The directory reads the
# plugin folder, which here is the repository root, so these run over tracked files.
NAME_PATTERN = re.compile(r"[a-z0-9](?:[a-z0-9-]{0,62}[a-z0-9])?")
RESERVED_NAMES = {"claude", "anthropic", "official", "plugin", "mcp", "test"}
RESERVED_PREFIXES = ("claude-", "anthropic-", "anthropics-", "cc-plugin-")
README_MIN_WORDS = 40
# The packaged README is the listing text; the directory flags clone-and-run or
# pipe-to-shell install steps in it as an install-time risk (docs/claude-directory-rules.md).
DOWNLOAD_AND_RUN = re.compile(
    r"git clone|curl\s|wget\s|\birm\b|\biwr\b|Invoke-WebRequest|Invoke-Expression|\biex\b"
    r"|\|\s*(ba|z)?sh\b|\bbash\s+\S+\.sh|\.ps1\b|\bnpx\s|\buvx\s|\bpipx\s", re.I)
MAX_FILE_BYTES = 5 * 1024 * 1024          # stops validation
MAX_TEXT_FILE_BYTES = 256 * 1024          # held for a reviewer (images and fonts exempt)
MAX_FILES = 512                           # held for a reviewer
MEDIA_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".woff", ".woff2", ".ttf", ".otf"}
HELD_SUFFIXES = {".zip", ".ico", ".pdf", ".exe", ".dll", ".so", ".dylib", ".jar", ".tar", ".gz", ".7z"}
JUNK_NAMES = {".DS_Store", "Thumbs.db", "desktop.ini", "__MACOSX"}


def _load_build_suite():
    spec = importlib.util.spec_from_file_location("build_suite", REPO / "scripts" / "build_suite.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


_suite = _load_build_suite()
FIXED_TIME = _suite.FIXED_TIME
excluded = _suite.excluded            # same exclusions as dev-pdca.zip
read_normalized = _suite.read_normalized


def version_tuple(version: str) -> tuple[int, ...]:
    return tuple(int(p) for p in version.split("."))


def skill_dirs(manifest: dict) -> list[str]:
    """Skill folder names from plugin.json, e.g. './planner' -> 'planner'."""
    return [s.strip("./").rstrip("/") for s in manifest.get("skills", [])]


def check(repo: Path = REPO, tag: str | None = None, since: str | None = None) -> list[str]:
    errors: list[str] = []
    plugin_json = repo / ".claude-plugin" / "plugin.json"
    try:
        manifest = json.loads(plugin_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"plugin.json is not readable JSON: {exc}"]

    # 1. required fields and version format
    for field in ("name", "version"):
        if not manifest.get(field):
            errors.append(f"plugin.json is missing {field}")
    version = manifest.get("version", "")
    if version and not VERSION_PATTERN.fullmatch(version):
        errors.append(f"plugin.json version {version!r} is not x.y.z")

    # 2. plugin.json lists exactly the top-level skill folders (the marketplace
    #    list lives in tealun/tealun-plugins, so this is the guard against a new
    #    skill folder that never made it into the manifest)
    skills = skill_dirs(manifest)
    on_disk = sorted(p.parent.name for p in repo.glob("*/SKILL.md"))
    if sorted(skills) != on_disk:
        errors.append(f"skills differ: plugin.json {sorted(skills)} vs skill folders {on_disk}")

    # 3 and 4. each SKILL.md exists, name matches folder, referenced files exist
    for skill in skills:
        skill_md = repo / skill / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"{skill}/SKILL.md is missing")
            continue
        text = skill_md.read_text(encoding="utf-8")
        m = re.search(r"^name:\s*['\"]?([\w-]+)", text, re.M)
        if not m or m.group(1) != skill:
            errors.append(f"{skill}/SKILL.md: frontmatter name does not match folder")
        for ref in sorted(set(REFERENCE_PATTERN.findall(text))):
            if not (repo / skill / ref).is_file():
                errors.append(f"{skill}/SKILL.md references missing file {ref}")

    icon = manifest.get("icon")
    if icon and not (repo / icon).is_file():
        errors.append(f"plugin.json icon {icon} does not exist")

    # directory rules that block a submission
    name = manifest.get("name", "")
    if name and (not NAME_PATTERN.fullmatch(name) or name in RESERVED_NAMES or name.startswith(RESERVED_PREFIXES)):
        errors.append(f"plugin name {name!r} breaks the directory naming rules")
    readme = repo / "README.md"
    words = len(re.sub(r"```.*?```", "", readme.read_text(encoding="utf-8"), flags=re.S).split()) if readme.is_file() else 0
    if words < README_MIN_WORDS:
        errors.append(f"README.md has {words} words outside code blocks; the directory needs {README_MIN_WORDS}")
    if readme.is_file():
        for n, line in enumerate(readme.read_text(encoding="utf-8").splitlines(), 1):
            if DOWNLOAD_AND_RUN.search(line):
                errors.append(f"README.md line {n}: download-and-run install step; the directory shows it "
                              f"to users as an install-time risk")
    if not (repo / "LICENSE").is_file() and not manifest.get("license"):
        errors.append("no LICENSE file and no license in plugin.json")
    for missing in ("description", "author", "version"):
        if not manifest.get(missing):
            errors.append(f"plugin.json should set {missing}")
    errors += content_rewriting_attributes(repo)
    errors += export_mismatches(repo)
    for f in tracked_files(repo):
        if f.is_symlink():
            errors.append(f"{f.relative_to(repo)} is a symlink; the directory refuses symlinks")
        elif f.stat().st_size > MAX_FILE_BYTES:
            errors.append(f"{f.relative_to(repo)} is over 5 MiB")

    # 5. tag matches version, and CHANGELOG has this version's release notes
    if tag is not None:
        if tag != f"v{version}":
            errors.append(f"tag {tag} does not match plugin.json version {version} (expected v{version})")
        if not release_notes(version, repo):
            errors.append(f"CHANGELOG.md has no '## {NAME} {version}' section for the release notes")

    # 6. skills changed since the previous tag -> version must be higher
    if since:
        diff = subprocess.run(["git", "-C", str(repo), "diff", "--quiet", since, "--", *skills],
                              capture_output=True, text=True)
        if diff.returncode not in (0, 1):
            errors.append(f"git diff against {since} failed: {diff.stderr.strip()}")
        elif diff.returncode == 1:
            previous = since.lstrip("v")
            if not VERSION_PATTERN.fullmatch(previous):
                errors.append(f"--since {since} is not a v<x.y.z> tag")
            elif VERSION_PATTERN.fullmatch(version) and version_tuple(version) <= version_tuple(previous):
                errors.append(f"skill folders changed since {since} but plugin.json version {version} "
                              f"is not higher; bump it (see the bump rule in AGENTS.md)")
    return errors


def release_notes(version: str, repo: Path = REPO) -> str:
    """The body of the CHANGELOG section headed '## tealun-dev-pdca <version>'."""
    path = repo / "CHANGELOG.md"
    if not path.is_file():
        return ""
    m = re.search(rf"^## {re.escape(NAME)} {re.escape(version)}\b.*?\n(.*?)(?=^## |\Z)",
                  path.read_text(encoding="utf-8"), re.M | re.S)
    return m.group(1).strip() if m else ""


# .gitattributes settings that make checked-out or exported bytes differ from the stored
# ones on some platform. "-text" and "binary" switch conversion off and are allowed.
REWRITING_ATTRIBUTES = ("text", "eol", "filter", "export-ignore", "export-subst", "ident",
                        "working-tree-encoding", "crlf")


def content_rewriting_attributes(repo: Path) -> list[str]:
    errors = []
    for path in sorted(repo.rglob(".gitattributes")):
        if ".git" in path.relative_to(repo).parts[:-1]:
            continue
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            fields = line.split("#", 1)[0].split()
            for attr in fields[1:]:
                name = attr.split("=", 1)[0]
                if name.startswith(("-", "!")) or name == "binary":
                    continue
                if name in REWRITING_ATTRIBUTES:
                    errors.append(f"{path.relative_to(repo)} line {n}: '{attr}' rewrites content on some "
                                  f"platform; the plugin directory cannot validate the repository")
    return errors


def export_mismatches(repo: Path) -> list[str]:
    """The directory validates the repository as exported; it refuses a repository whose
    export differs from what is stored (a .gitattributes eol, filter, export-ignore or
    export-subst rule). Export the index with git archive and compare every file."""
    run = lambda *a: subprocess.run(["git", "-C", str(repo), *a], capture_output=True)
    tree = run("write-tree")
    if tree.returncode != 0:
        return []  # not a Git work tree: nothing is exported
    archive = run("archive", tree.stdout.decode().strip())
    if archive.returncode != 0:
        return [f"git archive failed: {archive.stderr.decode().strip()}"]
    exported = {}
    with tarfile.open(fileobj=io.BytesIO(archive.stdout)) as tf:
        for member in tf.getmembers():
            if member.isfile():
                exported[member.name] = tf.extractfile(member).read()
    errors = []
    listing = run("ls-files", "-z", "--cached").stdout.decode().split("\0")
    for path in filter(None, listing):
        stored = run("cat-file", "blob", f":{path}").stdout
        if path not in exported:
            errors.append(f"{path} is missing from the git export (export-ignore?); the directory cannot validate the repository")
        elif exported[path] != stored:
            errors.append(f"{path} changes on git export (.gitattributes eol/filter rule); the directory cannot validate the repository")
    return errors


def tracked_files(repo: Path) -> list[Path]:
    out = subprocess.run(["git", "-C", str(repo), "ls-files", "-z"], capture_output=True, text=True)
    if out.returncode != 0:
        return [f for f in repo.rglob("*") if f.is_file() and ".git" not in f.parts]
    # a tracked file deleted from the work tree is still listed; skip it so the
    # reference check reports it instead of crashing on stat()
    return [repo / p for p in out.stdout.split("\0") if p and ((repo / p).is_symlink() or (repo / p).exists())]


def directory_warnings(repo: Path = REPO) -> list[str]:
    """Rules that hold a submission for a reviewer rather than block it."""
    warnings: list[str] = []
    files = tracked_files(repo)
    if len(files) > MAX_FILES:
        warnings.append(f"{len(files)} files in the plugin folder; over {MAX_FILES} is held for review")
    for f in files:
        rel = f.relative_to(repo)
        if f.name in JUNK_NAMES:
            warnings.append(f"{rel}: remove OS junk files")
        elif f.suffix.lower() in HELD_SUFFIXES:
            warnings.append(f"{rel}: {f.suffix} files are held for a reviewer")
        elif f.suffix.lower() not in MEDIA_SUFFIXES and f.is_file() and f.stat().st_size > MAX_TEXT_FILE_BYTES:
            warnings.append(f"{rel}: over 256 KiB is held for a reviewer")
    return warnings


def package_entries(repo: Path = REPO) -> tuple[dict, list[tuple[str, Path]]]:
    """(packaged manifest, [(path inside the package, source file)]) sorted."""
    manifest = json.loads((repo / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
    entries: list[tuple[str, Path]] = []
    for skill in skill_dirs(manifest):
        root = repo / skill
        for f in sorted(root.rglob("*")):
            inner = f.relative_to(root)
            if not f.is_file() or inner.parts[0] in DROP_DIRS or any(excluded(p) for p in inner.parts):
                continue
            entries.append((f"skills/{skill}/{inner.as_posix()}", f))
    for name in EXTRA_FILES:
        entries.append((name, repo / name))
    if manifest.get("icon"):
        icon = manifest["icon"].lstrip("./")
        entries.append((icon, repo / icon))
    packaged = dict(manifest)
    packaged["skills"] = [f"./skills/{s}" for s in skill_dirs(manifest)]
    return packaged, sorted(entries)


def make_plugin(repo: Path = REPO) -> tuple[str, bytes]:
    packaged, entries = package_entries(repo)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        files = [(".claude-plugin/plugin.json", (json.dumps(packaged, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))]
        files += [(rel, read_normalized(src)) for rel, src in entries]
        for rel, data in sorted(files):
            info = zipfile.ZipInfo(rel, FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, data)
    return packaged["version"], buf.getvalue()


def build(repo: Path = REPO, dist: Path = DIST) -> Path:
    version, data = make_plugin(repo)
    out_dir = dist / NAME
    if out_dir.exists():
        shutil.rmtree(out_dir)
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        zf.extractall(out_dir)
    target = dist / f"{NAME}-{version}.plugin"
    target.write_bytes(data)
    # claude.ai documents uploading a plugin as a zip (Customize > Plugins > Add > Upload
    # plugin); the same bytes are written under both names. See docs/claude-directory-rules.md.
    (dist / f"{NAME}-{version}.zip").write_bytes(data)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--check", action="store_true", help="run checks only, build nothing")
    parser.add_argument("--tag", help="release tag that must equal v<version>")
    parser.add_argument("--since", help="previous release tag; skill changes since it require a higher version")
    parser.add_argument("--notes", metavar="FILE", help="write this version's CHANGELOG section to FILE and exit")
    args = parser.parse_args()
    if args.notes:
        version = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))["version"]
        notes = release_notes(version)
        if not notes:
            print(f"CHANGELOG.md has no '## {NAME} {version}' section")
            return 1
        Path(args.notes).write_text(notes + "\n", encoding="utf-8")
        return 0
    errors = check(tag=args.tag, since=args.since)
    if errors:
        print("plugin check failed:\n  " + "\n  ".join(errors))
        return 1
    version = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))["version"]
    print(f"ok: {NAME} {version}, plugin.json matches the skill folders, skill references resolve")
    for warning in directory_warnings():
        print(f"warning (directory review): {warning}")
    if args.check:
        return 0
    target = build()
    print(f"wrote {target.relative_to(REPO)}, the same bytes as {target.with_suffix('.zip').name}, and dist/{NAME}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
