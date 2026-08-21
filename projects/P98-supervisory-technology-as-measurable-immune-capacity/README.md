# P98 - Supervisory technology as measurable immune capacity

**Track Q - Technology, Fintech and AI Risk**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Policy researcher |
| **Upstream** | Discussion 6.2; PR #42 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The immune system is modelled as the rules that bind. A rule that cannot be monitored does not bind in practice, so supervisory capacity - the ability to observe compliance - is a precondition for the immune system working at all. The framework currently models the rule and not the capacity to enforce it, which means a jurisdiction with excellent rules and no supervision scores identically to one with both.

## 2. Purpose

Add supervisory capacity to the immune-system representation, or state clearly that immune scores measure rules on paper only.

## 3. Scope

**In scope**

- A structural characterisation of supervisory capacity.
- An assessment of whether it belongs to the immune or the nervous system.
- A ruling, with the paper-versus-practice consequence stated.

**Out of scope**

- Rating any supervisor's effectiveness.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Characterise capacity structurally: reporting obligations, data access, inspection powers and the existence of a monitoring function - all of which are properties of instruments, not judgements.
2. Decide the system. Monitoring is an information function, which argues for the nervous system; enforcement is a constraint function, which argues for the immune system. The split may be the honest answer.
3. Connect to P50, which already treats enforcement as a separate profile dimension sourced from implementation assessments; the two must not diverge.
4. State the consequence directly: without this, the immune score is a rules-on-paper measure, and that is what it should be called.
5. Rule, and if capacity is added, define it from instrument-derived properties only, never from an assessment of quality.
6. Keep the treatment neutral across jurisdictions.

## 5. Task board

- [ ] Characterise supervisory capacity from instrument properties.
- [ ] Decide immune, nervous, or split.
- [ ] Reconcile with P50's enforcement dimension.
- [ ] State the rules-on-paper consequence.
- [ ] Rule and define any added property.
- [ ] Publish `docs/policy/supervisory_capacity.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `regime-comparativist`

- **Mandate:** Derive capacity properties from instruments and implementation assessments.
- **Inputs:** Official texts and assessment reports.
- **Output artifact:** A capacity property table.
- **Stop condition:** Every property derives from an instrument or an assessment, not a judgement.

### `spec-drafter`

- **Mandate:** Decide the system placement and state the consequence.
- **Inputs:** The property table.
- **Output artifact:** `docs/policy/supervisory_capacity.md`.
- **Stop condition:** The placement decision is argued, including the split option.

### `red-team-critic`

- **Mandate:** Check no property amounts to rating a supervisor.
- **Inputs:** The draft.
- **Output artifact:** A neutrality critique.
- **Stop condition:** No jurisdiction or supervisor is rated.

**Hand-off order:** `regime-comparativist` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | Capacity is recorded | Cites the instrument and the implementation assessment with vintages. |
| `amf-boundary-check` | A capacity property is proposed | Runs the non-trading naming guard. |
| `amf-doc-page` | The consequence is published | Enforces documentation conventions and neutrality. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/supervisory_capacity.md`
- A capacity property table
- A system-placement decision
- A stated paper-versus-practice consequence

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every capacity property derives from an instrument or assessment.
- [ ] The placement decision argues the split option explicitly.
- [ ] The rules-on-paper consequence is stated where immune scores are read.
- [ ] No supervisor or jurisdiction is rated.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- International Monetary Fund & World Bank. *Financial Sector Assessment Program (FSAP)* methodology and Financial System Stability Assessments.
- Kaufmann, D., Kraay, A., & Mastruzzi, M. (2010). "The Worldwide Governance Indicators: Methodology and Analytical Issues." World Bank Policy Research Working Paper 5430.
- Carpenter, D., & Moss, D. A. (eds.) (2014). *Preventing Regulatory Capture: Special Interest Influence and How to Limit It*. Cambridge University Press.
- Arner, D. W., Barberis, J., & Buckley, R. P. (2017). "FinTech, RegTech, and the Reconceptualization of Financial Regulation." *Northwestern Journal of International Law & Business* 37(3), 371-413.
- Basel Committee on Banking Supervision (2011). *Basel III: A global regulatory framework for more resilient banks and banking systems* (rev. June 2011). Bank for International Settlements.
- CPMI-IOSCO (2012). *Principles for Financial Market Infrastructures*. Bank for International Settlements & IOSCO.
- Stigler, G. J. (1971). "The Theory of Economic Regulation." *Bell Journal of Economics and Management Science* 2(1), 3-21.

## 11. Commit protocol

Commits from this project use the scope `p98`:

```text
docs(p98): derive supervisory capacity from instrument properties
docs(p98): decide whether capacity is immune, nervous or split
docs(p98): state that immune scores measure rules on paper without it
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
