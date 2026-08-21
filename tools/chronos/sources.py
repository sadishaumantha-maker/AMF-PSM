"""Time sources, from a network round trip to a GNSS receiver.

Every source answers the same question -- "how far is this machine's clock from true time,
and how sure are you?" -- and returns the answer as a :class:`Sample` carrying both the
offset and an explicit error bound. A source that cannot bound its own error is not a source;
it raises :class:`~tools.chronos.errors.SourceUnavailableError` instead of guessing.
"""

from __future__ import annotations

import shutil
import socket
import struct
import subprocess
import time
from dataclasses import dataclass
from typing import Protocol

from tools.chronos.errors import SourceUnavailableError

_NTP_EPOCH_DELTA = 2_208_988_800
"""Seconds between the NTP epoch (1900-01-01) and the Unix epoch (1970-01-01)."""

_NTP_PACKET = "!B B B b 11I"
"""RFC 5905 header: flags, stratum, poll, precision, then eleven 32-bit words."""

_FRACTION = 2**32
"""Divisor converting an NTP fractional word to seconds."""

_FIXED_16_16 = 65536.0
"""Divisor for NTP's 16.16 fixed-point root delay and root dispersion."""

DEFAULT_NTP_SERVERS: tuple[str, ...] = (
    "time.cloudflare.com",
    "time.google.com",
    "pool.ntp.org",
    "time.nist.gov",
)
"""Independent, separately-operated servers. Independence is what makes a vote meaningful."""


@dataclass(frozen=True, slots=True)
class Sample:
    """One measurement of this machine's clock error.

    Attributes:
        source: Human-readable name of the source that produced it.
        offset: Seconds to add to the local clock to obtain true time.
        delay: Measured round-trip time in seconds; zero for a local source.
        dispersion: The source's own accumulated error estimate, in seconds.
        stratum: Distance from a reference clock, where 1 is a reference clock itself.
        root_delay: Total round-trip delay to the reference clock, in seconds.
        root_dispersion: Total dispersion to the reference clock, in seconds.
    """

    source: str
    offset: float
    delay: float = 0.0
    dispersion: float = 0.0
    stratum: int = 0
    root_delay: float = 0.0
    root_dispersion: float = 0.0

    @property
    def error(self) -> float:
        """Return the half-width of this sample's correctness interval, in seconds.

        This is NTP's root distance: half the measured round trip -- the most the unknown
        path asymmetry can have displaced the offset -- plus the error the upstream chain
        already admits to. It is the honest bound, and it is why an internet round trip
        cannot yield microseconds.
        """
        return self.delay / 2.0 + self.root_delay / 2.0 + self.root_dispersion + self.dispersion

    @property
    def interval(self) -> tuple[float, float]:
        """Return the closed interval that must contain the true offset."""
        return (self.offset - self.error, self.offset + self.error)


class TimeSource(Protocol):
    """A thing that can measure this machine's clock error."""

    @property
    def name(self) -> str:
        """Return a stable identifier for this source."""
        ...

    def sample(self) -> Sample:
        """Return one measurement.

        Raises:
            SourceUnavailableError: If the source cannot be reached or is not configured.
        """
        ...


