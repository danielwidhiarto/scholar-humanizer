---
name: scholar-humanizer
description: Strip AI-generated patterns from academic writing while preserving scholarly conventions like passive voice and hedging.
license: MIT
metadata:
  version: "1.0.0"
---

# Scholar Humanizer

Strip AI-generated patterns from academic writing while preserving scholarly conventions. Passive voice, hedging, and formal transitions are features, not bugs.

---

## When to Trigger

- User pastes academic text for review
- User points at a `.tex`, `.md`, `.docx`, or `.txt` file
- User says "humanize," "de-AI," or "make this sound human"

---

## Process

### 1. Detect Section Type

Identify which academic section the text belongs to. If multiple sections, process each separately.

| Section | Signals |
|---------|---------|
| Abstract | 150-300 words, standalone summary, keywords |
| Introduction | Background → gap → contribution structure |
| Literature Review | Dense citations, "argues that," "found that" |
| Methods | Past tense, materials, procedures, "was/were collected" |
| Results | Data presentation, "showed," "indicated," figures |
| Discussion | Interpretation, limitations, "suggests that" |
| Conclusion | Summary, future work, "this paper has shown" |

### 2. Apply Section-Specific Rules

Load `rules/academic_voice.md` for the detected section. These override general humanization rules.

### 3. Detect and Remove AI Patterns

Scan for patterns in `rules/ai_slop.md` and phrases in `references/banned_phrases.md`. Remove them.

### 4. Rewrite

Preserve every claim. Never invent facts. Match the academic register of the field.

### 5. Score

Rate across five dimensions (1-10 each):

| Dimension | Question |
|-----------|----------|
| **Precision** | Specific claims, not vague generalities? |
| **Voice** | Reads like a researcher, not a chatbot? |
| **Flow** | Varied sentence structure, not metronomic? |
| **Economy** | Filler cut, substance kept? |
| **Integrity** | All original claims preserved, nothing fabricated? |

**Threshold: 35/50.** Below = revise and re-score.

### 6. Output

Deliver:
1. The humanized text
2. Change summary (what was removed and why)
3. Rubric score with dimension breakdown
4. If below 35: revised version + new score

---

## Section-Aware Rules (Override Table)

These take precedence over general rules:

| Rule | Abstract | Introduction | Literature Review | Methods | Results | Discussion | Conclusion |
|------|----------|-------------|-------------------|---------|---------|------------|------------|
| Passive voice | Avoid | OK | OK | **Required** | OK | Avoid | Avoid |
| Hedging | Minimal | Moderate | Moderate | Minimal | Moderate | **Expected** | Minimal |
| First person | "We present" OK | Avoid | Avoid | "We" OK | Avoid | "We suggest" OK | "We" OK |
| Formality | High | High | High | Very High | High | Moderate-High | High |
| Transitions | Minimal | Formal | Formal | Minimal | Formal | Flexible | Minimal |

---

## Core Principles

1. **Academic conventions are not AI-isms.** Passive voice in Methods is standard. Hedging in Discussion is expected. Don't strip them.
2. **Preserve all claims.** Never add, remove, or distort factual content. (From humanizer's no-fabrication rule.)
3. **Section-aware.** The same sentence may be fine in Methods but wrong in Abstract.
4. **Cluster detection.** One "however" is fine. Three in a paragraph is a pattern. (From humanizer.)
5. **Score honestly.** The rubric catches what your eye misses. (From stop-slop.)

---

## Files

- `rules/academic_voice.md` — what to keep per section
- `rules/ai_slop.md` — what to remove
- `references/banned_phrases.md` — phrase-level bans
- `examples/before_after.md` — concrete rewrites
- `examples/scoring_examples.md` — rubric demonstrations
