# P97 - Monoculture: when redundancy stops providing substitutability

**Track Q - Technology, Fintech and AI Risk**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Complex systems analyst |
| **Upstream** | P27; P34; P96 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Redundancy is the framework's strongest resilience term - it dominates absorptive capacity and zeroes fragility at its maximum. Redundancy only helps if the redundant elements fail independently. Where they share a design, a supplier or a model, they fail together, and the framework's most heavily weighted resilience input becomes its most misleading one.

## 2. Purpose

Make common-mode failure representable, or make the independence assumption visible wherever redundancy is reported - because at present it is assumed silently.

## 3. Scope

**In scope**

- A statement of the independence assumption implicit in `redundancy`.
- A candidate representation of correlated redundancy.
- Measurement of how much resilience scores move when independence fails.

**Out of scope**

- Assessing any real supplier concentration.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the assumption explicitly: `redundancy` in `[0, 1]` carries no information about whether the redundant elements are alike, and every use of it assumes they are not.
2. Quantify the exposure. Compute resilience for a market at high redundancy, then recompute treating the redundant elements as perfectly correlated, and report the gap - that gap is the size of the hidden assumption.
3. Draw on the biological robustness literature, which treats degeneracy - different elements achieving the same function - as distinct from and stronger than redundancy. That distinction is exactly what the framework is missing.
4. Propose the minimal representation: a second metric distinguishing redundancy from degeneracy, or a documented assumption. Argue both, because adding a metric is a significant change to the model's shape.
5. If the assumption is retained, make it visible where redundancy is reported rather than in a document nobody reads at that moment.
6. Coordinate with P27 and P34, which own the formulas that consume redundancy.

## 5. Task board

- [ ] State the independence assumption formally.
- [ ] Measure the resilience gap under perfect correlation.
- [ ] Review redundancy versus degeneracy in the robustness literature.
- [ ] Propose and argue the minimal representation.
- [ ] Make the assumption visible at the point of use.
- [ ] Publish `docs/simulation/monoculture.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** State the independence assumption and express the correlated case.
- **Inputs:** `systems.py`, `diagnostics.py`.
- **Output artifact:** A formal statement.
- **Stop condition:** The assumption is expressed where redundancy enters each formula.

### `benchmark-runner`

- **Mandate:** Measure the resilience gap between independent and perfectly correlated redundancy.
- **Inputs:** The simulator and generated markets.
- **Output artifact:** A gap measurement table.
- **Stop condition:** The gap is reported across at least one hundred markets with uncertainty.

### `literature-scout`

- **Mandate:** Establish the redundancy-versus-degeneracy distinction from primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary.
- **Stop condition:** The distinction is sourced from the robustness literature.

### `docs-synthesizer`

- **Mandate:** Make the assumption visible wherever redundancy is reported.
- **Inputs:** The formal statement.
- **Output artifact:** A renderer and docstring change.
- **Stop condition:** Every rendered redundancy figure carries its assumption.

**Hand-off order:** `math-formalizer` -> `benchmark-runner` -> `literature-scout` -> `docs-synthesizer`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-sensitivity-design` | The gap is measured | Designs the comparison and reports rank stability. |
| `amf-invariant-spec` | The assumption is stated | Writes it into the docstring at the point of use. |
| `amf-doc-page` | The finding is published | Enforces documentation conventions. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/simulation/monoculture.md`
- A formal independence statement
- A measured resilience gap
- Visible assumptions at the point of use

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The independence assumption is stated where redundancy enters each formula.
- [ ] The correlated-case gap is measured across at least one hundred markets.
- [ ] The redundancy-degeneracy distinction is sourced from primary literature.
- [ ] Every rendered redundancy figure carries its assumption.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Kitano, H. (2004). "Biological robustness." *Nature Reviews Genetics* 5, 826-837.
- Csete, M. E., & Doyle, J. C. (2002). "Reverse Engineering of Biological Complexity." *Science* 295(5560), 1664-1669.
- Carlson, J. M., & Doyle, J. (2002). "Complexity and robustness." *PNAS* 99(suppl 1), 2538-2545.
- Alon, U. (2019). *An Introduction to Systems Biology: Design Principles of Biological Circuits* (2nd ed.). CRC Press.
- Wagner, W. (2011). "Systemic Liquidation Risk and the Diversity-Diversification Trade-Off." *Journal of Finance* 66(4), 1141-1175.
- Perrow, C. (1984). *Normal Accidents: Living with High-Risk Technologies*. Princeton University Press.
- Holling, C. S. (1973). "Resilience and Stability of Ecological Systems." *Annual Review of Ecology and Systematics* 4, 1-23.
- Danielsson, J., Shin, H. S., & Zigrand, J.-P. (2012). "Endogenous and Systemic Risk." In Haubrich, J. G. & Lo, A. W. (eds.), *Quantifying Systemic Risk*. University of Chicago Press.

## 11. Commit protocol

Commits from this project use the scope `p97`:

```text
docs(p97): state the independence assumption hidden inside redundancy
test(p97): measure the resilience gap under perfectly correlated redundancy
docs(p97): surface the independence assumption where redundancy is reported
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

