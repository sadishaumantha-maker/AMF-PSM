# Q2: Markov Chains as Quantum State Transitions

> **Discussion category**: Research · **Labels**: `theory`, `open-quantum-systems`,
> `markov-chains`, `stress-dynamics`, `boundary-review`, `illustrative-only`
> **Source**: `docs/QUANTUM_NEURAL_RESEARCH.md` § Discussion Q2
> **Status**: Open for comment · **Nature**: Theoretical module, illustrative and not
> empirically validated

## 0. Abstract and reading guide

This module asks one precise question: *is AMF's stress-propagation dynamic a Markov chain, and if so, does
the theory of quantum dynamical semigroups add anything the classical theory does not already give?* The
answer is a qualified yes to the first and a heavily qualified "one thing" to the second. Section 5 proves
that the `ShockSimulator` step map is an affine map whose matrix is **sub-stochastic** on the sample market,
that its sub-stochasticity defect *is* the absorbed fraction the engine already reports, and that `centrality`
and total accumulated stress are the same Neumann series at different attenuations. It then builds a GKSL
generator on `C^7` whose diagonal reproduces the classical propagation **exactly** (Theorem 5.7), so the
quantum lift is conservative; the only genuinely new object is the off-diagonal block, which under purely
dissipative coupling decays and never regenerates (Proposition 5.9).

This module does **not** claim that markets are quantum, that coherence exists in market data, that the
construction predicts crises, or that any parameter here is calibrated. It claims a structural correspondence
between two pieces of mathematics and nothing more. Section 6 names, one by one, where the source note's
deliverables collide with the repository's hard rules.

**Prerequisite ladder.** Linear algebra over `C` → discrete-time Markov chains and Perron–Frobenius theory →
hidden Markov models → density operators and completely positive maps → quantum dynamical semigroups and the
GKSL theorem → divisibility and non-Markovianity → metastability and escape rates. Section 3 maps each rung to
courses and chapters.

---

## 1. Verbatim source specification

The following is the complete text of Discussion Q2 as it appears in `docs/QUANTUM_NEURAL_RESEARCH.md`,
reproduced without alteration. Its typography, notation, arrows and file paths are quoted, not endorsed; §5
and §6 comment on them.

````markdown
### Discussion Q2: Markov Chains as Quantum State Transitions
**Theme**: Hidden Markov Models ↔ Quantum Markov Chains: Can we bridge them?

**Classical HMM Review**:
```
States: {S₁, S₂, S₃, S₄} (e.g., bull, bear, crisis, recovery)
Transition matrix P:
  P[i,j] = Pr(Sⱼ | Sᵢ)  (probability of moving from state i to j)
Observable: Price, volume, sentiment (emitted with state-dependent probabilities)
```

**Quantum Markov Chains (QMC)**:
```
Quantum states: |ψ₁⟩, |ψ₂⟩, |ψ₃⟩, |ψ₄⟩ (basis states)
Lindblad master equation (time evolution with dissipation):
  d𝜌/dt = -i[H,𝜌] + Σₖ (LₖρLₖ† - 1/2{Lₖ†Lₖ,𝜌})
  
where:
  H = Hamiltonian (unitary evolution — pure dynamics)
  Lₖ = Lindblad operators (dissipation — noise, decoherence, market friction)
  
Density matrix 𝜌: Encodes both classical probability AND quantum coherence
```

**Key Innovations**:
1. **Coherence as Market Correlation**
   - Classical: ρᵢⱼ = 0 (uncorrelated states)
   - Quantum: ρᵢⱼ ≠ 0 (coherence = entangled risk factors)
   - Interpretation: Markets "remember" past shocks (coherence) before forgetting (decoherence)

2. **Dissipation as Market Friction**
   - Lindblad operators model: Bid-ask spreads, market impact, trading delays
   - Different sectors have different dissipation rates (equities < bonds < forex)
   - Policy intervention = negative dissipation (reduces friction, re-energizes market)

3. **Non-Markovian Dynamics**
   - Classical Markov: Next state depends only on current state (memoryless)
   - Market reality: Past shocks matter (memory, path-dependence)
   - Quantum solution: Non-Markovian QMC with memory kernels
   - Implementation: Bohmian trajectories or retarded Green's functions

4. **Rare Events & Rare Transitions**
   - Classical HMM: Rare transition probabilities = very small
   - Quantum tunneling analogy: State jumps via "tunneling" (very rare, but non-zero)
   - Flash crashes, circuit breakers: Market "tunnels" to new state without gradual transition
   - Use case: Predict probability of sudden state switches

**Mathematical Framework**:
```
Lindblad master equation for financial market:
d𝜌/dt = -i[H_policy + H_sentiment + H_leverage, 𝜌]
       + Σₖ (Lₖ(𝜌) - 1/2{Lₖ†Lₖ, 𝜌})

Dissipation operators:
  L_spread = √(bid_ask_spread) × (raise to lower liquidity)
  L_impact = √(market_impact) × (amplifies for large trades)
  L_delay = √(settlement_lag) × (delays state update)

Transition probability (after dissipation):
  Pᵢⱼ = |⟨ψⱼ|U(t)|ψᵢ⟩|²  where U(t) solves Lindblad equation
```

**Deliverable**:
- `docs/research/markov_quantum_bridge.md` — Theoretical comparison
- `src/amf/quantum/lindblad_market_model.py` — Lindblad solver for market states
- `examples/quantum_markov_crisis_prediction.py` — Test on historical data

**Research Leaders Needed**: Quantum information theorist, mathematician specializing in open quantum systems
````

---

## 2. Formal foundations

Throughout, `S` is finite with `|S| = n`; for AMF `n = 7` and `S = SystemKind` in declaration order
(`skeleton, circulatory, nervous, musculature, organs, immune, metabolism`). Matrices are indexed by that
order, and the ordering is normative, not cosmetic (see §6).

### 2.1 Classical chains

**Definition 2.1 (stochastic, sub-stochastic).** `P ∈ R^{n×n}` is *stochastic* if `P[i][j] >= 0` and
`Σ_j P[i][j] = 1` for all `i`; *sub-stochastic* if that equality is relaxed to `<= 1`. The *defect* of row `i`
is `δ_i = 1 − Σ_j P[i][j]`.

**Definition 2.2 (DTMC).** `(X_t)_{t>=0}` on `S` is a time-homogeneous Markov chain with matrix `P` if
`Pr(X_{t+1}=j | X_t=i, X_{t-1}, …, X_0) = Pr(X_{t+1}=j | X_t=i) = P[i][j]`.

**Theorem 2.3 (Chapman–Kolmogorov).** `P^{(s+t)}[i][j] = Σ_k P^{(s)}[i][k] · P^{(t)}[k][j]`, i.e.
`P^{(t)} = P^t`. *Proof.* Condition on `X_s = k`, apply the Markov property, sum over `k`. ∎ Norris [8, §1.1].

**Definition 2.4 (irreducible, aperiodic, reversible).** `P` is *irreducible* if for every `(i,j)` some
`P^t[i][j] > 0`; *aperiodic* if `gcd{t : P^t[i][i] > 0} = 1`; *reversible* w.r.t. `π` if
`π_i P[i][j] = π_j P[j][i]`, which makes `P` self-adjoint in `ℓ²(π)` and its spectrum real.

**Theorem 2.5 (Perron–Frobenius / convergence).** For irreducible aperiodic `P` on finite `S` there is a unique
`π` with `πP = π`, `π > 0`, and `‖P^t[i][·] − π‖_TV → 0` geometrically at a rate set by the second-largest
eigenvalue modulus [9, Ch. 4, Thm. 4.9; 12, Ch. 1].

**Definition 2.6 (relaxation and mixing times).** For reversible `P`, `t_rel = (1 − λ_2)^{-1}`; and
`t_mix(ε) = min{t : max_i ‖P^t[i][·] − π‖_TV <= ε}`, with
`(t_rel − 1) log(1/2ε) <= t_mix(ε) <= t_rel log(1/(ε π_min))` [9, Ch. 12, Thms. 12.4–12.5].

**Definition 2.7 (CTMC generator).** `G` with `G[i][j] >= 0` for `i ≠ j` and `Σ_j G[i][j] = 0` generates
`P_t = exp(tG)`, solving `dP_t/dt = P_t G` (forward) and `= G P_t` (backward) [8, Ch. 2–3]; `exp(tG)` is
stochastic for every `t >= 0`.

### 2.2 Hidden chains

**Definition 2.8 (HMM).** `(P, B, π)` with `P` a transition matrix on latent `S`,
`B[i][o] = Pr(O_t = o | X_t = i)` an emission kernel on a finite alphabet, `π` an initial law. Rabiner [10] is
the canonical exposition; Cappé, Moulines & Rydén [13] the rigorous one.

**Algorithms 2.9 (inference).** *Forward–backward*: `α_t(i) = Pr(o_{1:t}, X_t = i)` obeys
`α_{t+1}(j) = B[j][o_{t+1}] Σ_i α_t(i) P[i][j]`, with a mirror recursion for
`β_t(i) = Pr(o_{t+1:T} | X_t = i)`; both `O(Tn²)` [10, §III.A]. *Viterbi*: replace the sum by a max and store
arg-maxes for the most likely latent path [11]. *Baum–Welch*: the EM instance for HMMs, non-decreasing in
likelihood each iteration [14] — and it requires *observed data*, which matters in §6.

**Remark 2.10 (a strictly larger class).** Observable operator models [15] replace scalar emission weights by
matrices `τ_o` with `Σ_o τ_o` stochastic; HMMs are the case where every `τ_o` is nonnegative. OOMs are the
half-way house to §2.3 — operator-valued Markov chains with no Hilbert-space commitment.

### 2.3 Quantum channels

**Definition 2.11 (state, channel).** A density operator on `H ≅ C^n` is `ρ = ρ† >= 0` with `Tr ρ = 1`; a
diagonal `ρ` is exactly a probability vector. A linear `Λ : B(H) → B(H)` is *positive* if it maps `ρ >= 0` to
`Λ(ρ) >= 0`, *completely positive* (CP) if `Λ ⊗ id_k` is positive for every `k`, and a *channel* (CPTP) if it
is CP and `Tr Λ(ρ) = Tr ρ`.

