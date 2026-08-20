"""The example scripts are the documented on-ramp, so CI must actually run them.

`ruff` checks their style and `mypy` skips them by design, which left nothing
verifying that they still execute against the current API.
"""

from __future__ import annotations

import runpy
from pathlib import Path

import pytest

EXAMPLES = Path(__file__).resolve().parents[2] / "examples"


@pytest.mark.integration
@pytest.mark.parametrize("script", ["equity_market.py", "liquidity_shock.py"])
def test_example_script_runs(script: str, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch):
    # liquidity_shock imports its market builder from the sibling equity_market
    # module, so the examples directory has to be importable.
    monkeypatch.syspath_prepend(str(EXAMPLES))
    runpy.run_path(str(EXAMPLES / script), run_name="__main__")
    assert capsys.readouterr().out.strip(), "the example should print its analysis"


@pytest.mark.integration
def test_every_example_script_is_covered():
    # A new example must be added to the parametrisation above rather than
    # silently going unrun.
    scripts = {p.name for p in EXAMPLES.glob("*.py")}
    assert scripts == {"equity_market.py", "liquidity_shock.py"}
