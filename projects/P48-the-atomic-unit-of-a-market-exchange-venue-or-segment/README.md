# P48 - The atomic unit of a market: exchange, venue or segment

**Track H - Global Market Mapping, Taxonomy & Standards**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Market structure researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 2.1 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The discussion asks whether a national stock exchange is the right unit or whether markets should split by segment, how to handle off-exchange trading which is a large share of some equity markets, whether retail and institutional should be modelled separately, and how to treat cross-listed issuers. Every downstream taxonomy depends on this answer, and it is currently unresolved.

## 2. Purpose

Choose the atomic unit on the criterion that matters for AMF - whether the candidate unit has its own distinguishable dependency structure - and record the consequences for everything built on top.

## 3. Scope

**In scope**

- A criterion for unit selection derived from the framework's own needs.
- Evaluation of at least four candidate units against that criterion.
- A ruling with its consequences for the register, the schema and the case studies.

**Out of scope**

- Modelling order flow or execution - forbidden.
- Any unit that requires market-data thresholds to determine membership.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the criterion: AMF represents seven systems per market, so a unit is atomic if it has its own distinguishable skeleton, circulatory, nervous, musculature, organs, immune and metabolism structure.
2. Apply it to each candidate: national exchange, venue, segment, and issuer-domicile grouping.
3. Address off-exchange trading directly: it has its own infrastructure, its own regulatory treatment and its own transparency regime, which is a strong argument for separate representation.
4. Address cross-listing: an issuer listed in two jurisdictions sits under two regulatory tiers, which is a structural fact the unit choice must accommodate.
5. Rule, and enumerate every downstream document that must change.
6. Feed the ruling into P47 so the register is built on a settled unit.

## 5. Task board

- [ ] State the unit-selection criterion.
- [ ] Evaluate four candidate units against it.
- [ ] Rule on off-exchange representation.
- [ ] Rule on cross-listing representation.
- [ ] Enumerate downstream consequences.
- [ ] Publish `docs/taxonomies/market_unit.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish the market-structure fragmentation literature from primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary.
- **Stop condition:** Fragmentation and off-exchange structure are sourced from peer-reviewed work.

### `spec-drafter`

- **Mandate:** Apply the seven-system criterion to each candidate unit and rule.
- **Inputs:** The criterion and literature.
- **Output artifact:** `docs/taxonomies/market_unit.md`.
- **Stop condition:** Each candidate is evaluated against all seven systems.

### `taxonomy-cartographer`

- **Mandate:** Enumerate every downstream artefact affected by the ruling.
- **Inputs:** The ruling.
- **Output artifact:** A consequences table.
- **Stop condition:** Every affected document is listed with the required change.

### `red-team-critic`

- **Mandate:** Construct a real market arrangement the chosen unit cannot represent.
- **Inputs:** The ruling.
- **Output artifact:** A falsification attempt.
- **Stop condition:** No unrepresentable arrangement remains, or the ruling is revised.

**Hand-off order:** `literature-scout` -> `spec-drafter` -> `taxonomy-cartographer` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-taxonomy-builder` | A unit of classification is chosen | Tests the unit against the seven-system criterion and records consequences. |
| `amf-boundary-check` | Unit membership rules are drafted | Rejects any rule requiring market-data thresholds. |
| `amf-red-team` | A unit is ruled | Searches for real arrangements the unit cannot represent. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/taxonomies/market_unit.md`
- A four-candidate evaluation
- Rulings on off-exchange and cross-listing
- A downstream consequences table

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The unit criterion is stated in terms of the seven AMF systems.
- [ ] Off-exchange trading and cross-listing each have an explicit ruling.
- [ ] No membership rule depends on a market-data threshold.
- [ ] Every downstream artefact affected is listed.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- O'Hara, M. (1995). *Market Microstructure Theory*. Blackwell. [Oxford / LSE / Chicago reading lists]
- Foucault, T., Pagano, M., & Roell, A. (2013). *Market Liquidity: Theory, Evidence, and Policy*. Oxford University Press.
- Hasbrouck, J. (2007). *Empirical Market Microstructure*. Oxford University Press.
- Menkveld, A. J. (2013). "High frequency trading and the new market makers." *Journal of Financial Markets* 16(4), 712-740.
- U.S. Securities and Exchange Commission (2005). *Regulation NMS*, Release No. 34-51808.
- European Union (2014). *Directive 2014/65/EU on markets in financial instruments (MiFID II)*. Official Journal of the European Union.
- Rosch, E. (1978). "Principles of Categorization." In Rosch, E. & Lloyd, B. B. (eds.), *Cognition and Categorization*. Lawrence Erlbaum.
- Bowker, G. C., & Star, S. L. (1999). *Sorting Things Out: Classification and Its Consequences*. MIT Press.

## 11. Commit protocol

Commits from this project use the scope `p48`:

```text
docs(p48): state the seven-system criterion for the atomic market unit
docs(p48): rule on off-exchange and cross-listed representation
docs(p48): enumerate downstream consequences of the unit ruling
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

