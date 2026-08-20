# P61 - Regime transitions: Markov formalism against quantum-superposition language

**Track J - Advanced Methods: Topology, Learning, Information & Quantum**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Research lead |
| **Upstream** | `docs/QUANTUM_NEURAL_RESEARCH.md` Discussions Q1, Q2 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The research document describes market states using the language of quantum superposition and treats Markov chains as quantum state transitions. Markov chains are classical stochastic processes; quantum state transitions are not. Borrowing the vocabulary does not import the mathematics, and using it in a diagnostic instrument's documentation risks the framework being read as physics-flavoured decoration.

## 2. Purpose

Adjudicate the terminology: adopt the classical formalism that actually applies, and either justify the quantum vocabulary mathematically or remove it from the framework's language.

## 3. Scope

**In scope**

- A statement of what the classical Markov formalism provides for regime modelling.
- A precise account of what quantum superposition is and why probability mixtures are not it.
- A terminology ruling applied across the research documentation.

**Out of scope**

- Implementing regime transitions before the formalism is settled.
- Retaining any metaphor that cannot be defined operationally.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Set out the classical formalism: a regime is a state, transitions are a stochastic matrix, and everything the discussion wants - uncertain current regime, transition probabilities, stationary behaviour - is available classically.
2. State precisely what distinguishes a quantum superposition from a classical probability mixture: interference and non-commuting observables, neither of which appears anywhere in the framework.
3. Apply the repository's own metaphor discipline: a borrowed term must either be defined operationally or dropped.
4. Rule, and apply the ruling by editing the research documentation rather than leaving the terminology in place.
5. Record the ruling so the vocabulary does not reappear.
6. Note that this ruling does not close the door on genuine quantum methods; that question is P63.

## 5. Task board

- [ ] Write the classical Markov account of regime modelling.
- [ ] Write the precise account of what superposition requires.
- [ ] Apply the metaphor discipline rule.
- [ ] Rule on the terminology.
- [ ] Edit the research documentation to match the ruling.
- [ ] Publish `docs/methods/regime_formalism.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** State both formalisms precisely and identify what the framework actually contains.
- **Inputs:** `docs/QUANTUM_NEURAL_RESEARCH.md`, the reading list.
- **Output artifact:** `docs/methods/regime_formalism.md`.
- **Stop condition:** Interference and non-commuting observables are addressed explicitly.

### `docs-synthesizer`

- **Mandate:** Apply the ruling by editing the affected research documentation.
- **Inputs:** The ruling.
- **Output artifact:** An edited `docs/QUANTUM_NEURAL_RESEARCH.md`.
- **Stop condition:** No undefined quantum term remains in the framework's language.

### `red-team-critic`

- **Mandate:** Argue the metaphor has pedagogical value worth keeping.
- **Inputs:** The ruling.
- **Output artifact:** A dissent section.
- **Stop condition:** The dissent is answered, and any retained metaphor is operationally defined.

**Hand-off order:** `math-formalizer` -> `docs-synthesizer` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-invariant-spec` | A formalism is adopted | Requires the formal object and its operations to be named before use. |
| `amf-doc-page` | Research documentation is edited | Enforces documentation conventions and the metaphor discipline. |
| `amf-red-team` | A borrowed term is retained | Requires an operational definition or removal. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/methods/regime_formalism.md`
- A terminology ruling
- Edited research documentation
- A recorded precedent

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The classical formalism is stated with the operations it provides.
- [ ] The distinction between superposition and probability mixture is stated precisely.
- [ ] No undefined quantum term remains in the framework's language.
- [ ] The ruling is recorded as a precedent for future borrowed terminology.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Norris, J. R. (1997). *Markov Chains*. Cambridge University Press.
- Hamilton, J. D. (1994). *Time Series Analysis*. Princeton University Press.
- Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information* (10th Anniversary ed.). Cambridge University Press.
- Cover, T. M., & Thomas, J. A. (2006). *Elements of Information Theory* (2nd ed.). Wiley.
- Shannon, C. E. (1948). "A Mathematical Theory of Communication." *Bell System Technical Journal* 27(3), 379-423.
- Box, G. E. P. (1976). "Science and Statistics." *Journal of the American Statistical Association* 71(356), 791-799.
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.

## 11. Commit protocol

Commits from this project use the scope `p61`:

```text
docs(p61): state the classical Markov formalism for regime modelling
docs(p61): rule on quantum-superposition terminology
docs(p61): apply the terminology ruling to the research documentation
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

