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
  the document and its proof `binary` and the plain-text overview `-text`, so no
  EOL normalisation can alter their bytes. Do not add source files to
  `SHA256SUMS`.
- **No trading system.** The `amf` package models market *structure and
  resilience* only. It must never gain orders, brokers, prices, returns, P&L,
  trading signals, or backtests. Every quantity is a dimensionless structural
  measure. `tests/unit/test_non_trading_boundary.py` enforces this mechanically:
  it walks every public class reachable from `amf.__all__` and checks the public
  names *and* every member and dataclass field they define against a `FORBIDDEN`
  substring list — `order`, `buy`, `sell`, `price`, `pnl`, `broker`, `backtest`,
  `ticker`, `trade`, `portfolio`, `candlestick`, `returns`, `signal`. One
  documented exception lives in that file's `ALLOWLIST` (`CouplingMatrix.order`,
  the matrix's row/column ordering); a meta-test asserts every allowlist entry
  still exists, so stale exemptions fail. Keep the guard passing — and note it
  constrains *naming*, so pick structural vocabulary (`load`, `stress`,
  `absorptive_capacity`), never market-data vocabulary.
- **Illustrative, not validated.** Treat `amf` as an educational tool. Its
  thresholds, weights, and scores are not empirically validated; its output is not
  financial advice and not a diagnosis or forecast of any real market. Keep the
  disclaimers (package docstring, README, the CLI's `_DISCLAIMER`, and `viz`'s
  `_FOOTNOTE` baked into every rendered image) in place, and do not add language
  that claims predictive power or validated performance.
- **Never read the framework document to generate output.** The CLI's `describe`
  text comes from paraphrased constants in `cli.py` (`_SYSTEM_SUMMARY`,
  `_METHOD_STEPS`), deliberately so the software never touches the protected
  artifacts.

## Repository layout

```
src/amf/            the Python package (see table below); ships py.typed
tests/conftest.py   fixtures: boundary, market_factory, healthy_market,
                    stressed_market; plus the importable build_market() helper
                    (hypothesis rejects function-scoped fixtures under @given)
tests/unit/         one file per module, plus test_non_trading_boundary.py
                    (the naming guard), test_properties.py (hypothesis), and
                    test_packaging.py (packaging / metadata invariants)
tests/integration/  test_cli.py (main() in-process), test_console_script.py
                    (the installed `amf` entry point, as a subprocess),
                    test_end_to_end.py, test_examples.py (runs examples/)
examples/           sample_market.json + three runnable scripts
pyproject.toml      packaging + ruff / mypy / pytest / coverage config
.github/workflows/  ci.yml (lint/typecheck/test/validate), integrity.yml
.github/mlc-config.json   markdown-link-check config used by the validate job
.pre-commit-config.yaml   ruff, ruff-format, mypy (src only), yamllint,
                          hygiene hooks, protect-ip-artifacts
.yamllint.yml       yamllint config (line length 140, `on:` truthy allowed)
.gitattributes      binary / EOL rules that keep the IP checksums stable
SHA256SUMS          the four protected artifacts and their digests
README.md, CHANGELOG.md, CITATION.cff, SECURITY.md   project metadata
```

## Package architecture (`src/amf/`)

