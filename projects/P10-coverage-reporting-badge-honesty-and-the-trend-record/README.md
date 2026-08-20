# P10 - Coverage reporting, badge honesty and the trend record

**Track B - Engineering Quality, CI & Reproducibility**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 days |
| **Lead role** | CI owner |
| **Upstream** | issues #117 (2.5), #150 (9.4), #152 (9.5) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The repository already enforces 100% statement and branch coverage, and `CLAUDE.md` states plainly that 100% coverage is not the same as 100% tested. Adding a coverage badge is therefore argued to be actively misleading - a permanent green 100% that says nothing about test quality.

## 2. Purpose

Publish coverage information that cannot be misread: the badge is accompanied by an explicit statement of what the number does and does not certify, and by the mutation score from P11 once it exists.

## 3. Scope

**In scope**

- A coverage trend record generated from CI artifacts.
- A badge plus a mandatory adjacent caveat sentence in `README.md`.
- A written statement of coverage's known blind spots in this repository.

**Out of scope**

- Lowering `--cov-fail-under` for any reason.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Collect `coverage.xml` from the 3.12 job and record statement and branch figures over time.
2. Write the blind-spot statement, citing the mutation-testing literature on coverage as a weak adequacy criterion.
3. Add the badge to `README.md` with an adjacent sentence naming what it does not prove.
4. Wire the trend record into the P05 metrics page rather than maintaining a second source of truth.

## 5. Task board

- [ ] Extract coverage figures from CI artifacts reproducibly.
- [ ] Write the coverage blind-spot statement.
- [ ] Add the badge and its caveat to `README.md`.
- [ ] Feed the trend into `docs/governance/metrics.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `coverage-gatekeeper`

- **Mandate:** Extract and record coverage figures and confirm the gate is still 100%.
- **Inputs:** `coverage.xml`, `pyproject.toml`.
- **Output artifact:** A coverage trend table.
- **Stop condition:** The gate reads `--cov-fail-under=100` and the trend has at least one recorded point.

### `docs-synthesizer`

- **Mandate:** Write the badge caveat so that a casual reader cannot over-read the number.
- **Inputs:** Blind-spot statement.
- **Output artifact:** A `README.md` diff.
- **Stop condition:** The caveat is adjacent to the badge, not in a footnote.

**Hand-off order:** `coverage-gatekeeper` -> `docs-synthesizer`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-coverage-gate` | Coverage configuration changes | Verifies the 100% branch gate and reports any uncovered branch. |
| `amf-doc-page` | Editing `README.md` | Enforces link-check safety and disclaimer placement. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- A coverage trend record
- A badge with an adjacent caveat
- A blind-spot statement

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The badge is never displayed without its caveat sentence.
- [ ] The gate remains at 100% statement and branch coverage.
- [ ] The trend record regenerates from CI artifacts with no manual editing.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Jia, Y., & Harman, M. (2011). "An Analysis and Survey of the Development of Mutation Testing." *IEEE Transactions on Software Engineering* 37(5), 649-678.
- Papadakis, M., Kintis, M., Zhang, J., Jia, Y., Le Traon, Y., & Harman, M. (2019). "Mutation Testing Advances: An Analysis and Survey." *Advances in Computers* 112, 275-378.
- Beck, K. (2002). *Test-Driven Development: By Example*. Addison-Wesley.
- Feathers, M. C. (2004). *Working Effectively with Legacy Code*. Prentice Hall.
- Wilson, G., Bryan, J., Cranston, K., Kitzes, J., Nederbragt, L., & Teal, T. K. (2017). "Good enough practices in scientific computing." *PLoS Computational Biology* 13(6), e1005510.

## 11. Commit protocol

Commits from this project use the scope `p10`:

```text
docs(p10): add coverage badge with an explicit adequacy caveat
ci(p10): record the coverage trend from CI artifacts
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

