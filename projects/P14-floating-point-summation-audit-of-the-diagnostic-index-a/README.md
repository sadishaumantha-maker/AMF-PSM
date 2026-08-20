# P14 - Floating-point summation audit of the diagnostic index and HHI

**Track C - Numerical Correctness & Determinism**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Numerical analyst |
| **Upstream** | `CLAUDE.md` -> Determinism; `src/amf/diagnostics.py` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

> [!IMPORTANT]
> **Status against `main`.** **Substantially superseded on `main`.** `amf.numeric.stable_sum` now performs exactly-rounded
> accumulation across every scoring path, and `amf.numeric.square` replaces `x ** 2` because IEEE 754
> requires multiplication to be correctly rounded while `libm`'s `pow` does not. That answers this
> charter's central question - canonical ordering was *not* sufficient, and the repository chose exact
> rounding over compensated summation.
>
> What remains for this charter, and only this: the **error-bound inventory** the landed change did not
> produce. Exact rounding removes order-dependence; it does not by itself bound the error of the
> *derived* quantities, nor does it cover the ensemble percentile machinery (owned by P19). Rewrite the
> dispute in section 1 before starting, and treat sections 4-5 as an audit of what `stable_sum` does and
> does not guarantee rather than a proposal to introduce it.

---

## 1. The dispute this project settles

`CLAUDE.md` records that insertion-ordered traversal once made a diagnosis differ in its last bits, because the concentration HHI sums over a list and floating-point addition is not associative. The fix was canonical ordering. The open dispute is whether canonical ordering is *sufficient*, or whether the summations themselves need compensated arithmetic to be defensible as a scientific instrument.

## 2. Purpose

Audit every accumulation in the scoring pipeline for error growth, quantify the worst-case and observed error, and decide - on measured evidence - between naive summation, pairwise summation and compensated (Kahan-Neumaier) summation.

## 3. Scope

**In scope**

- An inventory of every floating-point accumulation in `diagnostics.py`, `simulation.py` and `sensitivity.py`.
- A forward-error bound per accumulation using standard results for summation.
- An empirical worst-case search over admissible metric values in `[0, 1]`.
- A recommendation with a measured cost/benefit, implemented if it changes any reported digit.

**Out of scope**

- Changing the mathematical definition of any score - that is P27 to P32.
- Introducing numpy or any other runtime dependency.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Enumerate accumulations: the HHI share sum, the criticality-weighted mean, the feedback edge-weight products, the stress-vector inner loop, and the ensemble percentile machinery.
2. For each, write the standard forward error bound in terms of the condition number of the sum and the number of terms.
3. Note that with seven systems the term count is small; state explicitly where the bound is therefore negligible and where the condition number, not the length, is the risk.
4. Search empirically for adversarial inputs inside the admissible `[0, 1]` box that maximise observed relative error against an exact rational or extended-precision reference.
5. Only where the observed error can change a reported digit or flip a `Severity` band, implement compensated summation.
6. Record the decision and the measurements; a change with no measured effect is not made.

## 5. Task board

- [ ] Build the accumulation inventory with file and line references.
- [ ] Derive the per-accumulation error bound.
- [ ] Implement an extended-precision reference oracle for testing only.
- [ ] Run the adversarial search inside the admissible box.
- [ ] Implement compensated summation where justified.
- [ ] Add regression tests pinning the chosen behaviour.
- [ ] Publish `docs/numerics/summation_audit.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `numerics-auditor`

- **Mandate:** Inventory every accumulation and derive its forward error bound.
- **Inputs:** `src/amf/diagnostics.py`, `simulation.py`, `sensitivity.py`.
- **Output artifact:** `docs/numerics/summation_audit.md`.
- **Stop condition:** Every accumulation has a bound and a verdict of `negligible` or `at risk`.

### `benchmark-runner`

- **Mandate:** Run the adversarial error search against an exact reference and report the maximum observed relative error.
- **Inputs:** The accumulation inventory.
- **Output artifact:** A measurement table with the exact reproduction command.
- **Stop condition:** The search has converged or a `Severity` band flip has been demonstrated.

### `algorithm-implementer`

- **Mandate:** Implement compensated summation only where the measurement justifies it.
- **Inputs:** Measurement table.
- **Output artifact:** A minimal diff under `src/amf/`.
- **Stop condition:** `mypy` strict passes, no new dependency, and the diff touches only justified accumulations.

### `determinism-prover`

- **Mandate:** Prove the change preserves permutation invariance and reproduces prior results where no digit changed.
- **Inputs:** The diff.
- **Output artifact:** Property and regression tests.
- **Stop condition:** Permutation invariance holds and every intentionally changed digit is listed in the CHANGELOG.

**Hand-off order:** `numerics-auditor` -> `benchmark-runner` -> `algorithm-implementer` -> `determinism-prover`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-float-audit` | Any accumulation or ordering is touched | Locates accumulations, derives bounds and compares against an extended-precision oracle. |
| `amf-determinism-audit` | After any numerical change | Runs permutation and repeat-run invariance checks across the public API. |
| `amf-changelog-entry` | A reported digit changes | Records the change under `Changed` with the driving measurement. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/numerics/summation_audit.md`
- An adversarial measurement table
- Any justified summation change with regression tests

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every accumulation has a documented bound and verdict.
- [ ] The maximum observed relative error is measured, not assumed.
- [ ] Any behavioural change is recorded in `CHANGELOG.md` with the measurement that justified it.
- [ ] Permutation invariance and the 100% coverage gate both still pass.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Goldberg, D. (1991). "What Every Computer Scientist Should Know About Floating-Point Arithmetic." *ACM Computing Surveys* 23(1), 5-48.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms* (2nd ed.). SIAM.
- Kahan, W. (1965). "Further remarks on reducing truncation errors." *Communications of the ACM* 8(1), 40.
- IEEE (2019). *IEEE Standard for Floating-Point Arithmetic* (IEEE Std 754-2019).
- Wilkinson, J. H. (1963). *Rounding Errors in Algebraic Processes*. Prentice Hall.
- Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations* (4th ed.). Johns Hopkins University Press.

## 11. Commit protocol

Commits from this project use the scope `p14`:

```text
docs(p14): publish the floating-point accumulation inventory and error bounds
test(p14): add an extended-precision reference oracle and adversarial search
fix(p14): use compensated summation where the measured error can flip a severity band
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

