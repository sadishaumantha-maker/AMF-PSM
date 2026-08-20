# P88 - Detection base rates and the arithmetic of a rare-event screen

**Track O - Market Abuse and Forensic Network Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Research lead |
| **Upstream** | P84; P85 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Every screening proposal in this repository - abuse susceptibility, structural outliers, fragility ranking - is a rare-event screen, and rare-event screens are governed by arithmetic most proposals ignore. At a low base rate, even a highly specific screen produces mostly false positives. If that arithmetic is not stated alongside every screening output, the framework will be over-trusted exactly where it is weakest.

## 2. Purpose

Make the base-rate arithmetic a standing requirement: any screening output ships with the calculation that shows what a positive result is worth.

## 3. Scope

**In scope**

- The base-rate calculation stated generally and worked for the framework's screens.
- A requirement that every screening output carries it.
- A presentation format that non-specialists read correctly.

**Out of scope**

- Inventing a base rate for any real market; where none is known, that is what is reported.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the arithmetic plainly with natural frequencies rather than conditional probabilities; the evidence on communicating this is unambiguous that frequencies are understood and probabilities are not.
2. Work the calculation for each screen the framework proposes, using a stated base rate - and where no base rate is known, say so, because an unknown base rate makes the positive predictive value unknown too.
3. Note the sharpest consequence: for a screen with no measured sensitivity or specificity, which describes every screen in this framework, the calculation cannot even be performed. That is the finding.
4. Design the presentation so the reader sees what a positive means before they see the positive.
5. Make it a requirement in the conventions, not a suggestion.
6. Link it to P66, which owns uncertainty presentation, so the two use one format.

## 5. Task board

- [ ] State the arithmetic in natural frequencies.
- [ ] Work it per proposed screen.
- [ ] Record where sensitivity, specificity or base rate is unknown.
- [ ] Design the presentation format.
- [ ] Add the standing requirement to the conventions.
- [ ] Publish `docs/reporting/base_rates.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** State the arithmetic and work it per screen, marking unknowns as unknown.
- **Inputs:** The proposed screens.
- **Output artifact:** A per-screen calculation table.
- **Stop condition:** No unknown quantity is replaced by an assumed one.

### `literature-scout`

- **Mandate:** Establish the evidence on communicating conditional risk to non-specialists.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary.
- **Stop condition:** The natural-frequency finding is sourced from empirical work.

### `docs-synthesizer`

- **Mandate:** Design the presentation and add the standing requirement.
- **Inputs:** The calculation table.
- **Output artifact:** `docs/reporting/base_rates.md`.
- **Stop condition:** The requirement is in the conventions and the format matches P66.

### `red-team-critic`

- **Mandate:** Attempt to over-read a positive screening result under the proposed format.
- **Inputs:** Draft output.
- **Output artifact:** An over-reading report.
- **Stop condition:** No over-reading survives the format.

**Hand-off order:** `math-formalizer` -> `literature-scout` -> `docs-synthesizer` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-ensemble-stats` | A screening rate is reported | Supplies intervals and the estimator name. |
| `amf-doc-page` | The requirement is published | Enforces documentation conventions. |
| `amf-red-team` | A screen reports a positive | Attempts to over-read it and reports whether the format prevents it. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/reporting/base_rates.md`
- A per-screen calculation table
- A natural-frequency presentation format
- A standing conventions requirement

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The arithmetic is presented in natural frequencies.
- [ ] Every screen has a worked calculation or an explicit unknown.
- [ ] No unknown is replaced by an assumption.
- [ ] Every screening output carries the calculation.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Gigerenzer, G., Gaissmaier, W., Kurz-Milcke, E., Schwartz, L. M., & Woloshin, S. (2007). "Helping Doctors and Patients Make Sense of Health Statistics." *Psychological Science in the Public Interest* 8(2), 53-96.
- Spiegelhalter, D., Pearson, M., & Short, I. (2011). "Visualizing Uncertainty About the Future." *Science* 333(6048), 1393-1400.
- Ioannidis, J. P. A. (2005). "Why Most Published Research Findings Are False." *PLoS Medicine* 2(8), e124.
- Gelman, A., & Loken, E. (2014). "The Statistical Crisis in Science." *American Scientist* 102(6), 460-465.
- Manski, C. F. (2013). *Public Policy in an Uncertain World: Analysis and Decisions*. Harvard University Press.
- Morgan, M. G., & Henrion, M. (1990). *Uncertainty: A Guide to Dealing with Uncertainty in Quantitative Risk and Policy Analysis*. Cambridge University Press.
- Dyck, A., Morse, A., & Zingales, L. (2010). "Who Blows the Whistle on Corporate Fraud?" *Journal of Finance* 65(6), 2213-2253.

## 11. Commit protocol

Commits from this project use the scope `p88`:

```text
docs(p88): state the base-rate arithmetic for rare-event screens
docs(p88): work the calculation per proposed screen and mark the unknowns
docs(p88): require the calculation to ship with every screening output
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

