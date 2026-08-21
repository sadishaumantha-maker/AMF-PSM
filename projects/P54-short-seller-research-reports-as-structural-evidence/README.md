# P54 - Short-seller research reports as structural evidence

**Track I - Empirical Case Studies & Forensic Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Forensic research analyst |
| **Upstream** | issues #131-#133 (5.1-5.3, #28) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The backlog proposes studying a well-known activist short-seller report to identify frauds and scams. That framing has two problems: an activist report is an interested party's document, not a finding, and 'identifying frauds' invites accusations the repository is not positioned to make. What the framework can legitimately extract is the *structural conditions* such reports allege, and whether AMF can represent them.

## 2. Purpose

Reframe the task from fraud identification to structural-condition extraction: what structural weaknesses do activist reports typically allege, which of those are representable in AMF, and which are outside its scope.

## 3. Scope

**In scope**

- A taxonomy of structural allegations found in activist research: related-party dependency, opaque intermediation, concentrated control, auditor and regulator dependency.
- A representability assessment against the AMF seven-system model.
- A strict evidentiary rule: allegations are recorded as allegations, with their disposition where known.

**Out of scope**

- Asserting that any named entity committed fraud.
- Reproducing accusations without their subsequent regulatory or judicial disposition.
- Any price, return or trading-related quantity.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the evidentiary rule first and enforce it in every sentence: an allegation is an allegation until a regulator or court says otherwise, and the disposition must be recorded alongside it.
2. Use the forensic-accounting literature to build the structural-allegation taxonomy, rather than deriving categories from a single report.
3. For each category, ask whether AMF can represent it: related-party dependency is a graph edge, auditor dependency is a nervous-system property, concentrated control is a concentration score.
4. Where a category is not representable, say so plainly; that is the more useful finding for the framework.
5. Cross-reference the whistleblower and enforcement-outcome literature to note base rates: most allegations are not upheld, and a case file that omits that is misleading.
6. Have the red-team critic read the file specifically for defamation risk before it is committed.

## 5. Task board

- [ ] Write and enforce the evidentiary rule.
- [ ] Build the structural-allegation taxonomy from the forensic literature.
- [ ] Assess AMF representability per category.
- [ ] Record dispositions for every allegation cited.
- [ ] Run the defamation-risk review.
- [ ] Publish `docs/case_studies/activist_research_structure.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Build the structural-allegation taxonomy from peer-reviewed forensic-accounting research.
- **Inputs:** The reading list.
- **Output artifact:** An annotated taxonomy.
- **Stop condition:** Categories derive from published research, not from one report.

### `case-study-archivist`

- **Mandate:** Record each cited allegation with its regulatory or judicial disposition.
- **Inputs:** Official filings and enforcement records.
- **Output artifact:** A dated allegation-and-disposition table.
- **Stop condition:** No allegation appears without its disposition or an explicit `undetermined` marker.

### `spec-drafter`

- **Mandate:** Assess AMF representability per allegation category.
- **Inputs:** Taxonomy and the seven-system model.
- **Output artifact:** A representability table.
- **Stop condition:** Every category is marked representable, partial or out of scope.

### `red-team-critic`

- **Mandate:** Read the file for defamation risk and unstated accusation.
- **Inputs:** The draft.
- **Output artifact:** A risk report.
- **Stop condition:** No sentence asserts wrongdoing by a named entity.

**Hand-off order:** `literature-scout` -> `case-study-archivist` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-case-dossier` | The case file is assembled | Applies the protocol and enforces the allegation-plus-disposition rule. |
| `amf-source-vetting` | An activist report is cited | Marks it as an interested-party document and requires a corroborating official source. |
| `amf-red-team` | Before the file is committed | Runs the defamation-risk and accusation scan. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/case_studies/activist_research_structure.md`
- A structural-allegation taxonomy
- An allegation-and-disposition table
- A representability assessment

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] No sentence asserts that a named entity committed fraud.
- [ ] Every cited allegation carries its disposition or an explicit undetermined marker.
- [ ] Allegation categories derive from peer-reviewed research.
- [ ] Every category is marked representable, partial or out of scope.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Beneish, M. D. (1999). "The Detection of Earnings Manipulation." *Financial Analysts Journal* 55(5), 24-36.
- Dechow, P. M., Ge, W., Larson, C. R., & Sloan, R. G. (2011). "Predicting Material Accounting Misstatements." *Contemporary Accounting Research* 28(1), 17-82.
- Dyck, A., Morse, A., & Zingales, L. (2010). "Who Blows the Whistle on Corporate Fraud?" *Journal of Finance* 65(6), 2213-2253.
- Karpoff, J. M., Lee, D. S., & Martin, G. S. (2008). "The Cost to Firms of Cooking the Books." *Journal of Financial and Quantitative Analysis* 43(3), 581-611.
- Nigrini, M. J. (2012). *Benford's Law: Applications for Forensic Accounting, Auditing, and Fraud Detection*. Wiley.
- Akoglu, L., Tong, H., & Koutra, D. (2015). "Graph based anomaly detection and description: a survey." *Data Mining and Knowledge Discovery* 29(3), 626-688.
- European Union (2014). *Regulation (EU) No 596/2014 on market abuse (Market Abuse Regulation)*. Official Journal of the European Union.
- Chandola, V., Banerjee, A., & Kumar, V. (2009). "Anomaly detection: A survey." *ACM Computing Surveys* 41(3), 15.

## 11. Commit protocol

Commits from this project use the scope `p54`:

```text
docs(p54): reframe activist research as structural-allegation evidence
docs(p54): record allegations with their regulatory dispositions
docs(p54): assess AMF representability per allegation category
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
