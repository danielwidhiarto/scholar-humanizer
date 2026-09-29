#!/usr/bin/env python3
"""Install Scholar Humanizer into supported agent skill directories."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "scholar-humanizer"
START_MARKER = "<!-- scholar-humanizer:start -->"
END_MARKER = "<!-- scholar-humanizer:end -->"
PAYLOAD_PATHS = (
    Path("SKILL.md"),
    Path("rules"),
    Path("references"),
    Path("examples"),
    Path("LICENSE"),
    Path("scripts") / "academic-slop-checker.py",
    Path("scripts") / "academic_slop_checker.py",
)


@dataclass(frozen=True)
class Agent:
    key: str
    label: str
    project_skills: tuple[str, ...]
    global_skills: tuple[str, ...]
    executable: str | None
    markers: tuple[str, ...]
    pointer_file: tuple[str, ...] | None
    pointer_format: str = "markdown"

    def skills_directory(self, scope: str) -> Path:
        parts = self.project_skills if scope == "project" else self.global_skills
        return Path(*parts)

    def instruction_file(self) -> Path | None:
        return Path(*self.pointer_file) if self.pointer_file else None


@dataclass
class PointerPlan:
    paths: set[str]
    pointer_format: str


AGENTS: tuple[Agent, ...] = (
    Agent(
        "claude-code",
        "Claude Code",
        (".claude", "skills"),
        (".claude", "skills"),
        "claude",
        (".claude", "CLAUDE.md"),
        ("CLAUDE.md",),
    ),
    Agent(
        "codex",
        "Codex",
        (".codex", "skills"),
        (".agents", "skills"),
        "codex",
        (".codex",),
        ("AGENTS.md",),
    ),
    Agent(
        "antigravity",
        "Antigravity",
        (".agents", "skills"),
        (".gemini", "config", "skills"),
        "agy",
        (".antigravity",),
        ("AGENTS.md",),
    ),
    Agent(
        "cursor",
        "Cursor",
        (".cursor", "skills"),
        (".cursor", "skills"),
        "cursor-agent",
        (".cursor",),
        (".cursor", "rules", "scholar-humanizer.mdc"),
        "cursor",
    ),
    Agent(
        "cline",
        "Cline",
        (".cline", "skills"),
        (".cline", "skills"),
        "cline",
        (".cline", ".clinerules"),
        None,
    ),
    Agent(
        "opencode",
        "OpenCode",
        (".opencode", "skills"),
        (".config", "opencode", "skills"),
        "opencode",
        (".opencode",),
        ("AGENTS.md",),
    ),
    Agent(
        "amp",
        "Amp",
        (".agents", "skills"),
        (".config", "agents", "skills"),
        "amp",
        (".amp",),
        ("AGENTS.md",),
    ),
    Agent(
        "gemini-cli",
        "Gemini CLI",
        (".gemini", "skills"),
        (".gemini", "skills"),
        "gemini",
        (".gemini", "GEMINI.md"),
        ("GEMINI.md",),
    ),
    Agent(
        "hermes",
        "Hermes",
        (".hermes", "skills"),
        (".hermes", "skills"),
        "hermes",
        (".hermes", "HERMES.md"),
        ("HERMES.md",),
    ),
    Agent(
        "github-copilot",
        "GitHub Copilot",
        (".agents", "skills"),
        (".agents", "skills"),
        "copilot",
        (".github/copilot-instructions.md",),
        (".github", "copilot-instructions.md"),
    ),
    Agent(
        "kimi-code",
        "Kimi Code",
        (".agents", "skills"),
        (".agents", "skills"),
        "kimi",
        (".kimi-code", ".kimi"),
        ("AGENTS.md",),
    ),
    Agent(
        "pi",
        "Pi",
        (".pi", "skills"),
        (".pi", "agent", "skills"),
        "pi",
        (".pi",),
        ("AGENTS.md",),
    ),
)

AGENT_BY_KEY = {agent.key: agent for agent in AGENTS}
ALIASES = {
    "claude": "claude-code",
    "gemini": "gemini-cli",
    "copilot": "github-copilot",
    "kimi": "kimi-code",
}


class InstallError(Exception):
    """An actionable installation error."""


def normalize_agent_names(values: Iterable[str]) -> list[Agent]:
    selected: dict[str, Agent] = {}
    for value in values:
        key = value.strip().lower()
        if key == "all":
            return list(AGENTS)
        key = ALIASES.get(key, key)
        agent = AGENT_BY_KEY.get(key)
        if agent is None:
            valid = ", ".join(agent.key for agent in AGENTS)
            raise InstallError(f"Unknown agent '{value}'. Choose one of: {valid}, all.")
        selected[agent.key] = agent
    if not selected:
        raise InstallError("Select at least one agent.")
    return [agent for agent in AGENTS if agent.key in selected]


def detect_agents(scope_root: Path) -> list[Agent]:
    detected: list[Agent] = []
    for agent in AGENTS:
        has_marker = any((scope_root / marker).exists() for marker in agent.markers)
        has_cli = bool(agent.executable and shutil.which(agent.executable))
        if has_marker or has_cli:
            detected.append(agent)
    return detected


def payload_files(source_root: Path = ROOT) -> list[Path]:
    files: list[Path] = []
    for item in PAYLOAD_PATHS:
        source = source_root / item
        if not source.exists():
            raise InstallError(f"Required package content is missing: {item}")
        if source.is_dir():
            files.extend(path for path in source.rglob("*") if path.is_file())
        else:
            files.append(source)
    return files


def destination_for(scope_root: Path, skills_directory: Path) -> Path:
    root = scope_root.resolve()
    raw_destination = scope_root / skills_directory / SKILL_NAME
    if raw_destination.is_symlink():
        raise InstallError(f"Refusing to install through a symbolic link: {raw_destination}")
    destination = raw_destination.resolve()
    try:
        destination.relative_to(root)
    except ValueError as error:
        raise InstallError(f"Install destination escapes the selected scope: {destination}") from error
    return destination


def copy_payload(
    source_root: Path,
    destination: Path,
    *,
    overwrite: bool,
) -> bool:
    if destination.is_symlink():
        raise InstallError(f"Refusing to install through a symbolic link: {destination}")
    if destination.exists() and not destination.is_dir():
        raise InstallError(f"Install destination is not a directory: {destination}")
    if destination.exists() and not overwrite:
        return False

    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(
        prefix=".scholar-humanizer-",
        dir=destination.parent,
    ) as temporary:
        staged = Path(temporary) / SKILL_NAME
        staged.mkdir()
        for relative_path in PAYLOAD_PATHS:
            source = source_root / relative_path
            target = staged / relative_path
            if source.is_dir():
                shutil.copytree(source, target)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)

        if destination.exists():
            shutil.copytree(staged, destination, dirs_exist_ok=True)
        else:
            staged.replace(destination)
    return True


def pointer_content(skill_paths: Iterable[str], pointer_format: str) -> str:
    paths = sorted(set(skill_paths))
    read_lines = "\n".join(f"- `{path}`" for path in paths)
    if pointer_format == "cursor":
        return (
            f"{START_MARKER}\n"
            "## Scholar Humanizer\n"
            "When editing academic prose, read and follow the skill file(s):\n"
            f"{read_lines}\n"
            "Treat pattern matches as review cues, preserve claims and technical syntax, "
            "and do not optimize text to evade AI detectors.\n"
            f"{END_MARKER}"
        )
    return (
        f"{START_MARKER}\n"
        "## Scholar Humanizer\n"
        "When editing academic prose, read and follow the skill file(s):\n"
        f"{read_lines}\n"
        "Treat pattern matches as review cues, preserve claims and technical syntax, "
        "and do not optimize text to evade AI detectors.\n"
        f"{END_MARKER}"
    )


def ensure_pointer_is_scoped(scope_root: Path, pointer_path: Path) -> None:
    if pointer_path.is_symlink():
        raise InstallError(f"Refusing to modify a symbolic-link instruction file: {pointer_path}")
    try:
        pointer_path.resolve().relative_to(scope_root.resolve())
    except ValueError as error:
        raise InstallError(
            f"Instruction file escapes the selected project: {pointer_path}"
        ) from error


def update_pointer_file(
    path: Path,
    skill_paths: Iterable[str],
    pointer_format: str,
) -> None:
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    new_paths = set(skill_paths)
    if pointer_format == "cursor" and not existing.lstrip().startswith("---"):
        frontmatter = (
            "---\n"
            "description: Apply Scholar Humanizer to academic prose editing\n"
            "alwaysApply: false\n"
            "---\n"
        )
        existing = f"{frontmatter}\n{existing}" if existing else frontmatter
    start_count = existing.count(START_MARKER)
    end_count = existing.count(END_MARKER)
    if start_count != end_count or start_count > 1:
        raise InstallError(f"Managed pointer markers are malformed in {path}")

    block = pointer_content(new_paths, pointer_format)
    if start_count == 1:
        start = existing.index(START_MARKER)
        end = existing.index(END_MARKER, start) + len(END_MARKER)
        old_block = existing[start:end]
        old_paths = re.findall(r"(?m)^- `([^`]+/SKILL\.md)`$", old_block)
        block = pointer_content(set(old_paths) | new_paths, pointer_format)
        updated = existing[:start] + block + existing[end:]
    elif not existing:
        updated = f"{block}\n"
    else:
        separator = "" if not existing or existing.endswith("\n") else "\n"
        updated = f"{existing}{separator}\n{block}\n"

    path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=path.parent,
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(updated)
        temporary_path.replace(path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def resolve_selection(args: argparse.Namespace, scope_root: Path) -> list[Agent]:
    if args.agent:
        raw_names = [name for group in args.agent for name in group.split(",")]
        return normalize_agent_names(raw_names)

    detected = detect_agents(scope_root)
    detected_names = ", ".join(agent.key for agent in detected) or "none"
    if args.yes:
        if not detected:
            raise InstallError("No agents detected; pass --agent <id> or --agent all.")
        print(f"Detected agents: {detected_names}")
        return detected

    print("Supported agents:")
    for agent in AGENTS:
        print(f"  {agent.key}: {agent.label}")
    if detected:
        print(f"Detected in {scope_root}: {detected_names}")
        response = input("Agent IDs, 'all', or Enter to use detected agents: ").strip()
        return normalize_agent_names(response.split(",")) if response else detected

    response = input("Enter agent IDs separated by commas, or 'all': ").strip()
    return normalize_agent_names(response.split(","))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Install Scholar Humanizer into agent skill directories."
    )
    parser.add_argument(
        "--agent",
        action="append",
        help="Agent ID(s), comma-separated, or 'all'. May be repeated.",
    )
    parser.add_argument(
        "--scope",
        choices=("project", "global"),
        default="project",
        help="Install into the current project or the current user's home directory.",
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path.cwd(),
        help="Project root for project-scope installs (default: current directory).",
    )
    parser.add_argument(
        "--home-dir",
        type=Path,
        default=Path.home(),
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--no-pointer",
        action="store_true",
        help="Do not add or update project instruction-file pointers.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite package files in an existing skill directory; leave other files untouched.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show destinations without writing files.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip the final confirmation; auto-select detected agents if --agent is omitted.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List supported agents and their configured install paths.",
    )
    return parser


def print_agent_list() -> None:
    print("Configured agent skill directories (paths are maintained by this installer):")
    for agent in AGENTS:
        project = agent.skills_directory("project").as_posix()
        global_path = (Path.home() / agent.skills_directory("global")).as_posix()
        print(f"{agent.key:16} project: {project}; global: {global_path}")


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.list:
        print_agent_list()
        return 0

    scope_root = args.project_dir if args.scope == "project" else args.home_dir
    scope_root = scope_root.expanduser().resolve()
    if not scope_root.is_dir():
        parser.error(f"Selected scope does not exist or is not a directory: {scope_root}")

    try:
        selected = resolve_selection(args, scope_root)
        payload_files(ROOT)

        destinations: dict[Path, list[Agent]] = {}
        pointers: dict[Path, PointerPlan] = {}
        for agent in selected:
            destination = destination_for(
                scope_root,
                agent.skills_directory(args.scope),
            )
            destinations.setdefault(destination, []).append(agent)
            pointer_file = agent.instruction_file()
            if args.scope == "project" and not args.no_pointer and pointer_file:
                pointer_path = scope_root / pointer_file
                ensure_pointer_is_scoped(scope_root, pointer_path)
                skill_reference = destination.relative_to(scope_root).as_posix() + "/SKILL.md"
                record = pointers.setdefault(
                    pointer_path,
                    PointerPlan(set(), agent.pointer_format),
                )
                record.paths.add(skill_reference)

        print(f"Scope: {args.scope} ({scope_root})")
        print("Install destinations:")
        for destination, agents in destinations.items():
            names = ", ".join(agent.key for agent in agents)
            action = "overwrite package files" if destination.exists() and args.force else (
                "skip existing" if destination.exists() else "install"
            )
            print(f"  {destination} ({names}; {action})")
        if pointers:
            print("Instruction files to add/update:")
            for pointer_path in sorted(pointers):
                print(f"  {pointer_path}")
                existing = (
                    pointer_path.read_text(encoding="utf-8")
                    if pointer_path.exists()
                    else ""
                )
                if (
                    existing.count(START_MARKER) != existing.count(END_MARKER)
                    or existing.count(START_MARKER) > 1
                ):
                    raise InstallError(
                        f"Managed pointer markers are malformed in {pointer_path}"
                    )
        if args.dry_run:
            print("Dry run only; no files were written.")
            return 0
        if not args.yes and input("Continue? [y/N] ").strip().lower() not in {"y", "yes"}:
            print("Installation cancelled.")
            return 0

        installed = 0
        skipped = 0
        for destination in destinations:
            if copy_payload(ROOT, destination, overwrite=args.force):
                installed += 1
                print(f"Installed: {destination}")
            else:
                skipped += 1
                print(f"Skipped existing skill (use --force to update): {destination}")

        for pointer_path, record in pointers.items():
            update_pointer_file(
                pointer_path,
                record.paths,
                record.pointer_format,
            )
            print(f"Updated pointer: {pointer_path}")

        print(f"Done: {installed} skill folder(s) installed, {skipped} skipped.")
        return 0
    except EOFError:
        print(
            "install.py: error: no interactive input; pass --agent <id> "
            "and use --yes after reviewing the destination.",
            file=sys.stderr,
        )
        return 1
    except (InstallError, OSError, UnicodeError) as error:
        print(f"install.py: error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
