# P51 - Non-equity markets: commodities, bonds and foreign exchange

**Track H - Global Market Mapping, Taxonomy & Standards**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Market taxonomy researcher |
| **Upstream** | issue #144 (7.1, #26) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Extending to commodities, bonds and foreign exchange is currently held behind the equity foundation, and correctly so - but the deeper dispute is whether the seven-system model transfers at all. Foreign exchange has no central venue and no single regulator; physical commodities have delivery infrastructure that equities do not; bond markets are predominantly dealer-intermediated. The anatomy may not be the same anatomy.

## 2. Purpose

Test whether the seven-system model transfers to each non-equity asset class, and report honestly where it does not, before any implementation work begins.

## 3. Scope

**In scope**

- A per-asset-class mapping attempt onto the seven systems.
- Identification of structures with no equity analogue, notably physical delivery and dealer intermediation.
- A go/no-go recommendation per asset class with its reasoning.

**Out of scope**

- Implementing any non-equity market before the mapping is accepted.
- Prices, yields, rates or any market-data quantity.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Map each asset class onto the seven systems one at a time; do not generalise from equities.
2. For foreign exchange, confront the absence of a central venue and a single regulator directly - the skeleton and immune systems are the hard cases.
3. For commodities, treat physical delivery and storage infrastructure as first-class structure, not as an appendix.
4. For bonds, treat dealer intermediation as the circulatory structure and check whether the framework can represent it without market data.
5. Where a structure has no analogue, say so; an honest gap is more useful than a forced mapping.
6. Give a go/no-go per asset class and sequence the ones that pass.

## 5. Task board

- [ ] Map commodities onto the seven systems.
- [ ] Map bonds onto the seven systems.
- [ ] Map foreign exchange onto the seven systems.
- [ ] Identify structures with no equity analogue.
- [ ] Issue a go/no-go per asset class.
- [ ] Publish `docs/taxonomies/non_equity_markets.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Collect primary structural descriptions of each asset class's infrastructure.
- **Inputs:** The reading list and official-sector sources.
- **Output artifact:** An annotated structure summary per class.
- **Stop condition:** Each class has a sourced description of its settlement and intermediation structure.

### `taxonomy-cartographer`

- **Mandate:** Attempt the seven-system mapping per class and record failures explicitly.
- **Inputs:** Structure summaries.
- **Output artifact:** A mapping table with gaps marked.
- **Stop condition:** Every unmapped structure is named, not glossed.

### `boundary-sentinel`

- **Mandate:** Ensure no proposed structure introduces market-data vocabulary.
- **Inputs:** The mapping table.
- **Output artifact:** A boundary report.
- **Stop condition:** No forbidden term appears in any proposed name.

### `red-team-critic`

- **Mandate:** Argue that the seven-system model does not transfer and force the mapping to answer.
- **Inputs:** The mapping.
- **Output artifact:** A dissent section.
- **Stop condition:** The dissent is adopted for at least one class, or answered for all.

**Hand-off order:** `literature-scout` -> `taxonomy-cartographer` -> `boundary-sentinel` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-taxonomy-builder` | An asset class is mapped | Builds the seven-system mapping table with sourced structural descriptions. |
| `amf-boundary-check` | A structure is named | Runs the non-trading naming guard. |
| `amf-red-team` | A mapping is proposed | Argues the analogy fails and requires an answer. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/taxonomies/non_equity_markets.md`
- A per-class seven-system mapping
- A named list of unmapped structures
- A go/no-go recommendation per class

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Each asset class is mapped independently, not by analogy to equities.
- [ ] Every structure without an equity analogue is named explicitly.
- [ ] A go/no-go with reasoning is issued per class.
- [ ] No market-data quantity appears anywhere.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Foucault, T., Pagano, M., & Roell, A. (2013). *Market Liquidity: Theory, Evidence, and Policy*. Oxford University Press.
- O'Hara, M. (1995). *Market Microstructure Theory*. Blackwell. [Oxford / LSE / Chicago reading lists]
- Bouchaud, J.-P., Bonart, J., Donier, J., & Gould, M. (2018). *Trades, Quotes and Prices: Financial Markets Under the Microscope*. Cambridge University Press.
- CPMI-IOSCO (2012). *Principles for Financial Market Infrastructures*. Bank for International Settlements & IOSCO.
- Pozsar, Z., Adrian, T., Ashcraft, A., & Boesky, H. (2013). "Shadow Banking." *FRBNY Economic Policy Review* 19(2), 1-16.
- Eichengreen, B. (2011). *Exorbitant Privilege: The Rise and Fall of the Dollar and the Future of the International Monetary System*. Oxford University Press.
- Farhi, E., & Maggiori, M. (2018). "A Model of the International Monetary System." *Quarterly Journal of Economics* 133(1), 295-355.
- ISO (2019). *ISO 10962: Securities and related financial instruments - Classification of financial instruments (CFI) code*.

## 11. Commit protocol

Commits from this project use the scope `p51`:

```text
docs(p51): map commodities, bonds and foreign exchange onto the seven systems
docs(p51): name the structures with no equity analogue
docs(p51): issue go/no-go recommendations per asset class
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

