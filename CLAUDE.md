# CLAUDE.md — contributor & design guide

Guidance for working in this repository (for both humans and AI agents).

## What this repository is

Two things live side by side:

1. **The Anatomical Market Framework (AMF) v1.0** — a proprietary analytical
   framework, captured in `AMF Framework v1.docx` and summarised in
   `anatomical-market-framework`. This is intellectual property protected by an
   OpenTimestamps proof and SHA-256 checksums.
2. **The `amf` Python package** (`src/amf/`) — a software implementation of the
   framework's *analytical method*. Zero runtime dependencies; standard library
   only.

## Hard rules

- **Never modify the checksum-protected artifacts.** These are:
  `AMF Framework v1.docx`, `AMF Framework v1.docx.ots`,
  `anatomical-market-framework`, and `LICENSE.txt`. They are listed in
  `SHA256SUMS`; changing any of them breaks the integrity proofs. Three
  mechanisms enforce this: a `language: fail` pre-commit hook
  (`protect-ip-artifacts`, which also covers `SHA256SUMS` itself), exclusions on
  the whitespace-fixing hooks, and the `integrity.yml` workflow
  (`sha256sum --check --strict SHA256SUMS`). `.gitattributes` additionally marks
  them binary / `-text` so no EOL normalisation can alter their bytes. Do not add
  source files to `SHA256SUMS`.
- **No trading system.** The `amf` package models market *structure and
  resilience* only. It must never gain orders, brokers, prices, returns, P&L,
  trading signals, or backtests. Every quantity is a dimensionless structural
  measure. `tests/unit/test_non_trading_boundary.py` enforces this mechanically:
  it scans `amf.__all__` and every public dataclass's field names for a
  `FORBIDDEN` substring list (`order`, `buy`, `sell`, `price`, `pnl`, `broker`,
  `backtest`, `ticker`, `trade`, `portfolio`, `candlestick`). Keep it passing —
  and note it constrains *naming*, so pick structural vocabulary.
