# P124 - What would falsify the framework

**Track U - Method, Epistemics and External Validation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Research lead |
| **Upstream** | `CLAUDE.md` -> Illustrative, not validated |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The framework declares itself illustrative and not validated, which is honest. But an unvalidated model that also has no stated falsification condition is unfalsifiable, and an unfalsifiable model is not a weak scientific claim - it is not a scientific claim at all. Nobody has written down what observation would show the framework wrong.

## 2. Purpose

State falsification conditions for the framework's central claims, so that being unvalidated is a stage it is at rather than a permanent condition it is protected by.

## 3. Scope

**In scope**

- An enumeration of the framework's substantive empirical claims, if any.
- A falsification condition per claim, or an admission that the claim is definitional.
- A pre-registered protocol for any claim that could be tested.

**Out of scope**

- Running a validation study.
- Claiming validation on the basis of a protocol.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Enumerate the claims first, and separate them ruthlessly: 'a system with low redundancy and high criticality is fragile' is definitional given the formula, while 'markets with the structural signature the framework calls fragile fail more often' is empirical and testable.
2. Expect most claims to be definitional. That is worth knowing, because a model composed entirely of definitions cannot be wrong, only useful or not.
3. For each empirical claim, state what observation would refute it, following the strong-inference practice of designing the test that could kill the hypothesis.
4. Pre-register the protocol for any testable claim - the analysis plan written before the data - because the alternative is a garden of forking paths in which any result confirms the framework.
5. State the standing of a definitional model plainly: it is an instrument for organising thought, and the honest defence of it is coherence and usefulness rather than correctness.
6. Publish the protocol whether or not anyone runs it; an unrun pre-registration is still a commitment.

## 5. Task board

- [ ] Enumerate and classify the framework's claims.
- [ ] Separate definitional from empirical rigorously.
- [ ] State a falsification condition per empirical claim.
- [ ] Pre-register the analysis plan.
- [ ] State the standing of the definitional core.
- [ ] Publish `docs/methods/falsification.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish falsification, strong inference and pre-registration from primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated methodological summary.
- **Stop condition:** The criteria come from the primary philosophical and methodological literature.

### `spec-drafter`

- **Mandate:** Enumerate and classify every claim the framework makes.
- **Inputs:** `CLAUDE.md`, docstrings, renderers.
- **Output artifact:** A claim register with classifications.
- **Stop condition:** Every claim is marked definitional or empirical, with no third category used to avoid the choice.

### `math-formalizer`

- **Mandate:** State the falsification condition for each empirical claim.
- **Inputs:** The register.
- **Output artifact:** A condition per claim.
- **Stop condition:** Each condition names an observation that would refute the claim.

### `red-team-critic`

- **Mandate:** Attempt to show every claim is definitional and the framework unfalsifiable.
- **Inputs:** The register.
- **Output artifact:** An unfalsifiability argument.
- **Stop condition:** The argument is answered with at least one genuinely empirical claim, or conceded in writing.

**Hand-off order:** `literature-scout` -> `spec-drafter` -> `math-formalizer` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-source-vetting` | A methodological criterion is cited | Requires the primary source. |
| `amf-red-team` | A claim is classified | Argues it is definitional and forces the classification to hold. |
| `amf-doc-page` | The protocol is published | Enforces documentation conventions. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/methods/falsification.md`
- A classified claim register
- A falsification condition per empirical claim
- A pre-registered analysis plan

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every claim is classified definitional or empirical.
- [ ] Each empirical claim names a refuting observation.
- [ ] The analysis plan is pre-registered before any data is examined.
- [ ] If every claim is definitional, that is stated plainly.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Popper, K. R. (1959). *The Logic of Scientific Discovery*. Hutchinson.
- Lakatos, I. (1970). "Falsification and the Methodology of Scientific Research Programmes." In Lakatos, I. & Musgrave, A. (eds.), *Criticism and the Growth of Knowledge*. Cambridge University Press.
- Platt, J. R. (1964). "Strong Inference." *Science* 146(3642), 347-353.
- Meehl, P. E. (1990). "Appraising and Amending Theories: The Strategy of Lakatosian Defense and Two Principles That Warrant It." *Psychological Inquiry* 1(2), 108-141.
- Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). "The preregistration revolution." *PNAS* 115(11), 2600-2606.
- Gelman, A., & Loken, E. (2014). "The Statistical Crisis in Science." *American Scientist* 102(6), 460-465.
- Ioannidis, J. P. A. (2005). "Why Most Published Research Findings Are False." *PLoS Medicine* 2(8), e124.
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.

## 11. Commit protocol

Commits from this project use the scope `p124`:

```text
docs(p124): enumerate and classify every claim the framework makes
docs(p124): state a falsification condition for each empirical claim
docs(p124): pre-register the analysis plan for the testable claims
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
