"""Repository operations tooling for AMF-PSM.

This package is developer and CI infrastructure, not part of the shipped ``amf``
distribution. ``pyproject.toml`` pins the wheel contents to ``src/amf`` alone, so nothing
here is ever published, and the ``--cov=amf`` gate does not measure it.

Subpackages:
    docsync: Detects drift between ``CLAUDE.md`` and the repository it documents.
    chronos: Produces a time attestation with a proven uncertainty bound.
"""
