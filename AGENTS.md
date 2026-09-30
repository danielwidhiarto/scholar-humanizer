# AGENTS.md

Guidance for AI coding agents working in this repository.

## What this repo is

A portable, harness-neutral agent skill for improving academic prose. The runtime artifact is `SKILL.md`: an agent reads its YAML frontmatter and instructions. There is no build step.

## Key files

- `SKILL.md` — skill instructions, section matrix, workflow, and rubric. YAML frontmatter includes `name`, `description`, `license`, and `metadata.version`. **This is the behavior source of truth.**
- `README.md` — installation, usage, section rules, scoring guidance, and source attribution.
- `rules/academic_voice.md` — academic conventions to preserve by section.
- `rules/ai_slop.md` — contextual pattern-review guidance.
- `rules/narrative_citation.md` — cluster conditions for reviewing "Author (Year) found..." templates.
- `references/banned_phrases.md` — phrase-level review cues, not universal bans.
- `examples/before_after.md` — rewrites and regression cases, including LaTeX syntax protection.
- `examples/scoring_examples.md` — rubric demonstrations.
- `scripts/install.py` — optional, dependency-free installer for the configured agent skill directories.
- `scripts/academic-slop-checker.py` and `scripts/academic_slop_checker.py` — optional diagnostic checker and implementation module; findings are cues, never authorship verdicts.
- `scripts/validate-package.py` — dependency-free package-structure and portability checks.
- `tests/` — standard-library regression tests for the installer and checker.

## The maintenance contract

`SKILL.md` and `README.md` must stay in sync. When changing behavior or content:

- **Rules:** Preserve section-aware behavior. Pattern matches are review cues; do not turn passive voice, hedging, transitions, adverbs, contrasts, triads, or dashes into universal bans. Preserve numbered findings; convert related unnumbered bullets to prose only when no claim is lost.
- **Phrase cues:** Keep `references/banned_phrases.md` consistent with `rules/ai_slop.md`; make clear that a phrase match alone is not a verdict.
- **Integrity:** Do not add unsupported claims, numbers, citations, methods, or recommendations in rules or examples. For `.tex`, protect commands, math, environments, citation keys, labels/references, values, and escaped syntax.
- **Examples:** Keep before/after pairs faithful to their source and include false positives when changing a pattern rule.
- **Version:** `SKILL.md` frontmatter stores the version under `metadata.version`. Bump for behavior changes and update `CHANGELOG.md`.
- **Compatibility:** Keep usage language harness-neutral. The README's `npx skills add danielwidhiarto/scholar-humanizer` package path was recognized by the Skills CLI in a non-installing `--list` check; retain manual installation as fallback and do not claim untested agent-specific support.
- **Installer:** Keep the supported agent IDs and configured project/global directories in `scripts/install.py` and the README table synchronized. Detection is a convenience, not proof that an agent runtime loads a given path. Do not overwrite existing package folders without `--force`, remove unrelated files, or write outside the chosen scope.
- **Checker:** Keep `scripts/academic-slop-checker.py` diagnostic-only. It must preserve source files, report line numbers, mask protected LaTeX/Markdown spans, and never call a citation fabricated or text AI-written from a pattern match.
- **Validation:** Run `python -m unittest discover -s tests -v` and `python scripts/validate-package.py` before publishing. The validator checks frontmatter, required package files and tests, and the 200-line `SKILL.md` limit.

## Editing SKILL.md

- Preserve valid YAML frontmatter (formatting and indentation).
- The prompt below the frontmatter is the product. Edit it like a careful instruction document, not code.
- Keep the skill at or below 200 lines.
- Section-aware rules are the core differentiator — do not flatten them into generic humanization rules.

## Academic conventions

This skill deliberately preserves conventions that general humanizers may remove:

- **Passive voice in Methods** — required by the repository default, unless explicit target guidance says otherwise
- **Hedging in Discussion** — expected academic caution
- **Formal transitions** — standard in academic prose
- **Discipline-specific terminology** — not AI-isms

Do not judge a construction by a phrase match alone. When editing rules, ask whether the construction is accurate, clear, and appropriate for its section and target style.
