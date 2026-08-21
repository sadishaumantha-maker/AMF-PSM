# P69 - Disclaimer integrity and defence against over-reading

**Track K - Communication, Visualisation & Documentation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Communication lead |
| **Upstream** | package docstring, `README.md`, `cli._DISCLAIMER`, `viz._FOOTNOTE` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Four separate disclaimers exist in four places, maintained independently. Independent copies drift, and a drifted disclaimer is worse than none because it suggests the strongest version was deliberately weakened somewhere. Separately, nobody has tested whether the disclaimers actually prevent over-reading.

## 2. Purpose

Establish a single source of truth for the disclaimer text, prove every surface carries it, and test empirically whether a reader can extract an over-claim from the rendered output despite it.

## 3. Scope

**In scope**

- A single canonical disclaimer with derived surface-specific forms.
- A test that fails if any surface loses or weakens its disclaimer.
- An over-reading test: adversarial extraction of an unsupported claim from real output.

**Out of scope**

- Weakening any disclaimer.
- Removing the footnote baked into rendered images.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Locate every disclaimer surface: the package docstring, the README, the CLI's stderr disclaimer, and the footnote baked into every rendered image.
2. Define one canonical statement and derive each surface's form from it, so drift becomes impossible rather than merely discouraged.
3. Add a test that asserts every surface carries its derived form; this is a governance test, not a cosmetic one.
4. Run the over-reading exercise: take real CLI output and attempt to write a defensible-looking but unsupported claim from it.
5. Where the exercise succeeds, strengthen the output, not only the disclaimer - a disclaimer does not undo a misleading number.
6. Confirm the CLI keeps writing the disclaimer to stderr so `--format json` stdout stays machine-parseable.

## 5. Task board

- [ ] Inventory every disclaimer surface.
- [ ] Define the canonical statement and the derivation.
- [ ] Add the surface-coverage test.
- [ ] Run the adversarial over-reading exercise.
- [ ] Strengthen output where over-reading succeeded.
- [ ] Publish `docs/disclaimers.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `docs-synthesizer`

- **Mandate:** Define the canonical disclaimer and derive each surface form.
- **Inputs:** All four surfaces.
- **Output artifact:** A canonical statement plus derivations.
- **Stop condition:** No surface carries independently authored text.

### `unit-test-author`

- **Mandate:** Add a test asserting every surface carries its derived disclaimer.
- **Inputs:** The derivation.
- **Output artifact:** A governance test.
- **Stop condition:** Removing or weakening any surface's disclaimer turns the test red.

### `red-team-critic`

- **Mandate:** Extract an unsupported but defensible-looking claim from real CLI output.
- **Inputs:** Real output from all subcommands.
- **Output artifact:** An over-reading report.
- **Stop condition:** Every successful extraction has produced an output change, not only a disclaimer change.

### `integrity-warden`

- **Mandate:** Confirm the image footnote survives every rendering path.
- **Inputs:** All `viz` outputs.
- **Output artifact:** A footnote coverage attestation.
- **Stop condition:** Every rendered format carries the footnote.

**Hand-off order:** `docs-synthesizer` -> `unit-test-author` -> `red-team-critic` -> `integrity-warden`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-red-team` | Output text or figures change | Attempts to extract an unsupported claim from the rendered result. |
| `amf-figure-render` | A figure is rendered | Verifies the mandatory footnote is present and unaltered. |
| `amf-doc-page` | Disclaimer text is edited | Enforces the canonical derivation rather than independent authoring. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/disclaimers.md`
- A canonical disclaimer with derived forms
- A surface-coverage governance test
- An over-reading report and resulting output changes

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every surface derives its disclaimer from one canonical statement.
- [ ] Weakening any surface's disclaimer turns a test red.
- [ ] Every successful over-reading extraction produced an output change.
- [ ] The CLI disclaimer still goes to stderr and JSON stdout stays machine-parseable.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.
- Saltelli, A., et al. (2020). "Five ways to ensure that models serve society: a manifesto." *Nature* 582, 482-484.
- Spiegelhalter, D., Pearson, M., & Short, I. (2011). "Visualizing Uncertainty About the Future." *Science* 333(6048), 1393-1400.
- Gigerenzer, G., Gaissmaier, W., Kurz-Milcke, E., Schwartz, L. M., & Woloshin, S. (2007). "Helping Doctors and Patients Make Sense of Health Statistics." *Psychological Science in the Public Interest* 8(2), 53-96.
- Manski, C. F. (2013). *Public Policy in an Uncertain World: Analysis and Decisions*. Harvard University Press.
- Board of Governors of the Federal Reserve System & OCC (2011). *Supervisory Guidance on Model Risk Management* (SR 11-7 / OCC Bulletin 2011-12).
- Box, G. E. P. (1976). "Science and Statistics." *Journal of the American Statistical Association* 71(356), 791-799.

## 11. Commit protocol

Commits from this project use the scope `p69`:

```text
docs(p69): define one canonical disclaimer and derive every surface form
test(p69): fail the build if any surface loses its disclaimer
fix(p69): strengthen output where the over-reading exercise succeeded
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
