"""Drift detection between ``CLAUDE.md`` and the repository it claims to describe.

``CLAUDE.md`` is prose that asserts mechanical facts: which modules exist, what the CLI
accepts, which constants hold, how many tests run. Prose rots. This package extracts the
real facts from the tree (``facts``), extracts the asserted claims from the document
(``claims``), and reports every disagreement (``checks``, ``drift``).

Two properties are deliberate:

* **Offline.** No check performs network I/O, so a scan is reproducible anywhere.
* **Deterministic.** Findings are emitted in a canonical order with canonical JSON, so the
  same commit always produces byte-identical output. That is what lets a checked-in
  baseline serve as a regression gate.
"""

from tools.docsync.model import Finding, Severity

__all__ = ["Finding", "Severity"]
