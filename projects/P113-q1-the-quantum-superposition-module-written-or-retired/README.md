# P113 - Q1 - the quantum-superposition module, written or retired

**Track T - The Promised Research Modules**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Mathematical physicist |
| **Upstream** | `docs/discussions/README.md` module Q1; P75's write-or-retire ruling |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

`docs/discussions/README.md` promises `Q1-quantum-market-superposition.md` and the file does not exist. The substantive dispute underneath the dead link is harder than the link: a market state is not a ray in a Hilbert space, and saying that it is buys vocabulary rather than content. Superposition, density matrices and decoherence are precise objects with precise commitments - a complex inner-product space, unitary evolution, the Born rule - and a structural framework that adopts the words without the commitments is worse off than one that never mentioned them. The dispute is whether any of the formalism survives being taken seriously.

## 2. Purpose

Write the Q1 module to the standard the index advertises, and let the analysis reach a negative verdict if that is where the mathematics goes.

## 3. Scope

**In scope**

- The Hilbert-space postulates stated exactly, with every commitment they carry made explicit.
- A term-by-term audit of what a market state would have to be for each postulate to hold.
- A verdict on which parts, if any, are usable and which are metaphor.
- The module's sections 1-7 in the structure the index specifies.

**Out of scope**

- Any implementation inside `src/amf/` - the zero-dependency rule forbids a simulator in the package.
- Any claim that the framework predicts a market state.
- Asset prices, returns or any market data series.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the postulates from a primary text before applying anything: state space, composition by tensor product, unitary evolution, measurement, and the density-matrix generalisation to mixed states. Nothing may be applied before it is stated.
2. Audit each postulate against a structural market description one at a time, and write down what would have to be true. The composition postulate is the sharp one: coupled markets would have to compose by tensor product, and a seven-system model whose parts are described by real-valued metrics in `[0, 1]` does not.
3. Separate the two defensible readings from the indefensible one. A density matrix as a bookkeeping device for a classical mixture of structural configurations is defensible and is just a probability distribution; genuine superposition with interference is not, absent a mechanism that produces complex amplitudes.
4. Treat decoherence honestly: it is the mechanism by which quantum descriptions become classical, so invoking it as an analogy for regime change concedes the point that the classical description is the operative one.
5. Write section 6 - repository governance - against the four standing constraints in the index, and state plainly that the zero-dependency rule keeps any simulator outside the package.
6. Write section 7 as falsifiable propositions. `A market state is a superposition` is not falsifiable as stated; make each proposition say what observation would refute it, or drop it.
7. Let the verdict be negative if the audit says so. An honest module reporting that the formalism does not transfer is worth more than an enthusiastic one that borrows notation.

## 5. Task board

- [ ] State the postulates from a primary source.
- [ ] Audit each postulate against a structural market description.
- [ ] Separate the classical-mixture reading from the interference reading.
- [ ] Write the decoherence section without the analogy trick.
- [ ] Write section 6 against the four standing constraints.
- [ ] Write section 7 as refutable propositions.
- [ ] Publish `docs/discussions/Q1-quantum-market-superposition.md` and relink it in the index.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Assemble the primary quantum-foundations sources and the quantum-finance survey literature separately.
- **Inputs:** The reading list.
- **Output artifact:** An annotated bibliography with the two bodies kept apart.
- **Stop condition:** No survey paper is cited for a postulate a textbook states.

### `math-formalizer`

- **Mandate:** State the postulates and audit each against a structural market description.
- **Inputs:** The primary sources, `models.py`, `systems.py`.
- **Output artifact:** A postulate-by-postulate audit table.
- **Stop condition:** The tensor-product composition requirement is addressed explicitly, not skipped.

### `spec-drafter`

- **Mandate:** Write the module in the index's seven-section structure, verdict included.
- **Inputs:** The audit and bibliography.
- **Output artifact:** `docs/discussions/Q1-quantum-market-superposition.md`.
- **Stop condition:** Section 7's propositions each name the observation that would refute them.

### `citation-verifier`

- **Mandate:** Verify every citation resolves to a real work of the standing claimed.
- **Inputs:** The draft.
- **Output artifact:** A verification report.
- **Stop condition:** No identifier is guessed; an unverifiable entry carries none.

### `red-team-critic`

- **Mandate:** Attack the module for borrowed vocabulary unsupported by mathematics.
- **Inputs:** The draft.
- **Output artifact:** A borrowed-vocabulary report.
- **Stop condition:** Every quantum term either carries its formal commitment or is marked as analogy.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `spec-drafter` -> `citation-verifier` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-literature-brief` | The evidence base is assembled | Produces the annotated brief in the house format. |
| `amf-invariant-spec` | A postulate is stated formally | Records the commitments it carries and what would violate them. |
| `amf-red-team` | The module is drafted | Scans for terms used without their formal content. |
| `amf-doc-page` | The module is published | Enforces documentation conventions and disclaimer placement. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/discussions/Q1-quantum-market-superposition.md`
- A postulate-by-postulate audit table
- A written verdict on transferability
- A relinked index entry

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every postulate is stated from a primary source before it is applied.
- [ ] The tensor-product composition requirement is confronted, not omitted.
- [ ] The classical-mixture reading is distinguished from genuine superposition.
- [ ] Section 7's propositions are individually refutable.
- [ ] No implementation is added to `src/amf/`.
- [ ] The index link resolves and `Validate metadata` passes.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Nielsen, M. A., & Chuang, I. L. (2010). *Quantum Computation and Quantum Information* (10th Anniversary ed.). Cambridge University Press.
- von Neumann, J. (1955). *Mathematical Foundations of Quantum Mechanics* (R. T. Beyer, trans.). Princeton University Press.
- Dirac, P. A. M. (1958). *The Principles of Quantum Mechanics* (4th ed.). Oxford University Press.
- Sakurai, J. J., & Napolitano, J. (2020). *Modern Quantum Mechanics* (3rd ed.). Cambridge University Press.
- Zurek, W. H. (2003). "Decoherence, einselection, and the quantum origins of the classical." *Reviews of Modern Physics* 75(3), 715-775.
- Orus, R., Mugel, S., & Lizaso, E. (2019). "Quantum computing for finance: Overview and prospects." *Reviews in Physics* 4, 100028.
- Egger, D. J., et al. (2020). "Quantum Computing for Finance: State-of-the-Art and Future Prospects." *IEEE Transactions on Quantum Engineering* 1, 3101724.
- Hesse, M. B. (1966). *Models and Analogies in Science*. University of Notre Dame Press.
- Bailer-Jones, D. M. (2009). *Scientific Models in Philosophy of Science*. University of Pittsburgh Press.
- Popper, K. R. (1959). *The Logic of Scientific Discovery*. Hutchinson.

## 11. Commit protocol

Commits from this project use the scope `p113`:

```text
docs(p113): state the Hilbert-space postulates and their commitments
docs(p113): audit each postulate against a structural market description
docs(p113): publish the Q1 module and relink it from the index
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

