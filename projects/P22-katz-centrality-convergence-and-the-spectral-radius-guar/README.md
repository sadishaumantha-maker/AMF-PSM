# P22 - Katz centrality convergence and the spectral radius guard

**Track D - Graph & Network Theory of Market Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Numerical analyst |
| **Upstream** | `DependencyGraph.centrality`; `CLAUDE.md` -> Centrality |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

> [!IMPORTANT]
> **Status against `main`.** **Substantially superseded on `main`.** `DependencyGraph.centrality` now raises rather than
> returning a coin flip when the max-normalised vector never settles, and its docstring states the
> above-`1 / spectral radius` behaviour explicitly: the iteration still settles there, but on the
> dominant-eigenvector direction rather than on the Katz sum.
>
> That leaves a sharper dispute than the one section 1 describes, and it is worth this charter's
> remaining effort: **"settles" and "is the Katz sum" are not the same acceptance criterion.** Above
> `1 / rho` the returned vector is well defined and stable, and is *not* the quantity the Katz
> interpretation promises, so a caller reading the result as attenuated influence is misreading a
> converged number. Rewrite section 1 to that question before starting; sections 4-5 become "decide
> whether to report which regime the result came from", not "add a guard".

---

## 1. The dispute this project settles

The documentation already concedes the problem: the influence series converges only while `alpha` stays below the inverse of the graph's spectral radius, the default `0.4` satisfies that on a sparse market but not on a densely coupled one, and on a dense graph the series diverges before max-normalisation, so the reader is told to "treat a dense graph's centrality with suspicion". A documented warning is not a guard.

## 2. Purpose

Replace the warning with a computed guarantee: estimate the spectral radius, validate `alpha` against it, and refuse or clearly flag any centrality computation that is not convergent.

## 3. Scope

**In scope**

- A spectral radius estimate computed with the standard library only.
- A convergence precondition checked at call time and raised as `InvalidConfigError` when violated.
- A documented fallback for the dense case, and tests on graphs that currently diverge.

**Out of scope**

- Replacing Katz centrality with another measure - that is P23.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the convergence condition formally in terms of the attenuation factor and the spectral radius.
2. Implement a power-iteration estimate of the spectral radius with an explicit iteration cap and tolerance, both validated.
3. Add the precondition check to `centrality`, raising `InvalidConfigError` with a message naming the largest admissible `alpha`.
4. Construct dense test graphs that provably violate the condition and confirm the guard fires.
5. Decide the default behaviour: refuse, or clamp `alpha` and report the clamp. Refusing silently degrades usability; clamping silently changes the number. Argue and choose.
6. Update the module docstring so the guarantee, not the warning, is what the reader sees.

## 5. Task board

- [ ] Formalise the convergence condition.
- [ ] Implement a validated power-iteration spectral radius estimate.
- [ ] Add and test the precondition guard.
- [ ] Build divergent dense test graphs.
- [ ] Decide and implement the refuse-or-clamp policy.
- [ ] Publish `docs/graph/centrality_convergence.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** State the convergence condition and the error introduced by the spectral-radius estimate.
- **Inputs:** `graph.py`, the reading list.
- **Output artifact:** `docs/graph/centrality_convergence.md`.
- **Stop condition:** The admissible `alpha` interval is expressed exactly in terms of the estimate and its error.

### `algorithm-implementer`

- **Mandate:** Implement the estimate and the guard without new dependencies.
- **Inputs:** The formal condition.
- **Output artifact:** A diff under `src/amf/graph.py`.
- **Stop condition:** Divergent inputs raise `InvalidConfigError`; `mypy` strict passes.

### `numerics-auditor`

- **Mandate:** Bound the power-iteration error and verify the guard is conservative rather than optimistic.
- **Inputs:** The implementation.
- **Output artifact:** An error analysis section.
- **Stop condition:** The guard errs on the side of refusing borderline cases.

### `unit-test-author`

- **Mandate:** Add dense graphs that previously returned NaN and confirm they now raise.
- **Inputs:** The guard.
- **Output artifact:** Cases in `tests/unit/test_graph.py`.
- **Stop condition:** Every historical NaN case is now a typed error or a documented clamp.

**Hand-off order:** `math-formalizer` -> `algorithm-implementer` -> `numerics-auditor` -> `unit-test-author`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-centrality-diagnostics` | Centrality is computed or configured | Estimates the spectral radius and validates the attenuation factor against it. |
| `amf-config-validator` | `alpha`, `iterations` or `tolerance` change | Adds domain validation raising `InvalidConfigError` with boundary tests. |
| `amf-float-audit` | An iterative estimate is added | Bounds the iteration error and checks for overflow to infinity. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/graph/centrality_convergence.md`
- A spectral radius estimator
- The convergence guard
- Divergence regression tests

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] No input can produce a NaN centrality without raising first.
- [ ] The admissible `alpha` interval is computed, not assumed.
- [ ] The refuse-or-clamp decision is argued in writing and implemented consistently.
- [ ] The module docstring states a guarantee rather than a warning.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Katz, L. (1953). "A new status index derived from sociometric analysis." *Psychometrika* 18(1), 39-43.
- Bonacich, P. (1987). "Power and Centrality: A Family of Measures." *American Journal of Sociology* 92(5), 1170-1182.
- Horn, R. A., & Johnson, C. R. (2012). *Matrix Analysis* (2nd ed.). Cambridge University Press.
- Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations* (4th ed.). Johns Hopkins University Press.
- Berman, A., & Plemmons, R. J. (1994). *Nonnegative Matrices in the Mathematical Sciences*. SIAM (Classics in Applied Mathematics 9).
- Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.

## 11. Commit protocol

Commits from this project use the scope `p22`:

```text
docs(p22): state the Katz convergence condition and its admissible alpha interval
feat(p22): estimate spectral radius and guard centrality against divergence
test(p22): pin previously divergent dense graphs to a typed error
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

