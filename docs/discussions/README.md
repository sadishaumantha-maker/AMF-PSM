# Repository Discussion Modules — Advanced Computational & Quantum Research

> **Purpose of this directory**: one self-contained, dense theoretical module per research
> discussion, each ready to be posted verbatim as a GitHub Discussion in this repository.
> Each module reproduces its source specification word for word, then develops the formal
> theory, the standard graduate curriculum around it, and the exact academic source
> material behind every claim.

---

## 0. Source of record

Every module in this directory derives from a single source document committed at
[`docs/QUANTUM_NEURAL_RESEARCH.md`](../QUANTUM_NEURAL_RESEARCH.md). Its header metadata is
reproduced here verbatim so that nothing from the source note is lost in the split:

```markdown
# Advanced Computational & Quantum Research Discussions

**Generated**: August 20, 2026
**Purpose**: Explore cutting-edge computational approaches (quantum, neural, information-theoretic) to enhance AMF predictions and systemic risk detection
```

And its footer, likewise verbatim:

```markdown
**Created**: August 20, 2026
**Maintained by**: Quantum-Neural Research Initiative
**Contact**: Open discussions in repository
```

The source note groups its eleven discussions under four thematic headings, reproduced here
exactly as they appear:

```markdown
## 🔬 Quantum Computing in Finance
## 🧠 Deep Neural Networks for Market Prediction
## 🌊 Quantum-Neural Hybrid Systems
## 🔗 Integration & Implementation
```

---

## 1. Module index

Eleven discussions are planned, one file each. **None of the module files has been written
yet** — this section is the specification for them, not an index of existing documents. The
`Module` column names the filename each module will take when it lands in this directory;
the names are deliberately shown as plain filenames rather than links, because a link to a
file that does not exist fails the repository's Markdown link check.

When a module is written, add it to this directory and turn its filename into a link in the
same pull request.

> **Status: the module files are not committed yet.** This index landed ahead of the eleven
> files it describes, so the codes below are plain filenames rather than links — a link to a
> file that does not exist fails the Markdown link check in CI, and with it the whole
> `validate` job. Restore each entry to a link in the same pull request that adds its file.

### 🔬 Quantum Computing in Finance

| Code | Module | Discussion title to use | Suggested category | Core theory |
|------|--------|------------------------|--------------------|-------------|
| **Q1** | `Q1-quantum-market-superposition.md` | Quantum Interpretation for Financial State Superposition | Ideas / Research | Hilbert-space postulates, density matrices, measurement, decoherence |
| **Q2** | `Q2-quantum-markov-lindblad.md` | Markov Chains as Quantum State Transitions | Ideas / Research | Markov chains, CPTP maps, GKSL/Lindblad generators, non-Markovianity |
| **Q3** | `Q3-shannon-information-market-entropy.md` | Shannon Information Theory & Market Entropy | Ideas / Research | Entropy, mutual information, channel capacity, transfer entropy |

### 🧠 Deep Neural Networks for Market Prediction

| Code | Module | Discussion title to use | Suggested category | Core theory |
|------|--------|------------------------|--------------------|-------------|
| **D1** | `D1-deep-learning-architectures.md` | Deep Learning Architectures for Multi-Asset Forecasting | Ideas / Research | Recurrent gating, self-attention, message passing, GNN expressivity |
| **D2** | `D2-embedding-spaces-regimes.md` | Embedding Spaces & Latent Representations of Market Regimes | Ideas / Research | Manifold learning, VAE/ELBO, contrastive objectives, projection pitfalls |
| **D3** | `D3-knowledge-graphs-causal-pathways.md` | Neural Connection Pathways & Knowledge Graphs | Ideas / Research | Ontologies, structural causal models, do-calculus, identification strategies |

### 🌊 Quantum-Neural Hybrid Systems

| Code | Module | Discussion title to use | Suggested category | Core theory |
|------|--------|------------------------|--------------------|-------------|
| **H1** | `H1-quantum-neural-hybrid-circuits.md` | Quantum Circuits as Neural Network Components | Ideas / Research | Variational circuits, parameter-shift rule, barren plateaus, quantum kernels |
| **H2** | `H2-topological-data-analysis.md` | Topological Data Analysis (TDA) & Persistent Homology | Ideas / Research | Simplicial homology, persistence modules, stability, Takens embedding |
| **H3** | `H3-symplectic-hamiltonian-dynamics.md` | Symplectic Geometry & Hamiltonian Dynamics | Ideas / Research | Symplectic manifolds, Liouville's theorem, symplectic integrators, port-Hamiltonian systems |

