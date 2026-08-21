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
- **Private distribution only.** `amf` is proprietary and all-rights-reserved, so
  it must never be published to PyPI or any other public index — doing so would
  invite the use its licence forbids. `pyproject.toml` carries the
  `Private :: Do Not Upload` classifier (PyPI rejects such uploads) and
  `tests/unit/test_packaging.py` fails if it is removed from the config or the
  built wheel. Do not add a publish workflow. Note the repository is public, so a
  GitHub Release asset or Actions artifact is *not* a private channel. See
  `RELEASING.md`.
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
tests/unit/         one file per module for the nine modules with direct unit
                    tests (errors.py is covered via test_packaging.py, and the
                    CLI is covered by tests/integration/test_cli.py), plus
                    test_non_trading_boundary.py (the naming guard),
                    test_properties.py (hypothesis), and test_packaging.py
                    (packaging / metadata invariants)
tests/tools/        the docsync + chronos harness, including the mutation corpus
tests/integration/  test_cli.py (main() in-process), test_console_script.py
                    (the installed `amf` entry point, as a subprocess),
                    test_end_to_end.py, test_examples.py (runs examples/)
examples/           sample_market.json + four runnable scripts
tools/              repository operations tooling, none of it shipped in the wheel
                    and none of it measured by the coverage gate: docsync
                    (CLAUDE.md drift detection), chronos (verified-time
                    attestation), and sync_milestones.py, which reconciles the
                    repository's Milestones section with .github/milestones.json
                    (stdlib only, idempotent, never deletes) and is validated
                    offline by test_milestones_manifest.py
.claude/            agents, hooks and slash commands for the maintenance run
projects/           73 charters decomposing the open work, plus AGENT_PROTOCOL.md
                    and COMMIT_PROTOCOL.md — prose only, no authority over the package
docs/               prose only — planning and research notes, no code and no
                    authority over the package (see *Prose docs* below)
.github/milestones.json   the 20-working-day delivery schedule as code
pyproject.toml      packaging + ruff / mypy / pytest / coverage config
.github/workflows/  ci.yml (lint/typecheck/test/validate), integrity.yml,
                    codeql.yml, milestones.yml, claude-md-drift.yml,
                    claude-md-sync.yml
.github/mlc-config.json   markdown-link-check config used by the validate job
.github/pull_request_template.md   PR checklist rendered on every new PR
.github/RULESET-POLICY.md          branch-protection rules and rationale
.pre-commit-config.yaml   ruff, ruff-format, mypy (src only), yamllint,
                          hygiene hooks, protect-ip-artifacts
