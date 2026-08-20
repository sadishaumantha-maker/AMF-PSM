# P25 - Coupling matrix direction semantics: stress flows against the dependency edge

**Track D - Graph & Network Theory of Market Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 3 days |
| **Lead role** | Simulation engineer |
| **Upstream** | `CouplingMatrix`; `CLAUDE.md` -> Simulation ("stress flows target -> source") |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

A dependency edge means the source relies on the target, while stress propagates from target to source - the reverse direction. This inversion is correct but easy to invert again by accident, and it is the single most consequential sign convention in the simulation. It is currently defended by one line of prose and the existence of `CouplingMatrix.order` on the non-trading allowlist.

## 2. Purpose

Make the direction convention structurally impossible to get wrong: state it formally, encode it in the type or the naming, and add a test that fails if the matrix is transposed.

## 3. Scope

**In scope**

- A formal statement of the convention with a worked two-system example.
- A transposition-detection test that fails on a reversed matrix.
- A review of every consumer of the matrix for consistent orientation.

**Out of scope**

- Changing the propagation dynamics - that is Track F.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Write the convention as a worked example: system A depends on B; B is stressed; show the exact matrix entry that carries stress to A.
2. Construct an asymmetric two-system market where the transposed matrix gives a visibly different trace.
3. Add that case as a regression test so a transposition can never pass silently.
4. Audit every consumer of the matrix - propagation, stress test, ensemble - for a consistent reading.
5. Consider encoding orientation in the type so that a transposed matrix is a type error rather than a wrong number.
6. Update the docstring and the `CLAUDE.md` maths summary if the wording admits two readings.

## 5. Task board

- [ ] Write the worked two-system example.
- [ ] Build the asymmetric transposition-detection case.
- [ ] Add the regression test.
- [ ] Audit all matrix consumers.
- [ ] Evaluate encoding orientation in the type.
- [ ] Publish `docs/graph/coupling_orientation.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** State the orientation formally with a worked example.
- **Inputs:** `graph.py`, `simulation.py`.
- **Output artifact:** `docs/graph/coupling_orientation.md`.
- **Stop condition:** The example makes the direction checkable by hand.

### `unit-test-author`

- **Mandate:** Add a test that fails on a transposed matrix.
- **Inputs:** The asymmetric case.
- **Output artifact:** A regression case in `tests/unit/test_graph.py`.
- **Stop condition:** Transposing the matrix in a scratch branch turns the test red.

### `api-surface-reviewer`

- **Mandate:** Audit every consumer for consistent orientation and check the allowlist entry is still accurate.
- **Inputs:** All matrix consumers.
- **Output artifact:** An orientation audit note.
- **Stop condition:** Every consumer reads the matrix the same way and `CouplingMatrix.order` remains the only allowlist entry needed.

**Hand-off order:** `math-formalizer` -> `unit-test-author` -> `api-surface-reviewer`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-invariant-spec` | A sign or direction convention is stated | Writes it into the docstring and mirrors it as a failing-on-inversion test. |
| `amf-boundary-check` | Names on the allowlist are touched | Runs the non-trading guard and verifies every allowlist entry still exists. |
| `amf-determinism-audit` | Matrix construction changes | Confirms the matrix is identical under permuted assembly order. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/graph/coupling_orientation.md`
- A transposition-detection regression test
- An orientation audit of every consumer

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Transposing the coupling matrix causes at least one test to fail.
- [ ] Every consumer reads the orientation identically.
- [ ] The worked example lets a reader verify direction by hand.
- [ ] The non-trading boundary test passes with no new allowlist entries.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Eisenberg, L., & Noe, T. H. (2001). "Systemic Risk in Financial Systems." *Management Science* 47(2), 236-249.
- Gai, P., & Kapadia, S. (2010). "Contagion in financial networks." *Proceedings of the Royal Society A* 466(2120), 2401-2423.
- Acemoglu, D., Ozdaglar, A., & Tahbaz-Salehi, A. (2015). "Systemic Risk and Stability in Financial Networks." *American Economic Review* 105(2), 564-608.
- Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.
- Horn, R. A., & Johnson, C. R. (2012). *Matrix Analysis* (2nd ed.). Cambridge University Press.
- Meyer, B. (1988). *Object-Oriented Software Construction*. Prentice Hall. (design by contract)

## 11. Commit protocol

Commits from this project use the scope `p25`:

```text
docs(p25): formalise the coupling matrix orientation with a worked example
test(p25): fail loudly when the coupling matrix is transposed
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

