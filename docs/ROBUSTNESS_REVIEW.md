# Robustness & precision review — assessment of an external proposal

**Reviewer:** Claude Code, acting as senior engineer on the `amf` package
**Date:** 20 August 2026
**Subject:** an "AMF Advanced Robustness & Precision Enhancement" note proposing a
three-layer programme (Decimal arithmetic, invariants, stress scenarios, circuit
breakers, a validation suite, auto-configuration, and a provenance record) over 8–10 weeks.

> Prose only. This document has no authority over [`CLAUDE.md`](../CLAUDE.md),
> `pyproject.toml`, or the test suite; where it and the code disagree, the code wins.

---

## Verdict in one paragraph

The proposal's **goals are right and most of its mechanisms are wrong**. Its headline
justification for Decimal arithmetic — that JSON round-tripping loses precision — is
false for this codebase, and measurably so. Several of its code sketches do not run as
written, one of its two "safety" mechanisms is a no-op, and its provenance design would
break the repository's hardest rule outright. Meanwhile it did not find the three
reproducibility defects that were actually live in `main`. Two of those were caught by
taking the proposal's *intent* seriously and applying it with the right tools; all three
are now fixed, with regression tests.

The corrected programme is cheaper than the one proposed and strictly stronger: no new
dependency, no arithmetic rewrite, no API break, and a determinism guarantee the original
plan would not have delivered.

---

## 1. Baseline

Measured on this repository at the time of review, not quoted from the proposal:

| Property | Measured |
|---|---|
| Tests passing | 520 |
| Statement + branch coverage of `src/amf` | 100 % (gate is 100 %) |
| `ruff check`, `ruff format --check`, `mypy --strict` | all silent |
| Lines in `src/amf` | 3,536 |
| Lines of Python in the repository | 7,569 |
| Runtime dependencies | 0 |

The proposal states the codebase is "~2000" lines growing to "~3500". The starting figure
is already wrong by 1.8×, which matters because every effort estimate in its roadmap is
scaled from it.

---

## 2. Claim-by-claim assessment

Each verdict below was produced by running code against this repository, not by reading it.

### 2.1 "Round-trip serialization (JSON → Python → JSON) loses precision" — **false**

This is the proposal's primary argument for Decimal, and it does not hold. CPython has
emitted the shortest round-tripping repr since 3.1.

```
200,005 doubles round-tripped through json.dumps/json.loads → 0 mismatches
Market.to_dict() → from_dict() → to_dict() → byte-identical
```

The fixed-point property is already asserted by a hypothesis test in
`tests/unit/test_properties.py`. There is no precision to recover here.

### 2.2 "Weighted sums are order-dependent" — **true in general, already handled here, and now handled better**

The repository canonicalises traversal order throughout, and a hypothesis test asserts a
market diagnoses identically under any permutation of its assembly order. The proposal's
remedy — a `_canonical_sum` that sorts terms ascending and adds them as `Decimal` — is
both slower and less accurate than the stdlib answer, `math.fsum`, which returns the
correctly rounded sum in one linear pass with no ordering assumption at all.

Accuracy is not the only reason. Sorting ascending is *not* the accuracy-optimal ordering
in general; `fsum` is exact regardless.

### 2.3 `PrecisionContext` — **does not do what its docstring says**

The class is documented "Thread-safe, stateless". It stores `self._original`, so it is
stateful, and two threads sharing an instance corrupt each other's saved precision.
`decimal.localcontext()` in the standard library already solves this correctly. The
comment "28 is 84 bits" is also wrong: 28 decimal digits is about 93 bits.

### 2.4 `_canonical_sum(..., precision: Decimal | None)` — **raises on its own signature**

```python
with PrecisionContext(28 if precision is None else precision.as_tuple().exponent):
```

`Decimal.as_tuple().exponent` is negative for any fractional Decimal, so the non-default
path sets `getcontext().prec` to a negative integer, which raises `ValueError`. The
parameter cannot be exercised as designed.

### 2.5 `assert_unit_interval(..., strict)` — **dead parameter**

```python
lower, upper = (0.0, 1.0) if not strict else (0.0, 1.0)
```

Both branches are identical, so `strict` has no effect.

### 2.6 `assert_centrality_sum_bounded` — **name contradicts behaviour**

Section 2.1 of the proposal says centrality "sums to <= 1"; the function checks that the
*maximum* is ≤ 1. The maximum is the correct property — this project's centrality is
max-normalised — so the body is right and the name and the prose are wrong.

### 2.7 "Assertions after every operation" — **unsafe as specified**

```python
assert 0.0 <= result <= 1.0, f"metric out of bounds: {result}"
```

