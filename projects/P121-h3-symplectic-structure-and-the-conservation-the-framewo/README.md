# P121 - H3 - symplectic structure, and the conservation the framework does not have

**Track T - The Promised Research Modules**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Dynamical-systems researcher |
| **Upstream** | `docs/discussions/README.md` module H3 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

H3 promises symplectic geometry and Hamiltonian dynamics. The framework's dynamics are dissipative by construction - damping below one, a clip, and absorptive capacity that removes stress - so they are not Hamiltonian, and Liouville's theorem does not apply. The dispute is whether that closes the module or opens it: the port-Hamiltonian formalism exists precisely to handle dissipative systems with structure, and whether it fits is a real question rather than a rhetorical one.

## 2. Purpose

Show why the framework's dynamics are not Hamiltonian, then assess the port-Hamiltonian generalisation seriously and rule on whether it offers anything the current formulation lacks.

## 3. Scope

**In scope**

- Symplectic manifolds, Hamiltonian flow and Liouville's theorem stated exactly.
- A demonstration that the framework's step map is not volume preserving.
- The port-Hamiltonian formalism assessed against the framework's dissipation and clipping.
- A verdict on structure-preserving integration, given the model is a discrete map already.

**Out of scope**

- Rewriting `simulation.py` in this project.
- Any claim of energy conservation in a market.
- Numerical-integration dependencies.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Demonstrate the non-conservation rather than asserting it. Compute the Jacobian of the step map away from the clip, show its determinant is below one for any damping below one, and state that volume contracts by that factor per step - that is a short calculation and it settles the Hamiltonian question.
2. State the formalism exactly anyway, because section 3 of the module is a curriculum and a reader has to be able to follow the argument.
3. Take the port-Hamiltonian assessment seriously: it splits a system into a conservative interconnection structure, a dissipation term and external ports, which is structurally similar to what the framework does with coupling, absorptive capacity and injected shocks. Ask whether the analogy is exact and be willing to conclude that it is not - the clip is a hard nonlinearity with no port-Hamiltonian counterpart.
4. Address structure-preserving integrators correctly. They preserve the structure of a continuous flow when discretising it; the framework has no continuous flow to discretise, its map is primitive. So the entire integrator literature applies only if the framework first commits to a continuous-time model, which is itself a decision nobody has taken.
5. State that continuous-time reformulation as an open question with its cost, rather than recommending it: it would change every published trajectory and every settling time.
6. Write section 7's propositions about the Jacobian and the clip, which are computable, rather than about physical analogy.

## 5. Task board

- [ ] Compute the Jacobian and its determinant away from the clip.
- [ ] State the symplectic formalism and Liouville's theorem.
- [ ] Assess the port-Hamiltonian split against coupling, absorption and shocks.
- [ ] Rule on structure-preserving integration given a primitive discrete map.
- [ ] State the continuous-time reformulation as an open question with its cost.
- [ ] Publish `docs/discussions/H3-symplectic-hamiltonian-dynamics.md` and relink it.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** Compute the Jacobian determinant and settle the conservation question.
- **Inputs:** `simulation.py`.
- **Output artifact:** A derivation with the contraction factor stated.
- **Stop condition:** The clip is handled as a separate case, not averaged away.

### `literature-scout`

- **Mandate:** Assemble the classical-mechanics and geometric-integration primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated bibliography.
- **Stop condition:** Liouville's theorem is cited to a primary text.

### `numerics-auditor`

- **Mandate:** Verify the contraction factor numerically across the parameter range.
- **Inputs:** The derivation, `simulation.py`.
- **Output artifact:** A verification table.
- **Stop condition:** The clip boundary is exercised explicitly.

### `spec-drafter`

- **Mandate:** Write the module with the port-Hamiltonian assessment and the open question.
- **Inputs:** All of the above.
- **Output artifact:** `docs/discussions/H3-symplectic-hamiltonian-dynamics.md`.
- **Stop condition:** The continuous-time question states its cost in changed published output.

### `red-team-critic`

- **Mandate:** Attack any physical-conservation language applied to a market.
- **Inputs:** The draft.
- **Output artifact:** An adversarial report.
- **Stop condition:** No sentence asserts a conserved quantity in a market.

**Hand-off order:** `math-formalizer` -> `literature-scout` -> `numerics-auditor` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-invariant-spec` | The Jacobian result is derived | Records the invariant and the conditions under which it holds. |
| `amf-float-audit` | The contraction factor is verified | Checks accumulation and boundary behaviour in the verification. |
| `amf-literature-brief` | The sources are assembled | Produces the annotated brief. |
| `amf-doc-page` | The module is published | Enforces conventions and disclaimers. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/discussions/H3-symplectic-hamiltonian-dynamics.md`
- A Jacobian derivation with the contraction factor
- A port-Hamiltonian assessment
- A costed continuous-time open question

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Non-conservation is demonstrated by calculation, not asserted.
- [ ] The clip is treated as its own case.
- [ ] The port-Hamiltonian assessment reaches a verdict.
- [ ] The integrator literature is correctly scoped to continuous flows.
- [ ] The continuous-time question states its cost.
- [ ] The index link resolves.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Arnold, V. I. (1989). *Mathematical Methods of Classical Mechanics* (2nd ed.). Springer. (symplectic geometry)
- Goldstein, H., Poole, C., & Safko, J. (2002). *Classical Mechanics* (3rd ed.). Addison Wesley.
- Marsden, J. E., & Ratiu, T. S. (1999). *Introduction to Mechanics and Symmetry* (2nd ed.). Springer.
- Hairer, E., Lubich, C., & Wanner, G. (2006). *Geometric Numerical Integration: Structure-Preserving Algorithms for Ordinary Differential Equations* (2nd ed.). Springer.
- Strogatz, S. H. (2015). *Nonlinear Dynamics and Chaos* (2nd ed.). Westview Press.
- Khalil, H. K. (2002). *Nonlinear Systems* (3rd ed.). Prentice Hall.
- Horn, R. A., & Johnson, C. R. (2012). *Matrix Analysis* (2nd ed.). Cambridge University Press.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms* (2nd ed.). SIAM.
- Goldberg, D. (1991). "What Every Computer Scientist Should Know About Floating-Point Arithmetic." *ACM Computing Surveys* 23(1), 5-48.
- May, R. M. (1972). "Will a Large Complex System be Stable?" *Nature* 238, 413-414.

## 11. Commit protocol

Commits from this project use the scope `p121`:

```text
docs(p121): settle the conservation question by Jacobian calculation
docs(p121): assess the port-Hamiltonian split against the framework's dynamics
docs(p121): publish the H3 module and relink it from the index
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

