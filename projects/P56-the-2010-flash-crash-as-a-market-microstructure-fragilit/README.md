# P56 - The 2010 flash crash as a market-microstructure fragility case

**Track I - Empirical Case Studies & Forensic Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Market structure researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 6.1; Track 3 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The flash crash is the canonical case of a market whose structure, not whose fundamentals, failed. It is unusually well documented in the peer-reviewed literature. The dispute is whether AMF - which has no concept of time below a step and no concept of order flow - can say anything about an episode that unfolded in minutes through order-book dynamics.

## 2. Purpose

Establish the resolution limits of the framework by attempting a structural reading of an episode that sits close to, and possibly beyond, its representational floor.

## 3. Scope

**In scope**

- A structural reading of the episode: venue interconnection, liquidity-provision obligations, volatility controls.
- An explicit statement of AMF's temporal and structural resolution limits.
- A recommendation on whether sub-step dynamics are worth representing at all.

**Out of scope**

- Order-book modelling, order flow, quotes or execution - forbidden by the non-trading rule.
- Any claim about individual participants.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Read the peer-reviewed account of the episode, not the popular one; the academic record differs materially from the initial narrative.
2. Extract only the structural features: how venues were interconnected, what liquidity-provision obligations existed, which volatility controls fired and which did not.
3. State AMF's resolution floor honestly: a simulation step has no defined duration, so an episode measured in minutes has no natural representation.
4. Assess the post-episode structural changes - volatility controls and their coordination across venues - since those *are* representable as immune-system structure.
5. Recommend for or against sub-step temporal resolution, with the cost of adding it.
6. Keep every observation structural; the boundary guard applies to the prose as much as to the code.

## 5. Task board

- [ ] Assemble the peer-reviewed account.
- [ ] Extract the structural features only.
- [ ] State the framework's resolution floor.
- [ ] Assess post-episode structural changes as immune structure.
- [ ] Recommend on sub-step resolution with costs.
- [ ] Publish `docs/case_studies/flash_crash_2010.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Assemble the peer-reviewed record and distinguish it from the initial narrative.
- **Inputs:** The reading list.
- **Output artifact:** An annotated account with the divergences noted.
- **Stop condition:** The academic and initial accounts are explicitly compared.

### `case-study-archivist`

- **Mandate:** Build the structural feature list with sources.
- **Inputs:** The account.
- **Output artifact:** A structural feature table.
- **Stop condition:** No feature requires order-flow data to state.

### `spec-drafter`

- **Mandate:** State the resolution floor and recommend on sub-step dynamics with costs.
- **Inputs:** The feature table and `simulation.py`.
- **Output artifact:** `docs/case_studies/flash_crash_2010.md`.
- **Stop condition:** The recommendation names the implementation cost, not only the benefit.

### `boundary-sentinel`

- **Mandate:** Verify no order, quote or execution vocabulary enters the file.
- **Inputs:** The draft.
- **Output artifact:** A boundary report.
- **Stop condition:** No forbidden term appears anywhere in the file.

**Hand-off order:** `literature-scout` -> `case-study-archivist` -> `spec-drafter` -> `boundary-sentinel`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-case-dossier` | The case file is assembled | Applies the protocol and the structural-reading rule. |
| `amf-boundary-check` | A structural feature is stated | Rejects order-flow and execution vocabulary. |
| `amf-red-team` | The resolution claim is made | Tests whether the framework is being credited with resolution it does not have. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/case_studies/flash_crash_2010.md`
- A structural feature table
- A resolution-limit statement
- A sub-step resolution recommendation

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The peer-reviewed account is used and distinguished from the initial narrative.
- [ ] The framework's temporal resolution floor is stated explicitly.
- [ ] No order, quote or execution vocabulary appears.
- [ ] The recommendation states implementation cost as well as benefit.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Kirilenko, A., Kyle, A. S., Samadi, M., & Tuzun, T. (2017). "The Flash Crash: High-Frequency Trading in an Electronic Market." *Journal of Finance* 72(3), 967-998.
- Menkveld, A. J. (2013). "High frequency trading and the new market makers." *Journal of Financial Markets* 16(4), 712-740.
- Budish, E., Cramton, P., & Shim, J. (2015). "The High-Frequency Trading Arms Race: Frequent Batch Auctions as a Market Design Response." *Quarterly Journal of Economics* 130(4), 1547-1621.
- O'Hara, M. (2015). "High frequency market microstructure." *Journal of Financial Economics* 116(2), 257-270.
- Foucault, T., Pagano, M., & Roell, A. (2013). *Market Liquidity: Theory, Evidence, and Policy*. Oxford University Press.
- U.S. Securities and Exchange Commission (2005). *Regulation NMS*, Release No. 34-51808.
- CPMI-IOSCO (2012). *Principles for Financial Market Infrastructures*. Bank for International Settlements & IOSCO.
- Perrow, C. (1984). *Normal Accidents: Living with High-Risk Technologies*. Princeton University Press.

## 11. Commit protocol

Commits from this project use the scope `p56`:

```text
docs(p56): assemble the peer-reviewed structural account of the 2010 flash crash
docs(p56): state AMF's temporal resolution floor
docs(p56): recommend for or against sub-step temporal resolution
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
