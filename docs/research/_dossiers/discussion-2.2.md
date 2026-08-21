# Dossier: discussion-2.2 — Liquidity Measurement Across Asset Classes

**Issue**: #59 · **Source**: `docs/RESEARCH_DISCUSSIONS.md` → Track 2 → Discussion 2.2
**Written**: 2026-08-21 · **Author**: `issue-researcher`
**Confidence**: **medium** — the structural mapping rests on T1 code evidence and is solid; the
asset-class specifics rest on T4/UNVERIFIED market knowledge that a domain expert should check.

> Agent-generated guidance on how to approach this issue. It is **not** the deliverable the source
> note asks for — that is `docs/research/liquidity_unified_framework.md`, still to be written.

## What is actually being asked

On the surface: "can one liquidity metric work across equities, bonds, forex and commodities?"

Underneath, two different questions are tangled together, and separating them dissolves most of the
difficulty:

1. **A measurement question** — which observable proxies indicate liquidity in each asset class?
   Genuinely asset-class-specific, and genuinely outside this repository's scope.
2. **A modelling question** — what does the framework need liquidity *for*? That has a narrow answer:
   it feeds the circulatory system's structural metrics and, through them, absorption and propagation.

The framework does not need to measure liquidity. It needs a dimensionless statement of how well
capital movement holds up under stress. Those are different asks, and conflating them is what makes
the unification look impossible.

## What already exists

Read the code before proposing anything here — a surprising amount of this is built.

- **T1** `src/amf/systems.py` — `circulatory()` builds the "capital flow" system. It already carries
  the four structural metrics, all constrained to `[0, 1]`: `integrity`, `redundancy`, `criticality`,
  `load`.
- **T1** `src/amf/systems.py` — two derived quantities exist and are distinct:
  `health = integrity·(1 − load)` and
  `absorptive_capacity = 0.5·redundancy + 0.3·integrity + 0.2·(1 − load)`.
- **T1** `src/amf/diagnostics.py` — `DiagnosticEngine.concentration()` is an **HHI over a system's
  outgoing dependency weights**. It is *share-based*: it measures how unevenly reliance is spread,
  **not how much reliance there is**. A system with a single coupling scores 1.0 at any weight; one
  with none scores 0. The opt-in `scale_concentration_by_reliance` flag multiplies by
  `min(1, total outgoing weight)` and is **off by default because turning it on moves every published
  concentration score**.
- **T2** `docs/roadmap.md`, "Guardrail translation rules" — already maps
  *"liquidity / capital depth"* → circulatory `integrity` / `redundancy`. This discussion is
  re-opening a question the repo has already answered once; the dossier's job is to say whether that
  answer holds.

**Nothing needs building to represent liquidity.** The representation exists. What is missing is the
documented mapping from each asset class onto it, and example markets that exercise it.

## Findings

1. **The note contains its own answer.** Its fourth research area — *"Stress liquidity vs.
   normal-times liquidity (two different beasts)"* — is the key. The framework already keeps these
   apart: **T1** `redundancy` is how many independent capital paths exist (normal times);
   **T1** `absorptive_capacity` is what survives when load rises (stress). Forcing them into one
   "unified liquidity number" would destroy the distinction the note itself identifies as essential.
   *The unification the title asks for is the wrong goal.*

2. **The share-vs-amount subtlety is a real trap.** **T1** Because `concentration` is share-based, a
   market with one enormous capital channel and a market with one tiny one score identically (1.0).
   For liquidity work this is exactly backwards from intuition. Any liquidity mapping must decide
   deliberately whether depth belongs in `redundancy` (path count) or in the reliance scaling, and
   must record why. This is the single most likely place for a subtle modelling error.

3. **Question 2 is a boundary question, not a metric question.** "Forex trades $6T/day but mostly
   between banks — is retail liquidity separate?" **T2** `docs/roadmap.md` already answers the shape:
   distinct participant populations with distinct access are **distinct `MarketBoundary` segments**,
   each with its own anatomy. Retail and interbank forex are two markets that share an asset, not one
   market with two liquidity numbers. The `$6T/day` figure is the note's claim, unverified here.

4. **Question 4 is already modelled, under a different name.** "Flash crash risk as an illiquidity
   metric" is **T1** the cascade machinery in `simulation.py`: `cascade_threshold` marks where a
   system's stress makes it amplify rather than absorb, with `cascade_gain` and
   `cascade_absorption_drop` governing the non-linearity. Illiquidity-under-stress *is* low
   `absorptive_capacity` near a threshold. No new metric is required.

