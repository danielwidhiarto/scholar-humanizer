#!/usr/bin/env python3
"""Validate Scholar Humanizer's package structure without external dependencies."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = (ROOT / "SKILL.md").read_text()


def require(match: re.Match[str] | None, message: str) -> re.Match[str]:
    if match is None:
        raise SystemExit(message)
    return match


# Check YAML frontmatter
frontmatter = require(
    re.match(r"\A---\n(.*?)\n---\n", SKILL, re.DOTALL),
    "SKILL.md must start with YAML frontmatter",
).group(1)

for nonportable_key in ("compatibility:", "allowed-tools:"):
    if re.search(rf"(?m)^{re.escape(nonportable_key)}", frontmatter):
        raise SystemExit(f"Remove nonportable frontmatter key: {nonportable_key[:-1]}")

# Check version
skill_version = require(
    re.search(r'(?m)^\s+version:\s*["\']([^"\']+)["\']\s*$', frontmatter),
    "SKILL.md metadata.version is missing",
).group(1)

# Check rule files exist
rules_dir = ROOT / "rules"
for rule_file in ("academic_voice.md", "ai_slop.md", "narrative_citation.md"):
    if not (rules_dir / rule_file).exists():
        raise SystemExit(f"Missing rule file: rules/{rule_file}")

# Check references exist
refs_dir = ROOT / "references"
for ref_file in ("banned_phrases.md",):
    if not (refs_dir / ref_file).exists():
        raise SystemExit(f"Missing reference file: references/{ref_file}")

# Check examples exist
examples_dir = ROOT / "examples"
for example_file in ("before_after.md", "scoring_examples.md"):
    if not (examples_dir / example_file).exists():
        raise SystemExit(f"Missing example file: examples/{example_file}")

# Check optional tooling and its regression tests exist
scripts_dir = ROOT / "scripts"
for script_file in (
    "install.py",
    "academic-slop-checker.py",
    "academic_slop_checker.py",
):
    if not (scripts_dir / script_file).is_file():
        raise SystemExit(f"Missing script: scripts/{script_file}")

tests_dir = ROOT / "tests"
for test_file in ("test_install.py", "test_academic_slop_checker.py"):
    if not (tests_dir / test_file).is_file():
        raise SystemExit(f"Missing regression test: tests/{test_file}")

# Check SKILL.md line count (portability budget)
if len(SKILL.splitlines()) > 200:
    raise SystemExit(f"SKILL.md exceeds 200-line portability budget ({len(SKILL.splitlines())} lines)")

print(f"Scholar Humanizer v{skill_version} is valid")
