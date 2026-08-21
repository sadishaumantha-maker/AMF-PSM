# Source registry

Which documents have been decomposed into issues, and the content hash of each at the time it was
decomposed. This is the idempotency record: if a document's hash is unchanged, re-running
decomposition on it must produce zero writes.

Read on demand — not auto-loaded.

| Document | sha256 (prefix) | Atoms | Issues | Manifest | Decomposed |
|---|---|---|---|---|---|
| `docs/RESEARCH_DISCUSSIONS.md` | `844ba4b4645d0307` | 253 | 43 (#45–#92) | `manifests/RESEARCH_DISCUSSIONS.manifest.yaml` | 2026-08-20 |
| `docs/QUANTUM_NEURAL_RESEARCH.md` | `534eea72432523af` | 22 of ~700 | 0 | none — deliberately | **rewrite proposed** — issue #169 (Q-001 → C, ADR-009) |
| `docs/ANALYSIS_AND_ROADMAP.md` | — | — | — | — | reference only, not a decomposition source |
| `docs/roadmap.md` | — | — | — | — | reference only; source of the guardrail translation table |

## Atom breakdown for `docs/RESEARCH_DISCUSSIONS.md`

Recorded so a re-run can be checked against a known-correct decomposition without re-deriving it.

| Atom type | Count |
|---|---|
| Key Questions | 96 |
| Research Areas | 96 |
| Discussion Themes | 24 |
| Deliverables | 24 |
| Cross-cutting theme bullets | 13 (A=4, B=3, C=3, D=3) |
| **Total** | **253** |

Structural units: 8 tracks, 24 discussions, 4 cross-cutting themes, 5 next-step items, 1 program
document (engagement steps + discussion template + header/footer metadata).

Non-ASCII characters that must survive a round trip: `ö` `–` `—` `→` `↔`. If any of these degrade to
an ASCII lookalike, the extractor or the transport is lossy — treat it as a defect, not a rendering
quirk.

## How to update this file

The publisher writes a row after a successful run. Never hand-edit a hash: recompute it with

```sh
python3 -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest()[:16])" docs/FILE.md
```

A hash that changes without a deliberate edit to the document means someone modified a source note
in place — find out why before re-decomposing, because issue bodies quoting the old text are now
stale.

## Why `docs/QUANTUM_NEURAL_RESEARCH.md` has no manifest

No manifest was written for it, deliberately. A manifest is a publishing proposal, and writing one
that is known to be lossy invites someone to approve it. Two blockers, both recorded in Q-001:

1. **All 11 units are guardrail-flagged** — uniform predictive framing plus forbidden vocabulary.
   There is no compliant subset to carve out without a decision from the author.
2. **The extractor captured 22 atoms from 799 lines.** That ratio is the stop signal: this document
   uses bold list-headers, numbered items with nested bullets, and fenced code blocks, none of which
   the parser models (ADR-007).

Re-run `extract_atoms.py --stats-only` against it after any parser extension. If the atom count is
still small relative to the document's size, it is still not ready to publish.

Resolution (2026-08-21): Q-001 was decided as Option C — issue #169 proposes the rewrite (ADR-009).
The two blockers above remain the acceptance criteria for lifting the block.
