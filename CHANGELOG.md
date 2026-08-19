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
