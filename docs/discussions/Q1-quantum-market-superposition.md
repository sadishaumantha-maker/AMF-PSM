# Q1: Quantum Interpretation for Financial State Superposition

> **Discussion category**: Research · **Labels**: `theory`, `quantum-information`, `boundary-review`, `not-validated`, `needs-reformulation`
> **Source**: `docs/QUANTUM_NEURAL_RESEARCH.md` § Discussion Q1
> **Status**: Open for comment · **Nature**: Theoretical module, illustrative and not
> empirically validated

## 0. Abstract and reading guide

This module asks whether the Hilbert-space formalism of quantum mechanics gives AMF
anything that Kolmogorov probability does not. It claims three things. First, that AMF's
present computations already *are* quantum-mechanical, in the degenerate sense that the
diagnostic index is a Born-rule expectation `Tr(rho S)` of a diagonal observable in a
diagonal state — so the formalism embeds exactly and adds exactly nothing. Second, that
everything the formalism could add lives in the off-diagonal entries of the density
operator, and AMF's determinism guarantee is formally equivalent to the statement that all
its diagnostic observables commute; introducing genuine quantum structure therefore
*breaks* a repository invariant rather than extending it. Third, that the source note's
four research questions admit precise answers, two of them negative, and that the negative
answers are the useful part.

It does **not** claim that markets are quantum systems, that superposition is a better
model of uncertainty than a mixture, that entanglement exists between asset classes, or
that any construction here predicts anything about any real market. Nothing below is
financial advice, a diagnosis, or a forecast.

**Prerequisite ladder.** Complex inner-product spaces and the spectral theorem
([28] Ch. 6–7, [29] Ch. 4) → the postulates of quantum mechanics ([18] Ch. 2, [19] Ch. 1)
→ density operators, partial trace, Schmidt decomposition ([18] §2.4–2.5) → POVMs, Kraus
operators, the Lüders rule ([21] Ch. 9, [22] Ch. 1) → quantum dynamical semigroups and
decoherence ([23] Ch. 3, [13]) → hidden Markov and Markov-switching models ([43], [44]).
Section 5 assumes the whole ladder; Sections 6–9 assume none of it.

## 1. Verbatim source specification

The following is reproduced word for word from `docs/QUANTUM_NEURAL_RESEARCH.md`,
including its notation, typography, and deliverable paths. It is quoted, not endorsed.

````markdown
### Discussion Q1: Quantum Interpretation for Financial State Superposition
**Theme**: Can quantum superposition model market uncertainty better than classical probability?

**Foundational Theory**:
- Classical: Market is in one state; we observe it imperfectly
- Quantum: Market exists in superposition of states; measurement collapses to reality
- Analogy: Schrödinger's portfolio — simultaneously bullish and bearish until observed

**Key Research Questions**:
1. **Superposition as Uncertainty Model**
   - Market price as quantum wavefunction: P(t) = Σ αᵢ|state_i⟩
   - States: {bullish, bearish, neutral, chaotic, regime-shift, ...}
   - Amplitude |αᵢ|² = probability of state i
   - Can this encode multi-regime market dynamics better than hidden Markov models?

2. **Entanglement as Cross-Market Correlation**
   - Entangled states: If stock A rises, bond B falls (coupled)
   - Classical: Covariance matrix (symmetric, finite correlation)
   - Quantum: Entanglement (non-local, spooky action at distance)
   - Use case: Predict contagion across markets (equity → credit → currency)
   - Measurement: Quantum mutual information vs. classical mutual information

3. **Measurement Problem & Market Impact**
   - Observer effect: Observation changes market (trading affects price)
   - Quantum mechanics: Measurement collapses wavefunction
   - Finance parallel: Trader enters order → market moves → filled at different price
   - Can we model market impact as wavefunction collapse?
   - Reduce market impact by "gentle measurement" (dark pools, algorithmic execution)?

4. **Decoherence & Market Efficiency**
   - Decoherence: Quantum state loses superposition (becomes classical)
   - Markets: Start chaotic (many scenarios); efficient markets remove uncertainty
   - Timeline: How fast does "decoherence" happen post-shock?
   - Policy role: Can central bank delay decoherence (maintain uncertainty longer)?

**Mathematical Framework**:
```
Quantum Market State:
|Ψ(t)⟩ = Σᵢ αᵢ(t) |sᵢ⟩  (superposition of market regimes)

Hamiltonian (time evolution):
i∂|Ψ⟩/∂t = H|Ψ⟩
where H includes: policy shocks, sentiment, liquidity, leverage

Measurement operator (observation):
O = {O₁ (price), O₂ (volume), O₃ (volatility), ...}

Post-measurement state (collapse):
|Ψ_post⟩ = (Oᵢ|Ψ⟩) / ||Oᵢ|Ψ⟩||
```

**Deliverable**: 
- `docs/research/quantum_market_superposition.md` — Theoretical framework
- `src/amf/quantum/superposition_model.py` — Implementation using Qiskit/Cirq
- Comparison: Quantum vs. HMM predictions on historical crises

**Research Leaders Needed**: Quantum physicist, financial mathematician
````

## 2. Formal foundations

Throughout, `H` denotes a finite-dimensional complex Hilbert space, `L(H)` the bounded
operators on it, `I` the identity, and `Tr` the trace. `A*` denotes the adjoint. All
statements below are standard; each is attributed to its originator, with a textbook
location for the proof.

### 2.1 States, observables, and the Born rule

**Definition 2.1 (Density operator).** A *state* on `H` is an operator `rho` in `L(H)`
with `rho = rho*`, `rho >= 0`, and `Tr(rho) = 1`. The set of states is convex and compact;
its extreme points are exactly the rank-one projections `|psi><psi|`, called *pure* states.
Non-extreme states are *mixed*. ([18] §2.4.1; [21] Ch. 2.)

**Definition 2.2 (Superposition vs. mixture).** For orthonormal `|a>`, `|b>` in `H`, the
pure superposition `|psi> = alpha|a> + beta|b>` has density operator

```
rho_pure = |alpha|^2 |a><a| + |beta|^2 |b><b| + alpha*conj(beta) |a><b| + conj(alpha)*beta |b><a|
```

whereas the classical mixture with the same weights is
`rho_mix = |alpha|^2 |a><a| + |beta|^2 |b><b|`. The two agree on their diagonal and differ
only in the *coherences* `rho_ab`. **This distinction is the entire empirical content of
"superposition".** A model whose reported quantities are all diagonal in the basis
`{|a>, |b>}` cannot distinguish `rho_pure` from `rho_mix`, and for such a model the words
"superposition" and "probability distribution" denote the same object.

**Definition 2.3 (POVM).** A *positive operator-valued measure* on a finite outcome set `X`
is a family `{E_x : x in X}` with `E_x >= 0` and `sum_x E_x = I`. It is *projective* (a
von Neumann measurement) when each `E_x` is an orthogonal projection and `E_x E_y = 0` for
`x != y`. ([18] §2.2.6; [26] Ch. 1.)

**Axiom 2.4 (Born rule).** Measuring `{E_x}` on state `rho` yields outcome `x` with
probability `p(x) = Tr(E_x rho)`. Due to Born [2], in the form given by von Neumann [1].

**Theorem 2.5 (Gleason, 1957).** Let `dim(H) >= 3` and let `mu` map the orthogonal
projections of `H` to `[0, 1]` with `mu(I) = 1` and `mu(sum_i P_i) = sum_i mu(P_i)` for any
countable family of mutually orthogonal projections. Then there is a unique density
operator `rho` with `mu(P) = Tr(rho P)` for every projection `P`. ([3]; proof in [21] §7-2.)

*Significance for this module.* Gleason's theorem says the Born rule is not an extra
modelling choice: once you commit to the projection lattice of a Hilbert space of dimension
at least three as your event structure, quadratic amplitude weighting is forced. AMF's
seven systems give `dim(H) = 7 >= 3`, so the hypothesis is satisfied. The theorem is
therefore a constraint, not a licence: you may not adopt the state space and then use some
other rule for turning it into numbers.

**Theorem 2.6 (Spectral theorem, finite dimension).** Every self-adjoint `A` in `L(H)`
admits `A = sum_k a_k P_k` with real `a_k` and mutually orthogonal projections `P_k`
summing to `I`. Two self-adjoint operators are simultaneously diagonalisable if and only if
they commute. ([28] Ch. 7; [29] Thm 4.1.5 and §1.3.)

### 2.2 Update rules

**Definition 2.7 (Lüders rule).** After a projective measurement with outcome `x` and
projection `P_x` such that `Tr(P_x rho) > 0`, the post-measurement state is
`rho' = P_x rho P_x / Tr(P_x rho)`. ([4]; discussion in [26] Ch. 4.)

