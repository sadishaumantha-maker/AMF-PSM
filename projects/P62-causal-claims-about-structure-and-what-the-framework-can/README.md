# P62 - Causal claims about structure and what the framework can support

**Track J - Advanced Methods: Topology, Learning, Information & Quantum**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Applied statistician |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Track 3; Discussion 3.2 (feedback loops markets and policy) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The framework's language is causal throughout: stress propagates, systems fail because others failed, interventions reduce stress. Inside the model those statements are definitionally true. Outside it they are empirical claims requiring identification. The documentation does not currently mark which is which, and a reader has no way to tell.

## 2. Purpose

Draw the line explicitly between model-internal causal statements and empirical causal claims, and specify what evidence would be needed before any empirical claim could be made.

## 3. Scope

**In scope**

- A classification of every causal statement in the framework's documentation as internal or empirical.
- An identification analysis: what would be required to support the empirical ones.
- A writing rule that marks model-internal statements as such.

**Out of scope**

- Making any empirical causal claim.
- Implementing causal-discovery methods on market data.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Inventory the causal language across the package docstrings, the renderers and the research documentation.
2. Classify each statement: model-internal (true by construction) or empirical (requires identification).
3. For the empirical ones, state what identification strategy would be needed - and note that for market structure, natural experiments are rare and identification is genuinely hard.
4. Review the candidate empirical methods honestly: predictive causality tests, information-transfer measures and state-space methods each have known limitations on short, non-stationary series.
5. Write the writing rule: model-internal causal statements must be marked, in every output format.
6. Apply the rule to the existing documentation as part of this project, not as follow-up work.

## 5. Task board

- [ ] Inventory causal language across the repository.
- [ ] Classify each statement internal or empirical.
- [ ] State the identification requirement per empirical claim.
- [ ] Review candidate methods and their limitations.
- [ ] Write and apply the marking rule.
- [ ] Publish `docs/methods/causal_claims.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish causal identification requirements and the limitations of the candidate methods.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary with limitations foregrounded.
- **Stop condition:** Each candidate method's known failure mode is stated.

### `spec-drafter`

- **Mandate:** Classify the causal inventory and write the marking rule.
- **Inputs:** The inventory.
- **Output artifact:** `docs/methods/causal_claims.md`.
- **Stop condition:** Every inventoried statement is classified.

### `docs-synthesizer`

- **Mandate:** Apply the marking rule across docstrings and renderers.
- **Inputs:** The rule.
- **Output artifact:** A documentation and renderer diff.
- **Stop condition:** Every model-internal causal statement is marked in text, markdown and JSON output.

### `red-team-critic`

- **Mandate:** Find a statement a reader would take as empirical that is only internal.
- **Inputs:** The marked documentation.
- **Output artifact:** A misreading report.
- **Stop condition:** No such statement remains unmarked.

**Hand-off order:** `literature-scout` -> `spec-drafter` -> `docs-synthesizer` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-red-team` | Causal language is drafted | Classifies each statement and flags unmarked model-internal claims. |
| `amf-doc-page` | Documentation is edited | Enforces the marking rule and the illustrative-not-validated rule. |
| `amf-source-vetting` | A causal method is cited | Requires the primary source and its stated limitations. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/methods/causal_claims.md`
- A classified causal-language inventory
- An identification requirement analysis
- An applied marking rule

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every causal statement in the repository is classified internal or empirical.
- [ ] Model-internal statements are marked in text, markdown and JSON output.
- [ ] No empirical causal claim is made anywhere.
- [ ] Each candidate method's limitations are stated alongside it.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.). Cambridge University Press.
- Peters, J., Janzing, D., & Scholkopf, B. (2017). *Elements of Causal Inference: Foundations and Learning Algorithms*. MIT Press.
- Granger, C. W. J. (1969). "Investigating Causal Relations by Econometric Models and Cross-spectral Methods." *Econometrica* 37(3), 424-438.
- Schreiber, T. (2000). "Measuring Information Transfer." *Physical Review Letters* 85(2), 461-464.
- Sugihara, G., et al. (2012). "Detecting Causality in Complex Ecosystems." *Science* 338(6106), 496-500.
- Manski, C. F. (2013). *Public Policy in an Uncertain World: Analysis and Decisions*. Harvard University Press.
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.
- Box, G. E. P. (1976). "Science and Statistics." *Journal of the American Statistical Association* 71(356), 791-799.

## 11. Commit protocol

Commits from this project use the scope `p62`:

```text
docs(p62): inventory and classify causal language across the repository
docs(p62): state the identification requirement for each empirical claim
docs(p62): mark model-internal causal statements in every output format
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

