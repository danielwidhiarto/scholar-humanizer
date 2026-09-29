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

The repository was recognized by the CLI as containing the `scholar-humanizer` skill. Manual fallback: clone the repository or copy `SKILL.md`, `rules/`, `references/`, and `examples/` into a project or agent skill location.

## What It Does

1. **Identifies section type** (Abstract, Methods, Discussion, etc.)
2. **Applies section-aware guidance** — Methods defaults to passive voice; Discussion often needs appropriate hedging
3. **Reviews style patterns in context** — vocabulary, formulaic structures, arrow-linked outlines, repetition, and filler are cues, not proof of AI authorship
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
references/
  banned_phrases.md           # Phrase-level review cues
examples/
  before_after.md             # Rewrites and regression examples
  scoring_examples.md         # Rubric demonstrations
```

## Background & Credits

- [humanizer](https://github.com/blader/humanizer) by Siqi Chen builds on [Wikipedia's "Signs of AI writing" guide](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). The version reviewed for this update lists 26 pattern categories; Scholar Humanizer adapts patterns as contextual cues rather than universal bans.
- [stop-slop](https://github.com/hardikpandya/stop-slop) by Hardik Pandya has 8 Core Rules in the reviewed `SKILL.md`. Scholar Humanizer adapts its five-dimension scoring idea for academic prose without importing generic voice rules wholesale.
- [anti-slop](https://github.com/miqdadbadjuber/anti-slop) informed the distinction between hard integrity constraints and contextual quality review. Scholar Humanizer's Audit/Rewrite modes and final review checks are local adaptations, not names or features attributed to that project.

Section-aware rules preserve academic conventions where general style heuristics may not apply. Passive voice is required by the Methods default unless supplied target guidance says otherwise; hedging is common in Discussion, and formal transitions may be useful throughout.

## License

MIT
