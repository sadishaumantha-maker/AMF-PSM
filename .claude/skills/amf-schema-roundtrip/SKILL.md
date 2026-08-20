---
name: amf-schema-roundtrip
description: Prove that a new or changed serialised field keeps Market.to_dict / from_dict a lossless fixed point. Use whenever the JSON schema or a result type changes.
---

# amf-schema-roundtrip

`to_dict`/`from_dict` must round-trip losslessly, including each dependency's `kind`.

## Procedure

1. Add the field to `to_dict` and parse it in `from_dict`.
2. Extend `report._to_jsonable` and the text and Markdown renderers if the value is serialised.
3. Prove the fixed point as a hypothesis property, not only an example.
4. Verify ordering: `Market.assemble` stores the seven systems in `SystemKind` declaration order and
   `to_dict` emits them in it.
5. Verify parse failure handling: malformed structure, non-numeric metrics, unknown kinds and out-of-range
   values must all surface as `MarketParseError`. An unrecognised field in a system entry is a
   `MarketParseError`, so a typo such as `integritty` fails loudly. A `components` value that is not a list
   is also an error - a bare string is iterable and would silently split into characters.
6. Verify that a `(source, target)` pair appearing under several kinds keeps each as its own edge and
   survives the round trip.

## Constraint

New result types are frozen, slotted dataclasses with a `to_dict()`.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