| Module | Responsibility |
|--------|----------------|
| `errors.py` | Typed exception hierarchy. Every public-API failure derives from `AMFError` (`InvalidSystemError`, `InvalidDependencyError`, `IncompleteMarketError`, `InvalidShockError`, `InvalidConfigError`, `MarketParseError`). Has no internal dependencies. |
| `models.py` | Value types: `SystemKind` (the 7 systems), `DependencyKind`, `Dependency`, `MarketBoundary`, `Severity`, and the frozen result types (`WeaknessFinding`, `DiagnosticReport`, `Shock`, `Intervention`, `SimulationTrace`, `ResilienceScore`, `MetricStats`, `ResilienceDistribution`). All are `@dataclass(frozen=True, slots=True)` with a `to_dict()`. |
| `systems.py` | `AnatomicalSystem` (frozen; validated in `__post_init__`), the seven factory functions (`skeleton`, `circulatory`, `nervous`, `musculature`, `organs`, `immune`, `metabolism`), and the `SYSTEM_FACTORIES` registry that keys them by kind. Structural metrics (`integrity`, `redundancy`, `criticality`, `load`) live in `[0, 1]`; derived `health()` and `absorptive_capacity()`. An unrecognised metric keyword raises `InvalidSystemError` rather than being silently dropped. |
| `graph.py` | `DependencyGraph`: edges keyed by `(source, target, kind)`, with `dependencies()`, `edge_weight`, `edge_kinds`, `dependencies_of`, `dependents_of`, feedback-loop (simple-cycle) enumeration, articulation points, Katz-style `centrality`, and the stress-transmission `CouplingMatrix`. Dependency-free. |
| `market.py` | `Market` aggregate root; `assemble`, `require_complete`, `system`, and the JSON `from_dict`/`to_dict` schema. `assemble` stores the seven systems in `SystemKind` declaration order and `require_complete` rejects a system filed under a key that is not its own `kind`. The one mutable dataclass in the package (`slots=True`, not frozen) — it is a container, and its parts are immutable. |
| `diagnostics.py` | `DiagnosticEngine` (+ tunable, validated `DiagnosticConfig`): deterministic structural-weakness scoring (`fragility`, `concentration`, `feedback_amplification`, `single_points_of_failure`) → `DiagnosticReport`. Both the findings ranking and the SPOF ranking break ties by `SystemKind` declaration order. |
| `simulation.py` | `ShockSimulator` (+ tunable, validated `SimulationConfig`): damped, capacity-gated shock-propagation dynamics; `propagate()` → `SimulationTrace`, `resilience()` → `ResilienceScore`, `stress_test()` shocks every system in turn, `ensemble()` runs a seeded Monte Carlo → `ResilienceDistribution`. Opt-in extensions: cascade/threshold dynamics, recovery, multi-wave shocks (`Shock.at_step`), and `Intervention`s. |
| `report.py` | Pure textual renderers: `render_text`, `render_json`, `render_markdown`, `render_stress_test`, `render_distribution`, plus the `Renderable` type alias naming the result types the text/Markdown/JSON renderers accept (`ResilienceDistribution` is deliberately excluded — only `render_json` serialises one). No I/O. |
| `viz.py` | Pure visual renderers: `render_dot`, `render_mermaid`, `render_graph_svg` (dependency graph, severity-coloured when given a `DiagnosticReport`), `render_timeline_svg` (stress timeline). SVG is drawn with the standard library alone — no Graphviz, no matplotlib. |
| `cli.py` | `argparse` CLI exposed as the `amf` console script. |

The public API is re-exported from `amf/__init__.py` (`__all__`); import types and
engines from `amf`, not submodules. The renderers are the exception — they live
in `amf.report` and `amf.viz` and are imported from there (as `cli.py` and
`examples/` do). Dependencies flow one way: `errors`/`models` ←
`systems`/`graph` ← `market` ← `diagnostics`/`simulation` ← `report`/`viz`/`cli`.
Keep it acyclic.

## Determinism and parameter validation

The toolkit is a diagnostic instrument, so identical inputs must give identical
output — bit for bit — and a nonsensical knob must fail rather than produce a
plausible-looking number. Several design choices exist only to protect that, and
are easy to break by accident:

- **Equal markets produce equal output.** Nothing user-visible may depend on the
  order a market was assembled in. `DependencyGraph` canonicalises its own
  orderings (`dependencies` by `(source, target, kind)` declaration order,
  `dependencies_of` / `dependents_of` by system declaration order);
  `Market.assemble` stores the seven systems in `SystemKind` declaration order
  and `to_dict` emits them in it; `DiagnosticEngine.diagnose` breaks ties in both
  the findings ranking and the SPOF ranking by declaration order. This is not
  cosmetic on either count: the diagnostic HHI sums over those lists and
  floating-point addition is not associative, so insertion-ordered traversal made
  a diagnosis differ in the last bits; and `musculature` and `metabolism` share a
  criticality of 0.60, so ranking ties are routine. A dict-insertion-order
  tie-break is a bug, not a detail — `tests/unit/test_properties.py` asserts that
  a market and any permutation of it diagnose identically.
