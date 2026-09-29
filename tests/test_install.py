from __future__ import annotations

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import install


class InstallTests(unittest.TestCase):
    def test_declares_twelve_agents_and_unique_ids(self) -> None:
        self.assertEqual(len(install.AGENTS), 12)
        self.assertEqual(len(install.AGENT_BY_KEY), 12)

    def test_normalizes_aliases_and_deduplicates(self) -> None:
        selected = install.normalize_agent_names(["claude", "claude-code", "copilot"])
        self.assertEqual([agent.key for agent in selected], ["claude-code", "github-copilot"])

    def test_rejects_unknown_agent(self) -> None:
        with self.assertRaises(install.InstallError):
            install.normalize_agent_names(["unknown"])

    def test_agent_detection_uses_specific_markers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".claude").mkdir()
            (root / ".github").mkdir()
            with patch("install.shutil.which", return_value=None):
                detected = {agent.key for agent in install.detect_agents(root)}
            self.assertIn("claude-code", detected)
            self.assertNotIn("github-copilot", detected)
            (root / ".github" / "copilot-instructions.md").write_text(
                "instructions\n",
                encoding="utf-8",
            )
            with patch("install.shutil.which", return_value=None):
                detected = {agent.key for agent in install.detect_agents(root)}
            self.assertIn("github-copilot", detected)

    def test_cursor_pointer_has_one_frontmatter_block(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            pointer = Path(temporary) / ".cursor" / "rules" / "scholar-humanizer.mdc"
            install.update_pointer_file(
                pointer,
                [".cursor/skills/scholar-humanizer/SKILL.md"],
                "cursor",
            )
            install.update_pointer_file(
                pointer,
                [".cursor/skills/scholar-humanizer/SKILL.md"],
                "cursor",
            )
            contents = pointer.read_text(encoding="utf-8")
            self.assertEqual(contents.count("description: Apply Scholar Humanizer"), 1)
            self.assertEqual(contents.count(install.START_MARKER), 1)
            self.assertIn("alwaysApply: false", contents)

    def test_install_copies_skill_payload_and_preserves_extra_files(self) -> None:
        source_root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / ".agents" / "skills" / install.SKILL_NAME
            self.assertTrue(
                install.copy_payload(source_root, destination, overwrite=False)
            )
            self.assertTrue((destination / "SKILL.md").is_file())
            self.assertTrue((destination / "rules" / "academic_voice.md").is_file())
            self.assertTrue((destination / "scripts" / "academic-slop-checker.py").is_file())
            self.assertTrue((destination / "scripts" / "academic_slop_checker.py").is_file())

            custom_file = destination / "local-note.txt"
            custom_file.write_text("keep me\n", encoding="utf-8")
            (destination / "SKILL.md").write_text("local version\n", encoding="utf-8")
            self.assertFalse(
                install.copy_payload(source_root, destination, overwrite=False)
            )
            self.assertEqual((destination / "SKILL.md").read_text(encoding="utf-8"), "local version\n")

            self.assertTrue(
                install.copy_payload(source_root, destination, overwrite=True)
            )
            self.assertIn("# Scholar Humanizer", (destination / "SKILL.md").read_text(encoding="utf-8"))
            self.assertTrue(custom_file.exists())

    def test_pointer_update_is_idempotent_and_preserves_other_text(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            pointer = Path(temporary) / "AGENTS.md"
            pointer.write_text("# Project instructions\n\nKeep this text.\n", encoding="utf-8")
            reference = ".agents/skills/scholar-humanizer/SKILL.md"

            install.update_pointer_file(pointer, [reference], "markdown")
            install.update_pointer_file(pointer, [reference], "markdown")

            contents = pointer.read_text(encoding="utf-8")
            self.assertEqual(contents.count(install.START_MARKER), 1)
            self.assertEqual(contents.count(install.END_MARKER), 1)
            self.assertIn("Keep this text.", contents)
            self.assertIn(reference, contents)

    def test_pointer_update_keeps_other_installed_agent_paths(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            pointer = Path(temporary) / "AGENTS.md"
            first = ".codex/skills/scholar-humanizer/SKILL.md"
            second = ".agents/skills/scholar-humanizer/SKILL.md"
            install.update_pointer_file(pointer, [first], "markdown")
            install.update_pointer_file(pointer, [second], "markdown")
            contents = pointer.read_text(encoding="utf-8")
            self.assertTrue(contents.startswith(install.START_MARKER))
            self.assertIn(first, contents)
            self.assertIn(second, contents)
            self.assertEqual(contents.count(install.START_MARKER), 1)

    def test_malformed_pointer_markers_fail_without_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            pointer = Path(temporary) / "AGENTS.md"
            original = f"{install.START_MARKER}\nunfinished\n"
            pointer.write_text(original, encoding="utf-8")
            with self.assertRaises(install.InstallError):
                install.update_pointer_file(pointer, [], "markdown")
            self.assertEqual(pointer.read_text(encoding="utf-8"), original)

    def test_global_paths_include_agent_specific_locations(self) -> None:
        codex = install.AGENT_BY_KEY["codex"]
        opencode = install.AGENT_BY_KEY["opencode"]
        pi = install.AGENT_BY_KEY["pi"]
        self.assertEqual(codex.skills_directory("global"), Path(".agents/skills"))
        self.assertEqual(opencode.skills_directory("global"), Path(".config/opencode/skills"))
        self.assertEqual(pi.skills_directory("global"), Path(".pi/agent/skills"))

    def test_readme_install_paths_match_installer_configuration(self) -> None:
        readme = (Path(__file__).resolve().parents[1] / "README.md").read_text(
            encoding="utf-8"
        )
        for agent in install.AGENTS:
            project_path = agent.skills_directory("project").as_posix().rstrip("/") + "/"
            global_path = (
                Path("~") / agent.skills_directory("global")
            ).as_posix().rstrip("/") + "/"
            row = next(
                line
                for line in readme.splitlines()
                if line.startswith(f"| {agent.label} |")
            )
            self.assertIn(f"`{project_path}`", row)
            self.assertIn(f"`{global_path}`", row)

    def test_list_option_is_read_only_and_lists_all_agents(self) -> None:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = install.main(["--list"])
        self.assertEqual(status, 0)
        for agent in install.AGENTS:
            self.assertIn(agent.key, output.getvalue())

    def test_project_cli_installs_payload_and_pointer(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                status = install.main(
                    [
                        "--agent",
                        "codex",
                        "--project-dir",
                        str(root),
                        "--yes",
                    ]
                )
            destination = root / ".codex" / "skills" / install.SKILL_NAME
            self.assertEqual(status, 0)
            self.assertTrue((destination / "SKILL.md").is_file())
            self.assertIn(
                ".codex/skills/scholar-humanizer/SKILL.md",
                (root / "AGENTS.md").read_text(encoding="utf-8"),
            )
            self.assertIn("Installed:", output.getvalue())

    def test_global_cli_installs_without_modifying_instruction_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                status = install.main(
                    [
                        "--agent",
                        "pi",
                        "--scope",
                        "global",
                        "--home-dir",
                        str(root),
                        "--yes",
                    ]
                )
            destination = root / ".pi" / "agent" / "skills" / install.SKILL_NAME
            self.assertEqual(status, 0)
            self.assertTrue((destination / "SKILL.md").is_file())
            self.assertFalse((root / "AGENTS.md").exists())
            self.assertIn("Done:", output.getvalue())

    def test_project_dry_run_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            with contextlib.redirect_stdout(io.StringIO()):
                status = install.main(
                    [
                        "--agent",
                        "claude-code",
                        "--project-dir",
                        str(root),
                        "--dry-run",
                    ]
                )
            self.assertEqual(status, 0)
            self.assertFalse((root / ".claude").exists())
            self.assertFalse((root / "CLAUDE.md").exists())

    def test_malformed_pointer_stops_install_before_copying_payload(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "AGENTS.md").write_text(
                f"{install.START_MARKER}\nunfinished\n",
                encoding="utf-8",
            )
            errors = io.StringIO()
            with contextlib.redirect_stderr(errors):
                status = install.main(
                    [
                        "--agent",
                        "codex",
                        "--project-dir",
                        str(root),
                        "--yes",
                    ]
                )
            destination = root / ".codex" / "skills" / install.SKILL_NAME
            self.assertEqual(status, 1)
            self.assertFalse(destination.exists())
            self.assertIn("markers are malformed", errors.getvalue())


if __name__ == "__main__":
    unittest.main()
