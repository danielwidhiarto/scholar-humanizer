# AI Slop — Patterns to Review

These patterns can signal formulaic or unhelpful prose, but none proves AI authorship. Treat each as a review cue, not a hard ban: revise only when the wording is empty, repetitive, misleading, or inconsistent with the section, evidence, or supplied voice.

---

## Quick Checks

Use these as a first-pass review, then check the surrounding argument and source.

| Check | What to find | How to review |
|-------|-------------|----------------|
| Adverb clusters | Repeated or stacked intensifiers, including -ly words | Remove only empty or redundant modifiers; keep precise, discipline-standard adverbs. No numeric cap. |
| Inanimate subjects | "The data tells us..." or "The study believes..." | Review literal personification or a hidden actor. "The data suggest" and "Results indicate" are standard academic phrasing. |
| Repeated sentence rhythm | Several sentences with the same length or syntax | Vary only when the passage becomes monotonous; do not force variation. |
| Comma-tail cadence | Most sentences end with a comma-attached elaboration: ", indicating that...", ", an approach that...", ", particularly for...", ", with..." | Review the passage: split one tail into its own sentence or drop a redundant one; keep tails that add distinct information. See "Comma-Tail Cadence". |
| Balanced antithesis | Many "X while -ing Y" mirrors in one passage ("degrades accuracy while inflating costs"), or several contrast pivots in one sentence | Review the cluster: keep contrasts that carry real distinctions; rephrase all but the strongest so the two sides are not perfectly mirrored. See "Balanced Antithesis". |
| Dramatic register | Intensified verbs and nominals: "plummets", "slashed", "fail catastrophically", "Dominance of X" | Swap to the plainest verb that preserves the claim and its magnitude; keep dramatis personae that the source supports. See "Dramatic Register". |
| Uniform scaffold cluster | "First/Second/Third" items sharing one sentence shape, or identical connectors opening consecutive paragraphs | Review the whole passage: keep every claim and the listed order; vary sentence shape or drop redundant connectors. A numbered structure itself is kept — see "Numbered Findings and Unnumbered Bullets". |
| Dramatic one-line ending | "This matters." or "This changes everything." | Keep a concise sentence that adds a result or qualification; trim only empty emphasis. |
| Arrow-linked outline | Fragments connected by arrows in narrative text | Convert to complete sentence(s) when prose is intended; preserve meaning and order. Keep intentional diagrams and workflows. |
| Unnumbered bullets in narrative | Related subpoints listed inside running academic prose | Prefer a coherent paragraph when every claim remains clear; keep bullets for independent or scannable items. Preserve numbered findings and ordered steps. |
| Vague declarative | "This is important" without a stated reason | Specify only what the source supports, or remove empty emphasis. |
| Distant narrator | "It should be noted that researchers have found..." | Remove throat-clearing when it adds nothing; retain passive voice when appropriate. |
| Repeated meta-joiners | Paragraphs repeatedly open with "Furthermore" or "Moreover" | Keep useful formal transitions; vary or restructure only if repetition obscures the logic. |
| Repeated Wh-word openers | Several sentences begin with "Which," "Where," "When," or "How" | Review a repetitive cluster; keep grammatical, purposeful openings. |
| Narrative citation template | Three or more close "Author (Year) verb + claim" sentences, or a repeated reporting verb | See `rules/narrative_citation.md`; single sentences and foundational works are not cues. |
| Em/en dash | A dash appears in prose | Follow the writer's sample and target style. Preserve ranges, symbols, math, and file syntax. |

## Optional Diagnostic Checker

When available, `scripts/academic-slop-checker.py <file>` can locate configured review cues and report source line numbers and detected sections. It masks common LaTeX and Markdown syntax, does not edit files, and does not produce an authorship verdict or PASS/FAIL result. Inspect every match in context.

---

## AI Vocabulary Overuse

