# P84 - Market abuse detection via network analysis: what is actually claimable

**Track O - Market Abuse and Forensic Network Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Forensic research analyst |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 4.2 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Discussion 4.2 proposes detecting market abuse through network analysis. Every published abuse-detection method operates on transaction-level or account-level data - who traded with whom, when. The framework has seven systems and a dependency graph, and forbids trade-level data by construction. Proposing detection here is close to a category error, and the danger is not that it fails but that it appears to work.

## 2. Purpose

Separate what the framework can say about *susceptibility to abuse* from what it cannot say about *occurrence of abuse*, and make the second impossible to claim from its output.

## 3. Scope

**In scope**

- A survey of network-based abuse detection and its actual data requirements.
- A structural notion of abuse susceptibility - opacity, concentration, weak supervisory coupling.
- A prohibition, stated in the framework's own conventions, on reading susceptibility as detection.

**Out of scope**

- Transaction, account or order-level data of any kind.
- Naming or scoring any real venue, firm or participant.
- Any output that could be read as an allegation.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Survey the detection literature and record what each method consumes; anomaly detection over transaction graphs is the dominant family and needs exactly the data the framework refuses.
2. Draw the line explicitly: detection is a claim about an event; susceptibility is a claim about structure. The framework can address the second only.
3. Build the susceptibility notion from structure the framework already has - transparency-regime tier, concentration, supervisory coupling strength, articulation-point venues.
4. State the base-rate problem plainly: abuse is rare, so any screen with a realistic false-positive rate produces mostly false positives, and a structural screen is far weaker than a transactional one.
5. Write the prohibition into the conventions: no AMF output may be described as detecting, indicating or suggesting abuse by any party.
6. Have the red-team critic attempt to write an accusation from real output before this is merged.

## 5. Task board

- [ ] Survey detection methods and their data requirements.
- [ ] Define susceptibility against detection formally.
- [ ] Build the susceptibility notion from existing structure.
- [ ] State the base-rate argument.
- [ ] Write the no-detection-claim prohibition.
- [ ] Publish `docs/research/abuse_susceptibility.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Record what each network-based detection method consumes, from its originating paper.
- **Inputs:** The reading list.
- **Output artifact:** A method and data-requirement table.
- **Stop condition:** Every method's inputs are stated; none is summarised as 'network data'.

### `spec-drafter`

- **Mandate:** Define susceptibility, distinguish it from detection, and write the prohibition.
- **Inputs:** The survey and the AMF model.
- **Output artifact:** `docs/research/abuse_susceptibility.md`.
- **Stop condition:** The prohibition is stated in the conventions, not only in this document.

### `boundary-sentinel`

- **Mandate:** Reject any construct requiring transaction, account or order data.
- **Inputs:** The proposals.
- **Output artifact:** A boundary report.
- **Stop condition:** Every surviving construct is purely structural.

### `red-team-critic`

- **Mandate:** Attempt to write a defensible-looking accusation from real framework output.
- **Inputs:** Rendered output on the example markets.
- **Output artifact:** An accusation attempt report.
- **Stop condition:** No attempt succeeds, or the output is changed until none does.

**Hand-off order:** `literature-scout` -> `spec-drafter` -> `boundary-sentinel` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-boundary-check` | A detection construct is proposed | Rejects transaction-, account- and order-level inputs. |
| `amf-red-team` | Before merge | Attempts to extract an allegation from rendered output. |
| `amf-source-vetting` | A detection claim is cited | Requires peer-reviewed sourcing and records reported false-positive rates. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/research/abuse_susceptibility.md`
- A method and data-requirement table
- A structural susceptibility notion
- A prohibition in the conventions

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Detection and susceptibility are formally distinguished.
- [ ] No construct consumes transaction, account or order data.
- [ ] The base-rate argument is stated with figures from the literature.
- [ ] No accusation can be extracted from any rendered output.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Akoglu, L., Tong, H., & Koutra, D. (2015). "Graph based anomaly detection and description: a survey." *Data Mining and Knowledge Discovery* 29(3), 626-688.
- Chandola, V., Banerjee, A., & Kumar, V. (2009). "Anomaly detection: A survey." *ACM Computing Surveys* 41(3), 15.
- European Union (2014). *Regulation (EU) No 596/2014 on market abuse (Market Abuse Regulation)*. Official Journal of the European Union.
- Dyck, A., Morse, A., & Zingales, L. (2010). "Who Blows the Whistle on Corporate Fraud?" *Journal of Finance* 65(6), 2213-2253.
- Karpoff, J. M., Lee, D. S., & Martin, G. S. (2008). "The Cost to Firms of Cooking the Books." *Journal of Financial and Quantitative Analysis* 43(3), 581-611.
- O'Hara, M. (1995). *Market Microstructure Theory*. Blackwell. [Oxford / LSE / Chicago reading lists]
- Foucault, T., Pagano, M., & Roell, A. (2013). *Market Liquidity: Theory, Evidence, and Policy*. Oxford University Press.
- Ioannidis, J. P. A. (2005). "Why Most Published Research Findings Are False." *PLoS Medicine* 2(8), e124.

## 11. Commit protocol

Commits from this project use the scope `p84`:

```text
docs(p84): distinguish abuse susceptibility from abuse detection
docs(p84): state the base-rate argument against structural abuse screens
docs(p84): prohibit reading AMF output as an abuse indication
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
