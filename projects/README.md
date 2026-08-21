# Projects

The AMF-PSM project section. Each entry below is a **charter**: a written, self-contained unit of work
that settles one specific dispute raised in the repository's issues or in
[`docs/RESEARCH_DISCUSSIONS.md`](../docs/RESEARCH_DISCUSSIONS.md) and
[`docs/QUANTUM_NEURAL_RESEARCH.md`](../docs/QUANTUM_NEURAL_RESEARCH.md).

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. No project in
> this section may introduce orders, prices, P&L, trading signals or backtests, and no output of this
> work is financial advice, a diagnosis, or a forecast of any real market. See
> [`CLAUDE.md`](../CLAUDE.md) -> *Hard rules*.

## What a charter contains

| Section | What it fixes |
|---------|---------------|
| The dispute this project settles | The actual disagreement, stated so both sides recognise it |
| Purpose | What the project produces, in two or three sentences |
| Scope | What is in, and explicitly what is out |
| Instructions | Ordered steps; no step starts before the previous artifact is committed |
| Task board | The checklist |
| Autonomous agents | Which agents run, each with a mandate, inputs, output and a stop condition |
| Skills | Which skills the work invokes, and when |
| Deliverables | The files that must exist at the end |
| Acceptance criteria | Objectively checkable; the project is not done until every line is true |
| Required reading | Primary literature and standard graduate texts |
| Commit protocol | The exact commit subjects this project produces |

## How the pieces fit

- **Agents** are defined once in [`.claude/agents/`](../.claude/agents) and are given a
  project-specific mandate by each charter. An agent may not widen its own mandate; it stops at its
  stop condition and hands off. See [AGENT_PROTOCOL.md](AGENT_PROTOCOL.md).
- **Skills** are defined once in [`.claude/skills/`](../.claude/skills) and are invoked by agents at
  the moments each charter names. See [SKILL_CATALOG.md](SKILL_CATALOG.md).
- **Sources** are collected in [REFERENCES.md](REFERENCES.md) and repeated in full inside each charter,
  so a charter is readable on its own.
- **Commits** follow [COMMIT_PROTOCOL.md](COMMIT_PROTOCOL.md).

## Reading order

Track A and Track B are prerequisites for everything else: until the backlog is triaged and CI is proven
to block, no analytical result produced here can be trusted or reproduced. Tracks C to F harden the
instrument itself. Tracks G to I supply the domain content. Tracks J to L cover advanced methods,
communication and the protection of the intellectual property.

Track M is the exception to that order and runs first regardless: it holds the failures that are red on
`main` right now, and a red build makes every other result unreproducible. Tracks N to S extend the
domain coverage into the disputes the first pass left uncharted - policy contagion, market abuse,
shadow finance, technology, geopolitics and climate. Track T writes the eleven research modules the
discussion index promises and does not contain. Track U is last and gating in the same sense Track B
is first: it asks what would falsify any of this, and answers to someone other than the authors.

## Tracks

| Track | Name | Projects | Aim |
|-------|------|----------|-----|
| **A** | Governance, Ownership & Delivery Cadence | 6 | Make the backlog legible and the delivery rhythm predictable before any modelling work scales. |
| **B** | Engineering Quality, CI & Reproducibility | 7 | Guarantee that an identical input yields an identical, independently reproducible result. |
| **C** | Numerical Correctness & Determinism | 6 | Defend the floating-point and ordering guarantees the whole diagnostic instrument rests on. |
| **D** | Graph & Network Theory of Market Structure | 7 | Put every graph query in `graph.py` on a cited algorithmic and theoretical footing. |
| **E** | Diagnostics, Sensitivity & Leverage | 6 | Justify every weight, threshold and ranking rule in the scoring pipeline, or replace it. |
| **F** | Shock Propagation, Cascades & Resilience | 7 | Ground the simulation dynamics in the contagion and critical-transition literature. |
| **G** | Policy Architecture & Regulatory Regimes | 7 | Settle the policy-stack disputes with constitutional-economics and institutional-change scholarship. |
| **H** | Global Market Mapping, Taxonomy & Standards | 6 | Fix the atomic unit of a 'market' and the classification scheme, using published standards. |
| **I** | Empirical Case Studies & Forensic Structure | 5 | Test the framework against documented episodes instead of intuition. |
| **J** | Advanced Methods: Topology, Learning, Information & Quantum | 7 | Decide, on evidence, which advanced method earns a place in AMF and which is decoration. |
| **K** | Communication, Visualisation & Documentation | 5 | Make the output honest, readable and impossible to over-read. |
| **L** | Intellectual Property, Provenance & Security | 4 | Keep the protected artifacts provably untouched and the distribution private. |
| **M** | Live Defects and the Green-Main Obligation | 4 | Close the failures actually red on `main` today, and stop the same class recurring. |
| **N** | Policy-Market Contagion and Systemic Indicators | 6 | Model the channel that runs through the rulebook rather than through the coupling graph. |
| **O** | Market Abuse and Forensic Network Structure | 5 | Say what a structural model can and cannot detect, before anyone claims it detects abuse. |
| **P** | Shadow Finance, Capital Flows and Currency | 6 | Represent the parts of the system that sit outside the perimeter the framework can see. |
| **Q** | Technology, Fintech and AI Risk | 6 | Treat the toolchain of finance as market structure, because it now is. |
| **R** | Geopolitics, Sanctions and Fragmentation | 6 | Model chokepoints and fragmentation structurally, without taking a political position. |
| **S** | Climate, Nature and Long-Horizon Risk | 6 | Handle risks whose horizon exceeds every feedback loop the framework represents. |
| **T** | The Promised Research Modules | 11 | Write the eleven modules the discussion index links to and that do not exist. |
| **U** | Method, Epistemics and External Validation | 6 | State what would falsify the framework, and submit it to something other than its authors. |

