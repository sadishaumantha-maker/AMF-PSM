# P24 - Multi-kind edge aggregation semantics and the cap at one

**Track D - Graph & Network Theory of Market Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 4 days |
| **Lead role** | Library maintainer |
| **Upstream** | `CLAUDE.md` -> Market JSON schema; `DependencyGraph.edge_weight` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

> [!IMPORTANT]
> **Status against `main`.** **Unchanged in substance by `main`.** Pair-weight aggregation now sums with
> `amf.numeric.stable_sum`, so the order-dependence artefact is gone. The `min(1.0, ...)` cap and the
> information it destroys when reliance saturates are exactly as this charter describes them, so the
> dispute stands as written. Section 4 should use the landed implementation as its starting point rather
> than the pre-merge one.

---

## 1. The dispute this project settles

A source-target pair may carry several dependency kinds. Every structural query aggregates across kinds and caps the result at 1.0, so that "splitting one coupling across kinds never changes a score". The cap is a modelling decision with a consequence nobody has stated: two markets with genuinely different total reliance become indistinguishable once the sum saturates.

## 2. Purpose

Make the aggregation rule explicit, quantify the information the cap destroys, and decide whether saturation is the right semantics or whether the cap is hiding a normalisation problem.

## 3. Scope

**In scope**

- A formal statement of the aggregation rule and the invariant it protects.
- Measurement of how often saturation occurs on realistic market definitions.
- A comparison of capping against normalising, and a ruling.

**Out of scope**

- Changing the `(0, 1]` per-edge weight domain.
- Breaking `to_dict`/`from_dict` round-tripping of edge kinds.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the rule formally: aggregation function, cap, and which queries consume the aggregate.
2. State the invariant the cap protects and check whether any other mechanism could protect it instead.
3. Generate markets across a range of kind multiplicities and measure the saturation frequency.
4. Where saturation occurs, measure how much score variation is lost.
5. Compare with a normalising alternative that preserves ordering without saturating.
6. Rule, implement, and preserve lossless round-tripping of every edge kind either way.

## 5. Task board

- [ ] Write the formal aggregation statement.
- [ ] Measure saturation frequency across generated markets.
- [ ] Quantify lost score variation under saturation.
- [ ] Compare cap against normalisation.
- [ ] Implement the ruling.
- [ ] Publish `docs/graph/edge_aggregation.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** State the aggregation rule, its invariant and the alternatives.
- **Inputs:** `graph.py`, the schema documentation.
- **Output artifact:** `docs/graph/edge_aggregation.md`.
- **Stop condition:** The invariant is stated in a form a test can check.

### `benchmark-runner`

- **Mandate:** Measure saturation frequency and lost variation.
- **Inputs:** A generated market corpus.
- **Output artifact:** A measurement table.
- **Stop condition:** Saturation frequency is reported across at least four multiplicity levels.

### `algorithm-implementer`

- **Mandate:** Implement the ruling and preserve edge-kind round-tripping.
- **Inputs:** The ruling.
- **Output artifact:** A diff under `src/amf/graph.py` and `market.py`.
- **Stop condition:** `to_dict`/`from_dict` remains a fixed point including every kind.

### `property-test-author`

- **Mandate:** Encode the splitting invariance claim as a property.
- **Inputs:** The rule.
- **Output artifact:** A property asserting that splitting a coupling across kinds leaves every score unchanged.
- **Stop condition:** No counterexample within the example budget, or the claim is corrected.

**Hand-off order:** `math-formalizer` -> `benchmark-runner` -> `algorithm-implementer` -> `property-test-author`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-schema-roundtrip` | Edge representation changes | Proves lossless `to_dict`/`from_dict` round-tripping including kinds. |
| `amf-property-harness` | An invariance claim is made | Scaffolds the hypothesis property. |
| `amf-graph-algorithm` | Aggregation feeds a structural query | Re-verifies the query against its source algorithm under the new aggregate. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/graph/edge_aggregation.md`
- Saturation measurements
- The implemented ruling
- A splitting-invariance property

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The aggregation rule is stated formally and tested as an invariant.
- [ ] Saturation frequency and lost variation are measured on generated markets.
- [ ] Edge kinds round-trip losslessly.
- [ ] Splitting one coupling across kinds provably leaves every score unchanged.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.
- Jackson, M. O. (2008). *Social and Economic Networks*. Princeton University Press.
- Barabasi, A.-L. (2016). *Network Science*. Cambridge University Press.
- Cont, R., Moussa, A., & Santos, E. B. (2013). "Network structure and systemic risk in banking systems." In Fouque, J.-P. & Langsam, J. (eds.), *Handbook on Systemic Risk*. Cambridge University Press.
- Acemoglu, D., Ozdaglar, A., & Tahbaz-Salehi, A. (2015). "Systemic Risk and Stability in Financial Networks." *American Economic Review* 105(2), 564-608.

## 11. Commit protocol

Commits from this project use the scope `p24`:

```text
docs(p24): formalise multi-kind edge aggregation and the saturation cap
test(p24): measure saturation frequency and prove splitting invariance
fix(p24): adopt the ruled aggregation semantics
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