**Theorem 2.12 (Choi; Kraus; Stinespring; Jamiołkowski).** The following are one theorem in four dresses.
(i) `Λ` is CP iff its Choi matrix `J(Λ) = Σ_{i,j} Λ(|i⟩⟨j|) ⊗ |i⟩⟨j|` is positive semidefinite [16].
(ii) `Λ` is CPTP iff `Λ(ρ) = Σ_a K_a ρ K_a†` with `Σ_a K_a† K_a = I` [18]; the `K_a` are eigenvectors of
`J(Λ)` rescaled by its eigenvalues. (iii) every CP map on a finite-dimensional C*-algebra is
`Λ(ρ) = V†(ρ ⊗ I)V` for an isometry `V` [19] — so every channel is a unitary on a larger space followed by a
partial trace, which is the precise sense in which "dissipation" is "coupling to something you chose not to
model". (iv) `Λ ↦ J(Λ)/n` is an affine bijection onto bipartite states with maximally mixed marginal [17].

### 2.4 Quantum dynamical semigroups and the GKSL equation

**Definition 2.13 (QDS).** A family of channels `{Λ_t}_{t>=0}` with `Λ_0 = id`, `Λ_t Λ_s = Λ_{t+s}` and
`t ↦ Λ_t` continuous; its generator is `L = lim_{t→0}(Λ_t − id)/t`.

**Theorem 2.14 (Gorini–Kossakowski–Sudarshan; Lindblad).** On `C^n`, `L` generates a semigroup of completely
positive trace-preserving maps if and only if it can be written

```
L(ρ) = -i[H, ρ] + Σ_k γ_k ( L_k ρ L_k† - (1/2){ L_k† L_k , ρ } )
```

with `H = H†`, `{L_k}` traceless and Hilbert–Schmidt orthonormal, and **all rates `γ_k >= 0`** — equivalently,
the Kossakowski matrix is positive semidefinite. Gorini, Kossakowski & Sudarshan [2] proved the bounded
finite-dimensional case, Lindblad [1] the norm-continuous case on a general C*-algebra; Chruściński & Pascazio
[20] reconstruct the history. This is the most load-bearing theorem in the module: the sign condition on `γ_k`
is not a technicality, and §5.9 shows the source note violates it.

**Definition 2.15 (divisibility).** `{Λ_t}` is *P-divisible* if for `t >= s` there is a positive
trace-preserving `V_{t,s}` with `Λ_t = V_{t,s} Λ_s`, and *CP-divisible* if every `V_{t,s}` may be taken CP.
CP-divisibility is the operational definition of quantum Markovianity used by Rivas, Huelga & Plenio [4].

**Theorem 2.16 (Wolf & Cirac; Wolf, Eisert, Cubitt & Cirac).** Not every channel lies on a continuous CP
semigroup: *indivisible* channels exist, and membership of a Markovian evolution is decidable from a single
snapshot by computable criteria [21, 22].

**Definitions 2.17 (measures of non-Markovianity).** *BLP* [5]: `N = max_{ρ_1,ρ_2} ∫_{σ>0} σ dt` with
`σ = (d/dt)‖Λ_t(ρ_1) − Λ_t(ρ_2)‖_1`, so any transient *increase* of trace distance is a witness. *RHP* [4]:
detect failure of CP-divisibility via positivity of `(id ⊗ V_{t+ε,t})` on a maximally entangled state.
*LFS* [23]: a correlation-based alternative. Li, Hall & Wiseman [6] prove these form a strict hierarchy and
are **not** equivalent — so "non-Markovian" must always be qualified by which definition is meant.

### 2.5 Memory kernels

**Theorem 2.18 (Nakajima–Zwanzig).** With `P` a projection onto the relevant part of a closed unitary dynamics
and `Q = 1 − P`, the relevant part obeys exactly

```
d(Pρ)/dt = P L (Pρ) + ∫_0^t K(t - s) (Pρ)(s) ds + I(t)
```

with kernel `K(τ) = P L Q exp(Q L Q τ) Q L P` and inhomogeneity `I(t) = P L Q exp(Q L Q t) Q ρ(0)`. Nakajima
[24] and Zwanzig [25] derived it independently; Breuer & Petruccione [3, §9.1] give the modern treatment.
Note `I(t)` vanishes for factorised initial conditions and is an initial-correlation term, **not** memory —
a distinction used in §5.10.

**Definition 2.19 (TCL).** The time-convolutionless expansion replaces the convolution by a time-local
generator `L_t` with time-dependent rates, order by order in the coupling [3, §9.2]. Transiently negative
rates are the standard signature of memory in time-local form.

**Remark 2.20 (what Born–Markov costs).** Deriving a GKSL equation from a system–bath model requires (i) weak
coupling, (ii) bath correlation time much shorter than the system relaxation time, and (iii) a secular /
rotating-wave step discarding fast-oscillating cross terms. Dropping (iii) gives the Redfield equation, which
is *not* CP in general [3, §3.3]. Any AMF-side analogue must state which of the three it assumes.

### 2.6 Rare transitions

**Theorem 2.21 (Kramers escape rate).** For overdamped Brownian motion in a well of barrier height `ΔU` at
temperature `T`, the mean escape rate in the high-friction limit is `k ≈ (ω_0 ω_b / 2πγ) exp(−ΔU / k_B T)`,
with `ω_0, ω_b` the curvatures at well and barrier [26]. Hänggi, Talkner & Borkovec [27] survey fifty years of
extensions, including the full friction turnover.

**Remark 2.22 (large deviations).** The statement generalises to Freidlin–Wentzell theory — escape times from a
metastable well scale as `exp(V/ε)` for a quasipotential `V` [28] — with the potential-theoretic sharpening in
Bovier & den Hollander [29]; Touchette [30] is the physicist's route in.

**Theorem 2.23 (metastability in open quantum dynamics).** If the spectrum of a Lindbladian `L` has a gap
between a low-lying group of `m` eigenvalues and the rest, the dynamics first relaxes into an `m`-dimensional
*metastable manifold* and only later reaches the stationary state; under stated conditions the long-time
dynamics inside that manifold is an effective classical `m`-state Markov chain [31]. **This theorem, not
tunnelling, is the honest quantum counterpart of "a market sits in a regime and occasionally switches."**

**Remark 2.24 (tunnelling proper).** Genuine tunnelling needs a coherent off-diagonal matrix element
connecting classically disconnected configurations; the semiclassical rate follows from WKB/instanton analysis
[32, 33], and coupling to an environment *suppresses* it (Caldeira–Leggett [34]). A model whose only
off-diagonal structure is dissipative jumps has **no** tunnelling, only activated hopping — made precise for
AMF in §5.11.

---

## 3. Academic curriculum modules

The ladder below is the sequence a graduate student would actually take. "What AMF needs" is deliberately
narrow: most of each course is not required, and the column names the part that is.

| Module | Level | Canonical course(s) | Core texts (exact units) | What AMF needs from it |
|---|---|---|---|---|
| M1. Linear algebra of nonnegative matrices | UG3 | Any advanced linear algebra sequence | Horn & Johnson, *Matrix Analysis*, 2nd ed., CUP 2013, **Ch. 8** (positive & nonnegative matrices); Seneta [12] **Ch. 1–2** | Perron root, spectral radius, why `α·ρ(A) < 1` is the exact convergence criterion for `centrality` |
| M2. Measure-theoretic probability | UG4/PG1 | Cambridge Part III *Advanced Probability*; equivalent first-year PhD probability | Williams, *Probability with Martingales*, CUP 1991, **Ch. 9–12**; Durrett, *Probability: Theory and Examples*, 5th ed., CUP 2019, **Ch. 4–5** | Conditional expectation done properly; the Markov property as a statement about σ-algebras |
| M3. Discrete stochastic processes | PG1 | MIT **6.262** *Discrete Stochastic Processes* (OCW, Gallager); Stanford / Berkeley applied stochastic-processes sequences | Norris [8] **Ch. 1** (DTMC), **Ch. 2–3** (CTMC, generators); Gallager's 6.262 notes **Ch. 3–6** | Generator matrices, embedded jump chains, first-passage decompositions |
| M4. Mixing times and spectral methods | PG2 | Topics courses following Levin–Peres | Levin & Peres [9] **Ch. 1–4, 7, 12–13** | Relaxation time as the principled version of AMF's "settling time"; the `t_rel`/`t_mix` bounds |
| M5. Hidden Markov models & regime switching | PG1 | Statistical ML / time-series econometrics sequences | Rabiner [10] **§II–IV**; Bishop, *PRML*, Springer 2006, **Ch. 13.1–13.2**; Cappé–Moulines–Rydén [13] **Ch. 3–6**; Hamilton, *Time Series Analysis*, Princeton 1994, **Ch. 22** | Forward–backward, Viterbi, EM; and the honest limits on identifiability with short samples |
| M6. Regime-switching econometrics | PG2 | Advanced time-series econometrics | Hamilton [35] (the 1989 paper) plus [36, **Ch. 22**] | What a "market regime" means when estimated rather than assumed; standard-error realities |
| M7. Quantum mechanics foundations | UG4 | Standard graduate QM | Sakurai & Napolitano, *Modern Quantum Mechanics*, **Ch. 1–3**; Nielsen & Chuang [37] **Ch. 2** | Hilbert space, density operators, partial trace |
| M8. Quantum information & channels | PG1 | MIT **8.370x/8.371x** *Quantum Information Science I & II*; Caltech **Ph219/CS219** *Quantum Computation* (Preskill) | Nielsen & Chuang [37] **Ch. 8** (quantum noise & operations); Watrous, *The Theory of Quantum Information*, CUP 2018, **Ch. 2, 4**; Wilde, *Quantum Information Theory*, 2nd ed., CUP 2017, **Ch. 4** | Choi/Kraus/Stinespring as one theorem; the CP condition as a linear-algebraic test |
| M9. Open quantum systems | PG2 | ETH Zürich and Ulm graduate lecture courses on open quantum systems (Plenio/Huelga school) | Breuer & Petruccione [3] **Ch. 3 (§3.1–3.3), Ch. 9**; Rivas & Huelga [38] **Ch. 3–4**; Alicki & Lendi [7] | The GKSL theorem with hypotheses; Born–Markov–secular derivation and what each step costs |
| M10. Non-Markovianity | PG3 / research | Topics seminars | Rivas, Huelga & Plenio [4] **§2–4**; de Vega & Alonso [39] **§II–IV**; Li, Hall & Wiseman [6] **§2–6** | Why "non-Markovian" names at least four inequivalent things; how to pick one and say so |
| M11. Rare events & metastability | PG3 | Statistical-mechanics / applied-probability topics | Kramers [26]; Hänggi et al. [27] **§II–IV**; Freidlin & Wentzell [28] **Ch. 4**; Bovier & den Hollander [29] **Part II**; Macieszczak et al. [31] | The correct escape-rate formalism, and the correct quantum version (spectral gap, not tunnelling) |
| M12. Matrix functions & numerics | PG1 | Numerical analysis sequence | Higham, *Functions of Matrices*, SIAM 2008, **Ch. 10**; Moler & Van Loan [40] | How to compute `exp(τG)` reproducibly; why eigendecomposition is a determinism hazard |
| M13. Floating-point determinism | PG1 | Scientific-computing / systems courses | Goldberg [41]; Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM 2002, **Ch. 1–4** | Why insertion order changes the last bits, which is exactly why `SystemKind` order is normative |
| M14. Financial networks & systemic risk | PG2 | Financial-stability / network-economics courses | Eisenberg & Noe [42]; Gai & Kapadia [43]; Haldane & May [44]; Acemoglu, Ozdaglar & Tahbaz-Salehi [45]; Elliott, Golub & Jackson [46] | The domain-native contagion literature AMF is adjacent to, and against which any claim here must be positioned |
| M15. Critical reading of quantum-finance claims | PG3 | Reading groups | Gallegati et al. [47]; Sornette [48]; Aaronson [49]; Herman et al. [50] | Calibration of expectation; the skeptical prior this module adopts |

