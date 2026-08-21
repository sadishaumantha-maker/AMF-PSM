"""Deterministic floating-point primitives shared by the analytical engines.

The toolkit is a diagnostic instrument, so identical inputs must give identical
output -- bit for bit, on every platform and Python version. Plain arithmetic
does not give that for free, and the two traps this module closes are both
subtle enough to have been live in the package:

* **Order-dependent accumulation.** Floating-point addition is not associative,
  so a sum whose terms arrive in a different order can differ in its last bits.
  Canonicalising traversal order (as :mod:`amf.graph` and :mod:`amf.market` do)
  removes the *observable* variation only where the order is under the engine's
  control. :func:`stable_sum` removes the sensitivity itself: it is exactly
  rounded, so every permutation of the same terms yields the identical double.
* **Platform-dependent operators.** ``x ** 2`` dispatches to the platform's
  ``libm`` ``pow``, which is not required to be correctly rounded and does
  differ between C libraries; measured on CPython 3.11/x86-64, ``x ** 2`` and
  ``x * x`` disagree for roughly 1 double in 1 200. IEEE 754 *does* require
  multiplication to be correctly rounded, so :func:`square` is identical
  everywhere.

Nothing here is a market quantity; these are numeric utilities. The module sits
at the bottom of the dependency order alongside :mod:`amf.errors` and
:mod:`amf.models` and imports nothing from the package.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable


def stable_sum(values: Iterable[float]) -> float:
    """Return the exactly-rounded sum of ``values``.

    Unlike the built-in :func:`sum`, the result does not depend on the order the
    terms are supplied in: it is the correctly rounded double nearest the exact
    mathematical sum. Any permutation of the same terms therefore returns the
    identical value, which is what lets two equal markets score identically no
    matter how they were assembled.

    Args:
        values: The terms to add.

    Returns:
        The exactly-rounded sum; ``0.0`` for an empty iterable.
    """
    return math.fsum(values)


def square(value: float) -> float:
    """Return ``value`` squared, reproducibly across platforms.

    Written as a multiplication rather than ``value ** 2`` deliberately. IEEE 754
    requires multiplication to be correctly rounded, so this returns the same
    double on every conforming platform; ``**`` routes to the C library's ``pow``
    and carries no such guarantee.

    Args:
        value: The number to square.

    Returns:
        ``value * value``.
    """
    return value * value


def clip_unit(value: float) -> float:
    """Clamp ``value`` into the unit interval ``[0, 1]``.

    This is the single place the toolkit enforces the interval that
    :class:`~amf.models.Severity` and every score type document and rely on.

    ``NaN`` clamps to ``0.0``, because it compares false against both bounds and
    the ``max`` therefore keeps its first argument. That is a floor, not a
    verdict: a ``NaN`` reaching this function means a broken upstream
    computation, and :mod:`amf.invariants` is what refuses to return it.

    Args:
        value: The number to clamp.

    Returns:
        ``value`` confined to ``[0, 1]``.
    """
    return min(1.0, max(0.0, value))