- **Illustrative, not validated.** Treat `amf` as an educational tool. Its
  thresholds, weights, and scores are not empirically validated; its output is not
  financial advice and not a diagnosis or forecast of any real market. Keep the
  disclaimers (package docstring, README, and the CLI's `_DISCLAIMER`) in place,
  and do not add language that claims predictive power or validated performance.
- **Never read the framework document to generate output.** The CLI's `describe`
  text comes from paraphrased constants in `cli.py` (`_SYSTEM_SUMMARY`,
  `_METHOD_STEPS`), deliberately so the software never touches the protected
  artifacts.

## Repository layout

```
src/amf/            the Python package (see table below); ships py.typed
tests/unit/         one file per module
tests/integration/  test_cli.py, test_end_to_end.py
tests/conftest.py   shared fixtures: boundary, healthy_market, stressed_market
examples/           sample_market.json + two runnable scripts
.github/workflows/  ci.yml (lint/typecheck/test/validate), integrity.yml
.github/mlc-config.json   markdown-link-check config used by the validate job
.pre-commit-config.yaml   ruff, ruff-format, mypy (src only), yamllint,
                          hygiene hooks, protect-ip-artifacts
.yamllint.yml       yamllint config (line length 140, `on:` truthy allowed)
.gitattributes      binary / EOL rules that keep the IP checksums stable
SHA256SUMS          the four protected artifacts and their digests
```

## Package architecture (`src/amf/`)

| Module | Responsibility |
|--------|----------------|
| `errors.py` | Typed exception hierarchy. Every public-API failure derives from `AMFError` (`InvalidSystemError`, `InvalidDependencyError`, `IncompleteMarketError`, `InvalidShockError`, `MarketParseError`, `InvalidConfigError`). Has no internal dependencies. |
| `models.py` | Value types: `SystemKind` (the 7 systems), `DependencyKind`, `Dependency`, `MarketBoundary`, `Severity`, and the frozen result types (`WeaknessFinding`, `DiagnosticReport`, `Shock`, `SimulationTrace`, `ResilienceScore`). All are `@dataclass(frozen=True, slots=True)` with a `to_dict()`. |
| `systems.py` | `AnatomicalSystem` and the seven factory functions (`skeleton`, `circulatory`, `nervous`, `musculature`, `organs`, `immune`, `metabolism`). Structural metrics (`integrity`, `redundancy`, `criticality`, `load`) live in `[0, 1]`; derived `health()` and `absorptive_capacity()`. |
| `graph.py` | `DependencyGraph`: feedback-loop (simple-cycle) enumeration, articulation points, Katz-style centrality, and the stress-transmission `CouplingMatrix`. Dependency-free. |
| `market.py` | `Market` aggregate root; `assemble`, `require_complete` (which also re-validates each system, catching post-construction mutation at the engine boundary), `system`, and the JSON `from_dict`/`to_dict` schema. |
| `diagnostics.py` | `DiagnosticEngine` (+ tunable `DiagnosticConfig`): deterministic structural-weakness scoring (fragility, concentration, feedback) → `DiagnosticReport`. |
| `simulation.py` | `ShockSimulator` (+ tunable `SimulationConfig`): damped, capacity-gated shock-propagation dynamics → `SimulationTrace` / `ResilienceScore`; `stress_test()` shocks every system in turn. |
| `report.py` | Pure renderers: `render_text`, `render_json`, `render_markdown`, `render_stress_test`. |
| `viz.py` | Pure visual renderers: dependency graph as DOT / Mermaid / SVG, stress timeline as SVG. Dependency-free. |
| `cli.py` | `argparse` CLI exposed as the `amf` console script. |

The public API is re-exported from `amf/__init__.py` (`__all__`); import types and
engines from `amf`, not submodules. The renderers are the exception — they live
in `amf.report` and `amf.viz` and are imported from there (as `cli.py` and
`examples/` do). Dependencies flow one way: `errors`/`models` ←
`systems`/`graph` ← `market` ← `diagnostics`/`simulation` ← `report`/`viz`/`cli`.
Keep it acyclic.

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
`weight` is in `(0, 1]`. `to_dict`/`from_dict` round-trips losslessly (including
each dependency's `kind`) — keep it that way. See `examples/sample_market.json`.

Within a system entry every field is optional, and an omitted one takes the same
default as the corresponding factory in `systems.py` — parsing goes through
`SYSTEM_FACTORIES`, so a market built from JSON and one built from the factories
are identical. Defaults are `integrity` 1.0, `redundancy` 0.5, `load` 0.0,
`components` empty, and a per-system `name` and `criticality` (0.60–0.90; e.g.
`skeleton` is "Market infrastructure" at 0.90). Because `criticality` weights the
overall diagnostic index, omitting it is a meaningful choice rather than a
neutral one. Any unrecognised field in a system entry is a `MarketParseError`,
so a typo such as `integritty` fails loudly instead of being ignored.

A `(source, target)` pair may appear more than once with different `kind`s. Each
is kept as its own edge and survives a `to_dict`/`from_dict` round trip, while
every structural query (`edge_weight`, feedback loops, centrality, articulation
points) aggregates across kinds, capped at 1.0 — so splitting one coupling across
kinds never changes a score.

## Using the CLI

The `amf` console script prints the `_DISCLAIMER` to stderr (so `--format json`
stdout stays machine-parseable) after every analytical command, and offers five
subcommands:

```sh
amf diagnose    examples/sample_market.json [--format text|json|md]
amf simulate    examples/sample_market.json --target circulatory [--magnitude 0.8] [--format ...]
amf stress-test examples/sample_market.json [--magnitude 0.8] [--format ...]  # shocks each system in turn
amf describe                                                    # explains the 7 systems & method
amf version
```

`--target` accepts any `SystemKind` value; `--magnitude` is in `(0, 1]`.
`main(argv)` returns an exit code rather than calling `sys.exit`, so it is unit
tested in-process: `0` on success, `2` on a handled `AMFError`, `1` on bad usage
(no subcommand). Runnable scripts live in `examples/` (`equity_market.py`
builds a market in code and diagnoses it; `liquidity_shock.py` imports that
builder and runs a shock + stress test).

## The maths, briefly

- **Per-system derived metrics**: `health = integrity·(1 − load)`;
  `absorptive_capacity = 0.5·redundancy + 0.3·integrity + 0.2·(1 − load)` (weights
  sum to 1, so the result stays in `[0, 1]`).
- **Config validation**: `DiagnosticConfig` rejects negative weights and
  `SimulationConfig` rejects `max_steps < 1`, `damping` outside `(0, 1]`, and
  negative `retention`/`transmission`/`jitter`, all as `InvalidConfigError`. These
  keep every score inside `[0, 1]` and keep the dynamics a contraction.
- **Diagnostics** (deterministic): per-system
  `fragility = criticality·(1 − health)·(1 − redundancy)`; `concentration` is an
  HHI over a system's outgoing dependency weights; `feedback` sums the edge-weight
  products of the loops a system is in. These combine under `DiagnosticConfig`
  weights (`0.4 / 0.3 / 0.3`, normalised by their sum) into a per-system score;
  findings are sorted by score descending, and the report's overall index is the
  criticality-weighted mean of those scores. A single point of failure is an
  articulation point with redundancy below `_LOW_REDUNDANCY` (0.5).
- **Centrality**: Katz-style "being depended upon" influence, max-normalised to
  `[0, 1]`, attenuated by `alpha` (default 0.4) per hop. Chosen over eigenvector
  centrality because it is well defined on acyclic graphs.
- **Simulation**: a stress vector `x_t ∈ [0,1]^7` evolves by
  `x_{t+1}[j] = clip(damping·(x_t[j]·retention + Σ_i x_t[i]·W[i][j]·transmission·(1−a_j)), 0, 1)`,
  where `W` is the coupling matrix (stress flows target → source, the reverse of
  the dependency edge) and `a_j` is absorptive capacity. Metrics are peak stress,
  settling time, absorbed fraction, and amplification factor. `SimulationConfig`
  defaults: `max_steps=50, damping=0.85, retention=0.5, transmission=1.0,
  convergence_eps=1e-4, seed=None, jitter=0.0` — with `jitter=0.0` the simulation
  is fully deterministic, which the tests rely on; `jitter` has no effect unless
  `seed` is also set.
  Damping and absorptive capacity damp the trajectory, but the step map is *not* a
  contraction for every market: with enough incoming weight and little absorptive
  capacity the per-step gain exceeds one and stress grows until it saturates at the
  `1.0` clip. `converged` therefore reports whether the trajectory settled within
  `max_steps`, not whether it is stable — a slowly-settling market can exhaust the
  budget, which yields a settling time of `-1` and the full settling penalty.
- **Severity bands** (`Severity.from_score`, on a normalised `[0, 1]` score):
  `< 0.25` low, `< 0.50` moderate, `< 0.75` elevated, else critical. The mapping is
  total and saturating: input below `0` reports low, above `1` reports critical, and
  `NaN` falls through to critical.

## Developing

```sh
python -m pip install -e ".[dev]"
ruff check . && ruff format --check .   # lint & format (line length 120)
mypy                                    # strict type-check of src/ only
pytest                                  # tests + branch coverage gate (100%)
pre-commit install                      # optional: run hooks on commit
```

Conventions: Python 3.11+ (CI tests 3.11/3.12/3.13), full type annotations,
Google-style docstrings on public API. Ruff selects
`E,F,W,I,N,UP,B,C4,SIM,TC,PTH,RUF,ANN,D` (ignoring `D203`, `D213`), with `ANN`/`D`
waived under `tests/**` and `examples/**` — tests and examples omit annotations
and module docstring rules by design. `mypy` is `strict` with `warn_unreachable`
and `disallow_any_generics`, and checks `files = ["src"]` only; tests and examples
are covered by ruff and exercised by pytest instead. Add tests for any new
behaviour and keep coverage at or above the gate. Use the `integration` pytest
marker for cross-module tests (`--strict-markers` is on).

### Checklist for a change

1. Put new behaviour in the module that owns it; respect the one-way dependency
   order and do not import `report`/`cli` from lower layers.
2. Export new public types from `amf/__init__.py` and add them to `__all__`
   (kept sorted). Check the name against the non-trading `FORBIDDEN` list.
3. New result types are frozen, slotted dataclasses with a `to_dict()`; if they
   are serialised, extend `report._to_jsonable` and the text/Markdown renderers.
4. Raise a typed `AMFError` subclass, never a bare `ValueError`, across the
   public API.
5. Add unit tests in the matching `tests/unit/test_<module>.py`, plus an
   integration test if the CLI or an end-to-end path changed.
6. Run ruff, mypy, and pytest locally before pushing.
7. Record user-visible changes under `## [Unreleased]` in `CHANGELOG.md`
   (Added / Changed / Fixed).

### Versioning

The package version appears in `pyproject.toml` (`version`) and
`amf/__init__.py` (`__version__`, printed by `amf version`) — keep them in sync.
`CITATION.cff`'s `version` tracks the *framework* release (1.0), not the package,
and is validated by `cffconvert` in CI.

## CI

Two workflows gate every push and pull request:

- `.github/workflows/ci.yml` — four jobs: **lint** (`ruff check` + `ruff format
  --check`), **typecheck** (`mypy`), **test** (`pytest` on the 3.11/3.12/3.13
  matrix, uploading `coverage.xml` from 3.12), and **validate** (`yamllint .`,
  `cffconvert --validate -i CITATION.cff`, and a Markdown link check). `cffconvert`
  is installed standalone in that job rather than in the `dev` extra, because a
  transitive dependency fails to build under some patched local setuptools.
- `.github/workflows/integrity.yml` — verifies the `SHA256SUMS` artifacts are
  untouched.

Project metadata lives in `CITATION.cff`, `CHANGELOG.md`, and `SECURITY.md`.
