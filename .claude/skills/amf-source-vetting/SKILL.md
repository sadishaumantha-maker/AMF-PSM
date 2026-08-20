---
name: amf-source-vetting
description: Vet a proposed source for primary status and scholarly or official standing before it is cited in AMF-PSM. Use whenever a citation is proposed for any document under docs/ or projects/.
---

# amf-source-vetting

Run this before any source enters a document.

## Procedure

1. **Identify the type.** Peer-reviewed article, university-press or equivalent scholarly book, official
   instrument text, standards body specification, official-sector report, or none of these.
2. **Reject outright**: vendor white papers, consultancy reports, press releases, blog posts, and
   encyclopaedia entries. News reporting is admissible only to establish the date of an event.
3. **Prefer the primary.** If the candidate is a textbook restating an earlier result, find and cite the
   original. Keep the textbook only as a reading pointer.
4. **Read the caveats.** Record the limitations the authors state themselves. A source cited without its own
   caveats is misrepresented.
5. **Check the claim.** Confirm the source says what the citing sentence needs it to say. A correct citation
   attached to an unsupported claim is the more dangerous error.
6. **Record standing**: venue, publisher and why it qualifies.

## Output format

`Author (Year). "Title." *Venue* volume(issue), pages.` - plain text, no hyperlink. External URLs in reading
lists are avoided because the CI markdown link check runs over every file.

## Failure

If no adequate source exists, mark the claim `unevidenced` and say so. That is a valid, useful outcome.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