**Definition 2.8 (Kraus / instrument form).** A general measurement is a family of
operators `{M_x}` with `sum_x M_x* M_x = I`; outcome `x` occurs with probability
`Tr(M_x* M_x rho)` and updates the state to `M_x rho M_x* / Tr(M_x* M_x rho)`. The induced
POVM is `E_x = M_x* M_x`. ([18] §2.2.3, §8.2.)

> **Correction to the source note.** The note's collapse formula
> `|Ψ_post⟩ = (Oᵢ|Ψ⟩) / ||Oᵢ|Ψ⟩||` is the Lüders rule only when `Oᵢ` is an orthogonal
> *projection*. Its list `O = {O₁ (price), O₂ (volume), O₃ (volatility), ...}` is a list of
> *observables*, not of projections, and observables are generally neither idempotent nor
> mutually orthogonal, so `sum_i Oᵢ != I` and the family is not a measurement in the sense
> of Definition 2.3. To make the note's framework well posed one must either (a) replace
> each `Oᵢ` by its spectral projections, giving one measurement per observable, or (b)
> supply Kraus operators `M_x` per Definition 2.8. This is not pedantry: without (a) or (b)
> the post-measurement states do not normalise and the probabilities do not sum to one.

**Theorem 2.9 (Gentle measurement lemma; Winter, 1999).** Let `rho` be a state and `E` an
element of a POVM with `0 <= E <= I`. If `Tr(E rho) >= 1 - eps`, then the post-measurement
state `rho' = sqrt(E) rho sqrt(E) / Tr(E rho)` satisfies

```
|| rho' - rho ||_1  <=  2 * sqrt(eps)
```

where `||.||_1` is the trace norm. ([14]; statement and proof as Lemma 9.4.1 in [25].)

*Significance.* This is the exact, theorem-grade content of the note's phrase "gentle
measurement": a measurement whose outcome you were already nearly certain of barely
disturbs the state. It is the only part of the note's item 3 that survives formalisation
intact, and it transfers to AMF (Proposition 5.11) without any market-data vocabulary.

### 2.3 Composite systems and entanglement

**Definition 2.10 (Composite system).** The state space of a system composed of parts
`1..n` is the tensor product `H = H_1 (x) ... (x) H_n`. A pure state is *product* if it
equals `|psi_1> (x) ... (x) |psi_n>`, and *entangled* otherwise. A mixed state is
*separable* if it is a convex combination of product states, entangled otherwise.

**Theorem 2.11 (Schmidt decomposition; Schmidt, 1907).** For any pure `|psi>` in
`H_A (x) H_B` there exist orthonormal `{|a_n>}` in `H_A`, orthonormal `{|b_n>}` in `H_B`,
and `lambda_n >= 0` with `sum_n lambda_n^2 = 1` such that
`|psi> = sum_n lambda_n |a_n> (x) |b_n>`. The number of nonzero `lambda_n` is the Schmidt
rank; `|psi>` is product iff the rank is 1. ([6]; as applied to quantum theory, [18] §2.5.)

*Proof sketch.* Write `|psi> = sum_{ij} c_ij |i>|j>` and take the singular value
decomposition `C = U D V*`. Absorb `U` into a new basis of `H_A` and `V*` into one of
`H_B`; the singular values are the `lambda_n`. The Schmidt theorem is the SVD in disguise,
which is why it is finite-dimensionally elementary. □

**Definition 2.12 (Entanglement entropy).** For pure `|psi>` and bipartition `A|B`,
`E(A|B) = S(rho_A) = -Tr(rho_A log_2 rho_A) = -sum_n lambda_n^2 log_2 lambda_n^2`, where
`rho_A = Tr_B |psi><psi|`.

**Definition 2.13 (Quantum mutual information).**
`I(A:B) = S(rho_A) + S(rho_B) - S(rho_AB)`, with `S` the von Neumann entropy.

**Proposition 2.14.** If `rho_AB = sum_{ij} p_ij |i><i| (x) |j><j|` is *classical–classical*
— diagonal in a fixed product basis — then `S` reduces to the Shannon entropy of `p`, and
`I(A:B)` equals the classical Shannon mutual information of the joint distribution `p_ij`.

*Proof.* All three reduced operators are diagonal in the same product basis, and the von
Neumann entropy of a diagonal density matrix is the Shannon entropy of its diagonal. The
three terms then reproduce `H(A) + H(B) - H(A,B)` exactly. □

*Significance.* Proposition 2.14 disposes of the note's item 2 measurement proposal:
"quantum mutual information vs. classical mutual information" is a distinction without a
difference for any classically-specified joint distribution. To get a gap you must first
exhibit a non-diagonal state, and AMF has none (Proposition 5.7).

**Theorem 2.15 (No-communication).** If `rho_AB` is a state on `H_A (x) H_B` and Alice
applies any instrument on `H_A`, the reduced state `rho_B = Tr_A(rho_AB)` is unchanged when
the outcome is not conditioned on. ([18] §2.4.3; [25] §4.6.)

*Significance.* The note's parenthetical "non-local, spooky action at distance" is
physically incorrect as a description of entanglement's operational content: entanglement
produces correlations that violate Bell inequalities [8] between *spacelike-separated*
parties with *freely chosen* measurement settings [7], and it transmits nothing. There is
no market analogue of spacelike separation with free setting choice — every coupling in
`DependencyGraph` is an explicit, directed, finite-weight channel with a definite
propagation path — so the phrase should be struck rather than modelled.

### 2.4 Dynamics

**Theorem 2.16 (Stone, 1932).** There is a bijection between strongly continuous
one-parameter unitary groups `{U(t)}` on `H` and self-adjoint operators `A`, given by
`U(t) = exp(-i t A)`. ([5]; textbook form in [19] §2.1.)

Consequently closed-system evolution is unitary, hence norm-preserving, reversible, and
entropy-preserving. This is the content of the note's `i d|Ψ>/dt = H|Ψ>`.

**Theorem 2.17 (GKLS generator; Gorini–Kossakowski–Sudarshan and Lindblad, 1976).** A
family `{T_t}` of completely positive, trace-preserving maps forming a norm-continuous
semigroup on `L(H)`, `dim(H) < inf`, has generator

```
d(rho)/dt  =  -i [H, rho]  +  sum_mu ( L_mu rho L_mu*  -  (1/2){ L_mu* L_mu , rho } )
```

for some self-adjoint `H` and operators `L_mu`. ([10], [11]; derivation in [23] §3.2.)

**Definition 2.18 (Pure dephasing).** Taking `L_k = sqrt(gamma_k) |k><k|` for an
orthonormal basis `{|k>}` gives, for `i != j`,

```
rho_ij(t) = rho_ij(0) * exp( -(gamma_i + gamma_j) t / 2 ),        rho_kk(t) = rho_kk(0).
```

*Proof.* Substitute into Theorem 2.17. The commutator term contributes a phase; each
`L_mu rho L_mu*` term contributes only to the diagonal, while the anticommutator term
contributes `-(1/2)(gamma_i + gamma_j) rho_ij` off the diagonal and cancels exactly on it.
Integrating the resulting decoupled scalar ODEs gives the stated solution. □

**Theorem 2.19 (Einselection; Zurek).** For a system coupled to an environment by an
interaction Hamiltonian `H_int`, the *pointer basis* is the eigenbasis of the system
observable that commutes with `H_int`; coherences off that basis decay on a timescale set
by the coupling, while the diagonal is preserved. ([13] §III; [12] for the original
scattering calculation; [24] Ch. 2–3.)

> **Correction to the source note.** Item 4 equates decoherence with the removal of
> uncertainty ("efficient markets remove uncertainty"). Decoherence does the opposite of
> what that sentence implies: by Definition 2.18 it leaves the diagonal of `rho` — the
> classical probability distribution, and hence the Shannon entropy in the pointer basis —
> exactly invariant while destroying interference. Decoherence converts a coherent
> superposition into an *equally uncertain* classical mixture. Whatever process removes
> uncertainty from a market, it is not the analogue of decoherence.

### 2.5 The classical comparators

**Axioms 2.20 (Kolmogorov, 1933).** A probability space is `(Omega, F, P)` with `F` a
`sigma`-algebra and `P` a countably additive measure with `P(Omega) = 1`. ([9].) The
event lattice `F` is a Boolean algebra and therefore *distributive*.

**Proposition 2.21.** The projection lattice of a Hilbert space with `dim >= 2` is not
distributive; in `C^2`, taking `P` = projection onto `|0>`, `Q` = projection onto `|+>`,
`R` = projection onto `|->`, one has `P and (Q or R) = P` while `(P and Q) or (P and R) = 0`.
Hence quantum probability is not a Kolmogorov model on the same event set. ([21] Ch. 7.)

*This is the single mathematically respectable reason to prefer quantum probability for
anything*: not "superposition", but non-distributivity, which is observable only through
non-commuting measurements and the order effects they produce ([30] Ch. 3; [32]).

**Definition 2.22 (HMM).** A hidden Markov model is `(S, X, A, B, pi)` with hidden states
`S`, observation alphabet `X`, row-stochastic transition matrix `A`, emission matrix `B`,
and initial distribution `pi`. ([43].)

