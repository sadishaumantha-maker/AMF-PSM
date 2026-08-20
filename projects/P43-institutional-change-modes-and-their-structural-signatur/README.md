# P43 - Institutional change modes and their structural signature

**Track G - Policy Architecture & Regulatory Regimes**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Policy researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 1.3; issue #123 (31d) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The discussion asks which institutional change mode - displacement, layering, drift or conversion - creates the most market disruption, and proposes comparing two major post-crisis reform programmes as instances of layering and displacement. The dispute is whether those episodes can be classified cleanly at all, and whether 'disruption' can be measured structurally without reaching for market data.

## 2. Purpose

Classify a set of reform episodes by change mode using the published typology, define a purely structural notion of disruption that AMF can represent, and report what each mode does to the dependency structure.

## 3. Scope

**In scope**

- Application of the four-mode typology to at least six documented reform episodes.
- A structural definition of disruption expressed in AMF terms: edges added or removed, tiers changed, absorptive capacity affected.
- A per-mode structural signature, or a documented finding that no clean signature exists.

**Out of scope**

- Any measure of disruption based on prices, volumes or returns - forbidden by the non-trading rule.
- Claiming a mode causes a specific market outcome.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Take the typology from its primary source, including the authors' own warnings about classification difficulty.
2. Classify each episode with an explicit justification and a confidence marker; a contested classification is data, not failure.
3. Define disruption structurally: which dependency edges change, which tier is touched, which systems lose absorptive capacity.
4. Map each episode onto that structural definition using the AMF vocabulary.
5. Report per-mode signatures only if the episodes support them; a null result is publishable and preferable to a forced pattern.
6. Keep every quantity dimensionless and structural throughout.

## 5. Task board

- [ ] Extract the typology from its primary source with the authors' caveats.
- [ ] Select and classify at least six reform episodes.
- [ ] Define disruption structurally in AMF terms.
- [ ] Map each episode to the structural definition.
- [ ] Test for per-mode signatures.
- [ ] Publish `docs/policy/change_modes.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Extract the change-mode typology and its stated limits from the primary source.
- **Inputs:** The reading list.
- **Output artifact:** An annotated typology summary with caveats.
- **Stop condition:** The authors' own classification caveats are quoted, not omitted.

### `case-study-archivist`

- **Mandate:** Build a dated, cited file per reform episode.
- **Inputs:** Official texts and peer-reviewed accounts.
- **Output artifact:** Episode files under `docs/policy/_cases/`.
- **Stop condition:** Each episode has enactment dates and at least two independent sources.

### `spec-drafter`

- **Mandate:** Define disruption structurally and map episodes onto it.
- **Inputs:** Typology and episode files.
- **Output artifact:** `docs/policy/change_modes.md`.
- **Stop condition:** The definition uses only dimensionless structural quantities.

### `boundary-sentinel`

- **Mandate:** Verify no market-data vocabulary enters the definition or any proposed code.
- **Inputs:** The draft and any code sketch.
- **Output artifact:** A boundary report.
- **Stop condition:** No forbidden term appears in any proposed public name.

**Hand-off order:** `literature-scout` -> `case-study-archivist` -> `spec-drafter` -> `boundary-sentinel`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-case-dossier` | A reform episode is documented | Builds the dated, sourced structural file. |
| `amf-boundary-check` | A structural measure is proposed | Runs the non-trading naming guard against the proposal. |
| `amf-red-team` | A per-mode signature is claimed | Attempts to reclassify episodes and see whether the signature survives. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/change_modes.md`
- At least six sourced episode files
- A structural disruption definition
- A signature analysis or a null result

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every episode classification carries a justification and a confidence marker.
- [ ] Disruption is defined without any market-data quantity.
- [ ] The non-trading boundary guard passes for every proposed name.
- [ ] A null result is reported as such if no signature holds.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Streeck, W., & Thelen, K. (eds.) (2005). *Beyond Continuity: Institutional Change in Advanced Political Economies*. Oxford University Press.
- Mahoney, J., & Thelen, K. (eds.) (2010). *Explaining Institutional Change: Ambiguity, Agency, and Power*. Cambridge University Press.
- Pierson, P. (2000). "Increasing Returns, Path Dependence, and the Study of Politics." *American Political Science Review* 94(2), 251-267.
- United States Congress (2010). *Dodd-Frank Wall Street Reform and Consumer Protection Act*, Pub. L. 111-203.
- European Union (2014). *Directive 2014/65/EU on markets in financial instruments (MiFID II)*. Official Journal of the European Union.
- Basel Committee on Banking Supervision (2011). *Basel III: A global regulatory framework for more resilient banks and banking systems* (rev. June 2011). Bank for International Settlements.
- North, D. C. (1990). *Institutions, Institutional Change and Economic Performance*. Cambridge University Press.

## 11. Commit protocol

Commits from this project use the scope `p43`:

```text
docs(p43): extract the institutional change-mode typology with its stated limits
docs(p43): add sourced reform episode files
docs(p43): define disruption structurally and test for per-mode signatures
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

