"""Unit tests for the repository scripts. Run: python3 -m unittest discover -s tests"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


check_ledger = load("check_ledger", REPO / "scripts" / "check_ledger.py")
build_suite = load("build_suite", REPO / "scripts" / "build_suite.py")
build_plugin = load("build_plugin", REPO / "scripts" / "build_plugin.py")
APPEND = REPO / "evolver" / "scripts" / "append_evolution_ledger.py"

LEDGER_HEADER = (
    "| ID | Trigger/Evidence | Root Cause | Local Fix | Systemic Action | "
    "Guard Verification | Closure Level | Next Planning Input |\n"
    "|---|---|---|---|---|---|---|---|\n"
)
COMPLIANCE_HEADER = "| 日期 | 周期 / 提交 | Gate | 适用 | 遵守 | 证据 | 记录方式 |\n|---|---|---|---|---|---|---|\n"


def append(root: Path, entry_id: str, trigger: str = "t") -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(APPEND), "--root", str(root), "--id", entry_id, "--trigger", trigger,
         "--root-cause", "r", "--local-fix", "l", "--systemic-action", "s",
         "--guard-verification", "g", "--closure-level", "Corrected", "--next-planning-input", "n"],
        capture_output=True, text=True,
    )


class AppendLedgerTest(unittest.TestCase):
    def test_outside_git_falls_back_to_root(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = append(Path(tmp), "EV-20260101-001")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("git=unavailable", result.stdout)
            ledger = Path(tmp) / "docs" / "98_evolution" / "evolution-ledger.md"
            self.assertTrue(ledger.read_text(encoding="utf-8").startswith(LEDGER_HEADER))

    def test_duplicate_id_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(append(Path(tmp), "EV-20260101-001").returncode, 0)
            second = append(Path(tmp), "EV-20260101-001")
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("Duplicate ledger ID", second.stderr)

    def test_pipe_and_newline_escaped(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(append(Path(tmp), "EV-20260101-001", trigger="a|b\nc").returncode, 0)
            text = (Path(tmp) / "docs" / "98_evolution" / "evolution-ledger.md").read_text(encoding="utf-8")
            self.assertIn("| a\\|b c |", text)
            errors, rows = check_ledger.check_ledger(Path(tmp) / "docs" / "98_evolution" / "evolution-ledger.md")
            self.assertEqual((errors, rows), ([], 1))

    def test_missing_root_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = append(Path(tmp) / "absent", "EV-20260101-001")
            self.assertNotEqual(result.returncode, 0)

    def test_foreign_schema_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            ledger = Path(tmp) / "docs" / "98_evolution" / "evolution-ledger.md"
            ledger.parent.mkdir(parents=True)
            ledger.write_text("| other | table |\n", encoding="utf-8")
            result = append(Path(tmp), "EV-20260101-001")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unsupported schema", result.stderr)


class CheckLedgerTest(unittest.TestCase):
    def write(self, text: str) -> Path:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".md", delete=False, encoding="utf-8")
        tmp.write(text)
        tmp.close()
        self.addCleanup(Path(tmp.name).unlink)
        return Path(tmp.name)

    def test_duplicate_and_malformed_ids(self):
        row = "| EV-20260101-001 | a | b | c | d | e | Corrected | f |\n"
        path = self.write(LEDGER_HEADER + row + row + "| EV-2026-1 | a | b | c | d | e | Corrected | f |\n")
        errors, rows = check_ledger.check_ledger(path)
        self.assertEqual(rows, 3)
        self.assertTrue(any("duplicate ID" in e for e in errors))
        self.assertTrue(any("malformed ID" in e for e in errors))

    def test_wrong_column_count(self):
        path = self.write(LEDGER_HEADER + "| EV-20260101-001 | a | b |\n")
        errors, _ = check_ledger.check_ledger(path)
        self.assertTrue(any("columns" in e for e in errors))

    def test_compliance_valid_rows(self):
        path = self.write(COMPLIANCE_HEADER
                          + "| 2026-11-04 | cycle | G1 | 是 | 部分 | evidence | 自评 |\n"
                          + "| 2026-11-04 | cycle | G4 | 不适用 | — | no failure | 独立 |\n")
        self.assertEqual(check_ledger.check_compliance(path), ([], 2))

    def test_compliance_rejects_bad_values(self):
        cases = {
            "| 2026-11-04 | c | G6 | 是 | 是 | e | 自评 |": "gate",
            "| 2026-11-04 | c | G1 | 也许 | 是 | e | 自评 |": "适用",
            "| 2026-11-04 | c | G1 | 是 | 大概 | e | 自评 |": "遵守",
            "| 2026-11-04 | c | G1 | 不适用 | 是 | e | 自评 |": "不适用 rows",
            "| 2026-11-04 | c | G1 | 是 | — | e | 自评 |": "need a verdict",
            "| 2026-11-04 | c | G1 | 是 | 是 |  | 自评 |": "empty evidence",
            "| 2026-11-04 | c | G1 | 是 | 是 | e | 他评 |": "记录方式",
            "| 2026-11-04 | c | G1 | 是 | 是 | e |": "columns",
        }
        for line, expected in cases.items():
            with self.subTest(line=line):
                errors, _ = check_ledger.check_compliance(self.write(COMPLIANCE_HEADER + line + "\n"))
                self.assertTrue(any(expected in e for e in errors), errors)

    def test_repository_files_pass(self):
        self.assertEqual(check_ledger.check_ledger(check_ledger.DEFAULT)[0], [])
        self.assertEqual(check_ledger.check_compliance(check_ledger.COMPLIANCE)[0], [])


class BuildSuiteTest(unittest.TestCase):
    def test_frontmatter_parsing(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "SKILL.md"
            path.write_text('---\nname: x\ndescription: >\n  folded\n  text\nversion: "1.2.3"\n---\nbody\n', encoding="utf-8")
            fm = build_suite.frontmatter(path)
            self.assertEqual(fm["description"], "folded text")
            self.assertEqual(fm["version"], "1.2.3")

    def test_release_notes_excluded(self):
        self.assertTrue(build_suite.excluded("RELEASE_v1.2.0.md"))
        self.assertTrue(build_suite.excluded("INTRO.md"))
        self.assertFalse(build_suite.excluded("verification.md"))

    def test_repository_sources_validate(self):
        with contextlib.redirect_stdout(io.StringIO()):
            version = build_suite.validate()
        self.assertRegex(version, r"^\d+\.\d+\.\d+$")

    def test_package_is_one_skill_and_deterministic(self):
        entries = build_suite.package_files()
        build_suite.validate_package(entries)
        first = build_suite.make_zip(entries, "dev-pdca/")
        self.assertEqual(first, build_suite.make_zip(entries, "dev-pdca/"))
        with zipfile.ZipFile(io.BytesIO(first)) as zf:
            names = zf.namelist()
        self.assertEqual([n for n in names if n.lower().endswith("skill.md")], ["dev-pdca/SKILL.md"])
        self.assertTrue(all(n.count("/") <= 2 for n in names))

    def test_subskill_field_check_catches_missing_field(self):
        original = build_suite.frontmatter

        def without_hint(path):
            fields = original(path)
            if path.parent.name == "evolver":
                fields.pop("argument-hint", None)
            return fields

        build_suite.frontmatter = without_hint
        try:
            with self.assertRaises(SystemExit) as caught:
                with contextlib.redirect_stdout(io.StringIO()):
                    build_suite.validate()
        finally:
            build_suite.frontmatter = original
        self.assertIn("evolver/SKILL.md: frontmatter fields", str(caught.exception))


def plugin_fixture(tmp: Path) -> Path:
    """A copy of the plugin-relevant parts of the repository."""
    import shutil
    root = tmp / "repo"
    for part in [".claude-plugin", "README.md", "LICENSE", "CHANGELOG.md", "assets"] + build_plugin.skill_dirs(
            json.loads((REPO / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))):
        src = REPO / part
        (shutil.copytree if src.is_dir() else shutil.copy2)(src, root / part)
    return root


def git(root: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True,
                   env={"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t",
                        "GIT_COMMITTER_EMAIL": "t@t", "PATH": "/usr/bin:/bin:/usr/local/bin"})


class BuildPluginTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: __import__("shutil").rmtree(self.tmp))
        self.root = plugin_fixture(self.tmp)
        self.manifest_path = self.root / ".claude-plugin" / "plugin.json"

    def manifest(self) -> dict:
        return json.loads(self.manifest_path.read_text(encoding="utf-8"))

    def write_manifest(self, data: dict) -> None:
        self.manifest_path.write_text(json.dumps(data), encoding="utf-8")

    def test_repository_passes(self):
        self.assertEqual(build_plugin.check(REPO), [])
        self.assertEqual(build_plugin.check(self.root), [])

    def test_skill_list_must_match_marketplace(self):
        data = self.manifest()
        data["skills"] = data["skills"][:-1]
        self.write_manifest(data)
        self.assertTrue(any("skills differ" in e for e in build_plugin.check(self.root)))

    def test_missing_reference_file(self):
        (self.root / "tasker" / "references" / "verification.md").unlink()
        errors = build_plugin.check(self.root)
        self.assertTrue(any("references missing file references/verification.md" in e for e in errors), errors)

    def test_deleted_tracked_reference_reports_instead_of_crashing(self):
        git(self.root, "init", "-q")
        git(self.root, "add", "-A")
        git(self.root, "commit", "-qm", "base")
        (self.root / "tasker" / "references" / "verification.md").unlink()
        errors = build_plugin.check(self.root)
        self.assertTrue(any("references missing file references/verification.md" in e for e in errors), errors)

    def test_tag_must_match_version(self):
        version = self.manifest()["version"]
        self.assertEqual(build_plugin.check(self.root, tag=f"v{version}"), [])
        self.assertTrue(any("does not match" in e for e in build_plugin.check(self.root, tag="v0.0.1")))

    def test_tag_needs_changelog_section(self):
        changelog = self.root / "CHANGELOG.md"
        version = self.manifest()["version"]
        heading = f"## {build_plugin.NAME} {version}"
        changelog.write_text(changelog.read_text(encoding="utf-8").replace(heading, "## old"), encoding="utf-8")
        errors = build_plugin.check(self.root, tag=f"v{version}")
        self.assertTrue(any(f"no '{heading}' section" in e for e in errors), errors)
        self.assertEqual(build_plugin.check(self.root), [])

    def test_skill_change_needs_version_bump(self):
        version = self.manifest()["version"]
        tag = f"v{version}"
        git(self.root, "init", "-q")
        git(self.root, "add", "-A")
        git(self.root, "commit", "-qm", "base")
        git(self.root, "tag", tag)
        self.assertEqual(build_plugin.check(self.root, since=tag), [])
        with (self.root / "planner" / "SKILL.md").open("a", encoding="utf-8") as f:
            f.write("\nchanged\n")
        self.assertTrue(any("is not higher" in e for e in build_plugin.check(self.root, since=tag)))
        major, minor, patch = (int(p) for p in version.split("."))
        data = self.manifest()
        data["version"] = f"{major}.{minor}.{patch + 1}"
        self.write_manifest(data)
        self.assertEqual(build_plugin.check(self.root, since=tag), [])

    def test_export_must_match_stored_content(self):
        git(self.root, "init", "-q")
        (self.root / "crlf.ps1").write_bytes(b"line one\nline two\n")
        (self.root / ".gitattributes").write_text("*.ps1 text eol=crlf\n", encoding="utf-8")
        git(self.root, "add", "-A")
        errors = build_plugin.check(self.root)
        self.assertTrue(any("crlf.ps1 changes on git export" in e for e in errors), errors)
        (self.root / ".gitattributes").write_text("*.ps1 -text\n", encoding="utf-8")
        git(self.root, "add", "-A")
        self.assertEqual(build_plugin.check(self.root), [])

    def test_directory_naming_rules(self):
        for bad in ("claude-tools", "Tealun", "plugin", "-x"):
            with self.subTest(name=bad):
                data = self.manifest()
                data["name"] = bad
                self.write_manifest(data)
                self.assertTrue(any("naming rules" in e for e in build_plugin.check(self.root)))

    def test_build_is_reproducible_and_scoped(self):
        _, first = build_plugin.make_plugin(self.root)
        _, second = build_plugin.make_plugin(self.root)
        self.assertEqual(first, second)
        with zipfile.ZipFile(io.BytesIO(first)) as zf:
            names = zf.namelist()
            packaged = json.loads(zf.read(".claude-plugin/plugin.json"))
        self.assertEqual(sum(n.endswith("/SKILL.md") for n in names), 6)
        self.assertTrue(all(s.startswith("./skills/") for s in packaged["skills"]))
        for forbidden in ("CLAUDE.md", "AGENTS.md", "docs/", "tests/", "/agents/", ".github/", "RELEASE_", "INTRO.md"):
            self.assertFalse(any(forbidden in n for n in names), forbidden)
        self.assertIn(packaged["icon"].lstrip("./"), names)


if __name__ == "__main__":
    unittest.main()
