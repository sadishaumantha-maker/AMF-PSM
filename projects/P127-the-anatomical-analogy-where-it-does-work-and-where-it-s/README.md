# P127 - The anatomical analogy: where it does work and where it smuggles conclusions

**Track U - Method, Epistemics and External Validation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Research lead |
| **Upstream** | The framework's central metaphor; `SystemKind` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The framework is built on an analogy between a market and a body. Analogies in science are legitimate and productive, and they also import structure that may not hold. The seven systems, their names, and the language of health and immunity all carry implications - that there is a healthy state, that the parts serve the whole, that disease is deviation - and none of those has been argued for markets.

## 2. Purpose

Audit the analogy properly: identify what it buys, what it assumes, and where it has already determined a modelling decision that should have been argued on its own terms.

## 3. Scope

**In scope**

- An analysis of the analogy's positive, negative and neutral parts in the standard sense.
- Identification of decisions the analogy made rather than argued.
- A ruling on each: keep with an argument, or revise.

**Out of scope**

- Renaming the framework or its systems as a first move; the audit comes first.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Use the established treatment of scientific analogy: the positive analogy is what genuinely corresponds, the negative what does not, and the neutral what is untested - and the neutral part is where both discovery and error live.
2. Identify smuggled conclusions concretely. `health = integrity x (1 - load)` presupposes there is a healthy state; `immune` presupposes that regulation defends the organism rather than serving some parts against others; `criticality` fixed per system presupposes the anatomy is the same everywhere.
3. That third one is testable against the framework's own content, since the factory defaults assign fixed criticalities to all seven systems in every market.
4. For each smuggled conclusion, rule: it is defensible and here is the argument, or it is an artefact and here is what changes.
5. Note the strongest case for the analogy - it gives a functional decomposition that is genuinely hard to obtain otherwise, which is why it has produced a usable model.
6. Keep the audit fair. The purpose is to know which parts are load-bearing, not to discredit the framework.

## 5. Task board

- [ ] Analyse the analogy into positive, negative and neutral parts.
- [ ] Identify decisions the analogy made rather than argued.
- [ ] Test the fixed-criticality assumption against the framework's own defaults.
- [ ] Rule per smuggled conclusion.
- [ ] State the analogy's genuine contribution.
- [ ] Publish `docs/methods/analogy_audit.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish the standard treatment of analogy and models in science.
- **Inputs:** The reading list.
- **Output artifact:** An annotated methodological summary.
- **Stop condition:** The positive/negative/neutral distinction is taken from the primary source.

### `spec-drafter`

- **Mandate:** Identify the smuggled conclusions and rule on each.
- **Inputs:** `systems.py`, `models.py`, the summary.
- **Output artifact:** `docs/methods/analogy_audit.md`.
- **Stop condition:** Every identified conclusion is defended with an argument or marked an artefact.

### `benchmark-runner`

- **Mandate:** Test whether fixed per-system criticality is defensible across constructed market types.
- **Inputs:** The factory defaults and generated markets.
- **Output artifact:** A measurement.
- **Stop condition:** The fixed-criticality assumption is supported or contradicted by measurement.

### `red-team-critic`

- **Mandate:** Argue the analogy is decorative and the framework would be identical without it.
- **Inputs:** The audit.
- **Output artifact:** A dissent section.
- **Stop condition:** The dissent is answered by naming what the analogy contributed.

**Hand-off order:** `literature-scout` -> `spec-drafter` -> `benchmark-runner` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-source-vetting` | A methodological claim is cited | Requires the primary source. |
| `amf-red-team` | The analogy is defended | Argues it is decorative and demands a concrete contribution. |
| `amf-doc-page` | The audit is published | Enforces documentation conventions. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/methods/analogy_audit.md`
- A positive/negative/neutral analysis
- A list of smuggled conclusions with rulings
- A measurement of the fixed-criticality assumption

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The analysis uses the established treatment of scientific analogy.
- [ ] Every smuggled conclusion is defended or marked an artefact.
- [ ] The fixed-criticality assumption is tested, not assumed.
- [ ] The analogy's genuine contribution is stated.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Hesse, M. B. (1966). *Models and Analogies in Science*. University of Notre Dame Press.
- Bailer-Jones, D. M. (2009). *Scientific Models in Philosophy of Science*. University of Pittsburgh Press.
- Weisberg, M. (2013). *Simulation and Similarity: Using Models to Understand the World*. Oxford University Press.
- Lakoff, G., & Johnson, M. (1980). *Metaphors We Live By*. University of Chicago Press.
- Kitano, H. (2004). "Biological robustness." *Nature Reviews Genetics* 5, 826-837.
- Csete, M. E., & Doyle, J. C. (2002). "Reverse Engineering of Biological Complexity." *Science* 295(5560), 1664-1669.
- Cannon, W. B. (1932). *The Wisdom of the Body*. W. W. Norton. (homeostasis)
- Gell-Mann, M. (1994). *The Quark and the Jaguar: Adventures in the Simple and the Complex*. W. H. Freeman.

## 11. Commit protocol

Commits from this project use the scope `p127`:

```text
docs(p127): analyse the anatomical analogy into positive, negative and neutral parts
test(p127): test the fixed per-system criticality assumption
docs(p127): rule on each conclusion the analogy made rather than argued
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

