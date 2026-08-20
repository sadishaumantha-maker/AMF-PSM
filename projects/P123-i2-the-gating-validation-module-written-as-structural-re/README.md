# P123 - I2 - the gating validation module, written as structural retrodiction

**Track T - The Promised Research Modules**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 3 weeks |
| **Lead role** | Research-methods lead |
| **Upstream** | `docs/discussions/README.md` module I2; the governance annotations in its section 3.1 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The index calls I2 deliberately last and deliberately gating - no module's claims mean anything until they survive the discipline described there - and then names that discipline with a word the repository's own boundary test forbids. The index has already proposed the resolution: reframe as structural retrodiction, replaying recorded structural configurations and scoring the resilience index. The dispute is whether that reframing is substantive or cosmetic, and it is decided by whether anyone can say what a replay would be evaluated against - which is exactly the question I1 leaves open.

## 2. Purpose

Write the gating module: define structural retrodiction precisely, state the evaluation discipline it requires, and rule on whether the framework can be validated at all in its present form.

## 3. Scope

**In scope**

- A precise definition of structural retrodiction, with its inputs, its procedure and its scoring target.
- The dependence problem stated exactly - why independent-sample learning theory does not apply.
- The multiple-comparison and leakage disciplines, stated as procedure rather than as warning.
- A ruling on validatability in the present form, and what would have to change.

**Out of scope**

- Any use of the forbidden vocabulary in a public name, a field or a test helper.
- Historical market data of any kind entering this repository.
- Any claim of validated performance - the standing constraints forbid it and this module must not weaken them.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Define structural retrodiction operationally, in a form someone could execute: a dated structural configuration of the seven systems, assembled by the case-study protocol from published sources; a recorded shock; the resilience index computed; and a stated comparison target. If the fourth element cannot be supplied, the definition fails, and the module says so.
2. State the dependence problem exactly. Independent-sample bounds require independence, structural configurations of the same market at nearby dates are strongly dependent, and the sample size at the level of distinct market episodes is small - tens, not thousands. Write the arithmetic.
3. Write the multiple-comparison discipline as procedure: how many configurations were examined, how many thresholds were tried, and what the false-discovery correction is. The repository has tunable weights and thresholds throughout, and a validation claim that does not count its own degrees of freedom is not a validation claim.
4. Write the leakage discipline concretely, since it is the failure mode that has quietly invalidated whole literatures: if a configuration is assembled with knowledge of how the episode turned out, the assembly is contaminated, and the case-study protocol must forbid it in writing.
5. Reach the ruling. If, after all of the above, the honest answer is that the framework cannot presently be validated and its illustrative-not-validated disclaimer is therefore load-bearing rather than defensive, write that, and note that it makes the disclaimer a finding rather than a hedge.
6. Check every name the module proposes against the boundary list before it is written down, not after - this module is where a forbidden name would most plausibly be introduced.
7. Cross-reference the falsification charter rather than duplicating it: this module supplies the evaluation procedure, that one supplies what would count as refutation.

## 5. Task board

- [ ] Define structural retrodiction operationally, all four elements.
- [ ] State the dependence problem with the episode-count arithmetic.
- [ ] Write the multiple-comparison discipline as countable procedure.
- [ ] Write the leakage prohibition into the case-study protocol.
- [ ] Rule on validatability in the present form.
- [ ] Boundary-check every proposed name before adoption.
- [ ] Publish `docs/discussions/I2-validation-backtesting-generalization.md` and relink it.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** Define structural retrodiction operationally and write the ruling.
- **Inputs:** The case-study protocol, the I1 inventory.
- **Output artifact:** `docs/discussions/I2-validation-backtesting-generalization.md`.
- **Stop condition:** All four elements of the definition are supplied or the failure is stated.

### `literature-scout`

- **Mandate:** Assemble learning-theory-under-dependence, multiple-comparison and leakage sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated bibliography.
- **Stop condition:** The leakage source reports measured consequences, not warnings.

### `boundary-sentinel`

- **Mandate:** Check every proposed name against the forbidden list before it is adopted.
- **Inputs:** `tests/unit/test_non_trading_boundary.py`, the draft.
- **Output artifact:** A name verdict list.
- **Stop condition:** No proposed name contains a forbidden substring; no allowlist entry is proposed.