Some words become formulaic through repetition or vague use. Replace them only when they add no precise meaning; keep technical terms and accurate field-specific uses.

See `references/banned_phrases.md` for phrase-level review cues and context-dependent examples.

---

## Copula Avoidance

Review elaborate constructions that obscure a simple, equivalent statement. Do not simplify if it changes the claim.

**Before:** "The method serves as a foundation for the analysis."
**After:** "The method is the foundation for the analysis."

**Before:** "This finding stands as evidence of the relationship."
**After:** "This finding is evidence of the relationship."

**Before:** "The study boasts a large sample size."
**After:** "The study has a large sample size."

---

## Formulaic Structures

### Arrow-Linked Outlines

Arrow-connected fragments can read like notes or a diagram when the intended output is academic prose. Convert them to complete sentence(s), keeping each item and the relationship or order the source actually expresses. Do not turn association into causation or imply a process sequence when the arrows do not establish one. Keep arrows in diagrams, equations, code, and intentional workflows; if their meaning is unclear, preserve the notation and flag the ambiguity.

### Numbered Findings and Unnumbered Bullets

Keep numbering for enumerated findings, ordered steps, rankings, and items the text needs to reference. Do not change a numbered list into unordered bullets or prose just to vary the format. For related unnumbered bullets in running narrative, prefer a paragraph when the relationship is clear and no claim is lost. Retain bullets for independent points, procedures, criteria, scannability, or when the author or target style prefers them.

### "Not X, but Y" / "Not only X, but also Y"

Review a contrast when it creates a false opposition or adds drama without information. Keep contrasts that distinguish methods, hypotheses, findings, or interpretations.

**Empty contrast — revise if both halves repeat the same point:**

**Before:** "The measure is not only useful, but also valuable."
**After:** "The measure is useful."

**Meaningful contrast — keep:**

"The intervention increased adherence, not overall attendance."

### Uniform Parallel Scaffold

Future-work and limitation passages often enumerate steps in a fully parallel scaffold — "First, X should be investigated. Second, Y should be extended. Third, Z is needed." — where every item shares one sentence shape (problem → modal + passive verb → expected outcome) and one opener. The content is usually sound; the uniform rhythm across many items is the cue.

**Review the cluster, not each sentence:**

- Keep every claim, the listed order, and the numbering itself.
- Break the symmetry where the prose allows: one item can open differently ("The Autorun.K confusion comes first."), two shorter items can merge, and some items can drop the explicit ordinal.
- Removing an item, inventing a detail, or weakening a stated claim is never the fix.

### Comma-Tail Cadence

An elaboration tail — a comma-attached modifier after the main clause (", indicating that X", ", an approach explored in recent work", ", particularly for low-support classes") — is a normal academic construction. The cue is frequency: when most sentences in a passage end this way, the prose takes on a uniform cadence.

**Review the cluster:**

- Keep tails that add distinct information. A Methods parameter tail (", with batch size 32") reports a value, not a cadence tic; Methods parameter sentences stay as written.
- A single sentence doing several reporting jobs (reporting averages, interpreting them, and pointing to a table) can usually be split without losing any claim.
- Split one tail into its own sentence, or drop a tail that repeats what a neighboring sentence already says. Never remove a qualification the source makes.

**Before:** "The survey records weighted averages of 0.97 and 0.98 for all three instruments, indicating that weak items concentrate in a small set of scales, particularly for scales with few questions, an outcome visible in Table 3."
**After:** "The survey records weighted averages of 0.97 and 0.98 for all three instruments. Weak items concentrate in a small set of scales, especially where scales have few questions; Table 3 lists them."

### Balanced Antithesis

Two mirrored clauses of near-identical shape ("degrades accuracy while inflating computing costs", "cutting overhead while maintaining maximal speed", "it is simultaneously the most expensive and the least effective") are a legitimate rhetorical figure. The cue is density: several mirrored antitheses in one passage, or several contrast pivots stacked in a single sentence.