- **Tuning knobs are validated on construction, never normalised into nonsense.**
  `DiagnosticConfig` requires finite, non-negative weights (an all-zero triple is
  still allowed and yields zero scores); `SimulationConfig` validates every
  dynamics parameter (`max_steps >= 1`, `damping` in `(0, 1]`, `retention` in
  `[0, 1]`, finite non-negative `transmission` and `jitter`,
  `convergence_eps > 0`, `cascade_threshold` `None` or in `(0, 1)`, and so on);
  `DependencyGraph.centrality` requires `alpha` in `(0, 1)`, `iterations >= 1`,
  and a finite non-negative `tolerance`. All raise `InvalidConfigError`. These
  are not cosmetic either: a negative blend weight used to yield findings scoring
  `2.0`, and `alpha >= 10` overflowed the influence series to infinity and
  returned `NaN` for every system. Keeping every score inside `[0, 1]` is what
  lets `Severity.from_score` and `WeaknessFinding` rely on that interval.
- **Jitter needs a seed.** `SimulationConfig.jitter` has no effect unless `seed`
  is also set, so the default configuration is fully deterministic; the tests
  rely on it.
- **Renderers are pure.** Nothing in `report.py` or `viz.py` performs I/O, reads
  the clock, or uses randomness; `viz` tests assert byte-identical repeat renders.

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
so a typo such as `integritty` fails loudly instead of being ignored, as is a
`components` value that is not a list — a bare string is iterable, so accepting one
would silently split `"abc"` into three single-character components.

A `(source, target)` pair may appear more than once with different `kind`s. Each
is kept as its own edge and survives a `to_dict`/`from_dict` round trip, while
every structural query (`edge_weight`, feedback loops, centrality, articulation
points) aggregates across kinds, capped at 1.0 — so splitting one coupling across
kinds never changes a score.

Every parse failure — malformed structure, a non-numeric metric, an unknown kind,
an out-of-range value — surfaces as `MarketParseError`. `Market.from_dict` wraps
`KeyError`/`TypeError`/`ValueError` and re-raises domain `AMFError`s as parse
errors, and the CLI's `_load_market` additionally maps `OSError`,
`UnicodeDecodeError` (a `ValueError`, so it does not fall under `OSError`), and
`json.JSONDecodeError` onto it — so no raw exception escapes the schema
boundary.

## Using the CLI

The `amf` console script prints the `_DISCLAIMER` to stderr (so `--format json`
stdout stays machine-parseable) after every analytical command, and offers seven
subcommands:

```sh
amf diagnose    examples/sample_market.json [--format text|json|md]
amf simulate    examples/sample_market.json --target circulatory [--magnitude 0.8] \
                [--cascade-threshold 0.2] [--cascade-gain 0.5] [--recovery 0.0] \
                [--seed N] [--jitter 0.0] [--format ...]
amf stress-test examples/sample_market.json [--magnitude 0.8] [--format ...]  # shocks each system in turn
amf ensemble    examples/sample_market.json --target circulatory [--runs 100] [--seed 0] [--jitter 0.05] [--format text|json]
amf viz         examples/sample_market.json [--format svg|dot|mermaid] [--output FILE] \
                [--timeline SYSTEM [--magnitude 0.8]]
amf describe                                                    # explains the 7 systems & method
amf version
```