.yamllint.yml       yamllint config (line length 140, `on:` truthy allowed)
.gitattributes      binary / EOL rules that keep the IP checksums stable
SHA256SUMS          the four protected artifacts and their digests
RELEASING.md        private-only release procedure and what enforces it
CONTRIBUTING.md     workflow guide — its tooling section is stale, see below
README.md, CHANGELOG.md, CITATION.cff, SECURITY.md   project metadata
```

## Package architecture (`src/amf/`)

| Module | Responsibility |
|--------|----------------|
| `errors.py` | Typed exception hierarchy. Every public-API failure derives from `AMFError` (`InvalidSystemError`, `InvalidDependencyError`, `IncompleteMarketError`, `InvalidShockError`, `InvalidConfigError`, `InvariantError`, `MarketParseError`). Has no internal dependencies. |
| `numeric.py` | Deterministic floating-point primitives: `stable_sum` (`math.fsum`; exactly rounded, so a reduction cannot depend on the order its terms arrive in), `square` (a multiplication -- IEEE 754 requires that to be correctly rounded, whereas `x ** 2` routes to the platform's `libm` `pow` and does not have to be), and `clip_unit`. Every scoring path reduces through these. No internal dependencies. |
| `invariants.py` | The guard each engine runs over its own result before returning it: `require_unit` / `require_non_negative` / `require_finite`, plus `check_diagnostic_report`, `check_simulation_trace`, `check_resilience_score`, `check_sensitivity_report`, `check_centrality`. Each `check_*` returns its argument unchanged, so an engine adopts it by wrapping its return value. Always on -- there is no flag to forget. Raises `InvariantError`, never `assert` (assertions vanish under `python -O`). Depends only on `errors`/`models`. |
| `models.py` | Value types: `SystemKind` (the 7 systems), `DependencyKind`, `SystemMetric`, `Dependency`, `MarketBoundary`, `Severity`, and the frozen result types (`WeaknessFinding`, `DiagnosticReport`, `Shock`, `Intervention`, `SimulationTrace`, `ResilienceScore`, `MetricStats`, `ResilienceDistribution`, `Sensitivity`, `LeveragePoint`, `SensitivityReport`). All are `@dataclass(frozen=True, slots=True)` with a `to_dict()`. |
| `systems.py` | `AnatomicalSystem` (frozen; validated in `__post_init__`), the seven factory functions (`skeleton`, `circulatory`, `nervous`, `musculature`, `organs`, `immune`, `metabolism`), and the `SYSTEM_FACTORIES` registry that keys them by kind. Structural metrics (`integrity`, `redundancy`, `criticality`, `load`) live in `[0, 1]`; derived `health()` and `absorptive_capacity()`; `metric()`/`with_metric()` read and replace one metric. An unrecognised metric keyword raises `InvalidSystemError` rather than being silently dropped. |
| `graph.py` | `DependencyGraph`: edges keyed by `(source, target, kind)`, with `dependencies()`, `edge_weight`, `edge_kinds`, `dependencies_of`, `dependents_of`, feedback-loop (simple-cycle) enumeration, articulation points, Katz-style `centrality`, and the stress-transmission `CouplingMatrix`. Depends only on `errors` and `models` — nothing above it in the layering. |
| `market.py` | `Market` aggregate root; `assemble`, `require_complete`, `system`, `with_system`, and the JSON `from_dict`/`to_dict` schema. `assemble` stores the seven systems in `SystemKind` declaration order and `require_complete` rejects a system filed under a key that is not its own `kind`. The one mutable dataclass in the package (`slots=True`, not frozen) — it is a container, and its parts are immutable. |
| `diagnostics.py` | `DiagnosticEngine` (+ tunable, validated `DiagnosticConfig`): deterministic structural-weakness scoring (`fragility`, `concentration`, `feedback_amplification`, `single_points_of_failure`) → `DiagnosticReport`. Both the findings ranking and the SPOF ranking break ties by `SystemKind` declaration order. |
| `sensitivity.py` | `SensitivityAnalyzer` (+ tunable, validated `SensitivityConfig`): perturbs each `SystemMetric` of each system and re-diagnoses → `SensitivityReport` (gradients + ranked `LeveragePoint`s). Builds on `diagnostics`. |
| `simulation.py` | `ShockSimulator` (+ tunable, validated `SimulationConfig`): damped, capacity-gated shock-propagation dynamics; `propagate()` → `SimulationTrace`, `resilience()` → `ResilienceScore`, `stress_test()` shocks every system in turn, `ensemble()` runs a seeded Monte Carlo → `ResilienceDistribution`. Opt-in extensions: cascade/threshold dynamics, recovery, multi-wave shocks (`Shock.at_step`), and `Intervention`s. |
| `report.py` | Pure textual renderers: `render_text`, `render_json`, `render_markdown`, `render_stress_test`, `render_distribution`, plus the `Renderable` type alias naming the result types the text/Markdown/JSON renderers accept, including `SensitivityReport` (`ResilienceDistribution` is deliberately excluded — only `render_json` serialises one). No I/O. |
| `viz.py` | Pure visual renderers: `render_dot`, `render_mermaid`, `render_graph_svg` (dependency graph, severity-coloured when given a `DiagnosticReport`), `render_timeline_svg` (stress timeline). SVG is drawn with the standard library alone — no Graphviz, no matplotlib. |
| `cli.py` | `argparse` CLI exposed as the `amf` console script. |

The public API is re-exported from `amf/__init__.py` (`__all__`); import types and
engines from `amf`, not submodules. The renderers are the exception — they live
in `amf.report` and `amf.viz` and are imported from there (as `cli.py` and
`examples/` do). `amf.numeric` and `amf.invariants` follow the same rule as the renderers: import
them from their own modules. Dependencies flow one way:
`errors`/`models`/`numeric` ← `invariants` ← `systems`/`graph` ← `market` ←
`diagnostics`/`simulation` ← `sensitivity` ← `report`/`viz`/`cli`. Keep it acyclic.

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
  `SensitivityConfig` requires a `step` in `(0, 1]`; `DependencyGraph.centrality`
  requires `alpha` in `(0, 1)`, `iterations >= 1`, and a finite non-negative
  `tolerance`. All raise `InvalidConfigError`. These
  are not cosmetic either: a negative blend weight used to yield findings scoring
  `2.0`, and `alpha >= 10` overflowed the influence series to infinity and
  returned `NaN` for every system. Keeping every score inside `[0, 1]` is what
  lets `Severity.from_score` and `WeaknessFinding` rely on that interval.
- **Jitter needs a seed.** `SimulationConfig.jitter` has no effect unless `seed`
  is also set, so the default configuration is fully deterministic; the tests
  rely on it.
- **Renderers are pure.** Nothing in `report.py` or `viz.py` performs I/O, reads
  the clock, or uses randomness; `viz` tests assert byte-identical repeat renders.
- **Reductions go through `stable_sum`, squaring through `square`.** Canonical
  traversal order alone is a workaround, not a guarantee: it removes the
  *observable* variation only where the engine controls the order. Two operations
  broke that in practice. `DependencyGraph.centrality` accumulated influence while
  iterating a dict keyed in *insertion* order, so 265 of 400 random permutations of
  `examples/sample_market.json`'s eight dependencies produced a different
  centrality vector; and `diagnostics.concentration` squared with `** 2`, which
  dispatches to the platform's `libm` `pow` and disagrees with `x * x` for about 1
  double in 1,200. Both are fixed, and the rule now is: reduce with
  `amf.numeric.stable_sum` (exactly rounded, so order cannot matter), square with
  `amf.numeric.square` (correctly rounded on every conforming platform), and clamp
  with `amf.numeric.clip_unit`. Do not write a bare `sum(...)` or `** 2` on a path
  that feeds a published score.
- **Every engine checks its own result.** `DiagnosticEngine.diagnose`,
  `ShockSimulator.propagate`, `SensitivityAnalyzer.analyse`, and
  `DependencyGraph.centrality` each wrap their return value in the matching
  `amf.invariants.check_*`, which raises `InvariantError` if a score has escaped
  `[0, 1]`, gone non-finite, or lost its normalisation. Note 100% coverage does not
  substitute for this: the settling-penalty defect — `_score` dividing by
  `max_steps` while `propagate` had extended the horizon past it, so a multi-wave
  run scored its settling term at `-1.8` against a documented `[0, 1]` — executed
  every line involved and was invisible to the gate. A new engine method that
  returns a result type adds the corresponding check.

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
`KeyError`/`TypeError`/`AttributeError`/`ValueError` and re-raises domain `AMFError`s as parse
errors, and the CLI's `_load_market` additionally maps `OSError`,
`UnicodeDecodeError` (a `ValueError`, so it does not fall under `OSError`), and
`json.JSONDecodeError` onto it — so no raw exception escapes the schema
boundary.

## Using the CLI

The `amf` console script prints the `_DISCLAIMER` to stderr (so `--format json`
stdout stays machine-parseable) after every analytical command, and offers eight
subcommands:

```sh
amf diagnose    examples/sample_market.json [--format text|json|md]
amf simulate    examples/sample_market.json --target circulatory [--magnitude 0.8] \
                [--cascade-threshold 0.2] [--cascade-gain 0.5] [--recovery 0.0] \
                [--seed N] [--jitter 0.0] [--format ...]
