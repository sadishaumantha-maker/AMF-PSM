# P40 - Formalising the policy-tier hierarchy: who decides, and how fast

**Track G - Policy Architecture & Regulatory Regimes**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Policy researcher |
| **Upstream** | issue #120 (31a); PR #42 (immune system as a layered policy stack) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The immune system is modelled as a layered regulatory policy stack, but the number of tiers, their boundaries and their ordering criterion are all unsettled. Some contributors order tiers by legal authority, others by speed of change. Those two orderings do not coincide - a central bank operating procedure changes faster than a statute but binds more immediately.

## 2. Purpose

Fix the tier hierarchy on an explicit ordering criterion drawn from the institutional-analysis literature, and define each tier by properties that can be checked against a real rule rather than argued about.

## 3. Scope

**In scope**

- An explicit ordering criterion for tiers, with the rejected alternatives recorded.
- A tier definition table: decision-maker, binding scope, typical change latency, reversal cost.
- A classification test: given a real rule, which tier does it belong to, and why.

**Out of scope**

- Implementing tiers in `src/amf/` before the definitions are ratified.
- Assigning normative value to any tier arrangement.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Adopt the institutional-analysis distinction between constitutional-choice, collective-choice and operational rules as the starting frame, and state where AMF's tiers sit relative to it.
2. Test the frame against the Lamfalussy four-level structure in European securities regulation, which is an existing, documented tiering of exactly this kind.
3. Define each tier by checkable properties, not by name: who may amend it, what it binds, how long a change takes, what a reversal costs.
4. Write a classification test and run it on at least fifteen real rules spanning statute, delegated regulation, supervisory guidance and exchange rulebook.
5. Where a rule classifies ambiguously, that is a boundary defect - refine the definition rather than the example.
6. Ratify the hierarchy before any code depends on it.

## 5. Task board

- [ ] Write the ordering-criterion decision with rejected alternatives.
- [ ] Build the tier definition table with checkable properties.
- [ ] Assemble a corpus of at least fifteen real rules.
- [ ] Run the classification test and record ambiguities.
- [ ] Refine definitions until ambiguity is eliminated or documented.
- [ ] Publish `docs/policy/tier_hierarchy.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish the institutional rule-level framework and the Lamfalussy structure from primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated source table.
- **Stop condition:** Both frames are quoted from primary sources, not summaries.

### `regime-comparativist`

- **Mandate:** Assemble the rule corpus across jurisdictions and instrument types.
- **Inputs:** Public regulatory sources.
- **Output artifact:** `docs/policy/_data/rule_corpus.md` with citation per rule.
- **Stop condition:** At least fifteen rules span four instrument types and three jurisdictions.

### `spec-drafter`

- **Mandate:** Write the tier definitions as checkable properties and the classification test.
- **Inputs:** Sources and corpus.
- **Output artifact:** `docs/policy/tier_hierarchy.md`.
- **Stop condition:** Every tier is defined without using the word 'important'.

### `red-team-critic`

- **Mandate:** Find rules that classify into two tiers under the definitions.
- **Inputs:** Definitions and corpus.
- **Output artifact:** An ambiguity report.
- **Stop condition:** Every ambiguity is resolved by refinement or documented as an accepted boundary case.

**Hand-off order:** `literature-scout` -> `regime-comparativist` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | A jurisdiction's rules are catalogued | Produces a structured regulatory-regime profile with citations to primary instruments. |
| `amf-source-vetting` | A regulatory source is cited | Confirms the instrument is the official text, not a commentary or news report. |
| `amf-red-team` | Tier definitions are drafted | Searches the corpus for rules that classify ambiguously. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/tier_hierarchy.md`
- A tier definition table with checkable properties
- A cited rule corpus
- A classification test with results

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The ordering criterion is stated with its rejected alternatives.
- [ ] Every tier is defined by checkable properties only.
- [ ] At least fifteen real rules classify unambiguously, or the exceptions are documented.
- [ ] No code depends on the hierarchy until it is ratified.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Ostrom, E. (2005). *Understanding Institutional Diversity*. Princeton University Press.
- Ostrom, E. (1990). *Governing the Commons: The Evolution of Institutions for Collective Action*. Cambridge University Press.
- North, D. C. (1990). *Institutions, Institutional Change and Economic Performance*. Cambridge University Press.
- Committee of Wise Men (2001). *Final Report of the Committee of Wise Men on the Regulation of European Securities Markets* (the Lamfalussy Report). European Commission.
- European Union (2014). *Directive 2014/65/EU on markets in financial instruments (MiFID II)*. Official Journal of the European Union.
- Brennan, G., & Buchanan, J. M. (1985). *The Reason of Rules: Constitutional Political Economy*. Cambridge University Press.
- Sabatier, P. A., & Weible, C. M. (eds.) (2014). *Theories of the Policy Process* (3rd ed.). Westview Press.

## 11. Commit protocol

Commits from this project use the scope `p40`:

```text
docs(p40): choose and justify the policy-tier ordering criterion
docs(p40): assemble a cited multi-jurisdiction rule corpus
docs(p40): ratify the tier hierarchy with a classification test
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