**Definition 2.23 (Markov-switching regression; Hamilton, 1989).** An observed series
follows a linear model whose parameters are indexed by an unobserved `s`-state Markov
chain, estimated by a filter over regime probabilities. ([44]; [45] Ch. 22; survey [46].)

**Definition 2.24 (HQMM).** A hidden quantum Markov model replaces `(A, B)` by Kraus
operators `{K_x}` with `sum_x K_x* K_x = I`; observation `x` has probability
`Tr(K_x rho K_x*)` and updates `rho -> K_x rho K_x* / Tr(K_x rho K_x*)`.

**Theorem 2.25 (Gu, Wiesner, Rieper, Vedral, 2012).** For almost every stationary
stochastic process, the entropy of the minimal *quantum* generative model is strictly less
than the statistical complexity of the minimal *classical* one. ([17].)

*Significance, stated honestly.* Theorem 2.25 is a statement about the **memory** required
to generate a process, not about **predictive accuracy**. Both models reproduce the same
conditional distributions over futures. Any claim that a quantum regime model "predicts
better" than an HMM misreads this literature. See Proposition 5.9.

## 3. Academic curriculum modules

A graduate student equipped to referee this module would take, in this sequence:

| Module | Level | Canonical course(s) | Core texts (exact units) | What AMF needs from it |
|---|---|---|---|---|
| M1. Complex linear algebra | UG year 2–3 | MIT 18.06 *Linear Algebra*; MIT 18.700 | Axler [28] Ch. 6 (inner-product spaces), Ch. 7 (spectral theorem, PSD operators); Horn & Johnson [29] §1.3, Thm 4.1.5, Ch. 7 (PSD) | `rho >= 0`, `Tr rho = 1`; simultaneous diagonalisation; Kronecker products for the `2^7` construction |
| M2. Probability and measure | UG year 3 / MSc | MIT 18.600 *Probability and Random Variables*; graduate probability-theory sequence | Williams, *Probability with Martingales* Ch. 1–3; Billingsley, *Probability and Measure* Ch. 1–2 | Kolmogorov axioms [9] as the comparator; conditional expectation; why the projection lattice is different (Prop. 2.21) |
| M3. Quantum mechanics I–III | UG year 3–4 | MIT 8.04, 8.05, 8.06 *Quantum Physics I/II/III* | Griffiths & Schroeter [27] Ch. 3–4; Sakurai & Napolitano [19] Ch. 1 (kets, operators, measurement), Ch. 2 (time evolution, Stone); Cohen-Tannoudji et al. [20] Ch. III (the postulates, stated as postulates) | Postulates in their standard form; the difference between an observable and a projection; unitary evolution |
| M4. Quantum information | MSc / PhD year 1 | MIT 18.435J *Quantum Computation*; Caltech Ph219/CS219 (Preskill); Stanford's quantum-computing sequence; Cambridge Part III quantum information; Oxford MMathPhys quantum-information option | Nielsen & Chuang [18] Ch. 2 (all), §2.4 (density operator), §2.5 (Schmidt, purification), Ch. 8 (quantum operations), Ch. 11–12 (entropy, information); Preskill notes [53] Ch. 2 *Foundations I*, Ch. 3 *Foundations II* | POVMs, Kraus operators, partial trace, entanglement measures, quantum mutual information |
| M5. Quantum measurement theory | PhD | measurement-theory topics courses | Peres [21] Ch. 9 (measurement); Busch, Lahti & Mittelstaedt [26] Ch. 1, 4; Wiseman & Milburn [22] Ch. 1–3 (POVMs, weak measurement, back-action) | Lüders rule stated correctly; back-action; the gentle-measurement lemma [14] |
| M6. Open quantum systems and decoherence | PhD | open-quantum-systems / decoherence topics courses | Breuer & Petruccione [23] §3.1–3.3 (dynamical semigroups, GKLS); Schlosshauer [24] Ch. 2–3; Zurek [13] §II–III (einselection, pointer states); Joos & Zeh [12] | The only route by which AMF's *damped* dynamics can be embedded at all (§5.4) |
| M7. Regime-switching time series | MSc / PhD | econometrics of time series | Hamilton [45] Ch. 22 (Markov-switching, the filter in full); Rabiner [43] §II–III (the three problems, Baum–Welch); Cappé, Moulines & Rydén [47] Ch. 1–2, 6; Ang & Timmermann [46] | The comparator the note names; what "encode multi-regime dynamics" already means quantitatively |
| M8. Graphs and spectra | MSc | network science / algebraic graph theory | Newman [50] Ch. 6 (matrix representations), Ch. 7 (centrality, Katz); Godsil & Royle, *Algebraic Graph Theory* Ch. 8 | `DependencyGraph`: articulation points, Katz attenuation, the spectral-radius condition on `alpha` |
| M9. Quantum-like modelling outside physics | PhD / reading | — | Busemeyer & Bruza [30] Ch. 2–4 (Hilbert-space models of judgement, order effects); Khrennikov [31]; Wang et al. [32] | The one demonstrated non-classical *behavioural* effect: order dependence from non-commuting observables |
| M10. Quantum algorithms in finance | PhD / reading | — | Orús, Mugel & Lizaso [36]; Egger et al. [37]; Rebentrost, Gupt & Bromley [38] §II–III (amplitude estimation, quadratic speedup); Herman et al. [39]; Preskill [42] (NISQ limits) | Realistic resource estimates; separating *quantum computing for* finance from *quantum models of* finance |
| M11. Skeptical literature | PhD / reading | — | Aaronson [41] (the four fine-print caveats); Bouland et al. [40] (resource estimates for real speedups); Herman et al. [39] §"Outlook" | Why most claimed advantages evaporate under state-preparation and readout costs |
| M12. Numerical determinism | any | scientific-computing courses | Goldberg [51] §1–2; Higham [52] Ch. 2 | Why AMF's canonical iteration order is load-bearing (non-associativity of float addition) |

Note the split M10/M11 enforce: **quantum computing for finance** (a hardware/algorithms
question, live and partially answered) is a different subject from **quantum models of
markets** (an ontological question, and the one the source note is actually asking). The
note conflates them; the deliverable it proposes (Qiskit/Cirq) belongs to the first, while
its four research questions belong to the second.

## 4. Exact source material

### 4.1 Primary and seminal papers

- **[2] Born (1926)** — introduces the probabilistic interpretation of the wavefunction; the amplitude-squared rule the note writes as `|αᵢ|² = probability of state i`.
- **[3] Gleason (1957)** — proves the Born rule is the *unique* probability assignment on the projection lattice for `dim >= 3`; forbids inventing a different amplitude-to-probability map.
- **[4] Lüders (1950/51)** — gives the correct state-update rule after a projective measurement, the rule the note's collapse formula approximates incorrectly.
- **[5] Stone (1932)** — the bijection between self-adjoint generators and unitary groups; the theorem that makes `i d|Ψ>/dt = H|Ψ>` a well-posed definition rather than an ansatz.
- **[6] Schmidt (1907)** — the decomposition, predating quantum mechanics, that quantifies bipartite entanglement.
- **[7] Einstein, Podolsky & Rosen (1935)** and **[8] Bell (1964)** — together, the precise operational meaning of "non-locality": a testable inequality on correlations, not an influence.
- **[10] Lindblad (1976)** and **[11] Gorini, Kossakowski & Sudarshan (1976)** — the general form of a Markovian open-system generator; the only equation in which AMF's damping can live.
- **[12] Joos & Zeh (1985)** — the first quantitative environment-induced decoherence calculation.
- **[14] Winter (1999)** — contains the gentle-measurement lemma (Theorem 2.9).
- **[15] Holevo (1973)** — bounds the classical information extractable from a quantum ensemble; the reason "more states in superposition" does not mean "more information available".
- **[16] Baumgratz, Cramer & Plenio (2014)** — the resource theory of coherence and the `l1` coherence measure used in §5.5.
- **[17] Gu, Wiesner, Rieper & Vedral (2012)** — quantum models of stochastic processes can need strictly less memory than the optimal classical model. The correct citation for any claim that a quantum regime model is "simpler" than an HMM — and it is about memory, not accuracy.
- **[43] Rabiner (1989)** and **[44] Hamilton (1989)** — the two comparators the note names, in their canonical statements.
- **[48] Kyle (1985)** and **[49] Almgren & Chriss (2001)** — the classical, empirically anchored account of observation-induced market movement that the note's item 3 proposes to replace.
- **[32] Wang, Solloway, Shiffrin & Busemeyer (2014)** — the strongest empirical case anywhere that a Hilbert-space model captures something a classical one does not (question-order effects obeying a quantitative `QQ` equality).

### 4.2 Canonical textbooks with the sections that matter

