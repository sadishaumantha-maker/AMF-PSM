"""Time sources, exercised offline.

The NTP client is tested against a real UDP socket on loopback rather than a mock, so the
packet encoding, the four-timestamp arithmetic and the field offsets are all genuinely
exercised. Nothing here touches the network.
"""

from __future__ import annotations

import socket
import struct
import threading
import time

import pytest
from tools.chronos.errors import SourceUnavailableError
from tools.chronos.sources import (
    ChronySource,
    LocalClockSource,
    NtpSource,
    PpsSource,
    PtpSource,
    Sample,
    parse_chrony_tracking,
)

NTP_DELTA = 2_208_988_800


def encode(seconds):
    """Encode a Unix timestamp as an NTP integer/fraction word pair."""
    ntp = seconds + NTP_DELTA
    whole = int(ntp)
    return whole, int((ntp - whole) * 2**32)


def build_reply(*, server_time=None, stratum=2, leap=0, root_delay=0.0, root_dispersion=0.0):
    """Build a well-formed 48-byte NTP server reply."""
    now = time.time() if server_time is None else server_time
    recv_i, recv_f = encode(now)
    tx_i, tx_f = encode(now)
    return struct.pack(
        "!B B B b 11I",
        (leap << 6) | (4 << 3) | 4,
        stratum,
        4,
        -20,
        int(root_delay * 65536),
        int(root_dispersion * 65536),
        0,
        0,
        0,  # reference timestamp
        0,
        0,  # originate timestamp
        recv_i,
        recv_f,
        tx_i,
        tx_f,
    )


class FakeNtpServer:
    """A one-shot UDP responder on loopback."""

    def __init__(self, reply):
        self.reply = reply
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("127.0.0.1", 0))
        self.port = self.socket.getsockname()[1]
        self.thread = threading.Thread(target=self._serve, daemon=True)

    def _serve(self):
        try:
            _, address = self.socket.recvfrom(1024)
            if self.reply is not None:
                self.socket.sendto(self.reply, address)
        except OSError:  # pragma: no cover - only on teardown races
            pass

    def __enter__(self):
        self.thread.start()
        return self

    def __exit__(self, *_exc):
        self.socket.close()


def query(reply, **kwargs):
    with FakeNtpServer(reply) as server:
        return NtpSource("127.0.0.1", port=server.port, timeout=3.0, **kwargs).sample()


# --- NtpSource ----------------------------------------------------------------------


def test_a_well_formed_reply_yields_a_small_offset():
    """Regression: the receive/transmit words sit at rest[5:7] and rest[7:9], not rest[6:10]."""
    result = query(build_reply())
    assert isinstance(result, Sample)
    assert abs(result.offset) < 1.0


def test_a_server_ahead_of_us_produces_a_positive_offset():
    result = query(build_reply(server_time=time.time() + 5.0))
    assert 4.0 < result.offset < 6.0


def test_a_server_behind_us_produces_a_negative_offset():
    result = query(build_reply(server_time=time.time() - 5.0))
    assert -6.0 < result.offset < -4.0


def test_root_delay_and_dispersion_are_decoded_from_fixed_point():
    result = query(build_reply(root_delay=0.5, root_dispersion=0.25))
    assert result.root_delay == pytest.approx(0.5, abs=1e-4)
    assert result.root_dispersion == pytest.approx(0.25, abs=1e-4)


def test_stratum_is_reported():
    assert query(build_reply(stratum=3)).stratum == 3


def test_the_error_bound_includes_the_upstream_chains_own_error():
    plain = query(build_reply())
    burdened = query(build_reply(root_dispersion=0.1))
    assert burdened.error > plain.error + 0.09


def test_a_server_declaring_itself_unsynchronised_is_refused():
    with pytest.raises(SourceUnavailableError, match="unsynchronised"):
        query(build_reply(leap=3))


@pytest.mark.parametrize("stratum", [0, 16, 200])
def test_an_unusable_stratum_is_refused(stratum):
    with pytest.raises(SourceUnavailableError, match="stratum"):
        query(build_reply(stratum=stratum))


def test_a_short_reply_is_refused():
    with pytest.raises(SourceUnavailableError, match="short reply"):
        query(b"too short")


def test_a_timeout_is_reported_as_unavailable():
    with pytest.raises(SourceUnavailableError):
        query(None)


def test_an_unroutable_host_is_reported_as_unavailable():
    with pytest.raises(SourceUnavailableError):
        NtpSource("127.0.0.1", port=1, timeout=0.5).sample()


def test_the_source_name_is_the_server():
    assert NtpSource("time.example.net").name == "time.example.net"


