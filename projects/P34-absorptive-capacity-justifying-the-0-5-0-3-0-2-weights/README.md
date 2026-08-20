# P34 - Absorptive capacity: justifying the 0.5 / 0.3 / 0.2 weights

**Track F - Shock Propagation, Cascades & Resilience**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Quantitative methodologist |
| **Upstream** | `AnatomicalSystem.absorptive_capacity()` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Absorptive capacity is `0.5 x redundancy + 0.3 x integrity + 0.2 x (1 - load)`. The weights sum to one, which keeps the result in the unit interval, and that is the only justification recorded. The ordering asserts that redundancy matters most and spare load capacity least, which is a substantive claim about how systems absorb stress, made without evidence.

## 2. Purpose

Either support the weight ordering with evidence from the absorptive-capacity and robustness literature, or replace it with an equal weighting and report the sensitivity of every downstream result to the choice.

## 3. Scope

**In scope**

- An evidence review on redundancy, integrity and spare capacity as absorption mechanisms.
- A sensitivity analysis of resilience scores to the absorptive-capacity weights.
- A decision, with equal weighting treated as the default null.

**Out of scope**

- Changing the resilience composite weights - that is P39.
- Any weighting fitted to market outcomes.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Separate the three mechanisms conceptually: redundancy provides substitutes, integrity provides margin, spare load capacity provides headroom.
2. Review the robustness literature on whether redundancy dominates, noting the common-mode failure caveat from P27.
3. Reuse the P31 sensitivity machinery to measure how resilience scores move across the weight simplex.
4. Report the rank stability of stress-test orderings under weight perturbation.
5. Adopt equal weighting unless the evidence supports an ordering; an unsupported ordering is a hidden assumption.
6. Record the change and its effect on every published resilience figure.

## 5. Task board

- [ ] Write the mechanism separation note.
- [ ] Review the absorption evidence.
- [ ] Measure resilience sensitivity across the weight simplex.
- [ ] Report stress-test rank stability.
- [ ] Decide and implement.
- [ ] Publish `docs/simulation/absorptive_capacity.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Find primary evidence on the relative contribution of redundancy, margin and headroom to absorption.
- **Inputs:** The reading list.
- **Output artifact:** An annotated evidence table.
- **Stop condition:** Each mechanism has at least one primary source or is marked unevidenced.

### `benchmark-runner`

- **Mandate:** Measure resilience and stress-test rank sensitivity across the weight simplex.
- **Inputs:** The simulator and generated markets.
- **Output artifact:** A sensitivity table with seeds and commands.
- **Stop condition:** Rank stability is reported for the stress-test ordering.

### `algorithm-implementer`

- **Mandate:** Implement the decision preserving unit-interval containment.
- **Inputs:** The decision.
- **Output artifact:** A diff under `src/amf/systems.py`.
- **Stop condition:** Absorptive capacity remains in `[0, 1]` for every admissible input.

### `red-team-critic`

- **Mandate:** Argue that the weights are unidentifiable from any available evidence and should therefore be equal.
- **Inputs:** The evidence table.
- **Output artifact:** A dissent section.
- **Stop condition:** The dissent is adopted or answered with cited evidence.

**Hand-off order:** `literature-scout` -> `benchmark-runner` -> `algorithm-implementer` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-sensitivity-design` | Weight sensitivity is measured | Designs the simplex sampling and reports rank stability. |
| `amf-source-vetting` | Evidence is proposed for a weight | Checks the source is primary and applicable to structural absorption. |
| `amf-changelog-entry` | Resilience figures move | Records the change and the evidence that drove it. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/simulation/absorptive_capacity.md`
- An evidence table
- A weight sensitivity analysis
- The implemented decision

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every weight is supported by cited evidence or set equal.
- [ ] Resilience sensitivity to the weights is measured and published.
- [ ] Absorptive capacity remains inside `[0, 1]`.
- [ ] Any moved figure is recorded in `CHANGELOG.md`.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Kitano, H. (2004). "Biological robustness." *Nature Reviews Genetics* 5, 826-837.
- Csete, M. E., & Doyle, J. C. (2002). "Reverse Engineering of Biological Complexity." *Science* 295(5560), 1664-1669.
- Holling, C. S. (1973). "Resilience and Stability of Ecological Systems." *Annual Review of Ecology and Systematics* 4, 1-23.
- Perrow, C. (1984). *Normal Accidents: Living with High-Risk Technologies*. Princeton University Press.
- OECD & European Commission JRC (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD Publishing.
- Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., & Tarantola, S. (2008). *Global Sensitivity Analysis: The Primer*. Wiley.
- Alon, U. (2019). *An Introduction to Systems Biology: Design Principles of Biological Circuits* (2nd ed.). CRC Press.

## 11. Commit protocol

Commits from this project use the scope `p34`:

```text
docs(p34): review the evidence for absorptive-capacity weighting
test(p34): measure resilience sensitivity across the absorption weight simplex
fix(p34): adopt the evidence-supported absorptive-capacity weights
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