`assert` is removed by `python -O`. A guard that vanishes under optimisation is absent
exactly where a deployment is most likely to want it. The proposal's own `invariants.py`
sketch is inconsistent with itself here: its module docstring says "raise AssertionError"
while its code raises `InvariantViolation`.

Separately, `InvariantViolation` would fail this repository's linting: `ruff`'s `N818`
requires an exception name to end in `Error`, and every member of the existing hierarchy
does. The implemented class is `InvariantError`.

### 2.8 `RobustDiagnosticEngine._diagnose_high_precision` — **a no-op circuit breaker**

```python
def _diagnose_high_precision(self, market):
    with PrecisionContext(28):
        return super().diagnose(market)
```

`DiagnosticEngine` computes in `float`. A `decimal` context has no effect on `float`
arithmetic, so this recomputes bit-for-bit the same value that just failed the invariant
check, and either re-raises or — worse — returns the invalid report the caller was
supposed to be protected from. This is the most consequential defect in the proposal: the
mechanism presented as the safety net does nothing.

### 2.9 `ValidationSuite.validate_centrality` — **compares two different quantities**

The sketch computes Katz centrality and eigenvector centrality and raises unless they
agree to `1e-10`. They are different measures and will not agree on essentially any
non-trivial graph. `CLAUDE.md` records that Katz was chosen *because* eigenvector
centrality is not well defined on acyclic graphs, where it collapses to zero. Adopting
this check would make the suite fail on correct results.

A sound cross-check computes the *same* quantity two independent ways: Katz by iteration
versus Katz by linear solve, `(I − αA)^{-1}·1`. That is scheduled for D13.

### 2.10 `Provenance` with a wall-clock timestamp — **breaks the repository outright**

```python
@dataclass(frozen=True)
class Provenance:
    timestamp: float  # Seconds since epoch
    intermediate_steps: dict[str, Any]
```

Three separate problems:

1. `DiagnosticReport.to_dict()` feeds `render_json`. A wall-clock field makes two renders
   of the same market differ, breaking the byte-identity guarantee that `viz`'s tests
   assert directly.
2. Adding a required field to a frozen dataclass is a breaking change for every existing
   constructor call.
3. `dict` and `list` fields contradict the repository's convention that result types are
   frozen, slotted, and serialisable.

Provenance is still worth having — as a **content hash** of the market, the configuration
and the package version. That is deterministic, reproducible across machines, and
answers the same question ("what produced this number?") without a clock. Scheduled D11–D12.

### 2.11 `AdaptiveSimulationConfig` — **right instinct, wrong layer**

"If graph is bipartite: raise `InvalidConfigError` (centrality will fail)" attaches a
*centrality* precondition to a *simulation* config. `DependencyGraph.centrality` already
raises `InvalidDependencyError` for a graph with no dominant mode. And `damping=0.99` for
acyclic graphs is an unvalidated heuristic that would move every published resilience
score; presets should describe rather than silently retune (D14).

---

## 3. What the review found that the proposal did not

Three reproducibility defects were live in `main`. All three are fixed in this change.

### 3.1 `centrality` depended on the order dependencies were added — **fixed**

`DependencyGraph.centrality` accumulated influence with

```python
for (source, target), weight in self._pair_weights.items():
    nxt[target] += alpha * weight * frontier[source]
```

`_pair_weights` is a dict keyed in **insertion order**. Floating-point addition is not
associative, so listing identical couplings in a different order shifted the published
centralities.

```
examples/sample_market.json, 8 dependencies, random permutations:
  before:  265 / 400 permutations produced a different centrality vector
  after:     0 / 1000
```

This was a live breach of the project's headline rule — *nothing user-visible may depend
on the order a market was assembled in*. It is the single most serious finding in this
review, and the proposal's Decimal programme would not have caught it: Decimal addition
is not associative either.

The fix iterates incoming influence in system declaration order and reduces it with
`stable_sum`. Guarded by an exhaustive 720-permutation test in `tests/unit/test_graph.py`
and a hypothesis property in `tests/unit/test_properties.py`.

### 3.2 The resilience composite could go out of range on a multi-wave run — **fixed**

`ShockSimulator.propagate` extends the horizon to `max(max_steps, last injection step)`
so a late `Shock.at_step` is actually simulated — but `_score` divided the settling time
by `max_steps` regardless.

```
max_steps=5, shock at at_step=40:
  settling_time  = 14
  settle_penalty = 14 / 5   = 2.8
  settling term  = 0.15 × (1 − 2.8) = −0.27   (documented range for the term: [0, 0.15])
  resilience     = 0.291   →   0.659 after the fix
```

