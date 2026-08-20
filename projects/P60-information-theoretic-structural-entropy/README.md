# P60 - Information-theoretic structural entropy

**Track J - Advanced Methods: Topology, Learning, Information & Quantum**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Applied mathematician |
| **Upstream** | `docs/QUANTUM_NEURAL_RESEARCH.md` Discussion Q3 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Shannon entropy is proposed as a market measure. Entropy is well defined only over a probability distribution, and the discussion does not say what the distribution is over. Applied to the dependency weights it is a concentration measure closely related to the Herfindahl index the framework already uses - which makes it either a duplicate or a genuine alternative, and nobody has determined which.

## 2. Purpose

Define precisely what distribution any entropy measure would be taken over, compare it against the existing concentration component, and adopt it only if it measures something the framework does not already measure.

## 3. Scope

**In scope**

- A candidate distribution definition over dependency weights.
- An analytical and empirical comparison against the existing concentration score.
- A ruling: adopt as an alternative, adopt as a complement, or reject as a duplicate.

**Out of scope**

- Entropy over price or return distributions - forbidden.
- Any use of the word entropy without a stated distribution.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Define the distribution explicitly: normalised outgoing dependency weights per system form a probability vector.
2. Note the relationship: entropy and the Herfindahl index are both functions of that same vector, and both are concentration measures with different sensitivity to the tail.
3. Derive where the two orderings differ analytically, then confirm empirically on generated markets.
4. If entropy orders differently in a way that matters structurally, that is the case for adopting it as a complement.
5. If the orderings agree almost everywhere, reject it as a duplicate and record the finding so it is not proposed again.
6. Apply the same rule to any other information-theoretic quantity proposed later: name the distribution first.

## 5. Task board

- [ ] Define the distribution explicitly.
- [ ] Derive the analytical relationship to the concentration score.
- [ ] Measure ordering differences on generated markets.
- [ ] Rule adopt, complement or reject.
- [ ] Write the name-the-distribution rule for future proposals.
- [ ] Publish `docs/methods/structural_entropy.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** Define the distribution and derive the relationship to the existing concentration measure.
- **Inputs:** `diagnostics.py`, the reading list.
- **Output artifact:** `docs/methods/structural_entropy.md`.
- **Stop condition:** The relationship is derived, not asserted.

### `benchmark-runner`

- **Mandate:** Measure where the two orderings differ across generated markets.
- **Inputs:** Both measures.
- **Output artifact:** An ordering-difference table.
- **Stop condition:** Rank correlation is reported across at least one hundred markets.

### `red-team-critic`

- **Mandate:** Argue the measure is a duplicate and force the evidence to answer.
- **Inputs:** The comparison.
- **Output artifact:** A dissent section.
- **Stop condition:** The dissent is adopted or answered with the ordering evidence.

### `boundary-sentinel`

- **Mandate:** Ensure no entropy proposal drifts toward price or return distributions.
- **Inputs:** The draft and any code.
- **Output artifact:** A boundary report.
- **Stop condition:** The distribution is over structural weights only.

**Hand-off order:** `math-formalizer` -> `benchmark-runner` -> `red-team-critic` -> `boundary-sentinel`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-invariant-spec` | A measure is defined over a distribution | Requires the distribution to be named and documented before the measure is used. |
| `amf-boundary-check` | An information measure is proposed | Rejects distributions over market-data quantities. |
| `amf-red-team` | A measure is proposed for adoption | Argues it duplicates an existing one and requires evidence. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/methods/structural_entropy.md`
- An analytical relationship derivation
- An ordering-difference measurement
- A ruling and a name-the-distribution rule

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The distribution is named explicitly before any entropy is computed.
- [ ] The analytical relationship to the concentration score is derived.
- [ ] Ordering differences are measured across at least one hundred markets.
- [ ] The ruling is recorded so the proposal is not reopened without new evidence.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Shannon, C. E. (1948). "A Mathematical Theory of Communication." *Bell System Technical Journal* 27(3), 379-423.
- Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley.
- Tirole, J. (1988). *The Theory of Industrial Organization*. MIT Press.
- Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.
- OECD & European Commission JRC (2008). *Handbook on Constructing Composite Indicators: Methodology and User Guide*. OECD Publishing.
- Jackson, M. O. (2008). *Social and Economic Networks*. Princeton University Press.

## 11. Commit protocol

Commits from this project use the scope `p60`:

```text
docs(p60): name the distribution any structural entropy is taken over
test(p60): measure where entropy and concentration orderings differ
docs(p60): rule on adopting structural entropy
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

