# Anatomical Market Framework (AMF) v1.0

![License: Proprietary — All Rights Reserved](https://img.shields.io/badge/License-Proprietary-red)
![Status: Released](https://img.shields.io/badge/Status-v1.0%20Released-blue)
![CI](https://github.com/sadishaumantha-maker/AMF-PSM/actions/workflows/ci.yml/badge.svg)
![Integrity](https://github.com/sadishaumantha-maker/AMF-PSM/actions/workflows/integrity.yml/badge.svg)

**Author:** Sadisha  
**Date of original creation:** March 17, 2026  
**Location:** Rathnapura, Sri Lanka

---

## What is the Anatomical Market Framework?

The Anatomical Market Framework (AMF) is an original analytical framework developed by Sadisha. It provides a structured approach to understanding and interpreting market dynamics through an anatomical lens — mapping the components, relationships, and behaviours of markets in a way that mirrors the systematic study of anatomy.

The framework maps a market's structure to biological analogues: infrastructure (skeleton), capital flow (circulatory system), information and signals (nervous system), active participants (musculature), functional subsystems (organs), risk management and regulation (immune system), and value creation and destruction (metabolism). The full methodology and applications are described in the documents below.

---

## Repository Contents

| File | Description |
|------|-------------|
| `AMF Framework v1.docx` | The full AMF framework document (Microsoft Word format) |
| `AMF Framework v1.docx.ots` | OpenTimestamps blockchain proof — cryptographically verifies the document existed on March 17, 2026 |
| `anatomical-market-framework` | Plain-text overview of the framework's seven core components and analytical method |
| `LICENSE.txt` | Proprietary copyright notice — all rights reserved |
| `CITATION.cff` | Machine-readable citation and authorship metadata |
| `CHANGELOG.md` | Release history of the framework |
| `SHA256SUMS` | SHA-256 checksums of the canonical artifacts, for integrity verification |
| `.github/workflows/integrity.yml` | CI workflow that verifies the artifact checksums on every change |
| `src/amf/` | `amf` Python package — a software implementation of the AMF analytical method |
| `examples/`, `tests/` | Runnable examples and the test suite for the `amf` package |

---

## Software: the `amf` package

The repository also ships `amf`, a small, dependency-free Python package
(Python 3.11+) that turns the AMF *analytical method* into runnable software. It
models a market as the seven anatomical systems and the dependency/feedback graph
that couples them, then computes structural diagnostics and shock-propagation
simulations over that anatomy.

> **Not a trading system.** `amf` models market *structure and resilience* only.
> It contains no orders, brokers, prices, returns, P&L, signals, or backtests;
> every quantity it produces is a dimensionless structural measure. This boundary
> is enforced by a test (`tests/unit/test_non_trading_boundary.py`).

### Disclaimer

`amf` is an **illustrative, educational** structural-analysis tool. Its inputs,
thresholds (including the severity bands), weights, and scores are **not
empirically validated**. Its output is **not financial, investment, or trading
advice**, and it does **not** constitute a diagnosis, forecast, or prediction of
any real or live market. Every result describes only the user-supplied,
hypothetical market model passed to it. The command-line tool prints this notice
on `stderr` after each analytical command.

### Install

```sh
python -m pip install -e ".[dev]"
```

### Use it from the command line

```sh
amf describe                                            # the 7 systems & method
amf diagnose examples/sample_market.json                # structural weaknesses
amf simulate examples/sample_market.json --target circulatory --magnitude 0.8
amf simulate examples/sample_market.json --target circulatory --cascade-threshold 0.2
amf stress-test examples/sample_market.json             # shock each system in turn
amf sensitivity examples/sample_market.json --top 5      # what matters most, & where to intervene
amf ensemble examples/sample_market.json --target circulatory --runs 200
```

`diagnose`, `simulate`, `stress-test`, and `sensitivity` accept `--format json`
or `--format md`; `ensemble` accepts `--format json`.

Render the dependency graph or a shock timeline (no extra dependencies needed —
the SVG output is drawn with the standard library alone):

```sh
amf viz examples/sample_market.json -o market.svg                 # severity-coloured graph (SVG)
amf viz examples/sample_market.json --format dot | dot -Tpng ...  # via Graphviz
amf viz examples/sample_market.json --format mermaid              # for Markdown/Mermaid renderers
amf viz examples/sample_market.json --timeline circulatory -o timeline.svg
```

### Extended simulation

The shock-propagation simulation is a damped linear diffusion by default. Damping
and absorptive capacity pull the trajectory down, but they do not make the step map
a contraction for every market, so settling is reported against the `max_steps`
budget rather than guaranteed. Four **opt-in** extensions add richer, still-bounded
and reproducible behaviour:

- **Threshold / cascade dynamics** (`SimulationConfig(cascade_threshold=…)`): systems
  that cross the threshold become impaired — they amplify onward stress and absorb
  less — producing tipping and self-reinforcing cascades, reported as `tipped_systems`.
- **Monte Carlo ensemble** (`ShockSimulator.ensemble`): summarise resilience across
  many seeded, jittered replications as a `ResilienceDistribution`.
- **Time-scheduled / multi-wave shocks** (`Shock(at_step=…)`): inject a second wave at
  a later timestep.
- **Recovery / intervention** (`SimulationConfig(recovery_rate=…)`, `Intervention`):
  active healing and time-gated containment that boosts a system's absorptive capacity.

See `examples/cascade_scenario.py`. The nonlinear cascade regime can settle at a
persistent non-zero state, and pushes the per-step gain higher still.

### Use it from Python

```python
from amf import DiagnosticEngine, Market, MarketBoundary, Shock, ShockSimulator, SystemKind
from amf.systems import skeleton, circulatory, nervous, musculature, organs, immune, metabolism

market = Market.assemble(
    MarketBoundary("equities", "US", "intraday"),
    [skeleton(), circulatory(), nervous(), musculature(), organs(), immune(), metabolism()],
)
report = DiagnosticEngine().diagnose(market)
score = ShockSimulator(market).resilience(Shock(SystemKind.CIRCULATORY, 0.8))
```

See `examples/equity_market.py`, `examples/liquidity_shock.py`, and
`examples/where_to_intervene.py` for complete runnable scripts, and `CLAUDE.md`
for the design and contributor guide.

### Roadmap

Planned Phase 2 work and the triage of the open issue backlog into
charter-compliant, structural tickets live in [`docs/roadmap.md`](docs/roadmap.md).

### Develop

```sh
ruff check . && ruff format --check .   # lint & format
mypy                                    # type-check (strict)
pytest                                  # tests with coverage gate (100%)
```

The `CI` GitHub Actions workflow runs all of the above (plus YAML, citation, and
Markdown-link validation) on every push and pull request.

---

## Integrity, Provenance & Rights

This repository uses three independent, layered mechanisms to establish and protect authorship of the AMF:

### 1. Blockchain timestamp (OpenTimestamps)
The file `AMF Framework v1.docx.ots` is an **OpenTimestamps** proof. It cryptographically anchors the contents of `AMF Framework v1.docx` to the Bitcoin blockchain, providing independent, tamper-proof evidence that this exact version of the document existed on the date it was created.

To verify the timestamp independently:
1. Visit [https://opentimestamps.org](https://opentimestamps.org)
2. Upload both `AMF Framework v1.docx` and `AMF Framework v1.docx.ots` together
3. The site will confirm the timestamp against the Bitcoin blockchain

### 2. Checksums (SHA-256)
`SHA256SUMS` records the exact SHA-256 hash of each canonical artifact. Anyone can confirm a file has not been altered by running, from the repository root:

```sh
sha256sum --check SHA256SUMS
```

### 3. Continuous verification (CI)
The `Integrity` GitHub Actions workflow runs the checksum verification automatically on every push and pull request, so any unauthorized change to a protected file is detected immediately.

---

## License and Copyright

Copyright (c) 2026 Sadisha. **All Rights Reserved.**

This work is proprietary. No part of this framework or its associated documents may be reproduced, distributed, published, modified, adapted, translated, transmitted, or used in any form — commercial or non-commercial — without the **explicit prior written permission** of the author. Unauthorized use may result in civil and criminal liability under applicable copyright and intellectual property law.

See [`LICENSE.txt`](LICENSE.txt) for the full notice.

**The `amf` package is distributed privately only.** It is never published to
PyPI or any other public index: the packaging metadata carries the
`Private :: Do Not Upload` classifier, which makes PyPI reject the upload, and
a test enforces that the guard stays in place. See [`RELEASING.md`](RELEASING.md)
for the release and distribution procedure.

---

## Contact and Permissions

For permissions, licensing inquiries, or collaboration requests, please contact the author directly via GitHub ([@sadishaumantha-maker](https://github.com/sadishaumantha-maker)).
