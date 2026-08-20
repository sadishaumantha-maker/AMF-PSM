# Changelog

All notable changes to the Anatomical Market Framework (AMF) are documented in
this file. Versions correspond to framework releases.

## [Unreleased]

### Added
- `InvalidConfigError`, a new `AMFError` subclass raised when an engine or
  algorithm parameter is outside its documented range — `DiagnosticConfig`,
  `SimulationConfig`, and `DependencyGraph.centrality()` all validate on
  construction rather than normalising an out-of-range knob into a plausible but
  meaningless result.
- Extended the shock-propagation simulation with four opt-in, backward-compatible
  capabilities (the default dynamics are unchanged): nonlinear **threshold /
  cascade** dynamics with a `tipped_systems` signal; a seeded **Monte Carlo
  ensemble** (`ShockSimulator.ensemble` → `ResilienceDistribution`);
  **time-scheduled / multi-wave shocks** (`Shock.at_step`); and **recovery /
  intervention** modeling (`SimulationConfig.recovery_rate`, `Intervention`). New
  CLI: `amf ensemble` plus `simulate --cascade-threshold/--recovery/--seed/...`.
- `amf sensitivity` subcommand and `amf.sensitivity` module: comparative-statics
  analysis that perturbs each structural metric of each system and reports (a)
  the finite-difference gradient of the overall weakness index and (b) ranked
  *leverage points* — the feasible adjustments that reduce the index most (AMF
  analytical Step 5). `criticality` is reported as sensitive but excluded from
  leverage rankings, since it describes how load-bearing a system is rather than
  a lever an operator tunes. Supporting API: `SystemMetric`,
  `AnatomicalSystem.metric`/`with_metric`, and `Market.with_system`.
- `amf viz` subcommand and `amf.viz` module: dependency-free renderers that draw
  the dependency graph as Graphviz DOT, Mermaid, or a self-contained SVG
  (severity-coloured when diagnostics are available) and a shock-propagation
  stress timeline as SVG. `DependencyGraph.edge_kinds` exposes the aggregated
  dependency kinds of an edge for these renderers.
- `amf` Python package (`src/amf/`) — a dependency-free, software implementation
  of the AMF analytical method: the seven anatomical systems, a dependency and
  feedback graph, a structural-weakness diagnostic engine, and a non-trading
  shock-propagation simulation engine, with a command-line interface.
- Runnable examples (`examples/`) and a test suite (`tests/`) with a 90% coverage
  gate.
- Property-based tests (`tests/unit/test_properties.py`, using a new `hypothesis`
  dev dependency) covering the invariants the docstrings promise: stress stays in
  `[0, 1]` at every step, diagnostic scores stay in `[0, 1]` for any blend of
  config weights, `to_dict`/`from_dict` is a fixed point, and feedback-loop
  enumeration matches a brute-force search of every simple cycle.
- Tests closing gaps found by a one-off mutation-testing pass over `report.py`,
  `simulation.py`, and `diagnostics.py`: resilience severity is now asserted at
  the high-resilience end as well as the critical end, `absorbed_fraction` is
  pinned on a genuinely partial absorption rather than only at exactly 0.0 or
  1.0, and the seeded transmission jitter is pinned to an exact perturbation
  rather than only "differs" and "repeats".
- Tooling and quality gates: `pyproject.toml` (ruff, mypy strict, pytest,
  coverage), `.pre-commit-config.yaml` (including a guard that blocks edits to
  checksum-protected artifacts), and a `CI` GitHub Actions workflow running lint,
  type-check, tests, and YAML/citation/Markdown-link validation.
- `CLAUDE.md` contributor and design guide.

### Fixed
- `Market.from_dict()` now rejects a `components` value that is not a list. A
  bare string is iterable, so it was previously split into single-character
  components rather than reported as malformed.
- Diagnostic output no longer depends on the order a market was assembled in.
  Both the per-system findings ranking and the single-point-of-failure ranking
  fell back on `dict` insertion order whenever two systems tied, so two markets
  that compare equal produced differently ordered reports — `musculature` and
  `metabolism` share a criticality of 0.60 and tie routinely. Ties now break by
  `SystemKind` declaration order, `Market.assemble` stores the seven systems in
  that order, and `Market.to_dict()` emits them in it.
- `DependencyGraph.centrality()` no longer returns `NaN` for every system. The
  `alpha`, `iterations`, and `tolerance` arguments were unvalidated; an `alpha`
  of 10 or more overflowed the influence series to infinity, and max-normalising
  by an infinite peak produced `NaN` throughout. They are now checked against the
  ranges the docstring already documented.
- `DiagnosticConfig` now rejects negative and non-finite blend weights. A
  negative weight was normalised like any other and pushed scores outside the
  `[0, 1]` interval that `WeaknessFinding` documents and `Severity.from_score`
  assumes — a fragility weight of `-2` produced findings scoring `2.0`, banded
  `critical`. An all-zero triple remains supported and still yields zero scores.
- `SimulationConfig` now validates every dynamics parameter. `max_steps=0`
  reported a market as never settling without simulating a step, `damping=5.0`
  amplified every step globally, and a negative `transmission` inverted the
  direction of stress flow — each silently produced a plausible-looking but
  meaningless trajectory.
- `Market.require_complete()` now rejects a system filed under a key that is not
  its own `kind`. `systems` is a plain mutable dict and every engine reads a
  finding's label from the key and its metrics from the value, so a mismatch
  silently attributed one system's weaknesses to another.