**129 charters in total.**

---

## Track A - Governance, Ownership & Delivery Cadence

*Make the backlog legible and the delivery rhythm predictable before any modelling work scales.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P01](P01-backlog-triage-constitution-and-dependency-graph/README.md) | Backlog triage constitution and dependency graph | 1 week | issues #111 (1.5), #106 (0.8), #104 (0.6), #147 (9.1) |
| [P02](P02-branch-protection-ruleset-design-for-main-develop-and-re/README.md) | Branch protection ruleset design for main, develop and release | 3 days | issues #107 (1.1), #108 (1.2), #109 (1.3), #153 (9.6) |
| [P03](P03-ownership-model-codeowners-and-assignee-discipline/README.md) | Ownership model, CODEOWNERS and assignee discipline | 2 days | issues #103 (0.5), #148 (9.2), #110 (1.4) |
| [P04](P04-milestone-design-and-a-defensible-release-cadence/README.md) | Milestone design and a defensible release cadence | 3 days | issues #105 (0.7), #143 (6.7), #112 (1.6), #149 (9.3) |
| [P05](P05-delivery-metric-instrumentation-and-the-goodhart-guard/README.md) | Delivery metric instrumentation and the Goodhart guard | 1 week | issues #147-#155 (9.1-9.8) |
| [P06](P06-charter-ratification-for-the-phase-2-and-new-concepts-ba/README.md) | Charter ratification for the phase-2 and new-concepts backlog items | 4 days | issues #145 (7.2, #21), #146 (7.3, #23) |

## Track B - Engineering Quality, CI & Reproducibility

*Guarantee that an identical input yields an identical, independently reproducible result.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P07](P07-continuous-integration-audit-and-hardening/README.md) | Continuous integration audit and hardening | 4 days | issues #114 (2.2), #152 (9.5) |
| [P08](P08-private-release-workflow-without-any-public-index-exposu/README.md) | Private release workflow without any public index exposure | 3 days | issue #115 (2.3), `RELEASING.md` |
| [P09](P09-dependency-update-policy-and-supply-chain-review-gates/README.md) | Dependency update policy and supply-chain review gates | 2 days | issue #118 (2.6) |
| [P10](P10-coverage-reporting-badge-honesty-and-the-trend-record/README.md) | Coverage reporting, badge honesty and the trend record | 2 days | issues #117 (2.5), #150 (9.4), #152 (9.5) |
| [P11](P11-mutation-testing-programme-to-expose-coverage-blind-spot/README.md) | Mutation testing programme to expose coverage blind spots | 1.5 weeks | `CLAUDE.md` ("100% coverage is not the same as 100% tested"), issue #150 |
| [P12](P12-reproducible-run-manifest-for-every-published-number/README.md) | Reproducible-run manifest for every published number | 1 week | `CLAUDE.md` determinism rules; issues #137 (6.1), #139 (6.3) |
| [P13](P13-documentation-build-evaluation-and-the-decision-to-add-o/README.md) | Documentation build evaluation and the decision to add or refuse it | 3 days | issue #116 (2.4), #154 (9.7) |

## Track C - Numerical Correctness & Determinism