**Review the cluster:**

- Keep the contrast that carries the passage's key distinction; express the others more plainly (subordinate clause, separate sentence, or plain "and").
- Never drop one side of a real trade-off. Both claims survive; only the mirroring is relieved.
- A single antithesis per passage is normal academic rhetoric and is not a cue.

**Before:** "Pruning degrades coverage while inflating per-build latency, and the alternative adds metrics while inflating memory use."
**After:** "Pruning trades a little coverage for higher per-build latency. The alternative raises memory use instead."

### Dramatic Register

Intensified verbs and event nominals — "plummets to", "slashed", "fail catastrophically", "Collapses of", "Dominance of", "Efficiency synergy" — state a real result with more theater than the numbers require. The claims are usually supported; the register is the cue.

**Review:**

- Swap to the plainest verb that preserves the claim and its magnitude: "plummets" → "drops", "slashed" → "cut", "fail catastrophically" → "break down" (keep "collapse" where the source itself defines a collapse).
- Review section-heading-style nominals ("Dominance of execution history.") when they dramatize rather than label; keep them when they are the paper's own established terminology.
- Do not weaken a claim the evidence supports: if the drop is from 0.62 to 0.35, "drops" still tells the truth; the magnitude lives in the numbers, not the verb.

**Before:** "APFDc plummets to 0.3503 — well below random ordering."
**After:** "APFDc drops to 0.3503, below random ordering."

### Overloaded Reporting Sentence

A sentence that performs several reporting jobs at once — reporting values, interpreting them, and pointing to where they live — packs three clauses into one long chain. The claims are usually sound; the density is the cue.

**Review when a sentence stacks all of these:**

- A value statement ("the reports record weighted averages of X and Y")
- An interpretation ("indicating that errors concentrate...")
- A cross-reference ("every family below 1.00 appears in Table 5")

Split it so each claim keeps its own sentence. All numbers, qualifiers, and references survive the split; the table pointer often works better as its own short sentence.

### Forced Triads

Review three-part lists only when the third item is padding or the parallel form is imposed for effect. Keep lists that represent actual categories, measures, or findings.

**Before:** "The study was rigorous, comprehensive, and systematic." (if only systematic is supported)
**After:** "The study was systematic."

### Dramatic Fragmentation

Review stacked fragments when they add emphasis but no distinct information. Keep short sentences that report a result, limitation, or qualification.

**Before:** "The model works. It is reliable. It is valid. It is ready."
**After:** "The model works, is reliable and valid, and is ready."

### Generic "Gap + Contribution" Formula

The gap-plus-contribution sequence can become formulaic when it asserts novelty without evidence. A specific, supported research gap is valid academic content; do not delete it solely because it uses the word "gap."

**Signals to review:**
- "Despite extensive research on X..."
- "Few studies have examined..."
- "This paper addresses this gap..."
- "This study fills a critical gap in the literature..."
- "To the best of our knowledge, this is the first study to..."

**Rule:** State a gap only when supported by the supplied literature or citations. Do not invent novelty, citations, or a contribution; keep a real, specific gap when it helps explain the study.

---

## Signposting and Meta-Commentary

Academic writing uses signposting. Remove it only when it is redundant or contributes no information.

**Review when redundant:**
- "This paper is organized as follows."
- "Let us now turn to..."
- "Having established X, we now examine Y."
- "It is worth noting that..."
- "This section explores..."

**Often useful:**
- "As discussed in Section 3..." (cross-reference)
- "Building on the framework established by..." (context)

---

## Generic Conclusions

Review conclusions that end with vague uplift or repeat an earlier claim.

**Review when no specific content follows:**
- "These findings have important implications for future research."
- "This study contributes to the growing body of literature on..."
- "The future of this field is promising."
- "Exciting opportunities lie ahead."
- "These results pave the way for..."

