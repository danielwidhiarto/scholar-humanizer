# Scholar Humanizer

A Claude Code skill that strips AI-generated patterns from academic writing while preserving scholarly conventions.

## Why

General humanizers ban passive voice, hedging, and formal transitions — all standard in academic writing. This skill knows the difference between "AI slop" and "academic voice."

## Install

```bash
# Claude Code
claude skill add scholar-humanizer

# Or copy SKILL.md and the rules/ directory into your project's .claude/skills/
```

## What It Does

1. **Detects section type** (Abstract, Methods, Discussion, etc.)
2. **Applies section-aware rules** — passive voice is required in Methods, hedging is expected in Discussion
3. **Strips AI patterns** — vocabulary overuse, formulaic structures, filler phrases
4. **Scores the result** — 5 dimensions, 1-10 each, threshold 35/50
5. **Preserves all claims** — never invents or removes factual content

## Section-Aware Rules

| Section | Passive Voice | Hedging | First Person |
|---------|--------------|---------|--------------|
| Abstract | Avoid | Minimal | "We present" OK |
| Introduction | OK | Moderate | Avoid |
| Methods | **Required** | Minimal | "We" OK |
| Results | OK | Moderate | Avoid |
| Discussion | Avoid | **Expected** | "We suggest" OK |
| Conclusion | Avoid | Minimal | "We" OK |

## Scoring Rubric

| Dimension | Question |
|-----------|----------|
| Precision | Specific claims, not vague generalities? |
| Voice | Reads like a researcher, not a chatbot? |
| Flow | Varied sentence structure? |
| Economy | Filler cut, substance kept? |
| Integrity | All claims preserved, nothing fabricated? |

**Threshold: 35/50.** Below = revise.

## Files

```
SKILL.md                      ← Entry point
rules/
  academic_voice.md            ← What to keep (passive voice, hedging, formal tone)
  ai_slop.md                   ← What to remove (AI patterns)
references/
  banned_phrases.md            ← Phrase-level bans
examples/
  before_after.md              ← Concrete rewrites per section
  scoring_examples.md          ← Rubric demonstrations
```

## License

MIT
