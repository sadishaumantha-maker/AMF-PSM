# P77 - Behavioural drift in the platform beneath a determinism guarantee

**Track M - Live Defects and the Green-Main Obligation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Library maintainer |
| **Upstream** | P74; `CLAUDE.md` -> Determinism |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The package promises bit-identical output for identical input, and it is built on a platform that is explicitly allowed to change. CPython 3.12 changed `sum()`; a future release may change another primitive the engines rely on. The `x ** 2` versus `x * x` note in `amf/numeric.py` is the same hazard seen from the other side - the platform's `libm` already varies between C libraries. The dispute is what a determinism guarantee can honestly mean when the substrate is a moving target.

## 2. Purpose

State the determinism guarantee precisely enough to be true: which operations it covers, across which versions and platforms, and what would invalidate it. Then detect drift rather than discovering it in CI.

## 3. Scope

**In scope**

- A precise restatement of the guarantee: bit-identical across which versions, platforms and libc implementations.
- An inventory of every platform primitive the engines depend on for exact results.
- A drift detector: a golden-value test that fails when the platform changes a result.

**Out of scope**

- Vendoring a numeric runtime or adding a dependency to escape the problem.
- Weakening the guarantee to whatever currently happens to be true.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Enumerate the primitives: summation, multiplication, division, comparison, `math` functions, and the hashing and iteration order the canonicalisation relies on.
2. Classify each by what the standard actually guarantees. IEEE 754 requires correct rounding for the basic arithmetic operations and does not for transcendentals, which is exactly why `square` is written as a multiplication.
3. Restate the guarantee in those terms: exact where the standard requires it, and identified explicitly where it does not.
4. Build the drift detector as golden values - a small set of inputs with their expected exact outputs, checked on every supported version. When the platform changes underneath the package, this fails first and deliberately.
5. Note that golden values must be derived from an exact reference, not recorded from a run, or the detector encodes whatever the platform did that day.
6. Document what a contributor should do when the detector fires: it is a signal to investigate, not to update the golden value.

## 5. Task board

- [ ] Enumerate the platform primitives the engines rely on.
- [ ] Classify each against what the standard guarantees.
- [ ] Restate the determinism guarantee precisely.
- [ ] Build the golden-value drift detector from an exact reference.
- [ ] Document the response procedure when it fires.
- [ ] Publish `docs/numerics/platform_drift.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `numerics-auditor`

- **Mandate:** Enumerate and classify the primitives against the standard's actual guarantees.
- **Inputs:** `src/amf/`, IEEE 754, the language reference.
- **Output artifact:** `docs/numerics/platform_drift.md`.
- **Stop condition:** Every primitive is marked standard-guaranteed or platform-dependent.

### `math-formalizer`

- **Mandate:** Derive golden values from exact rational arithmetic, never from a recorded run.
- **Inputs:** The primitive inventory.
- **Output artifact:** A golden-value table with its derivation.
- **Stop condition:** Every golden value is reproducible from the exact reference.

### `determinism-prover`

- **Mandate:** Implement the drift detector across the supported version matrix.
- **Inputs:** The golden values.
- **Output artifact:** A test module.
- **Stop condition:** The detector passes on all supported versions and fails when a value is perturbed.

### `spec-drafter`

- **Mandate:** Restate the guarantee and write the response procedure.
- **Inputs:** The classification.
- **Output artifact:** A `CLAUDE.md` determinism-section revision.
- **Stop condition:** The restated guarantee is true as written, with its scope named.

**Hand-off order:** `numerics-auditor` -> `math-formalizer` -> `determinism-prover` -> `spec-drafter`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-determinism-audit` | The guarantee is restated | Runs permutation, repeat and cross-version invariance checks. |
| `amf-float-audit` | A primitive is classified | Checks it against an exact reference and identifies platform dependence. |
| `amf-invariant-spec` | A golden value is adopted | Writes the invariant and mirrors it as a failing-on-drift test. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/numerics/platform_drift.md`
- A primitive classification
- A golden-value drift detector
- A restated determinism guarantee

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every primitive is classified against what the standard guarantees.
- [ ] Golden values derive from exact arithmetic, not from a recorded run.
- [ ] The detector fails when any golden value is perturbed.
- [ ] The restated guarantee names its scope and is true as written.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- IEEE (2019). *IEEE Standard for Floating-Point Arithmetic* (IEEE Std 754-2019).
- Goldberg, D. (1991). "What Every Computer Scientist Should Know About Floating-Point Arithmetic." *ACM Computing Surveys* 23(1), 5-48.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms* (2nd ed.). SIAM.
- Wilkinson, J. H. (1963). *Rounding Errors in Algebraic Processes*. Prentice Hall.
- Python Software Foundation. *PEP 387: Backwards Compatibility Policy*.
- CPython issue gh-100425 / bpo tracker. "Improve accuracy of builtin sum() for float inputs" - the Neumaier compensated-summation change shipped in CPython 3.12.
- Shewchuk, J. R. (1997). "Adaptive Precision Floating-Point Arithmetic and Fast Robust Geometric Predicates." *Discrete & Computational Geometry* 18(3), 305-363.
- Sandve, G. K., Nekrutenko, A., Taylor, J., & Hovig, E. (2013). "Ten Simple Rules for Reproducible Computational Research." *PLoS Computational Biology* 9(10), e1003285.

## 11. Commit protocol

Commits from this project use the scope `p77`:

```text
docs(p77): classify the platform primitives the determinism guarantee rests on
test(p77): add a golden-value detector for platform behavioural drift
docs(p77): restate the determinism guarantee with its actual scope
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

