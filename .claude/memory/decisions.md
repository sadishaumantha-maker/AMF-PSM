# Decision log

Why each rule exists. Every entry names the failure that caused it, so a future agent can tell a
load-bearing rule from an arbitrary preference.

---

## ADR-001: Issue titles are copied verbatim from source headings

**Status**: enforced by `fidelity_check.py`

**Cause**: Issue #62 was created with the title `Discussion 3.2: Feedback Loops — Markets ↔ Policy`.
The source heading in `docs/RESEARCH_DISCUSSIONS.md` line 150 reads
`Discussion 3.2: Feedback Loops: Markets ↔ Policy`. The inner colon became an em dash — most likely
because a colon inside a colon-prefixed title reads awkwardly, so it was "improved" in passing.

The body of #62 was verbatim-perfect, and its own parent (#48) rendered the colon correctly. Only the
title drifted, and body-level review never looked at titles.

**Decision**: the title is an atom like any other. It is copied byte-for-byte from the source heading.
Restyling is confined to a bracketed prefix (`[Track 1] …`), never to the heading text itself.

---

## ADR-002: The auditor is never the author

**Status**: enforced by agent separation

**Cause**: the #62 defect survived a careful self-review. An agent checking its own output shares its
own blind spots — it verifies what it thought about, not what it forgot.

**Decision**: `issue-auditor` re-derives atoms from source with its **own** parser, independent of
`extract_atoms.py`. The two parsers agreeing on a count (253 for `RESEARCH_DISCUSSIONS.md`) is
evidence; one parser agreeing with itself is not. The duplication is deliberate — do not refactor the
two into a shared module.

---

## ADR-003: Nothing reaches GitHub except through an approved manifest

**Status**: enforced by tool restrictions on `issue-cartographer`

**Cause**: two sessions independently created overlapping issue sets (#45–#92, #77–#98) covering the
same underlying issues (#25, #28, #31, #32). Neither could see the other's work, because work only
became visible once it was already published.

**Decision**: decomposition produces a manifest file first. It is reviewable, diffable, and cheap to
throw away. Publishing is a separate step against an approved manifest, and claims each unit in
`issue-index.md` before writing.

---

## ADR-004: Comparison unescapes before diffing

**Status**: enforced by `fidelity_check.py`

**Cause**: the GitHub MCP server HTML-escapes on read — `&`→`&amp;`, `"`→`&#34;`, `'`→`&#39;`,
`>`→`&gt;`. A naive diff reports a false failure on essentially every issue containing an ampersand,
which is most of them. Worse, it trains the reader to ignore audit output.

**Decision**: normalise both sides before comparing. Escaping is a transport artifact, never a defect.

---

## ADR-005: A guardrail conflict is surfaced, never resolved silently

**Status**: enforced by the `guardrail-review` label and the three-point gate

**Cause**: `docs/QUANTUM_NEURAL_RESEARCH.md` is framed around market prediction and forecasting.
Transcribing it literally would inject forbidden framing across a dozen issues at once. Silently
rewriting it would hide from the author that their intent was altered.

**Decision**: quote the source verbatim under its own heading, add a
`## Structural reframing required` section giving the compliant reading, and label the issue. The
human sees both and can overrule either.

---

## ADR-006: Guardrail flags scan the whole source body, not the extracted atoms

**Status**: enforced by `extract_atoms.py`

**Cause**: found by the first acceptance run against `docs/QUANTUM_NEURAL_RESEARCH.md`. Flags were
originally computed over the atoms the parser had successfully extracted. Because that document's
shape defeats the parser (22 atoms from 799 lines), the safety check only ever saw the `**Theme**:`
lines — and reported **2 flagged units out of 11**. Scanning the full block body instead reports
**11 out of 11**. Nine units carrying `predict`, `forecast`, `price`, `trade` and `portfolio` would
have passed through unflagged.

**Decision**: guardrail detection runs over the unit's entire source text, independent of how much
of it the extractor understood. A safety check that inherits the parser's blind spots is worse than
no safety check, because it produces a clean report over unexamined content.

**Side effect worth knowing**: the same change raised the flag count on the already-published
`docs/RESEARCH_DISCUSSIONS.md` set from 12 units to 19. Those 7 additional units are published and
were reviewed under the weaker scan; they are not necessarily defective, but they have not been
looked at with the stronger one.

---

## ADR-007: The intake parser is document-shape-specific, and that is a known limit

**Status**: documented, not solved

**Cause**: `docs/RESEARCH_DISCUSSIONS.md` puts each discussion at `####` as a leaf with
`**Field**: value` lines and simple bullet lists. `docs/QUANTUM_NEURAL_RESEARCH.md` puts each
discussion at `###` containing `####` sub-sections, bold list-headers, numbered items with nested
bullets, and fenced code blocks. The extractor handles the first shape and captures almost nothing
of the second.

**Decision**: do not keep generalising the parser speculatively. Extend it deliberately, per
document shape, and always re-run the known-good fixture (`docs/RESEARCH_DISCUSSIONS.md` → 43 units,
258 atoms) to prove the extension broke nothing. An atom count that looks small relative to the
source's line count is the signal to stop and extend rather than publish.

---

## ADR-008: The two issue sets are split by role, not merged

**Status**: enacted 2026-08-21 (Q-002)

**Cause**: issues #45–#92 (research decomposition) and #77–#138 (90-day implementation plan) were
created by independent sessions and collide on five artifacts — the equity market taxonomy
(#58↔#124), the liquidity mapping (#59↔#125), the regulatory-regime taxonomy (#60↔#126), the
Hindenburg case study (#64↔#132), and the policy-tier architecture (#46↔#120–#123) — with no
cross-links, so the sets were diverging on shared ground.

**Decision**: neither set is retired and they are not merged, because they answer different
questions. The research set is canonical for **content and acceptance criteria**; the 90-day set is
canonical for **scheduling and ownership**. Both sides of every collision pair carry a cross-link
comment stating that split. A future task that would touch a shared artifact starts from the
research issue's content and the 90-day issue's schedule.

---

## ADR-009: QUANTUM_NEURAL_RESEARCH.md is not decomposed until it is rewritten

**Status**: enacted 2026-08-21 (Q-001, Option C) — tracked by issue #169

**Cause**: the acceptance run measured two independent blockers. All 11 units are
guardrail-flagged — the predictive framing is uniform, so Option B (decompose the compliant
subset) selects the empty set. And the intake parser captures 22 atoms from 799 lines (ADR-007),
so Option A (reframe everything now) would first require a parser extension and would then inject
`Structural reframing required` sections into ~11 issues at once.

**Decision**: one proposal issue (#169) asks for the document to be restructured with structural
framing per the guardrails translation table, in a parser-compatible shape or alongside a
deliberate parser extension. The go signal for decomposition is a re-run of
`extract_atoms.py --stats-only` reporting an atom count consistent with the document's real size.
