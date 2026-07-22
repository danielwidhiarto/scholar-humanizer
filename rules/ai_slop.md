# AI Slop — Patterns to Remove

These patterns signal AI-generated text. Remove them from academic writing.

---

## Quick Checks

Fast first-pass heuristics. Run these before the detailed pattern scan. (Adapted from stop-slop.)

| Check | What to find | Fix |
|-------|-------------|-----|
| Adverb density | Count -ly words per paragraph. More than 2 is a pattern. | Kill all adverbs except discipline-standard ones ("significantly" in stats is OK). |
| Inanimate subject + human verb | "The study argues," "The paper claims," "The data suggest" | Name the researcher or use "Results show," "Data indicate." |
| Three same-length sentences in a row | Metronomic rhythm | Break one sentence's length — shorten or combine. |
| Paragraph ending on punchy one-liner | "This is significant." "This matters." "This changes everything." | Delete or merge into the preceding sentence. |
| Vague declarative | "This is important," "The implications are significant," "This is noteworthy" | Name the specific implication or delete. |
| Distant narrator | "It should be noted that researchers have found..." | State directly: "Researchers found..." |
| Meta-joiners as paragraph openers | "Furthermore," "Moreover," "Additionally" starting every paragraph | Vary openers: start with the subject, a question, or a concrete detail. |
| Wh- word sentence openers | Excessive "Which," "Where," "When," "How" starters | Lead with subject or verb instead. |
| Em dash present | Any em dash (—) or en dash (–) | Replace with comma, parentheses, colon, or period. |

---

## AI Vocabulary Overuse

LLMs favor specific "smart-sounding" words far more than human writers. Replace with plain equivalents.

**Always remove:** See `references/banned_phrases.md` → "AI Vocabulary" section for the full kill list with replacements.

**Context-dependent:** See `references/banned_phrases.md` → "Context-Dependent" section for phrases that may be acceptable in some academic contexts.

---

## Copula Avoidance

AI replaces simple "is/are" with elaborate constructions.

**Before:** "The method serves as a foundation for the analysis."
**After:** "The method is the foundation for the analysis."

**Before:** "This finding stands as evidence of the relationship."
**After:** "This finding is evidence of the relationship."

**Before:** "The study boasts a large sample size."
**After:** "The study has a large sample size."

---

## Formulaic Structures

### "Not X, but Y" / "Not only X, but also Y"
AI overuses contrast patterns. Just state the point.

**Before:** "This is not merely a theoretical contribution, but a practical framework for implementation."
**After:** "This is a practical framework for implementation."

### Rule of Three
AI forces ideas into triplets. Break them or keep only what matters.

**Before:** "The study was rigorous, comprehensive, and systematic."
**After:** "The study was systematic." (or "The study was rigorous and systematic" if both are true)

### Dramatic Fragmentation
Short punchy sentences stacked for false gravitas.

**Before:** "The model works. It is reliable. It is valid. It is ready."
**After:** "The model is reliable and valid."

### The "Gap + Contribution" Formula

The single most common AI academic writing structure. Nearly every AI-generated introduction follows this template:

**Before:** "Despite extensive research on social media, few studies have examined its impact on academic performance among university students. This paper addresses this gap by proposing a novel framework for understanding this relationship."

**After:** State what you actually did and why it matters. "We measured the relationship between daily social media use and GPA among 342 university students, focusing on study habits as a mediator."

**Signals:**
- "Despite extensive research on X..."
- "Few studies have examined..."
- "This paper addresses this gap..."
- "This study fills a critical gap in the literature..."
- "To the best of our knowledge, this is the first study to..."

**Rule:** If the "gap" is real, name the specific missing work. If it's not real, don't invent it. Never use the word "gap" — just state your contribution.

---

## Signposting and Meta-Commentary

Academic writing has some signposting, but AI overdoes it.

