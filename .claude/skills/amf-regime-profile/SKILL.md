---
name: amf-regime-profile
description: Produce a dated, multi-dimensional regulatory regime profile for a jurisdiction from primary instruments. Use for any cross-jurisdiction comparison.
---

# amf-regime-profile

Regimes are compared on separate dimensions, never on a composite score.

## Procedure

1. **Use separate dimensions** - disclosure requirements, supervisory powers, investor-protection provisions,
   capital-account openness, enforcement record. Never collapse them; they are incommensurable and a
   composite hides the trade-offs.
2. **Cite the instrument text** for each cell - the official publication, not a commentary, news report or
   vendor summary.
3. **Source enforcement separately.** What the statute says and what is enforced are different facts; use
   published implementation assessments rather than inferring from text.
4. **Record the vintage** of every source. Regimes change and an undated profile misleads.
5. **Link to the tier hierarchy** so the regime map and the policy stack form one model.
6. **Stay neutral.** No jurisdiction is characterised as risky, strict, lax or badly governed. Report
   observable structure only.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
