# Narrative Citation Pattern — Review Conditions

The template "Author (Year) + reporting verb + claim" — for example, "Smith (2020) found that X" — is standard academic attribution. One or two such sentences are normal in every section and are not a cue on their own. The template matters most in Literature Review / Related Work and Introduction sections, including the system-by-system Related Work sections common in machine learning and computer science papers.

Treat this as a clustering cue: review the group, not each sentence.

---

## When to Flag

Flag the pattern only when at least one of these holds:

1. **Cluster:** three or more sentences with the same template appear close together (same paragraph or adjacent paragraphs).
2. **Repeated verb:** the same reporting verb (found, showed, demonstrated, examined, applied...) is used for several nearby citations.

Fewer than three template sentences with varied verbs is ordinary academic prose. Do not flag it.

---

## How to Review a Cluster

- When the sentences restate one shared finding, they can often be synthesized: "Three studies reported X (A, 2020; B, 2021; C, 2022)." Do this only when the supplied material establishes the shared finding.
- When each sentence describes a distinct contribution, method, or result, the structure may be correct as written. Do not merge sentences whose findings differ, and do not infer a shared result from titles, authors, or years.
- Swapping reporting verbs (found → observed → noted) without changing the structure is cosmetic. Prefer synthesis when it is supported; otherwise keep the sentences.

---

## Foundational Works — Do Not Flag

Describing the introduction of a seminal method, dataset, metric, architecture, or theory is expected and should be kept, even inside a cluster. Signals that a citation is foundational:

- The verb is "introduced," "proposed," "presented," or "developed," and the sentence names the specific artifact the work contributed.
- The paper itself builds on, extends, or compares against that artifact.
- The sentence describes what the work contributed, not a pooled result.

Such sentences usually cannot be synthesized: readers need to know who introduced the method the paper now uses. Keep them unless the surrounding text shows real redundancy.

If it is unclear whether a work is foundational, treat the sentence as ordinary attribution and rely on the cluster and repeated-verb conditions above.

---

## Related Guidance

- `rules/ai_slop.md` — "AI Citation Patterns": synthesis examples and citation-chain review.
- A template match never establishes that a citation is verified, fabricated, or removable; follow the citation rules there.
