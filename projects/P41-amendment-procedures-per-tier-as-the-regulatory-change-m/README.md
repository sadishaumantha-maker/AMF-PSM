# P41 - Amendment procedures per tier as the regulatory change mechanism

**Track G - Policy Architecture & Regulatory Regimes**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Policy researcher |
| **Upstream** | issue #121 (31b) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Each tier is supposed to carry its own amendment procedure, but a procedure has at least four separable properties - who initiates, who must consent, how long it takes and what can veto it - and the current sketch collapses them into a single 'difficulty' rating. Collapsing them loses exactly the information that determines whether a rule can be changed in a crisis.

## 2. Purpose

Decompose amendment into its separable properties, populate them per tier from primary instruments, and identify which property actually binds when speed matters.

## 3. Scope

**In scope**

- A property decomposition of amendment procedure.
- Per-tier population from primary legal instruments across at least three jurisdictions.
- Identification of the binding constraint under time pressure, with documented crisis examples.

**Out of scope**

- Predicting whether any specific rule will change.
- Normative claims about which procedure is better.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Decompose amendment into initiation, consent, latency and veto properties, and justify the decomposition.
2. Populate each property per tier from the actual instruments, citing the article or section that sets it.
3. Identify emergency and expedited procedures explicitly - most regimes have them, and they change which property binds.
4. Use documented crisis episodes to test which property actually bound, rather than which one looks strictest on paper.
5. Record the gap between the nominal and the effective procedure; that gap is a structural finding in its own right.
6. Link the result to the tier hierarchy from P40 so the two documents form one model.

## 5. Task board

- [ ] Write and justify the property decomposition.
- [ ] Populate properties per tier with instrument-level citations.
- [ ] Catalogue emergency and expedited procedures.
- [ ] Test against documented crisis episodes.
- [ ] Record nominal versus effective procedure gaps.
- [ ] Publish `docs/policy/amendment_procedures.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `regime-comparativist`

- **Mandate:** Populate amendment properties per tier from primary instruments in at least three jurisdictions.
- **Inputs:** Official regulatory texts.
- **Output artifact:** A populated property table with citations.
- **Stop condition:** Every cell cites an article or section, or is marked `not specified in instrument`.

### `case-study-archivist`

- **Mandate:** Assemble documented crisis episodes where an expedited procedure was used.
- **Inputs:** Official records and peer-reviewed accounts.
- **Output artifact:** A dated episode file per case.
- **Stop condition:** Each episode has a primary-source date and instrument reference.

### `spec-drafter`

- **Mandate:** Write the decomposition and identify the binding constraint under time pressure.
- **Inputs:** Property table and episodes.
- **Output artifact:** `docs/policy/amendment_procedures.md`.
- **Stop condition:** The binding property is named per tier with evidence.

### `red-team-critic`

- **Mandate:** Argue that the nominal procedure never binds and see whether the evidence answers.
- **Inputs:** The draft.
- **Output artifact:** A dissent section.
- **Stop condition:** The dissent is adopted or answered with cited episodes.

**Hand-off order:** `regime-comparativist` -> `case-study-archivist` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | Amendment properties are catalogued | Produces the structured per-jurisdiction profile with instrument citations. |
| `amf-case-dossier` | A crisis episode is used as evidence | Builds a dated, sourced structural case file with no market-data quantities. |
| `amf-source-vetting` | An instrument or account is cited | Confirms it is a primary source of adequate standing. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/amendment_procedures.md`
- A populated per-tier property table
- Crisis episode files
- A nominal-versus-effective gap analysis

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Amendment is decomposed into at least four separable properties with justification.
- [ ] Every property cell is cited to an instrument or marked unspecified.
- [ ] The binding constraint under time pressure is named per tier with evidence.
- [ ] The document links coherently to the P40 tier hierarchy.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Ostrom, E. (2005). *Understanding Institutional Diversity*. Princeton University Press.
- Streeck, W., & Thelen, K. (eds.) (2005). *Beyond Continuity: Institutional Change in Advanced Political Economies*. Oxford University Press.
- Mahoney, J., & Thelen, K. (eds.) (2010). *Explaining Institutional Change: Ambiguity, Agency, and Power*. Cambridge University Press.
- Committee of Wise Men (2001). *Final Report of the Committee of Wise Men on the Regulation of European Securities Markets* (the Lamfalussy Report). European Commission.
- United States Congress (2010). *Dodd-Frank Wall Street Reform and Consumer Protection Act*, Pub. L. 111-203.
- European Union (2014). *Directive 2014/65/EU on markets in financial instruments (MiFID II)*. Official Journal of the European Union.
- Brennan, G., & Buchanan, J. M. (1985). *The Reason of Rules: Constitutional Political Economy*. Cambridge University Press.

## 11. Commit protocol

Commits from this project use the scope `p41`:

```text
docs(p41): decompose amendment procedure into separable properties
docs(p41): populate per-tier amendment properties from primary instruments
docs(p41): record the gap between nominal and effective amendment procedures
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
