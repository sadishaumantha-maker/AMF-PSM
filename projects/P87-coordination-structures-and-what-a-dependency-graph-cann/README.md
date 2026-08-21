# P87 - Coordination structures and what a dependency graph cannot distinguish

**Track O - Market Abuse and Forensic Network Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Network scientist |
| **Upstream** | Discussion 4.2; P24 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Coordinated behaviour and common dependence produce the same structural signature: participants moving together. A dependency graph records that they are coupled, not why. Any framework claiming to see coordination in structure alone is claiming to distinguish two things its data cannot separate.

## 2. Purpose

Prove the indistinguishability rather than assert it, and derive from it what the framework may report about coordination - which is expected to be very little.

## 3. Scope

**In scope**

- A constructive proof: two markets with identical structure and different underlying causes.
- A statement of the additional information that would be needed to separate them.
- A reporting rule derived from the result.

**Out of scope**

- Any claim that observed coupling indicates agreement between parties.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Construct the pair explicitly: one market where systems are coupled by common dependence and one where they are coupled by coordination, with identical dependency graphs. If you can build the pair, the indistinguishability is proved, not argued.
2. Identify what would separate them - timing, counterparty identity, communication records - and note that all of it is outside the framework by design.
3. Read the algorithmic-collusion literature, which shows coordination can arise without agreement at all, making the inference from structure to intent weaker still.
4. Derive the reporting rule: the framework may report coupling and may not characterise its cause.
5. Add the constructed pair as a regression test, so any future feature claiming to distinguish them must first defeat it.
6. Record the result where a reader of a coupling score will see it.

## 5. Task board

- [ ] Construct the identical-structure pair.
- [ ] State the separating information and why it is out of scope.
- [ ] Review the algorithmic-collusion evidence.
- [ ] Derive and record the reporting rule.
- [ ] Add the pair as a regression test.
- [ ] Publish `docs/graph/coordination_limits.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** Construct the identical-structure pair and state the indistinguishability formally.
- **Inputs:** The graph model.
- **Output artifact:** A constructed pair with proof.
- **Stop condition:** The two markets are structurally identical and causally different by construction.

### `unit-test-author`

- **Mandate:** Add the pair as a regression test.
- **Inputs:** The construction.
- **Output artifact:** A test case.
- **Stop condition:** Any code claiming to distinguish the pair fails the test.

### `literature-scout`

- **Mandate:** Establish that coordination can arise without agreement.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary.
- **Stop condition:** The claim is sourced from peer-reviewed work.

### `red-team-critic`

- **Mandate:** Attempt to characterise the cause of coupling from framework output.
- **Inputs:** Rendered output.
- **Output artifact:** A characterisation attempt report.
- **Stop condition:** No attempt succeeds.

**Hand-off order:** `math-formalizer` -> `unit-test-author` -> `literature-scout` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-graph-algorithm` | The pair is constructed | Verifies the two graphs are identical under every structural query. |
| `amf-invariant-spec` | The indistinguishability is stated | Writes it into the docstring and mirrors it as a test. |
| `amf-red-team` | Coupling is reported | Tests whether the output characterises the cause. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/graph/coordination_limits.md`
- A constructed indistinguishable pair
- A regression test
- A reporting rule

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The pair is structurally identical under every structural query.
- [ ] The regression test fails any code claiming to distinguish them.
- [ ] The reporting rule appears where coupling is reported.
- [ ] No output characterises the cause of coupling.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Calvano, E., Calzolari, G., Denicolo, V., & Pastorello, S. (2020). "Artificial Intelligence, Algorithmic Pricing, and Collusion." *American Economic Review* 110(10), 3267-3297.
- Akoglu, L., Tong, H., & Koutra, D. (2015). "Graph based anomaly detection and description: a survey." *Data Mining and Knowledge Discovery* 29(3), 626-688.
- Tirole, J. (1988). *The Theory of Industrial Organization*. MIT Press.
- Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.
- Jackson, M. O. (2008). *Social and Economic Networks*. Princeton University Press.
- Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.). Cambridge University Press.
- European Union (2014). *Regulation (EU) No 596/2014 on market abuse (Market Abuse Regulation)*. Official Journal of the European Union.

## 11. Commit protocol

Commits from this project use the scope `p87`:

```text
docs(p87): prove coordination and common dependence are structurally indistinguishable
test(p87): pin the indistinguishable market pair as a regression
docs(p87): restrict reporting to coupling without characterising its cause
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
