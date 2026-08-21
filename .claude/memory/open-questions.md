# Open questions

Items needing a human decision. Agents append here rather than guessing. Each entry states the
question, why it cannot be settled autonomously, and what the options are.

---

## Q-001: How should `docs/QUANTUM_NEURAL_RESEARCH.md` be decomposed?

**Raised by**: Phase 6 planning · **Status**: open

The document (799 lines, discussions Q1–Q3, D1–D3, H1–H2+) is framed around "Deep Neural Networks for
Market **Prediction**" and "Multi-Asset **Forecasting**". Both collide with the non-trading boundary
and the illustrative-not-validated rule.

Cannot be settled autonomously because it is a question about author intent, not about compliance:

- **Option A** — reframe each unit structurally (prediction → conditional scenario trajectory;
  embeddings → redundancy/monoculture) and decompose with `guardrail-review` labels throughout.
- **Option B** — decompose only the units that already have compliant structural readings (topology,
  entropy, network pathways) and hold the forecasting-framed ones pending a rewrite of the document.
- **Option C** — decline to decompose, and instead open one issue proposing the document be rewritten.

Recommendation on file: **B**, because it produces useful issues immediately without either
transcribing forbidden framing or silently rewriting the author's stated intent.

**Evidence added 2026-08-21** — the acceptance run of `extract_atoms.py` against this document:

- **All 11 of 11 units are guardrail-flagged.** Every discussion carries predictive framing
  (`predict`, `forecast`, `prediction`) and most carry forbidden vocabulary (`price`, `trade`,
  `order`, `portfolio`, `signal`, `returns`, `backtest`). This is not a document with a few
  problem sections; the framing is uniform. That weakens Option B — there is no compliant subset to
  carve out — and strengthens Option C.
- **The extractor is not lossless for this document's shape.** It captured 22 atoms from 799 lines,
  because this document puts content in bold list-headers (`**Foundational Theory**:`), numbered
  items with nested bullets, and fenced code blocks — none of which the parser models. Publishing
  from the current manifest would silently drop most of the author's content.

**Therefore: blocked, correctly.** No issues have been created from this document. Two things must
happen before any are, in this order: (1) a human decision on A/B/C above, and (2) if the answer is
A or B, an extension to the intake parser plus a re-run showing an atom count consistent with the
document's real size.

---

## Q-002: Should the two overlapping issue sets be merged?

**Raised by**: session audit · **Status**: open

Issues #45–#92 (research-track decomposition) and #77–#98 (90-day implementation plan) were created
independently and cover overlapping ground — both claim #25, #28, #31, #32. Neither references the
other.

Options: cross-link only (cheapest, preserves both structures); designate one canonical and close the
other as duplicate (cleanest, discards work); or merge into a single hierarchy (most work).

Blocked on: which structure the maintainer actually intends to work from.

---

## Q-003: Which coverage figure is authoritative in contributor-facing docs?

**Raised by**: repo-facts verification · **Status**: open, low stakes

`.github/pull_request_template.md` says "minimum 80%". `CLAUDE.md` mandates 100% and CI enforces
`--cov-fail-under=100`. The template is simply wrong, but fixing it is a `.github` change that was
deliberately deferred out of the agent-system build. Recorded so it is not rediscovered a third time.

Related, same file: it carries GitHub *issue-template* YAML frontmatter (which renders as literal
text in every PR body) and asks about SQL injection and XSS for a stdlib-only offline library.
Separately, `.github/RULESET-POLICY.md` links a `CODE_OF_CONDUCT.md` that does not exist.