Prose note on sequencing: M1–M4 are self-contained and sufficient to read §5.1–§5.5 of this module. M7–M9 are
required for §5.6 onward. M10–M11 are needed only to evaluate the source note's claims 3 and 4. A reader who
takes M1–M5 and M14 alone will already be able to falsify or confirm most of §7.

---

## 4. Exact source material

### 4.1 Primary and seminal papers

- **Lindblad (1976)** [1] — the generator of a norm-continuous CPTP semigroup has the dissipator form.
- **Gorini, Kossakowski & Sudarshan (1976)** [2] — the `N`-level companion, with the Kossakowski matrix and its
  positive-semidefiniteness condition explicit.
- **Choi (1975)** [16] — CP ⟺ positivity of the Choi matrix; the computational criterion.
- **Jamiołkowski (1972)** [17] — the channel–state duality underlying [16].
- **Stinespring (1955)** [19] — every CP map dilates to an isometry: dissipation is unitarity on a bigger space.
- **Nakajima (1958)** [24] and **Zwanzig (1960)** [25] — the exact projection-operator equation with a memory kernel.
- **Breuer, Laine & Piilo (2009)** [5] — the trace-distance (information-backflow) measure of non-Markovianity.
- **Wolf, Eisert, Cubitt & Cirac (2008)** [22] — Markovianity is decidable from one channel snapshot;
  **Wolf & Cirac (2008)** [21] — indivisible channels exist.
- **Luo, Fu & Song (2012)** [23] — correlation-based non-Markovianity measure.
- **Macieszczak, Guţă, Lesanovsky & Garrahan (2016)** [31] — spectral theory of metastability in Lindbladian
  dynamics; an effective classical chain on the metastable manifold.
- **Kramers (1940)** [26] — thermally activated escape rate over a barrier.
- **Rabiner (1989)** [10] — the canonical HMM tutorial: forward–backward, Viterbi, Baum–Welch.
- **Baum, Petrie, Soules & Weiss (1970)** [14] — the maximisation technique that became EM for HMMs.
- **Viterbi (1967)** [11] — the maximum-likelihood path decoder.
- **Hamilton (1989)** [35] — Markov-switching regimes in econometrics; what `{bull, bear, crisis, recovery}` invokes.
- **Jaeger (2000)** [15] — observable operator models; HMMs as a proper subclass of linearly dependent processes.
- **Monras, Beige & Wiesner (2010)** [51] — hidden *quantum* Markov models: the object the note's title asks for.
- **Accardi, Frigerio & Lewis (1982)** [52] — quantum stochastic processes in the operator-algebraic sense.
- **Gudder (2008)** [53] — "quantum Markov chains" via transition operation matrices whose entries are CP maps.

### 4.2 Canonical textbooks

- **Breuer & Petruccione**, *The Theory of Open Quantum Systems*, OUP 2002 [3] — **Ch. 3** (§3.1 semigroups,
  §3.2 microscopic derivations, §3.3 Redfield vs. Lindblad) and **Ch. 9** (Nakajima–Zwanzig, TCL).
- **Rivas & Huelga**, *Open Quantum Systems: An Introduction*, Springer (SpringerBriefs), 2012 [38] — **Ch. 3**
  GKSL at a third of the length; **Ch. 4** the divisibility view of Markovianity.
- **Kraus**, *States, Effects, and Operations*, Springer LNP 190, 1983 [18] — the operator-sum representation.
- **Nielsen & Chuang**, *Quantum Computation and Quantum Information*, 10th Anniv. ed., CUP 2010 [37] — **Ch. 2**
  density operators and partial trace; **Ch. 8** quantum operations and the operator-sum freedom.
- **Norris**, *Markov Chains*, CUP 1997 [8] — **Ch. 1** discrete time, **Ch. 2** generators, **Ch. 3** hitting times.
- **Levin & Peres**, *Markov Chains and Mixing Times*, 2nd ed., AMS 2017 [9] — **Ch. 4** convergence, **Ch. 12**
  eigenvalues and relaxation time, **Ch. 13** conductance.
- **Hamilton**, *Time Series Analysis*, Princeton UP 1994 [36] — **Ch. 22**, the econometric HMM chapter.
- **Cappé, Moulines & Rydén**, *Inference in Hidden Markov Models*, Springer 2005 [13] — rigorous filtering and EM.
- **Seneta**, *Non-negative Matrices and Markov Chains*, Springer [12] — **Ch. 1–2**, Perron–Frobenius in the
  generality sub-stochastic kernels need.
- **Davies**, *Quantum Theory of Open Systems*, Academic Press 1976 [54] — functional-analytic parent of [1, 2].
- **Alicki & Lendi**, *Quantum Dynamical Semigroups and Applications*, Springer LNP [7] — the compact reference
  for the generator in the form used in §5.6.

### 4.3 Surveys and reviews

- **Rivas, Huelga & Plenio (2014)**, *Rep. Prog. Phys.* [4] — the standard non-Markovianity survey: definitions,
  measures, and their inequivalence.
- **de Vega & Alonso (2017)**, *Rev. Mod. Phys.* [39] — techniques beyond the Markov approximation (memory
  kernels, TCL, hierarchical equations, chain mappings, pseudomodes). The correct answer to the note's
  "Implementation" line.
- **Li, Hall & Wiseman (2018)**, *Physics Reports* [6] — a hierarchy of non-Markovianity concepts with the
  implication arrows drawn.
- **Hänggi, Talkner & Borkovec (1990)**, *Rev. Mod. Phys.* [27] — the definitive escape-rate review.
- **Touchette (2009)**, *Physics Reports* [30] — large deviations for physicists.
- **Chruściński & Pascazio (2017)** [20] — history of the GKLS equation and correct attribution of its parts.
- **Herman et al. (2023)**, *Nature Reviews Physics* [50] — quantum computing for finance, explicit about what is
  *not* yet demonstrated; **Orús, Mugel & Lizaso (2019)**, *Reviews in Physics* [55] — the earlier survey.

### 4.4 Open courseware and lecture notes

- **MIT OpenCourseWare 6.262, *Discrete Stochastic Processes*** (Spring 2011, R. Gallager) — video lectures,
  problem sets and draft text; the Markov-chain and renewal units are the relevant ones.
- **MIT 8.370x / 8.371x, *Quantum Information Science I & II*** (MITx / MIT Open Learning Library) — 8.371x runs
  as three modules (`8.371.1x` states, noise and error correction; `8.371.2x` fault tolerance and algorithms;
  `8.371.3x` complexity and information theory). Module 1 covers channels at the level §5 needs.
- **Caltech Ph219/CS219, *Quantum Computation*** (J. Preskill), lecture notes — the measurement-and-evolution
  chapter derives Kraus and Stinespring cleanly and free.
- **Cambridge Part III of the Mathematical Tripos**, *Advanced Probability* and *Quantum Information Theory* —
  between them these cover §2.1 and §2.3 at full rigour.
- **ETH Zürich and Ulm University graduate courses on open quantum systems** — the Ulm institute (Plenio,
  Huelga) is the group behind [4] and [38], and its material tracks that book closely. Course numbers are
  omitted deliberately: they change, and this module cites nothing it has not verified.

### 4.5 Domain application to finance and markets — including the skeptical literature

- **Baaquie**, *Quantum Finance*, CUP 2004 [56] — the most developed use of quantum *formalism* (not hardware) in
  finance. Read for technique; its Hamiltonians are reparameterisations of stochastic models, not discoveries.
- **Busemeyer & Bruza**, *Quantum Models of Cognition and Decision*, CUP 2012 [57] — the "quantum-like" programme,
  where interference models *order effects* in judgement. The closest thing to a genuine empirical case for
  non-classical probability in an economic setting — and it is about survey responses, not markets.
- **Khrennikov**, *Ubiquitous Quantum Structure: From Psychology to Finance*, Springer 2010 [58].
- **Aaronson (2015)**, *Nature Physics* [49] — "Read the fine print": quantum speed-ups in data-driven settings
  hide their costs in state preparation and read-out. Applies to any claim that this model "predicts" anything.
- **Gallegati, Keen, Lux & Ormerod (2006)**, *Physica A* [47] — "Worrying trends in econophysics": unawareness of
  prior economics literature, weak statistical methodology, unjustified universality, theoretical over-reach.
  Every one applies to the source note as written.
