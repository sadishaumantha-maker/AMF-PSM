"""Integration tests that run the CLI as a real process.

Every other CLI test calls ``amf.cli.main`` in-process, which never exercises the
``[project.scripts]`` entry point or the ``__main__`` block. A broken console
script declaration would otherwise ship green.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from amf import __version__

SAMPLE = Path(__file__).resolve().parents[2] / "examples" / "sample_market.json"

# No sys.path shim exists in conftest, so `import amf` only works when the
# package is installed -- which means the console script is always present in any
# environment where this suite runs at all. A skip here would be a silent hole.
AMF = shutil.which("amf")


@pytest.mark.integration
def test_console_script_is_installed():
    assert AMF is not None, "the `amf` console script is missing from the environment"


@pytest.mark.integration
def test_console_script_reports_the_version():
    result = subprocess.run([AMF, "version"], capture_output=True, text=True, check=False)
    assert result.returncode == 0
    assert result.stdout.strip() == __version__


@pytest.mark.integration
def test_module_entry_point_reports_the_version():
    # Covers the `if __name__ == "__main__"` block, which is pragma: no cover.
    result = subprocess.run([sys.executable, "-m", "amf.cli", "version"], capture_output=True, text=True, check=False)
    assert result.returncode == 0
    assert result.stdout.strip() == __version__


@pytest.mark.integration
def test_console_script_keeps_json_on_stdout_and_the_disclaimer_on_stderr():
    import json

    result = subprocess.run(
        [AMF, "diagnose", str(SAMPLE), "--format", "json"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    # Through a real process, not capsys: stdout must be machine-readable.
    assert "overall_index" in json.loads(result.stdout)
    assert "not financial advice" in result.stderr.lower()


@pytest.mark.integration
def test_console_script_reports_a_missing_file_as_exit_code_two():
    result = subprocess.run([AMF, "diagnose", "no-such-market.json"], capture_output=True, text=True, check=False)
    assert result.returncode == 2
    assert "error:" in result.stderr