- **[18] Nielsen & Chuang**, *Quantum Computation and Quantum Information*, 10th Anniversary Ed., Cambridge University Press, 2010. Ch. 2 in full; §2.2.6 (POVM), §2.4 (density operator, partial trace), §2.5 (Schmidt, purification); Ch. 8 (quantum noise, operator-sum representation); Ch. 11–12 (entropy, quantum information theory).
- **[19] Sakurai & Napolitano**, *Modern Quantum Mechanics*, 3rd ed., Cambridge University Press, 2020. Ch. 1 (kets, operators, measurement, compatible observables); Ch. 2 (time evolution).
- **[20] Cohen-Tannoudji, Diu & Laloë**, *Quantum Mechanics*, Vol. 1, Wiley-Interscience, 1977. Ch. III states the postulates as postulates, with the compatibility conditions spelled out; the complements to Ch. III on the density operator.
- **[21] Peres**, *Quantum Theory: Concepts and Methods*, Kluwer Academic, 1993. Ch. 7 (quantum tests and the lattice), Ch. 9 (measurement). The most careful book on what a measurement is.
- **[22] Wiseman & Milburn**, *Quantum Measurement and Control*, Cambridge University Press, 2010. Ch. 1 (POVMs and back-action), Ch. 2–3 (weak measurement, continuous monitoring).
- **[23] Breuer & Petruccione**, *The Theory of Open Quantum Systems*, Oxford University Press, 2002. §3.1–3.3 (dynamical semigroups, the GKLS generator, examples).
- **[24] Schlosshauer**, *Decoherence and the Quantum-to-Classical Transition*, Springer, 2007. Ch. 2–3. The clearest statement of what decoherence does and does not explain.
- **[25] Wilde**, *Quantum Information Theory*, 2nd ed., Cambridge University Press, 2017. Lemma 9.4.1 (gentle measurement), Ch. 11 (entropies), Ch. 4 (no-communication).
- **[26] Busch, Lahti & Mittelstaedt**, *The Quantum Theory of Measurement*, 2nd rev. ed., Springer, 1996. Ch. 1, 4.
- **[29] Horn & Johnson**, *Matrix Analysis*, 2nd ed., Cambridge University Press, 2013. §1.3 (simultaneous diagonalisation), Thm 4.1.5, Ch. 7 (positive semidefinite matrices).
- **[45] Hamilton**, *Time Series Analysis*, Princeton University Press, 1994. Ch. 22 in full.
- **[47] Cappé, Moulines & Rydén**, *Inference in Hidden Markov Models*, Springer, 2005. Ch. 1–2 (model class), Ch. 6 (filtering and smoothing recursions).
- **[50] Newman**, *Networks*, 2nd ed., Oxford University Press, 2018. Ch. 6, Ch. 7.

### 4.3 Surveys and reviews

- **[13] Zurek (2003)**, *Reviews of Modern Physics* 75, 715–775 — the standard decoherence review.
- **[36] Orús, Mugel & Lizaso (2019)**, *Reviews in Physics* 4, 100028 — first broad survey of quantum computing applied to finance; annealing, optimisation, machine learning.
- **[37] Egger et al. (2020)**, *IEEE Transactions on Quantum Engineering* 1, 3101724 — the practitioner-oriented state of the art with hardware constraints made explicit.
- **[39] Herman et al. (2023)**, *Nature Reviews Physics* 5, 450–465 — the most recent broad review; notable because it sets out the *classical* techniques first and is candid about limits.
- **[46] Ang & Timmermann (2012)**, *Annual Review of Financial Economics* 4, 313–337 — the regime-switching literature the note's item 1 must beat.

### 4.4 Open courseware and lecture notes

- **[53] Preskill**, *Ph219/CS219 Quantum Computation*, Caltech. Chapter 2 (*Foundations I: States and Ensembles* — axioms, density operator, Schmidt decomposition) and Chapter 3 (*Foundations II: Measurement and Evolution* — POVMs, superoperators, master equations, decoherence) are the single best free treatment of everything §2 needs. `http://theory.caltech.edu/~preskill/ph219/`
- **[54] MIT OpenCourseWare, 18.435J *Quantum Computation*** — full lecture notes and problem sets.
- **[55] MIT OpenCourseWare, 8.04 / 8.05 / 8.06 *Quantum Physics I / II / III*** — the standard three-semester ladder; 8.05 is where the operator formalism and measurement are done properly.

### 4.5 Domain application to finance, including the skeptical literature

- **[33] Baaquie (2004)**, *Quantum Finance: Path Integrals and Hamiltonians for Options and Interest Rates*, Cambridge University Press. Uses the *mathematical machinery* of quantum field theory (path integrals, Hamiltonians) as a computational technique for classical stochastic models. It does not claim markets are quantum systems, and is often miscited as if it did.
- **[34] Segal & Segal (1998)**, *PNAS* 95(7), 4072–4075 — embeds Black–Scholes in a quantum context and identifies a non-commutativity between two natural observables. Honest and narrow.
- **[35] Piotrowski & Sładkowski (2002)**, *Physica A* 312, 208–216 — quantum game-theoretic market models. Interesting formal exercise; no empirical validation.
- **[30] Busemeyer & Bruza (2012)** and **[31] Khrennikov (2010)** — the quantum-cognition programme, which is where the *only* replicated non-classical effects in social science live. Note that these are models of **judgement**, not of markets.
- **[38] Rebentrost, Gupt & Bromley (2018)**, *Physical Review A* 98, 022321 — quadratic speedup for Monte-Carlo valuation via amplitude estimation. A genuine algorithmic result; note that it speeds up a *classical* stochastic model and says nothing about market ontology.
- **Skeptical / corrective:**
  - **[41] Aaronson (2015)**, *Nature Physics* 11, 291–293 — the four caveats (state preparation, condition number, output readout, and the fact that quantum outputs are quantum states) that dissolve most claimed exponential advantages. Required reading before any Q-series proposal.
  - **[40] Bouland, van Dam, Joorati, Kerenidis & Prakash (2020)**, arXiv:2011.06492 — estimates the actual quantum resources needed for a practical speedup in finance; the numbers are large.
  - **[42] Preskill (2018)**, *Quantum* 2, 79 — what near-term hardware can and cannot do.
  - **[39] Herman et al. (2023)** — see §4.3; its outlook section is candid about the gap between asymptotic claims and deployable advantage.

## 5. Derivation for the AMF setting

We now do the mathematics. Fix `H_7 = C^7` with orthonormal basis
`B = { |skeleton>, |circulatory>, |nervous>, |musculature>, |organs>, |immune>,
|metabolism> }`, indexed in `SystemKind` declaration order. Numerical values below are
those of `examples/sample_market.json` and are illustrative only.

### 5.1 AMF's diagnostic index is already a Born-rule expectation

Let `c_k` be system `k`'s criticality and `s_k` its blended weakness score. Define

```
rho_c = sum_k w_k |k><k| ,    w_k = c_k / sum_j c_j        (a diagonal density operator)
S     = sum_k s_k |k><k|                                    (a diagonal observable)
```

`rho_c >= 0` and `Tr(rho_c) = 1`, so `rho_c` is a legitimate state by Definition 2.1; `S`
is self-adjoint with spectrum in `[0, 1]`.

**Proposition 5.1.** `DiagnosticReport`'s overall index equals `Tr(rho_c S)` exactly.

*Proof.* `Tr(rho_c S) = sum_k w_k s_k = (sum_k c_k s_k) / (sum_j c_j)`, which is the
criticality-weighted mean of the per-system scores — the definition of the index. □

For the sample market, `sum_k c_k = 0.90 + 0.85 + 0.70 + 0.60 + 0.65 + 0.75 + 0.60 = 5.05`,
so `w = (0.1782, 0.1683, 0.1386, 0.1188, 0.1287, 0.1485, 0.1188)` to four places.

This is the module's first substantive finding, and it is deflationary: **AMF is already
inside the formalism, at the point where the formalism is empty.** Everything the
quantum apparatus can contribute lies off the diagonal, and Proposition 5.1 uses none of it.

### 5.2 Commutativity, determinism, and measurement order

**Definition 5.2.** Call a proposed AMF diagnostic *basis-diagonal* if its operator is
diagonal in `B`.

**Theorem 5.3 (Determinism is commutativity).** Let `A_1, ..., A_m` be the operators of
AMF's diagnostic components (fragility, concentration, feedback amplification, the
single-point-of-failure indicator). Each is basis-diagonal, hence `[A_r, A_s] = 0` for all
`r, s`, and each commutes with every projection `P_k = |k><k|`. Consequently, for any
sequence of Lüders updates by these measurements, the joint outcome distribution is
invariant under permutation of the sequence. Conversely, if a proposed diagnostic `A`
satisfies `[A, P_k] != 0` for some `k`, then there exist states for which measuring `A`
then `P_k` gives a different joint distribution from measuring `P_k` then `A`.

