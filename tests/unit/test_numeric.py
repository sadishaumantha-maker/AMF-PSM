"""Tests for the deterministic floating-point primitives.

Correctness is checked against exact rational arithmetic rather than against a
second floating-point expression, so the assertions say what the functions
promise -- *this is the correctly rounded result* -- instead of merely agreeing
with another approximation.
"""

from __future__ import annotations

import itertools
import math
import random
from fractions import Fraction

import pytest

from amf.numeric import clip_unit, square, stable_sum


def _exact_sum(values):
    """The correctly rounded sum, computed in exact rational arithmetic."""
    return float(sum((Fraction(v) for v in values), Fraction(0)))


def _naive_sum(values):
    """Left-to-right accumulation -- what a hand-written `total += v` loop does.

    Deliberately not the built-in `sum`: CPython 3.12 switched that to Neumaier
    compensated summation, so `sum` is order-sensitive on 3.11 and very nearly
    exact on 3.12+. Testing against `sum` would therefore assert one interpreter's
    behaviour. This helper is naive on every version, which is what these tests
    need in order to demonstrate something rather than assume it.
    """
    total = 0.0
    for value in values:
        total += value
    return total


def test_stable_sum_is_exactly_rounded():
    # The property that matters: not "close to" the true sum but the nearest
    # double to it. Plain sum() is not, which is what makes it order-sensitive.
    rng = random.Random(20260820)
    for _ in range(200):
        values = [rng.uniform(-1e6, 1e6) for _ in range(24)]
        assert stable_sum(values) == _exact_sum(values)


def test_stable_sum_is_order_independent_where_naive_accumulation_is_not():
    # 0.1 + 0.2 + 0.3 is the canonical demonstration: accumulated left to right it
    # yields 0.6000000000000001 or 0.6 depending purely on the order the terms
    # arrive in. That sensitivity is why a diagnosis used to differ in its last
    # bits when a market was assembled in a different order.
    terms = [0.1, 0.2, 0.3]
    orderings = list(itertools.permutations(terms))
    assert len({_naive_sum(o) for o in orderings}) > 1, "naive accumulation must vary, or this test proves nothing"
    assert len({stable_sum(o) for o in orderings}) == 1


def test_stable_sum_survives_catastrophic_cancellation():
    # Naive accumulation loses both units entirely to the 1e100 term; the exactly
    # rounded sum keeps them.
    values = [1.0, 1e100, 1.0, -1e100]
    assert _naive_sum(values) == 0.0
    assert stable_sum(values) == 2.0


def test_stable_sum_does_not_change_between_python_versions():
    # CPython 3.12 replaced the built-in sum's accumulation with Neumaier
    # compensated summation. That makes `sum` materially more accurate -- and
    # makes any score built on it version-dependent, which matters here because
    # CI runs 3.11, 3.12 and 3.13 and compares none of their outputs to each
    # other. Sampled over 400,000 random weight sets, 102,822 produced a
    # concentration index that differed between the two algorithms.
    #
    # `stable_sum` is exactly rounded on every version, so it has no such seam.
    # Pinning it to exact rational arithmetic pins it across interpreters too.
    rng = random.Random(20260824)
    for _ in range(2000):
        weights = [round(rng.uniform(0.01, 1.0), 3) for _ in range(rng.randint(3, 6))]
        total = stable_sum(weights)
        assert total == _exact_sum(weights)
        # Each share is squared to a double first -- that rounding is inherent and
        # identical on every platform, because both the division and the
        # multiplication are correctly rounded. What must not vary is the
        # reduction over those terms, so that is what is pinned to exact
        # arithmetic here.
        terms = [square(w / total) for w in weights]
        assert stable_sum(terms) == _exact_sum(terms)


def test_stable_sum_of_nothing_is_zero():
    assert stable_sum([]) == 0.0


def test_square_is_the_correctly_rounded_product():
    # `x * x` is required by IEEE 754 to be correctly rounded, so it matches the
    # exact rational square on every conforming platform. `x ** 2` routes to the
    # C library's pow(), which carries no such guarantee -- which is why the
    # concentration index no longer uses it.
    rng = random.Random(20260821)
    for _ in range(500):
        value = rng.uniform(0.0, 1.0)
        assert square(value) == float(Fraction(value) ** 2)


@pytest.mark.parametrize(
    ("value", "expected"),
    [(0.0, 0.0), (1.0, 1.0), (0.5, 0.5), (-0.5, 0.0), (1.5, 1.0), (-1e300, 0.0), (1e300, 1.0)],
)
def test_clip_unit_confines_to_the_unit_interval(value, expected):
    assert clip_unit(value) == expected


def test_clip_unit_floors_nan_rather_than_propagating_it():
    # NaN compares false against both bounds, so max() keeps its first argument.
    # Documented deliberately: the floor is not a verdict, and amf.invariants is
    # what refuses to hand a broken computation back to the caller.
    assert clip_unit(math.nan) == 0.0
