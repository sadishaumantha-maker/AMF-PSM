# P17 - Completeness audit of tuning-knob validation

**Track C - Numerical Correctness & Determinism**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 4 days |
| **Lead role** | Library maintainer |
| **Upstream** | `DiagnosticConfig`, `SimulationConfig`, `SensitivityConfig`, `DependencyGraph.centrality` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

> [!IMPORTANT]
> **Status against `main`.** **Complemented by `main`, not superseded.** `amf.invariants` guards engine results on the way
> *out*; this charter guards tuning parameters on the way *in*. Both are needed, and the completeness
> question - is the set of input-domain validations complete? - is untouched by the new result-side
> guard. Section 4 should now state the relationship explicitly, so that a future contributor does not
> assume the output guard makes an input domain safe: a knob that produces a plausible-but-wrong score
> inside `[0, 1]` passes every invariant check.

---

## 1. The dispute this project settles

`CLAUDE.md` records two concrete failures caused by unvalidated knobs: a negative blend weight produced a finding scoring 2.0, and `alpha >= 10` overflowed the influence series to infinity and returned NaN for every system. Validation was added case by case. Nobody has shown the *set* of validations is complete.

## 2. Purpose

Establish a systematic completeness argument: for every tuning parameter, state the admissible domain, prove that the whole admissible domain keeps every score inside `[0, 1]`, and test the boundary of that domain.

## 3. Scope

**In scope**

- A parameter inventory across all configuration objects and validated method arguments.
- A domain justification per parameter tied to the invariant it protects.
- Boundary tests at every open and closed endpoint, including the all-zero weight triple.

**Out of scope**

- Changing default values - that is P29, P34 and P39.
- Adding new tuning knobs.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Enumerate every parameter, its declared domain and the exception raised on violation.
2. For each, name the downstream invariant it protects; `[0, 1]` score containment is the primary one because `Severity.from_score` and `WeaknessFinding` both rely on it.
3. Prove containment over the whole admissible domain, symbolically where the expression allows and by exhaustive boundary search otherwise.
4. Identify parameters whose admissible domain is currently wider than the containment proof supports; narrow the domain, do not weaken the invariant.
5. Test both sides of every endpoint, including the documented all-zero weight case that must remain legal.
6. Confirm every violation raises `InvalidConfigError`, never a bare `ValueError`.

## 5. Task board

- [ ] Build the parameter inventory table.
- [ ] Write the invariant-protection mapping.
- [ ] Prove or disprove containment over each domain.
- [ ] Narrow any domain the proof does not support.
- [ ] Add boundary tests at every endpoint.
- [ ] Publish `docs/numerics/config_domains.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** Produce the parameter inventory and the invariant-protection mapping.
- **Inputs:** All configuration dataclasses and validated methods.
- **Output artifact:** `docs/numerics/config_domains.md`.
- **Stop condition:** Every parameter names the invariant it protects.

### `math-formalizer`

- **Mandate:** Prove `[0, 1]` containment across each admissible domain, or produce the counterexample.
- **Inputs:** Score definitions and domains.
- **Output artifact:** A proof section per parameter.
- **Stop condition:** Each parameter has a proof or a counterexample; no parameter is left 'assumed safe'.

### `property-test-author`

- **Mandate:** Encode containment as hypothesis properties over the admissible domain.
- **Inputs:** Proof sections.
- **Output artifact:** Properties in `tests/unit/test_properties.py`.
- **Stop condition:** Scores remain in `[0, 1]` for any admissible configuration the generator produces.

### `unit-test-author`

- **Mandate:** Test both sides of every domain endpoint.
- **Inputs:** The inventory.
- **Output artifact:** Boundary cases in the matching unit test modules.
- **Stop condition:** Every open endpoint rejects and every closed endpoint accepts, with named tests.

**Hand-off order:** `spec-drafter` -> `math-formalizer` -> `property-test-author` -> `unit-test-author`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-config-validator` | A tuning knob is added or its domain changes | Adds validation raising `InvalidConfigError` and generates the matching boundary tests. |
| `amf-invariant-spec` | A containment claim is made | Writes the invariant into the docstring and mirrors it as a property. |
| `amf-property-harness` | Containment is claimed over a domain | Scaffolds the hypothesis property over that domain. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/numerics/config_domains.md` with proofs
- Narrowed domains where required
- Boundary and property tests

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every parameter has a proof of `[0, 1]` containment or a narrowed domain.
- [ ] Every domain endpoint has a test on both sides.
- [ ] All violations raise `InvalidConfigError`.
- [ ] The all-zero weight triple remains legal and yields zero scores.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms* (2nd ed.). SIAM.
- Meyer, B. (1988). *Object-Oriented Software Construction*. Prentice Hall. (design by contract)
- Hoare, C. A. R. (1969). "An Axiomatic Basis for Computer Programming." *Communications of the ACM* 12(10), 576-580.
- Claessen, K., & Hughes, J. (2000). "QuickCheck: a lightweight tool for random testing of Haskell programs." *ICFP '00*, 268-279.
- Horn, R. A., & Johnson, C. R. (2012). *Matrix Analysis* (2nd ed.). Cambridge University Press.
- Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., & Tarantola, S. (2008). *Global Sensitivity Analysis: The Primer*. Wiley.

## 11. Commit protocol

Commits from this project use the scope `p17`:

```text
docs(p17): prove score containment across every admissible configuration domain
fix(p17): narrow parameter domains the containment proof does not support
test(p17): add both-sided boundary tests for every configuration endpoint
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
