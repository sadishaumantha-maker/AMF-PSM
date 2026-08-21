# P112 - Climate stress-testing methodology and what transfers to a structural model

**Track S - Climate, Nature and Long-Horizon Risk**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Quantitative methodologist |
| **Upstream** | Discussion 8.1; `ShockSimulator.stress_test` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Supervisory climate stress testing is a mature published methodology, and the framework has a function called `stress_test`. The names coincide and the methods do not: supervisory exercises are scenario-driven, balance-sheet-based and calibrated, while the framework's shocks every system in turn with a dimensionless magnitude. The shared name invites a comparison the framework would lose.

## 2. Purpose

Compare the two explicitly, establish what if anything transfers, and ensure the framework's `stress_test` is never mistaken for a supervisory exercise.

## 3. Scope

**In scope**

- A structured comparison of the two methodologies.
- Identification of any transferable element.
- A naming and documentation decision about the shared term.

**Out of scope**

- Running any scenario-based exercise.
- Balance-sheet, exposure or scenario data.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Compare on the axes that matter: what is shocked, how the magnitude is chosen, what the output means, and what validates it. The framework loses on the last two and should say so.
2. Identify what transfers. The sweep-every-system design is genuinely similar to a sensitivity-style supervisory exercise, and the reverse-stress-testing idea - asking what would have to be true to break the system - transfers cleanly and is not currently implemented.
3. Take reverse stress testing seriously as the transferable element: it asks for the minimal structural change that produces failure, which is well posed in a dimensionless model.
4. Decide the naming question. If `stress_test` will be read as the supervisory term, the docstring must disclaim it explicitly at minimum.
5. State plainly what the framework's exercise does not do: it is uncalibrated, and its magnitudes are conventional rather than derived.
6. Coordinate with P39 and P31 on the sensitivity relationship.

## 5. Task board

- [ ] Compare the methodologies on four axes.
- [ ] Identify transferable elements.
- [ ] Specify reverse stress testing for the structural model.
- [ ] Decide the naming and disclaimer question.
- [ ] State the uncalibrated nature plainly.
- [ ] Publish `docs/simulation/stress_testing_comparison.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish supervisory climate stress-testing methodology from official-sector publications.
- **Inputs:** The reading list.
- **Output artifact:** A methodology summary.
- **Stop condition:** The summary states what validates a supervisory exercise.

### `math-formalizer`

- **Mandate:** Specify reverse stress testing for a dimensionless structural model.
- **Inputs:** The simulator.
- **Output artifact:** A formal specification.
- **Stop condition:** The minimal-change question is well posed and computable.

### `spec-drafter`

- **Mandate:** Decide the naming question and state the uncalibrated nature.
- **Inputs:** The comparison.
- **Output artifact:** `docs/simulation/stress_testing_comparison.md`.
- **Stop condition:** The docstring disclaimer is drafted, not merely recommended.

### `red-team-critic`

- **Mandate:** Attempt to present framework output as a stress-test result in the supervisory sense.
- **Inputs:** Rendered output.
- **Output artifact:** A misrepresentation report.
- **Stop condition:** The disclaimer prevents the reading.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-cascade-calibration` | Reverse stress testing is specified | Sweeps the parameter space to locate minimal failure-producing changes. |
| `amf-sensitivity-design` | The exercises are compared | Frames the sweep-every-system design against sensitivity practice. |
| `amf-red-team` | The shared name is retained | Tests whether output can be passed off as a supervisory result. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/simulation/stress_testing_comparison.md`
- A four-axis comparison
- A reverse-stress-testing specification
- A naming decision with a drafted disclaimer

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The comparison states what validates a supervisory exercise and that the framework has no equivalent.
- [ ] Reverse stress testing is specified as well posed and computable.
- [ ] The docstring disclaimer is drafted.
- [ ] No scenario or balance-sheet quantity appears.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Network for Greening the Financial System (2020). *NGFS Climate Scenarios for Central Banks and Supervisors*.
- Battiston, S., Mandel, A., Monasterolo, I., Schutze, F., & Visentin, G. (2017). "A climate stress-test of the financial system." *Nature Climate Change* 7, 283-288.
- Bolton, P., Despres, M., Pereira da Silva, L. A., Samama, F., & Svartzman, R. (2020). *The Green Swan: Central Banking and Financial Stability in the Age of Climate Change*. Bank for International Settlements.
- Board of Governors of the Federal Reserve System & OCC (2011). *Supervisory Guidance on Model Risk Management* (SR 11-7 / OCC Bulletin 2011-12).
- Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., & Tarantola, S. (2008). *Global Sensitivity Analysis: The Primer*. Wiley.
- Morgan, M. G., & Henrion, M. (1990). *Uncertainty: A Guide to Dealing with Uncertainty in Quantitative Risk and Policy Analysis*. Cambridge University Press.
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.
- Task Force on Climate-related Financial Disclosures (2017). *Recommendations of the Task Force on Climate-related Financial Disclosures*. Financial Stability Board.

## 11. Commit protocol

Commits from this project use the scope `p112`:

```text
docs(p112): compare supervisory and structural stress testing on four axes
docs(p112): specify reverse stress testing for a dimensionless model
docs(p112): disclaim the supervisory reading of stress_test
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
