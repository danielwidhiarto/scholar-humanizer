# Scholar Humanizer

A portable, harness-neutral agent skill for improving academic prose while preserving scholarly conventions.

## Why

General humanization rules can overcorrect academic writing by removing passive voice, hedging, formal transitions, and discipline-specific terminology. Scholar Humanizer applies section-aware guidance and treats style patterns as review cues, not automatic rewrite commands.

## Install

Use the Skills CLI:

```sh
npx skills add danielwidhiarto/scholar-humanizer
```

To list the skill without installing it:

```sh
npx skills add danielwidhiarto/scholar-humanizer --list
```

The repository was recognized by the CLI as containing the `scholar-humanizer` skill. Manual fallback: clone the repository or copy `SKILL.md`, `rules/`, `references/`, and `examples/` into a project or agent skill location. Also copy both checker files from `scripts/` if you want the optional prose checker in that installation.

### Zero-dependency installer

For a guided install into one or more agent skill folders, clone this repository. The installer uses only the Python standard library and requires Python 3.10 or newer:

```sh
python scripts/install.py --list
python scripts/install.py --scope project
```

The installer detects agent-specific project markers and available CLI commands, then asks which detected agents to target and confirms the planned writes. Shared folders such as `.agents/skills/` are not enough to identify a specific agent, so select one explicitly when needed:

```sh
python scripts/install.py --agent claude-code,codex --scope project --dry-run
python scripts/install.py --agent claude-code,codex --scope project
python scripts/install.py --agent claude-code --scope global
```

Project installs add or update a managed pointer in the relevant instruction file where configured; use `--no-pointer` to skip that. Existing skill folders are skipped unless `--force` is provided; `--force` overwrites only package files and leaves unrelated files in place. Global installs write to the selected user's home directory and do not edit global instruction files. Use `--dry-run` to inspect destinations before writing.

The installer supports these configured destinations. It creates/copies the skill folders; check an agent's current documentation if its skill-discovery paths change.

