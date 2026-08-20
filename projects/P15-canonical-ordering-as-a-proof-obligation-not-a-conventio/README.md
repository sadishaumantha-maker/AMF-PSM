# P15 - Canonical ordering as a proof obligation, not a convention

**Track C - Numerical Correctness & Determinism**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 4 days |
| **Lead role** | Numerical analyst |
| **Upstream** | `CLAUDE.md` -> Determinism; `tests/unit/test_properties.py` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Canonical ordering is currently enforced in four separate places - `DependencyGraph`, `Market.assemble`, `to_dict`, and both diagnostic tie-breaks - by convention and one property test. The dispute is whether a single property test over permutations is adequate evidence, given that `musculature` and `metabolism` share a criticality of 0.60 and ties are routine.

## 2. Purpose

Turn ordering from a convention into a stated, tested proof obligation: enumerate every place where iteration order can reach an output, prove each is canonicalised, and make an unordered traversal fail loudly.

## 3. Scope

**In scope**

- An exhaustive inventory of order-sensitive code paths from input parsing through to rendered output.
- A per-path canonicalisation proof or a defect report.
- Strengthened property tests covering ties, near-ties and adversarial permutations.

**Out of scope**

- Changing any score definition.
- Relaxing any existing ordering guarantee.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Trace every path from `Market.from_dict` to `render_text`, `render_json`, `render_markdown` and the `viz` renderers, marking each iteration over a collection.
2. For each iteration, state the canonical key and where it is imposed.
3. Construct the exact tie cases the codebase admits, starting from the documented `musculature`/`metabolism` criticality tie.
4. Extend the hypothesis properties to generate permutations that specifically stress ties, not just random reorderings.
5. Where an iteration has no canonical key, treat it as a defect and fix it in the owning module.
6. Document the obligation so future contributors know that a new iteration requires a new canonical key.

## 5. Task board

- [ ] Build the order-sensitive path inventory.
- [ ] Record the canonical key for every path.
- [ ] Add tie-focused permutation properties.
- [ ] Fix any path lacking a canonical key.
- [ ] Publish `docs/numerics/ordering_obligation.md`.
- [ ] Add the obligation to the change checklist in `CLAUDE.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `determinism-prover`

- **Mandate:** Inventory order-sensitive paths and prove each is canonicalised.
- **Inputs:** `src/amf/` in full.
- **Output artifact:** `docs/numerics/ordering_obligation.md`.
- **Stop condition:** Every iteration in the inventory names its canonical key.

### `property-test-author`

- **Mandate:** Generate permutations that concentrate on ties and near-ties rather than uniform shuffles.
- **Inputs:** The inventory and the documented tie cases.
- **Output artifact:** New properties in `tests/unit/test_properties.py`.
- **Stop condition:** The suite includes at least one property that fails if any tie-break is removed.

### `red-team-critic`

- **Mandate:** Attempt to construct two equal markets that render differently.
- **Inputs:** The public API.
- **Output artifact:** A falsification attempt report.
- **Stop condition:** No differing render is found, or a defect is filed.

**Hand-off order:** `determinism-prover` -> `property-test-author` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-determinism-audit` | Any iteration over a collection is added | Checks the iteration has a canonical key and runs permutation invariance. |
| `amf-property-harness` | A new ordering invariant is claimed | Scaffolds a hypothesis property using `build_market()`. |
| `amf-red-team` | Before the obligation is declared met | Searches for two equal markets producing different rendered output. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/numerics/ordering_obligation.md`
- Tie-focused permutation properties
- Fixes for any uncanonicalised path

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every order-sensitive path names its canonical key.
- [ ] Removing any single tie-break causes a test failure.
- [ ] The red-team report finds no differing render for equal markets.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms* (2nd ed.). SIAM.
- Goldberg, D. (1991). "What Every Computer Scientist Should Know About Floating-Point Arithmetic." *ACM Computing Surveys* 23(1), 5-48.
- Claessen, K., & Hughes, J. (2000). "QuickCheck: a lightweight tool for random testing of Haskell programs." *ICFP '00*, 268-279.
- Hoare, C. A. R. (1969). "An Axiomatic Basis for Computer Programming." *Communications of the ACM* 12(10), 576-580.
- Meyer, B. (1988). *Object-Oriented Software Construction*. Prentice Hall. (design by contract)
- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.

## 11. Commit protocol

Commits from this project use the scope `p15`:

```text
docs(p15): state canonical ordering as an explicit proof obligation
test(p15): add tie-focused permutation properties for every ranking
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

