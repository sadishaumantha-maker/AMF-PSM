# Issue index — source unit ↔ GitHub issue

**Check this file before creating any issue.** It is what stops the same source unit being
decomposed twice. If a unit already has a row here, do not create a new issue for it — update the
existing one, or stop and report the conflict.

`hash` is the sha256 prefix of the unit's verbatim atoms, used for idempotency: an unchanged hash
means an unchanged source unit, so republishing it is a no-op. Rows written before the publisher ran
carry `pending`; the publisher backfills them on first run.

Legend for `status`: `ok` verified against source · `defect` known fidelity defect · `pending` not yet audited.

## docs/RESEARCH_DISCUSSIONS.md

| unit | issue | id | parent | hash | status |
|---|---|---|---|---|---|
| program | #45 | 5200357262 | — | pending | ok |
| track-1 | #46 | 5200359394 | — | pending | ok |
| track-2 | #47 | 5200360382 | — | pending | ok |
| track-3 | #48 | 5200361402 | — | pending | ok |
| track-4 | #49 | 5200362778 | — | pending | ok |
| track-5 | #50 | 5200363970 | — | pending | ok |
| track-6 | #51 | 5200365479 | — | pending | ok |
| track-7 | #52 | 5200366629 | — | pending | ok |
| track-8 | #53 | 5200367797 | — | pending | ok |
| cross-cutting | #54 | 5200368870 | — | pending | ok |
| discussion-1.1 | #55 | 5200371541 | #46 | pending | ok |
| discussion-1.2 | #56 | 5200372555 | #46 | pending | ok |
| discussion-1.3 | #57 | 5200373551 | #46 | pending | ok |
| discussion-2.1 | #58 | 5200375129 | #47 | pending | ok |
| discussion-2.2 | #59 | 5200376190 | #47 | pending | ok |
| discussion-2.3 | #60 | 5200377221 | #47 | pending | ok |
| discussion-3.1 | #61 | 5200378213 | #48 | pending | ok |
| discussion-3.2 | #62 | 5200379123 | #48 | pending | ok — title defect fixed 2026-08-20 (ADR-001) |
| discussion-3.3 | #63 | 5200380271 | #48 | pending | ok |
| discussion-4.1 | #64 | 5200382184 | #49 | pending | ok |
| discussion-4.2 | #65 | 5200383337 | #49 | pending | ok |
| discussion-4.3 | #66 | 5200384726 | #49 | pending | ok |
| discussion-5.1 | #67 | 5200385697 | #50 | pending | ok |
| discussion-5.2 | #68 | 5200386722 | #50 | pending | ok |
| discussion-5.3 | #69 | 5200387805 | #50 | pending | ok |
| discussion-6.1 | #70 | 5200389490 | #51 | pending | ok |
| discussion-6.2 | #71 | 5200391112 | #51 | pending | ok |
| discussion-6.3 | #72 | 5200392503 | #51 | pending | ok |
| discussion-7.1 | #73 | 5200393976 | #52 | pending | ok |
| discussion-7.2 | #74 | 5200395097 | #52 | pending | ok |
| discussion-7.3 | #75 | 5200396045 | #52 | pending | ok |
| discussion-8.1 | #76 | 5200397577 | #53 | pending | ok |
| discussion-8.2 | #78 | 5200398803 | #53 | pending | ok |
| discussion-8.3 | #79 | 5200399949 | #53 | pending | ok |
| theme-a | #80 | 5200401171 | #54 | pending | ok |
| theme-b | #82 | 5200402194 | #54 | pending | ok |
| theme-c | #83 | 5200403258 | #54 | pending | ok |
| theme-d | #85 | 5200404236 | #54 | pending | ok |
| next-step-1 | #87 | 5200405778 | #45 | pending | ok |
| next-step-2 | #88 | 5200406437 | #45 | pending | ok |
| next-step-3 | #89 | 5200407177 | #45 | pending | ok |
| next-step-4 | #90 | 5200407854 | #45 | pending | ok |
| next-step-5 | #92 | 5200409370 | #45 | pending | ok |

**43 issues · 258 source atoms · all bodies verified verbatim · 1 known title defect (#62)**

Atom total reconciles as 253 content atoms (24 themes + 96 key questions + 96 research areas +
24 deliverables + 13 theme bullets) plus 5 process steps from the Next Steps section. Both the
intake extractor and the auditor's independent parser report 258; if either reports otherwise,
one of them has regressed.

## docs/QUANTUM_NEURAL_RESEARCH.md

Not decomposed, by decision: Q-001 was resolved 2026-08-21 as **Option C** (ADR-009). Issue **#169**
(id 5216948752) proposes the document be restructured with structural framing first; decomposition
stays blocked until that rewrite lands and `extract_atoms.py --stats-only` reports an atom count
consistent with the document's size.

## Not managed by this system

Issues **#77, #81, #84, #86, #91, #93–#138 and counting** were created by a separate session as a
"90-Day Implementation Plan" epic set plus its task breakdown. They have no provenance blocks and are
not indexed here. They overlap this set on #25, #28, #31, #32 — see Q-002. Several of their tasks
duplicate work this set already tracks: e.g. #124–#129 decompose global equity market mapping, which
overlaps `discussion-2.1` (#58); #126 maps regulatory regimes per segment, overlapping
`discussion-2.3` (#60); #132 creates a Hindenburg case study, overlapping `discussion-4.1` (#64).
Do not treat their numbers as free, and check for an overlapping task there before publishing here.

Resolved 2026-08-21 (Q-002 → ADR-008): the two sets are deliberately kept, split by role — this
research set is canonical for **content and acceptance criteria**, the 90-day set for **scheduling
and ownership** — and the five collision pairs (#58↔#124, #59↔#125, #60↔#126, #64↔#132,
#46↔#120–#123) carry cross-link comments on both sides.

Pre-existing issues **#11, #21, #23, #25, #26, #27, #28, #31, #32, #43** are human-authored and
outside this system's scope. Never edit them; reference them instead.
