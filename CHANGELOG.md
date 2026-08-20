# Changelog

All notable changes to the Anatomical Market Framework (AMF) are documented in
this file. Versions correspond to framework releases.

## [Unreleased]

### Added
- `amf.numeric` — deterministic floating-point primitives (`stable_sum`, `square`,
  `clip_unit`) now used by every scoring path. `stable_sum` is exactly rounded, so a
  reduction no longer depends on the order its terms arrive in; `square` is written as a
  multiplication because IEEE 754 requires that to be correctly rounded, while `x ** 2`
  routes to the platform's `libm` `pow`, which does not have to be and measurably is not
  (`x ** 2` and `x * x` disagree for roughly 1 double in 1,200 on CPython 3.11/x86-64).
  Imported from `amf.numeric`, like the renderers in `amf.report` and `amf.viz`.
- `amf.invariants` — a guard every engine runs over its own result before returning it
  (`check_diagnostic_report`, `check_simulation_trace`, `check_resilience_score`,
  `check_sensitivity_report`, `check_centrality`, plus the `require_*` primitives). It
  enforces the properties the result types document: scores and stress levels finite and
  inside `[0, 1]`, a finite non-negative amplification factor, a settling time that is a
  step index or the `-1` sentinel, a strictly positive sensitivity span, and a
  max-normalised centrality vector. The checks are always on — there is no flag to forget.
- `InvariantError`, a new `AMFError` subclass raised when a computed result breaks one of
  those properties. It is an exception and not an `assert` deliberately: assertions are
  stripped under `python -O`, which would disable the guard exactly where a deployment
  most wants it.
- `docs/ROBUSTNESS_REVIEW.md` — a technical assessment of an external "advanced
  robustness" proposal, with the measurements behind each verdict and the counter-proposal
  actually implemented here. Documentation only.
- `.github/milestones.json`, `tools/sync_milestones.py`, and
  `.github/workflows/milestones.yml` — the delivery milestones as a checked-in,
  idempotent manifest, so the repository's Milestones section is reproducible rather than
  hand-maintained. `tests/unit/test_milestones_manifest.py` validates the manifest offline.

- `docs/90_DAY_PLAN_INDEX.md` — a navigation map of the 90-day implementation
  program's GitHub issue tree (one program issue, ten epics, fifty-four sub-issues),
  with the phase calendar, the metric ledger, the guardrails every issue inherits, and
  the three points where the source analysis was reconciled against the repository as it
  actually stands. Documentation only — the issues remain the source of truth and no
  package behaviour changes.
- `projects/` — a project section holding 73 charters that decompose the open
  backlog and the research discussions into bounded, individually executable
  units of work. Each charter states the dispute it settles, its purpose, ordered
  instructions, a task board, the autonomous agents that execute it (mandate,
  inputs, output artifact and stop condition each), the skills those agents
  invoke, objectively checkable acceptance criteria, a required-reading list of
  primary literature, and the exact commit subjects it produces. Charters are
  grouped into twelve tracks from governance and CI through numerical
  correctness, graph theory, diagnostics, simulation, policy architecture, market
  taxonomy, case studies, advanced methods, communication and IP protection.
  Supporting pages: `projects/AGENT_PROTOCOL.md`, `projects/SKILL_CATALOG.md`,
  `projects/COMMIT_PROTOCOL.md` and `projects/REFERENCES.md` (a 248-entry vetted
  bibliography of peer-reviewed articles, scholarly monographs, official
  instrument texts and standards specifications). Documentation only — no package
  behaviour changes.
- `.claude/agents/` — 22 autonomous agent definitions used by the project
  charters, each with a single mandate and a hard stop condition, and each bound
  by the repository's hard rules (non-trading naming, illustrative-not-validated
  output, protected-artifact integrity, zero runtime dependencies, determinism).
- `.claude/skills/` — 25 repeatable procedures the agents invoke, covering source
  vetting, determinism and floating-point auditing, invariant and property
  authoring, mutation and coverage gates, the non-trading boundary and module
  layering checks, config validation and schema round-tripping, graph, centrality,
  cascade, ensemble and sensitivity analysis, taxonomy, regime and case-study
  construction, figure rendering, documentation and changelog conventions,
  integrity verification, and adversarial red-teaming.
- `DiagnosticConfig.scale_concentration_by_reliance` (default `False`), which
  multiplies the concentration index by `min(1, total outgoing weight)`. The
  index is share-based, so it measures how unevenly a system's reliance is spread
  and not how much of it there is: a system leaning on a single `0.01` coupling
  scores the same maximum `1.0` as one wholly dependent on a `1.0` coupling, and
  four of the seven systems in `examples/sample_market.json` score `1.00` on that
  basis. It also makes the measure discontinuous at zero — an isolated system
  scores `0.00`, and giving it one trivial coupling scores `1.00`. Enabling the
  flag fixes both. It is opt-in because it moves every concentration score the
  engine reports; the default output is unchanged.
- `docs/roadmap.md` — a Phase 2 roadmap that triages the open issue backlog into
  charter-compliant, structural work: it proposes an expansion for "PSM", restates the
  non-trading / illustrative / frozen-anatomy guardrails, gives translation rules that
  map real-market asks onto structural proxies, and sequences the planned concepts.
  Documentation only — no package behaviour changes.
