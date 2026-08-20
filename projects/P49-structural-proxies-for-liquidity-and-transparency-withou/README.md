# P49 - Structural proxies for liquidity and transparency without market data

**Track H - Global Market Mapping, Taxonomy & Standards**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Market structure researcher |
| **Upstream** | issue #125 (25b, "volume, spreads"); Discussion 2.2 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Issue #125 proposes liquidity proxies described as 'volume, spreads'. Both are market-data quantities and both are explicitly forbidden by the non-trading boundary that `tests/unit/test_non_trading_boundary.py` mechanically enforces. The framework needs a notion of liquidity provision it can legally represent, or it must state that it cannot represent liquidity at all.

## 2. Purpose

Define liquidity and transparency as *structural* properties - the arrangements that provide them - rather than as measured outcomes, and confirm the definitions pass the boundary guard.

## 3. Scope

**In scope**

- Structural proxies: market-maker obligation presence, venue redundancy, settlement-cycle structure, transparency-regime tier, circuit-breaker presence.
- A mapping from each proxy to the AMF system it belongs to.
- Boundary-guard verification for every proposed name.

**Out of scope**

- Volume, spreads, depth, turnover, price impact or any other measured market quantity.
- Any claim that a structural proxy predicts realised liquidity.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Read the liquidity literature to understand what the measured quantities capture, precisely so that the structural proxies do not silently claim to capture the same thing.
2. Enumerate the structural arrangements that provide liquidity: designated market makers and their obligations, venue multiplicity, settlement arrangements, transparency requirements, and volatility controls.
3. For each, name it in structural vocabulary and check it against the forbidden substring list before proceeding.
4. Map each proxy onto the AMF system it belongs to - most are circulatory or immune.
5. State explicitly and prominently that a structural proxy is not a liquidity measurement.
6. Run the boundary guard on the proposed names as the acceptance gate, not as an afterthought.

## 5. Task board

- [ ] Summarise what measured liquidity captures, to bound the claim.
- [ ] Enumerate structural liquidity and transparency arrangements.
- [ ] Name each in structural vocabulary and check the guard.
- [ ] Map proxies to AMF systems.
- [ ] Write the not-a-measurement statement.
- [ ] Publish `docs/taxonomies/liquidity_structure.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish what measured liquidity captures from primary market-microstructure sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary bounding the claim.
- **Stop condition:** The summary states what structural proxies cannot substitute for.

### `boundary-sentinel`

- **Mandate:** Check every proposed name against the forbidden substring list before it is adopted.
- **Inputs:** Proposed proxy names.
- **Output artifact:** A boundary report per name.
- **Stop condition:** No proposed name contains a forbidden substring and no allowlist entry is added.

### `spec-drafter`

- **Mandate:** Define each proxy structurally and map it to its AMF system.
- **Inputs:** Vetted names and the literature summary.
- **Output artifact:** `docs/taxonomies/liquidity_structure.md`.
- **Stop condition:** Every proxy is defined by an arrangement, never by an outcome.

### `red-team-critic`

- **Mandate:** Attempt to read any proxy as a liquidity measurement.
- **Inputs:** The draft.
- **Output artifact:** A misreading report.
- **Stop condition:** No proxy can be quoted as a measurement.

**Hand-off order:** `literature-scout` -> `boundary-sentinel` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-boundary-check` | Any proxy name is proposed | Runs the forbidden-substring guard and blocks adoption on a hit. |
| `amf-taxonomy-builder` | Proxies are catalogued | Builds the table with an AMF system mapping and citations. |
| `amf-red-team` | A proxy is defined | Tests whether it can be misread as a market measurement. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/taxonomies/liquidity_structure.md`
- A vetted structural proxy set
- An AMF system mapping
- Boundary-guard evidence

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every proxy is an arrangement, not an outcome.
- [ ] The non-trading boundary guard passes for every proposed name with no new allowlist entries.
- [ ] The not-a-measurement statement appears prominently.
- [ ] No forbidden quantity appears anywhere in the document or proposed schema.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Kyle, A. S. (1985). "Continuous Auctions and Insider Trading." *Econometrica* 53(6), 1315-1335.
- Amihud, Y. (2002). "Illiquidity and stock returns: cross-section and time-series effects." *Journal of Financial Markets* 5(1), 31-56.
- Brunnermeier, M. K., & Pedersen, L. H. (2009). "Market Liquidity and Funding Liquidity." *Review of Financial Studies* 22(6), 2201-2238.
- Foucault, T., Pagano, M., & Roell, A. (2013). *Market Liquidity: Theory, Evidence, and Policy*. Oxford University Press.
- O'Hara, M. (1995). *Market Microstructure Theory*. Blackwell. [Oxford / LSE / Chicago reading lists]
- Hasbrouck, J. (2007). *Empirical Market Microstructure*. Oxford University Press.
- CPMI-IOSCO (2012). *Principles for Financial Market Infrastructures*. Bank for International Settlements & IOSCO.
- European Union (2014). *Directive 2014/65/EU on markets in financial instruments (MiFID II)*. Official Journal of the European Union.

## 11. Commit protocol

Commits from this project use the scope `p49`:

```text
docs(p49): bound what structural liquidity proxies can and cannot claim
docs(p49): define liquidity and transparency as structural arrangements
test(p49): verify every proxy name against the non-trading boundary guard
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

