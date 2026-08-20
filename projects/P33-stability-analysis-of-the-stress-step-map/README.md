# P33 - Stability analysis of the stress step map

**Track F - Shock Propagation, Cascades & Resilience**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Dynamical systems analyst |
| **Upstream** | `ShockSimulator.propagate`; `CLAUDE.md` -> Simulation |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The documentation concedes that the step map is not a contraction for every market: with enough incoming weight and little absorptive capacity the per-step gain exceeds one and stress grows until it saturates at the clip. `converged` therefore reports whether the trajectory settled within the step budget, not whether it is stable. Users are told this in prose; the code does not distinguish the two cases.

## 2. Purpose

Derive the exact stability condition for the linear regime, compute it per market, and report stability as a first-class property rather than as a caveat in the documentation.

## 3. Scope

**In scope**

- A derivation of the spectral condition for the linear step map including damping, retention, transmission and absorptive capacity.
- A computed per-market stability indicator exposed through the public API.
- A clear distinction in the output between `settled`, `saturated` and `budget exhausted`.

**Out of scope**

- Changing the dynamics themselves.
- Claiming that a stable market is a safe market.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Write the step map in matrix form and identify the effective iteration matrix.
2. Derive the condition for the spectral radius of that matrix to be below one, in terms of the configuration parameters and absorptive capacities.
3. Compute the indicator with the P22 power-iteration estimator, reusing rather than duplicating it.
4. Classify each trajectory outcome as settled, saturated at the clip, or budget exhausted, and expose the classification.
5. Confirm the existing settling-time convention of `-1` for budget exhaustion still holds, and document that saturation is a different outcome.
6. Add regression tests for a market that is provably unstable and one that is provably stable.

## 5. Task board

- [ ] Derive the iteration matrix and the stability condition.
- [ ] Implement the per-market stability indicator.
- [ ] Classify trajectory outcomes into three cases.
- [ ] Expose the classification in `SimulationTrace` or `ResilienceScore`.
- [ ] Add provably stable and unstable regression markets.
- [ ] Publish `docs/simulation/stability.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** Derive the iteration matrix and the exact spectral stability condition.
- **Inputs:** `simulation.py`, `graph.py`.
- **Output artifact:** `docs/simulation/stability.md`.
- **Stop condition:** The condition is stated in terms of the configuration parameters and is checkable numerically.

### `algorithm-implementer`

- **Mandate:** Implement the indicator and the three-way outcome classification.
- **Inputs:** The derived condition.
- **Output artifact:** A diff under `src/amf/simulation.py` and `models.py`.
- **Stop condition:** `to_dict()` round-trips the new field and `mypy` strict passes.

### `numerics-auditor`

- **Mandate:** Bound the estimator error and ensure the indicator is conservative near the boundary.
- **Inputs:** The implementation.
- **Output artifact:** An error analysis.
- **Stop condition:** Borderline markets are classified pessimistically, not optimistically.

### `unit-test-author`

- **Mandate:** Add provably stable and provably unstable regression markets.
- **Inputs:** The derivation.
- **Output artifact:** Cases in `tests/unit/test_simulation.py`.
- **Stop condition:** Both cases are classified correctly and the classification is asserted.

**Hand-off order:** `math-formalizer` -> `algorithm-implementer` -> `numerics-auditor` -> `unit-test-author`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-invariant-spec` | A stability guarantee is stated | Writes it into the docstring and mirrors it as a test. |
| `amf-centrality-diagnostics` | A spectral radius is needed | Reuses the validated power-iteration estimator rather than duplicating it. |
| `amf-schema-roundtrip` | A field is added to a result type | Proves `to_dict`/`from_dict` remains a fixed point. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/simulation/stability.md`
- A per-market stability indicator
- A three-way trajectory outcome classification
- Stable and unstable regression markets

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The stability condition is derived, not asserted.
- [ ] Saturation and budget exhaustion are distinguishable in the output.
- [ ] Borderline markets are classified conservatively.
- [ ] The `-1` settling-time convention is preserved and documented.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Horn, R. A., & Johnson, C. R. (2012). *Matrix Analysis* (2nd ed.). Cambridge University Press.
- Berman, A., & Plemmons, R. J. (1994). *Nonnegative Matrices in the Mathematical Sciences*. SIAM (Classics in Applied Mathematics 9).
- Strogatz, S. H. (2015). *Nonlinear Dynamics and Chaos* (2nd ed.). Westview Press.
- Khalil, H. K. (2002). *Nonlinear Systems* (3rd ed.). Prentice Hall.
- May, R. M. (1972). "Will a Large Complex System be Stable?" *Nature* 238, 413-414.
- Gai, P., & Kapadia, S. (2010). "Contagion in financial networks." *Proceedings of the Royal Society A* 466(2120), 2401-2423.
- Acemoglu, D., Ozdaglar, A., & Tahbaz-Salehi, A. (2015). "Systemic Risk and Stability in Financial Networks." *American Economic Review* 105(2), 564-608.

## 11. Commit protocol

Commits from this project use the scope `p33`:

```text
docs(p33): derive the spectral stability condition for the stress step map
feat(p33): report per-market stability and distinguish saturation from budget exhaustion
test(p33): add provably stable and unstable regression markets
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

