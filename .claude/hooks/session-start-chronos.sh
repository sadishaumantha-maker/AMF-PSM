#!/bin/sh
# SessionStart hook: stamp every session with a time attestation.
#
# Written in POSIX sh rather than Python on purpose. `ruff check .` covers `.claude/**/*.py`
# with the repository's full ANN + D rule set, and CodeQL scans it too; shell keeps that
# surface at zero.
#
# This never fails the session. Its job is to put the verdict where a reader can see it, so
# that a session which cannot establish the time knows that about itself from the first
# turn. The hard gate belongs to the automation, not to interactive work.
set -u

repo_root=$(cd "$(dirname "$0")/../.." 2>/dev/null && pwd) || exit 0
cd "$repo_root" || exit 0

if ! command -v python3 >/dev/null 2>&1; then
    exit 0
fi

verdict=$(python3 -m tools.chronos now --timeout 2 --no-hardware 2>/dev/null)
status=$?

case "$status" in
    0) printf 'chronos: %s\n' "$verdict" ;;
    3) printf 'chronos: time is UNVERIFIED in this environment. %s\n' "$verdict"
       printf 'chronos: scheduled runs hard-fail on this; interactive work continues.\n' ;;
    4) printf 'chronos: locale gate FAILED. The machine disagrees with Asia/Colombo +05:30.\n' ;;
    *) printf 'chronos: attestation could not be run.\n' ;;
esac

exit 0