**Remove:**
- "This paper is organized as follows." (Let the structure speak for itself.)
- "Let us now turn to..." (Just turn to it.)
- "Having established X, we now examine Y." (Just examine Y.)
- "It is worth noting that..." (If it's worth noting, just note it.)
- "This section explores..." (Just explore it.)

**Keep (section-specific):**
- "As discussed in Section 3..." (Cross-references are useful.)
- "Building on the framework established by..." (Contextualizes contribution.)

---

## Generic Conclusions

AI ends sections and papers with vague uplift.

**Remove:**
- "These findings have important implications for future research."
- "This study contributes to the growing body of literature on..."
- "The future of this field is promising."
- "Exciting opportunities lie ahead."
- "These results pave the way for..."

**Replace with:** The specific implication, contribution, or opportunity. If you can't name it, delete the sentence.

---

## Filler Phrases

Wordy constructions that add nothing. See `references/banned_phrases.md` → "Filler Constructions" for the full list with replacements.

---

## Elegant Variation (Synonym Cycling)

AI swaps repeated nouns with synonyms to avoid repetition. This confuses readers.

**Before:** "The participants completed the survey. The respondents then answered follow-up questions. The subjects were compensated."
**After:** "The participants completed the survey. They then answered follow-up questions. All participants were compensated."

Use the same term throughout. Consistency aids comprehension.

---

## Em Dashes

Hard ban in academic writing. Replace with:

- Comma: "The method — which was validated — produced..." → "The method, which was validated, produced..."
- Parentheses: "The results — shown in Table 1 — indicate..." → "The results (shown in Table 1) indicate..."
- Colon: "One factor stood out — consistency." → "One factor stood out: consistency."
- Period: Split into two sentences.

**Exception:** If the user's own writing sample uses em dashes consistently, match their style.

---

## Sycophantic / Servile Tone

**Remove:**
- "It is important to note that..."
- "It goes without saying that..."
- "Needless to say..."
- "It is imperative that..."
- "It is crucial to understand..."

If it's important, state it. Don't announce its importance.

---

## Persuasive Authority Tropes

**Remove:**
- "The real question is..." (Just ask the question.)
- "At its core..." (Just state the core point.)
- "What really matters is..." (Just state what matters.)
- "The fundamental issue..." (Just name the issue.)
- "Ultimately..." (Usually filler in academic writing.)

---

## Manufactured Punchlines

Stacked short sentences for false emphasis.

**Before:** "The model works. It is validated. It is ready. It is here."
**After:** "The validated model is ready for deployment."

---

## False Ranges

**Before:** "From students to professionals, the method applies."
**After:** "The method applies to both students and professionals."

**Before:** "Across a wide range of disciplines..."
**After:** Name the disciplines, or say "across disciplines" without the filler adjective.

---

## AI Citation Patterns

AI generates distinctive citation patterns that signal machine writing.

### Generic Citations Without Synthesis
**Before:** "Smith (2020) found that social media affects students. Jones (2021) found similar results. Lee (2022) also found a relationship."
**After:** "Multiple studies converge on a negative relationship between social media use and academic performance (Smith, 2020; Jones, 2021; Lee, 2022), though the mechanisms differ."

**Rule:** Citations should synthesize, not list. If three studies found the same thing, say so in one sentence.

### Citation Chains Without Analysis
**Before:** "Smith (2020) studied social media. Jones (2021) examined Instagram. Lee (2022) looked at TikTok. Chen (2023) analyzed Twitter."
**After:** "Research has examined platform-specific effects, with studies on Instagram (Jones, 2021), TikTok (Lee, 2022), and Twitter (Chen, 2023) each finding distinct usage patterns."

**Rule:** Group citations by finding, not by author. Don't narrate a bibliography.

### Fabricated Citations
AI often generates real author names with fake years, titles, or journals. Signs:
- Citation appears only once and is never discussed again
- The finding attributed to the citation is suspiciously convenient
- The year is suspiciously recent (2023-2024)
- No DOI or URL provided

**Rule:** If you cannot verify a citation exists, flag it for the user. Never fabricate citations during rewrite.

### Over-Citation
**Before:** "Social media is widely used (Smith, 2020). Students spend time on platforms (Jones, 2021). This affects grades (Lee, 2022)."
**After:** "Social media use among students is associated with lower grades (Lee, 2022)."

**Rule:** Common knowledge doesn't need citation. Cite claims that are specific, surprising, or contested.

### Under-Citation
**Before:** "Social media clearly harms academic performance."
**After:** "Social media use is negatively associated with academic performance (r = -0.34, p < 0.01; Lee, 2022)."

**Rule:** Specific claims need specific evidence. If you state a finding, cite it.
