# P79 - The markets-to-policy feedback loop and reflexivity

**Track N - Policy-Market Contagion and Systemic Indicators**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Complex systems analyst |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 3.2 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The framework's feedback loops are cycles in a fixed dependency graph. Discussion 3.2 asks about a loop of a different type: market distress provokes a policy response, which changes market structure, which changes the distress. That loop crosses the boundary between the modelled system and the rules the model treats as fixed. A framework whose structure is static by construction cannot contain a loop that changes the structure.

## 2. Purpose

Determine whether the framework can represent structure-changing feedback at all, and if not, state that limitation precisely enough that no reader mistakes a static analysis for a dynamic one.

## 3. Scope

**In scope**

- A distinction between feedback *within* a fixed structure and feedback that *alters* the structure.
- An assessment of what the framework's static-graph assumption costs.
- A proposal - a sequence of static analyses, or an explicit refusal - with its limitations stated.

**Out of scope**

- Predicting any policy response.
- Implementing a dynamic-graph simulator before the modelling question is settled.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Separate the two loop types explicitly. The existing feedback-amplification component measures cycles in a graph that does not change; this is a different object.
2. Read the reflexivity and self-fulfilling-expectations literature: the mechanism where a belief or a rule changes the system it describes is well studied and is not a metaphor.
3. Assess the cost of the static assumption. If the response to distress reliably changes the structure, then a resilience score computed on the pre-response structure describes a market that will not exist by the time the stress matters.
4. Consider the tractable middle path: a sequence of static analyses across structures before and after a documented policy change, which is a comparative statics exercise and should be named as one.
5. State plainly what comparative statics cannot deliver - it cannot produce the path, only the endpoints.
6. If the recommendation is to refuse, write the refusal so the static assumption is visible in the output, not only in a document.

## 5. Task board

- [ ] Distinguish within-structure from structure-changing feedback.
- [ ] Review the reflexivity literature.
- [ ] Assess the cost of the static-graph assumption.
- [ ] Evaluate comparative statics as the tractable middle path.
- [ ] State what it cannot deliver.
- [ ] Publish `docs/simulation/reflexive_feedback.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish reflexivity and self-fulfilling dynamics from primary sources, not from popular accounts.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary.
- **Stop condition:** The mechanism is sourced from peer-reviewed work.

### `math-formalizer`

- **Mandate:** State what a static-graph model can and cannot express about structure-changing feedback.
- **Inputs:** The AMF model.
- **Output artifact:** A formal limitation statement.
- **Stop condition:** The limitation is stated as a property of the model, not as a caveat.

### `spec-drafter`

- **Mandate:** Write the comparative-statics proposal with its limits.
- **Inputs:** The limitation statement.
- **Output artifact:** `docs/simulation/reflexive_feedback.md`.
- **Stop condition:** The proposal names what it cannot deliver as prominently as what it can.

### `red-team-critic`

- **Mandate:** Attempt to read a comparative-statics result as a dynamic prediction.
- **Inputs:** Draft output wording.
- **Output artifact:** A misreading report.
- **Stop condition:** No wording supports a path claim.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-doc-page` | The limitation is published | Enforces the illustrative-not-validated rule and documentation conventions. |
| `amf-invariant-spec` | The static assumption is stated | Writes it into the docstring where the model is used. |
| `amf-red-team` | Comparative statics is reported | Tests whether the result can be quoted as a dynamic forecast. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/simulation/reflexive_feedback.md`
- A two-loop-type distinction
- A cost assessment of the static assumption
- A comparative-statics proposal or a written refusal

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The two feedback types are distinguished formally.
- [ ] The static-graph limitation is stated as a model property and appears in the output, not only in a document.
- [ ] Comparative statics, if adopted, is named as such with its limits stated.
- [ ] No wording supports a dynamic-path claim.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Soros, G. (2013). "Fallibility, reflexivity, and the human uncertainty principle." *Journal of Economic Methodology* 20(4), 309-329.
- Merton, R. K. (1948). "The Self-Fulfilling Prophecy." *The Antioch Review* 8(2), 193-210.
- Morris, S., & Shin, H. S. (1998). "Unique Equilibrium in a Model of Self-Fulfilling Currency Attacks." *American Economic Review* 88(3), 587-597.
- Obstfeld, M. (1996). "Models of currency crises with self-fulfilling features." *European Economic Review* 40(3-5), 1037-1047.
- Arthur, W. B. (2015). *Complexity and the Economy*. Oxford University Press.
- Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green.
- Lucas, R. E. (1976). "Econometric policy evaluation: A critique." *Carnegie-Rochester Conference Series on Public Policy* 1, 19-46.
- Danielsson, J., Shin, H. S., & Zigrand, J.-P. (2012). "Endogenous and Systemic Risk." In Haubrich, J. G. & Lo, A. W. (eds.), *Quantifying Systemic Risk*. University of Chicago Press.

## 11. Commit protocol

Commits from this project use the scope `p79`:

```text
docs(p79): distinguish within-structure from structure-changing feedback
docs(p79): state what the static-graph assumption costs
docs(p79): propose comparative statics and name what it cannot deliver
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