class NtpSource:
    """An RFC 5905 client-mode NTP query over UDP, using the standard library only.

    One packet, four timestamps, the classic offset and delay formulae. No dependency, no
    daemon, and no reliance on the host clock being disciplined -- which matters because the
    whole point is to find out whether it is.
    """

    def __init__(self, server: str, *, timeout: float = 5.0, port: int = 123) -> None:
        """Configure a query against one server.

        Args:
            server: Hostname or address of the NTP server.
            timeout: Seconds to wait for a reply.
            port: UDP port; 123 except in tests.
        """
        self.server = server
        self.timeout = timeout
        self.port = port

    @property
    def name(self) -> str:
        """Return the server's hostname."""
        return self.server

    def sample(self) -> Sample:
        """Query the server once.

        Returns:
            The measured offset with its error bound.

        Raises:
            SourceUnavailableError: On any network failure, a short or malformed reply, or a
                server that declares itself unsynchronised.
        """
        request = bytearray(48)
        request[0] = 0x23  # leap 0, version 4, mode 3 (client)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(self.timeout)
        try:
            originate = time.time()
            sock.sendto(bytes(request), (self.server, self.port))
            payload, _ = sock.recvfrom(1024)
            destination = time.time()
        except (TimeoutError, OSError) as exc:
            raise SourceUnavailableError(f"{self.server}: {exc}") from exc
        finally:
            sock.close()

        if len(payload) < 48:
            raise SourceUnavailableError(f"{self.server}: short reply ({len(payload)} bytes)")

        flags, stratum, _poll, _precision, root_delay_raw, root_dispersion_raw, *rest = struct.unpack(
            _NTP_PACKET, payload[:48]
        )
        leap = flags >> 6
        if leap == 3:
            raise SourceUnavailableError(f"{self.server}: server reports itself unsynchronised (leap=3)")
        if not 1 <= stratum <= 15:
            raise SourceUnavailableError(f"{self.server}: unusable stratum {stratum}")

        # `rest` holds the nine words after root delay and root dispersion:
        # 0 reference id, 1-2 reference timestamp, 3-4 originate, 5-6 receive, 7-8 transmit.
        receive = rest[5] + rest[6] / _FRACTION - _NTP_EPOCH_DELTA
        transmit = rest[7] + rest[8] / _FRACTION - _NTP_EPOCH_DELTA

        offset = ((receive - originate) + (transmit - destination)) / 2.0
        delay = max((destination - originate) - (transmit - receive), 0.0)
        return Sample(
            source=self.server,
            offset=offset,
            delay=delay,
            stratum=stratum,
            root_delay=root_delay_raw / _FIXED_16_16,
            root_dispersion=root_dispersion_raw / _FIXED_16_16,
        )


class ChronySource:
    """Reads the locally disciplined clock's own statistics from ``chronyc tracking``.

    A one-shot NTP query measures a single round trip. A running ``chronyd`` has been
    filtering many of them for as long as it has been up, so its residual error is far
    smaller than anything a single packet can establish -- typically tens of microseconds on
    a machine with a stable network path. When it is present, it is the better source, and
    on the Ratnapura machine it is the one that should be believed.
    """

    def __init__(self, executable: str = "chronyc", *, timeout: float = 5.0) -> None:
        """Configure the reader.

        Args:
            executable: Name or path of the ``chronyc`` binary.
            timeout: Seconds to wait for it to answer.
        """
        self.executable = executable
        self.timeout = timeout

    @property
    def name(self) -> str:
        """Return the source's identifier."""
        return "chronyd"

    def sample(self) -> Sample:
        """Read the daemon's current tracking state.

        Returns:
            The disciplined clock's residual offset with the daemon's own error bound.

        Raises:
            SourceUnavailableError: If ``chronyc`` is absent, fails, or reports no synchronisation.
        """
        binary = shutil.which(self.executable)
        if binary is None:
            raise SourceUnavailableError("chronyc is not installed; no local time daemon to interrogate")
        try:
            completed = subprocess.run(
                [binary, "-c", "tracking"],
                check=False,
                capture_output=True,
                text=True,
                timeout=self.timeout,
            )
        except (OSError, subprocess.SubprocessError) as exc:
            raise SourceUnavailableError(f"chronyc failed: {exc}") from exc
        if completed.returncode != 0:
            raise SourceUnavailableError(f"chronyc exited {completed.returncode}: {completed.stderr.strip()}")
        return parse_chrony_tracking(completed.stdout)


