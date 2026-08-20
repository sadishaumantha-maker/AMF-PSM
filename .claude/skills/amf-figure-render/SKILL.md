---
name: amf-figure-render
description: Render a deterministic figure under the AMF visual grammar with the mandatory footnote intact. Use for every figure the project publishes.
---

# amf-figure-render

Figures carry the same honesty and determinism obligations as numbers.

## Rules

1. **Standard library only.** SVG is drawn without matplotlib and without Graphviz.
2. **The footnote is mandatory.** `viz._FOOTNOTE` is baked into every rendered image and must survive every
   change.
3. **Purity** - no I/O, no clock, no randomness inside a renderer. Verify two renders of the same input are
   byte-identical.
4. **Encoding** - position is the most accurate channel for magnitude, colour hue among the least. Severity
   must never be carried by hue alone; pair it with a redundant channel.
5. **Colour-vision safety and greyscale legibility** - check both; these figures will be printed.
6. **Formats** - `render_dot`, `render_mermaid`, `render_graph_svg` and `render_timeline_svg` each need the
   check; `viz` has its own `--format` values (`svg|dot|mermaid`), distinct from the report formats.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