- **Sornette (2014)**, *Rep. Prog. Phys.* [48] — an honest audit of what physics has and has not contributed to
  financial economics since 1776.
- **Eisenberg & Noe (2001)** [42], **Gai & Kapadia (2010)** [43], **Haldane & May (2011)** [44], **Acemoglu,
  Ozdaglar & Tahbaz-Salehi (2015)** [45], **Elliott, Golub & Jackson (2014)** [46] — the mainstream
  network-contagion literature. Any structural-cascade claim should be positioned against these before it is
  positioned against quantum optics.

---

## 5. Derivation for the AMF setting

This is the substantive section. It works only with objects the repository already has: `SystemKind`,
`AnatomicalSystem` metrics, `DependencyGraph`, `CouplingMatrix`, `SimulationConfig`, and the stress recursion
in `simulation.py`. Every numeric value below is computed from `examples/sample_market.json` and the default
`SimulationConfig` (`damping = 0.85`, `retention = 0.5`, `transmission = 1.0`).

### 5.1 Notation fixed to the codebase

Index the seven systems by `SystemKind` declaration order, `i ∈ {0..6}`. Write:

```
a_i  = absorptive_capacity(i) = 0.5*redundancy + 0.3*integrity + 0.2*(1 - load)
W[i][j] = CouplingMatrix.get(transmitter=i, receiver=j)      # stress flows i -> j
d    = damping,  r = retention,  c = transmission
```

For `examples/sample_market.json`:

```
a = (skeleton .54, circulatory .54, nervous .67, musculature .80,
     organs .70, immune .75, metabolism .70)

W (non-zero entries, transmitter -> receiver):
  skeleton -> circulatory .8   skeleton -> nervous .5   skeleton -> immune .3
  circulatory -> musculature .7  circulatory -> organs .6
  nervous -> circulatory .5
  musculature -> nervous .6
  organs -> metabolism .4
  immune, metabolism: no outgoing stress
```

### 5.2 The AMF step map is an affine map with a nonnegative matrix

From `simulation.py`, before clipping,

```
x_{t+1}[j] = d * ( r * x_t[j] + Σ_i x_t[i] * W[i][j] * c * (1 - a_j) )
           = Σ_i M[i][j] * x_t[i],
where  M[i][j] = d * ( r * δ_ij + W[i][j] * c * (1 - a_j) ).
```

So `x_{t+1} = Mᵀ x_t` on the region where the clip is inactive. `M >= 0` entrywise because `d, r, c
>= 0`, `W >= 0`, and `a_j ∈ [0,1]`.

**Definition 5.1 (effective transmission).** `E[i][j] = W[i][j] · c · (1 − a_j)` for `i ≠ j`, so `M = d·r·I +
d·E`.

For the sample market, `E` (three decimals):

```
skeleton    -> circulatory .368   -> nervous .165   -> immune .075     (row sum .608)
circulatory -> musculature .140   -> organs  .180                      (row sum .320)
nervous     -> circulatory .230                                        (row sum .230)
musculature -> nervous     .198                                        (row sum .198)
organs      -> metabolism  .120                                        (row sum .120)
immune, metabolism: row sum 0
```

### 5.3 Proposition: the sample market's step matrix is sub-stochastic

**Proposition 5.2.** `M` is sub-stochastic iff for every `i`, `d·(r + Σ_j E[i][j]) <= 1`. For the sample
market and default config the row sums of `M` are

```
skeleton .9418   circulatory .6970   nervous .6205   musculature .5933
organs   .5270   immune      .4250   metabolism  .4250
```

all strictly below `1`, with defects

```
δ = (.0582, .3030, .3795, .4067, .4730, .5750, .5750).
```

*Proof.* Row sum of `M` at `i` is `d·r + d·Σ_{j≠i} E[i][j]`; substitute the table in §5.2. ∎

**Corollary 5.3 (the killed chain).** Adjoin an eighth, absorbing state `⊥` ("absorbed") and set `M̂[i][⊥] =
δ_i`, `M̂[⊥][⊥] = 1`. Then `M̂` is a genuine stochastic matrix on eight states and the AMF stress vector is
the *sub-probability* vector of an absorbed chain: `x_t[j] = Σ_i x_0[i] · Pr(X_t = j, X_s ≠ ⊥ for s <= t | X_0
= i)`.

**This is the exact sense in which AMF already is a Markov chain**, and it is a stronger statement than the
source note attempts. The defect `δ_i` is not a modelling artefact: it is stress removed by damping and by
absorptive capacity, i.e. precisely the quantity `ResilienceScore` reports as the absorbed fraction. Damping
and capacity are the *killing rate* of the chain.

**Caveat 5.4 (not universal).** Sub-stochasticity is a property of *this* market with *these* parameters, not
a theorem about AMF. If `Σ_j E[i][j] > 1/d − r` for some `i` — a system with many heavy outgoing couplings
into low-capacity receivers — the row sum exceeds one, `M` is no longer sub-stochastic, and the `[0,1]` clip
in `simulation.py` is what keeps the trajectory bounded. This is the same phenomenon `simulation.py`
records when it notes that damping and capacity do not make the step map a contraction for every market —
now with a name: the chain is
*super-stochastic* and the clip is a hard nonlinearity, not a rounding convenience.

### 5.4 Spectral radius, settling time, and the relaxation-time analogue

Since `M = d·r·I + d·E`, `spec(M) = d·r + d·spec(E)`. `E`'s directed graph has exactly one cycle, `circulatory
→ musculature → nervous → circulatory`, with weight product `.140 × .198 × .230 = 6.3756e-3`; every other
strongly connected component is a singleton with zero diagonal. Hence `ρ(E) = (6.3756e-3)^{1/3} ≈ 0.18543` and

```
ρ(M) = 0.85*0.5 + 0.85*0.18543 ≈ 0.4250 + 0.1576 = 0.5826.
```

**Proposition 5.5 (settling estimate).** While the clip is inactive, `‖x_t‖ ≲ ρ(M)^t ‖x_0‖`, so the number of
steps to reach `convergence_eps = 1e-4` is asymptotically `t* ≈ log(1e-4)/log(0.5826) ≈ 17.1`. The default
`max_steps = 50` therefore leaves roughly a factor of three of headroom on this market. The quantity `1/|log
ρ(M)|` is the AMF analogue of the relaxation time `t_rel` of Definition 2.6; "settling time" in
`SimulationTrace` is an empirical `t_mix`-like statistic, and the bounds of [9, Ch. 12] are the right tool for
relating them.

**Corollary 5.6 (Katz and total stress are one series).** Because `ρ(M) < 1`, the Neumann series converges and
the *total accumulated stress* is

```
Σ_{t>=0} x_t = (I - Mᵀ)^{-1} x_0.
```

`DependencyGraph.centrality` computes `Σ_{k>=1} α^k (Aᵀ)^k 1` for the pair-weight adjacency `A`. These are the
same object at different attenuation: total stress is the Katz series of `E` at `α = d`, seeded by `x_0`
instead of `1`. The convergence condition is identical, `α·ρ(A) < 1`. For the sample market the dependency
cycle `circulatory → nervous → musculature → circulatory` has weight product `.5×.6×.7 = 0.21`, so `ρ(A) =
0.21^{1/3} ≈ 0.5944` and the default `alpha = 0.4` gives `α·ρ(A) ≈ 0.238 << 1` — comfortably convergent. On a
densely coupled market where `ρ(A) > 2.5`, the default `alpha` alone breaks the series. That is the
mathematical content of the existing CLAUDE.md warning, stated as an inequality rather than an anecdote.

### 5.5 A continuous-time generator for AMF

Set a nominal timestep `τ > 0` (dimensionless: AMF has no clock) and define rates

```
γ_ij = W[i][j] * c * (1 - a_j) / τ      for i ≠ j
Γ_i  = Σ_{j≠i} γ_ij                      (total outflow rate of system i)
κ_i  = (1/τ) * ( 1/d - r - Σ_j E[i][j] )   (killing rate; may be negative — see 5.4)
```

Then `G[i][j] = γ_ij` for `i ≠ j` and `G[i][i] = −Γ_i` is a bona fide CTMC generator (Definition 2.7) on the
seven systems, and the killed generator `Ĝ` on eight states adds the column `κ_i` into `⊥`. For the sample
market at `τ = 1`:

```
Γ = (skeleton .608, circulatory .320, nervous .230, musculature .198,
     organs .120, immune 0, metabolism 0).
```

Note immediately: **`immune` and `metabolism` have zero outflow.** They are pure sinks of the dependency
graph. This is a fact about the sample market, and it will matter in §5.8.

### 5.6 The quantum lift, and the theorem that makes it conservative

Let `H = C^7` with the orthonormal basis `{|s⟩}` indexed by `SystemKind` **in declaration order** — the
ordering is part of the definition, not an implementation detail. States are density operators `ρ` on `H`;
`ρ_ss` is the share of systemic load carried by `s`, and `ρ_st` (`s ≠ t`) is what the source note calls
coherence.

Define the GKSL data:

```
Jump operators (couplings):   L_{i→j} = sqrt(γ_ij) |j><i|,      γ_ij >= 0
Dephasing operators (friction): L_j^φ = sqrt(κ_j^φ) |j><j|,     κ_j^φ >= 0
Hamiltonian:                  H = Σ_s ε_s |s><s| + Σ_{s<t} h_st (|s><t| + |t><s|)
```

with `ε_s = criticality(s)` and `h_st` a *coherent* coupling amplitude that AMF does not currently possess
(see §5.11). The generator is

```
L(ρ) = -i[H, ρ]
     + Σ_{i≠j} ( L_{i→j} ρ L_{i→j}† - (1/2){ L_{i→j}† L_{i→j}, ρ } )
     + Σ_j    ( L_j^φ   ρ L_j^φ†   - (1/2){ L_j^φ† L_j^φ,     ρ } ).
