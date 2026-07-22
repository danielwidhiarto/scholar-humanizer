# Changelog

## 1.1.0 — 2026-07-22

### Added

**SKILL.md process improvements:**
- Voice calibration step (from humanizer): analyze user's writing sample before rewriting
- Audit step: check for fabrication, voice match, remaining AI-isms, false positives
- Quick checks reference in step 4

**rules/ai_slop.md — new patterns:**
- Quick checks (9 heuristics from stop-slop): adverb density, inanimate subject + human verb, 3 same-length sentences, paragraph ending punchy one-liner, vague declarative, distant narrator, meta-joiners, Wh- word openers, em dash
- "Gap + contribution" formula detection: the most common AI academic structure
- AI citation pattern detection: generic citations, citation chains, fabricated references, over-citation, under-citation

**rules/academic_voice.md — new section:**
- False positives: what NOT to flag (bullet points, short paragraphs, formal tone, jargon, long sentences, etc.)

**Examples — new sections:**
- Literature Review before/after example
- Results before/after example
- Literature Review scoring example (AI: 16/50, Humanized: 42/50)
- Results scoring example (AI: 20/50, Humanized: 44/50)

### Changed

**Consolidated redundancy:**
- `rules/ai_slop.md` filler phrases table → cross-reference to `references/banned_phrases.md`
- `rules/ai_slop.md` AI vocabulary kill list → cross-reference to `references/banned_phrases.md`

## 1.0.0 — 2026-07-22

### Added

**Core skill (SKILL.md)**
- Section-aware humanization (Abstract, Introduction, Literature Review, Methods, Results, Discussion, Conclusion)
- Scoring rubric: Precision, Voice, Flow, Economy, Integrity (5 dimensions, 1-10 each, threshold 35/50)
- Passive voice preservation in Methods, hedging preservation in Discussion
- No-fabrication rule: rewrites never invent facts

**Rules**
- `rules/academic_voice.md` — patterns to keep per section (passive voice, hedging, formal transitions, discipline terminology)
- `rules/ai_slop.md` — patterns to remove (AI vocabulary, copula avoidance, formulaic structures, signposting, filler phrases, em dashes, sycophantic tone)

**References**
- `references/banned_phrases.md` — phrase-level bans split into always-remove and context-dependent

**Examples**
- `examples/before_after.md` — concrete rewrites for Abstract, Introduction, Methods, Discussion, Conclusion
- `examples/scoring_examples.md` — rubric demonstrations with scored samples

**Infrastructure**
- AGENTS.md — agent guidance
- scripts/validate-package.py — package validation
- .github/workflows/validate.yml — CI validation

### Background

This project was born from combining two existing AI-writing humanizers:

- **[stop-slop](https://github.com/hardikpandya/stop-slop)** by Hardik Pandya — scoring rubric (5 dimensions × 1-10, threshold 35/50), banned phrases list, structural pattern detection. We adapted the scoring system directly: Precision←Directness, Voice←Authenticity, Flow←Rhythm, Economy←Density, Integrity←Trust.
- **[humanizer](https://github.com/blader/humanizer)** by Siqi Chen (built on [Wikipedia's "Signs of AI writing" guide](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)) — 33 pattern categories, voice calibration from user samples, no-fabrication rule, audit-rewrite loop. We borrowed the pattern detection approach and the no-fabrication principle.

Both tools are excellent for general prose, but they share one critical flaw for academic writing: they ban passive voice, hedging, and formal transitions — all standard in scholarly work. This skill fixes that with section-aware rules.