amf stress-test examples/sample_market.json [--magnitude 0.8] [--format ...]  # shocks each system in turn
amf ensemble    examples/sample_market.json --target circulatory [--magnitude 0.8] \
                [--runs 100] [--seed 0] [--jitter 0.05] [--format text|json]
amf sensitivity examples/sample_market.json [--step 0.05] [--top N] [--format ...]
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
`SystemKind` value; `--magnitude` and `--step` are in `(0, 1]`. `viz` has its own
`--format` (image formats, not text/json/md) and writes to stdout unless `-o` is
given. `--top` truncates both rankings in the sensitivity report.

`main(argv)` returns an exit code rather than calling `sys.exit`, so it is unit
tested in-process: `0` on success, `2` on a handled `AMFError`, `1` on bad usage
(no subcommand); argparse itself exits `2` on an unknown flag or choice.

Runnable scripts live in `examples/`: `equity_market.py` builds a market in code
and diagnoses it; `liquidity_shock.py` imports that builder and runs a shock plus
a stress test; `cascade_scenario.py` contrasts linear and cascade dynamics and
demonstrates multi-wave shocks, interventions, and the ensemble;
`where_to_intervene.py` ranks metric sensitivities and leverage points. The
sibling imports only resolve when a script is run directly (its own directory
lands on `sys.path`), which is why `tests/integration/test_examples.py` runs them
as subprocesses. That test currently covers `equity_market.py` and
`liquidity_shock.py` — add a case there if you add or substantially change an
example.

