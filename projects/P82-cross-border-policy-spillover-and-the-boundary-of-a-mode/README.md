# P82 - Cross-border policy spillover and the boundary of a modelled market

**Track N - Policy-Market Contagion and Systemic Indicators**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Comparative regulation researcher |
| **Upstream** | Discussion 3.1; P44; `MarketBoundary` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

`MarketBoundary` records an asset class, a geography and a timeframe, which fixes what is inside the model. Policy spillover crosses that boundary by construction: a rule made outside the modelled geography binds participants inside it. Either the boundary is porous - in which case what does it mean? - or the framework models a closed system that does not exist.

## 2. Purpose

Make the boundary's semantics explicit: what it includes, what it excludes, and what the framework claims about influences that originate outside it.

## 3. Scope

**In scope**

- A precise semantics for `MarketBoundary`: is it a scope of representation or a claim of causal closure?
- A treatment of externally-originating rules that bind inside the boundary.
- A documented convention for recording out-of-boundary influences.

**Out of scope**

- Modelling multiple markets simultaneously before the boundary semantics are settled.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the two candidate readings and choose: a boundary that scopes what is *represented*, or one that asserts nothing outside *matters*. Only the first is defensible.
2. Given the first reading, an out-of-boundary rule that binds inside is not a contradiction - it is an input the model treats as exogenous, and should be recorded as such.
3. Design the recording convention so an exogenous influence is visible in the output. An unrecorded exogenous input is indistinguishable from an assumption of closure.
4. Use the extraterritoriality evidence from the sanctions and regulatory literature; rules binding beyond their home jurisdiction are the normal case, not the exception.
5. Update the `MarketBoundary` documentation so its semantics are stated where it is defined.
6. Coordinate with P44, which owns harmonisation, so the two do not produce competing vocabularies.

## 5. Task board

- [ ] State and choose between the two boundary readings.
- [ ] Define the treatment of exogenous binding rules.
- [ ] Design the recording convention.
- [ ] Update `MarketBoundary` documentation.
- [ ] Reconcile vocabulary with P44.
- [ ] Publish `docs/policy/boundary_semantics.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** Choose the boundary reading and define exogenous-influence recording.
- **Inputs:** `models.py`, P44.
- **Output artifact:** `docs/policy/boundary_semantics.md`.
- **Stop condition:** The chosen reading is stated where `MarketBoundary` is defined.

### `regime-comparativist`

- **Mandate:** Document extraterritorial rule application with instrument citations.
- **Inputs:** Official instruments.
- **Output artifact:** An extraterritoriality table.
- **Stop condition:** Every entry cites the instrument and its stated territorial scope.

### `api-surface-reviewer`

- **Mandate:** Ensure any type change keeps `to_dict`/`from_dict` lossless and the layering intact.
- **Inputs:** The proposal.
- **Output artifact:** An API review note.
- **Stop condition:** Round-tripping holds and no layer boundary is crossed.

**Hand-off order:** `spec-drafter` -> `regime-comparativist` -> `api-surface-reviewer`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-schema-roundtrip` | A boundary field is added | Proves `to_dict`/`from_dict` remains a fixed point. |
| `amf-regime-profile` | Extraterritorial scope is cited | Records the instrument and its territorial provisions. |
| `amf-doc-page` | The semantics are published | Enforces documentation conventions. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/boundary_semantics.md`
- An extraterritoriality table
- An exogenous-influence recording convention
- Updated `MarketBoundary` documentation

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The boundary's semantics are stated where the type is defined.
- [ ] Exogenous binding influences are recordable and visible in output.
- [ ] Every extraterritoriality claim cites an instrument.
- [ ] The vocabulary does not conflict with P44.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Farrell, H., & Newman, A. L. (2019). "Weaponized Interdependence: How Global Economic Networks Shape State Coercion." *International Security* 44(1), 42-79.
- European Union (2014). *Directive 2014/65/EU on markets in financial instruments (MiFID II)*. Official Journal of the European Union.
- United States Congress (2010). *Dodd-Frank Wall Street Reform and Consumer Protection Act*, Pub. L. 111-203.
- Committee of Wise Men (2001). *Final Report of the Committee of Wise Men on the Regulation of European Securities Markets* (the Lamfalussy Report). European Commission.
- Djankov, S., La Porta, R., Lopez-de-Silanes, F., & Shleifer, A. (2008). "The law and economics of self-dealing." *Journal of Financial Economics* 88(3), 430-465.
- International Monetary Fund (2023). "Geoeconomic Fragmentation and the Future of Multilateralism." IMF Staff Discussion Note SDN/2023/001.
- Basel Committee on Banking Supervision (2011). *Basel III: A global regulatory framework for more resilient banks and banking systems* (rev. June 2011). Bank for International Settlements.

## 11. Commit protocol

Commits from this project use the scope `p82`:

```text
docs(p82): choose and state the MarketBoundary semantics
docs(p82): record extraterritorial rule application with citations
docs(p82): define how exogenous influences are recorded in output
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