`viz` renders the severity-coloured dependency graph by default (it runs a
diagnosis to colour the nodes); `--timeline SYSTEM` instead propagates a shock to
that system and plots the stress trajectory as SVG. Without `--output` the
document goes to stdout; with it, the file is written and a `wrote <path>` note
goes to stderr. Note `viz` has its own `--format` values (`svg|dot|mermaid`), and
`ensemble` accepts only `text|json` — the shared `text|json|md` triple belongs to
`diagnose`, `simulate`, and `stress-test`.

Multi-wave (`Shock.at_step`) and `Intervention`s are exposed through the Python API
and `examples/cascade_scenario.py`, not the CLI. `--target` accepts any
`SystemKind` value; `--magnitude` is in `(0, 1]`.
`main(argv)` returns an exit code rather than calling `sys.exit`, so it is unit
tested in-process: `0` on success, `2` on a handled `AMFError`, `1` on bad usage
(no subcommand); argparse itself exits `2` on an unknown flag or choice.

Runnable scripts live in `examples/`: `equity_market.py` builds a market in code
and diagnoses it; `liquidity_shock.py` imports that builder and runs a shock plus
a stress test; `cascade_scenario.py` contrasts linear and cascade dynamics and
demonstrates multi-wave shocks, interventions, and the ensemble. The sibling
imports only resolve when a script is run directly (its own directory lands on
`sys.path`), which is why `tests/integration/test_examples.py` runs them as
subprocesses. That test currently covers `equity_market.py` and
`liquidity_shock.py` — add a case there if you add or substantially change an
example.

## The maths, briefly

- **Per-system derived metrics**: `health = integrity·(1 − load)`;
  `absorptive_capacity = 0.5·redundancy + 0.3·integrity + 0.2·(1 − load)` (weights
  sum to 1, so the result stays in `[0, 1]`).
- **Diagnostics** (deterministic): per-system
  `fragility = criticality·(1 − health)·(1 − redundancy)`; `concentration` is an
  HHI over a system's outgoing dependency weights; `feedback` sums the edge-weight
  products of the loops a system is in. These combine under `DiagnosticConfig`
  weights (`0.4 / 0.3 / 0.3`, normalised by their sum) into a per-system score;
  findings are sorted by score descending, and the report's overall index is the
  criticality-weighted mean of those scores. A single point of failure is an
  articulation point with redundancy below `_LOW_REDUNDANCY` (0.5); SPOFs are
  ranked by criticality. Both rankings break ties by `SystemKind` declaration
  order, so equal markets rank identically. Each finding also carries `drivers`,
  plain-language strings emitted when a component crosses its explanation
  threshold.
- **Centrality**: Katz-style "being depended upon" influence, max-normalised to
  `[0, 1]`, attenuated by `alpha` (default 0.4) per hop. Chosen over eigenvector
  centrality because it is well defined on acyclic graphs.
- **Simulation**: a stress vector `x_t ∈ [0,1]^7` evolves by
  `x_{t+1}[j] = clip(damping·(x_t[j]·retention + Σ_i x_t[i]·W[i][j]·transmission·(1−a_j)), 0, 1)`,
  where `W` is the coupling matrix (stress flows target → source, the reverse of
  the dependency edge) and `a_j` is absorptive capacity. Metrics are peak stress,
  settling time, absorbed fraction, and amplification factor; the composite
  resilience is `0.6·absorbed + 0.25·(1 − amp_penalty) + 0.15·(1 − settle_penalty)`.
  `SimulationConfig` defaults: `max_steps=50, damping=0.85, retention=0.5,
  transmission=1.0, convergence_eps=1e-4, seed=None, jitter=0.0` — with
  `jitter=0.0` the simulation is fully deterministic, which the tests rely on;
  `jitter` has no effect unless `seed` is also set.
  Damping and absorptive capacity damp the trajectory, but the step map is *not* a
  contraction for every market: with enough incoming weight and little absorptive
  capacity the per-step gain exceeds one and stress grows until it saturates at the
  `1.0` clip. `converged` therefore reports whether the trajectory settled within
  `max_steps`, not whether it is stable — a slowly-settling market can exhaust the
  budget, which yields a settling time of `-1` and the full settling penalty.