100 % branch coverage did not catch it, because every line involved was executed — just
with a denominator that was wrong for one input shape. That is the argument *for* the
proposal's invariants layer, made with a real example rather than a hypothetical one.

Single-shock runs are provably unaffected: their horizon equals `max_steps`, so the
penalty could never exceed 1.

### 3.3 `** 2` is not reproducible across platforms — **fixed**

`diagnostics.concentration` computed the Herfindahl index with `(w / total) ** 2`. The
`**` operator dispatches to the platform's `libm` `pow`, which is not required to be
correctly rounded; IEEE 754 *does* require multiplication to be.

```
x ** 2 != x * x  for 161 of 200,000 sampled doubles   (CPython 3.11, x86-64)
```

This — not JSON, not Decimal — is the actual obstacle to the proposal's stated goal of
bit-identical results across platforms, and the fix is one operator. Measured blast
radius on `examples/sample_market.json`: **zero**. Every concentration score is
byte-identical before and after.

---

## 4. What was implemented

Two new modules, no new dependency, no API break.

**`amf.numeric`** — `stable_sum` (exactly rounded via `math.fsum`, so the result cannot
depend on term order), `square` (a multiplication, so it is correctly rounded everywhere),
`clip_unit` (the single place the `[0, 1]` interval is enforced). Tested against exact
rational arithmetic with `fractions.Fraction`, so the assertions state what the functions
promise rather than agreeing with a second approximation.

**`amf.invariants`** — `InvariantError` plus `check_diagnostic_report`,
`check_simulation_trace`, `check_resilience_score`, `check_sensitivity_report`, and
`check_centrality`. Each returns its argument unchanged, so an engine adopts one by
wrapping its return value. They are wired into all four engines and are **always on**:
the cost is a handful of comparisons per result, so there is no flag to forget. Failures
raise, never `assert`.

One deliberate cost is recorded: reducing the diagnostic roll-up with `stable_sum` moves
the overall index by one unit in the last place on the sample market
(`0.27963855632147405` → `0.279638556321474`). The new value is the correctly rounded one;
the old was an accumulation-order artefact. No severity band moves, and it is written up
in `CHANGELOG.md`.

| | Proposed | Implemented |
|---|---|---|
| Numeric strategy | Decimal everywhere, 28 places | `math.fsum` + explicit multiplication; float throughout |
| New dependencies | none stated, but Decimal contexts everywhere | none |
| Invariants | `assert`-based, `strict` flag | raised `InvariantError`, always on |
| Circuit breaker | recomputes identically (no-op) | not built — it would have been theatre |
| Cross-check | Katz vs eigenvector (unsound) | Katz vs Katz-by-linear-solve (D13) |
| Provenance | wall-clock timestamp | content hash (D11–D12) |
| Defects fixed | — | 3, all with regression tests |
| Timeline | 8–10 weeks | 20 working days, Phases A–E |

---

## 5. Programme

Twenty working days, **Thu 20 Aug → Wed 16 Sep 2026**, one milestone per day in the
repository's [Milestones section](https://github.com/sadishaumantha-maker/AMF-PSM/milestones),
generated from [`.github/milestones.json`](../.github/milestones.json) by
[`tools/sync_milestones.py`](../tools/sync_milestones.py).

| Phase | Days | Theme |
|---|---|---|
| A | D01–D05 | Numerical determinism & invariants — *D01–D03 delivered* |
| B | D06–D10 | Stress-scenario corpus and golden regression outputs |
| C | D11–D15 | Deterministic provenance, sound cross-checks, operator surface |
| D | D16–D18 | Supply chain, release engineering, performance budget |
| E | D19–D20 | Model card and Day-20 review |

Creating those milestones also closes GAP 3 of the existing 90-day analysis
([issue #102](https://github.com/sadishaumantha-maker/AMF-PSM/issues/102), "No milestones"),
which had been open with the section empty.

---

## 6. Guardrails

Nothing here relaxes a hard rule. The new names (`numeric`, `invariants`, `stable_sum`,
`square`, `clip_unit`, `InvariantError`) all clear the non-trading `FORBIDDEN` list. No
wall clock and no unseeded randomness were introduced. The four checksum-protected
artifacts and `SHA256SUMS` are untouched. No publish workflow was added. Coverage remains
at 100 %, and the package still has zero runtime dependencies.

The `amf` package remains an illustrative, educational tool. Its thresholds, weights, and
scores are not empirically validated; nothing in this review changes that, and improved
numerical reproducibility must not be mistaken for improved predictive validity. Making a
number reproducible says nothing whatever about whether it is right.
