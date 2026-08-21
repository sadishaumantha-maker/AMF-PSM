# Agent protocol

Every charter in this section is executed by a small set of autonomous agents. This page states the
rules that hold for all of them; the per-project mandate lives in the charter.

## The five rules

1. **One mandate, one artifact.** An agent produces the artifact its charter names and nothing else. It
   may not decide it has found a better problem to solve.
2. **Stop conditions are hard.** An agent stops when its stop condition is met and hands off. Running
   past a stop condition is how a research agent turns into an unreviewed rewrite.
3. **Evidence before decision, decision before implementation.** `literature-scout` and
   `benchmark-runner` supply evidence; `spec-drafter` and `math-formalizer` decide;
   `algorithm-implementer` implements. An implementer that starts before a decision is ratified is
   working from an assumption.
4. **Adversarial review is mandatory.** No charter is done until `red-team-critic` has attacked it and
   every finding is closed or accepted in writing.
5. **Hard rules bind every agent.** No trading vocabulary, no predictive claim, no modification of a
   checksum-protected artifact, no runtime dependency, and no output that is not reproducible.
6. **Two agents are catalogue-wide.** `citation-verifier` runs against every charter's reading list
   before merge, whether or not the charter names it, and a flagged citation blocks the merge.
   `literature-scout` writes its findings in the format the `amf-literature-brief` skill defines.

## Hand-off

Each charter lists its hand-off order. The typical shape is:

```text
literature-scout  ->  spec-drafter / math-formalizer  ->  algorithm-implementer
                                                            |
                              property-test-author / unit-test-author
                                                            |
                                    determinism-prover / boundary-sentinel
                                                            |
                                                   red-team-critic
```

Governance and research charters replace the implementation stages with
`regime-comparativist`, `case-study-archivist` or `taxonomy-cartographer`, but the shape holds:
evidence, decision, artifact, adversarial review.

## The roster

| Agent | Role | Used by |
|-------|------|---------|
| [`algorithm-implementer`](../.claude/agents/algorithm-implementer.md) | Writes the change under `src/amf/` once a specification has been ratified | P12, P14, P16, P18, P19, P20 +17 |
| [`api-surface-reviewer`](../.claude/agents/api-surface-reviewer.md) | Reviews the public API: exports, `__all__` ordering, module layering and docstring accuracy | P03, P12, P25, P59, P64, P67 |
| [`benchmark-runner`](../.claude/agents/benchmark-runner.md) | Runs reproducible measurements, sweeps and profiles, and reports them with exact reproduction commands | P04, P05, P14, P18, P19, P20 +16 |
| [`boundary-sentinel`](../.claude/agents/boundary-sentinel.md) | Enforces the non-trading naming boundary | P11, P43, P44, P46, P47, P49 +7 |
| [`case-study-archivist`](../.claude/agents/case-study-archivist.md) | Assembles dated, sourced structural case files under the case study protocol | P41, P42, P43, P53, P54, P55 +1 |
| [`citation-verifier`](../.claude/agents/citation-verifier.md) | Verifies that every citation in a document resolves to a real work of the standing claimed | *every charter (merge gate)* |
| [`coverage-gatekeeper`](../.claude/agents/coverage-gatekeeper.md) | Guards the 100% statement and branch coverage gate and diagnoses uncovered branches | P10, P11 |
| [`determinism-prover`](../.claude/agents/determinism-prover.md) | Proves that equal inputs produce byte-identical output, under permutation, repetition and across the supported Python versions | P12, P14, P15, P18, P30, P65 |
| [`docs-synthesizer`](../.claude/agents/docs-synthesizer.md) | Writes and edits documentation pages under `docs/` | P05, P07, P10, P29, P32, P38 +6 |
| [`integrity-warden`](../.claude/agents/integrity-warden.md) | Protects the checksum-protected artifacts, the licence position and the private-distribution rule | P02, P07, P08, P52, P68, P69 +3 |
| [`literature-scout`](../.claude/agents/literature-scout.md) | Finds and ranks primary academic sources for an AMF-PSM project charter | P01, P23, P26, P27, P28, P31 +27 |
| [`math-formalizer`](../.claude/agents/math-formalizer.md) | States definitions, derives conditions and writes the invariants a claim implies | P17, P19, P20, P21, P22, P24 +13 |
| [`mutation-hunter`](../.claude/agents/mutation-hunter.md) | Runs mutation testing and triages surviving mutants | P11 |
| [`numerics-auditor`](../.claude/agents/numerics-auditor.md) | Audits floating-point behaviour: accumulation error, overflow, NaN paths and estimator stability | P14, P18, P22, P33 |
| [`property-test-author`](../.claude/agents/property-test-author.md) | Writes hypothesis property tests for claimed invariants | P15, P17, P20, P24 |
| [`red-team-critic`](../.claude/agents/red-team-critic.md) | Adversarially attempts to falsify a project's conclusion, break its rules or misread its output | P01, P02, P05, P06, P07, P08 +39 |
| [`regime-comparativist`](../.claude/agents/regime-comparativist.md) | Produces per-jurisdiction regulatory regime profiles from primary instruments | P40, P41, P42, P44, P45, P50 +1 |
| [`release-marshal`](../.claude/agents/release-marshal.md) | Manages version discipline: version-string agreement, changelog entries and release gating | P04, P08, P28, P71 |
| [`spec-drafter`](../.claude/agents/spec-drafter.md) | Turns verified findings into a written specification or decision record | P01, P02, P03, P04, P06, P09 +26 |
| [`taxonomy-cartographer`](../.claude/agents/taxonomy-cartographer.md) | Builds classification tables, registers and mappings from published standards | P01, P47, P48, P51, P52, P55 +1 |
| [`unit-test-author`](../.claude/agents/unit-test-author.md) | Writes deterministic unit tests, boundary cases and known-answer tests | P11, P16, P17, P19, P22, P25 +4 |
| [`viz-designer`](../.claude/agents/viz-designer.md) | Produces deterministic figures under the visual grammar, with the mandatory footnote intact | P35, P65 |

## Escalation

An agent escalates to a human, rather than deciding, when: a checksum-protected artifact would have to
change; a new entry would have to be added to the non-trading allowlist; a coverage or lint gate would
have to be weakened; a published number would move without a measurement to justify it; or a real person
or organisation would have to be characterised.
