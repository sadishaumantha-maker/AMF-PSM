# P89 - Informal finance and shadow banking as a system the perimeter excludes

**Track P - Shadow Finance, Capital Flows and Currency**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Market structure researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 5.2 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The seven systems describe a regulated market. Credit intermediation outside that perimeter performs the same functions under different rules, or none. If the framework models only what is inside the perimeter, then its immune system is measured against a body it only partly covers, and every resilience score is computed on an incomplete organism.

## 2. Purpose

Determine whether non-bank intermediation is a separate market, a set of systems inside the same market, or an unmodellable exterior - and state what the answer costs the resilience score.

## 3. Scope

**In scope**

- A functional characterisation of intermediation outside the regulatory perimeter.
- Three candidate representations, assessed against the seven-system model.
- A statement of what the chosen representation omits.

**Out of scope**

- Estimating the size of any shadow banking sector.
- Any quantity requiring balance-sheet or flow data.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Characterise by function, not by entity type. The official-sector work defines this sector by the credit-intermediation functions performed rather than by the label on the institution, and that is the definition that transfers to a functional model.
2. Assess the three representations: a separate `Market` with its own seven systems, additional components inside existing systems, or an exogenous influence per P82's convention.
3. Test each against the framework's own semantics - a separate market cannot be coupled to another market at all in the current model, which is decisive.
4. State the omission explicitly whichever way it rules: if the perimeter excludes a functioning part of the system, the immune-system score describes coverage of a subset.
5. Note the regulatory-arbitrage mechanism: activity migrates to where the rules bind least, which means the excluded region is not random but is precisely the region where constraints are weakest.
6. Coordinate with P51, which owns the question of whether the model transfers to other asset classes.

## 5. Task board

- [ ] Characterise the sector functionally with citations.
- [ ] Assess the three candidate representations.
- [ ] Test each against the current model semantics.
- [ ] Rule and state the omission.
- [ ] Record the regulatory-arbitrage mechanism.
- [ ] Publish `docs/taxonomies/shadow_intermediation.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish the functional definition from official-sector and peer-reviewed sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated functional definition.
- **Stop condition:** The definition is functional, not entity-based.

### `taxonomy-cartographer`

- **Mandate:** Assess the three representations against the seven-system model.
- **Inputs:** The definition and the AMF model.
- **Output artifact:** A representation comparison.
- **Stop condition:** Each representation is tested against current model semantics, not against intuition.

### `spec-drafter`

- **Mandate:** Rule and state the omission in terms a score reader understands.
- **Inputs:** The comparison.
- **Output artifact:** `docs/taxonomies/shadow_intermediation.md`.
- **Stop condition:** The omission's effect on the immune-system score is stated.

### `boundary-sentinel`

- **Mandate:** Reject any characterisation requiring balance-sheet or flow data.
- **Inputs:** The proposals.
- **Output artifact:** A boundary report.
- **Stop condition:** All surviving constructs are structural.

**Hand-off order:** `literature-scout` -> `taxonomy-cartographer` -> `spec-drafter` -> `boundary-sentinel`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-taxonomy-builder` | The sector is catalogued | Builds the functional table with official-source citations. |
| `amf-boundary-check` | A construct is proposed | Rejects balance-sheet and flow quantities. |
| `amf-regime-profile` | Perimeter definitions are compared | Records each jurisdiction's perimeter with instrument citations. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/taxonomies/shadow_intermediation.md`
- A functional definition
- A three-way representation comparison
- A stated omission

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The definition is functional and officially sourced.
- [ ] Each representation is tested against current model semantics.
- [ ] The omission's effect on the immune-system score is stated explicitly.
- [ ] No construct requires balance-sheet or flow data.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Pozsar, Z., Adrian, T., Ashcraft, A., & Boesky, H. (2013). "Shadow Banking." *FRBNY Economic Policy Review* 19(2), 1-16.
- Financial Stability Board (2011). *Shadow Banking: Scoping the Issues*. FSB Background Note.
- Gorton, G., & Metrick, A. (2012). "Securitized banking and the run on repo." *Journal of Financial Economics* 104(3), 425-451.
- Buchak, G., Matvos, G., Piskorski, T., & Seru, A. (2018). "Fintech, regulatory arbitrage, and the rise of shadow banks." *Journal of Financial Economics* 130(3), 453-483.
- Adrian, T., & Brunnermeier, M. K. (2016). "CoVaR." *American Economic Review* 106(7), 1705-1741.
- Minsky, H. P. (1986). *Stabilizing an Unstable Economy*. Yale University Press.
- Demirguc-Kunt, A., Klapper, L., Singer, D., Ansar, S., & Hess, J. (2018). *The Global Findex Database 2017*. World Bank.
- Stigler, G. J. (1971). "The Theory of Economic Regulation." *Bell Journal of Economics and Management Science* 2(1), 3-21.

## 11. Commit protocol

Commits from this project use the scope `p89`:

```text
docs(p89): define non-bank intermediation functionally rather than by entity
docs(p89): compare three representations against the seven-system model
docs(p89): state what the chosen representation omits from the immune score
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
