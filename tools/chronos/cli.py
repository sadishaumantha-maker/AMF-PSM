"""Command-line interface for the time attestation.

Exit codes are the contract the automation depends on, so they are distinct and stable:

* ``0`` -- VERIFIED. Enough independent sources agreed, inside budget.
* ``3`` -- UNVERIFIED. A time was recorded but not established.
* ``4`` -- FAILED. No attestation could be produced; usually the locale gate.
* ``2`` -- bad usage.

``3`` and ``4`` are deliberately not ``1``: a shell that treats any non-zero as "the
command broke" still stops, but a caller that wants to distinguish "the clock is
untrustworthy" from "the tool is broken" can.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from tools.chronos.attest import DEFAULT_BUDGET_SECONDS, Status, TimeAttestation, attest
from tools.chronos.sources import (
    DEFAULT_NTP_SERVERS,
    ChronySource,
    LocalClockSource,
    NtpSource,
    PpsSource,
    PtpSource,
    TimeSource,
)

EXIT_VERIFIED = 0
"""The attestation may be relied on."""

EXIT_USAGE = 2
"""Bad arguments."""

EXIT_UNVERIFIED = 3
"""A time was recorded, but its accuracy was not established."""

EXIT_FAILED = 4
"""No attestation could be produced at all."""

_STATUS_EXIT: dict[Status, int] = {
    Status.VERIFIED: EXIT_VERIFIED,
    Status.UNVERIFIED: EXIT_UNVERIFIED,
    Status.FAILED: EXIT_FAILED,
}


def build_sources(
    servers: list[str],
    *,
    use_chrony: bool = True,
    use_hardware: bool = True,
    timeout: float = 5.0,
) -> list[TimeSource]:
    """Assemble the source set to measure against.

    The hardware sources are included even though they are unavailable on an ordinary
    machine. Listing them makes their absence visible in the attestation's ``unreachable``
    block, which is more useful than silently omitting the only paths to sub-microsecond
    accuracy.

    Args:
        servers: NTP hostnames to query.
        use_chrony: Whether to interrogate a local ``chronyd``.
        use_hardware: Whether to include the GNSS/PPS and PTP plug-ins.
        timeout: Per-source timeout in seconds.

    Returns:
        The sources, in query order.
    """
    sources: list[TimeSource] = [NtpSource(server, timeout=timeout) for server in servers]
    if use_chrony:
        sources.append(ChronySource(timeout=timeout))
    if use_hardware:
        sources.extend([PpsSource(), PtpSource()])
    sources.append(LocalClockSource())
    return sources


def _build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser."""
    parser = argparse.ArgumentParser(
        prog="chronos",
        description="Measure this machine's clock error against independent sources and "
        "report a proven uncertainty bound.",
    )
    parser.add_argument(
        "command",
        choices=["attest", "check", "now"],
        help="attest: full record; check: exit code only; now: the attested local time.",
    )
    parser.add_argument(
        "--budget-ms",
        type=float,
        default=DEFAULT_BUDGET_SECONDS * 1000.0,
        help="Widest uncertainty, in milliseconds, that still counts as verified.",
    )
    parser.add_argument(
        "--min-sources",
        type=int,
        default=3,
        help="How many independent sources must agree (default: 3, the NTP floor).",
    )
    parser.add_argument(
        "--server",
        action="append",
        dest="servers",
        default=None,
        help="NTP server to query; repeatable. Defaults to four independent operators.",
    )
    parser.add_argument("--timeout", type=float, default=5.0, help="Per-source timeout in seconds.")
    parser.add_argument("--no-chrony", action="store_true", help="Skip the local chronyd query.")
    parser.add_argument("--no-hardware", action="store_true", help="Skip the GNSS/PPS and PTP plug-ins.")
    parser.add_argument("--out", type=Path, default=None, help="Write the attestation JSON to this path.")
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format.",
    )
    return parser


def render(attestation: TimeAttestation, command: str, output_format: str) -> str:
    """Render an attestation for the given command and format."""
    if output_format == "json":
        return attestation.to_json()
    if command == "now":
        return attestation.render() + "\n"
    lines = [
        f"status      : {attestation.status.value}",
        f"local       : {attestation.local().isoformat()}  ({attestation.utc().isoformat()} UTC)",
    ]
    bound = attestation.uncertainty_seconds
    lines.append(
        f"uncertainty : ±{bound * 1000:.3f} ms  (budget ±{attestation.budget_seconds * 1000:.3f} ms)"
        if bound is not None
        else f"uncertainty : not established  (budget ±{attestation.budget_seconds * 1000:.3f} ms)"
    )
    if attestation.reason:
        lines.append(f"reason      : {attestation.reason}")
    if attestation.consensus is not None:
        lines.append(f"agreed by   : {', '.join(attestation.consensus.truechimers)}")
        if attestation.consensus.falsetickers:
            lines.append(f"rejected    : {', '.join(attestation.consensus.falsetickers)}")
    for name, why in sorted(attestation.unreachable.items()):
        lines.append(f"unreachable : {name}: {why}")
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    """Run the requested command.

    Args:
        argv: Argument vector; ``None`` reads ``sys.argv``.

    Returns:
        A process exit code, per this module's constants.
    """
    args = _build_parser().parse_args(argv)
    if args.budget_ms <= 0:
        print("chronos: --budget-ms must be positive")
        return EXIT_USAGE
    if args.min_sources < 1:
        print("chronos: --min-sources must be at least 1")
        return EXIT_USAGE

    sources = build_sources(
        list(args.servers or DEFAULT_NTP_SERVERS),
        use_chrony=not args.no_chrony,
        use_hardware=not args.no_hardware,
        timeout=args.timeout,
    )
    attestation = attest(
        sources,
        budget_seconds=args.budget_ms / 1000.0,
        minimum_sources=args.min_sources,
    )

    if args.command != "check" or args.format == "json":
        print(render(attestation, args.command, args.format), end="")
    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(attestation.to_json(), encoding="utf-8")
    return _STATUS_EXIT[attestation.status]
