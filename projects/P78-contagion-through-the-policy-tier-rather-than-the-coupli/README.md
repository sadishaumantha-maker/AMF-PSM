# P78 - Contagion through the policy tier rather than the coupling graph

**Track N - Policy-Market Contagion and Systemic Indicators**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Policy researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 3.1 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The simulator propagates stress along dependency edges. The discussion observes that distress also travels through the *rulebook*: a supervisory action in one jurisdiction changes what participants elsewhere may do, with no dependency edge between them. If that channel is real, the framework's contagion model is structurally incomplete, and every resilience score understates transmission by an unknown amount.

## 2. Purpose

Establish whether policy-mediated contagion is representable in the seven-system model at all, and if so whether it is a new edge kind, a new system-level mechanism, or something the framework must decline to model.

## 3. Scope

**In scope**

- A structural characterisation of the policy channel: what carries the transmission and what receives it.
- An assessment against the existing `DependencyKind` vocabulary, `regulatory` in particular.
- A ruling: representable as an edge, representable only as a coupling-matrix modification, or out of scope.

**Out of scope**

- Estimating the size of any real-world policy spillover.
- Any quantity derived from market data.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Characterise the channel precisely. A rule change alters the admissible actions of everything bound by it, which is a change to *capacity*, not a flow of stress along a link - that distinction decides the modelling.
2. Test the existing vocabulary first: the schema already admits a `regulatory` dependency kind, so establish whether it already expresses this or expresses something else.
3. Consider the alternative that policy transmission is better modelled as a simultaneous change to several systems' absorptive capacity than as propagation, and argue both.
4. Use the institutional-change and contagion literature rather than reasoning from the framework outward; the mechanism is well studied even where the representation is not.
5. Rule, and state the consequence honestly - if the framework cannot represent this channel, every resilience score carries an unmodelled omission that must be documented.
6. Link the ruling to P40's tier hierarchy so the policy stack and the contagion model are one model.

## 5. Task board

- [ ] Characterise the policy transmission channel structurally.
- [ ] Test it against the existing `regulatory` dependency kind.
- [ ] Argue propagation versus simultaneous capacity change.
- [ ] Rule on representability.
- [ ] Document the omission if the ruling is out of scope.
- [ ] Publish `docs/policy/policy_contagion.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Collect the primary evidence on regulatory and supervisory spillover across jurisdictions.
- **Inputs:** The reading list.
- **Output artifact:** An annotated evidence table.
- **Stop condition:** The channel is documented from primary research, not asserted.

### `math-formalizer`

- **Mandate:** Express both candidate representations formally and identify what distinguishes them observationally.
- **Inputs:** The AMF model and the evidence.
- **Output artifact:** A formal comparison.
- **Stop condition:** The two representations are distinguishable by a stated test.

### `spec-drafter`

- **Mandate:** Rule and state the consequence for existing scores.
- **Inputs:** The comparison.
- **Output artifact:** `docs/policy/policy_contagion.md`.
- **Stop condition:** If the ruling is out of scope, the omission is stated in terms a reader of a resilience score would understand.

### `boundary-sentinel`

- **Mandate:** Verify no proposed mechanism requires market data.
- **Inputs:** The proposal.
- **Output artifact:** A boundary report.
- **Stop condition:** All quantities remain structural and dimensionless.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `spec-drafter` -> `boundary-sentinel`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | A jurisdiction's supervisory powers are cited | Produces the dated profile with instrument citations. |
| `amf-boundary-check` | A transmission mechanism is proposed | Runs the non-trading naming guard. |
| `amf-red-team` | A ruling is drafted | Argues the opposite representation and forces the evidence to answer. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/policy_contagion.md`
- An evidence table
- A formal comparison of the two representations
- A ruling with its consequence stated

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The channel is characterised from primary research.
- [ ] The two candidate representations are distinguishable by a stated test.
- [ ] The `regulatory` dependency kind is either shown to express this or shown not to.
- [ ] If out of scope, the omission is documented where a score reader will see it.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Allen, F., & Gale, D. (2000). "Financial Contagion." *Journal of Political Economy* 108(1), 1-33.
- Glasserman, P., & Young, H. P. (2016). "Contagion in Financial Networks." *Journal of Economic Literature* 54(3), 779-831.
- Streeck, W., & Thelen, K. (eds.) (2005). *Beyond Continuity: Institutional Change in Advanced Political Economies*. Oxford University Press.
- Committee of Wise Men (2001). *Final Report of the Committee of Wise Men on the Regulation of European Securities Markets* (the Lamfalussy Report). European Commission.
- Basel Committee on Banking Supervision (2011). *Basel III: A global regulatory framework for more resilient banks and banking systems* (rev. June 2011). Bank for International Settlements.
- Financial Stability Board (2010). *Reducing the moral hazard posed by systemically important financial institutions: FSB Recommendations and Time Lines*.
- Acemoglu, D., Ozdaglar, A., & Tahbaz-Salehi, A. (2015). "Systemic Risk and Stability in Financial Networks." *American Economic Review* 105(2), 564-608.
- International Monetary Fund (2023). "Geoeconomic Fragmentation and the Future of Multilateralism." IMF Staff Discussion Note SDN/2023/001.

## 11. Commit protocol

Commits from this project use the scope `p78`:

```text
docs(p78): characterise policy-mediated contagion structurally
docs(p78): compare edge-propagation against simultaneous capacity change
docs(p78): rule on representability and state the consequence for resilience scores
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

