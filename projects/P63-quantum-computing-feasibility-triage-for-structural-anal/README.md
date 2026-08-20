# P63 - Quantum computing feasibility triage for structural analysis

**Track J - Advanced Methods: Topology, Learning, Information & Quantum**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Research lead |
| **Upstream** | `docs/QUANTUM_NEURAL_RESEARCH.md` Discussion H1; adoption roadmap |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The research document proposes quantum circuits as components and sets a multi-year adoption roadmap. The framework's computational load is a seven-node graph and a fifty-step linear recurrence, which runs in microseconds on a laptop. The dispute is whether there is any problem here that quantum computation could address, or whether the roadmap is aspiration without a problem statement.

## 2. Purpose

Triage the proposal against the actual computational profile of the framework, and record either a concrete candidate problem or a reasoned deferral with the condition that would revive it.

## 3. Scope

**In scope**

- A measured computational profile of the framework's heaviest operations.
- An assessment of which, if any, admit a quantum formulation with a known advantage.
- A deferral condition: what would have to change for this to become worth revisiting.

**Out of scope**

- Adding any quantum computing dependency.
- Claiming a speed-up without a cited algorithmic result.
- Retaining the multi-year roadmap without a problem statement.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Measure first. Profile feedback-loop enumeration, centrality, ensemble simulation and sensitivity analysis at realistic and stress sizes.
2. Identify which operations are actually expensive; feedback-loop enumeration on dense graphs is the only plausible candidate, and its cost is combinatorial rather than numerical.
3. Review the current state of quantum computing for finance from primary sources, including the honest assessments of near-term device limitations.
4. State the deferral condition concretely: for example, a market graph large enough that classical enumeration is infeasible, which the seven-system model does not produce.
5. Rewrite or retire the adoption roadmap so it is conditioned on a problem rather than on a date.
6. Record the triage so the proposal can be revisited on evidence rather than enthusiasm.

## 5. Task board

- [ ] Profile the framework's heaviest operations at several sizes.
- [ ] Identify candidate operations by cost class.
- [ ] Review the state of the art from primary sources.
- [ ] State the concrete deferral condition.
- [ ] Rewrite or retire the adoption roadmap.
- [ ] Publish `docs/methods/quantum_triage.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `benchmark-runner`

- **Mandate:** Profile the heaviest operations at realistic and stress sizes with reproducible commands.
- **Inputs:** The package.
- **Output artifact:** A profile table.
- **Stop condition:** Every operation has a measured cost at three input sizes.

### `literature-scout`

- **Mandate:** Summarise the state of quantum computing for finance from primary sources including limitation assessments.
- **Inputs:** The reading list.
- **Output artifact:** An annotated state-of-the-art summary.
- **Stop condition:** Near-term device limitations are stated as prominently as the prospects.

### `spec-drafter`

- **Mandate:** Write the triage and the concrete deferral condition.
- **Inputs:** Profile and literature.
- **Output artifact:** `docs/methods/quantum_triage.md`.
- **Stop condition:** The deferral condition is stated as a measurable property, not a date.

### `red-team-critic`

- **Mandate:** Argue the strongest case for proceeding and test it against the profile.
- **Inputs:** The draft.
- **Output artifact:** A dissent section.
- **Stop condition:** The dissent is answered with measured cost, not opinion.

**Hand-off order:** `benchmark-runner` -> `literature-scout` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-source-vetting` | A quantum advantage is claimed | Requires a cited algorithmic result with its stated assumptions. |
| `amf-doc-page` | The triage is published | Enforces documentation conventions and the negative-result rule. |
| `amf-red-team` | A roadmap is retained | Requires a problem statement rather than a date. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/methods/quantum_triage.md`
- A measured computational profile
- A state-of-the-art summary with limitations
- A concrete deferral condition

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The computational profile is measured, not estimated.
- [ ] The deferral condition is a measurable property, not a date.
- [ ] No quantum dependency is added.
- [ ] The adoption roadmap is rewritten or retired.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information* (10th Anniversary ed.). Cambridge University Press.
- Preskill, J. (2018). "Quantum Computing in the NISQ era and beyond." *Quantum* 2, 79.
- Orus, R., Mugel, S., & Lizaso, E. (2019). "Quantum computing for finance: Overview and prospects." *Reviews in Physics* 4, 100028.
- Egger, D. J., et al. (2020). "Quantum Computing for Finance: State-of-the-Art and Future Prospects." *IEEE Transactions on Quantum Engineering* 1, 3101724.
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.
- Johnson, D. B. (1975). "Finding all the elementary circuits of a directed graph." *SIAM Journal on Computing* 4(1), 77-84.
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.

## 11. Commit protocol

Commits from this project use the scope `p63`:

```text
test(p63): profile the framework's heaviest operations at three input sizes
docs(p63): triage quantum computing against the measured computational profile
docs(p63): condition the adoption roadmap on a problem rather than a date
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
