# P103 - Fragmentation and whether a split market is one market or two

**Track R - Geopolitics, Sanctions and Fragmentation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Comparative regulation researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 7.3; P48; P82 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Fragmentation is the process by which one market becomes several. The framework models one market with a fixed boundary and no way to represent a boundary changing. So the framework can represent the before and the after as two unrelated analyses, and cannot represent the transition at all - which is the part everyone actually cares about.

## 2. Purpose

Establish what the framework can say about fragmentation given a fixed boundary, and connect the answer to P79's structure-changing feedback problem, of which this is a special case.

## 3. Scope

**In scope**

- A structural characterisation of fragmentation as a boundary change.
- An assessment of what before-and-after comparison can and cannot show.
- A shared treatment with P79 rather than a duplicate one.

**Out of scope**

- Predicting fragmentation anywhere.
- Any position on whether fragmentation is good or bad.
- Trade or flow volumes.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Characterise fragmentation as a change in the boundary and in which dependencies cross it, using P82's boundary semantics as the base.
2. Recognise this is P79's problem again - the structure changes - and take that charter's comparative-statics ruling rather than reopening it.
3. Identify the one thing before-and-after comparison does show: which dependencies became cross-boundary, and therefore exogenous. That is a real structural finding and is worth stating.
4. State what it cannot show: the path, the timing and any feedback during the transition.
5. Use the official-sector work on geoeconomic fragmentation for the mechanism, and keep the treatment descriptive.
6. Coordinate vocabulary with P48's unit ruling; whether a fragment is a new market or a segment is exactly the question P48 settled.

## 5. Task board

- [ ] Characterise fragmentation as a boundary change.
- [ ] Adopt P79's comparative-statics ruling.
- [ ] State what before-and-after does show.
- [ ] State what it cannot show.
- [ ] Reconcile with P48's unit ruling.
- [ ] Publish `docs/policy/fragmentation.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** Characterise fragmentation using P82's boundary semantics and P79's ruling.
- **Inputs:** P48, P79, P82.
- **Output artifact:** `docs/policy/fragmentation.md`.
- **Stop condition:** No ruling already made by another charter is reopened.

### `regime-comparativist`

- **Mandate:** Document the divergence mechanisms from official-sector work.
- **Inputs:** Official publications.
- **Output artifact:** A mechanism table with citations.
- **Stop condition:** Every mechanism is cited and described without evaluation.

### `red-team-critic`

- **Mandate:** Check for any position on the desirability of fragmentation.
- **Inputs:** The draft.
- **Output artifact:** A neutrality critique.
- **Stop condition:** No sentence evaluates fragmentation.

**Hand-off order:** `spec-drafter` -> `regime-comparativist` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | Divergence is documented | Records the instruments and vintages. |
| `amf-taxonomy-builder` | Fragments are classified | Applies P48's unit rule consistently. |
| `amf-red-team` | The document is drafted | Scans for evaluative and political content. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/fragmentation.md`
- A boundary-change characterisation
- A statement of what comparison shows and hides
- A mechanism table

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] P79's and P48's rulings are adopted rather than reopened.
- [ ] The cross-boundary dependency finding is stated as the real deliverable.
- [ ] The path limitation is stated as prominently.
- [ ] No sentence evaluates fragmentation.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- International Monetary Fund (2023). "Geoeconomic Fragmentation and the Future of Multilateralism." IMF Staff Discussion Note SDN/2023/001.
- Baldwin, R. (2016). *The Great Convergence: Information Technology and the New Globalization*. Harvard University Press.
- Farrell, H., & Newman, A. L. (2019). "Weaponized Interdependence: How Global Economic Networks Shape State Coercion." *International Security* 44(1), 42-79.
- Obstfeld, M., Shambaugh, J. C., & Taylor, A. M. (2005). "The Trilemma in History: Tradeoffs Among Exchange Rates, Monetary Policies, and Capital Mobility." *Review of Economics and Statistics* 87(3), 423-438.
- European Union (2014). *Directive 2014/65/EU on markets in financial instruments (MiFID II)*. Official Journal of the European Union.
- Committee of Wise Men (2001). *Final Report of the Committee of Wise Men on the Regulation of European Securities Markets* (the Lamfalussy Report). European Commission.
- Eichengreen, B. (2011). *Exorbitant Privilege: The Rise and Fall of the Dollar and the Future of the International Monetary System*. Oxford University Press.

## 11. Commit protocol

Commits from this project use the scope `p103`:

```text
docs(p103): characterise fragmentation as a change in the market boundary
docs(p103): state what before-and-after comparison shows and what it hides
docs(p103): reconcile the fragment unit with the atomic market ruling
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
