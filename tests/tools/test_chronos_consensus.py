"""Marzullo intersection: the piece that turns raw samples into a defensible bound."""

from __future__ import annotations

import pytest
from hypothesis import given
from hypothesis import strategies as st
from tools.chronos.consensus import intersect
from tools.chronos.errors import NoConsensusError
from tools.chronos.sources import Sample


def sample(name, offset, error):
    """Build a sample whose correctness interval is exactly offset +/- error."""
    return Sample(source=name, offset=offset, dispersion=error)


def test_no_samples_is_an_error_not_a_zero_offset():
    with pytest.raises(NoConsensusError, match="no samples"):
        intersect([])


def test_three_agreeing_sources_reach_consensus():
    result = intersect([sample("a", 0.010, 0.005), sample("b", 0.012, 0.005), sample("c", 0.009, 0.005)])
    assert result.truechimers == ("a", "b", "c")
    assert result.falsetickers == ()
    assert result.low <= 0.010 <= result.high


def test_a_falseticker_is_excluded_not_averaged_in():
    """A single wildly wrong server must not drag the answer, as a mean would."""
    result = intersect(
        [sample("a", 0.010, 0.005), sample("b", 0.011, 0.005), sample("c", 0.010, 0.005), sample("liar", 5.0, 0.001)]
    )
    assert result.falsetickers == ("liar",)
    assert abs(result.offset - 0.010) < 0.01


def test_two_sources_do_not_meet_the_default_floor():
    """Three is the smallest number that lets one liar be outvoted rather than merely noticed."""
    with pytest.raises(NoConsensusError, match="3 are required"):
        intersect([sample("a", 0.01, 0.005), sample("b", 0.01, 0.005)])


def test_minimum_can_be_relaxed_explicitly():
    result = intersect([sample("a", 0.01, 0.005), sample("b", 0.01, 0.005)], minimum=2)
    assert len(result.truechimers) == 2


def test_disjoint_sources_have_no_consensus():
    with pytest.raises(NoConsensusError):
        intersect([sample("a", 0.0, 0.001), sample("b", 10.0, 0.001), sample("c", 20.0, 0.001)])


def test_intervals_touching_at_a_point_still_overlap():
    result = intersect([sample("a", 0.0, 1.0), sample("b", 2.0, 1.0), sample("c", 1.0, 1.0)], minimum=3)
    assert result.low == pytest.approx(1.0)


def test_uncertainty_is_the_half_width_of_the_agreed_interval():
    result = intersect([sample(n, 0.0, 0.01) for n in "abc"])
    assert result.uncertainty == pytest.approx(0.01)


def test_a_precise_source_narrows_the_bound():
    """Consensus is an intersection, so the tightest agreeing source dominates."""
    wide = intersect([sample(n, 0.0, 0.1) for n in "abc"])
    tight = intersect([sample("a", 0.0, 0.1), sample("b", 0.0, 0.1), sample("c", 0.0, 0.001)])
    assert tight.uncertainty < wide.uncertainty


def test_to_dict_records_the_method_and_both_bounds():
    payload = intersect([sample(n, 0.02, 0.01) for n in "abc"]).to_dict()
    assert payload["method"] == "marzullo"
    assert payload["low_seconds"] < payload["offset_seconds"] < payload["high_seconds"]


# --- properties ---------------------------------------------------------------------

offsets = st.floats(min_value=-1.0, max_value=1.0, allow_nan=False, allow_infinity=False)
errors = st.floats(min_value=1e-6, max_value=0.5, allow_nan=False, allow_infinity=False)


@given(st.lists(st.tuples(offsets, errors), min_size=3, max_size=8))
def test_consensus_never_exceeds_the_widest_input(pairs):
    samples = [sample(f"s{i}", o, e) for i, (o, e) in enumerate(pairs)]
    try:
        result = intersect(samples, minimum=1)
    except NoConsensusError:
        return
    assert result.uncertainty <= max(e for _, e in pairs) + 1e-9


@given(st.lists(st.tuples(offsets, errors), min_size=3, max_size=8), st.randoms())
def test_result_is_invariant_under_input_order(pairs, rng):
    """Determinism: a market and any permutation of it must diagnose identically."""
    samples = [sample(f"s{i}", o, e) for i, (o, e) in enumerate(pairs)]
    shuffled = list(samples)
    rng.shuffle(shuffled)
    try:
        first = intersect(samples, minimum=1)
    except NoConsensusError:
        with pytest.raises(NoConsensusError):
            intersect(shuffled, minimum=1)
        return
    second = intersect(shuffled, minimum=1)
    assert (first.low, first.high) == (second.low, second.high)
    assert first.truechimers == second.truechimers


@given(st.lists(st.tuples(offsets, errors), min_size=3, max_size=8))
def test_every_truechimer_actually_contains_the_result(pairs):
    samples = [sample(f"s{i}", o, e) for i, (o, e) in enumerate(pairs)]
    try:
        result = intersect(samples, minimum=1)
    except NoConsensusError:
        return
    by_name = {s.source: s for s in samples}
    for name in result.truechimers:
        low, high = by_name[name].interval
        assert low <= result.offset <= high
