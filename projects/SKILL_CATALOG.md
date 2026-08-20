# Skill catalogue

Skills are the repeatable procedures the agents invoke. Each is defined once under
[`.claude/skills/`](../.claude/skills) and is referenced by the charters that need it.

A skill earns its place by being **repeatable and consequential**: it encodes a procedure that would
otherwise be re-derived, inconsistently, every time. A one-off instruction belongs in a charter, not
here.

| Skill | Purpose | Used by |
|-------|---------|---------|
| [`amf-boundary-check`](../.claude/skills/amf-boundary-check/SKILL.md) | Run the non-trading naming guard against a proposed name and supply a structural replacement on a hit | P11, P23, P25, P43, P44, P46 +10 |
| [`amf-cascade-calibration`](../.claude/skills/amf-cascade-calibration/SKILL.md) | Sweep the cascade parameter plane, locate the sensitive region and flag knife-edge configurations | P35, P36 |
| [`amf-case-dossier`](../.claude/skills/amf-case-dossier/SKILL.md) | Assemble a dated, sourced structural case file under the AMF case study protocol | P41, P42, P43, P53, P54, P55 +2 |
| [`amf-centrality-diagnostics`](../.claude/skills/amf-centrality-diagnostics/SKILL.md) | Estimate the graph's spectral radius and validate the Katz attenuation factor against the convergence condition | P22, P23, P33 |
| [`amf-changelog-entry`](../.claude/skills/amf-changelog-entry/SKILL.md) | Write a Keep-a-Changelog entry under Unreleased and keep the two version strings in sync | P04, P08, P14, P16, P18, P21 +3 |
| [`amf-config-validator`](../.claude/skills/amf-config-validator/SKILL.md) | Add or change a validated tuning parameter so it raises InvalidConfigError outside its domain, with both-sided boundary tests | P17, P20, P22, P28, P31, P35 |
| [`amf-coverage-gate`](../.claude/skills/amf-coverage-gate/SKILL.md) | Verify the 100% statement and branch coverage gate and diagnose uncovered branches with reaching inputs | P07, P10, P11 |
| [`amf-determinism-audit`](../.claude/skills/amf-determinism-audit/SKILL.md) | Run permutation, repetition and cross-version invariance checks over the AMF public API | P12, P14, P15, P18, P25, P30 +1 |
| [`amf-doc-page`](../.claude/skills/amf-doc-page/SKILL.md) | Write or edit a page under docs/ following AMF documentation conventions, link-check safety and the disclaimer rules | P01, P02, P03, P04, P05, P06 +18 |
| [`amf-ensemble-stats`](../.claude/skills/amf-ensemble-stats/SKILL.md) | Compute percentiles and seeded bootstrap intervals with the documented estimator, standard library only | P18, P19, P26, P29, P31, P39 +1 |
| [`amf-figure-render`](../.claude/skills/amf-figure-render/SKILL.md) | Render a deterministic figure under the AMF visual grammar with the mandatory footnote intact | P35, P65, P69 |
| [`amf-float-audit`](../.claude/skills/amf-float-audit/SKILL.md) | Locate floating-point accumulations, bound their error and compare against an extended-precision reference | P14, P16, P22 |
| [`amf-graph-algorithm`](../.claude/skills/amf-graph-algorithm/SKILL.md) | Verify a graph query against its source algorithm, state its complexity, and check it on exhaustively enumerated small graphs | P20, P21, P24, P26, P58 |
| [`amf-integrity-verify`](../.claude/skills/amf-integrity-verify/SKILL.md) | Verify the checksum-protected artifacts and the private-distribution controls | P02, P07, P08, P09, P52, P68 +4 |
| [`amf-invariant-spec`](../.claude/skills/amf-invariant-spec/SKILL.md) | Write a claimed invariant into the docstring and mirror it as a test that fails when the invariant is removed | P16, P17, P19, P25, P27, P32 +7 |
| [`amf-layering-check`](../.claude/skills/amf-layering-check/SKILL.md) | Verify the one-way module dependency order in src/amf holds in the actual imports | P03, P59, P67 |
| [`amf-literature-brief`](../.claude/skills/amf-literature-brief/SKILL.md) | Produce a structured evidence brief from a set of vetted sources, with disagreements and gaps foregrounded | *every research charter* |
| [`amf-mutation-sweep`](../.claude/skills/amf-mutation-sweep/SKILL.md) | Run the pinned mutation-testing configuration over src/amf and triage every surviving mutant | P11 |
| [`amf-property-harness`](../.claude/skills/amf-property-harness/SKILL.md) | Scaffold a hypothesis property test for a universally quantified claim, using the importable build_market() helper | P12, P15, P17, P20, P24, P27 +1 |
| [`amf-red-team`](../.claude/skills/amf-red-team/SKILL.md) | Adversarially attack a finding, rule or rendered output before it is merged | P01, P02, P05, P06, P07, P08 +39 |
| [`amf-regime-profile`](../.claude/skills/amf-regime-profile/SKILL.md) | Produce a dated, multi-dimensional regulatory regime profile for a jurisdiction from primary instruments | P40, P41, P44, P45, P50, P57 |
| [`amf-schema-roundtrip`](../.claude/skills/amf-schema-roundtrip/SKILL.md) | Prove that a new or changed serialised field keeps Market.to_dict / from_dict a lossless fixed point | P12, P19, P24, P33, P37 |
| [`amf-sensitivity-design`](../.claude/skills/amf-sensitivity-design/SKILL.md) | Design a perturbation experiment - one-at-a-time, elementary effects or variance-based - and report rank stability | P29, P30, P31, P34, P39 |
| [`amf-source-vetting`](../.claude/skills/amf-source-vetting/SKILL.md) | Vet a proposed source for primary status and scholarly or official standing before it is cited in AMF-PSM | P01, P34, P40, P41, P42, P45 +8 |
| [`amf-taxonomy-builder`](../.claude/skills/amf-taxonomy-builder/SKILL.md) | Build a citable classification register from official standards, with an inclusion rule and a maintained exclusion list | P47, P48, P49, P50, P51, P52 +1 |

## Grouping

- **Evidence** - `amf-source-vetting`, `amf-literature-brief`
- **Correctness** - `amf-determinism-audit`, `amf-float-audit`, `amf-invariant-spec`,
  `amf-property-harness`, `amf-mutation-sweep`, `amf-coverage-gate`
- **Architecture** - `amf-boundary-check`, `amf-layering-check`, `amf-config-validator`,
  `amf-schema-roundtrip`
- **Analysis** - `amf-graph-algorithm`, `amf-centrality-diagnostics`, `amf-cascade-calibration`,
  `amf-ensemble-stats`, `amf-sensitivity-design`
- **Domain** - `amf-taxonomy-builder`, `amf-regime-profile`, `amf-case-dossier`
- **Communication** - `amf-figure-render`, `amf-doc-page`, `amf-changelog-entry`
- **Protection** - `amf-integrity-verify`, `amf-red-team`
