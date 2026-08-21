# P119 - H1 - variational circuits, and the trainability result that decides the module

**Track T - The Promised Research Modules**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Quantum-computing researcher |
| **Upstream** | `docs/discussions/README.md` module H1 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

H1 promises quantum circuits as neural-network components. The module cannot be written as advocacy because a published result decides most of it: for a broad class of randomly initialised parameterised circuits, the gradient concentrates exponentially in the number of qubits, so training stalls before it starts. The dispute is whether the module reports that result honestly at the top or buries it in a limitations section at the bottom, and whether anything the framework needs survives it.

## 2. Purpose

Write H1 with the trainability and hardware constraints stated first, and assess whether a variational circuit could do any job the framework has - given that it has twenty-eight numbers and no training set.

## 3. Scope

**In scope**

- Variational circuits and the parameter-shift rule stated exactly.
- The barren-plateau result stated with its scope and its known mitigations.
- The current hardware constraints stated as constraints, from primary sources.
- A verdict on whether the framework has a job for any of it.

**Out of scope**

- Any quantum simulator dependency, in the package or in its tests.
- Claims about quantum advantage for any market task.
- Circuit code of any kind in this repository.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Put the trainability result in section 2, not section 6. A module that presents variational circuits for three pages and then mentions barren plateaus in passing has misled its reader, and this index promises modules that cite the skeptical literature on purpose.
2. State the parameter-shift rule exactly, because it is the mechanism that makes gradient training of a circuit possible at all, and the module cannot assess trainability without it.
3. State the mitigations fairly - structured initialisation, shallow and problem-informed ansatze, layerwise training - and then state their cost: each one narrows the class of circuits, which narrows the claimed advantage.
4. Do the sizing honestly. The framework's object is seven systems; a problem that small does not need a quantum computer, and saying so is the correct engineering finding.
5. Read the quantum-finance surveys as claims to be checked rather than as evidence. Note where a survey's projected application assumes data the framework does not have.
6. Write section 6 to state that no quantum dependency may enter the package or its test suite, and that the sidecar boundary from D1 applies here unchanged.

## 5. Task board

- [ ] State variational circuits and the parameter-shift rule exactly.
- [ ] State the barren-plateau result with scope and mitigations in section 2.
- [ ] State the hardware constraints from primary sources.
- [ ] Do the problem-size assessment.
- [ ] Check the survey claims against available data.
- [ ] Publish `docs/discussions/H1-quantum-neural-hybrid-circuits.md` and relink it.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Assemble the variational-algorithm and trainability sources, and the surveys separately.
- **Inputs:** The reading list.
- **Output artifact:** An annotated bibliography.
- **Stop condition:** The barren-plateau paper is cited directly, not through a survey.

### `math-formalizer`

- **Mandate:** State the parameter-shift rule and the gradient-concentration result exactly.
- **Inputs:** The primary sources.
- **Output artifact:** A formal statement of both, scope included.
- **Stop condition:** The scope of the concentration result is stated, not generalised.

### `spec-drafter`

- **Mandate:** Write the module with the constraints leading and the size assessment included.
- **Inputs:** All of the above.
- **Output artifact:** `docs/discussions/H1-quantum-neural-hybrid-circuits.md`.
- **Stop condition:** The trainability result appears in section 2.

### `boundary-sentinel`

- **Mandate:** Confirm no quantum dependency enters the package or the test suite.
- **Inputs:** `pyproject.toml`, `tests/`.
- **Output artifact:** A dependency verdict.
- **Stop condition:** The test extras are checked, not only the runtime dependencies.

### `red-team-critic`

- **Mandate:** Attack the module for any implied quantum advantage.
- **Inputs:** The draft.
- **Output artifact:** An adversarial report.
- **Stop condition:** No sentence claims advantage for a market task.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `spec-drafter` -> `boundary-sentinel` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-literature-brief` | The sources are assembled | Produces the annotated brief. |
| `amf-invariant-spec` | The trainability result is stated | Records the conditions under which it holds. |
| `amf-boundary-check` | The dependency verdict is written | Checks the package and test surfaces against the zero-dependency rule. |
| `amf-doc-page` | The module is published | Enforces conventions and disclaimers. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/discussions/H1-quantum-neural-hybrid-circuits.md`
- A formal statement of the parameter-shift rule
- A scoped statement of the trainability result
- A problem-size assessment

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The trainability result appears in section 2 with its scope.
- [ ] The parameter-shift rule is written out.
- [ ] Mitigations are stated with their costs.
- [ ] The size assessment reaches an engineering conclusion.
- [ ] No quantum dependency enters the package or its tests.
- [ ] The index link resolves.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Cerezo, M., et al. (2021). "Variational quantum algorithms." *Nature Reviews Physics* 3, 625-644.
- McClean, J. R., Boixo, S., Smelyanskiy, V. N., Babbush, R., & Neven, H. (2018). "Barren plateaus in quantum neural network training landscapes." *Nature Communications* 9, 4812.
- Preskill, J. (2018). "Quantum Computing in the NISQ era and beyond." *Quantum* 2, 79.
- Biamonte, J., Wittek, P., Pancotti, N., Rebentrost, P., Wiebe, N., & Lloyd, S. (2017). "Quantum machine learning." *Nature* 549, 195-202.
- Schuld, M., & Petruccione, F. (2021). *Machine Learning with Quantum Computers* (2nd ed.). Springer.
- Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information* (10th Anniversary ed.). Cambridge University Press.
- Orus, R., Mugel, S., & Lizaso, E. (2019). "Quantum computing for finance: Overview and prospects." *Reviews in Physics* 4, 100028.
- Egger, D. J., et al. (2020). "Quantum Computing for Finance: State-of-the-Art and Future Prospects." *IEEE Transactions on Quantum Engineering* 1, 3101724.
- Wolpert, D. H., & Macready, W. G. (1997). "No Free Lunch Theorems for Optimization." *IEEE Transactions on Evolutionary Computation* 1(1), 67-82.
- Vapnik, V. N. (1998). *Statistical Learning Theory*. Wiley.

## 11. Commit protocol

Commits from this project use the scope `p119`:

```text
docs(p119): state the parameter-shift rule and the trainability result
docs(p119): assess problem size and the surveys' assumed data
docs(p119): publish the H1 module and relink it from the index
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