## The maths, briefly

- **Per-system derived metrics**: `health = integrity·(1 − load)`;
  `absorptive_capacity = 0.5·redundancy + 0.3·integrity + 0.2·(1 − load)` (weights
  sum to 1, so the result stays in `[0, 1]`).
- **Config validation**: `DiagnosticConfig` rejects negative and non-finite
  weights, `SimulationConfig` rejects `max_steps < 1`, `damping` outside `(0, 1]`,
  and negative `retention`/`transmission`/`jitter`, `SensitivityConfig` rejects a
  `step` outside `(0, 1]`, and `DependencyGraph.centrality` rejects `alpha`
  outside `(0, 1)` — all as `InvalidConfigError`. This is what keeps every score
  inside `[0, 1]`, the interval `Severity.from_score` and `WeaknessFinding` both
  rely on. See
  *Determinism and parameter validation* for the full set of checks and why each
  one exists. Note it does **not** make the dynamics a contraction — nothing does;
  see the Simulation bullet below.
- **Diagnostics** (deterministic): per-system
  `fragility = criticality·(1 − health)·(1 − redundancy)`; `concentration` is an
  HHI over a system's outgoing dependency weights (share-based, so it measures how
  *unevenly* reliance is spread and not how much of it there is — a system with a
  single coupling scores 1.0 at any weight, while one with none scores 0;
  `DiagnosticConfig.scale_concentration_by_reliance` opts into multiplying by
  `min(1, total outgoing weight)`, which is off by default because it moves every
  published concentration score); `feedback` sums the edge-weight
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
  centrality because it is well defined on acyclic graphs. Below
  `alpha = 1/spectral radius` this is the Katz sum proper; above it the series
  grows without bound but the *max-normalised* result still settles, on the
  dominant-eigenvector direction. Both rank "how much is depended upon", so
  divergence alone is not treated as an error — a densely coupled market returns a
  perfectly usable answer. What is rejected (`InvalidDependencyError`) is a graph
  with no single dominant mode, where the normalised ranking cycles forever and the
  answer would be decided by whichever step the iteration budget stopped on; a
  complete bipartite market with unequal sides does this. Exhausting `iterations`
  on a still-settling run returns the partial result, since a truncated run is what
  the caller asked for. Nothing in the scoring pipeline consumes `centrality`; it
  is a standalone query.
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
- **Sensitivity**: for each system and each `SystemMetric`, the overall index is
  re-evaluated at `baseline ± step` (clipped to `[0, 1]`), giving
  `gradient = index_delta / span`. The difference is central where the metric has
  room on both sides and one-sided near a bound, so `span` — the interval actually
  explored — is reported alongside the gradient. `SensitivityConfig` defaults:
  `step=0.05, include_criticality=True`.
- **Leverage points**: the same perturbation restricted to
  `SystemMetric.improving_direction()` (+1 for integrity/redundancy, −1 for load,
  0 for criticality), ranked by `index_before − index_after`. A metric with no
  headroom in its improving direction yields no leverage point. Criticality is
  never a leverage point — it describes how load-bearing a system *is*, not a
  lever — but it is still reported as a sensitivity.
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

This block is the authoritative dev setup — there is no `requirements.txt`, and
the project does not use `black`, `flake8`, or `pylint` despite what
`CONTRIBUTING.md` says (see *Prose docs* at the end of this file). A clean run of
the whole suite is currently 827 tests passing with `ruff` and `mypy` both
silent; that is the bar a change has to clear. Coverage is 100% statement and
branch *of `src/amf`* — the gate is scoped to the package (`--cov=amf`), so the
`tools/` tests contribute to the test total but not to that percentage.

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
2. Export new public types from `amf/__init__.py` and add them to `__all__`, whose
   order is enforced by ruff's `RUF022` — an isort-style natural sort, *not*
   `sorted()`. `tests/unit/test_packaging.py` deliberately declines to assert the
   ordering rather than duplicate the linter and encode the wrong convention, so do
   not add a `== sorted(__all__)` assertion. Check the name against the non-trading
   `FORBIDDEN` list.
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

Seven workflows are checked in. Four gate every push and pull request:

