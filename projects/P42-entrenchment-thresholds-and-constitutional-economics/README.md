# P42 - Entrenchment thresholds and constitutional economics

**Track G - Policy Architecture & Regulatory Regimes**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Policy researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 1.2; issue #122 (31c) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The discussion asks what percentage of binding coverage makes a layer 'entrenched', how long a policy must be in force before it is self-reinforcing, and whether the same thresholds hold across democracies, autocracies and mixed systems. Answering with a single number would be a category error: entrenchment in the constitutional-economics sense is about the rules for changing rules, not about age or coverage.

## 2. Purpose

Replace the percentage-threshold framing with a defensible operationalisation of entrenchment, and test it against the observable record of attempted and failed amendments.

## 3. Scope

**In scope**

- An operational definition of entrenchment grounded in constitutional political economy.
- A dataset of policy lifespans and documented amendment attempts for a defined instrument set.
- A test of whether age, coverage or amendment-rule structure best separates entrenched from mutable rules.

**Out of scope**

- Claiming to predict whether any specific rule will survive.
- Ranking political systems normatively.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Start from constitutional political economy: entrenchment is a property of the amendment rule, not of the rule being amended.
2. Distinguish formal entrenchment (supermajority or special procedure required) from de facto entrenchment (path dependence and increasing returns).
3. Build the lifespan dataset from primary sources: enactment date, amendment dates, and documented failed attempts.
4. Use the case the discussion raises directly - a foundational securities statute in force for over ninety years and rarely rewritten - as the worked example, and check whether age or amendment structure explains its durability.
5. Test the three candidate operationalisations against the dataset and report which separates cleanly.
6. State explicitly that regime-type generalisation is beyond what the dataset can support unless the dataset covers enough regimes.

## 5. Task board

- [ ] Write the operational definition from constitutional political economy.
- [ ] Distinguish formal from de facto entrenchment with examples.
- [ ] Build the policy lifespan and amendment-attempt dataset.
- [ ] Work the foundational-statute example end to end.
- [ ] Test the three operationalisations.
- [ ] Publish `docs/policy/entrenchment.md` plus the dataset.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish entrenchment and path dependence from primary theoretical sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated theory summary.
- **Stop condition:** Formal and de facto entrenchment are each defined from a primary source.

### `case-study-archivist`

- **Mandate:** Build the lifespan dataset with dated, cited enactments, amendments and failed attempts.
- **Inputs:** Official legislative records.
- **Output artifact:** `docs/policy/_data/policy_lifespans.md`.
- **Stop condition:** Every row has an enactment date and at least one primary citation.

### `regime-comparativist`

- **Mandate:** Assess whether the dataset supports any cross-regime claim, and say so if it does not.
- **Inputs:** The dataset.
- **Output artifact:** A coverage assessment.
- **Stop condition:** The assessment states the regimes represented and refuses generalisation beyond them.

### `red-team-critic`

- **Mandate:** Attack the operationalisation with rules that are old but easily changed, and young but immovable.
- **Inputs:** The definition and dataset.
- **Output artifact:** A counterexample report.
- **Stop condition:** Counterexamples are accommodated or the definition is revised.

**Hand-off order:** `literature-scout` -> `case-study-archivist` -> `regime-comparativist` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-case-dossier` | A policy history is documented | Builds the dated, sourced file with enactment, amendment and failed-attempt records. |
| `amf-source-vetting` | A legislative or scholarly source is cited | Confirms primary status and scholarly standing. |
| `amf-red-team` | An operationalisation is proposed | Searches for cases that break it in both directions. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/entrenchment.md`
- `docs/policy/_data/policy_lifespans.md`
- A three-way operationalisation test
- A coverage assessment

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Entrenchment is defined as a property of the amendment rule, with formal and de facto variants distinguished.
- [ ] The dataset rows are all primary-sourced and dated.
- [ ] The chosen operationalisation survives counterexamples in both directions.
- [ ] No cross-regime claim exceeds the dataset's coverage.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Brennan, G., & Buchanan, J. M. (1985). *The Reason of Rules: Constitutional Political Economy*. Cambridge University Press.
- Pierson, P. (2000). "Increasing Returns, Path Dependence, and the Study of Politics." *American Political Science Review* 94(2), 251-267.
- North, D. C. (1990). *Institutions, Institutional Change and Economic Performance*. Cambridge University Press.
- Acemoglu, D., & Robinson, J. A. (2012). *Why Nations Fail: The Origins of Power, Prosperity, and Poverty*. Crown.
- Mahoney, J., & Thelen, K. (eds.) (2010). *Explaining Institutional Change: Ambiguity, Agency, and Power*. Cambridge University Press.
- United States Congress (1933). *Securities Act of 1933*, Pub. L. 73-22.
- La Porta, R., Lopez-de-Silanes, F., Shleifer, A., & Vishny, R. W. (1998). "Law and Finance." *Journal of Political Economy* 106(6), 1113-1155.

## 11. Commit protocol

Commits from this project use the scope `p42`:

```text
docs(p42): operationalise entrenchment from constitutional political economy
docs(p42): publish the primary-sourced policy lifespan dataset
docs(p42): test three entrenchment operationalisations against the record
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

