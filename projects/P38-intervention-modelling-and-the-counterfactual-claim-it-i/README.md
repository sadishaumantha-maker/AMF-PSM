# P38 - Intervention modelling and the counterfactual claim it implies

**Track F - Shock Propagation, Cascades & Resilience**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Simulation engineer |
| **Upstream** | `Intervention`; `examples/cascade_scenario.py` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

An `Intervention` boosts a system's absorptive capacity from a given step. Comparing a run with and without it is a counterfactual claim: *this intervention would have reduced stress by this much*. The framework is explicitly illustrative and not validated, so it must be extremely careful about how that comparison is presented, and it currently has no guardrail at all.

## 2. Purpose

Define what an intervention comparison means inside the model, implement it so the comparison is structurally sound, and constrain its presentation so it can never be read as a policy recommendation.

## 3. Scope

**In scope**

- A formal definition of the intervention counterfactual within the model's own terms.
- A paired-comparison implementation that holds everything except the intervention fixed.
- Presentation rules for reporting an intervention effect.

**Out of scope**

- Any claim about what an intervention would do in a real market.
- Optimising over interventions to recommend one.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Define the counterfactual precisely: same market, same shock, same seed, one parameter changed at one step.
2. Implement the paired run so that seeds and every other input are provably identical between arms.
3. Report the effect as a within-model difference, with the model's assumptions attached to the number.
4. Consult the causal-inference literature on what a model-internal counterfactual does and does not support.
5. Write presentation rules: an intervention effect is a property of the model, never of a market.
6. Add a test proving the two arms differ only in the intervention.

## 5. Task board

- [ ] Formalise the model-internal counterfactual.
- [ ] Implement provably paired runs.
- [ ] Report the effect with attached assumptions.
- [ ] Write the presentation rules.
- [ ] Add the arm-equality test.
- [ ] Publish `docs/simulation/interventions.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** Define the counterfactual in the model's own terms and state what it cannot support.
- **Inputs:** `simulation.py`, the reading list.
- **Output artifact:** `docs/simulation/interventions.md`.
- **Stop condition:** The definition names the external claim it does not license.

### `algorithm-implementer`

- **Mandate:** Implement paired runs with provably identical inputs except the intervention.
- **Inputs:** The definition.
- **Output artifact:** A diff under `src/amf/simulation.py`.
- **Stop condition:** A test proves the two arms share seed, market and shock exactly.

### `docs-synthesizer`

- **Mandate:** Write the presentation rules and apply them to the example script.
- **Inputs:** The definition.
- **Output artifact:** Updated `examples/cascade_scenario.py` output text.
- **Stop condition:** Every printed intervention effect carries its model-internal qualifier.

### `red-team-critic`

- **Mandate:** Attempt to quote the output as a policy recommendation and see whether the wording permits it.
- **Inputs:** Draft output.
- **Output artifact:** A wording critique.
- **Stop condition:** No quotation survives as a policy claim.

**Hand-off order:** `math-formalizer` -> `algorithm-implementer` -> `docs-synthesizer` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-invariant-spec` | Paired-run equality is claimed | Writes the invariant and mirrors it as a test. |
| `amf-doc-page` | Publishing intervention guidance | Enforces the illustrative-not-validated rule. |
| `amf-red-team` | An effect size is reported | Attempts to extract a policy claim from the wording. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/simulation/interventions.md`
- Provably paired run support
- Presentation rules
- An arm-equality test

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The counterfactual is defined in model-internal terms and names what it cannot support.
- [ ] A test proves the two arms differ only in the intervention.
- [ ] Every reported effect carries its qualifier.
- [ ] No output can be quoted as a policy recommendation.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.). Cambridge University Press.
- Peters, J., Janzing, D., & Scholkopf, B. (2017). *Elements of Causal Inference: Foundations and Learning Algorithms*. MIT Press.
- Manski, C. F. (2013). *Public Policy in an Uncertain World: Analysis and Decisions*. Harvard University Press.
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.
- Morgan, M. G., & Henrion, M. (1990). *Uncertainty: A Guide to Dealing with Uncertainty in Quantitative Risk and Policy Analysis*. Cambridge University Press.
- Board of Governors of the Federal Reserve System & OCC (2011). *Supervisory Guidance on Model Risk Management* (SR 11-7 / OCC Bulletin 2011-12).
- Saltelli, A., et al. (2020). "Five ways to ensure that models serve society: a manifesto." *Nature* 582, 482-484.

## 11. Commit protocol

Commits from this project use the scope `p38`:

```text
docs(p38): define the intervention counterfactual and its limits
test(p38): prove intervention comparison arms are otherwise identical
docs(p38): constrain how intervention effects may be reported
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