- `.github/workflows/ci.yml` — the main gate. Four jobs: **lint** (`ruff check` +
  `ruff format --check`), **typecheck** (`mypy`), **test** (`pytest` on the
  3.11/3.12/3.13 matrix, uploading `coverage.xml` from 3.12), and **validate**
  (`yamllint .`, `cffconvert --validate -i CITATION.cff`, and a Markdown link
  check). `cffconvert` is installed standalone in that job rather than in the
  `dev` extra, because a transitive dependency fails to build under some patched
  local setuptools.
- `.github/workflows/milestones.yml` — reconciles the repository's Milestones
  section against `.github/milestones.json` via `tools/sync_milestones.py`, so the
  delivery schedule is reproducible rather than hand-maintained.
- `.github/workflows/integrity.yml` — verifies the `SHA256SUMS` artifacts are
  untouched.
- `.github/workflows/codeql.yml` — GitHub's CodeQL Advanced scan of the `python`
  and `actions` languages, on pushes and PRs to `main` plus a weekly schedule.
  `build-mode: none`, so it needs no project setup.

Three more run on their own triggers rather than gating pushes:
`claude-md-drift.yml` and `claude-md-sync.yml`, the two halves of CLAUDE.md
maintenance, described under *Verified time* below, and `manual.yml`, a
`workflow_dispatch`-only greeting placeholder the owner re-added after the
starter cleanup (kept, but re-indented to `.yamllint.yml` — yamllint runs first
in the validate job, and a YAML error there silently disables the metadata
validation behind it). This inventory is machine-checked: the drift scanner fails if a workflow file exists that this
guide does not mention, and fails harder if a conda, publish, or release
workflow appears at all.

### The validate job runs in order, and yamllint is first

`yamllint .` runs ahead of `cffconvert` and the link check, so **a YAML formatting
error silently disables both of them**. That is not hypothetical: it happened.
Two workflows were committed as unmodified GitHub templates, `yamllint` rejected
them, and for as long as that lasted the metadata validation and link checking the
job exists to perform never executed on any branch — while the job still *looked*
like it was doing its work. When `validate` fails, read far enough down the log to
see which step actually failed; and if you make `yamllint` pass, expect the steps
behind it to start reporting problems of their own that were never visible before.

Two consequences are baked into the tree, and undoing either re-breaks the job:

- **`codeql.yml` carries three `# yamllint disable-line rule:line-length`
  directives.** They sit above comments that are a single GitHub documentation
  URL, too long for the 140-character limit at any indentation and not shortenable
  without breaking the link. Keep the directives if you touch that file, and keep
  the rest of it formatted to `.yamllint.yml` (bracket spacing, sequence
  indentation) — it is a vendored template, so a careless re-copy from GitHub will
  reintroduce every violation at once.
- **There is deliberately no conda workflow.** `python-package-conda.yml` was
  removed: it was the stock conda starter, running on every push against an
  `environment.yml` that does not exist, and it contradicted the project on three
  counts — Python 3.10 (below the `requires-python = ">=3.11"` floor), `flake8`
  (the project lints with `ruff`), and a bare `pytest` with no install step, so
  `amf` was not importable. Do not re-add it, and do not add an `environment.yml`
  or a flake8 config to revive it; `ci.yml` already tests 3.11/3.12/3.13 and
  CodeQL already scans. This has now happened **twice**: the identical starter was
  re-added in August 2026 alongside thirteen other stock templates (C/C++, Clojure,
  Maven, Gradle, Terraform, Hugo, three cloud-deploy starters, and an OSSF SLSA
  release-publish workflow carrying `upload-assets: true` with `contents: write` —
  a direct breach of the private-distribution rule on a public repository) and every
  one of them failed on every push, since the repository contains no C/C++, Java,
  Clojure, Terraform, or Node source at all. All fourteen starters were removed —
  the eleven that could never pass and, in a parallel cleanup, the stock
  `stale.yml`, `summary.yml`, and `manual.yml` as well (`manual.yml` has since
  been re-added deliberately, and stays); the drift scanner's
  `ci.forbidden-workflow` check now rejects any workflow whose filename contains
  `conda`, `publish`, or `release` outright.

### Links in Markdown are checked, including relative ones

The link check covers every `.md` file in the tree, relative paths included, so a
link to a file that does not exist fails the build. Mind the directory a document
lives in: from `.github/RULESET-POLICY.md`, `./CONTRIBUTING.md` resolves to
`.github/CONTRIBUTING.md` and fails — root-level documents need `../`. Check a
change the way CI does before pushing:

```sh
npx markdown-link-check --config .github/mlc-config.json <file>.md
```

