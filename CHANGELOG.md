# Changelog

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
- .claude-plugin/ — Claude Code plugin manifest and marketplace entry
- agents/openai.yaml — OpenAI-compatible agent config
- scripts/validate-package.py — package validation
- .github/workflows/validate.yml — CI validation

### Inspired by
- [stop-slop](https://github.com/hardikpandya/stop-slop) by Hardik Pandya — scoring rubric approach, phrase/structure detection
- [humanizer](https://github.com/blader/humanizer) by Siqi Chen — 33 pattern categories, voice calibration, no-fabrication rule, audit loop
