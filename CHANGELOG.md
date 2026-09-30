# Changelog

## 1.3.0 — 2026-09-29

### Added

- Added `rules/narrative_citation.md`: cluster conditions for reviewing "Author (Year) + reporting verb + claim" sentences. Flag only clusters of three or more close template sentences or repeated reporting verbs; foundational works (introduced/proposed + named artifact) are kept. Motivated by ML/CS related-work sections.
- Added regression tests and before/after examples for the narrative citation template and for "feature" noun/verb disambiguation.

### Changed

- Tightened the checker's copula cue: "features" now matches only its verb sense ("features a novel module"); the ML noun "feature" (feature maps, feature extraction, spatial features, "features are extracted") is no longer flagged. Documented remaining ML/CS noise in the README checker section.
- Registered the new rule file in SKILL.md, `rules/ai_slop.md` (Quick Checks row + citation cross-reference), README, AGENTS.md, the installer payload (via the `rules/` directory), and package validation.

## 1.2.0 — 2026-09-29

### Changed

- Reframed AI-writing patterns and phrase lists as contextual review cues, not universal bans or proof of AI authorship.
- Clarified section-aware passive voice, hedging, transitions, meaningful contrasts, lists, short results, and dash usage.
- Added contextual conversion of arrow-linked outlines into prose while preserving intentional diagrams and workflows.
- Preserved numbering for findings and ordered steps; related unnumbered bullets in narrative can become paragraphs when clarity and claim integrity are maintained.
- Added Audit and Rewrite modes, integrity and quality review gates, and guidance against AI-detector evasion.
- Added prose-only LaTeX protections for math, commands, environments, citations, labels/references, values, and escaped symbols.
- Reworked examples to avoid unsupported facts and added regression cases for academic false positives and protected LaTeX.
- Clarified the scoring rubric as qualitative guidance; 35/50 is a revision prompt, not objective evidence.
- Made README and installation language harness-neutral; documented the Skills CLI after it recognized the repository's skill.
- Updated source attribution: the reviewed humanizer version lists 26 pattern categories, stop-slop has 8 Core Rules, and Scholar Humanizer's modes and review gates are local adaptations.

### Added

- Added `scripts/install.py`, a zero-dependency installer for the 12 configured agent skill directories. It supports project/global scope, detection hints, explicit selection, dry runs, guarded overwrite, and managed project pointers where configured.
- Added `scripts/academic-slop-checker.py` with section-aware, line-numbered diagnostic findings and optional Markdown output. It masks common LaTeX math, commands, citations, comments, and code spans; it never edits input or reports PASS/FAIL.
- Added standard-library regression tests for installer safety and checker behavior, and wired them into package validation and CI.

### Scope notes

- Installer paths are configured compatibility targets. Directory-copy behavior is tested; automatic skill discovery by every agent runtime is not claimed as integration-tested.
- The checker reports candidate patterns only. It does not verify citations, infer AI authorship, or provide Overleaf-specific navigation.

## 1.1.0 — 2026-07-22

### Added

**SKILL.md process improvements:**
- Voice calibration step (from humanizer): analyze user's writing sample before rewriting
- Audit step: check for fabrication, voice match, remaining AI-isms, false positives
- Quick checks reference in step 4

**rules/ai_slop.md — new patterns:**
- Quick checks (9 local heuristics adapted from stop-slop): adverb density, inanimate subject + human verb, 3 same-length sentences, paragraph ending punchy one-liner, vague declarative, distant narrator, meta-joiners, Wh- word openers, em dash
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
- `references/banned_phrases.md` — initial phrase list, then split into always-remove and context-dependent sections

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
- **[humanizer](https://github.com/blader/humanizer)** by Siqi Chen (built on [Wikipedia's "Signs of AI writing" guide](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)) — the version referenced in the 1.0.0 notes listed 33 pattern categories; the version reviewed for v1.2.0 lists 26. Its pattern catalog, voice calibration, and no-fabrication principle informed this skill.

The sources differ in scope and guidance. Scholar Humanizer does not attribute one blanket style rule to all of them; it applies local section-aware rules so that passive voice, hedging, and formal transitions are judged in academic context.