*Defend the floating-point and ordering guarantees the whole diagnostic instrument rests on.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P14](P14-floating-point-summation-audit-of-the-diagnostic-index-a/README.md) | Floating-point summation audit of the diagnostic index and HHI | 1 week | `CLAUDE.md` -> Determinism; `src/amf/diagnostics.py` |
| [P15](P15-canonical-ordering-as-a-proof-obligation-not-a-conventio/README.md) | Canonical ordering as a proof obligation, not a convention | 4 days | `CLAUDE.md` -> Determinism; `tests/unit/test_properties.py` |
| [P16](P16-severity-band-totality-and-the-nan-pessimism-policy/README.md) | Severity band totality and the NaN pessimism policy | 3 days | `src/amf/models.py` -> `Severity.from_score` |
| [P17](P17-completeness-audit-of-tuning-knob-validation/README.md) | Completeness audit of tuning-knob validation | 4 days | `DiagnosticConfig`, `SimulationConfig`, `SensitivityConfig`, `DependencyGraph.centrality` |
| [P18](P18-randomness-policy-seeding-discipline-and-ensemble-replic/README.md) | Randomness policy, seeding discipline and ensemble replication | 1 week | `SimulationConfig.jitter` / `seed`; `ShockSimulator.ensemble` |
| [P19](P19-percentile-estimator-selection-and-uncertainty-on-ensemb/README.md) | Percentile estimator selection and uncertainty on ensemble output | 4 days | `ResilienceDistribution`; "percentiles computed in-house by linear interpolation, no numpy" |

## Track D - Graph & Network Theory of Market Structure

*Put every graph query in `graph.py` on a cited algorithmic and theoretical footing.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P20](P20-feedback-loop-enumeration-correctness-and-complexity-aga/README.md) | Feedback loop enumeration: correctness and complexity against Johnson's algorithm | 1 week | `src/amf/graph.py` -> feedback-loop (simple-cycle) enumeration |
| [P21](P21-articulation-points-verification-against-hopcroft-tarjan/README.md) | Articulation points: verification against Hopcroft-Tarjan and the directed-graph caveat | 4 days | `src/amf/graph.py` -> articulation points; `DiagnosticEngine` SPOF detection |
| [P22](P22-katz-centrality-convergence-and-the-spectral-radius-guar/README.md) | Katz centrality convergence and the spectral radius guard | 1 week | `DependencyGraph.centrality`; `CLAUDE.md` -> Centrality |
| [P23](P23-centrality-selection-katz-against-betweenness-eigenvecto/README.md) | Centrality selection: Katz against betweenness, eigenvector and DebtRank | 1.5 weeks | `CLAUDE.md`: "Nothing in the scoring pipeline consumes centrality; it is a standalone query." |
| [P24](P24-multi-kind-edge-aggregation-semantics-and-the-cap-at-one/README.md) | Multi-kind edge aggregation semantics and the cap at one | 4 days | `CLAUDE.md` -> Market JSON schema; `DependencyGraph.edge_weight` |
| [P25](P25-coupling-matrix-direction-semantics-stress-flows-against/README.md) | Coupling matrix direction semantics: stress flows against the dependency edge | 3 days | `CouplingMatrix`; `CLAUDE.md` -> Simulation ("stress flows target -> source") |
| [P26](P26-null-models-and-structural-significance-for-amf-graph-fi/README.md) | Null models and structural significance for AMF graph findings | 1.5 weeks | `docs/RESEARCH_DISCUSSIONS.md` -> Theme D: Network Effects |

## Track E - Diagnostics, Sensitivity & Leverage

*Justify every weight, threshold and ranking rule in the scoring pipeline, or replace it.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P27](P27-derivation-and-defence-of-the-fragility-formula/README.md) | Derivation and defence of the fragility formula | 1 week | `src/amf/diagnostics.py`; `CLAUDE.md` -> Diagnostics |
| [P28](P28-concentration-share-based-hhi-against-reliance-scaled-co/README.md) | Concentration: share-based HHI against reliance-scaled concentration | 1 week | `DiagnosticConfig.scale_concentration_by_reliance`; `CLAUDE.md` -> Diagnostics |
| [P29](P29-weight-elicitation-for-the-diagnostic-blend-and-the-comp/README.md) | Weight elicitation for the diagnostic blend and the composite-index audit | 1.5 weeks | `DiagnosticConfig` weights `0.4 / 0.3 / 0.3`; `CLAUDE.md` -> Diagnostics |
| [P30](P30-single-point-of-failure-definition-and-the-low-redundanc/README.md) | Single point of failure: definition and the low-redundancy threshold | 4 days | `_LOW_REDUNDANCY = 0.5`; SPOF ranking by criticality |
| [P31](P31-from-one-at-a-time-perturbation-to-a-defensible-sensitiv/README.md) | From one-at-a-time perturbation to a defensible sensitivity design | 1.5 weeks | `SensitivityAnalyzer`; `SensitivityConfig.step` |
| [P32](P32-leverage-points-aligning-the-ranking-with-the-systems-in/README.md) | Leverage points: aligning the ranking with the systems-intervention literature | 1 week | `LeveragePoint`; `SystemMetric.improving_direction()` |

## Track F - Shock Propagation, Cascades & Resilience