`.github/mlc-config.json` holds the ignore patterns and the accepted status codes.
Five patterns are ignored: shields.io badges, opentimestamps.org, a repository's
`/milestones` page, Actions badge SVGs, and the author's bare profile URL — each
a URL GitHub answers `403` to an unauthenticated non-browser client (verified by
`curl`), and each decorative rather than documentation, so ignoring it costs no
coverage. `aliveStatusCodes` is deliberately *not* widened to accept `403`: that
would silence real failures on every host.

One diagnosis trap is worth recording, because it cost a wrong conclusion once.
The `push` and `pull_request` runs of `validate` check out **different trees for
the same head SHA**: push checks out the branch as it stands, while pull_request
checks out the merge of the branch with the base. A branch carrying a dead link
that `main` has since fixed therefore fails its push run and passes its PR run on
the *identical commit* — which looks exactly like a flaky checker and is nothing
of the kind. Before calling this job flaky, compare the two runs' events; the fix
for that case is merging the base branch in, not touching the checker.

Project metadata lives in `CITATION.cff`, `CHANGELOG.md`, and `SECURITY.md`.

## Time and locale (hard-gated)

This repository is operated from **Ratnapura, Sri Lanka** — `Asia/Colombo`, **UTC+05:30**,
no daylight saving. Those constants are frozen in `tools/chronos/locale_gate.py` and
validated against the system time zone database on import. The gate *raises* rather than
warns: a record stamped with the wrong offset is worse than one that was never written,
because it looks usable. It also checks Sri Lanka's historical transitions (+05:30 →
+06:30 in 1996 → +06:00 → +05:30 on 2006-04-15) as a fingerprint, which catches a stub
tzdata that would otherwise report a plausible-looking constant offset.

**Do not edit those constants to make a machine pass.** If the gate fails, the machine's tz
database is wrong, not the gate.

### What accuracy is actually achievable

This matters because the honest ceiling is set by physics, not by effort:

| Source | Realistic uncertainty |
|--------|-----------------------|
| NTP over the public internet | ~1–10 ms, bounded by path asymmetry |
| NTP on a quiet LAN | ~0.1–1 ms |
| A disciplined local clock (`chronyc tracking`) | tens of microseconds |
| PTP with hardware timestamping | sub-microsecond |
| GNSS with a PPS signal | tens of nanoseconds |

Microsecond accuracy from an internet round trip is **not attainable at any sampling
rate**: the one-way delays are unmeasurable and unequal, and that asymmetry lands directly
in the offset. Anything printing microseconds from an HTTP fetch is printing noise, so
`tools/chronos` never formats more digits than its measured bound supports.

### The attestation contract

`tools/chronos` does not try to be accurate. It measures how accurate it is, and refuses to
certify a run whose uncertainty it cannot prove.

- Each source returns an offset **and an explicit error bound**. A source that cannot bound
  its own error raises `SourceUnavailableError` rather than guessing.
- `consensus.py` uses **Marzullo interval intersection**, not averaging. A mean is dragged
  by one misconfigured server and says nothing about how wrong it might be; an intersection
  yields an interval every surviving source vouches for, so its half-width is a bound you
  can compare against a budget. Sources outside it are *falsetickers* and are discarded.
  Three agreeing sources is the floor — the smallest number that lets one liar be outvoted
  rather than merely noticed.
- An attestation is **always written**, even when nothing could be measured; silence is
  indistinguishable from success after the fact. Only `VERIFIED` authorises downstream work.
- Exit codes: `0` VERIFIED, `3` UNVERIFIED, `4` FAILED (usually the locale gate), `2` usage.
  `3` and `4` are deliberately not `1`, so a caller can tell an untrustworthy clock from a
  broken tool.

```sh
python -m tools.chronos attest [--budget-ms 50] [--min-sources 3] [--format text|json] [--out FILE]
python -m tools.chronos check     # exit code only
python -m tools.chronos now       # one line: attested local time and bound
```

`PpsSource` and `PtpSource` define the hardware interface so that adding a GNSS receiver or
a PTP grandmaster later is configuration rather than redesign. Until hardware exists they
report themselves unavailable, which is a truthful answer rather than a silent fallback to
something worse.

**A Claude Code sandbox has no reachable time source** — UDP/123 is blocked, egress is
filtered to an allowlist, and the proxy strips the `Date` response header. Such a session
correctly attests `UNVERIFIED`; it is a writer, not a timekeeper, and consumes the
attestation the scheduled GitHub Actions run produces.

## Automated CLAUDE.md maintenance

