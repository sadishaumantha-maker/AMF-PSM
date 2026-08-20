# P45 - Government philosophy archetypes as structural regime types

**Track G - Policy Architecture & Regulatory Regimes**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Comparative political economist |
| **Upstream** | issues #134 (5.4), #135 (5.5), #136 (5.6) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The proposal names four archetypes - liberal, socialist, authoritarian, mixed economy - and asks that five to seven real governments be mapped onto them. Those labels are ideological categories, and mapping real states onto them invites political argument rather than structural analysis. The dispute is whether the archetypes should be ideological at all, or defined by structural properties the framework can see.

## 2. Purpose

Replace ideological labels with structural regime dimensions that are observable, citable and non-pejorative, and position real jurisdictions on those dimensions using published governance and legal indicators rather than judgement.

## 3. Scope

**In scope**

- A dimensional scheme replacing the four labels: for example state ownership share, regulatory discretion, judicial reviewability, capital-account openness.
- Positioning of a defined jurisdiction set using published indicators with sources.
- An explicit statement of what the scheme cannot capture.

**Out of scope**

- Ranking political systems as better or worse.
- Using any indicator whose methodology is not publicly documented.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State plainly why ideological labels are unsuitable: they are contested, they change meaning by country, and they are not observable properties.
2. Choose dimensions that are observable and have published measurement methodologies.
3. Use established governance and legal-institution indicators, citing their methodology papers rather than their headline scores alone.
4. Position the jurisdiction set on the dimensions, recording the indicator, vintage and source for every position.
5. State the scheme's blind spots explicitly - informal governance and enforcement discretion are the obvious ones.
6. Write the whole document so that no sentence could reasonably be read as a political judgement.

## 5. Task board

- [ ] Write the argument against ideological labels.
- [ ] Select structural dimensions with published methodologies.
- [ ] Position the jurisdiction set with cited indicators.
- [ ] Document the scheme's blind spots.
- [ ] Run a neutrality review over the full text.
- [ ] Publish `docs/taxonomies/government_philosophies.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Identify indicator sets with published, citable methodologies.
- **Inputs:** The reading list.
- **Output artifact:** An indicator methodology table.
- **Stop condition:** Every candidate indicator has a methodology citation.

### `regime-comparativist`

- **Mandate:** Position the jurisdiction set and record indicator, vintage and source per cell.
- **Inputs:** Selected indicators.
- **Output artifact:** A positioning table.
- **Stop condition:** No cell is populated without a source and a vintage.

### `spec-drafter`

- **Mandate:** Write the dimensional scheme and the blind-spot statement.
- **Inputs:** Indicator table and positions.
- **Output artifact:** `docs/taxonomies/government_philosophies.md`.
- **Stop condition:** No dimension is named with an ideological label.

### `red-team-critic`

- **Mandate:** Read the document adversarially for any sentence that reads as a political judgement.
- **Inputs:** The draft.
- **Output artifact:** A neutrality critique.
- **Stop condition:** No sentence survives as a political claim.

**Hand-off order:** `literature-scout` -> `regime-comparativist` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | A jurisdiction is positioned | Produces the profile with indicator, vintage and methodology citation. |
| `amf-source-vetting` | An indicator is proposed | Requires a published methodology, not a headline score. |
| `amf-red-team` | The document is drafted | Scans for political judgement and unsupported characterisation. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/taxonomies/government_philosophies.md`
- An indicator methodology table
- A cited positioning table
- A blind-spot statement

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] No dimension carries an ideological label.
- [ ] Every position cites an indicator, its vintage and its methodology.
- [ ] The blind-spot statement names informal governance and enforcement discretion explicitly.
- [ ] The neutrality review finds no political claim.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Kaufmann, D., Kraay, A., & Mastruzzi, M. (2010). "The Worldwide Governance Indicators: Methodology and Analytical Issues." World Bank Policy Research Working Paper 5430.
- La Porta, R., Lopez-de-Silanes, F., Shleifer, A., & Vishny, R. W. (1998). "Law and Finance." *Journal of Political Economy* 106(6), 1113-1155.
- Djankov, S., La Porta, R., Lopez-de-Silanes, F., & Shleifer, A. (2008). "The law and economics of self-dealing." *Journal of Financial Economics* 88(3), 430-465.
- Acemoglu, D., & Robinson, J. A. (2012). *Why Nations Fail: The Origins of Power, Prosperity, and Poverty*. Crown.
- North, D. C. (1990). *Institutions, Institutional Change and Economic Performance*. Cambridge University Press.
- Ostrom, E. (2005). *Understanding Institutional Diversity*. Princeton University Press.
- Obstfeld, M., Shambaugh, J. C., & Taylor, A. M. (2005). "The Trilemma in History: Tradeoffs Among Exchange Rates, Monetary Policies, and Capital Mobility." *Review of Economics and Statistics* 87(3), 423-438.
- Bowker, G. C., & Star, S. L. (1999). *Sorting Things Out: Classification and Its Consequences*. MIT Press.

## 11. Commit protocol

Commits from this project use the scope `p45`:

```text
docs(p45): replace ideological archetypes with observable structural dimensions
docs(p45): position jurisdictions using cited indicator methodologies
docs(p45): state what the regime scheme cannot capture
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