*Ground the simulation dynamics in the contagion and critical-transition literature.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P33](P33-stability-analysis-of-the-stress-step-map/README.md) | Stability analysis of the stress step map | 1.5 weeks | `ShockSimulator.propagate`; `CLAUDE.md` -> Simulation |
| [P34](P34-absorptive-capacity-justifying-the-0-5-0-3-0-2-weights/README.md) | Absorptive capacity: justifying the 0.5 / 0.3 / 0.2 weights | 1 week | `AnatomicalSystem.absorptive_capacity()` |
| [P35](P35-cascade-threshold-and-gain-calibration-against-the-conta/README.md) | Cascade threshold and gain calibration against the contagion literature | 1.5 weeks | `SimulationConfig.cascade_threshold`, `cascade_gain`, `cascade_absorption_drop` |
| [P36](P36-recovery-dynamics-hysteresis-and-the-persistent-non-zero/README.md) | Recovery dynamics, hysteresis and the persistent non-zero state | 1 week | `SimulationConfig.recovery_rate`; cascade non-convergence caveat |
| [P37](P37-multi-wave-shocks-and-timing-independent-normalisation/README.md) | Multi-wave shocks and timing-independent normalisation | 1 week | `Shock.at_step`; "amplification/absorption use total injected load as a timing-independent denominator" |
| [P38](P38-intervention-modelling-and-the-counterfactual-claim-it-i/README.md) | Intervention modelling and the counterfactual claim it implies | 1 week | `Intervention`; `examples/cascade_scenario.py` |
| [P39](P39-the-resilience-composite-and-early-warning-signal-candid/README.md) | The resilience composite and early-warning signal candidates | 1.5 weeks | `resilience = 0.6 x absorbed + 0.25 x (1 - amp_penalty) + 0.15 x (1 - settle_penalty)` |

## Track G - Policy Architecture & Regulatory Regimes

*Settle the policy-stack disputes with constitutional-economics and institutional-change scholarship.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P40](P40-formalising-the-policy-tier-hierarchy-who-decides-and-ho/README.md) | Formalising the policy-tier hierarchy: who decides, and how fast | 1.5 weeks | issue #120 (31a); PR #42 (immune system as a layered policy stack) |
| [P41](P41-amendment-procedures-per-tier-as-the-regulatory-change-m/README.md) | Amendment procedures per tier as the regulatory change mechanism | 1 week | issue #121 (31b) |
| [P42](P42-entrenchment-thresholds-and-constitutional-economics/README.md) | Entrenchment thresholds and constitutional economics | 2 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 1.2; issue #122 (31c) |
| [P43](P43-institutional-change-modes-and-their-structural-signatur/README.md) | Institutional change modes and their structural signature | 2 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 1.3; issue #123 (31d) |
| [P44](P44-cross-jurisdiction-harmonisation-and-the-impedance-misma/README.md) | Cross-jurisdiction harmonisation and the impedance-mismatch cost | 2 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 1.1 |
| [P45](P45-government-philosophy-archetypes-as-structural-regime-ty/README.md) | Government philosophy archetypes as structural regime types | 2 weeks | issues #134 (5.4), #135 (5.5), #136 (5.6) |
| [P46](P46-regulatory-capture-and-policy-failure-as-structural-cond/README.md) | Regulatory capture and policy failure as structural conditions | 1.5 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 4.3 |

## Track H - Global Market Mapping, Taxonomy & Standards

*Fix the atomic unit of a 'market' and the classification scheme, using published standards.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P47](P47-equity-market-taxonomy-by-country/README.md) | Equity market taxonomy by country | 2 weeks | issue #124 (25a); `docs/ANALYSIS_AND_ROADMAP.md` #25 |
| [P48](P48-the-atomic-unit-of-a-market-exchange-venue-or-segment/README.md) | The atomic unit of a market: exchange, venue or segment | 1.5 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 2.1 |
| [P49](P49-structural-proxies-for-liquidity-and-transparency-withou/README.md) | Structural proxies for liquidity and transparency without market data | 2 weeks | issue #125 (25b, "volume, spreads"); Discussion 2.2 |
| [P50](P50-regulatory-regime-mapping-by-country-and-the-strictness/README.md) | Regulatory regime mapping by country and the strictness problem | 2 weeks | issue #126 (25c); Discussion 2.3 |
| [P51](P51-non-equity-markets-commodities-bonds-and-foreign-exchang/README.md) | Non-equity markets: commodities, bonds and foreign exchange | 2 weeks | issue #144 (7.1, #26) |
| [P52](P52-adopting-published-identifier-and-classification-standar/README.md) | Adopting published identifier and classification standards | 1.5 weeks | issue #43 (global stock market standards); Discussion 2.3 |