This file is checked mechanically against the repository it describes, because it has
drifted before: a stale test count, a miscounted directive, an undocumented flag, two
unmentioned docs files, and — in the other direction — `cli.py`'s own docstring omitting a
subcommand the guide listed correctly.

`tools/docsync` extracts the repository's real facts with `ast` (never importing or
executing `amf`), extracts this file's claims, and reports every disagreement:

```sh
python -m tools.docsync scan  [--format text|json|md] [--fail-on low|medium|high] [--baseline FILE]
python -m tools.docsync facts [--format json]   # the extracted ground truth
```

Three properties are deliberate and worth preserving:

- **Offline.** No check touches the network, so a scan reproduces anywhere and is fast
  enough for a pre-commit hook. That includes the dead-relative-link scan, which does not
  need Node or `npx`.
- **Deterministic.** Findings are emitted in canonical order as canonical JSON, so the same
  commit always yields byte-identical output — which is what lets a checked-in baseline act
  as a regression gate.
- **Bidirectional.** Most checks also ask "is everything real named here?", not only "is
  everything named here real?". Roughly half the drift found in this repository consisted of
  omissions, on which forward-only checking passes silently.

Two workflows drive it. `.github/workflows/claude-md-drift.yml` fires on push and pull
request, filtered to the paths whose facts this guide states. `.github/workflows/claude-md-sync.yml`
runs daily against the 06:00 Asia/Colombo target (00:30 UTC), attests the clock first and
hard-fails if it cannot, and records its own schedule slip — GitHub's cron is best-effort
and can be minutes to tens of minutes late, so the inaccuracy is measured rather than hidden.

`.claude/agents/` holds the agents that turn findings into prose: `chronos-warden` (gates
the run on verified time), `claude-md-auditor` (verifies each finding against the source),
`repo-cartographer` (regenerates the mechanical sections from extracted facts),
`ci-forensics`, `changelog-scribe`, `doc-guard-verifier` (adversarial — tries to *refute*
each changed sentence and vetoes what it cannot support), and `hard-rules-sentinel` (blocks
any diff that erodes a hard rule). `.claude/hooks/` is POSIX shell rather than Python on
purpose: `ruff check .` covers `.claude/**/*.py` with the full `ANN`+`D` rule set and CodeQL
scans it too.

**Never fix a finding by loosening a check.** If a check is genuinely wrong, that is a change
to `tools/docsync/checks.py` with a case added to the mutation corpus in
`tests/tools/test_docsync_corpus.py`, which asserts that a correct synthetic repository
produces *zero* findings and that each single-defect mutation is caught by exactly one check.

## Prose docs, governance, and what is authoritative

Several Markdown files describe intentions rather than the code as it stands.
They are useful background, but none of them overrides this file, `pyproject.toml`,
or the test suite. When a prose document and the code disagree, the code wins and
the document is the thing that is out of date.

- **`CONTRIBUTING.md`** — the workflow half (branch naming, Conventional Commits,
  PR and review etiquette) is worth following. Its **tooling half is wrong for this
  repository**: it names `pylint`, `black`, `flake8`, `requirements.txt`,
  `requirements-dev.txt`, a `develop` branch, and an 80% coverage floor. None of
  those exist here. The real setup is `pip install -e ".[dev]"`, `ruff` (lint *and*
  format), `mypy --strict`, `pytest` at a **100%** coverage gate, and a single
  long-lived branch, `main`. Follow the *Developing* section above, not that list,
  and do not add those tools or files to make the document true.
- **`.github/RULESET-POLICY.md`** and the branch-protection tables in
  `CONTRIBUTING.md` — the *intended* ruleset (2 approvals on `main`, signed
  commits, protected `develop` and `release/*` branches). They describe a policy
  target, not necessarily what GitHub currently enforces, and they reference
  branches this repository does not have. Do not infer the live configuration from
  them; check the repository settings if it matters.
- **`.github/pull_request_template.md`** — a long checklist (description, linked
  issues, testing, security, type of change, priority). Fill in the sections that
  apply to the diff and skip the rest; it is a layout to populate, not a set of
  instructions to obey.
- **`docs/roadmap.md`** — Phase 2 planning and issue triage. Explicitly marked a
  *proposal for ratification*, and it restates the hard rules above rather than
  relaxing them.
- **`docs/ROBUSTNESS_REVIEW.md`** — an assessment of an external "advanced robustness"
  proposal, recording which of its mechanisms survived review and which did not, with the
  measurements behind each verdict. It is the reasoning behind `numeric.py` and
  `invariants.py` existing in the form they do. A dated review, not a live specification.
