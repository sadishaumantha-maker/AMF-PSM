# P102 - Central bank independence as an amendment-procedure property

**Track R - Geopolitics, Sanctions and Fragmentation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Policy researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 7.2 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Independence is usually discussed as a matter of degree and of practice, which makes it an assessment. The framework cannot make assessments about institutions. But independence has a precise structural component - who may amend the mandate, who may remove the officeholder, and by what procedure - which is exactly what P41 already decomposed for policy tiers generally.

## 2. Purpose

Represent independence as a structural property of the amendment and appointment procedures, and refuse the assessment component entirely.

## 3. Scope

**In scope**

- A structural definition from appointment, removal and mandate-amendment procedures.
- An explicit refusal of the practice component.
- Reuse of P41's amendment decomposition rather than a parallel vocabulary.

**Out of scope**

- Rating any central bank's independence.
- Any inflation, rate or market outcome data.
- Predicting political pressure.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Reuse P41's four properties - initiation, consent, latency and veto - applied to the mandate and to the appointment, rather than inventing a second scheme.
2. Read the classical time-inconsistency argument for why the procedure matters structurally; the case for independence rests on commitment, which is a property of how hard the rule is to change.
3. Refuse the practice component explicitly. Whether a formally independent institution is independent in practice is exactly the kind of assessment this framework does not make, and saying so protects the structural part.
4. Note the tension honestly: the empirical literature on independence and outcomes uses indices that blend formal and practice measures, so the framework's structural subset is not the same construct the literature studies.
5. Keep every treatment neutral and unnamed - the procedures can be described generically.
6. Feed the result into P50's regime profiles as a dimension rather than a standalone document.

## 5. Task board

- [ ] Apply P41's decomposition to mandate and appointment.
- [ ] Review the commitment argument from primary sources.
- [ ] Write the explicit refusal of the practice component.
- [ ] State the difference from the literature's indices.
- [ ] Feed the dimension into P50.
- [ ] Publish `docs/policy/independence_structure.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish the commitment argument and how published indices are constructed.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary including index construction.
- **Stop condition:** The blend of formal and practice components in published indices is stated.

### `regime-comparativist`

- **Mandate:** Apply P41's four properties to mandate and appointment procedures generically.
- **Inputs:** P41's decomposition.
- **Output artifact:** A property table.
- **Stop condition:** No specific institution is named or rated.

### `spec-drafter`

- **Mandate:** Write the refusal and the difference-from-literature statement.
- **Inputs:** The property table and summary.
- **Output artifact:** `docs/policy/independence_structure.md`.
- **Stop condition:** The refusal is explicit and the construct difference is stated.

**Hand-off order:** `literature-scout` -> `regime-comparativist` -> `spec-drafter`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | The dimension is added | Records it with instrument citations and vintage. |
| `amf-source-vetting` | An index is cited | Requires the methodology paper and records what it blends. |
| `amf-red-team` | The document is drafted | Scans for institutional rating and political content. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/independence_structure.md`
- A property table from P41's decomposition
- An explicit refusal of the practice component
- A P50 profile dimension

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The decomposition reuses P41 rather than a parallel scheme.
- [ ] The practice component is refused explicitly.
- [ ] The difference from published indices is stated.
- [ ] No institution is named or rated.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Kydland, F. E., & Prescott, E. C. (1977). "Rules Rather than Discretion: The Inconsistency of Optimal Plans." *Journal of Political Economy* 85(3), 473-491.
- Barro, R. J., & Gordon, D. B. (1983). "Rules, discretion and reputation in a model of monetary policy." *Journal of Monetary Economics* 12(1), 101-121.
- Alesina, A., & Summers, L. H. (1993). "Central Bank Independence and Macroeconomic Performance." *Journal of Money, Credit and Banking* 25(2), 151-162.
- Cukierman, A. (1992). *Central Bank Strategy, Credibility, and Independence: Theory and Evidence*. MIT Press.
- Blinder, A. S. (1998). *Central Banking in Theory and Practice*. MIT Press.
- Goodhart, C. A. E. (1988). *The Evolution of Central Banks*. MIT Press.
- Brennan, G., & Buchanan, J. M. (1985). *The Reason of Rules: Constitutional Political Economy*. Cambridge University Press.
- Ostrom, E. (2005). *Understanding Institutional Diversity*. Princeton University Press.

## 11. Commit protocol

Commits from this project use the scope `p102`:

```text
docs(p102): represent independence through amendment and appointment procedure
docs(p102): refuse the practice component and state why
docs(p102): add the structural dimension to the regime profiles
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
