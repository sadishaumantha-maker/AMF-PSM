# P90 - Sudden stops and capital flight as structural withdrawal

**Track P - Shadow Finance, Capital Flows and Currency**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Emerging markets researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 5.3; P57 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

A sudden stop is usually described in flow terms - capital arrives, then does not. The framework cannot see flows. What it can potentially see is the structural precondition: a funding dependency on a source outside the boundary with no domestic substitute. Whether that structural reading captures enough of the phenomenon to be worth having is unsettled.

## 2. Purpose

Develop the structural reading of a sudden stop, test it against the documented episodes, and rule on whether it earns a place or merely renames something the framework already computes.

## 3. Scope

**In scope**

- A structural definition: external funding dependency without substitutable domestic capacity.
- A test against documented episodes for whether the structure was present beforehand.
- An overlap check against existing single-point-of-failure detection.

**Out of scope**

- Capital flow volumes, reserve levels or exchange rates.
- Predicting a stop in any real economy.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Define structurally: a circulatory dependency whose target lies outside the market boundary, where no in-boundary alternative exists at comparable weight.
2. Note immediately that this may be exactly what the articulation-point plus low-redundancy test already finds, and check that before building anything new.
3. Test against documented episodes from the primary literature: was the structural precondition present, and was it present in cases where no stop occurred? The second question is the one that matters and is usually skipped.
4. If the precondition is common and the event is rare, say so - that is a base-rate result of the kind P88 governs.
5. Rule on whether the construct adds anything beyond P30's SPOF detection.
6. Keep every observation structural; the temptation to reach for reserve adequacy ratios must be refused.

## 5. Task board

- [ ] Write the structural definition.
- [ ] Check overlap with existing SPOF detection first.
- [ ] Test presence and absence against documented episodes.
- [ ] Apply the base-rate treatment.
- [ ] Rule on whether it earns a place.
- [ ] Publish `docs/case_studies/sudden_stops.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish the sudden-stop mechanism from primary economic sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated mechanism summary.
- **Stop condition:** The mechanism is sourced, not paraphrased from memory.

### `case-study-archivist`

- **Mandate:** Assemble episodes including cases where the precondition held and no stop occurred.
- **Inputs:** Official records and peer-reviewed accounts.
- **Output artifact:** A dated episode table with both arms.
- **Stop condition:** The table includes non-events, not only events.

### `benchmark-runner`

- **Mandate:** Measure the overlap with existing SPOF detection on constructed markets.
- **Inputs:** Both constructs.
- **Output artifact:** An overlap table.
- **Stop condition:** The overlap is quantified across at least fifty markets.

### `boundary-sentinel`

- **Mandate:** Reject reserve, flow and exchange-rate quantities.
- **Inputs:** The proposals.
- **Output artifact:** A boundary report.
- **Stop condition:** Only structural constructs survive.

**Hand-off order:** `literature-scout` -> `case-study-archivist` -> `benchmark-runner` -> `boundary-sentinel`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-case-dossier` | Episodes are assembled | Applies the protocol and requires the non-event arm. |
| `amf-boundary-check` | A construct is proposed | Rejects flow, reserve and exchange-rate inputs. |
| `amf-sensitivity-design` | Overlap is measured | Designs the comparison and reports agreement across markets. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/case_studies/sudden_stops.md`
- A structural definition
- An episode table including non-events
- An overlap analysis against SPOF detection

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The overlap with existing SPOF detection is measured before anything new is built.
- [ ] The episode table includes cases where the precondition held and no event followed.
- [ ] The base-rate consequence is stated.
- [ ] No flow, reserve or exchange-rate quantity appears.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Calvo, G. A. (1998). "Capital Flows and Capital-Market Crises: The Simple Economics of Sudden Stops." *Journal of Applied Economics* 1(1), 35-54.
- Calvo, G. A., & Mendoza, E. G. (2000). "Rational contagion and the globalization of securities markets." *Journal of International Economics* 51(1), 79-113.
- Rey, H. (2015). "Dilemma not Trilemma: The Global Financial Cycle and Monetary Policy Independence." NBER Working Paper 21162.
- Obstfeld, M., Shambaugh, J. C., & Taylor, A. M. (2005). "The Trilemma in History: Tradeoffs Among Exchange Rates, Monetary Policies, and Capital Mobility." *Review of Economics and Statistics* 87(3), 423-438.
- Obstfeld, M. (1996). "Models of currency crises with self-fulfilling features." *European Economic Review* 40(3-5), 1037-1047.
- Morris, S., & Shin, H. S. (1998). "Unique Equilibrium in a Model of Self-Fulfilling Currency Attacks." *American Economic Review* 88(3), 587-597.
- Reinhart, C. M., & Rogoff, K. S. (2009). *This Time Is Different: Eight Centuries of Financial Folly*. Princeton University Press.
- Eichengreen, B. (2011). *Exorbitant Privilege: The Rise and Fall of the Dollar and the Future of the International Monetary System*. Oxford University Press.

## 11. Commit protocol

Commits from this project use the scope `p90`:

```text
docs(p90): define the sudden-stop precondition structurally
test(p90): measure overlap with existing single-point-of-failure detection
docs(p90): rule on whether the construct adds beyond SPOF detection
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