*Proof.* Diagonal operators in a common basis commute (Theorem 2.6). For commuting
projective measurements, `P_a P_b rho P_b P_a = P_b P_a rho P_a P_b` since the projections
commute, and the outcome probabilities `Tr(P_b P_a rho P_a P_b)` are therefore symmetric in
`a, b`. For the converse, take `rho = |k><k|`: the `P_k`-first sequence returns `k` with
probability 1 and then `A`'s distribution in the state `|k>`, whereas the `A`-first
sequence disturbs `|k>` whenever `[A, P_k] != 0`, so the subsequent `P_k` outcome is no
longer certain. □

**Corollary 5.4 (Governance).** `tests/unit/test_properties.py`'s guarantee that a market
and any permutation of it diagnose identically is, in Hilbert-space language, exactly the
assertion that AMF's diagnostic observables form a commuting family. Introducing a
genuinely quantum diagnostic — one with `[A, P_k] != 0` — is therefore not an extension of
AMF; it is a *repeal* of the property test. Any Q-series proposal that wants non-classical
behaviour must say, in its first paragraph, which determinism guarantee it is giving up.

This is the sharpest statement in the module and the one reviewers should attack first.

### 5.3 Where phase could enter: multi-kind dependency edges

`DependencyGraph` keys edges by `(source, target, kind)` with
`kind` in `{structural, informational, capital, regulatory}`, and every structural query
aggregates across kinds as `min(1, sum of weights)`. Write the aggregated coupling as
`g_ij`. Define a candidate structural Hamiltonian on `H_7`:

```
H_struct = sum_k c_k |k><k|
         + sum_{i<j} g_ij ( exp(i theta_ij) |i><j| + exp(-i theta_ij) |j><i| )
```

`H_struct` is self-adjoint for any real `theta_ij`, so Stone's theorem (2.16) applies and
`U(t) = exp(-i t H_struct)` is a legitimate unitary group.

**Proposition 5.5 (The phase is exactly what AMF forbids).** Let a single `(i, j)` coupling
be split across kinds with weights `w_1, ..., w_m` and per-kind phases
`theta_1, ..., theta_m`. AMF's aggregation yields `g_ij = min(1, sum_r w_r)`; the coherent
aggregation yields `g_ij^q = | sum_r w_r exp(i theta_r) |`. These agree for all splittings
if and only if all `theta_r` are equal modulo `2 pi`.

*Proof.* `| sum_r w_r exp(i theta_r) | <= sum_r w_r` with equality iff all the summands are
positive multiples of a common unit complex number, i.e. all phases coincide. Below the
saturation cap the AMF value is `sum_r w_r`; the two therefore agree for every splitting
exactly when equality always holds. □

*Worked instance.* Split `circulatory -> skeleton` (sample weight `0.8`) into
`structural = 0.5` and `capital = 0.3`. AMF gives `0.8`. With
`theta_structural = 0, theta_capital = pi/2`, coherent aggregation gives
`|0.5 + 0.3 i| = 0.5831`; with `theta_capital = pi` it gives `0.2`. The repository's
documented invariant — "splitting one coupling across kinds never changes a score" — is
therefore *precisely* the statement that all dependency kinds carry phase zero. A phase
model is not a refinement of AMF's edge-kind semantics; it contradicts them.

### 5.4 Embedding AMF's stress dynamics: what works and what cannot

AMF's step map is

```
x_{t+1}[j] = clip( damping * ( x_t[j]*retention + sum_i x_t[i]*W[i][j]*transmission*(1 - a_j) ), 0, 1 )
```

with `a_j = 0.5*redundancy + 0.3*integrity + 0.2*(1 - load)`.

**Proposition 5.6 (Three obstructions).**
1. *Not unitary.* With `damping = 0.85 < 1` the map contracts the `l1` mass of `x`, so no
   `U(t) = exp(-i t H)` reproduces it (Theorem 2.16 gives norm preservation).
2. *Not trace-preserving.* A single Kraus operator `K` with `K* K <= I` but `!= I`
   represents a *trace-decreasing* map, not a channel; Theorem 2.17 does not apply.
3. *Not linear.* `clip(., 0, 1)` is nonlinear, and every completely positive map is linear.
   No operator-sum representation of any kind exists once the clip is active.

*Repair for (1) and (2).* Enlarge to `H_8 = H_7 (+) C|absorbed>`, an eighth basis vector
acting as a sink. Let the lost weight `(1 - damping)` per step flow into `|absorbed>`. Then
the map is trace-preserving on `H_8`, `Tr(rho) = 1` is restored, and — pleasingly —

```
absorbed_fraction  =  <absorbed| rho_inf |absorbed>
```

so AMF's existing *absorbed* metric is exactly the steady-state population of the sink
mode. The eighth mode is the honest name for the stress AMF's damping term discards.

*No repair for (3).* The clip is genuinely outside the formalism. A faithful embedding
exists only in the sub-saturation regime where no component reaches `1.0`. Any
implementation must therefore either (a) restrict to sub-saturation trajectories and say so
in its docstring, or (b) abandon exact correspondence with `ShockSimulator`. Silently doing
neither is the failure mode to guard against.

### 5.5 Coherence, absorptive capacity, and a decoherence timescale

Adopt the `l1` measure of coherence of [16]: `C_l1(rho) = sum_{i != j} |rho_ij|`. Model the
environment as pure dephasing (Definition 2.18) with rates proportional to absorptive
capacity, `gamma_k = gamma_0 * a_k` for a single free scale `gamma_0 > 0`. Then

```
|rho_ij(t)| = |rho_ij(0)| * exp( - gamma_0 (a_i + a_j) t / 2 )
tau_ij      = 2 / ( gamma_0 (a_i + a_j) )
```

For the sample market, `a = (skeleton 0.54, circulatory 0.54, nervous 0.67,
musculature 0.80, organs 0.70, immune 0.75, metabolism 0.70)`. Hence

```
tau(musculature, immune)     = 2 / (gamma_0 * 1.55) = 1.290 / gamma_0     (fastest)
tau(skeleton, circulatory)   = 2 / (gamma_0 * 1.08) = 1.852 / gamma_0     (slowest)
ratio                        = 1.435
```

**Proposition 5.7 (AMF has no coherence to lose).** For every market AMF can currently
construct, `C_l1(rho) = 0` at every timestep.

*Proof.* The stress vector is real and non-negative and enters only through its components;
the induced state is `rho_t = sum_k p_t[k] |k><k|` with `p_t` the normalised stress. All
off-diagonal entries vanish identically, so `C_l1 = 0`; and by Definition 2.18 dephasing
preserves the diagonal, so no dynamics AMF runs can create coherence. □

**Corollary 5.8.** Every bipartition of AMF's seven systems has entanglement entropy zero
(Definition 2.12), and by Proposition 2.14 quantum mutual information between any two
subsets equals the classical Shannon mutual information of the corresponding stress
distribution. The note's item 2 has no purchase on AMF's data, and would not acquire any
by adding more markets.

This is the module's central negative result and the honest answer to the source note: the
apparatus is not wrong, it is *idle*. It becomes non-idle only if some future AMF quantity
is (i) off-diagonal in the state and (ii) reported through a non-diagonal observable — and
(ii) costs Corollary 5.4.

### 5.6 Regimes: the HMM comparison, precisely

The note asks whether the superposition encoding beats an HMM. Set up both on the same
footing over a hidden regime set `S` and an observation alphabet `X`:

```
classical:  p(x_{1:T}) = 1^T * B_{x_T} A ... B_{x_1} A * pi          (Def. 2.22)
quantum:    p(x_{1:T}) = Tr( K_{x_T} ... K_{x_1} rho K_{x_1}* ... K_{x_T}* )   (Def. 2.24)
```

**Proposition 5.9 (What the advantage is and is not).** Under Theorem 2.25, for almost
every stationary process the minimal quantum generative model has strictly lower entropy
than the minimal classical one. This is a statement about the *memory* of the generator.
Both models, when they model the same process, produce identical predictive conditional
distributions `p(x_{t+1} | x_{1:t})`, so no accuracy comparison — including the note's
proposed "Quantum vs. HMM predictions on historical crises" — can distinguish them on
predictive grounds. A measured accuracy difference between a fitted HQMM and a fitted HMM
is evidence about estimation, regularisation, and the number of free parameters, not about
quantum structure.

*Consequence for the deliverable.* The note's third bullet ("Comparison: Quantum vs. HMM
predictions on historical crises") is, as stated, not a well-posed experiment. It becomes
well posed if reformulated as: *at matched predictive log-likelihood on held-out data,
does the quantum model require fewer memory dimensions than the minimal classical one?*
That is Theorem 2.25's actual claim, it is falsifiable, and it needs no market data at
all — it can be run on synthetic processes with known `epsilon`-machines.

### 5.7 Observation as back-action, without market-data vocabulary

The note's item 3 (order entry, fills, dark pools) is squarely outside AMF's non-trading
boundary and must be reformulated or dropped. The reformulation that survives is:

