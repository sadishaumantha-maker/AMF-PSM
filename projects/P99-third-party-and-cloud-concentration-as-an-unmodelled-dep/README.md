# P99 - Third-party and cloud concentration as an unmodelled dependency

**Track Q - Technology, Fintech and AI Risk**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Market structure researcher |
| **Upstream** | Discussion 6.2; `SystemKind.skeleton` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Market participants increasingly depend on a small number of shared technology providers. Those providers are not market participants, so they appear nowhere in the seven systems, yet a failure at one would affect many systems simultaneously. The framework's dependency graph has no vertex for something that is not part of the market but on which the market depends.

## 2. Purpose

Decide how a non-market dependency is represented - a system component, an exogenous influence, or a new vertex type - and state what its absence currently costs.

## 3. Scope

**In scope**

- A characterisation of the non-market shared dependency.
- Three candidate representations assessed against the model.
- A statement of the simultaneity problem the current model cannot express.

**Out of scope**

- Naming any provider.
- Assessing any real concentration level.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the structural problem precisely: a single external failure that hits several systems at once is a *common-mode* event, and the coupling matrix propagates stress between systems rather than injecting it into several at once.
2. Note that `Shock` targets one system, so the framework cannot currently express a simultaneous multi-system shock at all - which is a finding independent of cloud providers.
3. Assess the three representations: a component inside each dependent system, an exogenous influence under P82's convention, or a genuine extension allowing multi-target shocks.
4. The third is the most invasive and possibly the most correct; argue it properly rather than dismissing it on cost.
5. Connect to P97 - shared providers are a monoculture, so the two charters describe one mechanism from different directions.
6. Draw on the operational-resilience standards, which treat third-party dependence as a first-class supervisory concern with published expectations.

## 5. Task board

- [ ] State the common-mode simultaneity problem.
- [ ] Confirm `Shock` cannot express a multi-system injection.
- [ ] Assess the three representations.
- [ ] Argue the multi-target shock extension properly.
- [ ] Reconcile with P97.
- [ ] Publish `docs/taxonomies/third_party_dependence.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** Express the common-mode event and show whether the current `Shock` type can represent it.
- **Inputs:** `models.py`, `simulation.py`.
- **Output artifact:** A formal statement.
- **Stop condition:** The representability of a simultaneous multi-system shock is settled.

### `literature-scout`

- **Mandate:** Establish the operational-resilience expectations from official-sector publications.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary.
- **Stop condition:** Third-party dependence is sourced from published supervisory expectations.

### `spec-drafter`

- **Mandate:** Assess the three representations and argue the invasive one fairly.
- **Inputs:** The formal statement.
- **Output artifact:** `docs/taxonomies/third_party_dependence.md`.
- **Stop condition:** The multi-target extension is argued on merit, not dismissed on cost.

### `boundary-sentinel`

- **Mandate:** Ensure no representation names a provider or requires market data.
- **Inputs:** The proposals.
- **Output artifact:** A boundary report.
- **Stop condition:** No provider is named and all constructs are structural.

**Hand-off order:** `math-formalizer` -> `literature-scout` -> `spec-drafter` -> `boundary-sentinel`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-invariant-spec` | Shock semantics are examined | States what `Shock` can and cannot express, as a tested invariant. |
| `amf-taxonomy-builder` | Dependence types are catalogued | Builds the table with official-source citations. |
| `amf-red-team` | A representation is chosen | Constructs a common-mode scenario the choice cannot express. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/taxonomies/third_party_dependence.md`
- A formal common-mode statement
- A three-way representation assessment
- A stated cost of the current absence

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Whether `Shock` can express a simultaneous multi-system injection is settled formally.
- [ ] The multi-target extension is argued on merit.
- [ ] The treatment is reconciled with P97's monoculture mechanism.
- [ ] No provider is named and no construct requires market data.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Financial Stability Board (2020). *Regulatory and Supervisory Issues Relating to Outsourcing and Third-Party Relationships*.
- Basel Committee on Banking Supervision (2021). *Principles for Operational Resilience*. Bank for International Settlements.
- CPMI-IOSCO (2012). *Principles for Financial Market Infrastructures*. Bank for International Settlements & IOSCO.
- Perrow, C. (1984). *Normal Accidents: Living with High-Risk Technologies*. Princeton University Press.
- Nygard, M. T. (2018). *Release It! Design and Deploy Production-Ready Software* (2nd ed.). Pragmatic Bookshelf.
- Kitano, H. (2004). "Biological robustness." *Nature Reviews Genetics* 5, 826-837.
- Wagner, W. (2011). "Systemic Liquidation Risk and the Diversity-Diversification Trade-Off." *Journal of Finance* 66(4), 1141-1175.
- Albert, R., Jeong, H., & Barabasi, A.-L. (2000). "Error and attack tolerance of complex networks." *Nature* 406, 378-382.

## 11. Commit protocol

Commits from this project use the scope `p99`:

```text
docs(p99): express third-party failure as a common-mode multi-system event
docs(p99): settle whether Shock can express a simultaneous injection
docs(p99): assess three representations of non-market dependence
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