**Prefer:** A specific implication or direction supported by the source. Do not invent a recommendation or research agenda to make an ending sound concrete.

---

## Filler Phrases

Wordy constructions may be concise without losing meaning. See `references/banned_phrases.md` for review cues and possible alternatives.

---

## Elegant Variation (Synonym Cycling)

Unnecessary synonym changes can make a technical term ambiguous. Prefer consistent terminology when the referent is the same; vary wording only when the meaning remains precise.

**Before:** "The participants completed the survey. The respondents then answered follow-up questions. The subjects were compensated."
**After:** "The participants completed the survey. They then answered follow-up questions. All participants were compensated."

---

## Em and En Dashes

Do not remove dashes mechanically. Preserve an author's established punctuation, numerical ranges, symbols, math, and syntax. If a dash conflicts with supplied journal guidance, revise prose punctuation without changing protected technical spans.

Otherwise, use the writer's sample and target style. Never change a dash inside math, a range, or file syntax as a style edit.

---

## Throat-Clearing and Overstated Tone

Review phrases such as:
- "It is important to note that..."
- "It goes without saying that..."
- "Needless to say..."
- "It is imperative that..."
- "It is crucial to understand..."

Remove them when they merely announce importance or urgency. Keep them only when they carry a specific, supported meaning or match the required register.

---

## Persuasive Authority Tropes

Review these when they create emphasis without an argument:
- "The real question is..."
- "At its core..."
- "What really matters is..."
- "The fundamental issue..."
- "Ultimately..."

---

## Manufactured Punchlines

Review stacked short sentences when they add emphasis but no separate finding. Keep a short sentence that carries a result or qualification.

**Before:** "The model works. It is validated. It is ready. It is here."
**After:** "The model works, is validated, and is ready."

---

## Ranges

Do not call a range false unless the source supports that conclusion.

**Before:** "From students to professionals, the method applies."
**After:** "The method applies to both students and professionals." (if both groups are in scope)

**Before:** "Across a wide range of disciplines..."
**After:** Name the disciplines, or say "across disciplines" only when the source supports that scope.

---

## AI Citation Patterns

Citation form alone does not establish whether a source is genuine or whether a claim is supported. Preserve citation content during rewriting and treat concerns as findings to verify, not facts.

For the "Author (Year) found that..." sentence template — including when a cluster of such sentences merits review — see `rules/narrative_citation.md`.

### Generic Citations Without Synthesis

**Before:** "Smith (2020) found a negative association between social media use and GPA. Jones (2021) reported a similar negative association. Lee (2022) also found a negative relationship."
**After:** "Three studies reported a negative association between social media use and academic performance (Smith, 2020; Jones, 2021; Lee, 2022)."

Synthesize only when the supplied source text establishes a shared finding. Preserve distinctions and citations when results differ or are not described.

### Citation Chains Without Analysis

**Before:** "Smith (2020) studied social media generally. Jones (2021) examined Instagram. Lee (2022) looked at TikTok. Chen (2023) analyzed Twitter."
**After:** "Studies examined social media generally (Smith, 2020) and specific platforms: Instagram (Jones, 2021), TikTok (Lee, 2022), and Twitter (Chen, 2023)."

Group studies only when the source establishes a shared finding. Do not infer a result from a citation title, author, or year.

### Unverified Citations

A citation that appears unfamiliar, recent, or only once is not by itself evidence of fabrication.

Never invent or silently remove a citation. If it cannot be checked against an available source, call it unverified rather than claiming it is false or verified.

### Citation Density

Do not remove citations because a sentence seems over-cited or add citations because a claim seems under-supported. Check the source-to-claim mapping and target style; if evidence is unavailable, flag the issue for the author instead of changing citations or adding statistics.

---

## Final Rule

Do not claim "100% slop" from a phrase match, and do not report that citations are verified unless their sources were checked. Preserve meaning first; revise style only where context supports it.
