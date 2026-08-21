# P11 - Mutation testing programme to expose coverage blind spots

**Track B - Engineering Quality, CI & Reproducibility**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Test engineer |
| **Upstream** | `CLAUDE.md` ("100% coverage is not the same as 100% tested"), issue #150 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The repository already admits that full coverage hid real gaps, and that some tests exist *because* of mutation-driven discovery. What is disputed is whether mutation testing becomes a standing CI gate - expensive and noisy - or a periodic audit.

## 2. Purpose

Establish a mutation-testing programme with a measured baseline mutation score, a triage protocol for surviving mutants, and an evidence-based decision on gating.

## 3. Scope

**In scope**

- A mutation run over `src/amf/` with a recorded configuration and seed.
- Triage of every surviving mutant into killed-by-new-test, equivalent, or accepted-with-reason.
- A gating recommendation supported by measured runtime and signal-to-noise.

**Out of scope**

- Weakening any existing test to raise the score.
- Adding tests that assert implementation details rather than behaviour.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Choose a mutation tool and record the exact version and configuration; determinism is required.
2. Run a full baseline over `src/amf/` and store the mutant inventory.
3. Triage every survivor. An equivalent mutant must be *argued*, not assumed.
4. Write a killing test for every non-equivalent survivor, respecting the non-trading naming guard.
5. Measure runtime; recommend gating only if the wall-clock cost is defensible against the DORA lead-time evidence.
6. Publish the protocol so future contributors triage survivors the same way.

## 5. Task board

- [ ] Select and pin the mutation tool.
- [ ] Produce the baseline mutation score per module.
- [ ] Triage all survivors with written rulings.
- [ ] Add killing tests for non-equivalent survivors.
- [ ] Measure and record runtime cost.
- [ ] Publish `docs/testing/mutation_protocol.md` with the gating recommendation.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `mutation-hunter`

- **Mandate:** Run the baseline, inventory survivors and classify each one.
- **Inputs:** `src/amf/`, existing test suite.
- **Output artifact:** A survivor inventory with per-mutant rulings.
- **Stop condition:** Every survivor is killed, argued equivalent, or accepted with a written reason.

### `unit-test-author`

- **Mandate:** Write the minimal behavioural test that kills each non-equivalent survivor.
- **Inputs:** Survivor inventory.
- **Output artifact:** New cases in `tests/unit/test_<module>.py`.
- **Stop condition:** Each new test fails on the mutant and passes on `main`.

### `boundary-sentinel`

- **Mandate:** Ensure no new test or helper introduces forbidden market-data vocabulary.
- **Inputs:** The new test files.
- **Output artifact:** A boundary report.
- **Stop condition:** `tests/unit/test_non_trading_boundary.py` passes and no new allowlist entry was added.

### `coverage-gatekeeper`

- **Mandate:** Confirm the 100% branch gate still holds after the new tests.
- **Inputs:** Test suite.
- **Output artifact:** A coverage confirmation.
- **Stop condition:** `pytest` passes with `--cov-fail-under=100`.

**Hand-off order:** `mutation-hunter` -> `unit-test-author` -> `boundary-sentinel` -> `coverage-gatekeeper`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-mutation-sweep` | Auditing test adequacy | Runs the pinned mutation configuration and produces a triaged survivor list. |
| `amf-boundary-check` | New public or test names are introduced | Runs the non-trading naming guard and checks the allowlist is unchanged. |
| `amf-coverage-gate` | Tests are added or changed | Confirms the 100% statement and branch gate. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- A baseline mutation score per module
- A triaged survivor inventory
- New killing tests
- `docs/testing/mutation_protocol.md`

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every surviving mutant has a written disposition.
- [ ] The suite still passes the 100% coverage gate.
- [ ] The non-trading boundary test passes with no new allowlist entries.
- [ ] The gating recommendation cites measured runtime, not intuition.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Jia, Y., & Harman, M. (2011). "An Analysis and Survey of the Development of Mutation Testing." *IEEE Transactions on Software Engineering* 37(5), 649-678.
- Papadakis, M., Kintis, M., Zhang, J., Jia, Y., Le Traon, Y., & Harman, M. (2019). "Mutation Testing Advances: An Analysis and Survey." *Advances in Computers* 112, 275-378.
- Claessen, K., & Hughes, J. (2000). "QuickCheck: a lightweight tool for random testing of Haskell programs." *ICFP '00*, 268-279.
- Beck, K. (2002). *Test-Driven Development: By Example*. Addison-Wesley.
- Feathers, M. C. (2004). *Working Effectively with Legacy Code*. Prentice Hall.
- Meyer, B. (1988). *Object-Oriented Software Construction*. Prentice Hall. (design by contract)
- Hoare, C. A. R. (1969). "An Axiomatic Basis for Computer Programming." *Communications of the ACM* 12(10), 576-580.

## 11. Commit protocol

Commits from this project use the scope `p11`:

```text
test(p11): record baseline mutation score and survivor inventory
test(p11): add killing tests for non-equivalent survivors
docs(p11): publish the mutation triage protocol and gating recommendation
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

