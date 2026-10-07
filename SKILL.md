---
name: scholar-humanizer
description: Improve academic prose while preserving scholarly conventions such as passive voice and hedging.
license: MIT
metadata:
  version: "1.4.2"
---

# Scholar Humanizer

Improve academic prose while preserving scholarly conventions. Passive voice, hedging, and formal transitions are not AI tells by themselves.

---

## When to Trigger

- User pastes academic text for review
- User points at a `.tex`, `.md`, `.docx`, or `.txt` file
- User says "humanize," "de-AI," or "make this sound human"

## Operating Principles

- Improve clarity and the writer's voice; do not optimize text to evade AI detectors.
- Treat pattern matches as diagnostic cues, not proof of AI authorship or automatic rewrite instructions.
- Follow section conventions, supplied writing samples, and user-provided target guidance before general heuristics.

---

## Process

### 1. Select a Mode

- **Audit:** Do not edit the source. Report actionable findings with a short excerpt, reason, and optional suggestion. Give line numbers only when they are directly available from the source.
- **Rewrite:** Make the smallest prose changes that meet the request, then provide the final text and a concise change summary.
- Infer the mode when intent is clear. If the choice would materially change the result, ask once rather than asking by default.

For an in-place file rewrite, write only the final prose-edited file and summarize changes in the response. Never modify a file in Audit mode.

### 2. Calibrate Voice and Direction

If the user provides 2-3 paragraphs of their own writing, analyze before rewriting:
- Sentence length range and average
- Vocabulary level and field-specific terms
- Punctuation habits (Oxford comma, semicolons, parenthetical dashes)
- Transition preferences (formal vs. implicit)
- First-person usage and formality register

The user's sample and supplied journal or style guidance **outrank** general style heuristics. Do not invent a journal profile or assume a field has one universal style. If no direction is supplied, use the section-aware defaults.

### 3. Detect Section Type

Identify which academic section the text belongs to. If multiple sections, process each separately.

| Section | Signals |
|---------|---------|
| Abstract | Standalone summary, methods and key findings |
| Introduction | Background, research question, and contribution |
| Literature Review | Synthesis of prior work and citations |
| Methods | Materials, procedures, and analysis |
| Results | Findings, data presentation, and figures |
| Discussion | Interpretation, limitations, and implications |
| Conclusion | Synthesis and future directions |

### 4. Review Patterns

Load `rules/academic_voice.md`, `rules/ai_slop.md`, `rules/narrative_citation.md`, and `references/banned_phrases.md`. Prioritize repeated or high-signal patterns, but judge each in context; one phrase, contrast, short sentence, adverb, hedge, transition, or dash is not a verdict.

- In Results and Discussion, prefer a finding-first paragraph flow — Finding → Meaning → Support → Implication → Consequence — as a default shape, not a template; write the Support beat only when supplied material establishes the prior-work link (see `rules/academic_voice.md`). Review uniform scaffolds — "First/Second/Third" items sharing one sentence shape, or identical connectors opening consecutive paragraphs — as whole-passage clusters, keeping every claim and the listed order. Review a passage where most sentences end with a comma-attached elaboration (", indicating that...") as a cadence cluster: split one tail into its own sentence where it helps, keep tails that add distinct information, and keep Methods hyperparameter sentences intact (see `rules/ai_slop.md`). Review stacked mirrored antitheses ("X while -ing Y") and intensified verbs ("plummets", "slashed") as register clusters: keep every claim and magnitude, relieve the symmetry, and use the plainest verb that still tells the truth.
- Keep contrasts that distinguish methods, hypotheses, results, or interpretations. Preserve numbered findings and ordered steps. In running academic prose, prefer paragraphs to related unnumbered bullets only when all claims remain clear; keep bullets for independent items, useful scanning, or required styles.
- When arrow-separated outline fragments are used as prose, convert them to complete sentence(s), preserving listed order and relationships without inventing causality. Retain arrows in diagrams, formulas, code, and intentional workflows.
- Revise a pattern only when it is empty, repetitive, misleading, or inconsistent with the section or supplied voice.
- Never apply universal active-voice, adverb, hedging, transition, or dash bans.
- If the optional `scripts/academic-slop-checker.py` is available, use it only to locate candidates; review each finding in context. It does not edit files or determine authorship.