### `case-study-archivist`

- **Mandate:** Write the leakage prohibition into the case-study protocol as a procedural rule.
- **Inputs:** The protocol.
- **Output artifact:** A protocol amendment.
- **Stop condition:** The rule states what an assembler may not know, and when.

### `red-team-critic`

- **Mandate:** Attack the ruling by trying to construct a validation claim the module would let through.
- **Inputs:** The draft.
- **Output artifact:** An adversarial construction attempt.
- **Stop condition:** Either an unsound claim passes - and the discipline is tightened - or none does.

### `citation-verifier`

- **Mandate:** Verify every citation in the module resolves.
- **Inputs:** The draft.
- **Output artifact:** A verification report.
- **Stop condition:** No identifier is guessed.

**Hand-off order:** `spec-drafter` -> `literature-scout` -> `boundary-sentinel` -> `case-study-archivist` -> `red-team-critic` -> `citation-verifier`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-case-dossier` | The retrodiction inputs are specified | Enforces the dated, sourced case-file format and the leakage rule. |
| `amf-boundary-check` | Any name is proposed | Checks it against the forbidden substring list before adoption. |
| `amf-source-vetting` | Sources are cited | Confirms standing and resolves identifiers. |
| `amf-red-team` | The discipline is drafted | Attempts to pass an unsound validation claim through it. |
| `amf-doc-page` | The module is published | Enforces conventions and disclaimer placement. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/discussions/I2-validation-backtesting-generalization.md`
- An operational definition of structural retrodiction
- A leakage prohibition in the case-study protocol
- A ruling on validatability in the present form

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The definition supplies all four elements or states which one fails.
- [ ] The dependence problem is stated with episode-count arithmetic.
- [ ] The multiple-comparison discipline requires counting degrees of freedom.
- [ ] The leakage prohibition is procedural and dated.
- [ ] No forbidden substring enters any proposed name, and no allowlist entry is proposed.
- [ ] The ruling is stated even if it is that validation is not presently possible.
- [ ] The index link resolves and `Validate metadata` passes.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Vapnik, V. N. (1998). *Statistical Learning Theory*. Wiley.
- Arlot, S., & Celisse, A. (2010). "A survey of cross-validation procedures for model selection." *Statistics Surveys* 4, 40-79.
- Kapoor, S., & Narayanan, A. (2023). "Leakage and the reproducibility crisis in machine-learning-based science." *Patterns* 4(9), 100804.
- Benjamini, Y., & Hochberg, Y. (1995). "Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing." *Journal of the Royal Statistical Society: Series B* 57(1), 289-300.
- Quinonero-Candela, J., Sugiyama, M., Schwaighofer, A., & Lawrence, N. D. (eds.) (2009). *Dataset Shift in Machine Learning*. MIT Press.
- Arjovsky, M., Bottou, L., Gulrajani, I., & Lopez-Paz, D. (2019). "Invariant Risk Minimization." arXiv:1907.02893.
- Ioannidis, J. P. A. (2005). "Why Most Published Research Findings Are False." *PLoS Medicine* 2(8), e124.
- Gelman, A., & Loken, E. (2014). "The Statistical Crisis in Science." *American Scientist* 102(6), 460-465.
- Meehl, P. E. (1990). "Appraising and Amending Theories: The Strategy of Lakatosian Defense and Two Principles That Warrant It." *Psychological Inquiry* 1(2), 108-141.
- Popper, K. R. (1959). *The Logic of Scientific Discovery*. Hutchinson.
- Manski, C. F. (2013). *Public Policy in an Uncertain World: Analysis and Decisions*. Harvard University Press.
- Stodden, V., McNutt, M., Bailey, D. H., et al. (2016). "Enhancing reproducibility for computational methods." *Science* 354(6317), 1240-1241.

## 11. Commit protocol

Commits from this project use the scope `p123`:

```text
docs(p123): define structural retrodiction and its four required elements
docs(p123): write the dependence, multiple-comparison and leakage disciplines
docs(p123): publish the gating I2 module and rule on validatability
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
