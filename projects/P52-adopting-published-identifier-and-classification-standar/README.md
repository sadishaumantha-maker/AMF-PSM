# P52 - Adopting published identifier and classification standards

**Track H - Global Market Mapping, Taxonomy & Standards**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Data standards engineer |
| **Upstream** | issue #43 (global stock market standards); Discussion 2.3 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The repository invents its own vocabulary for markets, instruments and entities. Mature, published standards already exist for entity identification, instrument classification and financial messaging. The dispute is whether adopting them constrains the framework's structural vocabulary unhelpfully, or whether refusing them condemns the taxonomy to being unmappable to anything else.

## 2. Purpose

Decide, standard by standard, which published identifiers and classifications the taxonomy adopts, and record the mapping so that AMF's structural vocabulary stays its own while remaining interoperable.

## 3. Scope

**In scope**

- An evaluation of entity, instrument and classification standards for fit.
- A mapping table from AMF taxonomy terms to standard identifiers.
- A rule for when a standard identifier is stored and when it is not.

**Out of scope**

- Storing any instrument-level or entity-level market data.
- Adopting a standard whose licensing prevents use in a proprietary, privately distributed package.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Evaluate each standard on three axes: fit to structural modelling, stability of the identifier, and licensing compatibility with a proprietary package.
2. Check licensing carefully - some classification standards are commercially licensed, and adopting one without checking would be a licence violation, not a design mistake.
3. Adopt identifiers where they name a structural entity the framework already models, and refuse them where they name a market-data concept.
4. Build the mapping table from AMF terms to standard terms in both directions.
5. State the rule for storage: an identifier is stored only when it identifies something structural.
6. Confirm the non-trading boundary guard passes for every adopted field name.

## 5. Task board

- [ ] Evaluate each standard on fit, stability and licensing.
- [ ] Record licensing findings explicitly.
- [ ] Decide adopt or refuse per standard.
- [ ] Build the bidirectional mapping table.
- [ ] Write the storage rule.
- [ ] Publish `docs/taxonomies/standards_adoption.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Collect the official specification and licensing terms for each candidate standard.
- **Inputs:** Standards bodies' published materials.
- **Output artifact:** A specification and licensing table.
- **Stop condition:** Every candidate has its licensing terms recorded, not assumed.

### `taxonomy-cartographer`

- **Mandate:** Build the bidirectional mapping between AMF terms and adopted standards.
- **Inputs:** Adopted standards and the AMF vocabulary.
- **Output artifact:** A mapping table.
- **Stop condition:** Every AMF taxonomy term either maps or is marked deliberately unmapped.

### `integrity-warden`

- **Mandate:** Confirm no adopted standard's licensing conflicts with the repository's proprietary, private-distribution position.
- **Inputs:** Licensing table, `LICENSE.txt`, `RELEASING.md`.
- **Output artifact:** A licensing compatibility attestation.
- **Stop condition:** Every adopted standard is compatible, or is refused.

### `boundary-sentinel`

- **Mandate:** Verify adopted field names pass the non-trading guard.
- **Inputs:** Proposed field names.
- **Output artifact:** A boundary report.
- **Stop condition:** No adopted name contains a forbidden substring.

**Hand-off order:** `literature-scout` -> `taxonomy-cartographer` -> `integrity-warden` -> `boundary-sentinel`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-taxonomy-builder` | A standard is mapped | Builds the bidirectional mapping with specification citations. |
| `amf-integrity-verify` | Licensing compatibility is assessed | Checks the adoption against the repository licence and distribution rules. |
| `amf-boundary-check` | A standard field is adopted | Runs the non-trading naming guard over the field name. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/taxonomies/standards_adoption.md`
- A per-standard evaluation with licensing findings
- A bidirectional mapping table
- A storage rule

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every candidate standard has recorded licensing terms.
- [ ] No adopted standard conflicts with the repository's licence or private-distribution rule.
- [ ] Every AMF taxonomy term maps or is marked deliberately unmapped.
- [ ] The non-trading boundary guard passes for every adopted field name.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- ISO (2020). *ISO 17442: Financial services - Legal entity identifier (LEI)*.
- ISO (2019). *ISO 10962: Securities and related financial instruments - Classification of financial instruments (CFI) code*.
- ISO (2022). *ISO 20022: Financial services - Universal financial industry message scheme*.
- EDM Council / Object Management Group. *Financial Industry Business Ontology (FIBO)*.
- MSCI & S&P Dow Jones Indices. *Global Industry Classification Standard (GICS) Methodology*.
- Gruber, T. R. (1993). "A translation approach to portable ontology specifications." *Knowledge Acquisition* 5(2), 199-220.
- Bowker, G. C., & Star, S. L. (1999). *Sorting Things Out: Classification and Its Consequences*. MIT Press.
- Wilkinson, M. D., et al. (2016). "The FAIR Guiding Principles for scientific data management and stewardship." *Scientific Data* 3, 160018.

## 11. Commit protocol

Commits from this project use the scope `p52`:

```text
docs(p52): evaluate identifier and classification standards for fit and licensing
docs(p52): publish the bidirectional AMF-to-standard mapping
docs(p52): state when a standard identifier is stored
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