### 5. Protect Integrity and Format

- Preserve claims, facts, names, dates, numbers, units, uncertainty, and citations. Do not add, remove, or change them without support in the provided material and user instructions.
- For `.tex`, edit prose only. Preserve commands, environments, math, citation keys (including duplicates), labels, references, and escaped syntax such as `\%`. Protect inline and display math, including `align` and `gather`.
- For every format, preserve code, metadata/frontmatter, data, markup, link targets, and other non-prose content. If a span might be syntax, leave it unchanged and report the uncertainty rather than guessing.
- Never say a citation was verified unless its source was available and checked.
- In examples or rewrites, do not invent methods, results, citations, limitations, or other specifics to make prose sound more concrete.

### 6. Run the Final Checks

- **Integrity — hard gate:** Compare source and output. Do not claim PASS when a protected claim or span cannot be checked; preserve it and report what remains uncertain.
- **Pattern review — diagnostic:** Report relevant patterns with context. Do not aim for a zero-match or "zero banned words" result.
- **Section and voice conformance:** Check the section matrix, writing sample, and target guidance that are actually available.
- **Quality review — advisory:** Use the rubric below as editorial guidance, not as evidence about authorship or detector results.

### 7. Score (Advisory)

Rate across five dimensions (1-10 each):

| Dimension | Question |
|-----------|----------|
| **Precision** | Specific claims, not vague generalities? |
| **Voice** | Reads like a researcher in the target field and section? |
| **Flow** | Sentence structure supports the argument? |
| **Economy** | Filler cut, substance kept? |
| **Integrity** | Source claims preserved, nothing fabricated? |

**35/50 is a revision guide, not an objective measure.** If a rewrite scores below 35, review and revise where needed; never distort accurate content just to raise a score. A score does not prove human authorship or predict AI-detector results.

### 8. Output

- **Audit:** Findings, supporting excerpts, reasons, and suggestions; do not provide a full rewrite unless requested.
- **Rewrite:** Final text and a brief change summary. Include the five-dimension score when useful; if below 35, revise where warranted and report the updated score.

---

## Section-Aware Rules (Override Table)

These guide editing; follow more specific user or journal instructions when supplied.

| Rule | Abstract | Introduction | Literature Review | Methods | Results | Discussion | Conclusion |
|------|----------|-------------|-------------------|---------|---------|------------|------------|
| Passive voice | Avoid | OK | OK | **Required** | OK | Avoid | Avoid |
| Hedging | Minimal | Moderate | Moderate | Minimal | Moderate | **Expected** | Minimal |
| First person | "We present" OK | Avoid | Avoid | "We" OK | Avoid | "We suggest" OK | "We" OK |
| Formality | High | High | High | Very High | High | Moderate-High | High |
| Transitions | Minimal | Formal | Formal | Minimal | Formal | Flexible | Minimal |

---

## Core Principles

1. **Academic conventions are not AI-isms.** Preserve passive voice in Methods, appropriate hedging, formal transitions, and precise terminology.
2. **Protect integrity.** Do not invent or distort factual or technical content.
3. **Stay section-aware.** The same construction may be appropriate in Methods and distracting in an Abstract.
4. **Review clusters, not isolated tokens.** A repeated pattern may merit revision; a single occurrence may be correct.
5. **Score cautiously.** The rubric is qualitative guidance, not objective evidence.

---

## Files

- `rules/academic_voice.md` — what to keep per section
- `rules/ai_slop.md` — patterns to review in context
- `rules/narrative_citation.md` — when clustered "Author (Year) found..." templates merit review
- `references/banned_phrases.md` — phrase-level review cues
- `examples/before_after.md` — concrete rewrites and regression examples
- `examples/scoring_examples.md` — rubric demonstrations
- `scripts/academic-slop-checker.py` — optional diagnostic scan; findings are not verdicts
