# P76 - Restoring a green main and making red-on-main a blocking condition

**Track M - Live Defects and the Green-Main Obligation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 4 days |
| **Lead role** | CI owner |
| **Upstream** | CI red on `main` continuously since run #115 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

`main` has been red since run #115. Between then and now the repository has merged more than a dozen pull requests, each of which inherited a red baseline and could not tell its own failures from the standing ones. The dispute is whether red-on-main is an inconvenience to be worked around - as it has been - or a stop condition. Everything Track B builds rests on the answer, because a gate nobody can trust is not a gate.

## 2. Purpose

Get `main` green and keep it green: fix the standing failures, then make a red `main` visible and consequential rather than ambient.

## 3. Scope

**In scope**

- Closing every failure currently red on `main`, including the ones P74 and P75 own.
- A recorded green run on `main` as the baseline.
- A mechanism making a red `main` immediately visible, and a written stop rule.

**Out of scope**

- Weakening any gate to achieve green.
- Merging further feature work while `main` is red, which is the practice this charter ends.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Inventory every check currently failing on `main` with its first-failing commit, so the standing set is known rather than assumed.
2. Sequence the fixes: P74 for the numeric tests, P75 for the dead links, and this charter for anything neither owns.
3. Record the first green `main` run number and date; that becomes the baseline every later claim references.
4. Write the stop rule: while `main` is red, the only merges are fixes for the red. Draw on the delivery-performance evidence that batch size and unreviewable baselines are what make recovery slow.
5. Make it visible - a status badge for `main` in `README.md` is the cheapest honest mechanism, and unlike the coverage badge it carries real information.
6. Wire the standing-red condition into the P05 metric set so it is counted rather than tolerated.

## 5. Task board

- [ ] Inventory failing checks on `main` with first-failing commits.
- [ ] Sequence and land the fixes.
- [ ] Record the first green baseline run.
- [ ] Write the while-red stop rule.
- [ ] Add a `main` CI status badge to `README.md`.
- [ ] Add standing-red to the metric set.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `benchmark-runner`

- **Mandate:** Produce the failing-check inventory with first-failing commit per check.
- **Inputs:** Workflow run history for `main`.
- **Output artifact:** An inventory table.
- **Stop condition:** Every currently failing check has a first-failing commit identified.

### `red-team-critic`

- **Mandate:** Attempt to merge a deliberately broken change while `main` is red and show what notices.
- **Inputs:** The current gates.
- **Output artifact:** A detection report.
- **Stop condition:** Either something blocks it, or the gap is documented as the reason for the stop rule.

### `spec-drafter`

- **Mandate:** Write the stop rule and its escalation.
- **Inputs:** The inventory and detection report.
- **Output artifact:** A conventions addition.
- **Stop condition:** The rule names who may merge while red and under what condition.

### `release-marshal`

- **Mandate:** Record the green baseline and wire standing-red into the metric set.
- **Inputs:** The first green run.
- **Output artifact:** A baseline record and a metric definition.
- **Stop condition:** The baseline run number and date are recorded in the repository.

**Hand-off order:** `benchmark-runner` -> `red-team-critic` -> `spec-drafter` -> `release-marshal`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-coverage-gate` | Any gate is touched | Confirms the 100% branch gate is unweakened. |
| `amf-integrity-verify` | Workflows change | Re-verifies the protected artifacts. |
| `amf-doc-page` | The badge and rule are added | Enforces documentation conventions and link-check safety. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- A failing-check inventory
- A recorded green `main` baseline
- The while-red stop rule
- A `main` status badge and a standing-red metric

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every check on `main` passes, with the run recorded as the baseline.
- [ ] No gate was weakened to achieve it.
- [ ] The stop rule is written and names its escalation.
- [ ] Standing-red is a counted metric, not an informal observation.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Forsgren, N., Humble, J., & Kim, G. (2018). *Accelerate: The Science of Lean Software and DevOps*. IT Revolution.
- Humble, J., & Farley, D. (2010). *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Addison-Wesley.
- Nygard, M. T. (2018). *Release It! Design and Deploy Production-Ready Software* (2nd ed.). Pragmatic Bookshelf.
- Perrow, C. (1984). *Normal Accidents: Living with High-Risk Technologies*. Princeton University Press.
- Brooks, F. P. (1995). *The Mythical Man-Month: Essays on Software Engineering* (Anniversary ed.). Addison-Wesley.
- Goodhart, C. A. E. (1984). "Problems of Monetary Management: The U.K. Experience." In *Monetary Theory and Practice*. Macmillan. (Goodhart's Law)

## 11. Commit protocol

Commits from this project use the scope `p76`:

```text
docs(p76): inventory the standing failures on main with first-failing commits
docs(p76): adopt the while-red stop rule and record the green baseline
docs(p76): surface main CI status and count standing-red as a metric
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
