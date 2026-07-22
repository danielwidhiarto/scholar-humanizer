# AGENTS.md

Guidance for AI coding agents (Claude Code, Codex, Warp, etc.) working in this repository.

## What this repo is

A portable agent skill for humanizing academic writing. The runtime artifact is `SKILL.md`: the agent reads its YAML frontmatter and editor prompt. There is no build step. The repo avoids wording that limits support to one or two harnesses.

## Key files

- `SKILL.md` — the skill itself. YAML frontmatter (`name`, `description`, `license`, `metadata.version`) followed by the section-aware rules, scoring rubric, and process. **This is the source of truth.**
- `README.md` — for humans: installation, usage, section rules table, scoring rubric.
- `rules/academic_voice.md` — what to KEEP per section (passive voice, hedging, formal transitions).
- `rules/ai_slop.md` — what to REMOVE (AI patterns adapted for academic context).
- `references/banned_phrases.md` — phrase-level bans, split into always-remove and context-dependent.
- `examples/before_after.md` — concrete rewrites per section type.
- `examples/scoring_examples.md` — rubric demonstrations with scored samples.
- `scripts/validate-package.py` — dependency-free package and synchronization checks.

## The maintenance contract

`SKILL.md` and `README.md` must stay in sync. When you change behavior or content:

- **Rules:** `rules/academic_voice.md` and `rules/ai_slop.md` define the section-aware behavior. If you add, remove, or renumber rules, update the README and SKILL.md references in the same change.
- **Banned phrases:** `references/banned_phrases.md` is the phrase-level ban list. Keep it in sync with `rules/ai_slop.md` — if a pattern appears in one, it should be reflected in the other.
- **Version:** `SKILL.md` frontmatter stores the version under `metadata.version`. Bump when behavior changes.
- **Compatibility:** keep install and usage language harness-neutral. The skill should work in any agent harness that can load Markdown skill instructions.
- **Validation:** run `python3 scripts/validate-package.py` before publishing.

## Editing SKILL.md

- Preserve valid YAML frontmatter (formatting and indentation).
- The prompt below the frontmatter is the product. Edit it like a careful instruction document, not code.
- Section-aware rules are the core differentiator — don't flatten them into generic humanization rules.

## Academic conventions

This skill deliberately preserves patterns that general humanizers remove:

- **Passive voice in Methods** — required, not a flaw
- **Hedging in Discussion** — expected academic caution
- **Formal transitions** — standard in academic prose
- **Discipline-specific terminology** — not AI-isms

When editing rules, ask: "Would a journal reviewer flag this?" If no, it's probably fine to keep.
