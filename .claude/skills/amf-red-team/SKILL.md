---
name: amf-red-team
description: Adversarially attack a finding, rule or rendered output before it is merged. Use as the final gate on every AMF-PSM project.
---

# amf-red-team

Your job is to break it. Report what survives.

## Attack directions

1. **Falsification** - construct the input where the conclusion gives an absurd answer. Sweep boundaries,
   ties, degenerate structures and empty cases.
2. **Misreading** - take the real rendered output and write the most defensible-looking unsupported claim you
   can from it. If you succeed, **the output must change** - a disclaimer does not undo a misleading number.
3. **Rule evasion** - find the path that satisfies the letter of a rule while defeating its purpose.
4. **Gaming** - satisfy a metric without improving the property it stands for. Every metric needs a stated
   gaming mode and a counter-measure, or it ships as advisory only.
5. **Steel-man the rejected option** - argue it in its strongest form. If the evidence cannot answer, the
   decision is not ready.

## Repository hard rules to check against

No trading vocabulary in any public name or document. No claim of predictive power or validated performance.
No characterisation of a named person or organisation. Nothing that reads as financial advice, a diagnosis,
or a forecast of a real market. Nothing that reads a checksum-protected artifact to produce output.

## Reporting

Each finding needs the exact input, quotation or path that produced it. "This feels weak" is not a finding.
You do not fix what you find - hand it back.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
