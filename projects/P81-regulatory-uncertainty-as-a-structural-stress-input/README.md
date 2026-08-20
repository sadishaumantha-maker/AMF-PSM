# P81 - Regulatory uncertainty as a structural stress input

**Track N - Policy-Market Contagion and Systemic Indicators**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Policy researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 1.3; P43 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The framework's shocks are injected into a named system at a named step. Discussion 1.3 asks whether regulatory *uncertainty* - the state of not knowing which rule will apply - is itself a stress. If it is, it is a stress with no single target system and no clear injection point, which the current `Shock` type cannot express.

## 2. Purpose

Decide whether uncertainty is a stress, a capacity reduction, or a category the framework should not model, and make the `Shock` vocabulary honest about which of those it supports.

## 3. Scope

**In scope**

- A structural characterisation of regulatory uncertainty and what it changes.
- An assessment against the `Shock` and `Intervention` types.
- A ruling, with any resulting type change or a documented exclusion.

**Out of scope**

- Any index of policy uncertainty derived from news or market data.
- Predicting a rule change.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Characterise it first: uncertainty about a future rule does not remove capacity today, it changes how participants deploy it - which is a behavioural claim the framework does not model.
2. Test that against the framework's own vocabulary honestly. If the mechanism is behavioural, the framework has no place to put it, and saying so is the finding.
3. If a structural reading exists - for example, an amendment procedure with a wide admissible outcome range is a structural property of the tier, not a belief - develop it, because that is representable.
4. Connect to P41's amendment-property decomposition: the width of the admissible outcome set is exactly the structural residue of uncertainty.
5. Rule, and if the ruling is exclusion, add it to the framework's stated limitations rather than leaving it unaddressed.
6. Keep every quantity structural; a policy-uncertainty index built from news coverage is out of bounds.

## 5. Task board

- [ ] Characterise regulatory uncertainty structurally.
- [ ] Test it against `Shock` and `Intervention`.
- [ ] Develop the amendment-width reading if it holds.
- [ ] Rule, and record any exclusion as a stated limitation.
- [ ] Link the result to P41.
- [ ] Publish `docs/policy/regulatory_uncertainty.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish what the policy-uncertainty literature measures and by what means.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary with methods foregrounded.
- **Stop condition:** The measurement basis of each cited construct is stated.

### `math-formalizer`

- **Mandate:** Develop the amendment-width reading or show it fails.
- **Inputs:** P41's property decomposition.
- **Output artifact:** A formal treatment.
- **Stop condition:** The reading is developed or rejected with a reason.

### `boundary-sentinel`

- **Mandate:** Reject any construct requiring news, price or survey data.
- **Inputs:** The proposals.
- **Output artifact:** A boundary report.
- **Stop condition:** Only structural constructs survive.

### `spec-drafter`

- **Mandate:** Rule and record any exclusion as a stated framework limitation.
- **Inputs:** The formal treatment.
- **Output artifact:** `docs/policy/regulatory_uncertainty.md`.
- **Stop condition:** An exclusion, if ruled, appears in the framework's limitations list.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `boundary-sentinel` -> `spec-drafter`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-boundary-check` | A stress construct is proposed | Rejects news-, price- and survey-derived inputs. |
| `amf-regime-profile` | Amendment width is assessed | Supplies the per-tier procedural properties with citations. |
| `amf-red-team` | A ruling is drafted | Argues the excluded reading and forces an answer. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/regulatory_uncertainty.md`
- A structural characterisation
- The amendment-width treatment
- A ruling and any stated limitation

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The behavioural component is identified and excluded explicitly.
- [ ] The amendment-width reading is developed or rejected with reasons.
- [ ] No construct depends on news, price or survey data.
- [ ] Any exclusion appears in the framework's stated limitations.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Streeck, W., & Thelen, K. (eds.) (2005). *Beyond Continuity: Institutional Change in Advanced Political Economies*. Oxford University Press.
- Mahoney, J., & Thelen, K. (eds.) (2010). *Explaining Institutional Change: Ambiguity, Agency, and Power*. Cambridge University Press.
- Brennan, G., & Buchanan, J. M. (1985). *The Reason of Rules: Constitutional Political Economy*. Cambridge University Press.
- Lucas, R. E. (1976). "Econometric policy evaluation: A critique." *Carnegie-Rochester Conference Series on Public Policy* 1, 19-46.
- Manski, C. F. (2013). *Public Policy in an Uncertain World: Analysis and Decisions*. Harvard University Press.
- Morgan, M. G., & Henrion, M. (1990). *Uncertainty: A Guide to Dealing with Uncertainty in Quantitative Risk and Policy Analysis*. Cambridge University Press.
- Pierson, P. (2000). "Increasing Returns, Path Dependence, and the Study of Politics." *American Political Science Review* 94(2), 251-267.

## 11. Commit protocol

Commits from this project use the scope `p81`:

```text
docs(p81): characterise regulatory uncertainty structurally
docs(p81): develop amendment width as the representable residue
docs(p81): rule on uncertainty as a stress and record the limitation
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
