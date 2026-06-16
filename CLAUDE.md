# CLAUDE.md — contributor & design guide

Guidance for working in this repository (for both humans and AI agents).

## What this repository is

Two things live side by side:

1. **The Anatomical Market Framework (AMF) v1.0** — a proprietary analytical
   framework, captured in `AMF Framework v1.docx` and summarised in
   `anatomical-market-framework`. This is intellectual property protected by an
   OpenTimestamps proof and SHA-256 checksums.
2. **The `amf` Python package** (`src/amf/`) — a software implementation of the
   framework's *analytical method*.

## Hard rules

- **Never modify the checksum-protected artifacts.** These are:
  `AMF Framework v1.docx`, `AMF Framework v1.docx.ots`,
  `anatomical-market-framework`, and `LICENSE.txt`. They are listed in
  `SHA256SUMS`; changing any of them breaks the integrity proofs. A pre-commit
  guard and the `integrity.yml` workflow enforce this. Do not add source files to
  `SHA256SUMS`.
- **No trading system.** The `amf` package models market *structure and
  resilience* only. It must never gain orders, brokers, prices, returns, P&L,
  trading signals, or backtests. Every quantity is a dimensionless structural
  measure. `tests/unit/test_non_trading_boundary.py` enforces this on the public
  API; keep it passing.

## Package architecture (`src/amf/`)

| Module | Responsibility |
|--------|----------------|
| `models.py` | Value types: `SystemKind` (the 7 systems), `DependencyKind`, `MarketBoundary`, `Severity`, and the frozen result types (`WeaknessFinding`, `DiagnosticReport`, `Shock`, `SimulationTrace`, `ResilienceScore`). |
| `systems.py` | `AnatomicalSystem` and the seven factory functions. Structural metrics (`integrity`, `redundancy`, `criticality`, `load`) live in `[0, 1]`. |
| `graph.py` | `DependencyGraph`: feedback-loop (simple-cycle) enumeration, articulation points, Katz-style centrality, and the stress-transmission `CouplingMatrix`. Dependency-free. |
| `market.py` | `Market` aggregate root; `assemble`, `require_complete`, and the JSON `from_dict`/`to_dict` schema. |
| `diagnostics.py` | `DiagnosticEngine`: deterministic structural-weakness scoring (fragility, concentration, feedback) → `DiagnosticReport`. |
| `simulation.py` | `ShockSimulator`: damped, capacity-gated shock-propagation dynamics → resilience metrics. |
| `report.py` | Pure renderers (text / JSON / Markdown). |
| `cli.py` | `argparse` CLI exposed as the `amf` console script. |

Dependencies flow one way: `models` ← `systems`/`graph` ← `market` ←
`diagnostics`/`simulation` ← `report`/`cli`. Keep it acyclic.

## Market JSON schema (CLI input)

```json
{
  "boundary": {"asset_class": "...", "geography": "...", "timeframe": "...", "notes": "..."},
  "systems": {
    "skeleton":    {"name": "...", "components": ["..."], "integrity": 0.7, "redundancy": 0.3, "criticality": 0.9, "load": 0.1},
    "circulatory": { ... }, "nervous": { ... }, "musculature": { ... },
    "organs": { ... }, "immune": { ... }, "metabolism": { ... }
  },
  "dependencies": [
    {"source": "circulatory", "target": "skeleton", "kind": "structural", "weight": 0.8}
  ]
}
```

All seven systems must be present. A dependency means `source` relies on
`target`; `kind` is one of `structural | informational | capital | regulatory`;
`weight` is in `(0, 1]`. See `examples/sample_market.json`.

## The maths, briefly

- **Diagnostics** (deterministic): per-system `fragility = criticality·(1−health)·(1−redundancy)`;
  `concentration` is an HHI over a system's outgoing dependency weights;
  `feedback` sums the edge-weight products of the loops a system is in. The
  overall index is the criticality-weighted mean.
- **Simulation**: a stress vector `x_t ∈ [0,1]^7` evolves by
  `x_{t+1}[j] = clip(damping·(x_t[j]·retention + Σ_i x_t[i]·W[i][j]·transmission·(1−a_j)), 0, 1)`,
  where `W` is the coupling matrix and `a_j` is absorptive capacity. Damping makes
  this a contraction, so it converges; metrics are peak stress, settling time,
  absorbed fraction, and amplification factor.

## Developing

```sh
python -m pip install -e ".[dev]"
ruff check . && ruff format --check .   # lint & format (line length 120)
mypy                                    # strict type-check of src/
pytest                                  # tests + coverage gate (>= 90%)
pre-commit install                      # optional: run hooks on commit
```

Conventions: Python 3.11+, full type annotations, Google-style docstrings on
public API (enforced by ruff `D`/`ANN`). Tests omit annotations by design. Add
tests for any new behaviour and keep coverage at or above the gate.
