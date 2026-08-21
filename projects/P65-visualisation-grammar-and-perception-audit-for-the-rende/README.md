# P65 - Visualisation grammar and perception audit for the renderers

**Track K - Communication, Visualisation & Documentation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Visualisation designer |
| **Upstream** | `src/amf/viz.py`; `_FOOTNOTE` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

`viz.py` draws severity-coloured dependency graphs and stress timelines using the standard library alone. The colour scale, the encoding choices and the layout are undocumented design decisions. Colour is one of the least accurate visual encodings for magnitude, and a severity palette that is not colour-vision-safe will mislead a substantial minority of readers.

## 2. Purpose

Audit the visual encodings against perception research, fix the ones that misrepresent, and document the grammar so future figures are consistent rather than improvised.

## 3. Scope

**In scope**

- An encoding audit: what each visual channel represents and how accurately that channel conveys it.
- A colour-vision-safe severity palette with documented contrast.
- A written visual grammar for future figures.

**Out of scope**

- Adding matplotlib, Graphviz or any rendering dependency.
- Removing the mandatory footnote from any rendered image.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Inventory every visual channel currently used: position, colour, line weight, size, and what each encodes.
2. Check each against the perception literature on channel accuracy; colour hue is poor for ordered magnitude and should carry category or be paired with a redundant channel.
3. Test the severity palette for colour-vision safety and for greyscale legibility, since these figures will be printed.
4. Where colour alone carries severity, add a redundant encoding rather than only changing the hues.
5. Verify the mandatory footnote survives every change, in every rendered format.
6. Confirm byte-identical repeat renders after every modification; the determinism guarantee applies to figures too.

## 5. Task board

- [ ] Inventory the visual channels and what they encode.
- [ ] Audit each channel against perception research.
- [ ] Build a colour-vision-safe severity palette.
- [ ] Add redundant encoding where colour alone carries meaning.
- [ ] Verify footnote presence and render determinism.
- [ ] Publish `docs/viz/grammar.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish channel accuracy rankings and colour-safety guidance from primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated encoding guidance summary.
- **Stop condition:** Channel accuracy is sourced from empirical perception research.

### `viz-designer`

- **Mandate:** Rebuild the palette and add redundant encodings without new dependencies.
- **Inputs:** The audit.
- **Output artifact:** A diff under `src/amf/viz.py`.
- **Stop condition:** Severity is never carried by hue alone and the palette is colour-vision-safe.

### `determinism-prover`

- **Mandate:** Verify byte-identical repeat renders after every change.
- **Inputs:** The renderers.
- **Output artifact:** Render determinism tests.
- **Stop condition:** Two renders of the same input are byte-identical in every format.

### `docs-synthesizer`

- **Mandate:** Write the visual grammar for future figures.
- **Inputs:** The audit and the new palette.
- **Output artifact:** `docs/viz/grammar.md`.
- **Stop condition:** Every channel has a stated permitted use.

**Hand-off order:** `literature-scout` -> `viz-designer` -> `determinism-prover` -> `docs-synthesizer`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-figure-render` | Any figure is produced | Applies the grammar, verifies the footnote and checks byte-identical repeats. |
| `amf-determinism-audit` | A renderer changes | Confirms repeat renders are byte-identical. |
| `amf-doc-page` | The grammar is published | Enforces documentation conventions. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/viz/grammar.md`
- A colour-vision-safe severity palette
- Redundant encodings for severity
- Render determinism tests

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] No visual channel encodes magnitude less accurately than an available alternative without a stated reason.
- [ ] Severity is never carried by hue alone.
- [ ] The mandatory footnote is present in every rendered format.
- [ ] Repeat renders are byte-identical.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Cleveland, W. S., & McGill, R. (1984). "Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods." *JASA* 79(387), 531-554.
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information* (2nd ed.). Graphics Press.
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
- Bertin, J. (1983). *Semiology of Graphics: Diagrams, Networks, Maps*. University of Wisconsin Press.
- Ware, C. (2020). *Information Visualization: Perception for Design* (4th ed.). Morgan Kaufmann.
- Spiegelhalter, D., Pearson, M., & Short, I. (2011). "Visualizing Uncertainty About the Future." *Science* 333(6048), 1393-1400.

## 11. Commit protocol

Commits from this project use the scope `p65`:

```text
docs(p65): audit the visualisation encodings against perception research
fix(p65): make the severity palette colour-vision-safe with redundant encoding
test(p65): pin byte-identical repeat renders across formats
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

