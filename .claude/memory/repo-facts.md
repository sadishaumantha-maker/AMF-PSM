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

## Resolved internal contradictions (2026-08-21 — kept so they are not re-reported)

Five contradictions were previously recorded here. All are closed:

1–3. The PR template defects (an "80%" coverage line vs the 100% gate, issue-template YAML
   frontmatter rendering as literal text, and SQL-injection/XSS items that fit no offline stdlib
   library) were **fixed in the template** under Q-003. It now states the 100% gate and carries
   repo-specific security items (protected artifacts, no new dependencies, no publish surface).
4. The "dead `CODE_OF_CONDUCT.md` link" claim was **stale**: `.github/RULESET-POLICY.md` actually
   links `../CONTRIBUTING.md#code-of-conduct`, and that section exists (CONTRIBUTING.md line 169).
5. The #45–#92 / #77–#138 overlap is reconciled by **ADR-008**: the research set is canonical for
   content and acceptance criteria, the 90-day set for scheduling and ownership; the five collision
   pairs (#58↔#124, #59↔#125, #60↔#126, #64↔#132, #46↔#120–#123) carry cross-link comments.

## Related memory

- `.claude/memory/issue-index.md` — unit ↔ issue registry (read before creating any issue)
- `.claude/memory/source-registry.md` — decomposed docs and their content hashes
- `.claude/memory/decisions.md` — ADR log
- `.claude/memory/open-questions.md` — items needing a human decision