- The CLI no longer aborts with an unhandled `UnicodeDecodeError` traceback when
  pointed at a binary or non-UTF-8 file. `UnicodeDecodeError` is a `ValueError`,
  not an `OSError`, so it escaped the `AMFError` contract in `main`; it is now
  reported as a `MarketParseError` with exit code 2 like every other bad input.
- `Market.to_dict()` now preserves each dependency's `kind` instead of
  serialising every coupling as `structural`, so a market survives a
  `to_dict`/`from_dict` round trip intact — five of the eight edges in
  `examples/sample_market.json` were being downgraded. A dependency in
  `DependencyGraph` is now identified by `(source, target, kind)`, so a pair
  coupled by several kinds keeps every one of them; `edge_kinds()` remains
  available and reports them in declaration order.
- The CLI now raises the typed `MarketParseError` (instead of a bare `AMFError`)
  when a market JSON file is unreadable or contains invalid JSON, matching the
  convention that every public-API failure uses a specific `AMFError` subclass.
  Exit codes and error messages are unchanged.

### Changed
- The coverage gate rose from 90% to 100% branch coverage. A suite already at
  100% cannot fail a 90% gate, so the gate was rejecting nothing.
- `amf.report` now exports a `Renderable` type alias for the result types the
  renderers accept, and `cli._format` is annotated with it instead of `object`.
  This removes three `# type: ignore[arg-type]` comments that were suppressing
  every argument check on the CLI's formatting path — mypy now rejects a wrong
  result type there. Runtime behaviour is unchanged.
- The `stress-test` CLI subcommand now accepts `--format {text,json,md}`, matching
  `diagnose` and `simulate`. JSON output for the stress-test profile was already
  supported by `render_json`; this adds a Markdown table renderer and routes the
  command through the shared formatter.
- `Market.from_dict` now reports a non-numeric metric or dependency weight as a
  `MarketParseError` instead of letting a raw `ValueError` escape. The CLI
  consequently exits with code 2 and an `error:` message where it previously
  aborted with an unhandled traceback.
- The system factories (`skeleton`, `circulatory`, ...) now raise
  `InvalidSystemError` for an unrecognised metric keyword. Previously a
  misspelling such as `skeleton(integritty=0.1)` was silently discarded and the
  default used instead.
- `AnatomicalSystem` is now immutable (`frozen=True`). Its metrics are validated
  on construction, so freezing keeps the documented `[0, 1]` ranges true for the
  object's lifetime; assignment now raises `FrozenInstanceError`.
- A market JSON that omits a system's `criticality` or `name` now inherits the
  AMF-aligned per-system default (criticality 0.60–0.90, e.g. `skeleton` 0.90)
  instead of a flat 0.5 and the bare kind string. Parsing is routed through the
  new `SYSTEM_FACTORIES` registry, so a market built from JSON and the equivalent
  market built from the factories now diagnose identically. Markets that state
  every metric — including `examples/sample_market.json` — are unaffected.
- `Market.from_dict` now rejects an unrecognised field inside a system entry
  rather than ignoring it, matching the factories' handling of unknown metrics.
- `DependencyGraph.dependencies()` returns the graph's dependencies in canonical
  `(source, target, kind)` order, and `Market.to_dict` uses it, so an exported
  market no longer depends on the order its dependencies were added in.
- `DependencyGraph.dependencies_of` and `dependents_of` now return their results
  in system declaration order. The diagnostic HHI sums over that list and
  floating-point addition is not associative, so the previous insertion-ordered
  traversal made a market's diagnosis differ in the last bits depending on the
  order its dependencies happened to be added — 48 such mismatches across 3000
  random markets, now zero. `examples/sample_market.json` is unaffected: its
  dependencies were already in canonical order.
- Corrected the claim that the shock dynamics are a contraction "guaranteed to
  converge", in the `simulation` docstrings and `CLAUDE.md`. With enough incoming
  weight and little absorptive capacity the per-step gain exceeds one
  (0.85 · (0.5 + 1.0 · 0.8) = 1.105) and stress grows until it saturates at the
  `1.0` clip; and `converged` reports settling *within `max_steps`*, so a stable
  but slowly-settling market can exhaust the budget and take the full settling
  penalty. Behaviour is unchanged — only the documentation and the tests pinning it.

### Security
- Bumped the dev-dependency pin `pytest` from 8.2.2 to 9.0.3 to resolve
  CVE-2025-71176 / GHSA-6w46-j5rx-g56g (predictable `/tmp/pytest-of-{user}`
  temporary-directory handling on UNIX; moderate severity). Dev-only tooling —
  the `amf` package itself has no runtime dependencies.

### Notes
- The software models market *structure and resilience* only; it is not a
  trading system. The checksum-protected framework artifacts are unchanged.
- Making dependency `kind` part of edge identity is numerically neutral: every
  pair-level query aggregates across kinds exactly as the previous single-bucket
  aggregation did, so no existing market's diagnostic or simulation scores
  change. Only the JSON `dependencies` list differs — correct `kind`, canonical
  order. The diagnosis of `examples/sample_market.json` is byte-identical.

## [1.0] — 2026-03-17

### Added
- Initial release of the **Anatomical Market Framework (AMF)**.
- `AMF Framework v1.docx` — the complete framework document.
- `AMF Framework v1.docx.ots` — OpenTimestamps proof anchoring the document to
  the Bitcoin blockchain as independent evidence of its creation date.
- `anatomical-market-framework` — plain-text overview of the framework's core
  components and analytical method.
- `LICENSE.txt` — proprietary, all-rights-reserved copyright notice.
