# P115 - Q3 - Shannon entropy and the diagnostic index that is already an HHI

**Track T - The Promised Research Modules**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Information theorist |
| **Upstream** | `docs/discussions/README.md` module Q3 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Q3 proposes entropy measures for market structure. The framework already computes a concentration index - an HHI over outgoing dependency weights - and HHI is one member of a family that includes Shannon entropy and the Hill numbers, differing only in the order parameter. So Q3's real content is a decision the repository has already made implicitly and never justified: why order two rather than order one. The dispute is whether there is a reason for the current choice or only an inheritance.

## 2. Purpose

Place the framework's concentration measure in the Renyi/Hill family, state what changing the order would do to published scores, and rule on whether to change it.

## 3. Scope

**In scope**

- Shannon entropy, Renyi entropy and the Hill numbers stated exactly, with HHI located among them.
- A numerical comparison of concentration under orders 0, 1 and 2 on the sample market.
- A ruling on whether to change the order, with the score-movement consequence stated.
- Mutual information and transfer entropy assessed against what the framework can observe.

**Out of scope**

- Estimating entropy from any market data series.
- Changing `diagnostics.py` in this project - the ruling is written first, implementation is a separate change.
- Channel-capacity claims about real markets.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the family from primary sources and locate HHI in it: HHI is the sum of squared shares, which is the exponential of the order-two Renyi entropy inverted, or equivalently Hill number two. Shannon is the limiting order-one case. Write the identity out rather than asserting the relationship.
2. Compute the comparison on `examples/sample_market.json` and report the numbers, so the ruling turns on evidence rather than taste.
3. State the qualitative difference: order two weights the largest share heavily and is insensitive to the tail, while order one weights all shares by their information content. Which is right depends on whether a market is fragile because of its biggest coupling or because of the shape of the whole distribution.
4. Rule, and state the consequence. Changing the order moves every published concentration score, which is exactly the consideration that kept `scale_concentration_by_reliance` off by default - apply the same standard.
5. Assess transfer entropy honestly: it requires a time series, the framework has a structural snapshot, so it is not computable here. Say that rather than listing it as future work.
6. Keep the module free of any claim that entropy measures predict anything.

## 5. Task board

- [ ] State the Renyi/Hill family and locate HHI exactly.
- [ ] Compute orders 0, 1 and 2 on the sample market.
- [ ] State the qualitative difference between orders.
- [ ] Rule on the order, with the score-movement consequence.
- [ ] Assess mutual information and transfer entropy against available observables.
- [ ] Publish `docs/discussions/Q3-shannon-information-market-entropy.md` and relink it.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** Write the identity locating HHI in the Renyi/Hill family exactly.
- **Inputs:** `diagnostics.py`, the primary sources.
- **Output artifact:** A derivation note.
- **Stop condition:** The identity is written out, not cited as folklore.

### `benchmark-runner`

- **Mandate:** Compute concentration at orders 0, 1 and 2 on the sample market and report reproduction commands.
- **Inputs:** `examples/sample_market.json`.
- **Output artifact:** A comparison table with commands.
- **Stop condition:** Every number is reproducible from the stated command.

### `spec-drafter`

- **Mandate:** Write the ruling with its score-movement consequence stated.
- **Inputs:** The derivation and comparison.
- **Output artifact:** A ruling section.
- **Stop condition:** The consequence for published scores is quantified, not described.

### `literature-scout`

- **Mandate:** Assemble the information-theory primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated bibliography.
- **Stop condition:** Shannon 1948 is cited for entropy, not a textbook restatement.

### `red-team-critic`

- **Mandate:** Attack any suggestion that an entropy measure here says something predictive.
- **Inputs:** The draft.
- **Output artifact:** An adversarial report.
- **Stop condition:** No sentence claims predictive content.

**Hand-off order:** `math-formalizer` -> `benchmark-runner` -> `spec-drafter` -> `literature-scout` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-invariant-spec` | The family identity is derived | Records the identity and the range each measure occupies. |
| `amf-literature-brief` | The sources are assembled | Produces the annotated brief. |
| `amf-doc-page` | The module is published | Enforces conventions and disclaimers. |
| `amf-red-team` | The ruling is drafted | Scans for predictive claims and unstated consequences. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/discussions/Q3-shannon-information-market-entropy.md`
- The Renyi/Hill identity for HHI
- A reproducible order comparison on the sample market
- A ruling on the order parameter

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] HHI is located in the family by an explicit identity.
- [ ] The comparison table is reproducible from stated commands.
- [ ] The ruling states the movement it would cause in published scores.
- [ ] Transfer entropy is ruled non-computable here rather than deferred.
- [ ] The index link resolves.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Shannon, C. E. (1948). "A Mathematical Theory of Communication." *Bell System Technical Journal* 27(3), 379-423.
- Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley.
- MacKay, D. J. C. (2003). *Information Theory, Inference, and Learning Algorithms*. Cambridge University Press.
- Jaynes, E. T. (1957). "Information Theory and Statistical Mechanics." *Physical Review* 106(4), 620-630.
- Kullback, S., & Leibler, R. A. (1951). "On Information and Sufficiency." *Annals of Mathematical Statistics* 22(1), 79-86.
- Hill, M. O. (1973). "Diversity and Evenness: A Unifying Notation and Its Consequences." *Ecology* 54(2), 427-432.
- Schreiber, T. (2000). "Measuring Information Transfer." *Physical Review Letters* 85(2), 461-464.
- Tirole, J. (1988). *The Theory of Industrial Organization*. MIT Press.
- OECD & European Commission JRC (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD Publishing.
- Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., & Tarantola, S. (2008). *Global Sensitivity Analysis: The Primer*. Wiley.

## 11. Commit protocol

Commits from this project use the scope `p115`:

```text
docs(p115): locate the concentration index in the Renyi/Hill family
docs(p115): compare concentration at orders zero, one and two
docs(p115): publish the Q3 module and rule on the order parameter
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

