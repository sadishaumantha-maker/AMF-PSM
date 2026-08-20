# P55 - The 2007-2009 crisis as a structural stress trace

**Track I - Empirical Case Studies & Forensic Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2.5 weeks |
| **Lead role** | Research lead |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Track 3 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The framework claims to model contagion, and the best-documented contagion episode in modern finance is available in exhaustive official and academic detail. Either the framework can represent that episode's structural sequence, or its contagion claims are decorative. Nobody has attempted the mapping.

## 2. Purpose

Attempt an honest structural mapping of the crisis sequence onto AMF systems and dependency edges, and report precisely where the framework's vocabulary runs out.

## 3. Scope

**In scope**

- A structural timeline: which functions failed, in what order, and through which dependency.
- A mapping onto the seven systems and the dependency-kind vocabulary.
- An explicit inventory of what the framework cannot represent about the episode.

**Out of scope**

- Any price, spread, loss or exposure figure.
- Claiming the framework would have predicted the episode.
- Retrospective parameter fitting to reproduce the sequence.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Build the timeline from official inquiry records and peer-reviewed accounts, not from popular narrative.
2. Express each step structurally: a funding dependency that stopped functioning, an information system that stopped pricing, a regulatory layer that did not bind.
3. Map each step onto a system and a dependency kind, and record the ones that do not map.
4. Resist the temptation to fit parameters until the framework reproduces the sequence - that is curve-fitting, and the repository's illustrative-not-validated rule forbids presenting it otherwise.
5. Report the unmappable steps prominently; they are the specification for future framework work.
6. State in the document that this is a retrospective structural reading, not a demonstration of predictive capability.

## 5. Task board

- [ ] Build the sourced structural timeline.
- [ ] Express each step in structural vocabulary.
- [ ] Map steps onto systems and dependency kinds.
- [ ] Inventory the unmappable steps.
- [ ] Write the no-prediction statement.
- [ ] Publish `docs/case_studies/crisis_2007_2009.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `case-study-archivist`

- **Mandate:** Build the timeline from official inquiry records and peer-reviewed accounts.
- **Inputs:** Official reports and academic sources.
- **Output artifact:** A dated structural timeline.
- **Stop condition:** Every step has a date and at least one primary or peer-reviewed source.

### `taxonomy-cartographer`

- **Mandate:** Map each step onto a system and a dependency kind, marking failures.
- **Inputs:** The timeline.
- **Output artifact:** A mapping table with an unmappable list.
- **Stop condition:** Every step is mapped or explicitly listed as unmappable.

### `boundary-sentinel`

- **Mandate:** Verify no market-data quantity enters the case file.
- **Inputs:** The draft.
- **Output artifact:** A boundary report.
- **Stop condition:** No price, spread, loss or exposure figure appears.

### `red-team-critic`

- **Mandate:** Check for any implication that AMF would have predicted the episode.
- **Inputs:** The draft.
- **Output artifact:** A wording critique.
- **Stop condition:** No sentence can be read as a predictive claim.

**Hand-off order:** `case-study-archivist` -> `taxonomy-cartographer` -> `boundary-sentinel` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-case-dossier` | The case file is assembled | Applies the protocol with source ranking, dating and the uncertainty section. |
| `amf-boundary-check` | A step is expressed structurally | Rejects any market-data quantity. |
| `amf-red-team` | Before commit | Scans for retrospective prediction claims and curve-fitting. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/case_studies/crisis_2007_2009.md`
- A dated structural timeline
- A system and dependency-kind mapping
- An unmappable-step inventory

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every timeline step is dated and primary-sourced or peer-reviewed.
- [ ] No market-data quantity appears anywhere in the file.
- [ ] The unmappable steps are listed prominently.
- [ ] The file states explicitly that this is retrospective structural reading, not prediction.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Brunnermeier, M. K. (2009). "Deciphering the Liquidity and Credit Crunch 2007-2008." *Journal of Economic Perspectives* 23(1), 77-100.
- Gorton, G., & Metrick, A. (2012). "Securitized banking and the run on repo." *Journal of Financial Economics* 104(3), 425-451.
- Brunnermeier, M. K., & Pedersen, L. H. (2009). "Market Liquidity and Funding Liquidity." *Review of Financial Studies* 22(6), 2201-2238.
- Adrian, T., & Brunnermeier, M. K. (2016). "CoVaR." *American Economic Review* 106(7), 1705-1741.
- Acharya, V. V., Pedersen, L. H., Philippon, T., & Richardson, M. (2017). "Measuring Systemic Risk." *Review of Financial Studies* 30(1), 2-47.
- Gai, P., & Kapadia, S. (2010). "Contagion in financial networks." *Proceedings of the Royal Society A* 466(2120), 2401-2423.
- Minsky, H. P. (1986). *Stabilizing an Unstable Economy*. Yale University Press.
- Reinhart, C. M., & Rogoff, K. S. (2009). *This Time Is Different: Eight Centuries of Financial Folly*. Princeton University Press.

## 11. Commit protocol

Commits from this project use the scope `p55`:

```text
docs(p55): build a sourced structural timeline of the 2007-2009 crisis
docs(p55): map the crisis sequence onto AMF systems and dependency kinds
docs(p55): publish the inventory of structurally unmappable steps
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