def parse_chrony_tracking(csv_line: str) -> Sample:
    """Parse one line of ``chronyc -c tracking`` output.

    The CSV form is stable across chrony versions, unlike the human-readable form. Fields,
    in order: reference id, reference name, stratum, ref time, system time offset, last
    offset, RMS offset, frequency, residual frequency, skew, root delay, root dispersion,
    update interval, leap status.

    Args:
        csv_line: A single CSV record from ``chronyc -c tracking``.

    Returns:
        The corresponding sample.

    Raises:
        SourceUnavailableError: If the record is malformed or reports no synchronisation.
    """
    fields = csv_line.strip().split(",")
    if len(fields) < 14:
        raise SourceUnavailableError(f"unrecognised chronyc output ({len(fields)} fields)")
    try:
        stratum = int(fields[2])
        system_offset = float(fields[4])
        rms_offset = float(fields[6])
        root_delay = float(fields[10])
        root_dispersion = float(fields[11])
    except ValueError as exc:
        raise SourceUnavailableError(f"unparseable chronyc output: {exc}") from exc
    if fields[13].strip().lower() not in {"normal", "insert second", "delete second"}:
        raise SourceUnavailableError(f"chronyd is not synchronised (leap status {fields[13]!r})")
    if stratum == 0:
        raise SourceUnavailableError("chronyd reports stratum 0; it is not synchronised")
    return Sample(
        source="chronyd",
        offset=-system_offset,
        delay=0.0,
        dispersion=rms_offset,
        stratum=stratum,
        root_delay=root_delay,
        root_dispersion=root_dispersion,
    )


class HardwareSource:
    """Base for the sub-microsecond sources: a GNSS receiver or a PTP-capable NIC.

    These are the only paths to the accuracy a market clock actually wants, and neither can
    be faked in software: GNSS needs a receiver with a pulse-per-second output, PTP needs a
    network interface that timestamps in hardware and a grandmaster on the same segment.

    The interface is defined now so that adding the hardware later is a configuration change
    rather than a redesign. Until then every instance reports itself unavailable, which is a
    truthful answer rather than a silent fallback to something worse.
    """

    kind = "hardware"
    """Short identifier for the flavour of hardware."""

    requirement = "dedicated timing hardware"
    """What an operator must provide to make this source real."""

    def __init__(self, device: str | None = None) -> None:
        """Record the device path an operator has configured, if any."""
        self.device = device

    @property
    def name(self) -> str:
        """Return the source's identifier."""
        return self.kind

    def sample(self) -> Sample:
        """Report that the hardware is not present.

        Raises:
            SourceUnavailableError: Always, until a device is configured and a driver implemented.
        """
        raise SourceUnavailableError(
            f"{self.kind} source is not configured on this machine; it requires {self.requirement}. "
            "Sub-microsecond accuracy is unobtainable without it."
        )


class PpsSource(HardwareSource):
    """A GNSS receiver disciplining the clock through a pulse-per-second line."""

    kind = "gnss-pps"
    requirement = "a GNSS receiver exposing a PPS device (for example /dev/pps0)"


class PtpSource(HardwareSource):
    """An IEEE 1588 grandmaster reached through a hardware-timestamping NIC."""

    kind = "ptp"
    requirement = "a PTP grandmaster on the local segment and a NIC with hardware timestamping"


class LocalClockSource:
    """The machine's own clock, reporting zero offset and an unbounded error.

    This is not a time source and is never allowed to establish consensus. It exists so that
    a run with no reachable source still produces a record -- stamped UNVERIFIED -- rather
    than producing nothing. Its error bound is deliberately enormous, so it can never narrow
    an interval or outvote a real measurement.
    """

    def __init__(self, assumed_error: float = 3600.0) -> None:
        """Record how wrong an undisciplined clock is assumed to be, in seconds."""
        self.assumed_error = assumed_error

    @property
    def name(self) -> str:
        """Return the source's identifier."""
        return "local-clock"

    def sample(self) -> Sample:
        """Return a zero offset with an unbounded error."""
        return Sample(source=self.name, offset=0.0, dispersion=self.assumed_error, stratum=16)
