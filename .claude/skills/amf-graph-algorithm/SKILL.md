---
name: amf-graph-algorithm
description: Verify a graph query against its source algorithm, state its complexity, and check it on exhaustively enumerated small graphs. Use for any change to graph.py.
---

# amf-graph-algorithm

Every structural query must trace to a published algorithm.

## Procedure

1. **Name the source** - the paper that introduced the algorithm, with its stated complexity.
2. **Verify differentially** against an independent reference implementation on *exhaustively enumerated*
   small digraphs, not only random ones. AMF graphs have seven nodes; exhaustive checking at small order is
   feasible and much stronger than sampling.
3. **State the complexity** in the module docstring so the cost is visible at the call site. Elementary
   circuit enumeration is output-sensitive and can blow up on dense graphs.
4. **Guard** any query whose cost is combinatorial, raising a typed `AMFError` beyond a documented threshold
   rather than hanging.
5. **Respect aggregation** - every structural query aggregates across dependency kinds, capped at 1.0, so
   splitting one coupling across kinds never changes a score. Verify your query preserves that.
6. **Canonicalise ordering** - `dependencies` by `(source, target, kind)` declaration order,
   `dependencies_of` and `dependents_of` by system declaration order.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