```

All rates are nonnegative by construction (`W >= 0`, `a_j <= 1`), so Theorem 2.14 applies: `Λ_t = exp(tL)` is
a CPTP semigroup. Good.

**Theorem 5.7 (classical embedding).** With `h_st = 0` and `κ_j^φ` arbitrary, the diagonal of `ρ` evolves
autonomously and reproduces the classical generator of §5.5 exactly:

```
d ρ_jj / dt = Σ_{i≠j} γ_ij ρ_ii - Γ_j ρ_jj .
```

*Proof.* For `L_{i→j} = sqrt(γ_ij)|j⟩⟨i|`, the gain term is `Σ_{i≠j} γ_ij |j⟩⟨i| ρ |i⟩⟨j| = Σ_j ( Σ_{i≠j} γ_ij
ρ_ii ) |j⟩⟨j|`, which is **diagonal**. The anticommutator term uses `L_{i→j}† L_{i→j} = γ_ij |i⟩⟨i|`, so
`−(1/2){ Σ_{i,j} γ_ij |i⟩⟨i| , ρ }` has `(j,j)` entry `−Γ_j ρ_jj`. Dephasing operators `|j⟩⟨j|` contribute
`κ_j^φ ρ_jj |j⟩⟨j| − κ_j^φ ρ_jj |j⟩⟨j| = 0` on the diagonal. With `h_st = 0` the commutator with a diagonal
`H` also has zero diagonal. Summing gives the claim. ∎

**Corollary 5.8.** The quantum lift is *conservative*: it contains AMF's existing stress propagation as an
exactly invariant subspace (the diagonal). No result of the current engine can change under the lift. Any
behavioural difference must come from the off-diagonal block, and therefore is attributable and auditable.

### 5.7 What the off-diagonal block actually does

**Proposition 5.9 (pure decoherence, no coherence generation).** Under the generator of §5.6 with `h_st = 0`,
for `j ≠ k`:

```
d ρ_jk / dt = [ -i(ε_j - ε_k) - (1/2)(Γ_j + Γ_k) - (1/2)(κ_j^φ + κ_k^φ) ] ρ_jk .
```

*Proof.* The gain term computed in Theorem 5.7 is diagonal, so it contributes nothing to `(j,k)` with `j ≠ k`.
The anticommutator contributes `−(1/2)(Γ_j + Γ_k)ρ_jk`; the dephasing anticommutator contributes `−(1/2)(κ_j^φ
+ κ_k^φ)ρ_jk` while its gain term `κ_j^φ ρ_jj |j⟩⟨j|` is diagonal. The commutator with diagonal `H` gives
`−i(ε_j − ε_k)ρ_jk`. ∎

Consequences, in order of importance:

1. **Coherence decays and is never created.** `|ρ_jk(t)| = |ρ_jk(0)| e^{-t/T_2^{jk}}` with `T_2^{jk} = 2 /
   (Γ_j + Γ_k + κ_j^φ + κ_k^φ)`. The source note's picture — "markets remember past shocks (coherence) before
   forgetting (decoherence)" — is *exactly* realised, but only as a decay of an initial condition. Nothing in
   AMF's structure generates coherence, so a lifted market that starts diagonal stays diagonal forever. The
   whole quantum apparatus is then inert.
2. **Coherence times are computable from the existing market file.** With `κ^φ = 0` and `τ = 1`, the sample
   market gives `T_2(skeleton, circulatory) = 2/0.928 ≈ 2.16` steps, `T_2(skeleton, immune) = 2/0.608 ≈ 3.29`,
   and — the pathological case — `T_2(immune, metabolism) = ∞`, because both are pure sinks with `Γ = 0`.
3. **The pathology is diagnostic, not fatal.** Two systems that transmit no stress retain perfect structural
   coherence indefinitely, which is obviously wrong as a model. The fix is the dephasing channel: setting
   `κ_j^φ = 1 − a_j` (low absorptive capacity ⟹ fast loss of structural memory) gives `T_2(immune, metabolism)
   = 2/(0.25 + 0.30) ≈ 3.64`. Note that `κ_j^φ` is then a *new free parameter with no empirical anchor*, which
   is precisely the kind of unvalidated knob §6 requires to be declared.
4. **The Hamiltonian only rotates phases.** With `H` diagonal, `ε_s = criticality(s)` produces oscillation at
   frequency `|ε_j − ε_k|` and no population transfer at all. Since `musculature` and `metabolism` share
   `criticality = 0.60`, that pair does not even oscillate. A Hamiltonian that *does* something requires the
   off-diagonal `h_st`, which AMF has no data to set.

### 5.8 The discrete channel: Kraus form of one AMF step

Fix `τ` and let `Λ_τ = exp(τ L)`. Theorem 2.12 guarantees a Kraus decomposition; for the purely dissipative
generator it can be written down to first order in `τ` as

```
K_{i→j} = sqrt(τ γ_ij) |j><i|      (i ≠ j)
K_0     = I - (τ/2) Σ_{i≠j} γ_ij |i><i| + O(τ²)
```

with `Σ_a K_a† K_a = I + O(τ²)`. Restricted to the diagonal, `K_{i→j}` reproduces exactly the classical
transition `i → j` with probability `τ γ_ij`, and `K_0` the stay probability. The Choi matrix `J(Λ_τ) = Σ_{ij}
Λ_τ(|i⟩⟨j|) ⊗ |i⟩⟨j|` is positive semidefinite for `τ γ_ij >= 0`; a **negative** rate makes one eigenvalue of
`J` negative and destroys complete positivity while leaving the diagonal dynamics superficially plausible.
This is the failure mode that the source note's item 2 walks into (§5.9).

### 5.9 Three corrections to the source note's mathematics

**Correction A (negative dissipation is not a policy lever; it breaks the theorem).** The note proposes
"Policy intervention = negative dissipation (reduces friction, re-energizes market)". By Theorem 2.14, a
generator in GKSL form with some `γ_k < 0` does **not** generate a semigroup of completely positive maps.
Concretely, at the Choi level the negative rate produces `J(Λ_τ) ⊁ 0` and there exist entangled inputs on
which `Λ_τ ⊗ id` returns a non-positive operator; at the reduced level `ρ` can acquire negative eigenvalues,
i.e. negative structural load. The *correct* formulation of "policy reduces friction" is a **time-dependent
but nonnegative** rate `γ_k(t) >= 0` that is lowered after the intervention step — which is exactly the
semantics of AMF's existing `Intervention` (a time-gated boost to `absorptive_capacity`). Transiently negative
rates *do* have a legitimate meaning: they signal a CP-indivisible, non-Markovian family (Definitions 2.15,
2.27) obtained by eliminating a memory, not a market being "re-energized".

**Correction B (there is no `U(t)` solving the Lindblad equation).** The note writes `Pᵢⱼ =
|⟨ψⱼ|U(t)|ψᵢ⟩|² where U(t) solves Lindblad equation`. The Lindblad equation does not generate a
unitary; that is its entire point. The correct expression for the state-to-state transition probability of the
AMF lift is

```
P_τ[i][j] = Tr[ |j><j| · Λ_τ( |i><i| ) ] = <j| Λ_τ(|i><i|) |j>,
```

which is manifestly a stochastic matrix by CPTP-ness (each row is a probability vector). The `|⟨·|·⟩|²` form
is recovered only in the special case `Λ_τ(ρ) = UρU†`, i.e. zero dissipation — the case the note is trying to
move away from.

**Correction C (Bohmian trajectories are not a memory-kernel technique).** The note lists "Bohmian
trajectories or retarded Green's functions" as the implementation route for non-Markovian dynamics. Bohmian
mechanics is an interpretation of *closed-system* quantum theory; it supplies trajectories, not memory
kernels. The actual toolkit for non-Markovian open dynamics — enumerated by de Vega & Alonso [39] — is:
Nakajima–Zwanzig kernels (Theorem 2.18), TCL expansions (Definition 2.19), hierarchical equations of motion,
pseudomode and chain-mapping constructions, and stochastic unravellings (non-Markovian quantum state
diffusion). Any of those is a defensible substitution; the sentence as written is not.

### 5.10 What in AMF is and is not non-Markovian

| AMF feature | Formal status | Correct name |
|---|---|---|
| `retention` (own stress carried forward) | Markovian: it is a diagonal entry of `M` | self-transition, not memory |
| `Shock.at_step` (multi-wave) | Markovian: it is the inhomogeneity `I(t)` of Theorem 2.18, not the kernel `K` | time-dependent driving |
| `Intervention.at_step` | Markovian with time-dependent generator; CP-divisible if rates stay `>= 0` | inhomogeneous Markov family |
| `cascade_threshold` (state-dependent impairment) | **Not a dynamical map at all**: the generator depends on the current state, so the evolution is *nonlinear* | mean-field / nonlinear master equation |
| `jitter` + `seed` | Random generator drawn per replication; each replication is Markovian, the ensemble average is generally not | stochastic Liouvillian / random unitary mixture |

**Proposition 5.10.** Because `cascade_threshold` makes the step map nonlinear in `x_t`, none of the
non-Markovianity measures of §2.4 apply to it: BLP, RHP and Luo–Fu–Song are all defined on *linear* families
`{Λ_t}`. A cascade-enabled AMF simulation is not a non-Markovian quantum channel; it is a different kind of
object. Claiming otherwise would be a category error, and it is the most likely error a well-meaning
implementer would make.

**Proposition 5.11 (the ensemble is where non-Markovianity could legitimately enter).**
`ShockSimulator.ensemble` averages replications with different transmission jitter. An average of distinct
CPTP semigroups `∫ dμ(θ) exp(t L_θ)` is CPTP for every `t` but is generally **not** CP-divisible, hence
non-Markovian in the sense of Definition 2.15 — this is the standard random-Liouvillian mechanism. If the
repository ever wants a defensible non-Markovianity claim, this is the only place it currently has one, and it
is a claim about the *ensemble*, not about any market.

### 5.11 Rare transitions: what AMF can and cannot say

**Proposition 5.12 (no tunnelling without coherent coupling).** With `h_st = 0` the generator of §5.6 has
strictly nonnegative off-diagonal elements in the population sector and zero coherent coupling. There is no
classically forbidden region and no barrier penetration: every `i → j` transition proceeds at the activated
rate `γ_ij`, which is zero exactly when `W[i][j] = 0`. Hence for a market with `W[i][j] = 0`, the "quantum
tunnelling" of the note's item 4 gives probability **exactly zero**, not "very rare but non-zero". To obtain a
nonzero rate between structurally decoupled systems one must postulate `h_st ≠ 0`, i.e. a coherent coupling
for which AMF has no input field.

**The defensible version.** The mechanism that genuinely produces "the market sits in a regime and then
switches abruptly" is metastability, Theorem 2.23: a spectral gap in `L` between `m` slow modes and the rest
yields an effective `m`-state classical chain on the metastable manifold, with switching rates set by the
small eigenvalues. Its classical counterpart is Kramers escape (Theorem 2.21) and, in full generality,
Freidlin–Wentzell large deviations (Remark 2.22). For AMF this is a *computable* research question with no new
physics: diagonalise the seven-state generator `Ĝ` of §5.5, look for a spectral gap, and report the resulting
slow-mode structure. On the sample market the generator is nearly triangular (only one cycle), so a rich
metastable manifold is unlikely — which is itself a falsifiable prediction, listed as P7 in §7.

### 5.12 The observation model: where the "hidden" in HMM would have to come from

A classical HMM (Definition 2.8) needs an emission kernel `B[i][o]`. The source note fills this with "Price,
volume, sentiment". **AMF has no such quantities and, by the repository's non-trading boundary, may not
acquire them.** A compliant emission alphabet must be built from structural output the package already
produces. The natural candidate is the severity band of the diagnostic index:

```
O = { low, moderate, elevated, critical }         (Severity, from Severity.from_score)
B[s][o] = Pr( band(finding_score(s)) = o | latent structural state s )
```

With that substitution the whole of §2.2 applies unchanged: forward–backward gives the posterior over latent
structural states given a sequence of severity readings; Viterbi gives the most likely structural trajectory;
the quantum generalisation is the hidden quantum Markov model of Monras, Beige & Wiesner [51], whose Kraus
operators `{K_o}` satisfy `Σ_o K_o† K_o = I` and reduce to an HMM exactly when they are simultaneously
diagonalisable in a fixed basis. Jaeger's observable operator models [15] are the classical object sitting
strictly between the two, and are the cheapest honest generalisation available.

**But Baum–Welch needs data.** Fitting `B` or `P` to any real market would be an empirical calibration and
therefore an implicit validation claim, which the repository forbids. The compliant use of §5.12 is: (i)
*synthetic* sequences generated from a hand-specified market to teach the algorithms, and (ii) *sensitivity*
studies of how the posterior responds to structural perturbations. Neither is a forecast.

### 5.13 Determinism requirements for any implementation

Everything in §5 must produce bit-identical output on identical inputs. That constrains the implementation
sharply:

1. **Basis order is normative.** All matrices are indexed by `tuple(SystemKind)`. A dict built in insertion
   order and iterated is a determinism bug, exactly as it was for the diagnostic HHI.
2. **No eigendecomposition in the hot path.** Eigenvalue ordering is ambiguous under ties (and
   `musculature`/`metabolism` already tie on criticality), and eigenvector phase is arbitrary. Compute
   `exp(τG)` by scaling-and-squaring with a **fixed** Padé degree and a **fixed** number of squarings chosen
   from `‖τG‖_1` by a documented, deterministic rule — never by an adaptive tolerance loop [40; Higham,
   *Functions of Matrices*, Ch. 10].
3. **Fix the summation order.** Floating-point addition is not associative; sum over the canonical index
   order, in the same order, every time.
4. **Complex arithmetic must be optional, not pervasive.** With `h_st = 0` the entire §5.7 dynamics is real
   (pure exponential decay), and `ε_s` only contributes a phase that is unobservable in the diagonal. A first
   implementation should be real-valued; complex arithmetic enters only when a coherent `h_st` is introduced,
   and that step should be a separate, separately-justified change.
5. **Randomness stays behind a seed.** Any stochastic unravelling (§5.10) uses `random.Random(seed)`
   explicitly, never module-level state, and replication `i` uses `base_seed + i` to match the existing
   `ensemble` contract.

---

## 6. Repository governance and boundary analysis

Every artefact and formula the source note proposes is reproduced below and annotated. None is silently
dropped; none is silently accepted.

| Proposed artefact / formula | Conflicts with which hard rule | Compliant reformulation |
|---|---|---|
| `docs/research/markov_quantum_bridge.md` | None directly. Must **not** be added to `SHA256SUMS` (rule 4) and must carry the illustrative-only disclaimer (rule 2) | Keep, or fold into this module. If kept, place under `docs/`, add to the Markdown link-check surface, and open with the same status banner used here |
| `src/amf/quantum/lindblad_market_model.py` | **Rule 3** (a credible Lindblad solver wants numpy/scipy/QuTiP; none may be a runtime dependency). **Rule 3** again (100 % statement + branch coverage of a dense linear-algebra kernel, `mypy --strict`, determinism under float summation). **Rule 1** on the module name only if members leak market-data vocabulary | Two options. (a) *Out-of-tree sidecar*: a separate, private repository or an optional extra (`amf-research`) that may depend on numpy, is not covered by the 100 % gate, and is never imported by `src/amf`. (b) *In-tree, minimal*: `src/amf/semigroup.py` (not a `quantum/` subpackage) exposing only a real-valued `TransitionKernel` built from `CouplingMatrix`, a deterministic `exp` by fixed-degree scaling-and-squaring, and `stationary_load()`. Option (b) is what §5.1–§5.5 actually needs; option (a) is where §5.6–§5.11 belongs |
| `examples/quantum_markov_crisis_prediction.py` | **Rule 2** (the filename asserts *prediction*). **Rule 1** ("historical data" for a market means prices/returns). **Rule 3** (`tests/integration/test_examples.py` would need a case) | `examples/metastable_regimes.py`: build a market in code, form the generator of §5.5, report its spectral gap and slow-mode structure, and print the standard disclaimer. No external data, no forecasting language, deterministic output |
| `L_spread = √(bid_ask_spread)` | **Rule 1**: `bid_ask_spread` is a price quantity | `friction_i = 1 − absorptive_capacity(i)`; jump rate `γ_ij = W[i][j]·c·(1 − a_j)` as derived in §5.5 |
| `L_impact = √(market_impact)` (`amplifies for large trades`) | **Rule 1**: `trade` is on the `FORBIDDEN` substring list, and market impact is a price-response concept | `amplification_gain`, reusing the existing `cascade_gain` semantics: an impaired transmitter raises `γ_ij` by `(1 + cascade_gain)` |
| `L_delay = √(settlement_lag)` | **Rule 1** borderline (settlement lag is infrastructure, not price) but operationally a market-microstructure input AMF cannot source | `transmission_latency`: a nonnegative integer step offset on a coupling, exposed as structural metadata, not a timing measurement |
| `Observable: Price, volume, sentiment` | **Rule 1** outright (`price` is `FORBIDDEN`) | `Severity` bands over diagnostic finding scores, per §5.12 |
| `Pᵢⱼ = \|⟨ψⱼ\|U(t)\|ψᵢ⟩\|²` | Mathematically wrong (Correction B, §5.9) | `P_τ[i][j] = ⟨j\| Λ_τ(\|i⟩⟨i\|) \|j⟩` |
| `Policy intervention = negative dissipation` | Violates Theorem 2.14 (Correction A, §5.9); also risks producing scores outside `[0,1]`, which `Severity.from_score` relies on | Time-dependent nonnegative rates; reuse `Intervention` semantics |
| `Bohmian trajectories` | Wrong technique (Correction C, §5.9) | Nakajima–Zwanzig kernel or TCL, per [39] |
| "Different sectors have different dissipation rates (equities < bonds < forex)" | **Rule 2**: an empirical ordering claim with no cited evidence, presented as fact | State as falsifiable proposition P4 (§7) with the evidence that would settle it, or drop |
| "Use case: Predict probability of sudden state switches" | **Rule 2** outright | "Report the spectral gap and, where one exists, the induced slow-mode structure of a *given, hand-specified* market" |
| `src/amf/quantum/` as a package path | Rule 1 tripwire on naming: the boundary test walks public members, and terms of art such as *time-ordered exponential* and *normal ordering* contain the forbidden substring `order` | Use `chronological_product` / `canonical_arrangement`; never name a public member `time_ordered_*`. Note `CouplingMatrix.order` is the single documented `ALLOWLIST` entry and must not be joined by undocumented ones |

### 6.1 Determinism implications

The naming constraint above is not the only tripwire. The `FORBIDDEN` list is checked against **substrings**
of public names and dataclass fields, so `signal` blocks `signal_strength` (tempting for the nervous system),
`price` blocks anything `*_price_*`, `returns` blocks a field literally named `returns`, and `order` blocks
the entire time-ordering vocabulary of §2.4. Every new public name introduced by an implementation of §5 must
be checked against that list before it is added to `__all__`, and the ordering-related names above are the
ones a physicist is most likely to reach for.

Beyond naming: §5.13 items 1–5 are hard requirements, not suggestions. In particular the 100 % branch-coverage
gate means every `InvalidConfigError` path in a new `SemigroupConfig` (`tau > 0`, `padé_degree` in a fixed
set, `squarings >= 0`, `dephasing >= 0`) ships with a test in the same change, and the fix for a failing gate
is a test, never a lower threshold.

### 6.2 Dependency implications

`src/amf` has zero runtime dependencies and must keep them. A `7×7` real matrix exponential by
scaling-and-squaring is perhaps eighty lines of pure Python and is entirely feasible; a complex Lindbladian on
the `49`-dimensional Liouville space is feasible but expensive to cover to 100 % branch coverage and hard to
keep bit-reproducible. That asymmetry is the strongest technical argument for the split proposed in the table:
the *classical* content of §5.1–§5.5 goes in-tree; the *quantum* content of §5.6–§5.11 goes to an out-of-tree
research sidecar that may depend on numpy and QuTiP and is explicitly excluded from the coverage gate and from
`pyproject.toml`'s distribution surface. Note that the sidecar inherits rule 4: it is private,
all-rights-reserved, and never published to a public index.

### 6.3 Validation-claim implications

Nothing in §5 is calibrated. `τ`, `κ_j^φ`, `ε_s`, and `h_st` are free parameters chosen for mathematical
convenience. The module therefore carries the same standing disclaimer as the rest of the repository: the
constructions are illustrative, the numbers are not empirically validated, the output is not financial advice
and is not a diagnosis or forecast of any real market. Any prose that says "predicts", "detects", or
"anticipates" a real event is a rule-2 violation regardless of how the mathematics is dressed.

---

## 7. Falsifiable propositions and open questions

Each is stated so it could be refuted, with the refuting evidence named. P1–P4 restate the note's four "Key
Innovations" in falsifiable form; P5–P12 extend them.

**P1 (coherence as correlation).** *Claim (note, item 1):* off-diagonal `ρ_ij ≠ 0` gives AMF representational
capacity a diagonal model lacks. *Falsifier:* Theorem 5.7 and Proposition 5.9 already refute the strong form —
the off-diagonal block never receives amplitude, so a market lifted from a diagonal initial condition has
`ρ_ij(t) = 0` for all `t`. The claim survives only by specifying a non-diagonal *initial* structural state or
a coherent `h_st` and showing the diagonal trajectory then differs from the classical one.

**P2 (dissipation as friction).** *Claim (note, item 2):* Lindblad operators encode market friction.
*Testable form:* the rates `γ_ij = W[i][j]·c·(1 − a_j)` of §5.5 reproduce the AMF stress trajectory to
`O(τ²)` under `Λ_τ = exp(τL)`. *Falsifier:* a market and `τ` where the diagonal of `exp(τL)` differs from one
`ShockSimulator` step by more than `O(τ²)`. Directly checkable; it should be the first test written.

**P3 (non-Markovian dynamics).** *Claim (note, item 3):* markets are non-Markovian, so AMF needs memory
kernels. *Falsifier:* §5.10 shows `cascade_threshold` is nonlinear rather than memoryful and `Shock.at_step`
is an inhomogeneity. The claim reduces to *exhibit an AMF-representable structure whose reduced dynamics is
CP-indivisible*; Proposition 5.11 says the ensemble is the only current candidate. Show one, or it is
unsupported.

**P4 (rare events and tunnelling).** *Claim (note, item 4):* abrupt regime switches are "tunnelling".
*Falsifier:* Proposition 5.12 — with `h_st = 0` the rate between structurally decoupled systems is exactly
zero, not small. Absent a postulated coherent coupling the correct mechanism is metastability (Theorem 2.23),
and any implementation reporting a nonzero "tunnelling probability" where `W[i][j] = 0` is producing an
artefact.

**P5 (sub-stochasticity).** *Claim:* whenever `Σ_j W[i][j](1 − a_j) <= 1/damping − retention` for all `i`, the
step matrix is sub-stochastic and the `[0,1]` clip never activates after `t = 0`. *Falsifier:* a market
satisfying the inequality whose trajectory still hits the clip — which would indicate a bug, and is therefore
worth testing.

**P6 (absorbed fraction equals defect mass).** *Claim:* the absorbed fraction in `ResilienceScore` equals the
mass accumulated in the adjoined `⊥` state of Corollary 5.3, up to the clip. *Falsifier:* a market where the
two differ beyond floating-point noise. This is the sharpest consistency check between §5 and the existing
implementation.

**P7 (no metastable manifold in the sample market).** *Claim:* the generator `Ĝ` of §5.5 on
`examples/sample_market.json` has no spectral gap isolating slow modes, since its graph has one 3-cycle and is
otherwise acyclic. *Falsifier:* compute the spectrum and exhibit a gap — which would mean AMF's canonical
example has genuine regime structure.

**P8 (Katz and total stress coincide).** *Claim (Corollary 5.6):* `Σ_t x_t` equals the Katz series of `E` at
`α = damping`, seeded by `x_0`. *Falsifier:* a market where the two, computed to convergence, disagree beyond
tolerance.

**P9 (centrality divergence threshold).** *Claim:* `DependencyGraph.centrality` saturates or returns `NaN`
exactly when `alpha · ρ(A) >= 1` for the pair-weight adjacency `A`. *Falsifier:* a market where centrality is
well behaved above the threshold, or diverges below it. This turns an anecdotal CLAUDE.md warning into a
checkable predicate and suggests raising `InvalidConfigError` at the threshold.

**P10 (dephasing is required).** *Claim:* without an explicit dephasing channel, any pair of pure-sink systems
has infinite structural coherence time. *Falsifier:* a construction from AMF's existing metrics giving finite
`T_2` for pure sinks with no new free parameter. Absent one, `κ_j^φ` is an unvalidated knob and must be
declared as such.

**P11 (the quantum lift adds no diagnostic power).** *Claim, stated so it can lose:* for every market
expressible in AMF's JSON schema, the diagnostic index, resilience score and leverage-point ranking computed
from the diagonal of the quantum lift are identical to the classical ones. *Falsifier:* a market and a
coherent `h_st` for which they differ. This is the module's central research question, and the default
expectation is that P11 holds.

**P12 (open question: any market-side referent for coherence?).** The quantum-like literature [57, 58] argues
non-classical probability is warranted where *order effects* appear — the joint outcome depends on the
sequence of questions. AMF has a candidate: if perturbing `integrity` then `load` gave a different index from
`load` then `integrity` beyond floating-point noise, that is genuine non-commutativity *in the model*. Does
`SensitivityAnalyzer` exhibit such order-dependence, and if so is it a feature of the diagnostic algebra or an
artefact of clipping at the `[0,1]` boundaries? The second is far more likely, and separating them is a cheap
experiment.

---

## 8. Deliverables

The source note's deliverable list, reproduced exactly, with a status and compliance column.

| Deliverable (verbatim from the note) | Status | Compliance |
|---|---|---|
| `docs/research/markov_quantum_bridge.md` — Theoretical comparison | **Superseded by this module.** If retained separately, it duplicates §2 and §5 | Compliant with rules 1–4 provided it carries the illustrative-only banner and is not added to `SHA256SUMS` |
| `src/amf/quantum/lindblad_market_model.py` — Lindblad solver for market states | **Blocked as specified.** Split required | Violates rule 3 as written (dependencies, coverage, determinism). Reformulate as (a) in-tree `src/amf/semigroup.py`, real-valued, deterministic, covering §5.1–§5.5 only; plus (b) an out-of-tree private research sidecar for §5.6–§5.11 |
| `examples/quantum_markov_crisis_prediction.py` — Test on historical data | **Blocked as specified.** | Violates rule 2 (the name asserts prediction) and rule 1 ("historical data" for a market means prices/returns). Reformulate as `examples/metastable_regimes.py` over a hand-built market, with a matching case in `tests/integration/test_examples.py` |

**Additional deliverables this module proposes** (all optional, all subject to the same rules):

| Proposed | Rationale | Compliance note |
|---|---|---|
| `tests/unit/test_semigroup.py` | P2, P5, P6, P8 are all mechanical checks | Required by the 100 % gate if `semigroup.py` lands |
| `InvalidConfigError` when `alpha * spectral_radius(A) >= 1` in `centrality` | P9; turns a documented caveat into an enforced precondition | Rule 3 compliant; needs a CHANGELOG entry under *Changed* and a note that it is a behaviour change |
| `docs/discussions/Q2-quantum-markov-lindblad.md` (this file) | The theoretical record | Compliant; documentation only |

---

## 9. Research leadership and prerequisites

The note's line, reproduced exactly:

> **Research Leaders Needed**: Quantum information theorist, mathematician specializing in open quantum systems

That is the right pair for §5.6–§5.11 and the wrong pair for §5.1–§5.5, which needs neither. The skills matrix
below reflects the split.

| Role | Owns | Must be fluent in | Must be able to say no to |
|---|---|---|---|
| **Applied probabilist / Markov-chain theorist** | §5.1–§5.5, §5.12, P5–P9 | Perron–Frobenius, sub-stochastic kernels, relaxation vs. mixing times, HMM inference | "It's basically a Markov chain, so it must have a stationary distribution" (a killed chain need not) |
| **Quantum information theorist** | §5.6–§5.9, P1, P2, P11 | Choi/Kraus/Stinespring; the GKSL theorem *with its hypotheses*; Liouville-space representation | Negative rates; `U(t)` "solving" a Lindblad equation; any claim that CPTP structure alone buys predictive power |
| **Mathematician, open quantum systems** | §5.10, §5.11, P3, P4, P10 | Divisibility hierarchy [6]; Nakajima–Zwanzig and TCL; Lindbladian spectral theory and metastability [31] | "Non-Markovian" used without saying *which* definition |
| **Numerical analyst** | §5.13, §6.1–§6.2 | Matrix exponentials [40], scaling-and-squaring, floating-point reproducibility [41] | Adaptive tolerance loops in a deterministic pipeline |
| **Financial-stability economist** | §6.3, positioning against [42–46] | Network contagion models and their empirical record | Any framing that presents an uncalibrated structural score as a risk measure |
| **Repository maintainer** | Rules 1–4 throughout | The `FORBIDDEN` list, the coverage gate, the checksum-protected artefacts | Every deliverable in §8 that is marked *Blocked* until reformulated |

**Prerequisite ladder, undergraduate to research frontier.**

1. *Undergraduate year 2–3.* Linear algebra over `C`; eigenvalues; the spectral theorem for Hermitian
   matrices. Elementary probability and finite Markov chains. → M1.
2. *Undergraduate year 4.* Measure-theoretic probability and conditional expectation (M2). First graduate
   quantum mechanics: Hilbert space, observables, density operators (M7).
3. *Graduate year 1.* Discrete and continuous-time Markov chains with generators (M3). Quantum channels: Choi,
   Kraus, Stinespring (M8). HMM inference (M5). Numerical linear algebra for matrix functions (M12).
4. *Graduate year 2.* Mixing times and spectral methods (M4). Open quantum systems: the GKSL theorem and its
   microscopic derivations, including what the secular approximation discards (M9). Regime-switching
   econometrics (M6). Financial networks (M14).
5. *Graduate year 3 / research frontier.* The non-Markovianity hierarchy and its inequivalent definitions
   (M10). Metastability, escape rates, large deviations (M11). Critical reading of quantum-finance claims
   (M15).

A reader who stops after rung 3 can implement and test every claim in §5.1–§5.5 and P5–P9, which is the part
of this module with a defensible payoff. Rungs 4–5 are required to evaluate whether the rest is worth building
at all — and the honest prior, stated plainly, is that P11 holds and it is not.

---

## References

- [1] G. Lindblad, "On the generators of quantum dynamical semigroups", *Communications in Mathematical
  Physics* **48**(2), 119–130 (1976).
- [2] V. Gorini, A. Kossakowski and E. C. G. Sudarshan, "Completely positive dynamical semigroups of N-level
  systems", *Journal of Mathematical Physics* **17**(5), 821–825 (1976).
- [3] H.-P. Breuer and F. Petruccione, *The Theory of Open Quantum Systems*, Oxford University Press, 2002.
  (Ch. 3, Ch. 9.)
- [4] Á. Rivas, S. F. Huelga and M. B. Plenio, "Quantum non-Markovianity: characterization, quantification and
  detection", *Reports on Progress in Physics* **77**(9), 094001 (2014).
- [5] H.-P. Breuer, E.-M. Laine and J. Piilo, "Measure for the degree of non-Markovian behavior of quantum
  processes in open systems", *Physical Review Letters* **103**, 210401 (2009).
- [6] L. Li, M. J. W. Hall and H. M. Wiseman, "Concepts of quantum non-Markovianity: A hierarchy", *Physics
  Reports* **759**, 1–51 (2018).
- [7] R. Alicki and K. Lendi, *Quantum Dynamical Semigroups and Applications*, Springer (Lecture Notes in
  Physics).
- [8] J. R. Norris, *Markov Chains*, Cambridge University Press (Cambridge Series in Statistical and
  Probabilistic Mathematics), 1997. (Ch. 1–3.)
- [9] D. A. Levin and Y. Peres, *Markov Chains and Mixing Times*, 2nd edition, American Mathematical Society,
  2017 (with contributions by E. L. Wilmer; chapter by J. G. Propp and D. B. Wilson). (Ch. 4, 12, 13.)
- [10] L. R. Rabiner, "A tutorial on hidden Markov models and selected applications in speech recognition",
  *Proceedings of the IEEE* **77**(2), 257–286 (1989).
- [11] A. J. Viterbi, "Error bounds for convolutional codes and an asymptotically optimum decoding algorithm",
  *IEEE Transactions on Information Theory* **13**(2), 260–269 (1967).
- [12] E. Seneta, *Non-negative Matrices and Markov Chains*, Springer (Springer Series in Statistics). (Ch.
  1–2.)
- [13] O. Cappé, E. Moulines and T. Rydén, *Inference in Hidden Markov Models*, Springer (Springer Series in
  Statistics), 2005.
- [14] L. E. Baum, T. Petrie, G. Soules and N. Weiss, "A maximization technique occurring in the statistical
  analysis of probabilistic functions of Markov chains", *The Annals of Mathematical Statistics* **41**(1),
  164–171 (1970).
- [15] H. Jaeger, "Observable operator models for discrete stochastic time series", *Neural Computation*
  **12**(6), 1371–1398 (2000).
- [16] M.-D. Choi, "Completely positive linear maps on complex matrices", *Linear Algebra and its
  Applications* **10**(3), 285–290 (1975).
- [17] A. Jamiołkowski, "Linear transformations which preserve trace and positive semidefiniteness of
  operators", *Reports on Mathematical Physics* **3**(4), 275–278 (1972).
- [18] K. Kraus, *States, Effects, and Operations: Fundamental Notions of Quantum Theory*, Springer (Lecture
  Notes in Physics 190), 1983.
- [19] W. F. Stinespring, "Positive functions on C*-algebras", *Proceedings of the American Mathematical
  Society* **6**(2), 211–216 (1955).
- [20] D. Chruściński and S. Pascazio, "A brief history of the GKLS equation", *Open Systems & Information
  Dynamics* **24**(3), 1740001 (2017).
- [21] M. M. Wolf and J. I. Cirac, "Dividing quantum channels", *Communications in Mathematical Physics*
  **279**(1), 147–168 (2008).
- [22] M. M. Wolf, J. Eisert, T. S. Cubitt and J. I. Cirac, "Assessing non-Markovian quantum dynamics",
  *Physical Review Letters* **101**, 150402 (2008).
- [23] S. Luo, S. Fu and H. Song, "Quantifying non-Markovianity via correlations", *Physical Review A* **86**,
  044101 (2012).
- [24] S. Nakajima, "On quantum theory of transport phenomena: steady diffusion", *Progress of Theoretical
  Physics* **20**(6), 948–959 (1958).
- [25] R. Zwanzig, "Ensemble method in the theory of irreversibility", *The Journal of Chemical Physics*
  **33**(5), 1338–1341 (1960).
- [26] H. A. Kramers, "Brownian motion in a field of force and the diffusion model of chemical reactions",
  *Physica* **7**(4), 284–304 (1940).
- [27] P. Hänggi, P. Talkner and M. Borkovec, "Reaction-rate theory: fifty years after Kramers", *Reviews of
  Modern Physics* **62**(2), 251–341 (1990).
- [28] M. I. Freidlin and A. D. Wentzell, *Random Perturbations of Dynamical Systems*, Springer (Grundlehren
  der mathematischen Wissenschaften 260).
- [29] A. Bovier and F. den Hollander, *Metastability: A Potential-Theoretic Approach*, Springer (Grundlehren
  der mathematischen Wissenschaften 351), 2015.
- [30] H. Touchette, "The large deviation approach to statistical mechanics", *Physics Reports* **478**(1–3),
  1–69 (2009).
- [31] K. Macieszczak, M. Guţă, I. Lesanovsky and J. P. Garrahan, "Towards a theory of metastability in open
  quantum dynamics", *Physical Review Letters* **116**, 240404 (2016).
- [32] S. Coleman, "Fate of the false vacuum: semiclassical theory", *Physical Review D* **15**, 2929–2936
  (1977).
- [33] J. S. Langer, "Theory of the condensation point", *Annals of Physics* **41**(1), 108–157 (1967).
- [34] A. O. Caldeira and A. J. Leggett, "Influence of dissipation on quantum tunneling in macroscopic
  systems", *Physical Review Letters* **46**(4), 211–214 (1981).
- [35] J. D. Hamilton, "A new approach to the economic analysis of nonstationary time series and the business
  cycle", *Econometrica* **57**(2), 357–384 (1989).
- [36] J. D. Hamilton, *Time Series Analysis*, Princeton University Press, 1994. (Ch. 22.)
- [37] M. A. Nielsen and I. L. Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary
  Edition, Cambridge University Press, 2010. (Ch. 2, Ch. 8.)
- [38] Á. Rivas and S. F. Huelga, *Open Quantum Systems: An Introduction*, Springer (SpringerBriefs in
  Physics), 2012.
- [39] I. de Vega and D. Alonso, "Dynamics of non-Markovian open quantum systems", *Reviews of Modern Physics*
  **89**, 015001 (2017).
- [40] C. Moler and C. Van Loan, "Nineteen dubious ways to compute the exponential of a matrix, twenty-five
  years later", *SIAM Review* **45**(1), 3–49 (2003).
- [41] D. Goldberg, "What every computer scientist should know about floating-point arithmetic", *ACM
  Computing Surveys* **23**(1), 5–48 (1991).
- [42] L. Eisenberg and T. H. Noe, "Systemic risk in financial systems", *Management Science* **47**(2),
  236–249 (2001).
- [43] P. Gai and S. Kapadia, "Contagion in financial networks", *Proceedings of the Royal Society A*
  **466**(2120), 2401–2423 (2010).
- [44] A. G. Haldane and R. M. May, "Systemic risk in banking ecosystems", *Nature* **469**, 351–355 (2011).
- [45] D. Acemoglu, A. Ozdaglar and A. Tahbaz-Salehi, "Systemic risk and stability in financial networks",
  *American Economic Review* **105**(2), 564–608 (2015).
- [46] M. Elliott, B. Golub and M. O. Jackson, "Financial networks and contagion", *American Economic Review*
  **104**(10), 3115–3153 (2014).
- [47] M. Gallegati, S. Keen, T. Lux and P. Ormerod, "Worrying trends in econophysics", *Physica A:
  Statistical Mechanics and its Applications* **370**(1), 1–6 (2006).
- [48] D. Sornette, "Physics and financial economics (1776–2014): puzzles, Ising and agent-based models",
  *Reports on Progress in Physics* **77**(6), 062001 (2014).
- [49] S. Aaronson, "Read the fine print", *Nature Physics* **11**, 291–293 (2015).
- [50] D. Herman, C. Googin, X. Liu, A. Galda, I. Safro, Y. Sun, M. Pistoia and Y. Alexeev, "Quantum computing
  for finance", *Nature Reviews Physics* **5**, 450–465 (2023).
- [51] A. Monras, A. Beige and K. Wiesner, "Hidden quantum Markov models and non-adaptive read-out of
  many-body states", arXiv:1002.2337 (2010).
- [52] L. Accardi, A. Frigerio and J. T. Lewis, "Quantum stochastic processes", *Publications of the Research
  Institute for Mathematical Sciences* **18**(1), 97–133 (1982).
- [53] S. Gudder, "Quantum Markov chains", *Journal of Mathematical Physics* **49**(7), 072105 (2008).
- [54] E. B. Davies, *Quantum Theory of Open Systems*, Academic Press, 1976.
- [55] R. Orús, S. Mugel and E. Lizaso, "Quantum computing for finance: overview and prospects", *Reviews in
  Physics* **4**, 100028 (2019).
- [56] B. E. Baaquie, *Quantum Finance: Path Integrals and Hamiltonians for Options and Interest Rates*,
  Cambridge University Press, 2004.
- [57] J. R. Busemeyer and P. D. Bruza, *Quantum Models of Cognition and Decision*, Cambridge University
  Press, 2012.
- [58] A. Khrennikov, *Ubiquitous Quantum Structure: From Psychology to Finance*, Springer, 2010.

---

*This module is theoretical and illustrative. Its thresholds, weights, rates and scores are not empirically
validated; nothing in it is financial advice, a diagnosis, or a forecast of any real market.*
