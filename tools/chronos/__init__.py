"""Verified time with a proven uncertainty bound, hard-gated to Ratnapura, Sri Lanka.

This package exists because a timestamp whose error you have not measured is not evidence.
It does not try to be accurate; it tries to be *honest about how accurate it is*, and to
refuse to certify a run whose uncertainty exceeds the budget it was given.

What is and is not achievable is worth stating plainly, because the difference is physics
rather than engineering effort:

============================  ===========================================================
Source                        Realistic uncertainty
============================  ===========================================================
NTP over the public internet  ~1-10 ms, bounded by path asymmetry
NTP on a quiet LAN            ~0.1-1 ms
A disciplined local clock     tens of microseconds, as reported by ``chronyc tracking``
PTP with hardware timestamps  sub-microsecond
GNSS with a PPS signal        tens of nanoseconds
============================  ===========================================================

Microsecond accuracy from an internet round trip is not attainable at any sampling rate:
the one-way delays are unmeasurable and unequal, and that asymmetry lands directly in the
offset. Anything printing microseconds from an HTTP fetch is printing noise. Accordingly
this package never formats more digits than its measured bound supports.

Modules:
    locale_gate: The frozen Asia/Colombo locale and its validation.
    sources: Pluggable time sources, from NTP to a GNSS receiver.
    consensus: Marzullo interval intersection over independent sources.
    attest: The signed-off attestation record and its status.
"""

from tools.chronos.locale_gate import LOCATION, TZ_NAME, UTC_OFFSET_MINUTES

__all__ = ["LOCATION", "TZ_NAME", "UTC_OFFSET_MINUTES"]