## Track I - Empirical Case Studies & Forensic Structure

*Test the framework against documented episodes instead of intuition.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P53](P53-case-study-protocol-and-the-reusable-research-template/README.md) | Case study protocol and the reusable research template | 1 week | issues #131 (5.1), #132 (5.2) |
| [P54](P54-short-seller-research-reports-as-structural-evidence/README.md) | Short-seller research reports as structural evidence | 2 weeks | issues #131-#133 (5.1-5.3, #28) |
| [P55](P55-the-2007-2009-crisis-as-a-structural-stress-trace/README.md) | The 2007-2009 crisis as a structural stress trace | 2.5 weeks | `docs/RESEARCH_DISCUSSIONS.md` Track 3 |
| [P56](P56-the-2010-flash-crash-as-a-market-microstructure-fragilit/README.md) | The 2010 flash crash as a market-microstructure fragility case | 1.5 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 6.1; Track 3 |
| [P57](P57-frontier-market-policy-volatility-and-capital-flow-rever/README.md) | Frontier market policy volatility and capital-flow reversal | 2 weeks | `docs/RESEARCH_DISCUSSIONS.md` Track 5 |

## Track J - Advanced Methods: Topology, Learning, Information & Quantum

*Decide, on evidence, which advanced method earns a place in AMF and which is decoration.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P58](P58-topological-data-analysis-of-structural-change/README.md) | Topological data analysis of structural change | 2 weeks | `docs/QUANTUM_NEURAL_RESEARCH.md` Discussion H2 |
| [P59](P59-graph-neural-networks-what-they-would-add-and-what-they/README.md) | Graph neural networks: what they would add and what they would cost | 2 weeks | `docs/QUANTUM_NEURAL_RESEARCH.md` Discussions D1-D3 |
| [P60](P60-information-theoretic-structural-entropy/README.md) | Information-theoretic structural entropy | 1.5 weeks | `docs/QUANTUM_NEURAL_RESEARCH.md` Discussion Q3 |
| [P61](P61-regime-transitions-markov-formalism-against-quantum-supe/README.md) | Regime transitions: Markov formalism against quantum-superposition language | 1 week | `docs/QUANTUM_NEURAL_RESEARCH.md` Discussions Q1, Q2 |
| [P62](P62-causal-claims-about-structure-and-what-the-framework-can/README.md) | Causal claims about structure and what the framework can support | 2 weeks | `docs/RESEARCH_DISCUSSIONS.md` Track 3; Discussion 3.2 (feedback loops markets and policy) |
| [P63](P63-quantum-computing-feasibility-triage-for-structural-anal/README.md) | Quantum computing feasibility triage for structural analysis | 1.5 weeks | `docs/QUANTUM_NEURAL_RESEARCH.md` Discussion H1; adoption roadmap |
| [P64](P64-interpretability-as-a-design-constraint-not-a-post-hoc-e/README.md) | Interpretability as a design constraint, not a post-hoc explanation | 1 week | `docs/QUANTUM_NEURAL_RESEARCH.md` Discussion I2; `WeaknessFinding.drivers` |

## Track K - Communication, Visualisation & Documentation

*Make the output honest, readable and impossible to over-read.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P65](P65-visualisation-grammar-and-perception-audit-for-the-rende/README.md) | Visualisation grammar and perception audit for the renderers | 1.5 weeks | `src/amf/viz.py`; `_FOOTNOTE` |
| [P66](P66-uncertainty-communication-in-every-rendered-report/README.md) | Uncertainty communication in every rendered report | 1 week | `report.py`; the P19, P29 and P39 uncertainty outputs |
| [P67](P67-the-core-documentation-set-getting-started-architecture/README.md) | The core documentation set: getting started, architecture and examples | 2 weeks | issues #140 (6.4), #141 (6.5), #142 (6.6), #154 (9.7) |
| [P68](P68-glossary-and-controlled-vocabulary-for-the-framework/README.md) | Glossary and controlled vocabulary for the framework | 1 week | `docs/RESEARCH_DISCUSSIONS.md` Theme A; the non-trading naming rule |
| [P69](P69-disclaimer-integrity-and-defence-against-over-reading/README.md) | Disclaimer integrity and defence against over-reading | 1 week | package docstring, `README.md`, `cli._DISCLAIMER`, `viz._FOOTNOTE` |

## Track L - Intellectual Property, Provenance & Security

