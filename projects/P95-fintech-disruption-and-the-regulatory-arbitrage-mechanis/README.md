# P95 - Fintech disruption and the regulatory-arbitrage mechanism

**Track Q - Technology, Fintech and AI Risk**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Comparative regulation researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 6.2 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

New entrants performing established functions under different rules is usually framed as innovation. The empirical literature frames a large part of it as regulatory arbitrage - the same function migrating to where the constraint binds least. Those two framings imply opposite things about resilience, and the framework's immune system cannot currently express either.

## 2. Purpose

Express the arbitrage mechanism structurally - as a shift in which policy tier binds a function - and give the framework a way to represent function migration across the perimeter.

## 3. Scope

**In scope**

- A structural expression of function migration between regulatory tiers.
- An assessment of what it does to the immune system's coverage.
- A test on documented migration episodes.

**Out of scope**

- Assessing any firm.
- Market-share, volume or valuation data.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Express migration as a change in which tier binds a function, holding the function constant. That framing is neutral between the innovation and arbitrage readings, which is why it is the right one for a structural model.
2. Assess the consequence: if a function migrates to a tier that binds less, the immune system's effective coverage falls without any rule changing, which is a resilience change the current model cannot see.
3. Test on documented episodes where the empirical work has identified the mechanism.
4. Note that the same mechanism drives P89's shadow intermediation, and keep the two vocabularies consistent.
5. Rule on representation: a per-function tier assignment is the minimal change, and its cost should be stated.
6. Keep the treatment neutral between innovation and arbitrage; the framework observes the tier, not the motive.

## 5. Task board

- [ ] Express migration as a tier reassignment.
- [ ] Assess the effect on immune coverage.
- [ ] Test on documented episodes.
- [ ] Reconcile vocabulary with P89.
- [ ] Rule on representation and state its cost.
- [ ] Publish `docs/policy/function_migration.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish the arbitrage mechanism from peer-reviewed empirical work.
- **Inputs:** The reading list.
- **Output artifact:** An annotated evidence table.
- **Stop condition:** The mechanism is evidenced, not assumed.

### `spec-drafter`

- **Mandate:** Express migration structurally and rule on representation.
- **Inputs:** The evidence and the tier hierarchy.
- **Output artifact:** `docs/policy/function_migration.md`.
- **Stop condition:** The expression is neutral between the two framings.

### `regime-comparativist`

- **Mandate:** Document the tier that binds each migrating function, with citations.
- **Inputs:** Official instruments.
- **Output artifact:** A function-to-tier table.
- **Stop condition:** Every assignment cites an instrument.

### `boundary-sentinel`

- **Mandate:** Reject market-share, volume and valuation quantities.
- **Inputs:** The proposals.
- **Output artifact:** A boundary report.
- **Stop condition:** Only structural constructs survive.

**Hand-off order:** `literature-scout` -> `spec-drafter` -> `regime-comparativist` -> `boundary-sentinel`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | A function's binding tier is recorded | Cites the instrument and its scope. |
| `amf-boundary-check` | A migration construct is proposed | Rejects market-data quantities. |
| `amf-taxonomy-builder` | The function-to-tier table is built | Builds it with citations and an exclusion list. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/function_migration.md`
- An evidence table
- A function-to-tier table
- A representation ruling with its cost

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The expression is neutral between innovation and arbitrage framings.
- [ ] The effect on immune coverage is stated.
- [ ] Every tier assignment cites an instrument.
- [ ] The vocabulary is consistent with P89.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Buchak, G., Matvos, G., Piskorski, T., & Seru, A. (2018). "Fintech, regulatory arbitrage, and the rise of shadow banks." *Journal of Financial Economics* 130(3), 453-483.
- Philippon, T. (2016). "The FinTech Opportunity." NBER Working Paper 22476.
- Fuster, A., Plosser, M., Schnabl, P., & Vickery, J. (2019). "The Role of Technology in Mortgage Lending." *Review of Financial Studies* 32(5), 1854-1899.
- Arner, D. W., Barberis, J., & Buckley, R. P. (2017). "FinTech, RegTech, and the Reconceptualization of Financial Regulation." *Northwestern Journal of International Law & Business* 37(3), 371-413.
- Stigler, G. J. (1971). "The Theory of Economic Regulation." *Bell Journal of Economics and Management Science* 2(1), 3-21.
- Pozsar, Z., Adrian, T., Ashcraft, A., & Boesky, H. (2013). "Shadow Banking." *FRBNY Economic Policy Review* 19(2), 1-16.
- Committee of Wise Men (2001). *Final Report of the Committee of Wise Men on the Regulation of European Securities Markets* (the Lamfalussy Report). European Commission.
- European Union (2014). *Directive 2014/65/EU on markets in financial instruments (MiFID II)*. Official Journal of the European Union.

## 11. Commit protocol

Commits from this project use the scope `p95`:

```text
docs(p95): express function migration as a change in binding tier
docs(p95): document the tier binding each migrating function
docs(p95): rule on representing migration and state its cost
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
