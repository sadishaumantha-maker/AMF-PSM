# P86 - Digit-distribution screening: scope, assumptions and misuse

**Track O - Market Abuse and Forensic Network Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Forensic research analyst |
| **Upstream** | Discussion 4.2; P54 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Digit-distribution screening is the most frequently proposed forensic technique and the most frequently misapplied. It has real assumptions - the data must span orders of magnitude and arise from a multiplicative process - and the framework's quantities are dimensionless structural measures in `[0, 1]`, which violate those assumptions outright. Proposing it here would be method-shaped decoration.

## 2. Purpose

Rule on whether any digit-distribution technique applies to AMF quantities, and record the reasoning so the proposal is not repeated without new grounds.

## 3. Scope

**In scope**

- A statement of the technique's assumptions from primary sources.
- A test of those assumptions against AMF's quantity types.
- A ruling and a precedent record.

**Out of scope**

- Applying the technique to accounting data the framework does not hold.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the assumptions from the originating work rather than from a practitioner guide, since the practitioner literature routinely omits them.
2. Test each against AMF quantities: metrics bounded in `[0, 1]`, weights in `(0, 1]`, and scores that are normalised composites. Bounded, normalised quantities do not span orders of magnitude.
3. Rule. The expected answer is that the technique does not apply, and a clean negative is a useful result.
4. If any AMF quantity does satisfy the assumptions, say so precisely and scope the technique to that quantity alone.
5. Record the ruling as a precedent so the proposal is evaluated against it next time rather than re-argued.
6. Note the general lesson for the framework: a technique's popularity is not evidence of its applicability.

## 5. Task board

- [ ] State the assumptions from primary sources.
- [ ] Test them against each AMF quantity type.
- [ ] Rule on applicability.
- [ ] Scope any surviving application precisely.
- [ ] Record the precedent.
- [ ] Publish `docs/research/digit_screening.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Recover the technique's assumptions from the originating work.
- **Inputs:** The reading list.
- **Output artifact:** An assumption statement with citations.
- **Stop condition:** The assumptions come from the primary source, not a practitioner guide.

### `math-formalizer`

- **Mandate:** Test each assumption against AMF's quantity types.
- **Inputs:** `models.py`, `systems.py`.
- **Output artifact:** A per-quantity applicability table.
- **Stop condition:** Every quantity type has a verdict.

### `spec-drafter`

- **Mandate:** Rule and record the precedent.
- **Inputs:** The applicability table.
- **Output artifact:** `docs/research/digit_screening.md`.
- **Stop condition:** The precedent states the grounds on which the proposal could be reopened.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `spec-drafter`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-source-vetting` | A forensic technique is proposed | Requires the originating work and its stated assumptions. |
| `amf-doc-page` | A negative result is published | Enforces the negative-result and documentation conventions. |
| `amf-red-team` | A ruling is drafted | Argues the technique does apply and forces the assumptions to answer. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/research/digit_screening.md`
- An assumption statement
- A per-quantity applicability table
- A recorded precedent

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Assumptions are quoted from the originating work.
- [ ] Every AMF quantity type has an applicability verdict.
- [ ] The ruling states the grounds for reopening it.
- [ ] A negative result, if that is the outcome, is published as a finding.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Newcomb, S. (1881). "Note on the Frequency of Use of the Different Digits in Natural Numbers." *American Journal of Mathematics* 4(1), 39-40. (with Benford, F. (1938), *Proc. Amer. Phil. Soc.* 78, 551-572)
- Nigrini, M. J. (2012). *Benford's Law: Applications for Forensic Accounting, Auditing, and Fraud Detection*. Wiley.
- Beneish, M. D. (1999). "The Detection of Earnings Manipulation." *Financial Analysts Journal* 55(5), 24-36.
- Dechow, P. M., Ge, W., Larson, C. R., & Sloan, R. G. (2011). "Predicting Material Accounting Misstatements." *Contemporary Accounting Research* 28(1), 17-82.
- Ioannidis, J. P. A. (2005). "Why Most Published Research Findings Are False." *PLoS Medicine* 2(8), e124.
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.

## 11. Commit protocol

Commits from this project use the scope `p86`:

```text
docs(p86): recover the digit-screening assumptions from the primary source
docs(p86): test the assumptions against AMF quantity types and rule
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
