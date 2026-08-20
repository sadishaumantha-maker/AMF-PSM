# Changelog

All notable changes to the Anatomical Market Framework (AMF) are documented in
this file. Versions correspond to framework releases.

## [Unreleased]

### Added
- `amf` Python package (`src/amf/`) — a dependency-free, software implementation
  of the AMF analytical method: the seven anatomical systems, a dependency and
  feedback graph, a structural-weakness diagnostic engine, and a non-trading
  shock-propagation simulation engine, with a command-line interface.
- Runnable examples (`examples/`) and a test suite (`tests/`) with a 100% branch
  coverage gate.
- Tooling and quality gates: `pyproject.toml` (ruff, mypy strict, pytest,
  coverage), `.pre-commit-config.yaml` (including a guard that blocks edits to
  checksum-protected artifacts), and a `CI` GitHub Actions workflow running lint,
  type-check, tests, and YAML/citation/Markdown-link validation.
- `CLAUDE.md` contributor and design guide.

- `InvalidConfigError`, raised when an engine configuration holds values outside
  its valid domain. `DiagnosticConfig` now rejects negative weights, and
  `SimulationConfig` rejects a non-positive `max_steps`, a `damping` outside
  `(0, 1]`, and a negative `retention`, `transmission`, or `jitter`. Previously a
  negative weight silently produced scores far outside `[0, 1]` (a market-wide
  index of `-2.09` was still reported as `low` severity), and a damping above one
  turned the shock dynamics from a contraction into an amplifier.


### Fixed
- `Market.from_dict()` now raises `MarketParseError` for a wrong-*typed* value,
  naming the offending field. A non-numeric metric or dependency weight (for
  example `"integrity": "high"`) previously raised a bare `ValueError` that
  escaped `from_dict` altogether and crashed the CLI with a traceback instead of
  exiting with code 2. A `components` value that is not a list is likewise
  rejected rather than being iterated — a bare string used to split silently into
  single-character components.
- `Market.to_dict()` now preserves each dependency's `kind` instead of
  serialising every coupling as `structural`, so a market survives a
  `to_dict`/`from_dict` round trip intact. `DependencyGraph` gained a public
  `edge_kinds()` accessor exposing the kinds it already recorded per edge.
- The CLI now raises the typed `MarketParseError` (instead of a bare `AMFError`)
  when a market JSON file is unreadable or contains invalid JSON, matching the
  convention that every public-API failure uses a specific `AMFError` subclass.
  Exit codes and error messages are unchanged.

### Changed
- `Market.require_complete()` now re-validates every system in addition to
  checking that all seven are present. Systems are mutable, so a metric could be
  pushed outside `[0, 1]` after construction and flow unchecked into every score;
  because both engines call `require_complete()` before reading a market, that
  mutation is now caught at the engine boundary and raises `InvalidSystemError`.
- The seven system factories (`skeleton()`, `circulatory()`, …) now raise
  `InvalidSystemError` on an unrecognised metric keyword instead of discarding it.
  A typo such as `skeleton(integirty=0.1)` previously returned a system built
  entirely from defaults, and `mypy` cannot catch it because the factories accept
  `**metrics: float`.
- The coverage gate rose from 90% to 100% branch coverage. A suite already at
  100% cannot fail a 90% gate, so the gate rejected nothing; at 100% a newly
  uncovered line is visible again.
- The `stress-test` CLI subcommand now accepts `--format {text,json,md}`, matching
  `diagnose` and `simulate`. JSON output for the stress-test profile was already
  supported by `render_json`; this adds a Markdown table renderer and routes the
  command through the shared formatter.

### Security
- Bumped the dev-dependency pin `pytest` from 8.2.2 to 9.0.3 to resolve
  CVE-2025-71176 / GHSA-6w46-j5rx-g56g (predictable `/tmp/pytest-of-{user}`
  temporary-directory handling on UNIX; moderate severity). Dev-only tooling —
  the `amf` package itself has no runtime dependencies.

### Notes
- The software models market *structure and resilience* only; it is not a
  trading system. The checksum-protected framework artifacts are unchanged.

## [1.0] — 2026-03-17

### Added
- Initial release of the **Anatomical Market Framework (AMF)**.
- `AMF Framework v1.docx` — the complete framework document.
- `AMF Framework v1.docx.ots` — OpenTimestamps proof anchoring the document to
  the Bitcoin blockchain as independent evidence of its creation date.
- `anatomical-market-framework` — plain-text overview of the framework's core
  components and analytical method.
- `LICENSE.txt` — proprietary, all-rights-reserved copyright notice.