- **Simulation extensions** (all opt-in; defaults reproduce the linear model above
  exactly, so existing tests stay green): `cascade_threshold` enables nonlinear
  cascade dynamics — a system above the threshold amplifies outgoing stress by
  `1 + cascade_gain` and has its absorption cut by `cascade_absorption_drop`,
  reported as `ResilienceScore.tipped_systems` (convergence is *not* guaranteed
  here — the trajectory may settle at a persistent non-zero state); `recovery_rate`
  subtracts an active healing term each step; `Shock.at_step` injects a shock at a
  later timestep (multi-wave, and the horizon extends to cover the last injection);
  `Intervention` boosts a system's absorptive capacity from its `at_step`; and
  `ShockSimulator.ensemble(...)` runs seeded, jittered replications (replication
  `i` uses `base_seed + i`) into a `ResilienceDistribution` (percentiles computed
  in-house by linear interpolation, no numpy). Amplification/absorption use total
  injected load as a timing-independent denominator.
- **Severity bands** (`Severity.from_score`, on a normalised `[0, 1]` score):
  `< 0.25` low, `< 0.50` moderate, `< 0.75` elevated, else critical. Weakness
  scores feed it directly; resilience feeds it `1 − value`, so a resilient market
  bands as low severity. The mapping is total and saturates pessimistically: a
  score below `0` reports low, above `1` reports critical, and `NaN` — which
  compares false against every threshold — falls through to critical, on the
  grounds that a score which escaped `[0, 1]` means a broken upstream computation
  and under-reporting it is the more dangerous failure.

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
are covered by ruff and exercised by pytest instead. Use the `integration` pytest
marker for cross-module tests (`--strict-markers` is on).

The only dev-time test dependency beyond pytest is `hypothesis`, used by
`tests/unit/test_properties.py` to check the invariants the docstrings promise:
stress stays in `[0, 1]` at every step, diagnostic scores stay in `[0, 1]` for any
blend of config weights, `to_dict`/`from_dict` is a fixed point, feedback-loop
enumeration matches a brute-force search of every simple cycle, and a market
diagnoses identically under any permutation of its assembly order. Because
hypothesis cannot use function-scoped fixtures under `@given`, `conftest.py`
exposes `build_market()` as a plain importable function alongside the
`market_factory` fixture — use the function inside `@given` and the fixture
everywhere else.

The coverage gate is **100%** statement and branch coverage of `src/amf`
(`--cov-fail-under=100` in `pyproject.toml`), so any uncovered line or branch fails
the build outright. New code therefore ships with its tests or not at all; the fix
for a failing gate is a test, never a lower threshold. Note that 100% coverage is
not the same as 100% tested — `tests/unit/test_packaging.py` and the mutation-driven
tests exist precisely because full coverage was hiding real gaps.

### Checklist for a change

1. Put new behaviour in the module that owns it; respect the one-way dependency
   order and do not import `report`/`viz`/`cli` from lower layers.
2. Export new public types from `amf/__init__.py` and add them to `__all__`
   (kept sorted). Check the name against the non-trading `FORBIDDEN` list.
3. New result types are frozen, slotted dataclasses with a `to_dict()`; if they
   are serialised, extend `report._to_jsonable` and the text/Markdown renderers.
4. Raise a typed `AMFError` subclass, never a bare `ValueError`, across the
   public API — `InvalidConfigError` for an out-of-range tuning parameter — and
   wrap anything the standard library raises at a parse boundary.
5. Keep output deterministic: iterate in canonical order, and do not introduce
   randomness that is not gated behind an explicit seed.
6. Add unit tests in the matching `tests/unit/test_<module>.py`, plus an
   integration test if the CLI, the console script, or an end-to-end path changed.
7. Run ruff, mypy, and pytest locally before pushing.
8. Record user-visible changes under `## [Unreleased]` in `CHANGELOG.md`
   (Added / Changed / Fixed / Security).

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
