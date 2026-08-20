"""Integration tests that run the shipped example scripts.

The README calls these "complete runnable scripts", but nothing executed them, so
they could rot silently. They are run as subprocesses rather than through
``runpy`` because ``liquidity_shock.py`` imports its sibling
(``from equity_market import build_market``), which only resolves because the
interpreter puts the script's own directory on ``sys.path``. A subprocess
therefore tests exactly the invocation the README documents.

Coverage is scoped to ``--cov=amf``, so these add no coverage; they are pure
regression guards.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

EXAMPLES = Path(__file__).resolve().parents[2] / "examples"


def _run(script: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(EXAMPLES / script)],
        capture_output=True,
        text=True,
        check=False,
    )


@pytest.mark.integration
def test_equity_market_example_runs():
    result = _run("equity_market.py")
    assert result.returncode == 0, result.stderr
    assert "Structural Diagnosis" in result.stdout


@pytest.mark.integration
def test_liquidity_shock_example_runs():
    result = _run("liquidity_shock.py")
    assert result.returncode == 0, result.stderr
    assert "Shock Propagation" in result.stdout
    assert "Systemic stress test" in result.stdout
