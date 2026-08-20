# AMF-PSM — Phase 2 roadmap & issue triage

> **Status: proposal for ratification.** This document turns the open issue backlog
> into a sequenced, guardrail-compliant plan. Nothing here changes the framework
> document or the package's behaviour; it is planning only.

## Charter (unchanged, restated)

Every item below inherits the project's hard rules from
[`CLAUDE.md`](../CLAUDE.md), and this roadmap cannot be read as a plan to relax them:

- **Structural, not trading.** The `amf` package models market *structure and
  resilience* only. No orders, brokers, prices, returns, P&L, signals, or backtests
  ever enter it. A test (`tests/unit/test_non_trading_boundary.py`) mechanically
  rejects public names/fields containing any of:
  `order, buy, sell, price, pnl, broker, backtest, ticker, trade, portfolio,
  candlestick`. New work must use structural vocabulary.
- **Illustrative, not validated.** Inputs, thresholds, weights, and scores are not
  empirically validated. Output is not advice and is not a diagnosis or forecast of
  any real market. No roadmap item may claim otherwise.
- **Protected IP is frozen.** `AMF Framework v1.docx`, its `.ots`, the
  `anatomical-market-framework` text, and `LICENSE.txt` are checksum-locked and are
  never edited, and `SHA256SUMS` is never extended with source files.
- **The seven-system anatomy is closed.** `SystemKind` has exactly seven members. New
  concepts attach to those seven — new metrics, dependency kinds, diagnostics,
  example markets — they do **not** add an eighth system (that would be a breaking,
  cross-cutting change to every "all seven present" check, factory, and round-trip).

## What "PSM" means (serves #21)

"PSM" currently appears **only** in the repository slug `AMF-PSM`; it is expanded
nowhere in the docs, source, or framework text. Phase 2 needs a name to hang off, so
this roadmap proposes one for the owner to ratify:

- **Recommended: "Positional Structural Model"** — a structural, non-predictive
  reading consistent with the charter.
