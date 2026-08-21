# Backlog strategy — sequencing, duplication, and the first slice

**Written**: 2026-08-21 · **Author**: `issue-strategist` · **Scope**: issues #21–#138
**Confidence**: **high** on dependencies and duplication (derived from source content and live issue
titles); **medium** on effort ordering.

> Agent-generated analysis of the backlog as a whole. Complements the per-issue dossiers in this
> directory; supersedes none of them.

## Headline

Three findings, in order of how much time they will save:

1. **Two independent issue sets now overlap substantially** and neither references the other. This is
   the most expensive problem in the backlog and it is growing.
2. **Four issues are gated by one taxonomy decision** (#58). Working them in parallel will produce
   incompatible results that have to be redone.
3. **Theme A (#80) is a gate, not a topic.** Every issue proposing a metric is downstream of it.

---

## 1. Duplication across issue sets — act on this first

Two decompositions were created independently, hours apart, by separate sessions:

| Set | Issues | Organising principle |
|---|---|---|
| Research tracks | #45–#92 (43 issues) | The 8 research tracks of `docs/RESEARCH_DISCUSSIONS.md` |
| 90-day plan | #77, #81, #84, #86, #91, #93–#138 | Phased delivery plan with task breakdown |

Each is internally coherent, which is exactly why the overlap is easy to miss. Concrete collisions:

| Research-track issue | 90-day-plan issue | Shared artifact |
|---|---|---|
| #58 Global Equity Market Classification | #124 `[25a]` equity market taxonomy by country | The equity market taxonomy |
| #59 Liquidity Measurement Across Asset Classes | #125 `[25b]` per-segment liquidity/transparency proxies | The liquidity mapping |
| #60 Regulatory Regime Mapping by Country | #126 `[25c]` regulatory regimes per segment | The jurisdiction taxonomy |
| #64 Hindenburg Report / market structure | #132 `[5.2]` `docs/case_studies/hindenburg.md` | The Hindenburg case study |
| Track 1 (#46, #55–#57) | #120–#123 `[31a–d]` policy tiers | The policy-tier architecture |

Both sets also claim the same pre-existing human issues (#25, #28, #31, #32) as their parents.

**Recommendation.** Do not merge them — they answer different questions. The research set says *what
we need to know*; the 90-day set says *when we will do it*. Make that split explicit: designate the
90-day set canonical for **scheduling and ownership**, the research set canonical for **content and
acceptance criteria**, and cross-link each collision pair above. Roughly a dozen comments, and it
stops the two sets diverging further.

This needs a human decision — recorded as **Q-002** in `.claude/memory/open-questions.md`.

## 2. Dependency order

Derived from content, not issue numbers. Numbering reflects creation order and carries no meaning.

```
#80 Theme A (Measurement & Metrics)
  └── gates EVERY issue that proposes a metric
        #59 liquidity · #60 regime encoding · #63 systemic risk indicators
        #66 capture metrics · #74 CB independence index

#58 Discussion 2.1 (equity market classification)
  └── #59 liquidity per segment      ← nothing to measure until segments exist
  └── #60 regulatory regime per segment
  └── #124–#129 the whole [25x] series

#46/#55–57 Track 1 (policy architecture)
  └── #67 frontier policy volatility  ← reuses the entrenchment model
  └── #74 central bank independence   ← same measurement problem as #66

#54/#80–85 Cross-cutting themes
  └── advisory to all tracks; only Theme A is a hard gate
```

**The load-bearing insight**: #80 (Theme A) reads like a discussion topic but functions as a
constraint. It asks "dimensionless metrics vs. calibrated estimates" — which in this repository is
not abstract. It decides whether a proposed metric can enter the package at all, because every
quantity must be a dimensionless structural measure in `[0, 1]`. Settle it once and five downstream
issues get easier; leave it open and each re-litigates it.

## 3. Not actionable as written

| Issue | Problem | Smallest fix |
|---|---|---|
| #63 Systemic Risk Indicators | Asks to "predict crisis 6–12 months ahead". The package is explicitly not a forecasting tool, so as written this cannot be accepted | Reframe as: which observable structural indicators correlate with historical stress, evaluated retrospectively and labelled illustrative |
| #69 Currency Risk & Capital Flight | Same predictive framing ("predict currency crises 6–12 months ahead") | Same reframing; the cascade model already covers the mechanism |
| #43 (human-authored) | "map out whole global stocks including each and every country" — no acceptance criteria, unbounded scope | Split per #124's country-tiering approach; define "done" as a documented tier-1 set |
| Anything from `QUANTUM_NEURAL_RESEARCH.md` | Source document is forecasting-framed throughout | Blocked on **Q-001**; do not decompose until resolved |

These are not blocked on effort. They are blocked on someone deciding what "done" means, which costs
a conversation, not a sprint.

## 4. The smallest first slice

**Settle Theme A (#80) — specifically, one decision: does a calibrated external estimate ever enter
the package, or only dimensionless structural proxies?**

Why this one:

- It is a single decision, not a research programme. An afternoon, not a sprint.
- It unblocks five issues at once (#59, #60, #63, #66, #74).
- It is already 80% answered by existing practice — `docs/roadmap.md`'s guardrail table has been
  making this call implicitly for every backlog item. Writing it down converts habit into a rule.
- It is cheap to get wrong and cheap to revise, unlike a taxonomy that gets baked into file layouts.

Second slice, once that lands: **#58**, because four issues and the entire `[25x]` series queue
behind it.

Do **not** start with #59 despite its dossier being ready — it is downstream of both.

## 5. What this analysis cannot tell you

- **Effort estimates.** No historical velocity data exists in the repo.
- **Which of the two issue sets the maintainer actually works from.** That determines whether the
  cross-linking in §1 is sufficient or whether one set should be retired.
- **Whether the `[25x]`/`[31x]` task issues have bodies that conflict with the research issues.** Only
  titles were read for this pass; a full body-level overlap audit is a follow-up.