### 🔗 Integration & Implementation

| Code | Module | Discussion title to use | Suggested category | Core theory |
|------|--------|------------------------|--------------------|-------------|
| **I1** | `I1-unified-framework-architecture.md` | Unified Framework Architecture | Ideas / Research | Forecast combination, proper scoring, calibration, conformal prediction |
| **I2** | `I2-validation-backtesting-generalization.md` | Validation, Backtesting & Generalization | Ideas / Research | Learning theory under dependence, purged CV, data-snooping tests, rare-event evaluation |

---

## 2. Cross-cutting prerequisite map

The eleven modules are not independent. This is the dependency order a reading group should
follow; an arrow means "the target module assumes the source module's language".

```
                    ┌──────────────────────────────────────────┐
                    │  Foundations (take these first)          │
                    │  linear algebra · measure-theoretic      │
                    │  probability · real analysis · statistics│
                    └──────────────────┬───────────────────────┘
                                       │
        ┌──────────────┬───────────────┼───────────────┬──────────────────┐
        ▼              ▼               ▼               ▼                  ▼
     Q3 (info      D1 (deep        H3 (classical   H2 (algebraic     D3 (causal
     theory)       learning)       mechanics)      topology)         inference)
        │              │               │               │                  │
        ▼              ▼               │               │                  │
     Q1 (quantum   D2 (latent         │               │                  │
     postulates)   representations)   │               │                  │
        │              │               │               │                  │
        ▼              │               │               │                  │
     Q2 (open       ───┴───► H1 (variational quantum ML)                  │
     quantum                     │                                        │
     systems)                    │                                        │
        │                        │                                        │
        └────────────┬───────────┴──────────────┬─────────────────────────┘
                     ▼                          ▼
                  I1 (ensemble integration) ──► I2 (validation & generalisation)
```

`I2` is deliberately last and deliberately gating: no module's claims mean anything until
they survive the evaluation discipline described there.

---

## 3. Adoption roadmap

Reproduced verbatim from the source note:

```markdown
## 🎯 Adoption Roadmap (24 Months)

| Phase | Timeline | Focus | Deliverables |
|-------|----------|-------|--------------|
| **1** | Months 1–4 | Theory & prototypes | Q1, Q2, Q3, D1–D2 discussions; basic implementations |
| **2** | Months 5–12 | Integration & testing | H1–I1 frameworks; backtesting infrastructure |
| **3** | Months 13–20 | Refinement & scaling | GPU acceleration; cloud deployment |
| **4** | Months 21–24 | Production & monitoring | Live predictions; alerts; feedback loops |
```

### 3.1 Governance annotations on the roadmap

The roadmap above is the source note's own plan and is preserved unaltered. Three of its
line items cannot be executed as written inside this repository without breaking rules that
`CLAUDE.md` states are hard. They are recorded here so the discussion can resolve them
rather than discover them late:

| Roadmap item | Constraint it meets | Resolution to discuss |
|---|---|---|
| "basic implementations" of Q1–Q3, D1–D2 inside `src/amf/` | Zero-runtime-dependency rule; the note's deliverables import Qiskit/Cirq/PyTorch | Host research code in a separate, out-of-tree sidecar repository or an optional extra that the `amf` package never imports |
| "backtesting infrastructure" | Non-trading boundary — `backtest` is on the mechanically enforced `FORBIDDEN` substring list, as are `price`, `returns`, `trade`, `signal`, `portfolio` | Reframe as *structural retrodiction*: replay historical structural configurations of the seven systems and score the resilience index, using structural vocabulary only |
| "Live predictions; alerts" | "Illustrative, not validated" — the package must not claim predictive power, and its output is not a forecast of any real market | Keep as a research-sidecar capability with its own disclaimers; the `amf` package itself continues to emit structural diagnostics, not predictions |

