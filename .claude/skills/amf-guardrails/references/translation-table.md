# Guardrail translation table

How to admit a real-market request into the model without breaking the non-trading boundary.

The backlog repeatedly asks for real-market quantities. Each is admitted only as a **dimensionless
structural proxy** built from what the model already has.

## Core table

Rows 1–6 are promoted verbatim from `docs/roadmap.md` ("Guardrail translation rules"), which remains
the canonical published statement. Keep the two in sync; if they diverge, `docs/roadmap.md` wins.

| Backlog phrasing | Compliant structural reading | Where it lives |
|---|---|---|
| "liquidity / capital depth" | circulatory-system `integrity` / `redundancy` (`[0,1]`) | `systems.py` metrics |
| "transparency / disclosure" | nervous-system `integrity`; informational dependencies | `systems.py`, `DependencyKind.INFORMATIONAL` |
| "fraud / manipulation / regulation" | immune-system health + articulation points + dependency `concentration` | `diagnostics.py`, `graph.py` |
| "companies / ETFs / hedge funds / banks" | illustrative **named components** inside a system | `components` list — never instruments/tickers/prices |
| "commodities / bonds / forex" | additional **market boundaries** (segments), each its own structural anatomy | `MarketBoundary`, new example markets |
| "policy / government philosophy" | `regulatory` dependencies + immune system; regimes as boundary/parameter descriptions | `DependencyKind.REGULATORY`, `MarketBoundary` |

## Extension rows

Added for the technology, quantitative, and computational source material. Same rule: the structural
reading must be dimensionless, deterministic, and free of the forbidden substrings.

| Backlog phrasing | Compliant structural reading | Where it lives |
|---|---|---|
| "prediction / forecasting / price target" | **Not admissible as a capability.** Admit only as a *scenario trajectory* under a stated shock: `propagate()` output is a conditional what-if, never a forecast | `simulation.py`; disclaimers unchanged |
| "returns / P&L / performance" | **Not admissible.** If the intent is "did the market absorb the shock", use `absorbed_fraction` and `amplification` | `ResilienceScore` |
| "order flow / execution / spoofing / latency arbitrage" | nervous-system `integrity` (information quality) and `load`; venue opacity as reduced immune-system detection | `systems.py` |
| "market crash / flash crash" | a `Shock` with high magnitude and a short horizon; the cascade threshold governs non-linearity | `Shock`, `SimulationConfig.cascade_threshold` |
| "volatility index / VIX / credit spread" | a dimensionless `[0,1]` stress input, explicitly labelled an illustrative proxy — never the instrument itself | `Shock.magnitude` |
| "ML model / neural network / embedding" | model **monoculture** is a redundancy failure: many participants sharing one decision rule reduces `redundancy` and correlates responses | `systems.py` `redundancy` |
| "crowding / herding / passive flows" | reduced `redundancy` plus raised coupling weight between affected systems | `redundancy`, `CouplingMatrix` |
| "quantum superposition / state vector" | a metaphor for *unresolved structural state*. Admit only if it reduces to a deterministic `[0,1]` measure; otherwise record as a research question, not a model change | `open-questions.md` |
| "entropy / information content" | nervous-system `integrity` as observability; graph `concentration` as unevenness of reliance | `diagnostics.py` |
| "network topology / persistent homology" | already native: feedback loops, articulation points, Katz-style `centrality` | `graph.py` |
| "capital flight / bank run" | a self-reinforcing cascade: `cascade_threshold` crossing, with `cascade_gain` amplification and `cascade_absorption_drop` | `simulation.py` |
| "sanctions / capital controls" | removal or reweighting of `regulatory` edges — the one instrument that deletes graph edges outright | `DependencyKind.REGULATORY` |
| "climate transition vs physical risk" | two distinct shock channels applied to different systems; transition is policy-mediated, physical is exogenous | `stress_test()`, `Shock.at_step` |
| "ecosystem services / unpriced dependency" | a dependency edge that exists in the graph whether or not anyone has valued it — the structural argument *is* the finding | `DependencyGraph` |

## How to use this table

1. Find the row whose phrasing matches the source material.
2. If the "compliant structural reading" says **not admissible**, the unit is flagged, not translated:
   apply `guardrail-review` and write the `## Structural reframing required` section.
3. If a translation exists, state **both** in the issue — what the source asked for, and the
   structural reading — so a human can overrule the mapping.
4. If no row matches, do not invent one. Record the gap in `.claude/memory/open-questions.md` and
   flag the unit. A wrong translation is worse than an open question, because it looks settled.

## The recurring pattern worth naming

**Monoculture is a redundancy failure**, and it shows up in at least four independent domains in this
backlog: regulatory monoculture (one agency covering an entire listed universe), model monoculture
(everyone running the same ML model), passive-investing monoculture, and agricultural monoculture in
the biodiversity material. All four reduce to the same structural statement: *low `redundancy` on a
high-`criticality` node*. Recognising this prevents four unrelated-looking metrics being invented for
one phenomenon.

## Forbidden-substring index

Direct lookup for every substring in the `FORBIDDEN` tuple of
`tests/unit/test_non_trading_boundary.py`. If you are about to name something and the name contains
one of these, find it here first. "Not admissible" means no identifier may carry the concept — the
idea belongs in prose or in a research document, never in a public name.

| Forbidden substring | Structural reading | Admissible as an identifier? |
|---|---|---|
| `order` | Sequencing of rows/columns or of iteration. The one allowlisted use is `CouplingMatrix.order`. As *order flow*: nervous-system `integrity` and `load` | Only for ordering, never for trade orders |
| `buy` | A directional participant action. The structural residue is a change in `load` on the circulatory system | No |
| `sell` | As above; under stress, a self-reinforcing exit is a cascade threshold crossing | No |
| `price` | Not a model quantity. Valuation pressure enters as dimensionless `load`; "unpriced dependency" is simply a graph edge | No |
| `pnl` | Outcome accounting. Use `absorbed_fraction` / `amplification` if the intent is "did the market withstand it" | No |
| `broker` | An intermediary institution — model as a **named component** inside a system, e.g. `components=["clearing"]` | No; use `components` |
| `backtest` | Historical replay for validation. The compliant analogue is a documented case study in `docs/research/`, explicitly illustrative | No |
| `ticker` | An instrument identifier. Markets are modelled as `MarketBoundary` segments, never instruments | No |
| `trade` | A transaction. Structurally: an edge carrying `load`, or a coupling weight | No |
| `portfolio` | A holdings collection. The structural analogue is the set of systems inside a `MarketBoundary` | No |
| `candlestick` | Price-series presentation. `viz` renders structure and stress trajectories only | No |
| `returns` | Performance over time. Use the stress trajectory `x_t` and `ResilienceScore` | No |
| `signal` | A trading indicator. For "this metric crossed a threshold", use `WeaknessFinding` and `Severity` | No; use finding/severity vocabulary |

Two reminders that prevent false alarms:

- The check matches **substrings of lowercased identifiers**, never prose. `reorder`, `border`, and
  `recorder` all contain `order` and would trip it; a paragraph discussing order flow would not.
- Prose in issue bodies, dossiers, and `docs/` is unrestricted. This table governs what may be
  *named* in `src/amf/`, and what an issue may claim the package does.
