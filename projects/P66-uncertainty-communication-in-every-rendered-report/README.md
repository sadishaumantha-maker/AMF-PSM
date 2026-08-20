# P66 - Uncertainty communication in every rendered report

**Track K - Communication, Visualisation & Documentation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Communication lead |
| **Upstream** | `report.py`; the P19, P29 and P39 uncertainty outputs |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The renderers report point estimates: an overall index, a resilience score, a ranked finding list. Once P19, P29 and P39 produce intervals and stability figures, the renderers must decide how to show them. Showing a number without its uncertainty invites false precision; showing too much makes the report unreadable. Neither failure is acceptable in a diagnostic instrument.

## 2. Purpose

Design and implement an uncertainty presentation for every output format that is honest without being unreadable, grounded in the research on communicating uncertainty to non-specialists.

## 3. Scope

**In scope**

- A presentation design per format: text, markdown and JSON.
- A rule for significant figures that reflects the actual precision of each quantity.
- Implementation across the renderers with the existing purity guarantees preserved.

**Out of scope**

- Any I/O, clock reading or randomness inside a renderer.
- Suppressing uncertainty to make a report look cleaner.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Establish what is known about communicating uncertainty to non-specialists; the evidence favours frequency framings and explicit ranges over verbal qualifiers.
2. Set the significant-figure rule from the measured precision, not from the float representation; reporting an index to six decimals when the weight simplex moves it in the second is false precision.
3. Design each format separately: text is read linearly, markdown can carry a table, JSON must stay machine-parseable and complete.
4. Implement without breaking renderer purity; no I/O, no clock, no randomness.
5. Keep `render_json` as the only renderer that serialises a distribution, per the existing contract.
6. Test that every uncertainty figure survives a round trip through the JSON format.

## 5. Task board

- [ ] Review uncertainty communication evidence.
- [ ] Set the significant-figure rule from measured precision.
- [ ] Design presentation per output format.
- [ ] Implement across the renderers.
- [ ] Verify renderer purity is preserved.
- [ ] Publish `docs/reporting/uncertainty.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish evidence-based uncertainty communication practice from primary research.
- **Inputs:** The reading list.
- **Output artifact:** An annotated practice summary.
- **Stop condition:** Recommendations trace to empirical studies, not style guides.

### `docs-synthesizer`

- **Mandate:** Design the presentation for each format.
- **Inputs:** The practice summary and the renderer contract.
- **Output artifact:** `docs/reporting/uncertainty.md`.
- **Stop condition:** Each format has a design that respects how it is read or parsed.

### `algorithm-implementer`

- **Mandate:** Implement across the renderers preserving purity.
- **Inputs:** The design.
- **Output artifact:** A diff under `src/amf/report.py`.
- **Stop condition:** No I/O, clock or randomness is introduced; `mypy` strict passes.

### `red-team-critic`

- **Mandate:** Attempt to quote a report figure as more precise than it is.
- **Inputs:** Rendered output.
- **Output artifact:** A false-precision report.
- **Stop condition:** No figure can be quoted beyond its measured precision.

**Hand-off order:** `literature-scout` -> `docs-synthesizer` -> `algorithm-implementer` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-ensemble-stats` | An interval is rendered | Supplies the estimator name and the interval alongside the point estimate. |
| `amf-doc-page` | The presentation is documented | Enforces documentation conventions. |
| `amf-red-team` | A figure is rendered | Tests whether it can be quoted at false precision. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/reporting/uncertainty.md`
- A significant-figure rule
- Uncertainty presentation in all three formats
- Round-trip tests

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every point estimate is rendered with its uncertainty where one exists.
- [ ] Significant figures reflect measured precision, not float representation.
- [ ] Renderers remain pure - no I/O, clock or randomness.
- [ ] `render_json` remains machine-parseable and complete.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Spiegelhalter, D., Pearson, M., & Short, I. (2011). "Visualizing Uncertainty About the Future." *Science* 333(6048), 1393-1400.
- Gigerenzer, G., Gaissmaier, W., Kurz-Milcke, E., Schwartz, L. M., & Woloshin, S. (2007). "Helping Doctors and Patients Make Sense of Health Statistics." *Psychological Science in the Public Interest* 8(2), 53-96.
- Morgan, M. G., & Henrion, M. (1990). *Uncertainty: A Guide to Dealing with Uncertainty in Quantitative Risk and Policy Analysis*. Cambridge University Press.
- Manski, C. F. (2013). *Public Policy in an Uncertain World: Analysis and Decisions*. Harvard University Press.
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information* (2nd ed.). Graphics Press.
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
- Saltelli, A., et al. (2020). "Five ways to ensure that models serve society: a manifesto." *Nature* 582, 482-484.

## 11. Commit protocol

Commits from this project use the scope `p66`:

```text
docs(p66): design evidence-based uncertainty presentation per output format
feat(p66): render uncertainty alongside every point estimate
test(p66): pin significant figures to measured precision
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

