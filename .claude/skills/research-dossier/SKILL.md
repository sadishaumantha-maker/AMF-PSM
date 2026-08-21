---
name: research-dossier
description: Produce a deep, evidence-graded research dossier for a GitHub issue — what it actually means, what already exists, what the options are, and the recommended path with acceptance criteria. Use whenever asked what an issue means, how to solve it, what approach to take, what the right path forward is, or to research a backlog item before work starts. Enforces citation discipline and explicit UNVERIFIED marking.
---

# Research dossiers

A dossier answers one question: **what should someone actually do about this issue, and why?**

It is not a summary of the issue. The issue already says what it says. A dossier that restates the
Key Questions in different words has done nothing — the reader could have read the issue.

## Where dossiers live

```
docs/research/_dossiers/<unit-id>.md
```

The underscore prefix keeps them separate from `docs/research/*.md`, which the source note reserves
for the actual research deliverables a human is expected to write. Conflating the two would let an
agent's guidance masquerade as the validated research the project asked for.

After writing, post a short pointer comment on the issue — three or four lines with the headline
finding and the file path. Never paste the whole dossier into a comment.

## Evidence tiers

Every factual claim carries its tier. This is the core discipline; without it a dossier is just
confident prose.

| Tier | Meaning | How to cite |
|---|---|---|
| **T1 — repo code** | Verified by reading the source in this repository | `src/amf/graph.py` — name the symbol |
| **T2 — repo docs** | Stated in a repo document | `docs/roadmap.md` "Guardrail translation rules" |
| **T3 — primary external** | A named standard, paper, statute, or dataset actually consulted | full reference |
| **T4 — general knowledge** | Widely-held domain knowledge, not checked this session | mark `[T4]` |
| **UNVERIFIED** | Believed true, not confirmed, and load-bearing | mark `[UNVERIFIED]` inline |

**Search the repository before searching anything else.** Most of these issues already have partial
answers in `src/amf/`. A dossier that proposes building what `graph.py` already does is worse than
no dossier, because it wastes the reader's time twice — once reading it, once discovering the
duplication.

## The absolute rule on citations

**Never invent a citation.** Not an author, not a year, not a title, not a URL, not a section number.
If you believe something is standard but cannot confirm it here, write the claim and mark it
`[UNVERIFIED]`. An honest gap is useful; a fabricated reference is a landmine that detonates when a
reader tries to follow it, and it discredits every other line in the document.

The same applies to numbers. "$1–2T at risk" appearing in a source note is the note's claim, not a
verified fact — attribute it, do not adopt it.

## Structure

```markdown
# Dossier: <unit-id> — <issue title>

**Issue**: #NN · **Source**: docs/X.md → <section> · **Written**: YYYY-MM-DD
**Confidence**: high | medium | low — <one line saying why>

## What is actually being asked
The question behind the question. Two or three sentences.

## What already exists
Repo-internal prior art first, with file paths. What is already built, and what it does not do.

## Findings
Numbered. Each carries an evidence tier. This is the substance.

## Options
Each with what it costs, what it buys, and what it forecloses. Include "do nothing" when it is live.

## Recommendation
One option, named, with the reasoning. Not a menu — a recommendation.

## Acceptance criteria
Checkboxes a reviewer can verify without re-doing the research.

## Guardrail notes
Which rules bear on this, and how the recommendation stays inside them.

## Open questions
What you could not resolve, and what would resolve it.
```

## Confidence labels

- **high** — grounded in T1/T2 evidence; someone could act on this today.
- **medium** — reasoning is sound, but key facts are T4 or UNVERIFIED.
- **low** — mostly framing; the research still needs doing.

Label honestly. A "low" dossier that correctly maps the unknowns is more valuable than a "high" one
that got there by not looking hard.

## Guardrails

Load `amf-guardrails` before writing. Two failure modes specific to dossiers:

1. **Recommending a forbidden name.** Check any proposed identifier against the `FORBIDDEN` list.
2. **Sliding into prediction.** Many of these issues ask "can we predict X?". The dossier may explore
   it as a research question. It may never conclude the toolkit can predict anything, and must not
   propose user-facing text that implies it.

## What makes a dossier worth reading

- It says something the issue does not.
- It names the smallest first step, not the whole programme.
- It is explicit about what it does not know.
- It cites the repo, so the reader can check it in a minute.
- It gives a recommendation, not a survey.
