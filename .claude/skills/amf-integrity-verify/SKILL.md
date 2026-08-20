---
name: amf-integrity-verify
description: Verify the checksum-protected artifacts and the private-distribution controls. Use before any commit that could touch the integrity chain or the distribution surface.
---

# amf-integrity-verify

## Protected artifacts

`AMF Framework v1.docx`, `AMF Framework v1.docx.ots`, `anatomical-market-framework`, `LICENSE.txt`. They are
listed in `SHA256SUMS`. **Never modify them. Never add source files to `SHA256SUMS`.**

## Procedure

1. Run `sha256sum --check --strict SHA256SUMS`. It must pass.
2. Confirm the `protect-ip-artifacts` pre-commit hook is intact and still covers `SHA256SUMS` itself.
3. Confirm the whitespace-fixing hooks still exclude the protected paths, and that `.gitattributes` still
   marks the document and its proof `binary` and the plain-text overview `-text`. EOL normalisation would
   alter their bytes.
4. Confirm `.github/workflows/integrity.yml` still runs on the same triggers.
5. **Never read a protected artifact to generate output.** The CLI's `describe` text comes from paraphrased
   constants in `cli.py` precisely so the software never touches them.
6. **Distribution** - confirm the `Private :: Do Not Upload` classifier is present in `pyproject.toml` *and*
   in the built wheel, that `tests/unit/test_packaging.py` passes, and that no workflow uploads to an index,
   attaches a release asset or produces an Actions artifact of the package. The repository is public, so a
   release asset is not a private channel.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
