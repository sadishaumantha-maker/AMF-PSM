---
name: issue-audit
description: Verify that published GitHub issues faithfully reproduce their source document — titles as well as bodies. Use this after any issue creation or update, whenever asked to check issue coverage, fidelity, completeness or "did we miss anything", and before closing out any decomposition work. Also use it to reconcile .claude/memory/issue-index.md against what is actually on GitHub.
---

# Auditing issue fidelity

The comparison is done by a script, not by reading. Model judgement is for classifying what the
script surfaces, never for deciding whether two strings are equal — that is exactly the judgement
that failed and let issue #62 through.

## The procedure

### 1. Fetch the issues

Load the tool, then read every issue named in the index for the source document under audit:

```
ToolSearch: select:mcp__github__issue_read
mcp__github__issue_read(method="get", owner="sadishaumantha-maker", repo="AMF-PSM", issue_number=N)
```

### 2. Write them to JSON

Build a single array. Keep the title and body **exactly as returned** — do not clean them up; the
script handles transport escaping and needs to see the raw form.

```json
[{"number": 62, "title": "…", "body": "…"}, …]
```

### 3. Run the checker

```sh
python3 .claude/skills/issue-audit/scripts/fidelity_check.py \
    --source docs/RESEARCH_DISCUSSIONS.md \
    --issues /path/to/issues.json \
    --index .claude/memory/issue-index.md
```

Exit code 0 = no defects, 1 = defects found, 2 = usage error. Add `--expect-atoms N` to fail loudly
if the parsed atom count drifts from a known-good figure.

### 4. Report

Per unit: PASS/FAIL, issue number, atom count. Then every defect quoting **both** the source text and
the published text. Never summarise a defect — quote it, or the reader cannot tell a typo from a
rewrite.

## What counts as a defect

| Kind | Meaning |
|---|---|
| `title` | The issue title does not match the source heading (ADR-001) |
| `atom` | A Theme, Key Question, Research Area, Deliverable or theme bullet is missing from the body |
| `unmapped` | A source unit has no row in `issue-index.md` — coverage gap |
| `missing` | The index names an issue that was not fetched |

## What is NOT a defect

Do not report these; reporting them trains the reader to ignore audit output.

- **HTML escaping.** The MCP server escapes on read (`&amp;`, `&#34;`, `&#39;`, `&gt;`). The script
  unescapes once before comparing. See ADR-004.
- **Checkbox rendering.** A source bullet `- text` published as `- [ ] text`.
- **Heading renames.** `**Key Questions**:` published as `## Key Questions`.
- **A bracketed track prefix.** `Track 1: Policy & Regulatory Architecture` published as
  `[Track 1] Policy & Regulatory Architecture` is allowed — and *only* that form.
- **Added commentary** under its own heading (Problem Statement, Guardrail, Cross-links). Additions
  are fine; what is never fine is invented text presented as if quoted from the source.

## Classifying additions

The script cannot judge this, so you must. For any content in an issue that is not in the source,
decide which it is:

- **(a) clearly-marked project commentary** — sits under its own heading, makes no claim to be source
  text. Acceptable.
- **(b) presented as source text** — appears inside a quoted block, a Theme line, or a Key Questions
  list without being in the document. **This is a defect**, and a more serious one than a typo,
  because it puts words in the author's mouth.

## After the audit

- Update the `status` column in `.claude/memory/issue-index.md`: `ok`, or `defect` with a one-line
  description.
- If defects were found, do **not** fix them here. The auditor does not write to GitHub. Report them
  and let `issue-publisher` apply the fix against an approved change.

## Extending to a new source document

`fidelity_check.py` parses the structure of `docs/RESEARCH_DISCUSSIONS.md` — `#### Discussion N.M`,
`### Theme X`, `### Track N`, `**Theme**:`, `**Deliverable**:`, `**Key Questions**:`,
`**Research Areas**:`, and numbered items under the two process sections. A document with a different
shape needs its parser extended. Extend deliberately and re-run against the known-good fixture
(`docs/RESEARCH_DISCUSSIONS.md` → 240 discussion atoms + 13 theme bullets + 5 next-step items) to
prove the change did not break existing coverage.