- **Alternative: "Policy & Structural Model"** — fits the policy-focused issues
  (#31/#32) if the owner intends policy to be a first-class lens.

"Predictive" is deliberately avoided: the no-forecast rule forbids predictive claims.
**Action:** owner confirms the expansion; this doc and the README are updated to use it
consistently. Until then, "PSM" = "the Phase 2 body of structural work below".

## Where Phase 1 landed (context for "new" work)

Phase 1 is effectively the current `main`: the seven systems, the dependency/feedback
graph, the diagnostic engine, and a shock-propagation simulation — plus already-merged
extensions that the backlog should **not** re-propose: threshold/cascade dynamics, a
Monte Carlo `ensemble`, time-scheduled multi-wave shocks, recovery/`Intervention`
modelling, and the `amf viz` renderers. Phase 2 is the conceptual expansion below.

## Guardrail translation rules

The backlog repeatedly asks for real-market quantities. Each is admitted only as a
**dimensionless structural proxy** built from what the model already has:

| Backlog phrasing | Compliant structural reading | Where it lives |
|---|---|---|
| "liquidity / capital depth" | circulatory-system `integrity` / `redundancy` (`[0,1]`) | `systems.py` metrics |
| "transparency / disclosure" | nervous-system `integrity`; informational dependencies | `systems.py`, `DependencyKind.INFORMATIONAL` |
| "fraud / manipulation / regulation" | immune-system health + articulation points + dependency `concentration` | `diagnostics.py`, `graph.py` |
| "companies / ETFs / hedge funds / banks" | illustrative **named components** inside a system (cf. `"ETF creation/redemption"` in [`examples/sample_market.json`](../examples/sample_market.json)) | `components` list — never instruments/tickers/prices |
| "commodities / bonds / forex" | additional **market boundaries** (segments), each its own structural anatomy | `MarketBoundary`, new example markets |
| "policy / government philosophy" | `regulatory` dependencies + immune system; regimes as boundary/parameter descriptions | `DependencyKind.REGULATORY`, `MarketBoundary` |

## Issue triage

| Issue | Reads as | Compliant scope | Kind | Depends on |
|---|---|---|---|---|
| **#21** Creating phase 2 | roadmap/charter | **this document** | doc | — |
| **#23** New PSM concepts *(priority)* | expand the model's vocabulary | catalogue of compliant extensions (below) | doc → code tickets | #21 |
| **#27** Companies & subsidiaries (ETF/hedge/banks) | who the participants are | structural **component taxonomy**, illustrative names only | doc → data | #23 |
| **#25** Map global stock markets to a supply chain | geography × market as structure | per-geography/segment `MarketBoundary` examples; "supply chain" = dependency graph between segments | doc → examples | #23 |
| **#26** Commodities, bonds, forex + liquidity | non-equity segments | new example market JSONs per segment; "liquidity/capabilities" → existing metrics | examples | #25 |
| **#28** Hindenburg report → frauds/scams | detect structural fragility patterns | an **immune-system stress lens** (articulation points + concentration + feedback loops) documented as an analytical reading; no real report ingested | doc | #23 |
| **#31** Policy making | how governance couples to the market | `regulatory` dependencies + immune modelling; policy layers as structural regimes | doc | #23 |
| **#32** Government philosophies | policy regime archetypes | a small set of **illustrative regime descriptors** (boundary/parameter presets) | doc → examples | #31 |

Guardrail flags to carry into each ticket: #26/#27 must never introduce
instrument/price/ticker/portfolio names; #28 must stay illustrative and ingest no real
short-seller data; #32 must describe regimes structurally, not endorse or forecast.

## New PSM concepts for #23 (the priority) — compliant extension menu

Each reuses the "Checklist for a change" in [`CLAUDE.md`](../CLAUDE.md) (owning module →
frozen `to_dict` dataclass → `__all__` + FORBIDDEN-name check → serialise in
`market.py` → render in `report.py` → tests). Ranked by effort/value:

1. **New `DependencyKind` member** *(cheapest, non-breaking)* — e.g. an additional
   structural coupling type in `models.py`. Round-trips through the existing
   `edge_kinds()` schema with no anatomy change. Good first exemplar for #23.
2. **New per-system structural metric** — a new `[0,1]` field on `AnatomicalSystem`
   (e.g. *transparency* or *adaptability*), validated with the existing
   `_check_unit`/`validate()` idiom, serialised in `market.py`
   `to_dict`/`_parse_system`, rendered in `report.py`. Feeds #26's "transparency"
   and #31's policy reading.
3. **New diagnostic index** in `DiagnosticEngine`/`DiagnosticConfig` — e.g. a
   systemic-contagion or cross-system concentration measure built from existing
   `graph.py` primitives (centrality, articulation points, loops). Directly serves the
   #28 fraud/fragility lens.
4. **Cross-market coupling** — represent several `MarketBoundary` anatomies and the
   structural dependencies between them (the #25 "supply chain" of segments), reusing
   `DependencyGraph` at a higher level.
5. **Segment example markets** under `examples/` — commodities, bonds, FX as distinct
   structural anatomies (#26), each a plain market JSON plus a runnable script, proving
   the framework generalises beyond equities with no new instrument vocabulary.

**Non-goal (restated):** no eighth `SystemKind`.

## Sequenced Phase 2 plan

1. **2.0 — Ratify** the PSM name and this charter → closes **#21**.
2. **2.1 — New concepts** (**#23**, priority): land concept 1 (a new `DependencyKind`)
   as the exemplar, then concept 2 (a new per-system metric). Each is a small,
   test-covered PR following the checklist.
3. **2.2 — Segment examples** (**#25/#26**): add non-equity example markets and map
   "liquidity/transparency" onto the metrics from 2.1.
4. **2.3 — Component taxonomy** (**#27**): document participant categories as
   illustrative `components`.
5. **2.4 — Immune stress lens** (**#28**): document the fragility-pattern reading using
   the diagnostic from concept 3.
6. **2.5 — Policy/regulatory layer** (**#31/#32**): regulatory-dependency modelling and
   illustrative regime descriptors.

Stages 2.2–2.5 depend on 2.0–2.1 landing first.

## Per-issue next action

- **#21** — Owner ratifies PSM name + charter; then close as delivered by this doc.
- **#23** — Open a small PR adding one new `DependencyKind` (exemplar), with tests.
- **#25** — Draft one non-US-equity `MarketBoundary` example to prove the segment model.
- **#26** — Add a commodities (or FX) example market JSON + script; map liquidity → metrics.
- **#27** — Write the component-taxonomy note (participant categories as `components`).
- **#28** — Write the immune-stress-lens note referencing existing diagnostics; no data ingest.
- **#31** — Draft the regulatory-coupling model note.
- **#32** — Draft 2–3 illustrative policy-regime descriptors as boundary/parameter presets.

## Out of scope / open questions

- **GitHub Discussions** are not covered here (they could not be read programmatically in
  the planning session). If any discussion should shape Phase 2, paste its content and
  this roadmap will be extended.
- The **PSM expansion** and whether **policy (#31/#32)** is a first-class Phase 2 lens or
  a later add-on are the two decisions blocking 2.0.
