---
name: amf-changelog-entry
description: Write a Keep-a-Changelog entry under Unreleased and keep the two version strings in sync. Use for every user-visible change.
---

# amf-changelog-entry

## Procedure

1. Categorise: **Added**, **Changed**, **Fixed** or **Security**.
2. Write from the reader's point of view: what changed for someone using the package.
3. **When a published number moves**, say which number and what evidence moved it. "Corrected the
   concentration default" is not enough; name the measurement.
4. Keep `pyproject.toml` `version` and `amf/__init__.py` `__version__` in sync. `CITATION.cff` `version`
   tracks the *framework* release (1.0), not the package - do not change it to match.
5. `cffconvert --validate -i CITATION.cff` must still pass.
6. Never add a publish workflow and never produce a downloadable artifact from CI. See `RELEASING.md`.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
