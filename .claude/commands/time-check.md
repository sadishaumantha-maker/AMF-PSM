---
description: Report the attested current time for Ratnapura with its proven uncertainty bound.
---

Run the time attestation and report the verdict plainly:

```sh
python -m tools.chronos attest
```

Report the status, the local Ratnapura time, and the measured bound — to the precision the
bound supports and no further. If the status is UNVERIFIED, say what is unreachable and
what would have to change; do not present the container's own clock as if it were verified.