- **`docs/ANALYSIS_AND_ROADMAP.md`** — a governance and delivery-pipeline audit
  with a 90-day plan. A snapshot of one moment's issue and PR backlog; its counts
  go stale immediately.
- **`docs/90_DAY_PLAN_INDEX.md`** — an index mapping that 90-day plan onto
  individual issues. Like the audit it annotates, its counts and issue numbers are
  a snapshot rather than live state.
- **`docs/discussions/`** — eleven self-contained theoretical modules derived from
  `docs/QUANTUM_NEURAL_RESEARCH.md`, one per discussion in that note, indexed by
  `docs/discussions/README.md`. Each module reproduces its source specification
  verbatim, then adds formal foundations with attributed theorem statements, the
  graduate curriculum around the topic, an annotated bibliography, a derivation for
  the AMF setting, a governance section reconciling the note's proposed deliverables
  with the hard rules, and falsifiable propositions. They carry the same standing as
  the rest of `docs/`: prose only, and nothing in them is implemented, agreed or
  scheduled. Three argue *against* their own source proposal, which is the point of
  reading them — `docs/discussions/H3-symplectic-hamiltonian-dynamics.md` shows the
  seven-dimensional stress space admits no symplectic form and that the step map
  contracts phase-space volume every step, so the note's Liouville alarm cannot
  discriminate; `docs/discussions/I1-unified-framework-architecture.md` corrects the
  note's inverse-RMSE weighting and its union-of-intervals rule; and
  `docs/discussions/I2-validation-backtesting-generalization.md` places several
  proposed artefacts outside the non-trading boundary. The remaining eight are
  `docs/discussions/Q1-quantum-market-superposition.md`,
  `docs/discussions/Q2-quantum-markov-lindblad.md`,
  `docs/discussions/Q3-shannon-information-market-entropy.md`,
  `docs/discussions/D1-deep-learning-architectures.md`,
  `docs/discussions/D2-embedding-spaces-regimes.md`,
  `docs/discussions/D3-knowledge-graphs-causal-pathways.md`,
  `docs/discussions/H1-quantum-neural-hybrid-circuits.md` and
  `docs/discussions/H2-topological-data-analysis.md`. The index links every module; if
  you add one, add the file and its link in the same pull request.
- **`docs/RESEARCH_DISCUSSIONS.md`** and **`docs/QUANTUM_NEURAL_RESEARCH.md`** —
  open-ended research prompts for a hypothetical v1.1 (regulatory architecture,
  quantum and neural formulations of market state, information-theoretic
  measures). These are speculative discussion material. **Nothing in them is
  implemented, agreed, or scheduled**, and several sketches would collide with the
  hard rules if taken literally — a request to "implement the roadmap" or "add the
  quantum model" needs the specific item confirmed with the user first, and still
  has to clear the non-trading naming guard, the determinism rules, and the 100%
  coverage gate like any other change.

The `docs/` tree is prose only. No code imports from it, no test reads it, and
adding a document there changes nothing about the package's behaviour.

## Agent operating system

Agents, skills, and durable memory for issue creation and deep research live under `.claude/`.
Read `.claude/README.md` for the map. The two files below are small and load with this document;
everything else is read on demand by the agent or skill that names it.

@.claude/memory/repo-facts.md
@.claude/memory/issue-index.md

**Before creating any GitHub issue**, check `.claude/memory/issue-index.md` — it records which source
unit already became which issue, and is what stops two sessions from decomposing the same document
twice (which has already happened once: #45–#92 and #77–#98 overlap).

**Before writing any issue, dossier, doc, or code**, load the `amf-guardrails` skill. It carries the
non-trading boundary, the illustrative-not-validated rule, determinism, and the IP protections, plus
the translation table for admitting real-market phrasing as structural measures.

Research dossiers live under `docs/research/_dossiers/` — one file per issue, written by the
issue-researcher agent, plus `docs/research/_dossiers/_strategy.md`, the strategist's whole-backlog
review. Currently: `docs/research/_dossiers/discussion-2.2.md` (issue #59). Like everything under
`docs/`, they are prose only, with no authority over the package — and the drift scanner requires
each new dossier to be named here, so add a file's path to this list in the same commit that adds
the file.

Nothing under `.claude/` is part of the `amf` package, so none of it affects the 100% coverage gate.
The repository is public: never put secrets or verbatim protected-framework text in these files.
