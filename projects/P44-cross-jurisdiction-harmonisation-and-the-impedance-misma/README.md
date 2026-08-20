# P44 - Cross-jurisdiction harmonisation and the impedance-mismatch cost

**Track G - Policy Architecture & Regulatory Regimes**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Comparative regulation researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 1.1 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The discussion proposes an 'impedance mismatch cost' when markets operate under divergent regimes, and asks which policy layers are harmonisable and which are path-dependent. 'Impedance mismatch' is a borrowed metaphor with no definition, and until it has one the concept cannot be tested, implemented or refuted.

## 2. Purpose

Either give the mismatch concept a structural definition AMF can compute, or retire the metaphor and replace it with something the framework can actually represent.

## 3. Scope

**In scope**

- A structural definition attempt: mismatch as a property of the dependency graph across regime boundaries.
- A harmonisability assessment per policy layer, grounded in the legal-origins and path-dependence literature.
- A ruling: define, or retire and replace.

**Out of scope**

- Estimating any monetary cost of divergence.
- Any claim about compliance expenditure or trading behaviour.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State what the metaphor is trying to capture: a cost that arises at a boundary because two sides expect different things.
2. Attempt a structural definition in AMF terms: a dependency edge whose source and target sit under different regimes, weighted by tier distance.
3. Test whether that definition behaves sensibly on constructed examples, including full harmonisation and complete divergence.
4. Assess harmonisability per layer using the legal-origins and institutional-persistence evidence; some layers are demonstrably path-dependent.
5. If the structural definition fails the sensibility tests, retire the metaphor explicitly and say what replaces it.
6. Record the ruling so the term stops circulating undefined.

## 5. Task board

- [ ] State what the metaphor is meant to capture.
- [ ] Draft the structural definition in AMF terms.
- [ ] Test it on constructed boundary examples.
- [ ] Assess harmonisability per policy layer with citations.
- [ ] Rule: define or retire.
- [ ] Publish `docs/policy/harmonisation.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** Draft the structural definition and test it on constructed extremes.
- **Inputs:** The AMF graph model and the tier hierarchy.
- **Output artifact:** A definition section with worked extremes.
- **Stop condition:** Full harmonisation and complete divergence both produce sensible values, or the definition is rejected.

### `regime-comparativist`

- **Mandate:** Assess harmonisability per layer against the legal-origins and persistence evidence.
- **Inputs:** The reading list and the P40 tier hierarchy.
- **Output artifact:** A per-layer harmonisability table.
- **Stop condition:** Each layer is marked harmonisable, partially harmonisable or path-dependent with a citation.

### `red-team-critic`

- **Mandate:** Argue the metaphor should be retired and force the definition to earn its place.
- **Inputs:** The draft definition.
- **Output artifact:** A dissent section.
- **Stop condition:** The definition survives with evidence, or the metaphor is retired in writing.

### `boundary-sentinel`

- **Mandate:** Ensure no cost measure introduces monetary or market-data vocabulary.
- **Inputs:** The draft.
- **Output artifact:** A boundary report.
- **Stop condition:** All quantities remain dimensionless and structural.

**Hand-off order:** `math-formalizer` -> `regime-comparativist` -> `red-team-critic` -> `boundary-sentinel`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | A jurisdiction is compared | Produces the structured regime profile with primary-instrument citations. |
| `amf-boundary-check` | A cost concept is proposed | Rejects any monetary or market-data framing. |
| `amf-red-team` | A borrowed metaphor is being formalised | Argues for retiring it and forces the definition to justify itself. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/harmonisation.md`
- A structural definition or a written retirement
- A per-layer harmonisability table

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The metaphor is either defined structurally and tested, or retired in writing.
- [ ] Every layer's harmonisability assessment carries a citation.
- [ ] No quantity is monetary or derived from market data.
- [ ] The term no longer appears anywhere undefined.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- La Porta, R., Lopez-de-Silanes, F., Shleifer, A., & Vishny, R. W. (1998). "Law and Finance." *Journal of Political Economy* 106(6), 1113-1155.
- Djankov, S., La Porta, R., Lopez-de-Silanes, F., & Shleifer, A. (2008). "The law and economics of self-dealing." *Journal of Financial Economics* 88(3), 430-465.
- Pierson, P. (2000). "Increasing Returns, Path Dependence, and the Study of Politics." *American Political Science Review* 94(2), 251-267.
- North, D. C. (1990). *Institutions, Institutional Change and Economic Performance*. Cambridge University Press.
- Committee of Wise Men (2001). *Final Report of the Committee of Wise Men on the Regulation of European Securities Markets* (the Lamfalussy Report). European Commission.
- European Union (2014). *Directive 2014/65/EU on markets in financial instruments (MiFID II)*. Official Journal of the European Union.
- Basel Committee on Banking Supervision (2011). *Basel III: A global regulatory framework for more resilient banks and banking systems* (rev. June 2011). Bank for International Settlements.
- Kaufmann, D., Kraay, A., & Mastruzzi, M. (2010). "The Worldwide Governance Indicators: Methodology and Analytical Issues." World Bank Policy Research Working Paper 5430.

## 11. Commit protocol

Commits from this project use the scope `p44`:

```text
docs(p44): attempt a structural definition of cross-regime impedance mismatch
docs(p44): assess harmonisability per policy layer against the legal-origins evidence
docs(p44): rule on defining or retiring the impedance-mismatch metaphor
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