**Definition 5.10 (Structural observation channel).** A diagnostic applied to a market is
an instrument `{M_x}` on `H_8` (Definition 2.8) whose action may alter the market's
structural state — for example, publishing a stress-test result raises the `load` on
`immune` and lowers the `redundancy` credited to `circulatory`. This is representable in
AMF today as an `Intervention`-shaped object with an `at_step`, not as a collapse.

**Proposition 5.11 (Gentle diagnosis).** Let `E_x` be the POVM element corresponding to
"this market is diagnosed at severity band `x`". If the diagnosis was already nearly
certain, `Tr(E_x rho) >= 1 - eps`, then by Theorem 2.9 the disturbance obeys
`|| rho' - rho ||_1 <= 2 sqrt(eps)`. Equivalently: a diagnostic that tells you nothing you
did not already know cannot move the market much; a diagnostic that is genuinely
informative necessarily can.

This is a real theorem with a real AMF reading, it uses only structural vocabulary, and it
is the one item from the note's question 3 worth keeping. Note also that it is *not*
distinctively quantum — classical measurement disturbance obeys an analogous bound — which
is itself informative: back-action is a general feature of instruments, and Kyle's
lambda [48] and the Almgren–Chriss framework [49] already model the market case classically
and with empirical support. Quantum framing adds content only if the disturbance depends on
the *basis* of the diagnostic in a non-commuting way (Theorem 5.3), which no proposal here
has motivated.

### 5.8 The tensor-product construction and why it is empty for AMF

If one insists on entanglement, the seven systems must become tensor factors rather than
basis labels: `H = (C^2)^{(x) 7}`, dimension `128`, with `|0>_k` = unstressed and
`|1>_k` = stressed. A natural Hamiltonian is

```
H = sum_k h_k Z_k  +  sum_{i<j} J_ij Z_i Z_j  +  sum_{i<j} K_ij ( X_i X_j + Y_i Y_j )
```

with `h_k` from criticality and `J_ij` from the aggregated coupling `g_ij`.

**Proposition 5.12.** If `K_ij = 0` for all `i, j`, then `H` is diagonal in the
computational basis, every eigenstate is a product state, the evolution maps the classical
distribution over bit-strings by a classical stochastic matrix, and every bipartite
entanglement entropy is identically zero. Setting `K = 0` recovers AMF's `CouplingMatrix`
dynamics exactly (up to the obstructions of Proposition 5.6).

*Proof.* `Z_k` and `Z_i Z_j` are simultaneously diagonal; a diagonal Hamiltonian has a
product eigenbasis, and the induced dynamics on diagonal states are a stochastic map.
Diagonal states over a product basis are separable, so all entanglement measures vanish. □

**Corollary 5.13 (Unidentifiability).** `K` is the entire quantum content of the model, and
no observation AMF makes — every AMF output is a function of the diagonal — constrains any
`K_ij`. A fitted `K` would be pure prior. Reporting it as a finding would violate the
repository's illustrative-not-validated rule twice over: it would be unvalidated *and*
unidentifiable.

## 6. Repository governance and boundary analysis

| Proposed artefact (from the note) | Conflicts with which hard rule | Compliant reformulation |
|---|---|---|
| `src/amf/quantum/superposition_model.py` — "Implementation using Qiskit/Cirq" | **Rule 3, zero runtime dependencies.** Qiskit and Cirq are large third-party packages with transitive dependencies; adding either ends `amf`'s stdlib-only guarantee and its `pyproject.toml` contract. | Move to an out-of-tree research sidecar, e.g. a separate repository `amf-research-quantum` that *depends on* `amf` and never the reverse. If an in-tree home is required, it must be a pure-stdlib module — a `7x7` or `8x8` complex matrix layer is a few hundred lines of `complex` arithmetic and needs no framework. |
| the same file, as a name | **Rule 1 is satisfied** (`superposition`, `quantum`, `model` contain none of the `FORBIDDEN` substrings), but the *contents* the note sketches are not: "market price", "trader enters order", "filled at different price". | Rename to `coherence_model.py`; expose `CoherenceModel`, `StructuralHamiltonian`, `DephasingChannel`, `coherence_ell1`, `decoherence_horizon`, `commutation_defect`. Check each against the `FORBIDDEN` list before export, and note that `order` is forbidden as a *substring*, so `ordered_basis` and `reorder` both fail — use `canonical_sequence` / `declaration_index`. |
| `src/amf/ml/`, `src/amf/backtest/` (elsewhere in the source note) | **Rule 1, non-trading boundary.** `backtest` is on the `FORBIDDEN` list verbatim; `tests/unit/test_non_trading_boundary.py` fails on the public name and on any member or dataclass field containing it. | There is no compliant rename for a backtest, because the object itself is out of scope. The compliant analogue is `stress_test` over structural configurations, which already exists. Delete rather than rename. |
| "Comparison: Quantum vs. HMM predictions on historical crises" | **Rule 1** (historical market data is price/returns data) and **Rule 2** (a comparison on historical crises presented as a result is a validation claim). Also ill-posed on its own terms (Proposition 5.9). | Reformulate as a memory-complexity comparison on *synthetic* processes with known minimal classical models, per Proposition 5.9. No market data, no validation claim, and it actually tests the cited theorem. |
| `docs/research/quantum_market_superposition.md` | No conflict. | Keep; this module is its content. Cross-link from `docs/QUANTUM_NEURAL_RESEARCH.md`. |
| "Market price as quantum wavefunction: P(t) = Σ αᵢ\|state_i⟩" | **Rule 1.** `price` is a `FORBIDDEN` substring. | The AMF-native object is the *structural stress state*, `rho_t` on `H_8` (§5.4). Every quantity in §5 is dimensionless and structural. |
| "Reduce market impact by gentle measurement (dark pools, algorithmic execution)" | **Rule 1** (execution venues and market impact are trading concepts); **Rule 2** if presented as actionable. | Proposition 5.11: a `DiagnosticInstrument` whose outcome is nearly certain perturbs the structural state by at most `2 sqrt(eps)` in trace norm. Structural, theorem-backed, non-actionable. |

**Determinism implications.** Corollary 5.4 is the binding constraint: non-commuting diagnostics are order-dependent by construction, and order-dependence is exactly what `test_properties.py` forbids. Additionally, matrix exponentials and eigendecompositions are iterative; a pure-stdlib implementation must fix its own iteration count and tolerance and validate them through `InvalidConfigError`, exactly as `DependencyGraph.centrality` does for `alpha`, `iterations`, and `tolerance`. Complex arithmetic in Python's `complex` type is IEEE-754 double under the hood, so §CLAUDE.md's warning about non-associative float addition applies unchanged: sums over basis states must iterate in `SystemKind` declaration order [51], [52].

**Dependency-direction implications.** Any in-tree module would sit at the `diagnostics`/`simulation` layer or above (it consumes `DependencyGraph` and `AnatomicalSystem`), must not be imported by `graph`, `market`, or `systems`, and must be re-exported from `amf/__init__.py` with `__all__` kept sorted.

**Coverage implications.** The 100% statement-and-branch gate applies. A complex-matrix layer has many branches (degenerate eigenvalues, zero-trace states, saturation, the `gamma_0 = 0` edge). Budget the tests before the code; the fix for a failing gate is a test, never a lower threshold.

**Validation-claim implications.** Rule 2 forbids claiming predictive power. Sections 5.5 and 5.6 are written so that every number is either an identity (Prop. 5.1), a counterexample (Prop. 5.5), or a consequence of a cited theorem (Props. 5.7, 5.9, 5.12). No sentence in this module asserts that any construction here describes a real market.

## 7. Falsifiable propositions and open questions

Each is stated so that a specific finding would refute it. **P1–P4 restate the note's four "Key Research Questions" in substance**, made precise; **P5–P10 extend them.**

