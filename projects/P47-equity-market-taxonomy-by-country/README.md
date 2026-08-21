# P47 - Equity market taxonomy by country

**Track H - Global Market Mapping, Taxonomy & Standards**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Market taxonomy researcher |
| **Upstream** | issue #124 (25a); `docs/ANALYSIS_AND_ROADMAP.md` #25 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The task is stated as documenting forty major markets with every country in scope. Those two clauses conflict: forty markets is a curated list, every country is a census, and the curation rule that produces forty has never been written down. Without it the taxonomy cannot be completed or audited.

## 2. Purpose

Write the inclusion rule first, then build the taxonomy that the rule produces, so that any reader can verify why a market is in or out.

## 3. Scope

**In scope**

- A written inclusion rule with a stated threshold and its source.
- A market register: jurisdiction, venue, operator, regulator, structural characteristics.
- An audit trail so every inclusion and exclusion decision is checkable.

**Out of scope**

- Trading volumes, market capitalisation figures, prices or any market-data quantity in the AMF model itself.
- Ranking markets as better or worse.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Write the inclusion rule before collecting anything. State the unit (jurisdiction, venue or segment) and the threshold.
2. Note that the unit question is itself disputed and is settled in P48; if P48 is not yet complete, record the assumption and proceed provisionally.
3. Populate the register from official sources only: regulator registers, exchange operator disclosures, and recognised standards bodies.
4. Record structural characteristics only - venue type, operator structure, regulator, settlement arrangement - never market-data quantities.
5. Keep an explicit exclusion list: every market considered and rejected, with the rule clause that rejected it.
6. Publish the register in a form that can be regenerated and diffed, not as prose.

## 5. Task board

- [ ] Write and justify the inclusion rule.
- [ ] Choose the register schema (structural fields only).
- [ ] Populate the register from official sources.
- [ ] Maintain the exclusion list with rule references.
- [ ] Cross-check against the P52 identifier standards.
- [ ] Publish `docs/taxonomies/equity_markets.md` plus the register data file.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** Write the inclusion rule and the register schema before any collection begins.
- **Inputs:** Issue #124, the reading list.
- **Output artifact:** An inclusion rule with a stated threshold.
- **Stop condition:** The rule decides every borderline case without further judgement.

### `taxonomy-cartographer`

- **Mandate:** Populate the register from official sources with a citation per row.
- **Inputs:** The rule and schema.
- **Output artifact:** `docs/taxonomies/_data/equity_market_register.md`.
- **Stop condition:** Every row cites an official source; no row contains a market-data quantity.

### `boundary-sentinel`

- **Mandate:** Verify no field or value introduces forbidden market-data vocabulary.
- **Inputs:** The register schema and data.
- **Output artifact:** A boundary report.
- **Stop condition:** The non-trading naming guard passes for every field name.

### `red-team-critic`

- **Mandate:** Find a market that the rule cannot decide.
- **Inputs:** The rule and register.
- **Output artifact:** An undecidable-case report.
- **Stop condition:** Every case is decidable or the rule is amended.

**Hand-off order:** `spec-drafter` -> `taxonomy-cartographer` -> `boundary-sentinel` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-taxonomy-builder` | A classification register is built | Builds the table from official standards with a citation per row and a maintained exclusion list. |
| `amf-boundary-check` | Register fields are named | Runs the non-trading naming guard over the schema. |
| `amf-source-vetting` | A register source is proposed | Requires an official register, operator disclosure or standards body. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/taxonomies/equity_markets.md`
- A structured, citable market register
- An exclusion list with rule references

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The inclusion rule decides every considered market without further judgement.
- [ ] Every register row cites an official source.
- [ ] No market-data quantity appears in the register.
- [ ] The exclusion list names the rule clause that rejected each excluded market.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- ISO (2019). *ISO 10962: Securities and related financial instruments - Classification of financial instruments (CFI) code*.
- ISO (2020). *ISO 17442: Financial services - Legal entity identifier (LEI)*.
- MSCI & S&P Dow Jones Indices. *Global Industry Classification Standard (GICS) Methodology*.
- CPMI-IOSCO (2012). *Principles for Financial Market Infrastructures*. Bank for International Settlements & IOSCO.
- Foucault, T., Pagano, M., & Roell, A. (2013). *Market Liquidity: Theory, Evidence, and Policy*. Oxford University Press.
- O'Hara, M. (1995). *Market Microstructure Theory*. Blackwell. [Oxford / LSE / Chicago reading lists]
- Bowker, G. C., & Star, S. L. (1999). *Sorting Things Out: Classification and Its Consequences*. MIT Press.
- Gruber, T. R. (1993). "A translation approach to portable ontology specifications." *Knowledge Acquisition* 5(2), 199-220.

## 11. Commit protocol

Commits from this project use the scope `p47`:

```text
docs(p47): write the equity market inclusion rule before collection
docs(p47): populate the structural equity market register from official sources
docs(p47): publish the exclusion list with rule references
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