*Keep the protected artifacts provably untouched and the distribution private.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P70](P70-integrity-chain-verification-for-the-protected-artifacts/README.md) | Integrity chain verification for the protected artifacts | 1 week | `SHA256SUMS`, `.github/workflows/integrity.yml`, the OpenTimestamps proof |
| [P71](P71-private-distribution-enforcement-audit/README.md) | Private distribution enforcement audit | 4 days | `RELEASING.md`, `pyproject.toml` classifier, `tests/unit/test_packaging.py` |
| [P72](P72-secure-development-framework-alignment-for-the-toolchain/README.md) | Secure development framework alignment for the toolchain | 1.5 weeks | `.pre-commit-config.yaml`, CI workflows, `SECURITY.md` |
| [P73](P73-vulnerability-disclosure-process-maturity/README.md) | Vulnerability disclosure process maturity | 4 days | `SECURITY.md` |

## Track M - Live Defects and the Green-Main Obligation

*Close the failures actually red on `main` today, and stop the same class recurring.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P74](P74-the-expired-control-premise-in-the-stable-sum-tests/README.md) | The expired control premise in the stable_sum tests | 2 days | `tests/unit/test_numeric.py`; CI red on py3.12 and py3.13 |
| [P75](P75-eleven-promised-research-modules-that-do-not-exist/README.md) | Eleven promised research modules that do not exist | 3 days | `docs/discussions/README.md`; the eleven dead links failing `Validate metadata` |
| [P76](P76-restoring-a-green-main-and-making-red-on-main-a-blocking/README.md) | Restoring a green main and making red-on-main a blocking condition | 4 days | CI red on `main` continuously since run #115 |
| [P77](P77-behavioural-drift-in-the-platform-beneath-a-determinism/README.md) | Behavioural drift in the platform beneath a determinism guarantee | 1 week | P74; `CLAUDE.md` -> Determinism |

## Track N - Policy-Market Contagion and Systemic Indicators

*Model the channel that runs through the rulebook rather than through the coupling graph.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P78](P78-contagion-through-the-policy-tier-rather-than-the-coupli/README.md) | Contagion through the policy tier rather than the coupling graph | 2 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 3.1 |
| [P79](P79-the-markets-to-policy-feedback-loop-and-reflexivity/README.md) | The markets-to-policy feedback loop and reflexivity | 2 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 3.2 |
| [P80](P80-systemic-risk-indicators-and-which-ones-amf-can-honestly/README.md) | Systemic risk indicators and which ones AMF can honestly compute | 2 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 3.3 |
| [P81](P81-regulatory-uncertainty-as-a-structural-stress-input/README.md) | Regulatory uncertainty as a structural stress input | 1.5 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 1.3; P43 |
| [P82](P82-cross-border-policy-spillover-and-the-boundary-of-a-mode/README.md) | Cross-border policy spillover and the boundary of a modelled market | 1.5 weeks | Discussion 3.1; P44; `MarketBoundary` |
| [P83](P83-backstops-and-the-lender-of-last-resort-as-immune-struct/README.md) | Backstops and the lender of last resort as immune structure | 1.5 weeks | PR #42 (immune system as a layered policy stack); Discussion 3.1 |

## Track O - Market Abuse and Forensic Network Structure

*Say what a structural model can and cannot detect, before anyone claims it detects abuse.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P84](P84-market-abuse-detection-via-network-analysis-what-is-actu/README.md) | Market abuse detection via network analysis: what is actually claimable | 2 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 4.2 |
| [P85](P85-graph-anomaly-detection-and-the-legitimacy-of-structural/README.md) | Graph anomaly detection and the legitimacy of structural outlier claims | 1.5 weeks | Discussion 4.2; P26 null models |
| [P86](P86-digit-distribution-screening-scope-assumptions-and-misus/README.md) | Digit-distribution screening: scope, assumptions and misuse | 1 week | Discussion 4.2; P54 |
| [P87](P87-coordination-structures-and-what-a-dependency-graph-cann/README.md) | Coordination structures and what a dependency graph cannot distinguish | 1.5 weeks | Discussion 4.2; P24 |
| [P88](P88-detection-base-rates-and-the-arithmetic-of-a-rare-event/README.md) | Detection base rates and the arithmetic of a rare-event screen | 1 week | P84; P85 |

## Track P - Shadow Finance, Capital Flows and Currency

*Represent the parts of the system that sit outside the perimeter the framework can see.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P89](P89-informal-finance-and-shadow-banking-as-a-system-the-peri/README.md) | Informal finance and shadow banking as a system the perimeter excludes | 2 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 5.2 |
| [P90](P90-sudden-stops-and-capital-flight-as-structural-withdrawal/README.md) | Sudden stops and capital flight as structural withdrawal | 1.5 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 5.3; P57 |
| [P91](P91-currency-mismatch-as-a-structural-rather-than-a-market-q/README.md) | Currency mismatch as a structural rather than a market quantity | 1.5 weeks | Discussion 5.3 |
| [P92](P92-the-global-financial-cycle-and-the-limits-of-policy-auto/README.md) | The global financial cycle and the limits of policy autonomy | 1.5 weeks | Discussion 5.3; Discussion 7.2 |
| [P93](P93-payment-and-settlement-infrastructure-as-skeletal-depend/README.md) | Payment and settlement infrastructure as skeletal dependence | 1.5 weeks | `SystemKind.skeleton`; CPMI-IOSCO principles |
| [P94](P94-reserve-currency-asymmetry-and-the-non-equivalence-of-ma/README.md) | Reserve currency asymmetry and the non-equivalence of markets | 1.5 weeks | Discussion 5.3; Discussion 7.1 |

