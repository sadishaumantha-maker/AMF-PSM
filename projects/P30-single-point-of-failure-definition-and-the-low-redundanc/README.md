# P30 - Single point of failure: definition and the low-redundancy threshold

**Track E - Diagnostics, Sensitivity & Leverage**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 4 days |
| **Lead role** | Quantitative methodologist |
| **Upstream** | `_LOW_REDUNDANCY = 0.5`; SPOF ranking by criticality |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

A single point of failure is an articulation point with redundancy below `0.5`. The threshold `0.5` is the midpoint of the unit interval and appears to have been chosen for that reason. A structural claim with a policy-relevant name should not rest on a number chosen because it is halfway.

## 2. Purpose

Either derive the threshold from a stated criterion or replace the binary flag with a graded measure that does not require an arbitrary cut.

## 3. Scope

**In scope**

- An analysis of what redundancy value actually removes single-point behaviour, given the framework's own dynamics.
- A comparison of a hard threshold against a graded SPOF score.
- Sensitivity of the flagged set to the threshold across generated markets.

**Out of scope**

- Changing the articulation-point notion - that is P21.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Test empirically, using the framework's own simulation, at what redundancy a system stops dominating the stress trace when shocked.
2. Compare that empirical value against the current `0.5`.
3. Evaluate a graded alternative: report a SPOF score rather than a flag, and let severity banding do the discretising.
4. Measure how the flagged set changes across the threshold range on generated markets.
5. Choose, implement, and document the criterion so the number is derived rather than assumed.
6. Confirm the SPOF ranking still breaks ties by declaration order.

## 5. Task board

- [ ] Run the redundancy sweep against simulated peak stress.
- [ ] Compare the empirical value with the current threshold.
- [ ] Evaluate the graded alternative.
- [ ] Measure flagged-set sensitivity to the threshold.
- [ ] Implement the chosen definition.
- [ ] Publish `docs/diagnostics/spof_threshold.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `benchmark-runner`

- **Mandate:** Sweep redundancy against simulated peak stress and locate any behavioural knee.
- **Inputs:** Simulation and generated markets.
- **Output artifact:** A sweep table with reproduction commands.
- **Stop condition:** The sweep covers the full `[0, 1]` redundancy range at a stated resolution.

### `math-formalizer`

- **Mandate:** Derive or reject the threshold from the sweep and state the criterion.
- **Inputs:** Sweep results.
- **Output artifact:** `docs/diagnostics/spof_threshold.md`.
- **Stop condition:** The threshold is derived from a stated criterion or replaced by a graded score.

### `algorithm-implementer`

- **Mandate:** Implement the chosen definition preserving declaration-order tie-breaks.
- **Inputs:** The decision.
- **Output artifact:** A diff under `src/amf/diagnostics.py`.
- **Stop condition:** Permutation invariance of the SPOF ranking still holds.

### `determinism-prover`

- **Mandate:** Confirm equal markets still produce identical SPOF rankings.
- **Inputs:** The diff.
- **Output artifact:** A permutation property.
- **Stop condition:** No counterexample within the example budget.

**Hand-off order:** `benchmark-runner` -> `math-formalizer` -> `algorithm-implementer` -> `determinism-prover`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-sensitivity-design` | A threshold is under review | Designs the sweep and reports flagged-set sensitivity. |
| `amf-determinism-audit` | A ranking changes | Runs permutation invariance across the public API. |
| `amf-changelog-entry` | The flagged set changes | Records the change and the criterion that drove it. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/diagnostics/spof_threshold.md`
- A redundancy sweep table
- The implemented definition
- Permutation properties

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The threshold is derived from a stated criterion, or replaced by a graded score.
- [ ] Flagged-set sensitivity is measured across the threshold range.
- [ ] SPOF ranking ties still break by `SystemKind` declaration order.
- [ ] Any change to the flagged set is recorded in `CHANGELOG.md`.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Perrow, C. (1984). *Normal Accidents: Living with High-Risk Technologies*. Princeton University Press.
- Kitano, H. (2004). "Biological robustness." *Nature Reviews Genetics* 5, 826-837.
- Albert, R., Jeong, H., & Barabasi, A.-L. (2000). "Error and attack tolerance of complex networks." *Nature* 406, 378-382.
- Callaway, D. S., Newman, M. E. J., Strogatz, S. H., & Watts, D. J. (2000). "Network Robustness and Fragility: Percolation on Random Graphs." *Physical Review Letters* 85(25), 5468-5471.
- Holling, C. S. (1973). "Resilience and Stability of Ecological Systems." *Annual Review of Ecology and Systematics* 4, 1-23.
- Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., & Tarantola, S. (2008). *Global Sensitivity Analysis: The Primer*. Wiley.

## 11. Commit protocol

Commits from this project use the scope `p30`:

```text
test(p30): sweep redundancy against simulated peak stress
docs(p30): derive the single-point-of-failure criterion from the sweep
fix(p30): adopt the derived SPOF definition
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

