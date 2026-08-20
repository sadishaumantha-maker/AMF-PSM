---
name: amf-taxonomy-builder
description: Build a citable classification register from official standards, with an inclusion rule and a maintained exclusion list. Use for any taxonomy, register or standards mapping.
---

# amf-taxonomy-builder

A register without a stated inclusion rule cannot be completed or audited.

## Procedure

1. **Write the inclusion rule first** - the unit, the threshold and the source of the threshold. Do not
   collect anything until the rule decides every borderline case without further judgement.
2. **Choose structural fields only.** No volumes, capitalisations, prices, spreads or any market-data
   quantity. Run `amf-boundary-check` over the schema field names.
3. **Cite every row** to an official source: a regulator register, an operator disclosure, or a standards
   body specification. Record the vintage.
4. **Maintain the exclusion list** - every candidate considered and rejected, with the rule clause that
   rejected it. The exclusion list is as important as the register.
5. **Check licensing** before adopting a published classification. Some are commercially licensed and
   adopting one without checking is a licence violation, not a design mistake.
6. **Publish as data plus narrative** - a form that can be regenerated and diffed, with a page explaining it.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
