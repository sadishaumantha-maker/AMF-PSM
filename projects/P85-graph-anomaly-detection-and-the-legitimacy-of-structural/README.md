# P85 - Graph anomaly detection and the legitimacy of structural outlier claims

**Track O - Market Abuse and Forensic Network Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Network scientist |
| **Upstream** | Discussion 4.2; P26 null models |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

P26 gives the framework null models, which makes it possible to say a structure is unusual. That capability is one short step from saying a structure is *suspicious*, and the step is not justified. Unusual is a statistical statement about a null; suspicious is a claim about intent. Without a written rule the first will be reported as the second.

## 2. Purpose

Define what an outlier claim means in this framework, bound it to the null model that produced it, and forbid the inferential step to intent.

## 3. Scope

**In scope**

- A formal statement of an outlier claim relative to a named null.
- The multiple-comparisons problem across seven systems and several statistics.
- A reporting rule binding every outlier claim to its null and its comparison count.

**Out of scope**

- Any inference from structural unusualness to conduct or intent.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the claim form: this statistic is at this percentile of this null distribution, computed over this many comparisons.
2. Address multiplicity directly. With seven systems and several statistics, testing everything guarantees extreme values somewhere; report the comparison count with every claim or the percentile is meaningless.
3. Draw on the research-integrity literature on why unadjusted multiple comparisons manufacture findings; the mechanism is identical here.
4. Forbid the step to intent in writing, and give the reason: a structure can be unusual for a hundred legitimate reasons, and the framework observes none of them.
5. Require the null model's identity to travel with the claim, since 'unusual' is undefined without it.
6. Add a worked example showing the same structure being unusual under one null and ordinary under another.

## 5. Task board

- [ ] Formalise the outlier claim relative to a named null.
- [ ] Treat the multiplicity problem explicitly.
- [ ] Write the no-intent-inference rule.
- [ ] Require null identity and comparison count in every claim.
- [ ] Build the two-null worked example.
- [ ] Publish `docs/graph/outlier_claims.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** State the claim form and the multiplicity correction the framework will use.
- **Inputs:** P26's null models.
- **Output artifact:** A formal claim specification.
- **Stop condition:** Every element of the claim form is defined, including the comparison count.

### `benchmark-runner`

- **Mandate:** Build the worked example where the verdict flips between two nulls.
- **Inputs:** Two null models and a constructed market.
- **Output artifact:** A demonstration with seeds.
- **Stop condition:** The flip is demonstrated and reproducible.

### `red-team-critic`

- **Mandate:** Attempt to report an outlier as evidence of misconduct and show what stops it.
- **Inputs:** The draft rules.
- **Output artifact:** An inference-step report.
- **Stop condition:** The rules block the step explicitly.

**Hand-off order:** `math-formalizer` -> `benchmark-runner` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-ensemble-stats` | A percentile is reported | Applies the documented estimator and seeded intervals. |
| `amf-graph-algorithm` | A structural statistic is computed | Verifies it and records the null it is compared against. |
| `amf-red-team` | An outlier claim is drafted | Tests whether it can be read as an allegation. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/graph/outlier_claims.md`
- A formal claim specification
- A two-null worked example
- A no-intent-inference rule

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every outlier claim names its null and its comparison count.
- [ ] The multiplicity problem is addressed with a stated correction.
- [ ] The worked example demonstrates a verdict flipping between nulls.
- [ ] The inference to intent is forbidden in writing.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Akoglu, L., Tong, H., & Koutra, D. (2015). "Graph based anomaly detection and description: a survey." *Data Mining and Knowledge Discovery* 29(3), 626-688.
- Chandola, V., Banerjee, A., & Kumar, V. (2009). "Anomaly detection: A survey." *ACM Computing Surveys* 41(3), 15.
- Gelman, A., & Loken, E. (2014). "The Statistical Crisis in Science." *American Scientist* 102(6), 460-465.
- Ioannidis, J. P. A. (2005). "Why Most Published Research Findings Are False." *PLoS Medicine* 2(8), e124.
- Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.
- Efron, B., & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall/CRC.
- Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). "The preregistration revolution." *PNAS* 115(11), 2600-2606.

## 11. Commit protocol

Commits from this project use the scope `p85`:

```text
docs(p85): formalise structural outlier claims against a named null
test(p85): demonstrate an outlier verdict flipping between null models
docs(p85): forbid inference from structural unusualness to intent
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

