# P110 - Transition risk as policy change and the one climate channel that fits

**Track S - Climate, Nature and Long-Horizon Risk**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Policy researcher |
| **Upstream** | Discussion 8.1; P43 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

P107 refuses climate projection, correctly. But one climate channel is not a projection at all: transition risk operates through policy change, and policy change is something Track G already models in detail. Treating all climate risk as out of scope would discard the one part that fits the framework's existing machinery exactly.

## 2. Purpose

Identify the transition channel as an instance of institutional change already covered by P43, and represent it with the existing vocabulary rather than a new one.

## 3. Scope

**In scope**

- A mapping of transition risk onto P43's change modes.
- A demonstration that the existing machinery represents it without extension.
- A clear line between this and the projection P107 refuses.

**Out of scope**

- Any scenario, pathway or projection.
- Physical risk, which P107 governs.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Map transition risk onto the change-mode typology: a phased requirement is layering, an abrupt prohibition is displacement, and an unenforced target is drift. The typology fits without modification, which is the finding.
2. Demonstrate rather than assert: express a documented transition measure as a policy-tier change and run it through the existing machinery.
3. Draw the line with P107 sharply - representing the structural effect of an enacted measure is not projecting a pathway, and the distinction must be legible to a reader.
4. Note the consequence: the framework can say something about climate policy that has already happened, and nothing about climate policy that has not.
5. Avoid scenario vocabulary entirely, since scenario language will pull the treatment back toward projection.
6. Reuse P43's vocabulary rather than introducing climate-specific terms.

## 5. Task board

- [ ] Map transition risk onto the change modes.
- [ ] Express a documented measure as a tier change.
- [ ] Run it through the existing machinery.
- [ ] Draw the line with P107 explicitly.
- [ ] Avoid scenario vocabulary.
- [ ] Publish `docs/policy/transition_channel.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `regime-comparativist`

- **Mandate:** Document enacted transition measures as tier changes with instrument citations.
- **Inputs:** Official instruments.
- **Output artifact:** A measure-to-tier table.
- **Stop condition:** Every entry cites an enacted instrument, never a proposal.

### `spec-drafter`

- **Mandate:** Map onto P43's typology and draw the line with P107.
- **Inputs:** The table and P43.
- **Output artifact:** `docs/policy/transition_channel.md`.
- **Stop condition:** No climate-specific vocabulary is introduced where P43's exists.

### `red-team-critic`

- **Mandate:** Attempt to read the treatment as a climate projection.
- **Inputs:** The draft.
- **Output artifact:** A projection-reading report.
- **Stop condition:** No reading supports a pathway claim.

**Hand-off order:** `regime-comparativist` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | A measure is recorded | Cites the enacted instrument with its vintage. |
| `amf-doc-page` | The channel is published | Enforces the illustrative-not-validated rule. |
| `amf-red-team` | The treatment is drafted | Tests whether it can be read as projection. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/transition_channel.md`
- A change-mode mapping
- A worked demonstration through existing machinery
- A clear line with P107

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Transition risk is expressed entirely in P43's existing vocabulary.
- [ ] Every documented measure is enacted, not proposed.
- [ ] The line with projection is legible to a reader.
- [ ] No scenario vocabulary appears.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Streeck, W., & Thelen, K. (eds.) (2005). *Beyond Continuity: Institutional Change in Advanced Political Economies*. Oxford University Press.
- Mahoney, J., & Thelen, K. (eds.) (2010). *Explaining Institutional Change: Ambiguity, Agency, and Power*. Cambridge University Press.
- Network for Greening the Financial System (2019). *A call for action: Climate change as a source of financial risk*. NGFS First Comprehensive Report.
- Task Force on Climate-related Financial Disclosures (2017). *Recommendations of the Task Force on Climate-related Financial Disclosures*. Financial Stability Board.
- Campiglio, E., Dafermos, Y., Monnin, P., Ryan-Collins, J., Schotten, G., & Tanaka, M. (2018). "Climate change challenges for central banks and financial regulators." *Nature Climate Change* 8, 462-468.
- Carney, M. (2015). *Breaking the Tragedy of the Horizon - climate change and financial stability*. Speech at Lloyd's of London, Bank of England.
- Battiston, S., Mandel, A., Monasterolo, I., Schutze, F., & Visentin, G. (2017). "A climate stress-test of the financial system." *Nature Climate Change* 7, 283-288.

## 11. Commit protocol

Commits from this project use the scope `p110`:

```text
docs(p110): map transition risk onto the existing change-mode typology
docs(p110): express enacted transition measures as policy-tier changes
docs(p110): draw the line between transition structure and climate projection
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