## Track Q - Technology, Fintech and AI Risk

*Treat the toolchain of finance as market structure, because it now is.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P95](P95-fintech-disruption-and-the-regulatory-arbitrage-mechanis/README.md) | Fintech disruption and the regulatory-arbitrage mechanism | 1.5 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 6.2 |
| [P96](P96-machine-learning-in-finance-as-a-systemic-risk-channel/README.md) | Machine learning in finance as a systemic risk channel | 2 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 6.3 |
| [P97](P97-monoculture-when-redundancy-stops-providing-substitutabi/README.md) | Monoculture: when redundancy stops providing substitutability | 1.5 weeks | P27; P34; P96 |
| [P98](P98-supervisory-technology-as-measurable-immune-capacity/README.md) | Supervisory technology as measurable immune capacity | 1 week | Discussion 6.2; PR #42 |
| [P99](P99-third-party-and-cloud-concentration-as-an-unmodelled-dep/README.md) | Third-party and cloud concentration as an unmodelled dependency | 1.5 weeks | Discussion 6.2; `SystemKind.skeleton` |
| [P100](P100-herding-and-the-behavioural-boundary-of-a-structural-mod/README.md) | Herding and the behavioural boundary of a structural model | 1 week | Discussion 6.3; P96 |

## Track R - Geopolitics, Sanctions and Fragmentation

*Model chokepoints and fragmentation structurally, without taking a political position.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P101](P101-sanctions-as-a-structural-chokepoint-rather-than-a-polit/README.md) | Sanctions as a structural chokepoint rather than a political act | 2 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 7.1 |
| [P102](P102-central-bank-independence-as-an-amendment-procedure-prop/README.md) | Central bank independence as an amendment-procedure property | 1.5 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 7.2 |
| [P103](P103-fragmentation-and-whether-a-split-market-is-one-market-o/README.md) | Fragmentation and whether a split market is one market or two | 2 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 7.3; P48; P82 |
| [P104](P104-network-asymmetry-and-the-leverage-a-topology-confers/README.md) | Network asymmetry and the leverage a topology confers | 1.5 weeks | Discussion 7.1; P23; P101 |
| [P105](P105-conflicting-jurisdictional-requirements-as-an-unsatisfia/README.md) | Conflicting jurisdictional requirements as an unsatisfiable constraint set | 1 week | Discussion 1.1; Discussion 7.3 |
| [P106](P106-the-sovereign-financial-loop-as-a-cycle-the-framework-sh/README.md) | The sovereign-financial loop as a cycle the framework should be able to see | 1.5 weeks | Discussion 7.2; `graph.py` feedback loops |

## Track S - Climate, Nature and Long-Horizon Risk

*Handle risks whose horizon exceeds every feedback loop the framework represents.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P107](P107-climate-risk-and-the-horizon-problem-for-a-step-based-mo/README.md) | Climate risk and the horizon problem for a step-based model | 2 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 8.1 |
| [P108](P108-rating-divergence-and-what-a-composite-built-on-disputed/README.md) | Rating divergence and what a composite built on disputed inputs inherits | 1.5 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 8.2 |
| [P109](P109-nature-related-dependence-and-the-limits-of-a-financial/README.md) | Nature-related dependence and the limits of a financial-system boundary | 1.5 weeks | `docs/RESEARCH_DISCUSSIONS.md` Discussion 8.3 |
| [P110](P110-transition-risk-as-policy-change-and-the-one-climate-cha/README.md) | Transition risk as policy change and the one climate channel that fits | 1 week | Discussion 8.1; P43 |
| [P111](P111-long-horizons-discounting-and-why-the-framework-has-no-t/README.md) | Long horizons, discounting and why the framework has no time preference | 1 week | Discussion 8.1; P107 |
| [P112](P112-climate-stress-testing-methodology-and-what-transfers-to/README.md) | Climate stress-testing methodology and what transfers to a structural model | 1.5 weeks | Discussion 8.1; `ShockSimulator.stress_test` |

## Track T - The Promised Research Modules

