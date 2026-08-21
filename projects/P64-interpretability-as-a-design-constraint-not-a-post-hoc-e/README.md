# P64 - Interpretability as a design constraint, not a post-hoc explanation

**Track J - Advanced Methods: Topology, Learning, Information & Quantum**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Research lead |
| **Upstream** | `docs/QUANTUM_NEURAL_RESEARCH.md` Discussion I2; `WeaknessFinding.drivers` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The framework already produces plain-language `drivers` explaining each finding, which is interpretable-by-construction. Several proposals in the research documentation would replace parts of that with learned components explained after the fact. The interpretability literature argues specifically against that trade in high-stakes settings.

## 2. Purpose

Adopt an explicit interpretability policy for the repository: what must remain interpretable by construction, and what standard any post-hoc explanation would have to meet before it could be accepted.

## 3. Scope

**In scope**

- A policy statement on interpretable-by-construction components.
- An audit of the existing `drivers` mechanism against that policy.
- A standard that any future post-hoc explanation method must meet.

**Out of scope**

- Implementing any post-hoc explanation method.
- Weakening the existing driver explanations.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the policy: any component whose output reaches a rendered finding must be interpretable by construction.
2. Audit the existing drivers: are the explanation thresholds documented, are the strings accurate, and does every driver correspond to a component that actually crossed its threshold?
3. Review the argument against post-hoc explanation in high-stakes settings, and the known instability of the popular attribution methods.
4. Set the standard a post-hoc method would have to meet: stability under input perturbation, and faithfulness to the underlying computation.
5. Note that the framework's own sensitivity analysis is already a faithfulness check available for free.
6. Publish the policy so future proposals are evaluated against it rather than argued from scratch.

## 5. Task board

- [ ] Write the interpretability policy.
- [ ] Audit the existing drivers mechanism.
- [ ] Review the post-hoc explanation critique.
- [ ] Set the acceptance standard for post-hoc methods.
- [ ] Link the standard to the existing sensitivity machinery.
- [ ] Publish `docs/methods/interpretability_policy.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Collect the interpretable-by-construction argument and the attribution-method critiques.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary.
- **Stop condition:** Both the methods and their critiques are represented.

### `api-surface-reviewer`

- **Mandate:** Audit the existing drivers mechanism for accuracy and threshold documentation.
- **Inputs:** `diagnostics.py`, `models.py`, `report.py`.
- **Output artifact:** A drivers audit report.
- **Stop condition:** Every driver string is traced to the component and threshold that emits it.

### `spec-drafter`

- **Mandate:** Write the policy and the post-hoc acceptance standard.
- **Inputs:** Literature and audit.
- **Output artifact:** `docs/methods/interpretability_policy.md`.
- **Stop condition:** The standard is testable, not aspirational.

### `unit-test-author`

- **Mandate:** Add tests pinning each driver to its emitting condition.
- **Inputs:** The audit.
- **Output artifact:** Cases in `tests/unit/test_diagnostics.py`.
- **Stop condition:** Each driver has a test that fails if its threshold changes silently.

**Hand-off order:** `literature-scout` -> `api-surface-reviewer` -> `spec-drafter` -> `unit-test-author`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-invariant-spec` | An explanation threshold is documented | Writes it into the docstring and mirrors it as a test. |
| `amf-doc-page` | The policy is published | Enforces documentation conventions. |
| `amf-red-team` | A post-hoc method is proposed | Tests it against the stability and faithfulness standard. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/methods/interpretability_policy.md`
- A drivers audit report
- A post-hoc acceptance standard
- Driver threshold tests

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The policy states which components must be interpretable by construction.
- [ ] Every driver string is traced to its emitting component and threshold.
- [ ] Each driver has a test that fails if its threshold changes silently.
- [ ] The post-hoc acceptance standard is testable.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Rudin, C. (2019). "Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead." *Nature Machine Intelligence* 1, 206-215.
- Lundberg, S. M., & Lee, S.-I. (2017). "A Unified Approach to Interpreting Model Predictions." *NeurIPS 2017*.
- Ribeiro, M. T., Singh, S., & Guestrin, C. (2016). "Why Should I Trust You?: Explaining the Predictions of Any Classifier." *KDD 2016*.
- Board of Governors of the Federal Reserve System & OCC (2011). *Supervisory Guidance on Model Risk Management* (SR 11-7 / OCC Bulletin 2011-12).
- Saltelli, A., et al. (2020). "Five ways to ensure that models serve society: a manifesto." *Nature* 582, 482-484.
- Morgan, M. G., & Henrion, M. (1990). *Uncertainty: A Guide to Dealing with Uncertainty in Quantitative Risk and Policy Analysis*. Cambridge University Press.
- Spiegelhalter, D., Pearson, M., & Short, I. (2011). "Visualizing Uncertainty About the Future." *Science* 333(6048), 1393-1400.

## 11. Commit protocol

Commits from this project use the scope `p64`:

```text
docs(p64): adopt interpretable-by-construction as a design constraint
test(p64): pin every finding driver to its emitting threshold
docs(p64): set the acceptance standard for post-hoc explanation methods
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
