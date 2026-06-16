"""Command-line interface for the :mod:`amf` toolkit.

Exposes ``diagnose``, ``simulate``, ``stress-test``, ``describe``, and
``version`` subcommands. ``main`` returns a process exit code so it can be unit
tested without spawning a subprocess.

The ``describe`` text is generated from the paraphrased constants below rather
than by reading the proprietary framework document, so the CLI never touches the
checksum-protected artifacts.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import TYPE_CHECKING

from amf import __version__
from amf.diagnostics import DiagnosticEngine
from amf.errors import AMFError
from amf.market import Market
from amf.models import Shock, SystemKind

if TYPE_CHECKING:
    from collections.abc import Sequence
from amf.report import render_json, render_markdown, render_stress_test, render_text
from amf.simulation import ShockSimulator

# Paraphrased, general descriptions of the seven systems and the analytical
# method. These are summaries written for this tool; the authoritative framework
# lives in the (protected) framework document.
_SYSTEM_SUMMARY: dict[SystemKind, str] = {
    SystemKind.SKELETON: "Infrastructure that gives the market shape and stability.",
    SystemKind.CIRCULATORY: "Channels through which capital and liquidity move.",
    SystemKind.NERVOUS: "Information and signals that coordinate participants.",
    SystemKind.MUSCULATURE: "Active participants that drive market movement.",
    SystemKind.ORGANS: "Specialised, interdependent functional subsystems.",
    SystemKind.IMMUNE: "Risk controls and regulation defending market integrity.",
    SystemKind.METABOLISM: "Rate at which value is created, recycled, or destroyed.",
}

_METHOD_STEPS: tuple[str, ...] = (
    "Define the market boundary (asset class, geography, timeframe).",
    "Map each anatomical system to its concrete market counterpart.",
    "Identify dependencies and feedback loops between systems.",
    "Diagnose structural weaknesses and single points of failure.",
    "Derive actionable insights or intervention points.",
)

# Shown after every analytical command. Printed to stderr so machine-readable
# stdout (e.g. `--format json`) stays clean and parseable.
_DISCLAIMER = (
    "Note: illustrative/educational structural model only — inputs and thresholds "
    "are not validated; not financial advice and not a diagnosis or forecast of any "
    "real or live market. Results describe the supplied hypothetical model only."
)


def _print_disclaimer() -> None:
    """Print the governance disclaimer to stderr."""
    print(_DISCLAIMER, file=sys.stderr)


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI and return a process exit code.

    Args:
        argv: Argument vector excluding the program name; defaults to ``sys.argv``.

    Returns:
        ``0`` on success, ``2`` on a handled AMF error, ``1`` on bad usage.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 1
    try:
        return int(handler(args))
    except AMFError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


def _build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser with all subcommands."""
    parser = argparse.ArgumentParser(prog="amf", description="Anatomical Market Framework toolkit.")
    sub = parser.add_subparsers(dest="command")

    diag = sub.add_parser("diagnose", help="Diagnose a market's structural weaknesses.")
    diag.add_argument("market", type=Path, help="Path to a market JSON file.")
    _add_format(diag)
    diag.set_defaults(handler=_cmd_diagnose)

    sim = sub.add_parser("simulate", help="Propagate a shock through a market.")
    sim.add_argument("market", type=Path, help="Path to a market JSON file.")
    sim.add_argument("--target", required=True, choices=[k.value for k in SystemKind], help="System to shock.")
    sim.add_argument("--magnitude", type=float, default=0.8, help="Shock magnitude in (0, 1].")
    _add_format(sim)
    sim.set_defaults(handler=_cmd_simulate)

    st = sub.add_parser("stress-test", help="Shock every system in turn.")
    st.add_argument("market", type=Path, help="Path to a market JSON file.")
    st.add_argument("--magnitude", type=float, default=0.8, help="Shock magnitude in (0, 1].")
    st.set_defaults(handler=_cmd_stress_test)

    desc = sub.add_parser("describe", help="Describe the seven systems and the method.")
    desc.set_defaults(handler=_cmd_describe)

    ver = sub.add_parser("version", help="Print the package version.")
    ver.set_defaults(handler=_cmd_version)

    return parser


def _add_format(parser: argparse.ArgumentParser) -> None:
    """Add the shared ``--format`` option."""
    parser.add_argument(
        "--format",
        choices=["text", "json", "md"],
        default="text",
        help="Output format.",
    )


def _load_market(path: Path) -> Market:
    """Load and parse a market JSON file."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise AMFError(f"cannot read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise AMFError(f"invalid JSON in {path}: {exc}") from exc
    return Market.from_dict(data)


def _cmd_diagnose(args: argparse.Namespace) -> int:
    """Handle the ``diagnose`` subcommand."""
    market = _load_market(args.market)
    report = DiagnosticEngine().diagnose(market)
    print(_format(report, args.format))
    _print_disclaimer()
    return 0


def _cmd_simulate(args: argparse.Namespace) -> int:
    """Handle the ``simulate`` subcommand."""
    market = _load_market(args.market)
    shock = Shock(target=SystemKind(args.target), magnitude=args.magnitude)
    trace = ShockSimulator(market).propagate(shock)
    print(_format(trace, args.format))
    _print_disclaimer()
    return 0


def _cmd_stress_test(args: argparse.Namespace) -> int:
    """Handle the ``stress-test`` subcommand."""
    market = _load_market(args.market)
    profile = ShockSimulator(market).stress_test(magnitude=args.magnitude)
    print(render_stress_test(profile))
    _print_disclaimer()
    return 0


def _cmd_describe(_: argparse.Namespace) -> int:
    """Handle the ``describe`` subcommand."""
    print("Anatomical Market Framework - seven systems:")
    for kind in SystemKind:
        print(f"  {kind.value:<12} {_SYSTEM_SUMMARY[kind]}")
    print("\nAnalytical method:")
    for i, step in enumerate(_METHOD_STEPS, start=1):
        print(f"  {i}. {step}")
    _print_disclaimer()
    return 0


def _cmd_version(_: argparse.Namespace) -> int:
    """Handle the ``version`` subcommand."""
    print(__version__)
    return 0


def _format(obj: object, fmt: str) -> str:
    """Render a result object in the requested format."""
    if fmt == "json":
        return render_json(obj)  # type: ignore[arg-type]
    if fmt == "md":
        return render_markdown(obj)  # type: ignore[arg-type]
    return render_text(obj)  # type: ignore[arg-type]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
