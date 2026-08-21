"""Deterministic fake time sources shared by the chronos tests.

A plain sibling module rather than a package import: there are no `__init__.py` files under
`tests/`, so pytest prepends each test file's own directory to `sys.path` and this is
importable by bare name from any test in `tests/tools/`.
"""

from __future__ import annotations

from tools.chronos.errors import SourceUnavailableError
from tools.chronos.sources import Sample


class Fixed:
    """A source that always returns the same measurement."""

    def __init__(self, name, offset, error):
        self._name = name
        self._sample = Sample(source=name, offset=offset, dispersion=error)

    @property
    def name(self):
        return self._name

    def sample(self):
        return self._sample


class Broken:
    """A source that is never reachable."""

    def __init__(self, name, why="not configured"):
        self._name = name
        self.why = why

    @property
    def name(self):
        return self._name

    def sample(self):
        raise SourceUnavailableError(self.why)


def agreeing(error=0.001, offset=0.0):
    """Return three sources that agree closely enough to reach consensus."""
    return [Fixed(f"s{i}", offset, error) for i in range(3)]
