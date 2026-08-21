---
name: issue-authoring
description: GitHub issue mechanics for AMF-PSM — the body contract, provenance blocks, label taxonomy, sub-issue linking, and the MCP call recipes that actually work. Use before creating, updating, or linking any GitHub issue in this repository, and whenever executing an approved decomposition manifest. Contains the tooling gotchas (id vs number, HTML escaping, sub-issue race conditions) that cost real debugging time to find.
---

# Authoring issues

## The body contract

Every generated issue body has three zones, in this order, and they never interleave:

```markdown
<!-- amf-provenance
source: docs/RESEARCH_DISCUSSIONS.md
unit: discussion-3.2
title_sha256: 4c1f…
body_sha256: 8f2a…
generated: 2026-08-20
-->

**Parent**: #48 — Track 3: Shock Propagation & Contagion
**Source**: `docs/RESEARCH_DISCUSSIONS.md` → Track 3 → Discussion 3.2

## <verbatim section from source>
…atoms, byte-for-byte…

## Problem Statement          ← your prose, clearly its own heading
## Guardrail                  ← your prose
## Cross-links                ← your prose
```

1. **Provenance** — an HTML comment. Renders invisibly; parsed by the auditor and the publisher.
2. **Verbatim zone** — the author's words, unedited. Typos included.
3. **Commentary zone** — your words, under their own headings.

The rule that matters: **never put your words inside the verbatim zone, and never put quotation
marks around a summary.** Additions are welcome; fabricated quotations are the one unforgivable
defect, because they put words in the author's mouth.

## Titles

Copy the source heading byte-for-byte (ADR-001). The only permitted restyling is a bracketed prefix
on container issues:

| Unit kind | Title form |
|---|---|
| discussion | `Discussion 3.2: Feedback Loops: Markets ↔ Policy` — exact |
| theme | `Theme A: Measurement & Metrics` — exact |
| track | `[Track 1] Policy & Regulatory Architecture` — prefix allowed |
| container / process | synthesised; no source heading to preserve |

Do not "fix" a heading that reads awkwardly. Issue #62 became a defect precisely because a colon
inside a colon-prefixed title looked wrong to someone and quietly became an em dash.

## Labels

| Label | Applied when |
|---|---|
| `research` | every issue from a research-discussion source |
| `documentation`, `enhancement` | issue type |
| `track-N-<slug>` | membership in a track |
| `discussion` | a leaf discussion unit |
| `cross-cutting` | a theme unit |
| `process` | a process/next-step unit |
| `guardrail-review` | **any unit the extractor flagged** — never omit this |

Labels that do not exist are created automatically on first use. Keep the taxonomy small; a label
per issue is not a taxonomy.

## MCP recipes

Load tools first: `ToolSearch` → `select:mcp__github__issue_write,mcp__github__sub_issue_write,mcp__github__issue_read,mcp__github__list_issues`

### Create

```
mcp__github__issue_write(method="create", owner="sadishaumantha-maker", repo="AMF-PSM",
                         title=…, body=…, labels=[…])
```
Returns `{"id": 5200379123, "url": ".../issues/62"}`. **Record both.** The `id` is not the number and
you cannot derive one from the other.

### Update

```
mcp__github__issue_write(method="update", owner=…, repo=…, issue_number=62, title=…)
```
Pass only the fields you are changing.

### Link a sub-issue

```
mcp__github__sub_issue_write(method="add", owner=…, repo=…,
                             issue_number=<PARENT number>, sub_issue_id=<CHILD id>)
```

Two traps, both of which will bite:

- **`sub_issue_id` is the numeric `id`, not the issue number.** Passing the number silently targets
  the wrong object or errors.
- **Add sub-issues sequentially within a single parent.** Parallel adds to the same parent race and
  drop links. Different parents in parallel is fine — that is the useful concurrency.

### Reading back

`issue_read` and `list_issues` **HTML-escape on read**: `&`→`&amp;`, `"`→`&#34;`, `'`→`&#39;`,
`>`→`&gt;`. Unescape once before comparing anything. A title that reads back as `&amp;` was almost
certainly stored correctly as `&` — verify before "fixing" it, or you will double-escape it for real.

## Idempotency

Before writing anything, read `.claude/memory/issue-index.md`:

- unit present, hash unchanged → **skip**, no API call
- unit present, hash changed → **update** that issue
- unit absent → **create**, then append the row

Write the index row *before* the create call where possible, so a crash mid-run leaves a claim rather
than an orphan. A duplicate issue is much more expensive to clean up than a stale index row.

## After publishing

1. Update `.claude/memory/issue-index.md` — number, id, parent, hash, status.
2. Update `.claude/memory/source-registry.md` — document hash, atom count, issue count, date.
3. Run the `issue-audit` skill. Publishing is not finished until the audit is clean.