- **P1 (note's Q1, superposition as uncertainty model).** *For any AMF market and any quantity AMF currently reports, the quantum model with `C_l1(rho) > 0` and the classical model with the same diagonal produce identical output.* **Refuted by:** exhibiting one AMF-reported quantity whose value differs between `rho_pure` and `rho_mix` of Definition 2.2. Given Proposition 5.1 this requires a non-diagonal observable, so a refutation is simultaneously a repeal of Corollary 5.4.
- **P2 (note's Q2, entanglement as cross-market correlation).** *Every AMF market state has zero entanglement across every bipartition, and quantum mutual information between any two subsets of systems equals the classical mutual information.* **Refuted by:** a construction procedure that maps AMF's JSON schema to a non-separable state without introducing free parameters unconstrained by the schema. Corollary 5.13 says any such procedure must smuggle in `K_ij`.
- **P3 (note's Q3, measurement and impact).** *Structural back-action in AMF is fully described by a classical instrument; no AMF diagnostic exhibits order effects.* **Refuted by:** two AMF diagnostics whose composition is order-dependent — which is currently impossible by Theorem 5.3, so the refutation must come with an API change.
- **P4 (note's Q4, decoherence and efficiency).** *Under the dephasing model of §5.5, decoherence leaves the stress distribution and its Shannon entropy exactly invariant.* **Refuted by:** a decoherence model whose diagonal is not preserved — i.e. one that is not pure dephasing, in which case it is an amplitude-damping process and should be named as such rather than as decoherence.
- **P5 (policy direction, contra the note).** *Under `gamma_k = gamma_0 a_k`, an `Intervention` that raises a system's absorptive capacity strictly **accelerates** decoherence involving that system.* This directly contradicts the note's suggestion that policy could "delay decoherence (maintain uncertainty longer)". **Refuted by:** a motivated alternative rate law in which `gamma_k` decreases in `a_k`; the burden is to say what mechanism makes a more absorptive system hold coherence longer.
- **P6 (phase and round-trip invariance).** *Assigning distinct phases to `DependencyKind`s breaks the documented `to_dict`/`from_dict` invariance that splitting a coupling across kinds never changes a score.* **Refuted by:** a phase assignment for which Proposition 5.5's equality holds for all splittings — which forces all phases equal, i.e. no phase at all.
- **P7 (embedding fidelity).** *No completely positive map reproduces `ShockSimulator`'s step whenever the clip is active.* **Refuted by:** an operator-sum representation of a clipping map, which cannot exist since CP maps are linear (Proposition 5.6(3)).
- **P8 (memory, not accuracy).** *At matched held-out predictive log-likelihood on a synthetic process with a known minimal `epsilon`-machine, an HQMM requires no more memory dimensions than the minimal HMM, and strictly fewer for a positive-measure set of processes.* This is Theorem 2.25 restated as an experiment. **Refuted by:** a process where the fitted HQMM needs strictly more.
- **P9 (dependency cost).** *A stdlib-only complex-matrix layer sufficient for §5.1–5.5 fits in under 400 statements at 100% branch coverage.* **Refuted by:** an implementation attempt that cannot. This determines whether the sidecar is needed at all.
- **P10 (identifiability, open).** *Is there any structural observable — not a market-data observable — whose measurement in AMF would be order-dependent for a principled reason?* Open. The candidate worth examining is a diagnostic over *overlapping* system groupings (e.g. "liquidity-and-execution" as one mode and "execution-and-participants" as another), since overlapping coarse-grainings do not commute in general. If no such candidate survives scrutiny, Q1 should be closed as formally correct and operationally empty.

**Further open questions.** (a) Does the eighth "absorbed" mode of §5.4 have an interpretation in the framework document's own vocabulary, or is it purely a bookkeeping device? (b) Is `C_l1` the right coherence measure here, or does the relative entropy of coherence [16] behave better under AMF's normalisation? (c) Does the Katz attenuation `alpha` have a spectral-radius analogue in `H_struct` that would let `centrality`'s divergence warning be stated as an operator-norm bound?

## 8. Deliverables

The note's deliverable list, reproduced exactly, with status and compliance.

| Deliverable (verbatim from the note) | Status | Compliance |
|---|---|---|
| `docs/research/quantum_market_superposition.md` — Theoretical framework | **Superseded by this file.** Content delivered as `docs/discussions/Q1-quantum-market-superposition.md`. | Compliant. Documentation only; no code, no dependencies, no validation claim. |
| `src/amf/quantum/superposition_model.py` — Implementation using Qiskit/Cirq | **Blocked as specified.** | **Non-compliant with Rule 3** (zero runtime dependencies). Reformulate as (a) an out-of-tree sidecar `amf-research-quantum` depending on `amf`, or (b) a stdlib-only `src/amf/coherence.py` exposing `StructuralHamiltonian`, `DephasingChannel`, `coherence_ell1`, `decoherence_horizon`. Option (b) is gated on P9 and on accepting Corollary 5.4's cost. Names must be checked against the `FORBIDDEN` substring list, `order` included. |
| Comparison: Quantum vs. HMM predictions on historical crises | **Blocked as specified.** | **Non-compliant with Rules 1 and 2**, and ill-posed (Proposition 5.9). Reformulate as the synthetic memory-complexity experiment of P8: no market data, no predictive claim, and it tests the theorem actually cited. |

Two deliverables are added by this module, both compliant:

| Added deliverable | Rationale |
|---|---|
| A one-page "boundary note" appended to `docs/QUANTUM_NEURAL_RESEARCH.md` recording that `src/amf/quantum/`, `src/amf/ml/`, and `src/amf/backtest/` are blocked, and why. | Prevents the same proposal being re-raised; makes the constraint discoverable at the point of temptation. |
| A `CHANGELOG.md` entry under `## [Unreleased]` → *Added*, recording this discussion module. | Repository convention for user-visible changes. |

## 9. Research leadership and prerequisites

> **Research Leaders Needed**: Quantum physicist, financial mathematician

Reproduced verbatim from the note. Two roles are not enough for the work as scoped; the skills matrix below is what the module actually requires.

| Role | Must be able to | Must have read | Failure mode if absent |
|---|---|---|---|
| **Quantum information theorist** (not "quantum physicist" — the relevant subfield is information, not spectroscopy) | State and apply Gleason, Lüders, GKLS, Schmidt, gentle measurement; distinguish coherence from correlation; compute a partial trace by hand | [18] Ch. 2, 8, 11–12; [53] Ch. 2–3; [23] §3.1–3.3; [13] | The module drifts into "superposition means uncertainty", which Definition 2.2 refutes |
| **Financial mathematician / time-series econometrician** | Estimate a Markov-switching model, state its identification conditions, compute a Hamilton filter | [45] Ch. 22; [44]; [46]; [47] Ch. 6 | The HMM comparison is run as an accuracy horse-race, which Proposition 5.9 shows is uninformative |
| **Foundations-of-QM specialist** | Say precisely what decoherence does and does not explain; state Bell's theorem's hypotheses including free choice | [24] Ch. 2–3; [21] Ch. 7, 9; [8], [7] | "Spooky action at a distance" survives into published text (Theorem 2.15) |
| **Numerical analyst / research software engineer** | Write deterministic complex linear algebra in pure stdlib; reason about float non-associativity; achieve 100% branch coverage | [52] Ch. 2; [51]; the repository's `CLAUDE.md` determinism section | Non-deterministic output; a `NaN` escaping into `Severity.from_score`, which saturates to `critical` |
| **Boundary reviewer** (may be one of the above) | Recite the `FORBIDDEN` substring list from memory; recognise `order` inside `reorder` | `tests/unit/test_non_trading_boundary.py`; `CLAUDE.md` hard rules | A `FORBIDDEN` name reaches a pull request and the guard fails in CI |
| **Skeptic-in-residence** | Kill proposals that cannot be falsified | [41]; [40]; [39] outlook | The Q-series accumulates formalism with no discriminating experiment |

**Prerequisite ladder, undergraduate to frontier.**

1. *Undergraduate year 2.* Linear algebra over `C`: inner products, adjoints, unitaries, the spectral theorem for self-adjoint operators, positive semidefiniteness ([28] Ch. 6–7). Probability to the level of conditional expectation.
2. *Undergraduate year 3.* Quantum mechanics I–II (MIT 8.04, 8.05). Stop at the point where the postulates are stated in operator form ([19] Ch. 1; [20] Ch. III); the hydrogen atom is irrelevant here.
3. *Undergraduate year 4 / MSc.* Quantum information: density operators, partial trace, POVMs, Kraus operators, Schmidt decomposition, von Neumann entropy ([18] Ch. 2, 11). Concurrently: time-series econometrics through the Hamilton filter ([45] Ch. 22).
4. *PhD year 1.* Open quantum systems and decoherence ([23] §3; [24]; [13]). This is the level at which §5.4–5.5 can be checked rather than believed.
5. *PhD year 2.* Measurement theory proper ([21] Ch. 9; [26]; [22] Ch. 1–3), and the quantum-cognition literature as the only place where non-classical models have met data in a social science ([30]; [32]).
6. *Frontier.* Quantum stochastic-process complexity ([17] and its successors); realistic resource accounting for quantum algorithms in finance ([40]; [39]); and the standing question P10 above, which is where this module's remaining value lies.

**Recommended entry point for a reader with none of the above:** read §2.2's correction to the note's collapse formula, then Definition 2.2, then Proposition 5.1. Those three items convey the module's thesis without any prerequisite beyond matrix multiplication.

## References

[1] von Neumann, J. *Mathematische Grundlagen der Quantenmechanik*. Springer, Berlin, 1932. English translation by R. T. Beyer, *Mathematical Foundations of Quantum Mechanics*, Princeton University Press, 1955.

[2] Born, M. "Zur Quantenmechanik der Stoßvorgänge." *Zeitschrift für Physik* 37(12), 863–867 (1926).

[3] Gleason, A. M. "Measures on the Closed Subspaces of a Hilbert Space." *Journal of Mathematics and Mechanics* 6, 885–893 (1957).

[4] Lüders, G. "Über die Zustandsänderung durch den Meßprozeß." *Annalen der Physik* 443(8), 322–328 (1950/51). English translation by K. A. Kirkpatrick, "Concerning the state-change due to the measurement process", *Annalen der Physik* 15(9), 663–670 (2006).

[5] Stone, M. H. "On One-Parameter Unitary Groups in Hilbert Space." *Annals of Mathematics* 33, 643–648 (1932).

[6] Schmidt, E. "Zur Theorie der linearen und nichtlinearen Integralgleichungen. I. Teil."
*Mathematische Annalen* 63, 433–476 (1907).

[7] Einstein, A., Podolsky, B. & Rosen, N. "Can Quantum-Mechanical Description of Physical Reality Be Considered Complete?" *Physical Review* 47(10), 777–780 (1935).

[8] Bell, J. S. "On the Einstein Podolsky Rosen Paradox." *Physics Physique Fizika* 1(3), 195–200 (1964).

[9] Kolmogorov, A. N. *Grundbegriffe der Wahrscheinlichkeitsrechnung*. Springer, Berlin, 1933. English translation, *Foundations of the Theory of Probability*, 2nd English ed., Chelsea, New York, 1956.

[10] Lindblad, G. "On the generators of quantum dynamical semigroups." *Communications in Mathematical Physics* 48(2), 119–130 (1976).

[11] Gorini, V., Kossakowski, A. & Sudarshan, E. C. G. "Completely positive dynamical semigroups of N-level systems." *Journal of Mathematical Physics* 17, 821–825 (1976).

[12] Joos, E. & Zeh, H. D. "The emergence of classical properties through interaction with the environment." *Zeitschrift für Physik B — Condensed Matter* 59, 223–243 (1985).

[13] Zurek, W. H. "Decoherence, einselection, and the quantum origins of the classical."
*Reviews of Modern Physics* 75, 715–775 (2003). DOI 10.1103/RevModPhys.75.715.

[14] Winter, A. "Coding theorem and strong converse for quantum channels." *IEEE Transactions on Information Theory* 45(7), 2481–2485 (1999).

[15] Holevo, A. S. "Bounds for the quantity of information transmitted by a quantum communication channel." *Problems of Information Transmission* 9(3), 177–183 (1973).

[16] Baumgratz, T., Cramer, M. & Plenio, M. B. "Quantifying Coherence." *Physical Review Letters* 113, 140401 (2014). DOI 10.1103/PhysRevLett.113.140401.

[17] Gu, M., Wiesner, K., Rieper, E. & Vedral, V. "Quantum mechanics can reduce the complexity of classical models." *Nature Communications* 3, 762 (2012).

[18] Nielsen, M. A. & Chuang, I. L. *Quantum Computation and Quantum Information*, 10th Anniversary Edition. Cambridge University Press, 2010.

[19] Sakurai, J. J. & Napolitano, J. *Modern Quantum Mechanics*, 3rd ed. Cambridge University Press, 2020.

[20] Cohen-Tannoudji, C., Diu, B. & Laloë, F. *Quantum Mechanics*, Vol. 1. Wiley-Interscience, 1977.

[21] Peres, A. *Quantum Theory: Concepts and Methods*. Kluwer Academic, 1993.

[22] Wiseman, H. M. & Milburn, G. J. *Quantum Measurement and Control*. Cambridge University Press, 2010.

[23] Breuer, H.-P. & Petruccione, F. *The Theory of Open Quantum Systems*. Oxford University Press, 2002.

[24] Schlosshauer, M. *Decoherence and the Quantum-to-Classical Transition*. Springer, 2007.

[25] Wilde, M. M. *Quantum Information Theory*, 2nd ed. Cambridge University Press, 2017.

[26] Busch, P., Lahti, P. J. & Mittelstaedt, P. *The Quantum Theory of Measurement*, 2nd rev. ed. Springer, 1996.

[27] Griffiths, D. J. & Schroeter, D. F. *Introduction to Quantum Mechanics*, 3rd ed. Cambridge University Press, 2018.

[28] Axler, S. *Linear Algebra Done Right*, 4th ed. Springer, 2024 (open access).

[29] Horn, R. A. & Johnson, C. R. *Matrix Analysis*, 2nd ed. Cambridge University Press, 2013.

[30] Busemeyer, J. R. & Bruza, P. D. *Quantum Models of Cognition and Decision*. Cambridge University Press, 2012.

[31] Khrennikov, A. Y. *Ubiquitous Quantum Structure: From Psychology to Finance*. Springer, 2010.

[32] Wang, Z., Solloway, T., Shiffrin, R. M. & Busemeyer, J. R. "Context effects produced by question orders reveal quantum nature of human judgments." *Proceedings of the National Academy of Sciences* 111(26), 9431–9436 (2014). DOI 10.1073/pnas.1407756111.

[33] Baaquie, B. E. *Quantum Finance: Path Integrals and Hamiltonians for Options and Interest Rates*. Cambridge University Press, 2004.

[34] Segal, W. & Segal, I. E. "The Black-Scholes pricing formula in the quantum context."
*Proceedings of the National Academy of Sciences* 95(7), 4072–4075 (1998).

[35] Piotrowski, E. W. & Sładkowski, J. "Quantum market games." *Physica A* 312, 208–216 (2002).

[36] Orús, R., Mugel, S. & Lizaso, E. "Quantum computing for finance: Overview and prospects." *Reviews in Physics* 4, 100028 (2019). DOI 10.1016/j.revip.2019.100028.

[37] Egger, D. J., Gambella, C., Mareček, J., et al. "Quantum Computing for Finance: State-of-the-Art and Future Prospects." *IEEE Transactions on Quantum Engineering* 1, 3101724 (2020). DOI 10.1109/TQE.2020.3030314.

[38] Rebentrost, P., Gupt, B. & Bromley, T. R. "Quantum computational finance: Monte Carlo pricing of financial derivatives." *Physical Review A* 98, 022321 (2018). DOI 10.1103/PhysRevA.98.022321.

[39] Herman, D., Googin, C., Liu, X., Sun, Y., Galda, A., Safro, I., Pistoia, M. & Alexeev, Y. "Quantum computing for finance." *Nature Reviews Physics* 5, 450–465 (2023).

[40] Bouland, A., van Dam, W., Joorati, H., Kerenidis, I. & Prakash, A. "Prospects and challenges of quantum finance." arXiv:2011.06492 (2020).

[41] Aaronson, S. "Read the fine print." *Nature Physics* 11, 291–293 (2015). DOI 10.1038/nphys3272.

[42] Preskill, J. "Quantum Computing in the NISQ era and beyond." *Quantum* 2, 79 (2018).

[43] Rabiner, L. R. "A tutorial on hidden Markov models and selected applications in speech recognition." *Proceedings of the IEEE* 77(2), 257–286 (1989).

[44] Hamilton, J. D. "A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle." *Econometrica* 57(2), 357–384 (1989).

[45] Hamilton, J. D. *Time Series Analysis*. Princeton University Press, 1994.

[46] Ang, A. & Timmermann, A. "Regime Changes and Financial Markets." *Annual Review of Financial Economics* 4, 313–337 (2012). DOI 10.1146/annurev-financial-110311-101808.

[47] Cappé, O., Moulines, E. & Rydén, T. *Inference in Hidden Markov Models*. Springer, 2005.

[48] Kyle, A. S. "Continuous Auctions and Insider Trading." *Econometrica* 53(6), 1315–1335 (1985).

[49] Almgren, R. & Chriss, N. "Optimal execution of portfolio transactions." *Journal of Risk* 3(2), 5–40 (2001).

[50] Newman, M. E. J. *Networks*, 2nd ed. Oxford University Press, 2018.

[51] Goldberg, D. "What Every Computer Scientist Should Know About Floating-Point Arithmetic." *ACM Computing Surveys* 23(1), 5–48 (1991).

[52] Higham, N. J. *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM, 2002.

[53] Preskill, J. *Ph219/CS219: Quantum Computation*, lecture notes, California Institute of Technology. Chapters 2 ("Foundations I: States and Ensembles") and 3 ("Foundations II: Measurement and Evolution"). `http://theory.caltech.edu/~preskill/ph219/`

[54] MIT OpenCourseWare. *18.435J Quantum Computation*, Massachusetts Institute of Technology. `https://ocw.mit.edu/courses/18-435j-quantum-computation-fall-2003/`

[55] MIT OpenCourseWare. *8.04 Quantum Physics I*, *8.05 Quantum Physics II*, *8.06 Quantum Physics III*, Massachusetts Institute of Technology.

---

*This module is theoretical and illustrative. Nothing in it is empirically validated, and nothing in it is financial advice, a diagnosis, or a forecast of any real market. The `amf` package models market structure and resilience only; every quantity above is a dimensionless structural measure.*
