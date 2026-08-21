# P16 - Severity band totality and the NaN pessimism policy

**Track C - Numerical Correctness & Determinism**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 3 days |
| **Lead role** | Numerical analyst |
| **Upstream** | `src/amf/models.py` -> `Severity.from_score` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

> [!IMPORTANT]
> **Status against `main`.** **Narrowed by `main`.** `amf.invariants` now checks every engine result at the public
> boundary and raises `InvariantError` for a non-finite or out-of-range score, so a NaN can no longer
> reach `Severity.from_score` *through an engine*. The dispute survives for the direct path:
> `Severity.from_score` is public, still total, and still bands NaN as critical when called directly. The
> consumer analysis in step 1 should now distinguish the guarded engine path from the unguarded direct
> one, and the fail-safe/fail-loud argument applies only to the latter.

---

## 1. The dispute this project settles

`Severity.from_score` is total and saturates pessimistically: a score above one reports critical, and NaN - which compares false against every threshold - falls through to critical. The stated reason is that an escaped score means a broken upstream computation. The dispute is whether silently banding a NaN as critical is safer than raising, given that a silent critical is indistinguishable from a real one.

## 2. Purpose

Decide between silent pessimism and a loud failure on the evidence of how the value is consumed downstream, and make the chosen behaviour explicit, tested and documented at the call site.

## 3. Scope

**In scope**

- A consumer analysis: every place a `Severity` reaches a human or a machine-readable output.
- A comparison of silent pessimism against raising `AMFError` at the boundary.
- Explicit tests for the sub-zero, above-one and NaN cases.

**Out of scope**

- Changing the band thresholds themselves - that is P29 and P30.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Trace every consumer of `Severity`: text, markdown and JSON renderers, the CLI, and `viz` colouring.
2. For each consumer, state what a spurious critical would cause a reader to conclude.
3. Argue both options in writing, drawing on the fail-safe and fail-loud literature in dependable systems.
4. If silent pessimism is retained, ensure every renderer distinguishes a banded NaN from a genuine critical.
5. If raising is chosen, raise a typed `AMFError` subclass at the computation boundary, never a bare `ValueError`.
6. Pin the decision with explicit tests for each degenerate input.

## 5. Task board

- [ ] Build the `Severity` consumer map.
- [ ] Write the fail-safe versus fail-loud analysis.
- [ ] Implement the chosen behaviour.
- [ ] Add tests for score < 0, score > 1 and NaN.
- [ ] Update the docstring to state the policy at the point of use.
- [ ] Record any behavioural change in `CHANGELOG.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** Argue both options against dependable-systems practice and recommend one.
- **Inputs:** Consumer map, reading list.
- **Output artifact:** `docs/numerics/severity_policy.md`.
- **Stop condition:** The recommendation names the failure it prefers to have.

### `algorithm-implementer`

- **Mandate:** Implement the chosen policy in `models.py` with a typed error if raising is selected.
- **Inputs:** The decision.
- **Output artifact:** A diff under `src/amf/models.py`.
- **Stop condition:** No bare `ValueError` crosses the public API; `mypy` strict passes.

### `unit-test-author`

- **Mandate:** Pin every degenerate input with an explicit test.
- **Inputs:** The implementation.
- **Output artifact:** Cases in `tests/unit/test_models.py`.
- **Stop condition:** Sub-zero, above-one and NaN each have a named test.

**Hand-off order:** `spec-drafter` -> `algorithm-implementer` -> `unit-test-author`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-invariant-spec` | A total function's behaviour on degenerate input is decided | Writes the invariant into the docstring and mirrors it as a test. |
| `amf-float-audit` | NaN or infinity handling is in question | Checks comparison semantics and identifies silent fall-through branches. |
| `amf-changelog-entry` | Behaviour on degenerate input changes | Records the change under `Changed` or `Fixed`. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/numerics/severity_policy.md`
- The implemented policy
- Degenerate-input tests

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Behaviour for score < 0, score > 1 and NaN is explicitly tested.
- [ ] A banded NaN is distinguishable from a genuine critical in every output format, or the code raises instead.
- [ ] No bare standard-library exception escapes the public API.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- IEEE (2019). *IEEE Standard for Floating-Point Arithmetic* (IEEE Std 754-2019).
- Goldberg, D. (1991). "What Every Computer Scientist Should Know About Floating-Point Arithmetic." *ACM Computing Surveys* 23(1), 5-48.
- Perrow, C. (1984). *Normal Accidents: Living with High-Risk Technologies*. Princeton University Press.
- Nygard, M. T. (2018). *Release It! Design and Deploy Production-Ready Software* (2nd ed.). Pragmatic Bookshelf.
- Meyer, B. (1988). *Object-Oriented Software Construction*. Prentice Hall. (design by contract)
- Hoare, C. A. R. (1969). "An Axiomatic Basis for Computer Programming." *Communications of the ACM* 12(10), 576-580.

## 11. Commit protocol

Commits from this project use the scope `p16`:

```text
docs(p16): decide the severity policy for degenerate scores
fix(p16): make NaN and out-of-range severity handling explicit and tested
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
