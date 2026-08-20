# AMF-PSM 90-day plan — issue index

> **Navigation aid only.** This page is a map of the GitHub issue tree created for the
> 90-day program. The issues themselves are the source of truth: they carry the acceptance
> criteria, the guardrail translations, and the evidence checklists. If this page and an
> issue disagree, the issue wins.
>
> Nothing here changes the framework document or the `amf` package's behaviour, and nothing
> here relaxes the hard rules in [`CLAUDE.md`](../CLAUDE.md).

- **Program issue:** [#77 — AMF-PSM 90-Day Implementation Plan](https://github.com/sadishaumantha-maker/AMF-PSM/issues/77)
- **Source analysis:** [`docs/ANALYSIS_AND_ROADMAP.md`](ANALYSIS_AND_ROADMAP.md)
- **Sequencing charter:** [`docs/roadmap.md`](roadmap.md)
- **Window:** Day 0 = **20 Aug 2026** · Day 90 = **18 Nov 2026**
- **Shape:** 1 program issue · 10 epics · 54 sub-issues · **65 issues total**

## Calendar

| Phase | Weeks | Dates | Epic |
|---|---|---|---|
| Baseline & gap register | Week 0 | 20 Aug 2026 | [#81](https://github.com/sadishaumantha-maker/AMF-PSM/issues/81) |
| 1 — Governance & process | 1–2 | 20 Aug – 2 Sep 2026 | [#84](https://github.com/sadishaumantha-maker/AMF-PSM/issues/84) |
| 2 — Code quality & delivery | 3–6 | 3 – 30 Sep 2026 | [#86](https://github.com/sadishaumantha-maker/AMF-PSM/issues/86) |
| 3 — Domain decomposition | 7–12 | 1 Oct – 11 Nov 2026 | [#91](https://github.com/sadishaumantha-maker/AMF-PSM/issues/91) · [#93](https://github.com/sadishaumantha-maker/AMF-PSM/issues/93) · [#94](https://github.com/sadishaumantha-maker/AMF-PSM/issues/94) |
| 4 — Testing, docs & v1.1 | 13–18 | 12 Nov – 23 Dec 2026 | [#95](https://github.com/sadishaumantha-maker/AMF-PSM/issues/95) |
| 5 — Scaling & backlog | 19–24 * | 24 Dec 2026 – 3 Feb 2027 | [#96](https://github.com/sadishaumantha-maker/AMF-PSM/issues/96) |

\* The source analysis writes Phase 5 as **"Weeks 19–12"**. That is a typo carried forward
verbatim in [#77](https://github.com/sadishaumantha-maker/AMF-PSM/issues/77) and
[#96](https://github.com/sadishaumantha-maker/AMF-PSM/issues/96); the reading used throughout is
Weeks 19–24. Phase 4 and Phase 5 extend past Day 90 by design — the 90-day measurement window
closes mid-Phase-4.

## Epic tree

### [EPIC 0](https://github.com/sadishaumantha-maker/AMF-PSM/issues/81) — Baseline, issue dossier & critical-gap register

The six gaps below are the analysis's own list, with its severities preserved.

| # | Sub-issue | Severity |
|---|---|---|
| 0.1 | [#99](https://github.com/sadishaumantha-maker/AMF-PSM/issues/99) — Baseline snapshot & measurement protocol | — |
| 0.2 | [#100](https://github.com/sadishaumantha-maker/AMF-PSM/issues/100) — GAP 1: no automated rulesets | 🔴 High |
| 0.3 | [#101](https://github.com/sadishaumantha-maker/AMF-PSM/issues/101) — GAP 2: unclear issue priorities | 🟠 High |
| 0.4 | [#102](https://github.com/sadishaumantha-maker/AMF-PSM/issues/102) — GAP 3: no milestones | 🟠 High |
| 0.5 | [#103](https://github.com/sadishaumantha-maker/AMF-PSM/issues/103) — GAP 4: no assignee clarity | 🟡 Medium |
| 0.6 | [#104](https://github.com/sadishaumantha-maker/AMF-PSM/issues/104) — GAP 5: discussion scattered | 🟡 Medium |
| 0.7 | [#105](https://github.com/sadishaumantha-maker/AMF-PSM/issues/105) — GAP 6: no sprint/release cycle | 🟡 Medium |
| 0.8 | [#106](https://github.com/sadishaumantha-maker/AMF-PSM/issues/106) — Issue-by-issue dossier + dependency graph | — |

### [EPIC 1](https://github.com/sadishaumantha-maker/AMF-PSM/issues/84) — Phase 1: governance & process (Weeks 1–2)

| # | Sub-issue |
|---|---|
| 1.1 | [#107](https://github.com/sadishaumantha-maker/AMF-PSM/issues/107) — `main` ruleset (2 approvals, signed commits, required checks) |
| 1.2 | [#108](https://github.com/sadishaumantha-maker/AMF-PSM/issues/108) — `develop` ruleset (1 approval, CI required) |
| 1.3 | [#109](https://github.com/sadishaumantha-maker/AMF-PSM/issues/109) — `release/*` ruleset (2 approvals, signed, strict) |
| 1.4 | [#110](https://github.com/sadishaumantha-maker/AMF-PSM/issues/110) — Distribute governance docs + acknowledgment |
| 1.5 | [#111](https://github.com/sadishaumantha-maker/AMF-PSM/issues/111) — Triage & prioritise the nine open issues |
| 1.6 | [#112](https://github.com/sadishaumantha-maker/AMF-PSM/issues/112) — Extend `docs/roadmap.md` with a quarterly breakdown |

### [EPIC 2](https://github.com/sadishaumantha-maker/AMF-PSM/issues/86) — Phase 2: code quality & delivery (Weeks 3–6)

| # | Sub-issue |
|---|---|
| 2.1 | [#113](https://github.com/sadishaumantha-maker/AMF-PSM/issues/113) — Review & merge PR #42 |
| 2.2 | [#114](https://github.com/sadishaumantha-maker/AMF-PSM/issues/114) — Audit `ci.yml` against the required-checks contract |
| 2.3 | [#115](https://github.com/sadishaumantha-maker/AMF-PSM/issues/115) — `release.yml` (private-only; no publish step) |
| 2.4 | [#116](https://github.com/sadishaumantha-maker/AMF-PSM/issues/116) — `docs.yml` decision (options A/B/C) |
| 2.5 | [#117](https://github.com/sadishaumantha-maker/AMF-PSM/issues/117) — Coverage badge + disclosure decision |
| 2.6 | [#118](https://github.com/sadishaumantha-maker/AMF-PSM/issues/118) — Dependabot (pip + github-actions) |

### [EPIC 3](https://github.com/sadishaumantha-maker/AMF-PSM/issues/91) — Decompose #31 (policy making)

| # | Sub-issue |
|---|---|
| 31a | [#120](https://github.com/sadishaumantha-maker/AMF-PSM/issues/120) — Policy-tier hierarchy |
| 31b | [#121](https://github.com/sadishaumantha-maker/AMF-PSM/issues/121) — Amendment procedures |
| 31c | [#122](https://github.com/sadishaumantha-maker/AMF-PSM/issues/122) — Time- and people-independent policies |
| 31d | [#123](https://github.com/sadishaumantha-maker/AMF-PSM/issues/123) — Policy change-history case studies |

### [EPIC 4](https://github.com/sadishaumantha-maker/AMF-PSM/issues/93) — Decompose #25 (global stock markets; absorbs #43)

| # | Sub-issue |
|---|---|
| 25a | [#124](https://github.com/sadishaumantha-maker/AMF-PSM/issues/124) — Equity-market taxonomy |
| 25b | [#125](https://github.com/sadishaumantha-maker/AMF-PSM/issues/125) — Liquidity & transparency as structural proxies |
| 25c | [#126](https://github.com/sadishaumantha-maker/AMF-PSM/issues/126) — Regulatory regimes (ties to #31) |
| 25d | [#127](https://github.com/sadishaumantha-maker/AMF-PSM/issues/127) — Data model in AMF terms |
| 25e | [#128](https://github.com/sadishaumantha-maker/AMF-PSM/issues/128) — Tests for ten segments |
| 25f | [#129](https://github.com/sadishaumantha-maker/AMF-PSM/issues/129) — `examples/global_equity_markets.py` |

### [EPIC 5](https://github.com/sadishaumantha-maker/AMF-PSM/issues/94) — Research commissions (#28, #32)

| # | Sub-issue |
|---|---|
| 5.1 | [#131](https://github.com/sadishaumantha-maker/AMF-PSM/issues/131) — Assign #28 an owner + research log |
| 5.2 | [#132](https://github.com/sadishaumantha-maker/AMF-PSM/issues/132) — `docs/case_studies/hindenburg.md` + template |
| 5.3 | [#133](https://github.com/sadishaumantha-maker/AMF-PSM/issues/133) — Link fragility patterns to the diagnostics |
| 5.4 | [#134](https://github.com/sadishaumantha-maker/AMF-PSM/issues/134) — Scope #32 (four regime archetypes → two axes) |
| 5.5 | [#135](https://github.com/sadishaumantha-maker/AMF-PSM/issues/135) — Map five to seven governments |
| 5.6 | [#136](https://github.com/sadishaumantha-maker/AMF-PSM/issues/136) — `docs/taxonomies/government_philosophies.md` |

### [EPIC 6](https://github.com/sadishaumantha-maker/AMF-PSM/issues/95) — Phase 4: testing, docs & v1.1 (Weeks 13–18)

| # | Sub-issue |
|---|---|
| 6.1 | [#137](https://github.com/sadishaumantha-maker/AMF-PSM/issues/137) — Integration scenarios (#25 + #31) |
| 6.2 | [#138](https://github.com/sadishaumantha-maker/AMF-PSM/issues/138) — Policy stack vs published regulatory structure |
| 6.3 | [#139](https://github.com/sadishaumantha-maker/AMF-PSM/issues/139) — Validate the global-equity models |
| 6.4 | [#140](https://github.com/sadishaumantha-maker/AMF-PSM/issues/140) — `docs/getting_started.md` |
| 6.5 | [#141](https://github.com/sadishaumantha-maker/AMF-PSM/issues/141) — `docs/architecture.md` |
| 6.6 | [#142](https://github.com/sadishaumantha-maker/AMF-PSM/issues/142) — `docs/examples.md` |
| 6.7 | [#143](https://github.com/sadishaumantha-maker/AMF-PSM/issues/143) — v1.1 release planning |

### [EPIC 7](https://github.com/sadishaumantha-maker/AMF-PSM/issues/96) — Phase 5: scaling & backlog (Weeks 19–24)

| # | Sub-issue |
|---|---|
| 7.1 | [#144](https://github.com/sadishaumantha-maker/AMF-PSM/issues/144) — #26: commodities, bonds, forex |
| 7.2 | [#145](https://github.com/sadishaumantha-maker/AMF-PSM/issues/145) — #21: Phase 2 charter + PSM name ratification |
| 7.3 | [#146](https://github.com/sadishaumantha-maker/AMF-PSM/issues/146) — #23: concept-extension menu |

### [EPIC 8](https://github.com/sadishaumantha-maker/AMF-PSM/issues/97) — Quick wins (~9 h)

Deliberately **childless**. Every quick win is already a sub-issue of another epic; duplicating
them here would double-count the effort. The epic is a Week-1 view, not a work container.

| Quick win | Effort | Tracked in |
|---|---|---|
| Merge PR #42 | 2 h | [#113](https://github.com/sadishaumantha-maker/AMF-PSM/issues/113) |
| Triage the nine issues | 2 h | [#111](https://github.com/sadishaumantha-maker/AMF-PSM/issues/111) |
| Close duplicate #43 | 15 min | [#93](https://github.com/sadishaumantha-maker/AMF-PSM/issues/93) |
| `docs/roadmap.md` — **extend**, not create | 4 h | [#112](https://github.com/sadishaumantha-maker/AMF-PSM/issues/112) |
| Unlock #25 | 15 min | [#111](https://github.com/sadishaumantha-maker/AMF-PSM/issues/111) |
| Re-title #23 / #21 | 30 min | [#111](https://github.com/sadishaumantha-maker/AMF-PSM/issues/111) |

### [EPIC 9](https://github.com/sadishaumantha-maker/AMF-PSM/issues/98) — Success metrics, cadence & Day-90 review

| Metric | Target | Current | Protocol |
|---|---|---|---|
| Backlog triaged | 100% | 0% | [#147](https://github.com/sadishaumantha-maker/AMF-PSM/issues/147) |
| Issues with milestones | 9/9 | 0/9 | [#148](https://github.com/sadishaumantha-maker/AMF-PSM/issues/148) |
| PRs merged per week | ≥1 | 0 | [#149](https://github.com/sadishaumantha-maker/AMF-PSM/issues/149) |
| Test coverage | ≥80% (gate is 100%) | 100% | [#150](https://github.com/sadishaumantha-maker/AMF-PSM/issues/150) |
| CI pass rate on `main` | 100% | — | [#152](https://github.com/sadishaumantha-maker/AMF-PSM/issues/152) |
| Rulesets active | 3 | 0 | [#153](https://github.com/sadishaumantha-maker/AMF-PSM/issues/153) |
| Documentation pages | ≥10 | — | [#154](https://github.com/sadishaumantha-maker/AMF-PSM/issues/154) |
| Cadence rituals + Day-90 review | — | — | [#155](https://github.com/sadishaumantha-maker/AMF-PSM/issues/155) |

## Guardrails every issue inherits

The plan is a schedule, not a licence. Each issue restates the constraint it could most easily
be read as relaxing; the full statements live in [`CLAUDE.md`](../CLAUDE.md) and
[`docs/roadmap.md`](roadmap.md).

1. **No trading system.** Structural vocabulary only — the naming guard in
   `tests/unit/test_non_trading_boundary.py` rejects `order`, `price`, `trade`, `portfolio`,
   `signal` and the rest. "Liquidity", "spreads", and "volume" enter as dimensionless `[0,1]`
   proxies on the circulatory system, never as market data.
2. **Illustrative, not validated.** No issue may produce a claim of predictive power, empirical
   validation, or a diagnosis of a real market.
3. **Protected IP is frozen.** `AMF Framework v1.docx`, its `.ots`, `anatomical-market-framework`,
   and `LICENSE.txt` are checksum-locked; `SHA256SUMS` is never extended with source files.
4. **The seven-system anatomy is closed.** New concepts attach to the existing seven; no eighth
   `SystemKind`.
5. **Private distribution only.** No PyPI, no public index, no publish workflow — this
   constrains [#115](https://github.com/sadishaumantha-maker/AMF-PSM/issues/115) directly.
6. **The 100% coverage gate is a floor, not a target.** The ≥80% metric row is a reporting
   threshold; the failing build stays at 100%.
7. **Determinism.** Nothing user-visible may depend on assembly order, and no randomness enters
   unseeded.

## Where the plan departs from the source analysis

The analysis was reconciled against the repository as it actually stands, and three of its
statements needed adjusting rather than transcribing:

- **`docs/roadmap.md` already exists** (merged in PR #36). The "create `docs/roadmap.md`" quick
  win is therefore an **extension** task —
  [#112](https://github.com/sadishaumantha-maker/AMF-PSM/issues/112) adds the quarterly
  breakdown to the existing document instead of overwriting it.
- **Three competing "Phase" vocabularies** were in play (the analysis's five delivery phases,
  the roadmap's Phase 1/Phase 2 product split, and stages 2.0–2.5).
  [#112](https://github.com/sadishaumantha-maker/AMF-PSM/issues/112) resolves the collision by
  naming them **Delivery Phases 1–5** and **Product Quarters Q1–Q3**.
- **Research issues #45–#66 already exist.** They are cross-linked from the relevant epics
  rather than duplicated. **#27 is closed** and is excluded from the nine-item backlog.

## Keeping this page honest

This index records structure, not status — it names no owner and tracks no completion, so it
does not go stale as work proceeds. It needs editing only when the tree itself changes: an epic
added, a sub-issue re-parented, or an issue closed as duplicate. Progress belongs in the weekly
standup on [#77](https://github.com/sadishaumantha-maker/AMF-PSM/issues/77), per
[#155](https://github.com/sadishaumantha-maker/AMF-PSM/issues/155).