Each module's **§6 Repository governance and boundary analysis** works this through in
detail for its own deliverables.

---

## 4. How to contribute

Reproduced verbatim from the source note:

```markdown
## 📌 How to Contribute

**For each discussion:**
1. **Open GitHub Discussion** (link to this document)
2. **Propose implementation approach** (quantum simulator? neural architecture?)
3. **Suggest domain data sources** (academic papers, market data APIs)
4. **Form research team** (assign lead researchers)
5. **Set milestones** (monthly deliverables)
```

### 4.1 Posting these modules as GitHub Discussions

Step 1 above — "Open GitHub Discussion" — is a repository-settings action that must be
performed through the GitHub web UI or a token with `discussions: write`; it cannot be
committed. The procedure:

1. **Enable Discussions** if it is not already on: repository **Settings → General →
   Features → Discussions**.
2. **Create the categories** used by the index table above. `Ideas` and `Research` are both
   suitable; `Research` may need to be added under **Discussions → Categories → New
   category** with the *Open-ended discussion* format.
3. For each module, **create a new Discussion**, set the title to the "Discussion title to
   use" column, and paste the module file's contents as the body. The files are written as
   complete Discussion bodies — GitHub-flavoured Markdown, no LaTeX rendering assumed, no
   relative-path images.
4. **Link back**: put the resulting Discussion URL into the module file's header block, and
   add the reverse link in the table in §1 of this file, so the committed document and the
   live thread stay findable from each other.
5. **Label** each Discussion with its code (`Q1` … `I2`) so cross-references in comments
   resolve unambiguously.

The module files are the source of record; the Discussion threads are where the conversation
happens. When a thread reaches a conclusion, amend the module file in a pull request rather
than letting the file and the thread drift apart.

### 4.2 What a good contribution to one of these threads looks like

- **A citation, not an assertion.** Every module's §4 is an annotated bibliography; extend it
  the same way, with author, year, exact title, venue, and a one-line statement of the exact
  contribution. Entries whose identifiers cannot be verified should carry no identifier at
  all rather than a guessed one.
- **A falsifiable claim.** Each module's §7 states propositions in a form that could be
  refuted, and says what evidence would refute them. Proposals that cannot fail are not yet
  research proposals.
- **A boundary check.** State explicitly which of the four hard repository rules your
  proposal touches, and how it stays inside them. §6 of each module is the template.
- **An honest negative result.** The skeptical literature is cited in every module on
  purpose. A comment that reports a method failing on this problem is worth as much as one
  reporting it succeeding.

---

## 5. Standing constraints that apply to every module

These are restated in each file's §6, and are non-negotiable regardless of what any thread
concludes:

1. **Non-trading boundary.** The `amf` package models market *structure and resilience*
   only. `tests/unit/test_non_trading_boundary.py` walks every public class reachable from
   `amf.__all__` and rejects public names, members and dataclass fields containing `order`,
   `buy`, `sell`, `price`, `pnl`, `broker`, `backtest`, `ticker`, `trade`, `portfolio`,
   `candlestick`, `returns`, `signal`. Structural vocabulary — `load`, `stress`,
   `absorptive_capacity`, `transmission`, `coupling` — is the only vocabulary available.
2. **Illustrative, not validated.** Thresholds, weights and scores are not empirically
   validated. Nothing here is financial advice, a diagnosis, or a forecast of any real
   market, and no module may claim predictive power or validated performance.
3. **Zero runtime dependencies, determinism, and the coverage gate.** The package is
   standard-library only; identical inputs must give bit-identical output; randomness lives
   only behind an explicit seed; the branch-coverage gate is 100%. Any proposal that needs
   NumPy, PyTorch, Qiskit, Cirq or GUDHI belongs outside the package boundary.
4. **Protected artefacts.** `AMF Framework v1.docx`, its `.ots` proof,
   `anatomical-market-framework`, `LICENSE.txt` and `SHA256SUMS` are checksum-protected and
   must never be modified. Distribution stays private; nothing is published to PyPI.

---

**Created**: August 20, 2026 · **Source**: `docs/QUANTUM_NEURAL_RESEARCH.md`
**Maintained by**: Quantum-Neural Research Initiative
**Contact**: Open discussions in repository
