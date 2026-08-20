---
name: amf-doc-page
description: Write or edit a page under docs/ following AMF documentation conventions, link-check safety and the disclaimer rules. Use for every documentation change.
---

# amf-doc-page

## Conventions

1. **One audience per page**, stated in one sentence before you write anything else.
2. **No duplication.** A fact lives in exactly one place; other pages link to it. `CLAUDE.md` and `README.md`
   already cover a great deal - check before writing.
3. **Relative links only**, and every one must resolve. The CI validate job runs a markdown link check over
   the repository.
4. **Plain-text citations.** Reading lists use `Author (Year). "Title." *Venue* volume(issue), pages.` with
   no hyperlink, so the link check stays green and citations stay stable.
5. **Disclaimers hold.** Nothing may claim predictive power or validated performance. AMF is illustrative;
   its thresholds, weights and scores are not empirically validated; its output is not financial advice and
   not a diagnosis or forecast of any real market.
6. **Mark model-internal statements.** A reader must never mistake a definitional truth for an empirical
   finding.
7. **Choose the medium.** A layering constraint, a comparison or a dependency graph belongs in a table or a
   diagram, not in prose.
8. **Record user-visible changes** under `## [Unreleased]` in `CHANGELOG.md`.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