| Agent | Project folder | User folder |
|-------|----------------|-------------|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex | `.codex/skills/` | `~/.agents/skills/` |
| Antigravity | `.agents/skills/` | `~/.gemini/config/skills/` |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` |
| Cline | `.cline/skills/` | `~/.cline/skills/` |
| OpenCode | `.opencode/skills/` | `~/.config/opencode/skills/` |
| Amp | `.agents/skills/` | `~/.config/agents/skills/` |
| Gemini CLI | `.gemini/skills/` | `~/.gemini/skills/` |
| Hermes | `.hermes/skills/` | `~/.hermes/skills/` |
| GitHub Copilot | `.agents/skills/` | `~/.agents/skills/` |
| Kimi Code | `.agents/skills/` | `~/.agents/skills/` |
| Pi | `.pi/skills/` | `~/.pi/agent/skills/` |

### Optional prose checker

The dependency-free checker reports candidate patterns with source line numbers and a detected section. It does not edit files, verify citations, or decide whether prose is AI-written; inspect every finding in context.

```sh
python scripts/academic-slop-checker.py paper.tex
python scripts/academic-slop-checker.py paper.tex --markdown
```

It accepts UTF-8 `.tex`, `.md`, and `.txt` files. For LaTeX, it masks comments, common math environments, inline/display math, citation keys, labels/references, and common code spans before checking prose. The report is diagnostic, not a PASS/FAIL gate.

Note for ML/CS prose: the checker's copula cue matches "features" only in its verb sense (as in "the module features a novel attention block"). The noun "feature" — as in feature maps, feature extraction, or spatial features — is not flagged. Other word-level cues can still be noisy in ML/CS writing (for example, "robust" for robustness testing, "leverage" for matrix operations); review every finding in context and keep precise technical uses.

## What It Does

1. **Identifies section type** (Abstract, Methods, Discussion, etc.)
2. **Applies section-aware guidance** — Methods defaults to passive voice; Discussion often needs appropriate hedging
3. **Reviews style patterns in context** — vocabulary, formulaic structures, arrow-linked outlines, repetition, comma-tail cadence, and filler are cues, not proof of AI authorship
3b. **Guides Results/Discussion paragraph flow** — a finding-first shape (Finding → Meaning → Support → Implication → Consequence) as a default, with the Support beat written only when the source establishes the prior-work link
4. **Respects academic list structure** — preserves numbered findings and can turn related unnumbered bullets into prose when clarity and meaning are preserved
5. **Supports Audit and Rewrite modes** — audit reports findings without changing the source; rewrite makes minimal prose edits
6. **Protects content and format** — preserves claims, citations, numbers, and non-prose syntax, including LaTeX commands and math
7. **Uses an advisory rubric** — five dimensions, 1-10 each; 35/50 is a revision guide, not an objective score or detector result

Humanization is for clarity and authorial voice, not evading AI detectors.

## Audit and Rewrite

- **Audit:** No edits. Report findings with excerpts and reasons; include line numbers only when directly available.
- **Rewrite:** Make the smallest supported changes and provide the final text with a brief summary.
- If asked to rewrite a `.tex` file, change prose only. Preserve commands, math, environments (`align`, `gather`), citation keys, labels/references, values, and escaped characters such as `\%`. Treat uncertain syntax as protected.
- Do not invent findings, citations, methods, limitations, or recommendations to make writing sound more specific. Never claim a citation is verified unless its source was checked.

## Section-Aware Rules

| Section | Passive Voice | Hedging | First Person |
|---------|--------------|---------|--------------|
| Abstract | Avoid | Minimal | "We present" OK |
| Introduction | OK | Moderate | Avoid |
| Literature Review | OK | Moderate | Avoid |
| Methods | **Required** | Minimal | "We" OK |
| Results | OK | Moderate | Avoid |

In Results (when interpretation is permitted) and Discussion, prefer a finding-first paragraph flow — Finding → Meaning → Support → Implication → Consequence — as a default shape, not a template: beats may be skipped, and the Support beat is written only when the supplied material establishes the prior-work link. Uniform scaffolds ("First/Second/Third" items sharing one sentence shape) are reviewed as whole-passage clusters; claims and order are always kept.
| Discussion | Avoid | **Expected** | "We suggest" OK |
| Conclusion | Avoid | Minimal | "We" OK |

Follow supplied author samples and journal guidance when available. The table is a default, not a universal style mandate.

## Scoring Rubric

The rubric is adapted for academic writing from [stop-slop](https://github.com/hardikpandya/stop-slop). Scores are qualitative editorial guidance.

| Dimension | Question |
|-----------|----------|
| Precision | Are claims specific rather than vague? |
| Voice | Does the prose fit the researcher, field, and section? |
| Flow | Does sentence structure support the argument? |
| Economy | Is filler reduced without losing substance? |
| Integrity | Are source claims preserved without fabrication? |

**35/50 is a revision guide.** A score does not establish authorship, prove quality objectively, or predict an AI-detector result.

## Files

```text
SKILL.md                      # Entry point and source of truth
rules/
  academic_voice.md           # Scholarly conventions to preserve
  ai_slop.md                  # Contextual pattern-review guidance
  narrative_citation.md       # Cluster conditions for "Author (Year) found..." templates
references/
  banned_phrases.md           # Phrase-level review cues
examples/
  before_after.md             # Rewrites and regression examples
  scoring_examples.md         # Rubric demonstrations
scripts/
  install.py                  # Optional multi-agent skill installer
  academic-slop-checker.py    # Optional no-edit pattern checker
```

## Background & Credits

- [humanizer](https://github.com/blader/humanizer) by Siqi Chen builds on [Wikipedia's "Signs of AI writing" guide](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). The version reviewed for this update lists 26 pattern categories; Scholar Humanizer adapts patterns as contextual cues rather than universal bans.
- [stop-slop](https://github.com/hardikpandya/stop-slop) by Hardik Pandya has 8 Core Rules in the reviewed `SKILL.md`. Scholar Humanizer adapts its five-dimension scoring idea for academic prose without importing generic voice rules wholesale.
- [anti-slop](https://github.com/miqdadbadjuber/anti-slop) informed the distinction between hard integrity constraints and contextual quality review. Scholar Humanizer's Audit/Rewrite modes and final review checks are local adaptations, not names or features attributed to that project.

Section-aware rules preserve academic conventions where general style heuristics may not apply. Passive voice is required by the Methods default unless supplied target guidance says otherwise; hedging is common in Discussion, and formal transitions may be useful throughout.

## License

MIT
