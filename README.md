# Scholar Humanizer

A Claude Code skill that strips AI-generated patterns from academic writing while preserving scholarly conventions.

## Why

General humanizers ban passive voice, hedging, and formal transitions — all standard in academic writing. This skill knows the difference between "AI slop" and "academic voice."

## Install

Copy-paste the repo link into your AI agent. That's it.

**Claude Code:**
```
Clone https://github.com/danielwidhiarto/scholar-humanizer and use SKILL.md as a skill.
```

**Cursor / Windsurf / Other agents:**
```
Read the rules from https://github.com/danielwidhiarto/scholar-humanizer — follow SKILL.md, rules/, and references/ when humanizing my academic writing.
```

**Manual:** Clone or copy `SKILL.md`, `rules/`, `references/`, and `examples/` into your project.

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

Adapted from [stop-slop](https://github.com/hardikpandya/stop-slop)'s scoring system (5 dimensions, 1-10, threshold 35/50), recalibrated for academic writing.

| Dimension | Question | stop-slop equivalent |
|-----------|----------|---------------------|
| Precision | Specific claims, not vague generalities? | Directness |
| Voice | Reads like a researcher, not a chatbot? | Authenticity |
| Flow | Varied sentence structure? | Rhythm |
| Economy | Filler cut, substance kept? | Density |
| Integrity | All claims preserved, nothing fabricated? | Trust |

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

## Background & Credits

This skill exists because general humanizers are too aggressive for academic writing.

[stop-slop](https://github.com/hardikpandya/stop-slop) by Hardik Pandya — taught us to score writing quality with a rubric (5 dimensions, 1-10, threshold 35/50) and to systematically detect AI phrases and structures. Our scoring system is adapted from stop-slop's approach.

[humanizer](https://github.com/blader/humanizer) by Siqi Chen — taught us to detect 33 AI writing patterns, calibrate voice from user samples, and enforce a no-fabrication rule (never invent facts during rewrite). Built on [Wikipedia's "Signs of AI writing" guide](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).

**The problem both share:** they ban passive voice, hedging, and formal transitions — patterns that are standard (even required) in academic writing. A Methods section that says "The samples were collected" is correct. A general humanizer would rewrite it to "We collected the samples" and break academic convention.

**What this skill adds:** section-aware rules that know the difference between AI slop and academic voice. Passive voice is required in Methods. Hedging is expected in Discussion. Formal transitions are standard everywhere. The skill only removes actual AI-isms, not scholarly conventions.

## License

MIT
