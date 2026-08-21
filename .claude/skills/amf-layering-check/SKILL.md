---
name: amf-layering-check
description: Verify the one-way module dependency order in src/amf holds in the actual imports. Use before any change that adds an import or moves code between modules.
---

# amf-layering-check

The dependency order is:

`errors` / `models` -> `systems` / `graph` -> `market` -> `diagnostics` / `simulation` -> `sensitivity` ->
`report` / `viz` / `cli`

## Procedure

1. Extract the actual import graph from `src/amf/` - read the imports, do not trust the documentation.
2. Verify it is acyclic and that no module imports a higher layer.
3. Confirm `errors` and `graph` have no internal dependencies.
4. Confirm nothing below the renderer layer imports `report`, `viz` or `cli`.
5. New behaviour belongs in the module that owns it. If a change needs an upward import, the behaviour is in
   the wrong module.
6. Public API is re-exported from `amf/__init__.py`; the renderers are the documented exception and are
   imported from `amf.report` and `amf.viz` directly.

## Output

The import graph and a pass, or the exact offending import.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
