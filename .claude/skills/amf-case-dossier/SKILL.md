---
name: amf-case-dossier
description: Assemble a dated, sourced structural case file under the AMF case study protocol. Use for every empirical episode the framework examines.
---

# amf-case-dossier

Case files are structural records, not narratives.

## Required sections

1. **Scope** - the episode, its dates, and what question the file answers.
2. **Structural timeline** - which functions stopped working, in what order, through which dependency. Every
   step dated and sourced.
3. **System mapping** - each step mapped to an AMF system and dependency kind, with unmappable steps listed
   explicitly. The unmappable list is the most useful part of the file.
4. **Allegations and dispositions** - every allegation recorded with its regulatory or judicial disposition,
   or marked `undetermined`.
5. **Uncertainty** - what the sources disagree about, and what is unknown.

## Rules

- Source ranking: official filings and regulatory findings, then peer-reviewed analysis, then
  contemporaneous reporting for dating only.
- No prices, spreads, losses, exposures or any market-data quantity.
- Never characterise a named individual's conduct or motive.
- Never imply the framework would have predicted the episode, and never fit parameters until it reproduces
  the sequence.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
