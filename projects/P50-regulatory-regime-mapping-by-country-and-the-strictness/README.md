# P50 - Regulatory regime mapping by country and the strictness problem

**Track H - Global Market Mapping, Taxonomy & Standards**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Comparative regulation researcher |
| **Upstream** | issue #126 (25c); Discussion 2.3 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The task asks how to represent regulatory strictness dimensionlessly and how to encode whether rules are enforced consistently. A single strictness score would compress incommensurable dimensions into one number, and enforcement consistency is precisely what a rules-on-paper reading cannot see.

## 2. Purpose

Build a multi-dimensional regime profile per jurisdiction that keeps incommensurable dimensions separate, and represent enforcement discretion as an explicit dimension rather than an unstated caveat.

## 3. Scope

**In scope**

- A per-jurisdiction profile across separate, named dimensions.
- An explicit enforcement-discretion dimension with a sourced basis.
- A link from each profile to the P40 policy tiers.

**Out of scope**

- A single composite strictness score.
- Any assessment of whether a jurisdiction's regulation is good.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Refuse the single score explicitly and record why: the dimensions are incommensurable and a composite would hide the trade-offs.
2. Select dimensions with published measurement bases: disclosure requirements, supervisory powers, investor-protection provisions, capital-account openness, and enforcement record.
3. For enforcement, use published assessment programmes rather than inferring from statute; official-sector stability assessments exist precisely to evaluate implementation rather than text.
4. Populate profiles for the jurisdictions in the P47 register, citing instrument and assessment sources per cell.
5. Link each dimension to the policy tier it belongs to, so the regime map and the policy stack are one model.
6. State the vintage of every source; regulatory regimes change and an undated profile is misleading.

## 5. Task board

- [ ] Record the refusal of a composite strictness score.
- [ ] Select dimensions with published measurement bases.
- [ ] Source the enforcement dimension from assessment programmes.
- [ ] Populate per-jurisdiction profiles with dated citations.
- [ ] Link dimensions to policy tiers.
- [ ] Publish `docs/taxonomies/regulatory_regimes.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `regime-comparativist`

- **Mandate:** Populate per-jurisdiction profiles with instrument and assessment citations and vintages.
- **Inputs:** Official texts and assessment reports.
- **Output artifact:** `docs/taxonomies/_data/regime_profiles.md`.
- **Stop condition:** Every cell carries a source and a vintage.

### `literature-scout`

- **Mandate:** Identify published measurement bases for each dimension, including enforcement.
- **Inputs:** The reading list.
- **Output artifact:** A measurement-basis table.
- **Stop condition:** Enforcement has a source that assesses implementation, not statute text.

### `spec-drafter`

- **Mandate:** Write the refusal of the composite score and the tier linkage.
- **Inputs:** Profiles and tier hierarchy.
- **Output artifact:** `docs/taxonomies/regulatory_regimes.md`.
- **Stop condition:** The refusal is argued, not asserted, and every dimension maps to a tier.

### `red-team-critic`

- **Mandate:** Attempt to collapse the profile into a ranking and show what is lost.
- **Inputs:** The profiles.
- **Output artifact:** A collapse-loss demonstration.
- **Stop condition:** The demonstration shows a concrete pair of jurisdictions the ranking would misorder.

**Hand-off order:** `regime-comparativist` -> `literature-scout` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | A jurisdiction profile is built | Produces the dimensional profile with per-cell source and vintage. |
| `amf-source-vetting` | An enforcement source is proposed | Requires an implementation assessment rather than statute text. |
| `amf-taxonomy-builder` | The profile table is assembled | Builds it with citations and links each dimension to its policy tier. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/taxonomies/regulatory_regimes.md`
- Per-jurisdiction dimensional profiles
- An enforcement-discretion dimension
- A tier linkage

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] No composite strictness score is produced, and the refusal is argued.
- [ ] Every profile cell carries a source and a vintage.
- [ ] Enforcement is sourced from implementation assessments.
- [ ] Every dimension links to a policy tier from P40.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Kaufmann, D., Kraay, A., & Mastruzzi, M. (2010). "The Worldwide Governance Indicators: Methodology and Analytical Issues." World Bank Policy Research Working Paper 5430.
- La Porta, R., Lopez-de-Silanes, F., Shleifer, A., & Vishny, R. W. (1998). "Law and Finance." *Journal of Political Economy* 106(6), 1113-1155.
- Djankov, S., La Porta, R., Lopez-de-Silanes, F., & Shleifer, A. (2008). "The law and economics of self-dealing." *Journal of Financial Economics* 88(3), 430-465.
- International Monetary Fund & World Bank. *Financial Sector Assessment Program (FSAP)* methodology and Financial System Stability Assessments.
- Basel Committee on Banking Supervision (2011). *Basel III: A global regulatory framework for more resilient banks and banking systems* (rev. June 2011). Bank for International Settlements.
- European Union (2014). *Directive 2014/65/EU on markets in financial instruments (MiFID II)*. Official Journal of the European Union.
- OECD & European Commission JRC (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD Publishing.
- Obstfeld, M., Shambaugh, J. C., & Taylor, A. M. (2005). "The Trilemma in History: Tradeoffs Among Exchange Rates, Monetary Policies, and Capital Mobility." *Review of Economics and Statistics* 87(3), 423-438.

## 11. Commit protocol

Commits from this project use the scope `p50`:

```text
docs(p50): refuse a composite strictness score and argue why
docs(p50): populate dated per-jurisdiction regulatory dimension profiles
docs(p50): link regime dimensions to the policy tier hierarchy
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