*Write the eleven modules the discussion index links to and that do not exist.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P113](P113-q1-the-quantum-superposition-module-written-or-retired/README.md) | Q1 - the quantum-superposition module, written or retired | 2 weeks | `docs/discussions/README.md` module Q1; P75's write-or-retire ruling |
| [P114](P114-q2-markov-transitions-cptp-maps-and-what-the-framework-a/README.md) | Q2 - Markov transitions, CPTP maps and what the framework already is | 2 weeks | `docs/discussions/README.md` module Q2 |
| [P115](P115-q3-shannon-entropy-and-the-diagnostic-index-that-is-alre/README.md) | Q3 - Shannon entropy and the diagnostic index that is already an HHI | 1.5 weeks | `docs/discussions/README.md` module Q3 |
| [P116](P116-d1-deep-architectures-and-the-boundary-that-keeps-them-o/README.md) | D1 - deep architectures, and the boundary that keeps them out of the package | 2 weeks | `docs/discussions/README.md` module D1 |
| [P117](P117-d2-embedding-spaces-regimes-and-the-two-dimensional-pict/README.md) | D2 - embedding spaces, regimes, and the two-dimensional picture that lies | 2 weeks | `docs/discussions/README.md` module D2 |
| [P118](P118-d3-knowledge-graphs-causal-pathways-and-the-graph-the-fr/README.md) | D3 - knowledge graphs, causal pathways, and the graph the framework already has | 2.5 weeks | `docs/discussions/README.md` module D3 |
| [P119](P119-h1-variational-circuits-and-the-trainability-result-that/README.md) | H1 - variational circuits, and the trainability result that decides the module | 2 weeks | `docs/discussions/README.md` module H1 |
| [P120](P120-h2-persistent-homology-and-the-one-stability-theorem-tha/README.md) | H2 - persistent homology, and the one stability theorem that makes it usable | 2 weeks | `docs/discussions/README.md` module H2 |
| [P121](P121-h3-symplectic-structure-and-the-conservation-the-framewo/README.md) | H3 - symplectic structure, and the conservation the framework does not have | 2 weeks | `docs/discussions/README.md` module H3 |
| [P122](P122-i1-combination-calibration-and-what-an-index-without-a-t/README.md) | I1 - combination, calibration, and what an index without a target can be scored against | 2.5 weeks | `docs/discussions/README.md` module I1 |
| [P123](P123-i2-the-gating-validation-module-written-as-structural-re/README.md) | I2 - the gating validation module, written as structural retrodiction | 3 weeks | `docs/discussions/README.md` module I2; the governance annotations in its section 3.1 |

## Track U - Method, Epistemics and External Validation

*State what would falsify the framework, and submit it to something other than its authors.*

| ID | Project | Effort | Upstream |
|----|---------|--------|----------|
| [P124](P124-what-would-falsify-the-framework/README.md) | What would falsify the framework | 2 weeks | `CLAUDE.md` -> Illustrative, not validated |
| [P125](P125-model-risk-management-alignment-for-an-unvalidated-instr/README.md) | Model risk management alignment for an unvalidated instrument | 1.5 weeks | SR 11-7 / OCC 2011-12; `CLAUDE.md` |
| [P126](P126-a-route-to-external-review-that-the-licence-currently-fo/README.md) | A route to external review that the licence currently forecloses | 2 weeks | `LICENSE.txt`; `RELEASING.md`; P125 |
| [P127](P127-the-anatomical-analogy-where-it-does-work-and-where-it-s/README.md) | The anatomical analogy: where it does work and where it smuggles conclusions | 1.5 weeks | The framework's central metaphor; `SystemKind` |
| [P128](P128-scale-and-resolution-limits-of-the-seven-system-model/README.md) | Scale and resolution limits of the seven-system model | 1.5 weeks | P56; P91; P104; P106; P107; P109 |
| [P129](P129-benchmarking-the-framework-against-an-established-struct/README.md) | Benchmarking the framework against an established structural measure | 2 weeks | P23; P80; P125 |

---

## Status convention

Every charter starts at `proposed`. A charter moves to `active` when an owner is assigned and the first
agent has been dispatched, and to `done` only when every line of its acceptance criteria is objectively
true. A charter whose dispute is resolved without doing the work is closed as `superseded`, with the
resolution recorded in the charter itself - never deleted, because the argument is the record.

## Adding a charter

1. State the dispute first. If you cannot write two paragraphs describing a real disagreement, the work
   belongs in an issue, not here.
2. Assign it to the track that owns the module or the domain it touches.
3. Reuse the existing agents and skills. A new agent needs a mandate no existing agent covers; a new
   skill needs a procedure that is genuinely repeatable.
4. Every source in the required reading must pass
   [`amf-source-vetting`](../.claude/skills/amf-source-vetting/SKILL.md) and be added to
   [REFERENCES.md](REFERENCES.md).
5. Acceptance criteria must be checkable by someone who did not do the work.
