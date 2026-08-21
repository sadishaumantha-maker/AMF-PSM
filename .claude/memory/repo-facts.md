# Repo facts — ground truth for agents

Always-on memory. Keep under ~100 lines. Facts only; rules live in the `amf-guardrails` skill.

## What this repository is

Two things side by side:

1. **The Anatomical Market Framework (AMF) v1.0** — a proprietary analytical framework captured in
   `AMF Framework v1.docx`, summarised in `anatomical-market-framework`. Protected by an
   OpenTimestamps proof and SHA-256 checksums.
2. **The `amf` Python package** (`src/amf/`) — a software implementation of the framework's
   *analytical method*. Zero runtime dependencies, standard library only.

The package models market **structure and resilience**. It is not a trading system and never becomes one.

## The seven systems

`skeleton`, `circulatory`, `nervous`, `musculature`, `organs`, `immune`, `metabolism`.
Per-system structural metrics — `integrity`, `redundancy`, `criticality`, `load` — all in `[0, 1]`.
Derived: `health = integrity·(1 − load)`; `absorptive_capacity = 0.5·redundancy + 0.3·integrity + 0.2·(1 − load)`.

## Module dependency order (one-way, keep acyclic)

`errors`/`models` ← `systems`/`graph` ← `market` ← `diagnostics`/`simulation` ← `sensitivity` ← `report`/`viz`/`cli`

## Protected artifacts — never modify

Listed in `SHA256SUMS`: `AMF Framework v1.docx`, `AMF Framework v1.docx.ots`,
`anatomical-market-framework`, `LICENSE.txt`. Enforced by the `protect-ip-artifacts` pre-commit hook
and the `integrity.yml` workflow. Do not add source files to `SHA256SUMS`.

## Quality gates

- **100%** statement *and* branch coverage of `src/amf` (`--cov-fail-under=100`). Scope is the `amf`
  package only — files under `.claude/` do not affect it.
- `ruff check` + `ruff format --check` (line length 120); `mypy` strict over `files = ["src"]`.
- Python 3.11+; CI matrix 3.11/3.12/3.13.

## Source documents and their decomposition status

| Document | Lines | Status |
|---|---|---|
| `docs/RESEARCH_DISCUSSIONS.md` | 561 | Decomposed → issues #45–#92 (253 atoms → 43 issues) |
| `docs/QUANTUM_NEURAL_RESEARCH.md` | 799 | **Not decomposed.** Forecasting-framed — needs structural reframing first |
| `docs/ANALYSIS_AND_ROADMAP.md` | 397 | Reference only |
| `docs/roadmap.md` | 144 | Source of the guardrail translation table |

## Tooling facts (hard-won; do not rediscover)

- **The GitHub MCP server HTML-escapes text on read**: `&`→`&amp;`, `"`→`&#34;`, `'`→`&#39;`,
  `>`→`&gt;`. Always unescape before comparing, or every comparison produces false failures.
- **`sub_issue_write` takes the numeric issue `id`, not the issue number.** The id comes back from
  `issue_write` on creation, or from `issue_read`.
- **Add sub-issues sequentially per parent.** Parallel adds to the same parent race.
- **There is no `gh` CLI in this environment.** All GitHub access is via `mcp__github__*` tools,
  loaded through ToolSearch.
- Issue-body HTML comments (`<!-- ... -->`) render invisibly — safe for provenance blocks.

## Known internal contradictions (verified — do not propagate)

These are real defects in the repo. Cite them; do not repeat them.

1. `.github/pull_request_template.md` states "**minimum 80%**" coverage. `CLAUDE.md` mandates **100%**.
   The 100% figure is authoritative.
2. That same PR template opens with GitHub *issue-template* YAML frontmatter
   (`name:`/`description:`/`title:`/`labels:`/`assignees:`), which renders as literal text at the top
   of every PR body. PR templates take no frontmatter.
3. The PR template asks about SQL injection and XSS — meaningless for a stdlib-only offline library.
4. `.github/RULESET-POLICY.md` links `CODE_OF_CONDUCT.md`, which does not exist in the repo.
5. Issues #45–#92 and #77–#98 are two independently-created decompositions covering overlapping
   ground (#25, #28, #31, #32) with no cross-links between them.

## Related memory

- `.claude/memory/issue-index.md` — unit ↔ issue registry (read before creating any issue)
- `.claude/memory/source-registry.md` — decomposed docs and their content hashes
- `.claude/memory/decisions.md` — ADR log
- `.claude/memory/open-questions.md` — items needing a human decision
