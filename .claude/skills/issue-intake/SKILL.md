---
name: issue-intake
description: Decompose a source document (research note, roadmap, spec) into a reviewable GitHub issue manifest without losing a single word. Use whenever asked to turn a document into issues, break a note into tasks, create issues from a doc, or plan a decomposition. Produces a manifest for human approval — it never writes to GitHub itself.
---

# Lossless decomposition

Turning a document into issues is a **transcription** job with a structuring job layered on top.
The transcription must be perfect; the structuring is where judgement belongs. Keeping those two
separate is what makes the result auditable.

## The output is a manifest, not issues

```sh
python3 .claude/skills/issue-intake/scripts/extract_atoms.py \
    --source docs/YOUR_DOC.md \
    --out .claude/manifests/YOUR_DOC.manifest.yaml
```

Use `--stats-only` first to see the atom counts and guardrail flags without writing anything.

The manifest is reviewable, diffable, and cheap to discard. 43 published issues are none of those.
A human approves the manifest before `issue-publisher` touches GitHub. See ADR-003 — this exists
because two sessions once published overlapping issue sets that neither could see.

## Atoms: what must survive verbatim

An **atom** is a unit of the author's own words. Atoms are copied byte-for-byte. Never paraphrase,
never "improve", never fix a typo silently.

For a research-discussion document the atom types are:

| Type | Source form |
|---|---|
| `theme` | the `**Theme**: …` line |
| `key-question` | each bullet under `**Key Questions**:` |
| `research-area` | each bullet under `**Research Areas**:` |
| `deliverable` | the `**Deliverable**: …` line |
| `theme-bullet` | each bullet under a `### Theme X:` heading |
| `process-step` | each numbered item in a process section |

**The heading is an atom too.** ADR-001 exists because a heading was silently restyled — a colon
became an em dash in issue #62's title and survived a full body-level review. The only permitted
restyling is a bracketed prefix for container issues (`[Track 1] Policy & Regulatory Architecture`);
the heading text itself is never edited.

Known-good reference: `docs/RESEARCH_DISCUSSIONS.md` yields **258 atoms** — 24 themes, 96 key
questions, 96 research areas, 24 deliverables, 13 theme bullets, 5 process steps — across 41 units.
If a change to the extractor moves that number, you broke something.

## Stable unit ids

Ids are derived from the document's own numbering so they survive re-runs and reordering:

```
discussion-3.2   theme-a   track-5   next-step-1
```

Never number units by position in the file. A unit inserted at the top must not renumber everything
below it, or every hash changes and every issue looks stale.

## Idempotency

Each unit carries `title_sha256` and `body_sha256`. On a re-run:

- hash unchanged → the unit is already published correctly → **no write**
- hash changed → the source was edited → update only that issue
- no row in `.claude/memory/issue-index.md` → new unit → create

Check `issue-index.md` *before* proposing anything. If a unit already has an issue, the manifest
records the existing number rather than proposing a new one.

## Structuring: where judgement belongs

Containers (tracks, programs, cross-cutting groups) are **synthesised** — they have no single source
heading of their own, or they aggregate their children. Two rules:

1. A container's body may summarise its children, but any text presented as a quotation must be a
   real quotation. Summarising is fine; summarising *in quotation marks* is fabrication.
2. Anything you write that is not from the source goes under its own heading — `## Problem Statement`,
   `## Guardrail`, `## Cross-links`. Never interleave your prose with quoted atoms.

## Guardrail flagging

The extractor flags two conditions and does not resolve either:

- **`predictive-framing`** — the text claims or invites prediction/forecasting. The package is
  explicitly illustrative and not validated.
- **`non-trading-vocabulary`** — the text uses words forbidden in identifiers.

A flag is not a veto. Source prose may discuss trading freely; the constraint is on what the package
*names* and what an issue *claims the toolkit does*. Load `amf-guardrails` and use its translation
table to write the reframing. Flagged units get the `guardrail-review` label and a
`## Structural reframing required` section giving both the source's ask and the compliant reading.

Do not silently transcribe a flagged unit, and do not silently rewrite it. Both hide the conflict
from the person who wrote the document.

## Before handing the manifest over

- [ ] Atom count matches an independent count (`fidelity_check.py` parses the same document with a
      different algorithm — run both and compare)
- [ ] Every unit id is stable and derived from the document's numbering
- [ ] Every existing unit in `issue-index.md` is matched, not duplicated
- [ ] Every guardrail flag has a written reframing, or an entry in `open-questions.md`
- [ ] Typos in the source are preserved verbatim, and noted separately as follow-ups
