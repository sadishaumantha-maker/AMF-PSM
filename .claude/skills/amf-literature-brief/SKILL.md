---
name: amf-literature-brief
description: Produce a structured evidence brief from a set of vetted sources, with disagreements and gaps foregrounded. Use when a project needs its evidence base written up before a decision is made.
---

# amf-literature-brief

Turn vetted sources into a brief a decision can be made from.

## Structure

1. **Question** - the exact question the brief answers, in one sentence.
2. **What is established** - claims with strong, converging support. Cite each.
3. **What is contested** - where the literature disagrees, with the positions and who holds them. Do not
   resolve the disagreement; that is the drafter's job with the evidence you supply.
4. **What is unknown** - questions the literature does not answer.
5. **Applicability** - what transfers to a seven-node structural model and what does not. Most financial
   network results are asymptotic; AMF is not.
6. **Implications** - what the evidence would license the project to decide.

## Rules

- Every claim carries a citation vetted by `amf-source-vetting`.
- Foreground the contested and unknown sections. A brief that reads as settled when the field is not is
  worse than no brief.
- State sample sizes, periods and jurisdictions for empirical claims. A result from one market in one decade
  is not a general finding.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
