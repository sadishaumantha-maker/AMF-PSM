# P114 - Q2 - Markov transitions, CPTP maps and what the framework already is

**Track T - The Promised Research Modules**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Applied probabilist |
| **Upstream** | `docs/discussions/README.md` module Q2 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Q2 proposes reading market state transitions as quantum channels. The buried finding is that the framework's own propagation step is already a linear map on a bounded state vector, which is a classical Markov-like object with a clip - so the honest question is not whether to add a Lindblad generator but what the existing map is, and whether the quantum generalisation adds anything the classical one lacks. The dispute is whether Q2 describes a new capability or renames one the repository has had since `simulation.py` was written.

## 2. Purpose

Classify the framework's existing propagation map in the standard hierarchy - linear map, stochastic matrix, semigroup - and state precisely what a CPTP generalisation would buy.

## 3. Scope

**In scope**

- A formal classification of `ShockSimulator`'s step map.
- The Markov chain, semigroup and GKSL/Lindblad definitions stated exactly.
- A verdict on what the quantum generalisation adds, if anything.
- The non-Markovianity question stated in terms the framework can answer.

**Out of scope**

- Adding a density-matrix state to `simulation.py`.
- Any dependency on a quantum simulator.
- Claiming the framework's dynamics are a physical process.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Classify the existing map first. `x_{t+1} = clip(damping * (retention * x_t + W^T x_t * transmission * (1 - a)), 0, 1)` is affine before the clip and nonlinear because of it, and it is not a stochastic matrix - the state does not sum to one and mass is not conserved. Say so precisely.
2. State the classical definitions exactly: transition matrix, Chapman-Kolmogorov, stationary distribution, mixing time. Then state complete positivity, trace preservation and the GKSL generator from primary sources.
3. Ask the real question: a CPTP map generalises a stochastic map to non-commuting observables. If the framework has no non-commuting observables - and it does not, its metrics are real numbers that all commute trivially - the generalisation is vacuous. Write that finding rather than dodging it.
4. Rescue the part that is genuinely useful. Mixing time, absorbing states and the spectral gap are classical Markov-chain notions that map cleanly onto convergence questions the framework already asks and answers badly - `converged` currently reports whether the trajectory settled inside the step budget, not whether it is stable.
5. Connect to the existing stability finding rather than restating it: the step map is not a contraction for every market, so the spectral condition belongs here in exact form.
6. Write section 6 against the standing constraints and state that no quantum object enters the package.

## 5. Task board

- [ ] Classify `ShockSimulator`'s step map formally.
- [ ] State the Markov, semigroup and GKSL definitions from primary sources.
- [ ] Rule on what CPTP adds given commuting observables.
- [ ] Extract the usable classical notions - mixing, absorption, spectral gap.
- [ ] State the exact spectral condition for contraction.
- [ ] Publish `docs/discussions/Q2-quantum-markov-lindblad.md` and relink it.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** Classify the step map and derive the spectral condition for contraction exactly.
- **Inputs:** `simulation.py`, `graph.py`.
- **Output artifact:** A classification note with the derived condition.
- **Stop condition:** The clip's effect on linearity is stated, not glossed.

### `literature-scout`

- **Mandate:** Assemble the Markov-chain and open-quantum-systems primary sources separately.
- **Inputs:** The reading list.
- **Output artifact:** An annotated bibliography.
- **Stop condition:** The GKSL generator is cited to its 1976 sources, not to a survey.

### `spec-drafter`

- **Mandate:** Write the module including the vacuity finding on commuting observables.
- **Inputs:** The classification and bibliography.
- **Output artifact:** `docs/discussions/Q2-quantum-markov-lindblad.md`.
- **Stop condition:** The finding is stated as a finding, not softened into a research direction.

### `numerics-auditor`

- **Mandate:** Check the spectral-gap and mixing claims against the implemented convergence test.
- **Inputs:** The derived condition, `simulation.py`.
- **Output artifact:** A reconciliation note.
- **Stop condition:** The gap between `converged` and actual stability is quantified on a worked market.

### `red-team-critic`

- **Mandate:** Attack the module for adopting quantum machinery with no work to do.
- **Inputs:** The draft.
- **Output artifact:** An adversarial report.
- **Stop condition:** Every quantum construct in the module has a stated job or is marked as unused.

**Hand-off order:** `math-formalizer` -> `literature-scout` -> `spec-drafter` -> `numerics-auditor` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-invariant-spec` | The step map is classified | Records the conditions under which each property holds. |
| `amf-literature-brief` | The sources are assembled | Produces the annotated brief. |
| `amf-cascade-calibration` | Convergence behaviour is examined | Exercises the dynamics across the parameter range and reports settling. |
| `amf-doc-page` | The module is published | Enforces conventions and disclaimers. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/discussions/Q2-quantum-markov-lindblad.md`
- A formal classification of the step map
- The exact spectral condition for contraction
- A reconciliation of `converged` with stability

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The step map is classified precisely, clip included.
- [ ] GKSL is cited to its primary sources.
- [ ] The commuting-observables verdict is stated plainly.
- [ ] The spectral condition is derived, not asserted.
- [ ] No quantum object is added to `src/amf/`.
- [ ] The index link resolves.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Lindblad, G. (1976). "On the generators of quantum dynamical semigroups." *Communications in Mathematical Physics* 48(2), 119-130.
- Gorini, V., Kossakowski, A., & Sudarshan, E. C. G. (1976). "Completely positive dynamical semigroups of N-level systems." *Journal of Mathematical Physics* 17(5), 821-825.
- Breuer, H.-P., & Petruccione, F. (2002). *The Theory of Open Quantum Systems*. Oxford University Press.
- Norris, J. R. (1997). *Markov Chains*. Cambridge University Press.
- Kemeny, J. G., & Snell, J. L. (1976). *Finite Markov Chains*. Springer.
- Levin, D. A., & Peres, Y. (2017). *Markov Chains and Mixing Times* (2nd ed.). American Mathematical Society.
- Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information* (10th Anniversary ed.). Cambridge University Press.
- Berman, A., & Plemmons, R. J. (1994). *Nonnegative Matrices in the Mathematical Sciences*. SIAM (Classics in Applied Mathematics 9).
- Horn, R. A., & Johnson, C. R. (2012). *Matrix Analysis* (2nd ed.). Cambridge University Press.
- Khalil, H. K. (2002). *Nonlinear Systems* (3rd ed.). Prentice Hall.

## 11. Commit protocol

Commits from this project use the scope `p114`:

```text
docs(p114): classify the propagation step map formally
docs(p114): derive the spectral condition the dynamics actually require
docs(p114): publish the Q2 module and relink it from the index
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
