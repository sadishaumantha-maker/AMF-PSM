# Changelog

All notable changes to the Anatomical Market Framework (AMF) are documented in
this file. Versions correspond to framework releases.

## [Unreleased]

### Added
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
- Tooling and quality gates: `pyproject.toml` (ruff, mypy strict, pytest,
  coverage), `.pre-commit-config.yaml` (including a guard that blocks edits to
  checksum-protected artifacts), and a `CI` GitHub Actions workflow running lint,
  type-check, tests, and YAML/citation/Markdown-link validation.
- `CLAUDE.md` contributor and design guide.

### Changed
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
- `Market.to_dict` now preserves each dependency's `kind`. Every exported edge
  was previously written as `structural`, silently downgrading informational,
  capital, and regulatory couplings — five of the eight edges in
  `examples/sample_market.json`. A dependency in `DependencyGraph` is now
  identified by `(source, target, kind)`, and the new `DependencyGraph.dependencies()`
  returns them in canonical order, so an exported market no longer depends on the
  order its dependencies were added in.
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