5. **Goodhart's Law is a live constraint here, not a footnote.** The note lists it as a research
   area. **T4** Where a liquidity measure gates capital access, participants optimise the measure.
   Because AMF metrics are structural and dimensionless rather than reported figures, the framework
   is somewhat insulated — but any mapping that pins a metric to a *published* market statistic
   reintroduces the problem. Prefer proxies that are structural (how many venues, how many
   independent providers) over reported ones (volumes, spreads).

6. **Kyle's lambda, effective spread, realized spread.** **[UNVERIFIED]** These are standard market
   microstructure measures and the note asks which best predicts crisis. I did not consult primary
   sources this session and will not characterise their relative predictive performance. Whoever
   writes the deliverable must cite primary literature; do not carry this bullet forward as if it
   were settled.

7. **This issue is blocked by #58.** Liquidity is measured *per segment*. Until Discussion 2.1
   settles what a segment is (one national exchange? a venue family? retail vs institutional?), there
   is nothing to attach a liquidity reading to. Sequencing matters more than effort here.

## Options

**A — Build a unified liquidity metric.** What the title literally asks. Costs the most, and finding
1 says it destroys the stress/normal distinction. **Not recommended.**

**B — Write the per-asset-class mapping onto existing metrics.** For each asset class, document which
observable notion of liquidity maps onto `integrity`, `redundancy` and `load`, and why. No code
change. Produces the deliverable the note asks for. Cheap, reversible, and it forces the modelling
decisions in finding 2 into the open.

**C — Add example markets per asset class.** Extend `examples/` with a bond, forex and commodity
market so the mapping is exercised rather than asserted. Small code, high value — an example that
diagnoses sensibly is stronger evidence than a paragraph claiming it would.

**D — Do nothing until #58 lands.** Defensible given finding 7. But B costs little and sharpens #58.

## Recommendation

**B now, C once #58 settles the segment taxonomy.**

Write `docs/research/liquidity_unified_framework.md` as a **mapping table**, not a new metric. One
row per asset class; columns for the liquidity notion in that class, the structural reading, and the
modelling caveat. Open it by stating finding 1 explicitly — that stress and normal-times liquidity
stay separate, and why that is a feature.

Smallest first step, doable in one sitting: **write the equities row and the bond row only.** They
are the two the note contrasts most sharply, and getting them right will expose whether the mapping
generalises before anyone invests in four more rows.

What this forecloses: a single headline "liquidity score". If a stakeholder needs one number, this
recommendation will disappoint them — and finding 1 is the argument for why they should not have one.

## Acceptance criteria

- [ ] `docs/research/liquidity_unified_framework.md` exists with at least the equities and bond rows
- [ ] It states explicitly that stress and normal-times liquidity map to different quantities, naming
      `absorptive_capacity` and `redundancy`
- [ ] It records the share-vs-amount decision from finding 2, with the reasoning
- [ ] Retail vs institutional is handled as separate `MarketBoundary` segments, not separate metrics
- [ ] Every external microstructure claim carries a primary citation, or is marked unverified
- [ ] No new metric is added to `src/amf/` by this work
- [ ] No identifier introduced contains a `FORBIDDEN` substring

## Guardrail notes

- **Non-trading boundary.** This topic is dense with forbidden vocabulary — `price`, `trade`,
  `order`, `returns`. Prose here may use them; `src/amf/` may not name them. If option C adds example
  markets, component names must be structural (`"settlement"`, `"market making"`), never instruments.
- **Illustrative, not validated.** The note asks which measure "best predicts crisis". The deliverable
  may survey that literature. It must not conclude that AMF predicts crises, and must not add
  user-facing text implying it.
- **Determinism.** Any metric mapping must land in `[0, 1]` so `Severity.from_score` keeps its
  guarantees.

## Open questions

- **Does depth belong in `redundancy` or in reliance scaling?** (finding 2) Needs a decision before
  the mapping is written. Candidate for `decisions.md` once settled.
- **Which microstructure measures actually predict crisis?** (finding 6) Needs primary literature;
  out of scope for an agent without source access.
- **Does #58 intend retail/institutional as separate segments?** Finding 3 assumes yes. If #58
  decides otherwise, this dossier's option B needs revisiting.
