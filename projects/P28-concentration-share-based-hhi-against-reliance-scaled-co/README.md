# P28 - Concentration: share-based HHI against reliance-scaled concentration

**Track E - Diagnostics, Sensitivity & Leverage**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Quantitative methodologist |
| **Upstream** | `DiagnosticConfig.scale_concentration_by_reliance`; `CLAUDE.md` -> Diagnostics |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The framework already states the problem in its own documentation: concentration is a share-based Herfindahl index, so a system with a single coupling scores 1.0 at any weight and a system with none scores 0. An opt-in flag multiplies by total outgoing weight, and it is off by default *because turning it on moves every published concentration score*. Backward compatibility is currently deciding a methodological question.

## 2. Purpose

Decide the concentration measure on methodological grounds and stop letting the default be set by reluctance to change published numbers. Whichever wins, the losing option is removed or clearly demoted.

## 3. Scope

**In scope**

- A statement of what concentration is meant to measure in AMF: unevenness of reliance, or amount of reliance.
- An analysis of the degenerate cases: one edge at weight 0.05, and zero edges.
- A measured comparison across generated markets and a default decision.

**Out of scope**

- Changing the blend weights - that is P29.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Write down the question the component answers. The Herfindahl index measures unevenness of a distribution; it says nothing about the size of the thing distributed.
2. Enumerate the degenerate cases explicitly and state what a reader would expect each to score.
3. Consult the industrial-organisation literature on where HHI is and is not appropriate, and the composite-indicator guidance on normalising sub-indicators.
4. Measure both variants across generated markets, reporting how many rankings flip.
5. Choose the default on the methodology. If the published numbers move, that is a corrected number, not a regression.
6. Remove or clearly deprecate the losing variant so the configuration surface does not carry an unresolved argument.

## 5. Task board

- [ ] State the question concentration answers.
- [ ] Enumerate and rule on the degenerate cases.
- [ ] Survey the appropriateness of HHI for this use.
- [ ] Measure ranking flips between variants.
- [ ] Set the default and deprecate the loser.
- [ ] Publish `docs/diagnostics/concentration.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** State what each variant measures and what each degenerate case should score.
- **Inputs:** `diagnostics.py`, the reading list.
- **Output artifact:** `docs/diagnostics/concentration.md`.
- **Stop condition:** Both degenerate cases have an expected value derived from the stated question.

### `literature-scout`

- **Mandate:** Establish the accepted scope of the Herfindahl index and composite sub-indicator normalisation.
- **Inputs:** The reading list.
- **Output artifact:** An annotated evidence table.
- **Stop condition:** The evidence addresses share-based versus level-based indices directly.

### `benchmark-runner`

- **Mandate:** Measure ranking flips between variants across generated markets.
- **Inputs:** Both implementations.
- **Output artifact:** A flip-rate table.
- **Stop condition:** Flip rate is reported with uncertainty across at least one hundred markets.

### `release-marshal`

- **Mandate:** Record the changed default as a breaking behavioural change and deprecate the losing flag.
- **Inputs:** The decision.
- **Output artifact:** A CHANGELOG entry and a deprecation note.
- **Stop condition:** The entry states which published numbers move and why.

**Hand-off order:** `math-formalizer` -> `literature-scout` -> `benchmark-runner` -> `release-marshal`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-config-validator` | A configuration default changes | Validates the domain and regenerates boundary tests. |
| `amf-changelog-entry` | A published score changes | Records the change under `Changed` with its justification. |
| `amf-red-team` | A default is proposed | Argues for the opposite default and forces measurement to answer. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/diagnostics/concentration.md`
- A ranking flip-rate measurement
- The new default
- A deprecation path for the losing variant

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The question concentration answers is stated before the measure is chosen.
- [ ] Both degenerate cases have a derived expected value and a matching test.
- [ ] The default is set by methodology, and any moved number is recorded in `CHANGELOG.md`.
- [ ] The configuration surface no longer carries an unresolved argument.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Tirole, J. (1988). *The Theory of Industrial Organization*. MIT Press.
- OECD & European Commission JRC (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD Publishing.
- Saltelli, A., Ratto, M., Andres, T., Campolongo, F., Cariboni, J., Gatelli, D., Saisana, M., & Tarantola, S. (2008). *Global Sensitivity Analysis: The Primer*. Wiley.
- Jackson, M. O. (2008). *Social and Economic Networks*. Princeton University Press.
- Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.
- Goodhart, C. A. E. (1984). "Problems of Monetary Management: The U.K. Experience." In *Monetary Theory and Practice*. Macmillan. (Goodhart's Law)

## 11. Commit protocol

Commits from this project use the scope `p28`:

```text
docs(p28): state what the concentration component measures and rule on degenerate cases
test(p28): measure ranking flips between share-based and reliance-scaled concentration
fix(p28)!: set the methodologically justified concentration default
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