# --- chrony -------------------------------------------------------------------------

TRACKING = (
    "C0248F97,time.example.net,3,1740000000.0,0.000000123,-0.000000123,"
    "0.000000456,1.0,0.0,0.1,0.000500,0.000100,64.0,Normal"
)


def test_chrony_tracking_is_parsed():
    result = parse_chrony_tracking(TRACKING)
    assert result.source == "chronyd"
    assert result.stratum == 3
    assert result.root_delay == pytest.approx(0.0005)
    assert result.root_dispersion == pytest.approx(0.0001)


def test_chrony_offset_sign_is_inverted_to_a_correction():
    """chronyd reports how far the system clock is from true time; we report the correction."""
    assert parse_chrony_tracking(TRACKING).offset == pytest.approx(-0.000000123)


def test_a_disciplined_clock_beats_a_single_round_trip():
    chrony = parse_chrony_tracking(TRACKING)
    single_packet = Sample("ntp", 0.0, delay=0.020)
    assert chrony.error < single_packet.error


def test_an_unsynchronised_daemon_is_refused():
    with pytest.raises(SourceUnavailableError, match="not synchronised"):
        parse_chrony_tracking(TRACKING.replace(",Normal", ",Not synchronised"))


def test_stratum_zero_is_refused():
    with pytest.raises(SourceUnavailableError, match="stratum 0"):
        parse_chrony_tracking(TRACKING.replace(",3,", ",0,"))


def test_a_truncated_record_is_refused():
    with pytest.raises(SourceUnavailableError, match="unrecognised"):
        parse_chrony_tracking("a,b,c")


def test_a_non_numeric_record_is_refused():
    with pytest.raises(SourceUnavailableError, match="unparseable"):
        parse_chrony_tracking(TRACKING.replace(",3,", ",three,"))


def test_a_leap_second_announcement_is_still_synchronised():
    assert parse_chrony_tracking(TRACKING.replace(",Normal", ",Insert second")).stratum == 3


def test_missing_chronyc_is_reported_clearly(monkeypatch):
    monkeypatch.setattr("tools.chronos.sources.shutil.which", lambda _name: None)
    with pytest.raises(SourceUnavailableError, match="not installed"):
        ChronySource().sample()


# --- hardware plug-ins and the local fallback ----------------------------------------


@pytest.mark.parametrize(("source", "needle"), [(PpsSource(), "PPS"), (PtpSource(), "grandmaster")])
def test_hardware_sources_say_exactly_what_they_need(source, needle):
    with pytest.raises(SourceUnavailableError, match=needle):
        source.sample()


def test_hardware_sources_are_honest_about_sub_microsecond_accuracy():
    with pytest.raises(SourceUnavailableError, match="Sub-microsecond accuracy is unobtainable"):
        PpsSource().sample()


def test_the_local_clock_never_narrows_an_interval():
    """It must be incapable of outvoting or tightening a real measurement."""
    local = LocalClockSource().sample()
    real = Sample("ntp", 0.0, delay=0.020)
    assert local.error > real.error * 100
    assert local.offset == 0.0


def fake_chronyc(tmp_path, *, stdout="", stderr="", code=0):
    """Write a stand-in `chronyc` executable and return its path."""
    script = tmp_path / "chronyc"
    script.write_text(
        f"#!/bin/sh\nprintf '%s' '{stdout}'\nprintf '%s' '{stderr}' >&2\nexit {code}\n",
        encoding="utf-8",
    )
    script.chmod(0o755)
    return script


def test_chrony_source_reads_a_real_subprocess(tmp_path):
    result = ChronySource(str(fake_chronyc(tmp_path, stdout=TRACKING))).sample()
    assert result.source == "chronyd"
    assert result.stratum == 3


def test_a_failing_chronyc_is_reported_with_its_exit_code(tmp_path):
    binary = fake_chronyc(tmp_path, stderr="506 Cannot talk to daemon", code=1)
    with pytest.raises(SourceUnavailableError, match="exited 1"):
        ChronySource(str(binary)).sample()


def test_a_chronyc_that_cannot_be_executed_is_reported(tmp_path, monkeypatch):
    monkeypatch.setattr("tools.chronos.sources.shutil.which", lambda _n: str(tmp_path / "absent"))
    with pytest.raises(SourceUnavailableError, match="chronyc failed"):
        ChronySource().sample()


def test_the_chrony_source_is_named_for_the_daemon_not_the_binary(tmp_path):
    assert ChronySource(str(fake_chronyc(tmp_path))).name == "chronyd"