- Private-distribution guard: the `Private :: Do Not Upload` classifier in
  `pyproject.toml` makes PyPI reject any upload of this proprietary package, and
  `tests/unit/test_packaging.py` fails if that classifier is dropped from either
  the source config or the built wheel, if a public-index URL is added, or if the
  package and `pyproject.toml` versions drift apart. `RELEASING.md` documents the
  private release procedure.
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
- `ResilienceScore.amplification_factor` could be infinite. Amplification is peak aggregate
  stress divided by injected aggregate stress -- both criticality-weighted and both in
  `[0, 1]` -- but the ratio still overflows when the shocked system carries almost no
  criticality and its stress loads systems that carry a great deal: at a target criticality of
  `1e-310` the division reaches infinity. The infinity escaped into the result, and
  `render_json` then emitted `Infinity`, which is not valid JSON. The factor now saturates at
  the largest finite double. No non-degenerate market's score moves, because the amplification
  penalty already saturates at any factor of two or more. Found by the hypothesis suite via the
  new invariant guard -- the guard's first catch.
- Two assertions in `tests/unit/test_numeric.py` encoded CPython 3.11's summation behaviour and
  failed on 3.12 and 3.13, which replaced the built-in `sum`'s float accumulation with Neumaier
  compensated summation (`sum([1.0, 1e100, 1.0, -1e100])` is `0.0` on 3.11 and `2.0` on 3.12+).
  They now assert against an explicit left-to-right accumulator, which is naive on every version.
  A new test pins `stable_sum` to exact rational arithmetic so the reduction cannot drift between
  interpreters — the seam mattered: sampled over 400,000 random weight sets, 102,822 produced a
  concentration index that differed between the two summation algorithms.
- `DependencyGraph.centrality()` no longer depends on the order the dependencies were
  added in. The influence propagation accumulated into each target while iterating the
  pair-weight dict, which is keyed in insertion order; because floating-point addition is
  not associative, listing the same couplings in a different order shifted the published
  centralities by an ulp. Measured on `examples/sample_market.json`: **265 of 400** random
  permutations of its eight dependencies produced a different vector before the fix, and
  **0 of 1,000** after. This was a live breach of the project's rule that nothing
  user-visible may depend on assembly order.
- The resilience composite no longer drives its settling term negative on a multi-wave
  run. `propagate` extends the horizon to `max(max_steps, last injection step)`, but the
  score divided the settling time by `max_steps` regardless, so a shock scheduled past the
  budget produced a settling penalty above `1`. Measured: `max_steps=5` with a shock at
  `at_step=40` gave a settling time of 14, a penalty of 2.8, and a settling term of −1.8
  against a documented range of `[0, 1]`. The penalty is now measured against the horizon
  actually run and clipped. Single-shock runs are provably unaffected, since their horizon
  equals `max_steps`.

- `DependencyGraph` no longer lets the order dependencies were listed in change a
  market's scores. A pair coupled by several kinds had its aggregate weight summed
  in dict-insertion order, and floating-point addition is not associative, so the
  same market described with its couplings in a different order produced
  `edge_weight` values differing in the last bits — and with them different
  concentration scores. Kinds are now summed in `DependencyKind` declaration order,
  matching the canonical ordering every other graph query already used. Found by
  the existing order-independence property test, which had been passing only
  because the generator had not yet drawn a multi-kind pair with weights that
  expose it.
- `DependencyGraph.centrality()` no longer returns a ranking decided by where the
  iteration budget happened to stop. On a graph with no single dominant mode — a
  complete bipartite market with unequal sides, for instance — the normalised
  ranking cycles between two states forever, and at 200 iterations four of the six
  coupled systems scored `0.7222` while at 199 or 201 they scored `0.6923`. That
  case now raises `InvalidDependencyError`. Convergence is also now tested on the
  max-normalised vector rather than on raw influence added, which is scale-free and
  so settles correctly whether the underlying series converges or grows; the
  previous absolute threshold was unreachable within the default budget on densely
  coupled graphs and silently returned an under-converged result.
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
- The diagnostic overall index is now reduced with `stable_sum` rather than a running
  `+=`. The result is the correctly rounded value rather than an accumulation-order
  artefact, which moves it by one unit in the last place — on `examples/sample_market.json`
  from `0.27963855632147405` to `0.279638556321474`. Every per-system concentration score
  is unchanged, and no severity band moves.

- `DependencyGraph.centrality()` treats a diverging series as valid rather than as
  an error. Above `alpha = 1/spectral radius` the max-normalised result settles on
  the dominant-eigenvector direction, which is still a meaningful "most depended
  upon" ranking, so a densely coupled market now returns an answer instead of being
  refused. Only a genuinely unstable ranking is rejected. Every graph that returned
  a stable answer before returns exactly that answer; nothing in the diagnostic or
  simulation pipeline consumes `centrality`, so no published score moves.
- The diagnostic concentration driver now reports the coupling count and total
  reliance alongside the index (`reliance concentrated in 1 coupling(s) (HHI 1.00,
  total reliance 0.30)`). The index alone cannot distinguish a genuine
  concentration risk from a single trivial coupling, both of which score `1.00`.
  Scores are unchanged; only the explanatory text differs.
- CI now pins the third-party `markdown-link-check` action to a full commit SHA
  rather than the mutable `v1` tag, and moves the GitHub-owned actions to
  `checkout@v5`, `setup-python@v6`, and `upload-artifact@v6`, which clears the
  Node 20 deprecation warning the runner emitted for the previous majors.
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
