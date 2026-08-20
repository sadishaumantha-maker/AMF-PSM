# H1: Quantum Circuits as Neural Network Components

> **Discussion category**: Research · **Labels**: `theory`, `quantum-machine-learning`, `boundary-review`, `not-validated`, `needs-reformulation`
> **Source**: `docs/QUANTUM_NEURAL_RESEARCH.md` § Discussion H1
> **Status**: Open for comment · **Nature**: Theoretical module, illustrative and not
> empirically validated

## 0. Abstract and reading guide

This module takes the source note's hybrid architecture — classical dense layer, quantum
"activation" layer, classical dense layer, trained by the parameter-shift rule — and works
out exactly what it computes when its input is an AMF market rather than market data. It
claims four things. First, that no quantum circuit implements a non-linear operation: gates
are linear by definition, and every non-linearity in such a model comes from the data
encoding and from the quadratic Born rule, never from `U` (Theorem 2.4). Second, that under
the natural encoding of AMF's metrics the quantum layer computes a *multilinear polynomial*
in those metrics, and that AMF's own `fragility` is exactly such a polynomial — so the
circuit reproduces, to within sampling error and after roughly `10^20` shots, a number that
`diagnostics.py` already computes exactly in four multiplications (Theorem 5.6, §5.9).
Third, that the note's three "Advantage Over Classical" bullets are each false, vacuous, or
backwards as stated, and each has a precise falsifiable restatement (§5.11–§5.13, §7).
Fourth, that the note's training formula is correct for a circuit expectation and wrong for
a loss, with an explicit counterexample (Corollary 2.14).

It does **not** claim that quantum machine learning is worthless, that no quantum advantage
exists anywhere, or that any construction here forecasts, diagnoses, or scores any real
market. Nothing below is financial advice.

**Prerequisite ladder.** Complex inner-product spaces and the spectral theorem → the
postulates of quantum mechanics, unitaries, observables, the Born rule ([2] Ch. 2) →
circuits, gate sets, universality ([2] Ch. 4) → density operators and quantum channels
([50] Ch. 2, [2] §8.2) → kernels and RKHS ([46], [47] Ch. 2) → parameterised circuits as
models ([7], [39] Ch. 5–6) → encoding and Fourier expressivity ([11], [12]) → gradients and
the parameter-shift rule ([3], [4], [6]) → trainability pathologies ([14], [15], [16], [17],
[18]) → the advantage question, honestly ([24], [27], [32], [51], [52]). Sections 2 and 5
assume the whole ladder; Sections 6–9 assume none of it.

---

## 1. Verbatim source specification

The following is reproduced word for word from `docs/QUANTUM_NEURAL_RESEARCH.md`, including
its notation, typography, arrows, and deliverable paths. It is quoted, not endorsed.

````markdown
### Discussion H1: Quantum Circuits as Neural Network Components
**Theme**: Use quantum circuits to compute non-linear activations in neural networks

**Motivation**:
- Classical neural networks: Sigmoid, ReLU activations are limited
- Quantum circuits: Can implement rich non-linear operations
- Hybrid: Classical processing + quantum activation functions

**Architecture**:
```
Input: x (classical data, e.g., market price)
Classical layer 1: Dense neural network
  → Output: z (feature representation)

Quantum layer:
  1. Encode z as quantum state |ψ⟩
  2. Apply quantum circuit U (non-linear operation)
  3. Measure observable O (e.g., ⟨σz⟩)
  4. Extract result as classical activation

Classical layer 2: Dense neural network
  → Final output: Forecast

Training: Use parameter shift rule (quantum analog of backprop)
  ∂L/∂θ = [L(θ + π/2) - L(θ - π/2)] / 2
```

**Advantage Over Classical**:
- Quantum activation can model "interference" (amplify good scenarios, cancel bad ones)
- Entanglement in quantum layer captures global market dependencies
- Might be harder to overfit (quantum noise acts as regularization)

**Deliverable**:
- `docs/research/quantum_neural_hybrid.md` — Architecture design
- `src/amf/quantum_ml/quantum_activation.py` — Quantum activation functions
- `src/amf/quantum_ml/variational_quantum_classifier.py` — QNN for regime classification
- `examples/quantum_nn_market_forecast.py` — Compare to classical NN

**Research Leaders Needed**: Quantum machine learning researcher
````

Note that H1, unlike Q1–Q3, carries no "Key Research Questions" heading. Its research claims
are the three **Motivation** bullets and the three **Advantage Over Classical** bullets;
those six sentences are reproduced verbatim again inside the propositions of §7, which is
where they are tested.

---

## 2. Formal foundations

Notation: `H_n = (C^2)^{tensor n}` is the state space of `n` qubits, of dimension `2^n`;
`|0>` is the all-zero computational basis state; `X, Y, Z` are the single-qubit Pauli
operators; `Z_j` means `Z` on qubit `j` and identity elsewhere; `P_S = prod_{j in S} Z_j`
for `S` a subset of qubits, with `P_{} = I`.

**Definition 2.1 (State).** A pure state is a unit vector `|psi> in H_n`, identified up to
global phase. A mixed state is a density operator `rho`, i.e. `rho >= 0` and `Tr(rho) = 1`.
Pure states are exactly the rank-one projectors `rho = |psi><psi|`. ([2] §2.1, §2.4.)

**Definition 2.2 (Gate, circuit).** A gate is a unitary `U` on `H_n` acting non-trivially on
at most two qubits. A circuit is a finite ordered product of gates. A *parameterised* gate is
a smooth family `theta -> U(theta)` of unitaries. ([2] Ch. 4.)

**Definition 2.3 (Observable, Born rule).** An observable is a Hermitian `O` on `H_n` with
spectral decomposition `O = sum_k lambda_k Pi_k`. Measuring `O` in state `rho` returns
`lambda_k` with probability `Tr(Pi_k rho)`; the expectation is `<O>_rho = Tr(O rho)`. ([2]
§2.2.)

**Theorem 2.4 (Linearity: there is no non-linear gate).** Every admissible evolution of a
quantum state is a linear map — a unitary conjugation `rho -> U rho U^dagger` in the closed
case, a completely positive trace-preserving (CPTP) linear map in general. In particular,
for any unitary `U` and any `a, b in C`,
`U(a|psi> + b|phi>) = a U|psi> + b U|phi>`, and `<U psi | U phi> = <psi | phi>`.

*Proof.* `U` is by definition a linear operator, which gives the first identity; the second
follows from `U^dagger U = I`. CPTP maps are linear on the operator space by definition. ∎

*Consequence.* The source note's line "Apply quantum circuit `U` (non-linear operation)" is a
category error, and its motivation bullet "Quantum circuits: Can implement rich non-linear
operations" is false as stated about the circuit. A parameterised-circuit model *is*
non-linear, but only in two places: (i) the encoding map `x -> |phi(x)>`, which is a
non-linear function of the classical input, and (ii) the Born rule, which is quadratic in the
amplitudes. Both are classical-side non-linearities in disguise; see [39] Ch. 5 and the
discussion in [7] §2.

**Definition 2.5 (Variational model).** Fix an encoding circuit `S(x)`, a variational circuit
`W(theta)`, and an observable `O`. The induced model is
`f_theta(x) = <0| S(x)^dagger W(theta)^dagger O W(theta) S(x) |0>`. ([7], [3], [36].)

**Definition 2.6 (Encoding strategies).** For `x in R^d`:
*basis encoding* writes a bit-string of `x` into computational-basis states (needs `d`
bits of precision per feature, exact but expensive);
*amplitude encoding* sets the `2^n` amplitudes proportional to `x` (needs `n = ceil(log2 d)`
qubits but `O(2^n)` gates in general, and destroys the norm of `x`, which must be carried
classically);
*angle encoding* applies one rotation per feature, `S(x) = tensor_j R(g(x_j))`, cost `O(d)`
gates and `d` qubits;
*data re-uploading* interleaves `L` copies of the encoding with variational blocks,
`S(x) W_1 S(x) W_2 ... ` ([12]).

**Theorem 2.7 (Fourier form of encoded models; Schuld, Sweke and Meyer [11]).** Suppose the
scalar input `x` enters only through gates `exp(-i x H_l)`, `l = 1..L`, where each `H_l` is
Hermitian with eigenvalues `lambda^{(l)}_1, ..., lambda^{(l)}_{m}`. Then for every `theta`,
`f_theta(x) = sum_{omega in Omega} c_omega(theta) exp(i omega x)`,
where `Omega` is the set of differences `Lambda_j - Lambda_k` of sums of one eigenvalue drawn
from each `H_l`. The circuit architecture fixes `Omega` (the accessible *frequencies*); the
variational parameters control only the coefficients `c_omega`, and not freely — the
achievable coefficient vectors form a constrained set.

**Corollary 2.8.** If each `H_l` is a Pauli word (eigenvalues `+/- 1`, so `exp(-i x P /2)`
contributes `+/- 1/2`) and the encoding is repeated `L` times, then
`Omega subset {-L, -L+1, ..., L}` and `f_theta` is a trigonometric polynomial of degree at
most `L` in `x`. With `L = 1`, `f_theta(x) = a + b cos(x) + c sin(x)`.

**Definition 2.9 (Quantum feature map and kernel).** `phi(x) = S(x)|0><0|S(x)^dagger` is the
*feature state*; `k(x, x') = Tr[phi(x) phi(x')] = |<0|S(x)^dagger S(x')|0>|^2` is the
*quantum kernel*. ([9], [8].)

**Proposition 2.10 (The quantum kernel is positive semidefinite).** For any finite
`x_1, ..., x_N`, the Gram matrix `K_{ij} = Tr[phi(x_i) phi(x_j)]` is symmetric PSD.

*Proof.* `Tr[A^dagger B]` is the Hilbert–Schmidt inner product on operators. Each `phi(x_i)`
is a Hermitian operator, so `K_{ij} = <phi(x_i), phi(x_j)>_HS` is a Gram matrix of real
vectors in a real inner-product space, hence PSD. ∎

**Theorem 2.11 (Moore–Aronszajn [46]).** Every symmetric positive-semidefinite kernel `k` on
a set `X` determines a unique reproducing-kernel Hilbert space `F_k` of functions on `X` with
`f(x) = <f, k(x, .)>` for all `f in F_k`.

**Theorem 2.12 (Supervised quantum models are kernel methods; Schuld [10], Schuld and
Killoran [9]).** With encoding fixed, `f_theta(x) = Tr[phi(x) O_theta]` is *linear* in the
feature `phi(x)`; hence `{f_theta}` is contained in `F_k`. Consequently, for any convex loss
and any training set, the regularised empirical-risk minimiser over all of `F_k` has the form
`sum_i alpha_i k(x_i, .)` (representer theorem, [47] §4.2), is found by convex optimisation,
and attains loss no worse than any variationally trained `f_theta`.

*Caveat, stated because it is often dropped.* The inclusion is one-way: `{f_theta}` is
generally a proper subset of `F_k`, so the kernel optimum is a *bound*, not a claim that the
two model classes coincide. Kernel methods also carry an `O(N^2)` kernel-evaluation cost in
the training-set size, each evaluation itself a sampled circuit; and [28] shows quantum
kernels can have an inductive bias so flat that they need exponentially many data points to
generalise.

**Theorem 2.13 (Parameter-shift rule; Mitarai et al. [3], Schuld et al. [4]).** Let
`U(theta) = exp(-i theta G / 2)` with `G` Hermitian, `G^2 = I` (so `G` has eigenvalues
`+/- 1`; every Pauli word qualifies). Let `A` be any observable, `|psi>` any state, and
`f(theta) = <psi| U(theta)^dagger A U(theta) |psi>`. Then, exactly and for every `theta`,

```
f'(theta) = (1/2) [ f(theta + pi/2) - f(theta - pi/2) ]
```

*Proof.* Since `G^2 = I`, `U(theta) = cos(theta/2) I - i sin(theta/2) G`. Writing
`c = cos(theta/2)`, `s = sin(theta/2)`,

```
U^dagger A U = c^2 A + s^2 G A G + i c s [G, A]
             = (1/2)(A + GAG) + (cos theta / 2)(A - GAG) + (sin theta / 2) i [G, A]
```

using `c^2 = (1 + cos theta)/2`, `s^2 = (1 - cos theta)/2`, `cs = (sin theta)/2`. Hence
`f(theta) = a0 + a1 cos(theta) + a2 sin(theta)` with `a0 = <(A + GAG)/2>`,
`a1 = <(A - GAG)/2>`, `a2 = <i[G, A]/2>` — all independent of `theta`. Then
`f'(theta) = -a1 sin(theta) + a2 cos(theta)`, while
`f(theta + pi/2) = a0 - a1 sin(theta) + a2 cos(theta)` and
`f(theta - pi/2) = a0 + a1 sin(theta) - a2 cos(theta)`; half their difference is exactly
`f'(theta)`. ∎

The identity is *exact*, not a finite difference: it is not an approximation improved by
shrinking the shift, and the shift `pi/2` is macroscopic. That is the whole point of the
rule — it is estimable on hardware with the same circuit family as `f` itself.

**Corollary 2.14 (Scope condition; the source note's formula, corrected).** Theorem 2.13
applies to `f`, the *circuit expectation*. It does **not** apply to a loss `L = l(f(theta))`
with `l` non-linear. Counterexample: take `f(theta) = cos(theta)` (achievable with `A = Z`,
`G = Y`, `|psi> = |0>`) and `l(u) = u^2`. At `theta = pi/4`,
`dL/dtheta = 2 f f' = -sin(2 theta) = -1`, whereas
`(1/2)[L(3 pi/4) - L(-pi/4)] = (1/2)[cos^2(3 pi/4) - cos^2(pi/4)] = (1/2)(1/2 - 1/2) = 0`.
The note writes `∂L/∂θ = [L(θ + π/2) - L(θ - π/2)] / 2`; the correct statement replaces `L`
by the expectation and then applies the chain rule,
`dL/dtheta = l'(f(theta)) * (1/2)[f(theta + pi/2) - f(theta - pi/2)]`. For a squared-error
loss the discrepancy is not a constant factor — it is a different function, zero where the
true gradient is largest.

**Theorem 2.15 (General shift rules; Wierichs, Izaac, Wang and Lin [6]).** If the generator
`G` has `R` distinct positive eigenvalue gaps, `f` is a trigonometric polynomial with `R`
frequencies and its derivative is recovered exactly from `2R` shifted evaluations at
prescribed points. Crooks [5] gives the complementary route: decompose a general
parameterised gate into shift-rule-differentiable factors.

**Definition 2.16 (Shot noise).** Hardware returns samples, not expectations. For an
observable with spectrum in `[-1, 1]`, the `N`-shot estimator `f_hat` satisfies
`E[f_hat] = f` and, by Hoeffding's inequality [49],
`P(|f_hat - f| >= eps) <= 2 exp(-N eps^2 / 2)`, i.e. `N >= (2 / eps^2) ln(2 / delta)` shots
suffice for accuracy `eps` with confidence `1 - delta`. The `1/eps^2` is the binding
constraint everywhere below.

**Proposition 2.17 (Sampling is never bit-deterministic).** For any finite `N`, `f_hat` is a
non-degenerate random variable unless `Var[O]_rho = 0`, i.e. unless `rho` is supported on a
single eigenspace of `O`. Hence no shot budget makes a measured model reproduce a fixed
bit-pattern; only exact state-vector evaluation does.

*Proof.* Immediate: a sum of i.i.d. non-constant bounded variables has positive variance. ∎

**Theorem 2.18 (Barren plateaus; McClean et al. [14]).** If the parameterised circuit forms a
unitary 2-design over its parameter distribution, then for every parameter `theta_k`,
`E[partial_k C] = 0` and `Var[partial_k C]` decays exponentially in the qubit count `n`.
Gradient-based training then requires exponentially many shots merely to resolve the
gradient's sign.

**Theorem 2.19 (Cost-function locality; Cerezo, Sone, Volkoff, Cincio and Coles [15]).** For
hardware-efficient ansätze, *global* cost functions (observables acting non-trivially on all
`n` qubits) exhibit barren plateaus even at depth `O(1)`, whereas *local* cost functions have
gradients vanishing at worst polynomially for depths up to `O(log n)`.

**Theorem 2.20 (Expressibility versus trainability; Holmes, Sharma, Cerezo and Coles [16]).**
The gradient variance is upper-bounded by a decreasing function of the ansatz's
expressibility, measured as the deviation of the induced unitary distribution from the Haar
2-design. More expressive ansätze are, quantifiably, flatter.

**Theorem 2.21 (Noise-induced barren plateaus; Wang et al. [17]).** Under local Pauli noise
with circuit depth growing linearly in `n`, gradient magnitudes vanish exponentially in the
depth. Unlike Theorem 2.18 this cannot be cured by initialisation strategy or by choosing a
local cost.

**Theorem 2.22 (Unification; Ragone et al. [18]).** For sufficiently deep circuits generated
by a Lie algebra `g`, the loss variance admits an exact expression in terms of `dim(g)` and
the projections of the input state and observable onto `g`, subsuming expressibility,
entanglement, locality and (for some models) noise as sources of the same phenomenon.

**Theorem 2.23 (Training is NP-hard; Bittel and Kliesch [21]).** The classical optimisation
problem underlying variational quantum algorithms is NP-hard, and remains so for systems of
only logarithmically many qubits.

**Theorem 2.24 (Classical surrogates; Schreiber, Eisert and Meyer [27]).** For a broad class
of trained quantum learning models, a classical model reproducing the input–output relation
can be extracted efficiently from the trained circuit, after which inference needs no quantum
hardware — and the surrogate can be optimised directly, so it is also a benchmark the quantum
model must beat.

**Theorem 2.25 (Generalisation from few data; Caro et al. [25]).** For a model with `T`
parameterised gates trained on `N` samples, the generalisation gap scales as
`O(sqrt(T log T / N))`; if only `K << T` gates are substantially altered by training, `T` is
replaced by `K`. **Caveat (Gil-Fuster, Eisert and Bravo-Prieto [26]).** Quantum models can
fit uniformly random labels and still generalise, so uniform-convergence bounds of this shape
do not by themselves explain observed generalisation — the same lesson the classical field
learned.

**Theorem 2.26 (Power of data; Huang et al. [24]).** Given training data, the potential
advantage of a quantum kernel over classical learners is controlled by a *geometric
difference* `g(K_C, K_Q)` between the kernel matrices. When `g` is small — the common case
for real datasets — a classical learner with access to the same data matches the quantum
model. Advantage claims therefore require exhibiting a large `g`, not merely a quantum
circuit.

**Theorem 2.27 (Dequantisation; Tang [33]).** Assuming sample-and-query access analogous to
the state-preparation assumption of quantum recommendation systems, a classical algorithm
solves the problem in time polylogarithmic in the dimension, collapsing the claimed
exponential speedup. Aaronson [32] states the general moral: the input/output assumptions do
the work.

**Proposition 2.28 (Global depolarising noise is a rescaling, not a regulariser).** Let
`D_p(rho) = (1 - p) rho + p I / 2^n`. For any traceless observable `O` (every non-identity
Pauli), `Tr[O D_p(rho)] = (1 - p) Tr[O rho]`.

*Proof.* `Tr[O D_p(rho)] = (1-p) Tr[O rho] + (p / 2^n) Tr[O] = (1-p) Tr[O rho]`. ∎

Under `L` such layers the model output — and its gradient, by linearity — is multiplied by
`(1-p)^L`. A uniform multiplicative rescaling of a model's output is exactly undone by
rescaling the next linear layer, so it imposes no capacity constraint whatsoever; what it
does impose is an exponentially worse shot cost, per Theorem 2.21.

**Lemma 2.29 (Diagonal invariance).** Let `E` be any unitary that is diagonal in the
computational basis, and let `P_S = prod_{j in S} Z_j`. Then `E^dagger P_S E = P_S`, so
`<P_S>` is unchanged by `E`.

*Proof.* `P_S` is diagonal in the computational basis; diagonal matrices commute. ∎

**Definition 2.30 (Expressibility and entangling capability; Sim, Johnson and Aspuru-Guzik
[23]).** *Expressibility* is the Kullback–Leibler divergence between the fidelity
distribution induced by sampling the ansatz's parameters and the Haar fidelity distribution;
*entangling capability* is the Meyer–Wallach measure averaged over sampled parameters. Both
are estimated by classical simulation, and both saturate with depth at ansatz-dependent
rates.

**Result 2.31 (Benchmarking, empirically; Bowles, Ahmed and Schuld [51]).** Across 12 popular
quantum models and 160 datasets, out-of-the-box classical models outperformed the quantum
classifiers overall, and *removing entanglement from the quantum model frequently left
performance unchanged or improved it*. This is the single most relevant empirical datum for
the source note's second "Advantage Over Classical" bullet.

---

## 3. Academic curriculum modules

The ladder below is the sequence a graduate student would actually take to hold an opinion
about this module. The final column is deliberately narrow: most of each course is irrelevant
to AMF, and the entry names the part that is not. Course codes are given only where verified;
where a code is uncertain the subject is named instead.

| Module | Level | Canonical course(s) | Core texts (exact units) | What AMF needs from it |
|---|---|---|---|---|
| M1. Linear algebra over `C`; spectral theorem | UG2 | **MIT 18.06** *Linear Algebra*; a second course covering the complex spectral theorem | [2] **§2.1 and Ex. 2.1–2.2**; Horn & Johnson **Ch. 1, 2, 4** | Unitarity, Hermitian spectra, tensor products — the content of Theorem 2.4 and of every derivation in §5 |
| M2. Probability and concentration | UG2 | Mathematical-probability sequences | Hoeffding [49]; Boucheron–Lugosi–Massart **Ch. 2** | Definition 2.16 and the shot-budget arithmetic of §5.9, which is the whole compliance argument |
| M3. Quantum mechanics, postulates | UG3 | **MIT 8.04/8.05** *Quantum Physics I/II*; any postulates-first QM course | [2] **Ch. 2 (§2.1 linear algebra, §2.2 postulates, §2.4 density operator, §2.5 Schmidt)** | Definitions 2.1–2.3; why a "non-linear gate" cannot exist |
| M4. Quantum computation I | PG1 | **MIT 8.370** *Quantum Information Science I* (Chuang, Shor); **Caltech Ph219/CS219** *Quantum Computation* (Preskill), first term | [2] **Ch. 4 (§4.2 single-qubit gates, §4.5 universality), Ch. 5–6**; Preskill notes [58] **Ch. 5–6** | Definition 2.2, rotation-gate algebra, the `exp(-i theta G/2)` normal form that Theorem 2.13 rests on |
| M5. Quantum computation II: channels, noise, error correction | PG1/PG2 | **MIT 8.371** *Quantum Information Science II* (Chuang, Harrow); **Caltech Ph219/CS219**, second term; **ETH Zurich** *Quantum Information Theory* | [2] **Ch. 8 (§8.2 Kraus, §8.3 examples incl. depolarising), Ch. 10**; Watrous [50] **Ch. 2, 4**; Wilde [53] **Ch. 4** | Proposition 2.28, Theorem 2.21, and an honest account of what "quantum noise" does to a model |
| M6. Statistical learning theory | PG1 | **Stanford CS229** *Machine Learning*; statistical-learning-theory sequences | Shalev-Shwartz & Ben-David **Ch. 2–6, 26**; Hastie–Tibshirani–Friedman **Ch. 7** | The meaning of "harder to overfit" (§5.13, P12), and why Theorem 2.25's caveat matters |
| M7. Kernel methods and RKHS | PG1 | Kernel-methods and advanced-ML courses | Schölkopf & Smola [47] **Ch. 2 (kernels), Ch. 4 (representer theorem)**; Shawe-Taylor & Cristianini [48] **Ch. 3**; Aronszajn [46] | Theorems 2.10–2.12; the fact that the "quantum neural network" is a linear model in disguise |
| M8. Neural networks and backpropagation | UG4/PG1 | **Stanford CS230** *Deep Learning*; **MIT 6.S191** | Goodfellow–Bengio–Courville **Ch. 6 (§6.3 activations), Ch. 7, Ch. 8** | What an "activation function" is, so that the note's claim about sigmoid/ReLU can be evaluated (P8) |
| M9. Parameterised quantum circuits as models | PG2 | Quantum-machine-learning topics courses; **Xanadu PennyLane** codebook and demos; **IBM Quantum Learning** (formerly the Qiskit textbook) chapters on variational algorithms | Schuld & Petruccione [39] **Ch. 5 (variational circuits), Ch. 6 (quantum models as kernel methods)**; Benedetti et al. [7] **§2–4**; Cerezo et al. [20] **§II–IV** | Definition 2.5 and the whole vocabulary of §5 |
| M10. Data encoding and expressivity | PG2 | Same topics courses, encoding units | [11] **§II–IV**; [12] **§2–3**; [13]; [39] **Ch. 5.1** | Theorem 2.7 and Corollary 2.8 — the result that fixes the model class before any training happens (§5.7) |
| M11. Quantum gradients | PG2 | Same courses; PennyLane's differentiation documentation | [3] **§II**; [4] **§II–III**; [6] **§2–3**; [5] | Theorem 2.13 with its hypotheses, and Corollary 2.14, which is where the source note is wrong |
| M12. Trainability: barren plateaus and their taxonomy | PG2/PG3 | Advanced QML seminars | [14]; [15]; [16]; [17]; [18]; [19] | Theorems 2.18–2.22, and the reason `n = 7` is the wrong size for the whole research programme (§5.10) |
| M13. Stochastic optimisation under shot noise | PG2 | Optimisation-for-ML plus QML seminars | [22] **§2–4**; Bottou–Curtis–Nocedal **§3–5** | Why the shot budget is an optimiser hyper-parameter, not an implementation detail |
| M14. Classical simulation of quantum circuits | PG2/PG3 | Quantum-complexity and simulation courses | [2] **§4.5.4**; Gottesman [54]; Jozsa & Linden [55]; Vidal [56] | Lemma 2.29, §5.5, and the exact cost of the `n = 7` state vector (§5.10) |
| M15. Quantum advantage, critically | PG3 | Quantum-complexity seminars; QML reading groups | [32]; [33]; [24]; [29]; [27]; [51]; [52] | The base rate for claims of the kind this module contains, and the evidence standard §7 imposes |
| M16. Quantum computing in finance, critically | PG3 | Computational-finance and quantum-finance topics courses | Herman et al. [41] **§3–5**; Egger et al. [42]; Orús et al. [43]; Montanaro [45]; Stamatopoulos et al. [44] | Where quantum methods *do* have a stated (asymptotic, fault-tolerant) case in finance — none of which is this architecture |
| M17. Floating-point determinism | PG1 | Numerical-analysis and scientific-computing courses | Higham **Ch. 1–4**; Goldberg | Why even an exact state-vector simulator must fix its summation arrangement to satisfy AMF's determinism rule (§6.2) |

Sequencing note: M1, M3, M4 and M9 suffice to read §5.1–§5.6. M10 and M11 are required for
§5.7–§5.9, which carry the compliance argument. M12 and M14 together are what turn §5.10 from
an observation into an argument — a contributor who skips them will propose scaling the qubit
count, which is precisely the move that trades simulability for untrainability. M15 is the
module whose absence produces the paper this discussion is trying not to be.

---

## 4. Exact source material

Every entry is annotated with the specific contribution AMF needs. Identifiers are given only
where confirmed.

### 4.1 Primary and seminal papers

- **Preskill [1]** — names the NISQ regime and states its limits: 50–100 qubits without error
  correction, shallow circuits, and no claim of general-purpose advantage. The correct frame
  for every sentence of the source note.
- **Mitarai, Negoro, Kitagawa and Fujii [3]** — introduces quantum circuit learning and the
  parameter-shift gradient; §II is the original derivation behind Theorem 2.13, and the paper
  is explicit that non-linearity comes from the encoding, not the gates.
- **Schuld, Bergholm, Gogolin, Izaac and Killoran [4]** — the general statement of analytic
  gradients on hardware, including the two-term rule's hypotheses and its extension by gate
  decomposition; the reference for *when* the rule applies.
- **Crooks [5]** — how to differentiate a gate whose generator does not satisfy `G^2 = I`:
  decompose it into factors that do.
- **Wierichs, Izaac, Wang and Lin [6]** — the `2R`-term generalisation (Theorem 2.15), with
  the optimal shift positions.
- **Schuld and Killoran [9]** — the feature-Hilbert-space view: encoding *is* a feature map,
  and inner products of feature states are kernels.
- **Havlíček et al. [8]** — the experimental companion: quantum kernel estimation and a
  variational classifier on superconducting hardware, with an explicitly conjectured (not
  proven) hardness of the chosen feature map.
- **Schuld [10]** — the sharpest statement of Theorem 2.12: supervised quantum models are
  kernel methods, and kernel training upper-bounds variational training on the same encoding.
- **Schuld, Sweke and Meyer [11]** — Theorem 2.7. The single most useful result for this
  module: the architecture fixes the accessible frequency spectrum before training begins.
- **Pérez-Salinas, Cervera-Lierta, Gil-Fuster and Latorre [12]** — data re-uploading; a single
  qubit with enough re-uploads is a universal classifier, which relocates "expressivity" from
  qubit count to circuit repetitions.
- **Goto, Tran and Nakajima [13]** — universal approximation for quantum-enhanced feature
  spaces: the model class is dense in `C(X)` under typical feature maps. Universality is
  therefore *not* the discriminating question (exactly as for classical networks).
- **McClean, Boixo, Smelyanskiy, Babbush and Neven [14]** — barren plateaus (Theorem 2.18).
- **Cerezo, Sone, Volkoff, Cincio and Coles [15]** — cost-function locality (Theorem 2.19).
- **Holmes, Sharma, Cerezo and Coles [16]** — expressibility bounds gradient magnitude
  (Theorem 2.20): the formal statement of the expressivity/trainability tension.
- **Wang, Fontana, Cerezo, Sharma, Sone, Cincio and Coles [17]** — noise-induced barren
  plateaus (Theorem 2.21); the direct refutation of "noise acts as regularization".
- **Ragone, Bakalov, Sauvage, Kemper, Ortiz Marrero, Larocca and Cerezo [18]** — the Lie
  algebraic theory unifying the plateau mechanisms.
- **Cerezo, Larocca, García-Martín, Díaz, Braccia, Fontana et al. [19]** — asks whether
  provable absence of barren plateaus implies classical simulability, and answers "yes and
  no" with the structure that makes both halves precise. The central reference for §5.10.
- **Bittel and Kliesch [21]** — NP-hardness of the classical optimisation (Theorem 2.23).
- **Sweke, Wilde, Meyer, Schuld, Fährmann, Meynard-Piganeau and Eisert [22]** — shot-limited
  gradient estimation *is* stochastic gradient descent, with convergence guarantees; the
  bridge between Definition 2.16 and any actual training loop.
- **Sim, Johnson and Aspuru-Guzik [23]** — expressibility and entangling capability as
  measurable descriptors (Definition 2.30).
- **Huang et al. [24]** — the geometric difference and the "power of data" (Theorem 2.26).
- **Caro et al. [25]** — generalisation bounds in terms of trainable gate count.
- **Gil-Fuster, Eisert and Bravo-Prieto [26]** — quantum models memorise random labels;
  uniform-convergence bounds do not explain their generalisation.
- **Schreiber, Eisert and Meyer [27]** — classical surrogates (Theorem 2.24).
- **Kübler, Buchholz and Schölkopf [28]** — the inductive bias of quantum kernels: a flat
  spectrum implies a large sample requirement; expressivity is not free.
- **Liu, Arunachalam and Temme [29]** — the one rigorous end-to-end supervised speedup, on a
  discrete-logarithm-based dataset engineered for the purpose. Read it to see exactly how much
  structure a provable advantage requires.
- **Abbas, Sutter, Zoufal, Lucchi, Figalli and Woerner [30]** — effective dimension and Fisher
  information as a capacity measure for quantum models.
- **Cong, Choi and Lukin [34]** — quantum convolutional networks: `O(log N)` parameters via
  a translation-invariant, hierarchical ansatz. The reference for structure-aware ansatz
  design, and the closest thing in the literature to "architecture matters".
- **Beer, Bondarenko, Farrelly, Osborne, Salzmann, Scheiermann and Wolf [35]** — a genuinely
  quantum notion of a "neuron" (a completely positive map between layers), trained on quantum
  data with a fidelity cost. Notably *not* what the source note describes.
- **Farhi and Neven [36]** — the early proposal of a variational classifier on near-term
  hardware; the direct ancestor of the note's architecture.
- **Temme, Bravyi and Gambetta [37]** — zero-noise extrapolation and probabilistic error
  cancellation, the two workhorse mitigation methods.
- **Tang [33]** — dequantisation (Theorem 2.27).
- **Gottesman [54]**, **Jozsa and Linden [55]**, **Vidal [56]** — three complementary reasons a
  quantum circuit can be classically simulable: stabiliser structure, bounded entanglement
  across every cut, and bounded Schmidt rank. Required before asserting that any 7-qubit
  circuit "does something classical hardware cannot".

### 4.2 Canonical textbooks, with the chapters that matter

- **Nielsen and Chuang [2]**, *Quantum Computation and Quantum Information*, 10th Anniversary
  Edition, Cambridge University Press, 2010. **§2.1–2.2** (postulates, Born rule) for
  Definitions 2.1–2.3; **§2.4** (density operators) and **§2.5** (Schmidt decomposition, for
  entanglement across a cut); **§4.2** (single-qubit rotations, the `exp(-i theta G/2)` form)
  and **§4.5** (universality); **§8.2–8.3** (quantum operations, the depolarising channel) for
  Proposition 2.28.
- **Schuld and Petruccione [39]**, *Machine Learning with Quantum Computers*, 2nd edition,
  Springer (Quantum Science and Technology), 2021. **Ch. 5** (variational circuits, encoding,
  gradients) and **Ch. 6** (quantum models as kernel methods) are the two chapters this module
  depends on; **Ch. 2** for the ML framing; **Ch. 4** for state preparation costs.
- **Watrous [50]**, *The Theory of Quantum Information*, Cambridge University Press, 2018.
  **Ch. 2** (states, channels, measurements) and **Ch. 4** (unital channels) for the
  channel-level statements.
- **Wilde [53]**, *Quantum Information Theory*, 2nd edition, Cambridge University Press, 2017.
  **Ch. 4** (noisy quantum theory) for the noise model vocabulary used in §5.13.
- **Schölkopf and Smola [47]**, *Learning with Kernels*, MIT Press, 2002. **Ch. 2** (kernels
  and feature spaces) and **Ch. 4** (the representer theorem) for Theorem 2.12.
- **Shawe-Taylor and Cristianini [48]**, *Kernel Methods for Pattern Analysis*, Cambridge
  University Press, 2004. **Ch. 3** for kernel construction and closure properties — the tools
  used to recognise the AMF kernel of §5.4 as a product kernel.

### 4.3 Surveys and reviews

- **Cerezo et al. [20]**, "Variational quantum algorithms", *Nature Reviews Physics*. The
  standard map of the field: ansätze, cost functions, gradients, trainability, applications.
  **§II–IV** are the relevant units.
- **Benedetti, Lloyd, Sack and Fiorentini [7]**, "Parameterized quantum circuits as machine
  learning models". Shorter, model-centric, and the best single entry point for a contributor.
- **Biamonte, Wittek, Pancotti, Rebentrost, Wiebe and Lloyd [31]**, "Quantum machine
  learning", *Nature*. The high-visibility survey; read alongside [32], which is its
  correction.
- **Cai et al. [38]**, "Quantum error mitigation", *Reviews of Modern Physics*. The honest
  accounting of mitigation's sampling overhead, which grows exponentially in circuit volume.

### 4.4 Open courseware and lecture notes

- **MIT OpenCourseWare 8.370x** *Quantum Information Science I* and **8.371x** *Quantum
  Information Science II* (Chuang; Shor; Harrow) — full lecture sequences with problem sets;
  8.370 covers postulates, protocols and algorithms, 8.371 covers error correction, fault
  tolerance and quantum information theory.
- **Caltech Ph219/CS219** *Quantum Computation* (Preskill), lecture notes [58] and recorded
  lectures — the standard graduate treatment; the chapters on quantum algorithms and quantum
  error correction are the relevant ones.
- **Xanadu PennyLane** demonstrations and codebook — the reference implementations of
  encoding, the parameter-shift rule, expressibility measurement, and barren-plateau
  experiments; PennyLane itself is documented in [40].
- **IBM Quantum Learning** (formerly the Qiskit textbook) — the variational-algorithm and
  quantum-kernel courses; useful for the measurement and transpilation mechanics that papers
  elide.

### 4.5 Domain application to finance and markets, including the skeptical literature

- **Herman, Googin, Liu, Sun, Galda, Safro, Pistoia and Alexeev [41]**, "Quantum computing for
  finance", *Nature Reviews Physics* **5**, 450–465 (2023) — the current survey; **§3–5** cover
  stochastic modelling, optimisation and machine learning respectively, and are careful about
  which results are asymptotic and fault-tolerant.
- **Egger et al. [42]**, IEEE *Transactions on Quantum Engineering* — the earlier
  problem-class survey, with explicit resource discussion.
- **Orús, Mugel and Lizaso [43]**, *Reviews in Physics* — annealing-centric; useful mainly as
  a record of what was claimed in 2019.
- **Montanaro [45]** and **Stamatopoulos et al. [44]** — the strongest concrete financial
  case: a near-quadratic speedup for Monte Carlo estimation via amplitude estimation. Note the
  shape of the claim: quadratic, asymptotic, fault-tolerant, and about *estimating an
  expectation*, not about learning.
- **Aaronson [32]**, "Read the fine print", *Nature Physics* — the standing correction to
  every exponential-speedup claim in machine learning: check the state-preparation assumption,
  the output-readout assumption, and the condition number.
- **Schuld and Killoran [52]**, "Is quantum advantage the right goal for quantum machine
  learning?", *PRX Quantum* — argues the advantage framing itself distorts the field's
  research agenda; the healthiest available prior for a module like this one.
- **Bowles, Ahmed and Schuld [51]** — the benchmark study (Result 2.31). Classical baselines
  win; removing entanglement often does not hurt. If one paper is read before writing any
  code proposed by the source note, this is it.
- **Arute et al. [57]** — the sampling-advantage demonstration, included precisely to mark the
  gap: a contrived sampling task, not a learning task on classical data.

---

## 5. Derivation for the AMF setting

This section does the arithmetic the source note gestures at. Throughout, `n` is the qubit
count, the seven systems are indexed in `SystemKind` declaration order (`skeleton`,
`circulatory`, `nervous`, `musculature`, `organs`, `immune`, `metabolism`), and every metric
lives in `[0, 1]`.

### 5.1 The AMF state and the encoding budget

A `Market` is fully described, for diagnostic purposes, by

```
m = (integrity_j, redundancy_j, criticality_j, load_j)_{j = 1..7}   in [0,1]^28
W = the 7x7 CouplingMatrix derived from the DependencyGraph        in [0,1]^{7x7}
```

`W` is *not* symmetric: `W[transmitter][receiver]` is the strength with which stress flows
from a transmitter to a receiver, and stress flows opposite to the dependency edge. Hold on
to the asymmetry; §5.12 turns on it.

The source note's "Input: `x` (classical data, e.g., market price)" has no counterpart here.
The AMF input is the 28-dimensional structural vector `m` and the coupling matrix `W`. Every
construction below therefore encodes `m`, never a price, a return, or a series.

### 5.2 Two candidate registers

**Register A (metric-per-qubit).** `n = 28`, one qubit per `(system, SystemMetric)` pair, in
declaration order of `SystemKind` and then of `SystemMetric`. Encoding depth 1, no
re-uploading needed.

**Register B (system-per-qubit).** `n = 7`, one qubit per `SystemKind`, with the four metrics
of a system entering through four successive rotations on its qubit — a four-fold data
re-upload in the sense of [12]. Register B is what the note's "Encode `z` as quantum state
`|psi>`" most plausibly means once `z` has been produced by a dense layer.

Both are angle encodings (Definition 2.6). Amplitude encoding is available in principle —
`m` has 28 components, so `n = 5` qubits suffice — but it normalises `m` away (the state is
`m / ||m||`, so all scale information must be carried classically) and costs `O(2^n)` gates
for a generic vector. Basis encoding costs one qubit per bit of metric precision; at IEEE-754
double precision that is 53 qubits per metric, which is a non-starter.

**Definition 5.1 (The AMF angle encoding).** For a metric value `x in [0, 1]` write
`u(x) = 2x - 1 in [-1, 1]` and `theta(x) = arccos(u(x)) in [0, pi]`. The encoding gate is
`R_Y(theta(x)) = exp(-i theta(x) Y / 2)`, so that

```
R_Y(theta)|0> = cos(theta/2)|0> + sin(theta/2)|1>
```

This choice is not arbitrary. It is the unique angle map (up to reflection) that makes the
`Z`-readout *affine* in the metric, which is what makes Theorem 5.6 exact rather than
approximate.

### 5.3 What one qubit reads out

**Lemma 5.2.** For the encoding of Definition 5.1,
`<Z> = cos(theta(x)) = 2x - 1` and `<X> = sin(theta(x)) = 2 sqrt(x (1 - x))`.

*Proof.* With `c = cos(theta/2)`, `s = sin(theta/2)`, the state is `c|0> + s|1>`, so
`<Z> = c^2 - s^2 = cos(theta)` and `<X> = 2 c s = sin(theta)`. Substitute `cos(theta) = u(x)`
and `sin(theta) = sqrt(1 - u(x)^2) = sqrt(1 - (2x-1)^2) = 2 sqrt(x(1-x))`. ∎

The `<X>` reading is worth noticing: `sqrt(x(1-x))` is maximised at `x = 1/2` and vanishes at
both bounds. It is a *dispersion* coordinate on the metric, not a level coordinate — a
genuinely new feature relative to anything `diagnostics.py` computes, and the only such
feature this whole construction produces (see §5.5).

**Lemma 5.3 (Product readout).** On a product-encoded register, for any subset `S` of qubits,
`<P_S> = prod_{j in S} <Z_j> = prod_{j in S} u(x_j)`.

*Proof.* The state is a tensor product and `P_S` is a tensor product of single-qubit
operators, so the expectation factorises. ∎

Lemma 5.3 is the first deflationary result: with a product encoding and a Pauli-`Z` readout
there is **no interference in the output at all**. Every quantity the circuit reports is a
product of independent single-qubit numbers.

### 5.4 The AMF quantum kernel, in closed form

**Proposition 5.4.** For the product angle encoding of Definition 5.1 on `n` metrics, the
quantum kernel of Definition 2.9 is

```
k(m, m') = prod_{j=1..n} cos^2( (theta(m_j) - theta(m'_j)) / 2 )
         = prod_{j=1..n} ( 1 + cos(theta(m_j) - theta(m'_j)) ) / 2
```

*Proof.* The overlap factorises:
`<phi(m)|phi(m')> = prod_j [ cos(t_j/2) cos(t'_j/2) + sin(t_j/2) sin(t'_j/2) ]`
`= prod_j cos((t_j - t'_j)/2)`, writing `t_j = theta(m_j)`. Square the modulus. ∎

**Corollary 5.5.** `k` is a product of one-dimensional stationary cosine kernels, computable
classically in `O(n)` floating-point operations and exactly — no sampling, no hardware. By
[47] §2.3 (closure of kernels under products) it is PSD by construction, consistent with
Proposition 2.10.

So the "quantum kernel" of the AMF feature map is a closed-form classical kernel. This is the
generic situation for product encodings and is well known ([39] Ch. 6); it becomes an
argument only when someone proposes to *estimate* it on hardware. Estimating a number one can
compute exactly is a strict loss.

### 5.5 What an entangling layer does — and what it does not

**Proposition 5.6 (Controlled-Z entanglers are invisible to `Z` readout).** Let `E` be any
product of `CZ` gates (or any unitary diagonal in the computational basis, including
`exp(-i t H)` for diagonal `H`). Then for every subset `S`,
`<phi(m)| E^dagger P_S E |phi(m)> = <phi(m)| P_S |phi(m)>`.

*Proof.* Lemma 2.29. ∎

The standard hardware-efficient template — encode, apply a `CZ` (or `CNOT`) ladder, measure
`<Z_j>` — therefore produces *exactly the numbers of Lemma 5.3*, entangler or no entangler.
The entanglement is real (the state is entangled) and the readout is unchanged. Any claim
that "entanglement in the quantum layer captures global market dependencies" must therefore
specify a readout that is not diagonal, or a rotation layer after the entangler. Result 2.31
[51] reports empirically that in practice, removing the entangler frequently costs nothing.

**Proposition 5.7 (What a `CZ` buys, exactly).** Take two qubits `i, j` product-encoded per
Definition 5.1, apply `CZ_{ij}`, and read `X_i`. Then

```
<X_i> = sin(theta_i) cos(theta_j) = 2 sqrt(m_i (1 - m_i)) * (2 m_j - 1)
```

whereas without the `CZ`, `<X_i> = sin(theta_i) = 2 sqrt(m_i (1 - m_i))`.

*Proof.* Write `a = theta_i / 2`, `b = theta_j / 2`. The pre-`CZ` amplitudes are
`(c_a c_b, c_a s_b, s_a c_b, s_a s_b)` on `(|00>, |01>, |10>, |11>)`; `CZ` flips the sign of
the last. For `X` on the first qubit,
`<X_i> = 2 Re sum_y conj(alpha_{0y}) alpha_{1y}`
`= 2 [ c_a c_b * s_a c_b + c_a s_b * (- s_a s_b) ] = 2 c_a s_a (c_b^2 - s_b^2)`
`= sin(2a) cos(2b) = sin(theta_i) cos(theta_j)`. Without the `CZ` the second term flips sign
and the bracket becomes `c_a s_a (c_b^2 + s_b^2) = c_a s_a`, giving `sin(theta_i)`. ∎

This is the honest positive result of the whole module: the entangled circuit computes the
bilinear feature `2 sqrt(m_i(1-m_i)) (2 m_j - 1)` — a dispersion-weighted, direction-signed
cross term between two metrics. It is a legitimate feature. It is also a five-operation
closed-form expression in Python, and it appears nowhere in `diagnostics.py`, which is a fact
about `diagnostics.py`, not about quantum mechanics.

### 5.6 The fragility identity

Recall `fragility_j = criticality_j * (1 - health_j) * (1 - redundancy_j)` with
`health_j = integrity_j * (1 - load_j)`.

**Theorem 5.8 (`fragility` is exactly a four-qubit Pauli-`Z` expectation).** Encode the four
metrics `(c, i, l, r) = (criticality, integrity, load, redundancy)` of one system on four
qubits by Definition 5.1. Then, writing `u_x = 2x - 1`,

```
fragility = (1/16) (1 + u_c)(1 - u_r)(3 - u_i + u_l + u_i u_l)
          = sum_{S subset {c,i,l,r}} a_S * <P_S>
```

with the sixteen coefficients

```
a_{}       =  3/16     a_{c}      =  3/16     a_{r}      = -3/16    a_{c,r}     = -3/16
a_{i}      = -1/16     a_{c,i}    = -1/16     a_{r,i}    =  1/16    a_{c,r,i}   =  1/16
a_{l}      =  1/16     a_{c,l}    =  1/16     a_{r,l}    = -1/16    a_{c,r,l}   = -1/16
a_{i,l}    =  1/16     a_{c,i,l}  =  1/16     a_{r,i,l}  = -1/16    a_{c,r,i,l} = -1/16
```

*Proof.* Substitute `c = (1+u_c)/2`, `r = (1+u_r)/2`, `i = (1+u_i)/2`, `l = (1+u_l)/2`. Then
`1 - r = (1-u_r)/2` and `health = (1+u_i)(1-u_l)/4`, so
`1 - health = [4 - (1 - u_l + u_i - u_i u_l)] / 4 = (3 - u_i + u_l + u_i u_l)/4`.
Multiplying the three factors gives the first line. Expanding
`(1 + u_c)(1 - u_r) = 1 + u_c - u_r - u_c u_r` against
`3 - u_i + u_l + u_i u_l` gives sixteen distinct monomials with the stated coefficients, and
each monomial `prod_{x in S} u_x` equals `<P_S>` by Lemma 5.3. ∎

*Check.* At `c = 1, i = 0, l = 0, r = 0`: `health = 0`, `fragility = 1`. The formula gives
`(1/16)(2)(2)(3 + 1 - 1 + 1) = (1/16)(4)(4) = 1`. At `c = 1, i = 1, l = 0, r = 0`:
`health = 1`, `fragility = 0`; the formula gives `(1/16)(2)(2)(3 - 1 - 1 - 1) = 0`.

**Corollary 5.9.** The class of functions a product-encoded, `Z`-read AMF circuit can compute
is exactly the span of multilinear monomials in the `u`-coordinates — that is, the multilinear
polynomials in the metrics. `fragility` lies in that span; so, per system, do `health` and
`absorptive_capacity` (both of degree at most 2 and 1 respectively); so does
`feedback amplification`, which is a sum over simple cycles of products of *distinct* edge
weights, hence multilinear in the edge weights.

**Corollary 5.10 (What does not lie in the span).** `concentration` is a
Herfindahl–Hirschman index over outgoing shares, `sum_k (w_k / sum_k' w_k')^2` — a *ratio*,
not a polynomial, in the weights. The report's `overall_index` is likewise a ratio, the
criticality-weighted mean `sum_j c_j s_j / sum_j c_j`. `Severity.from_score` is a step
function with three thresholds, so it is not exactly representable by any finite
trigonometric polynomial. A quantum readout supplies no division and no discontinuity; all
three require classical post-processing, exactly as they do today.

### 5.7 Fourier-degree accounting

By Corollary 2.8, one Pauli-rotation encoding of a variable gives trigonometric degree 1 in
that variable; `L` re-uploads give degree `L`. Under Definition 5.1 the diagnostic targets
need degree **1**: they are affine in `cos(theta)` per variable, and Theorem 5.8 exhibits the
exact coefficients. AMF's diagnostic functions therefore sit at the very bottom of the
expressivity hierarchy that [11] and [12] construct. Data re-uploading, deep ansätze,
expressibility tuning in the sense of [23] — none of it is needed, and by Theorem 2.20 all of
it costs trainability.

The degree-4 term `a_{c,i,l,r} <Z_c Z_i Z_l Z_r> = -(1/16) <Z_c Z_i Z_l Z_r>` deserves a note.
It is a *global* observable on the four-qubit subregister, exactly the class Theorem 2.19
[15] identifies as inducing barren plateaus at `O(1)` depth. AMF's own target function
therefore requires the observable that is worst for training, and the local-observable
prescription that fixes trainability cannot reach it without the classical recombination the
theorem was trying to avoid.

### 5.8 The diagnostic index is already a Born expectation

Write `p_j = c_j / sum_k c_k` and let `rho = diag(p_1, ..., p_7)` and `S = diag(s_1, ..., s_7)`
where `s_j` is the per-system weakness score. Then

```
DiagnosticReport.overall_index = sum_j p_j s_j = Tr(rho S)
```

which is a Born-rule expectation of a diagonal observable in a diagonal state. This is the
same observation module Q1 makes about superposition, restated for the diagnostic index: the
formalism embeds, and it embeds trivially, because everything commutes. Off-diagonal
structure — the only place quantum mechanics differs from probability — has no referent in
`diagnostics.py`, and introducing it would break the commutation that makes the pipeline
deterministic.

### 5.9 The shot budget versus the determinism rule

Fix the accuracy `eps` of a reconstruction of `fragility` from Theorem 5.8. The identity term
`a_{}` is exact; the other fifteen are estimated. By the triangle inequality it suffices to
estimate each `<P_S>` to within `t` where `t * sum_{S nonempty} |a_S| <= eps`. From the
coefficient table, `sum_S |a_S| = (1/16) * 4 * 6 = 3/2`, so the non-identity mass is
`3/2 - 3/16 = 21/16 = 1.3125` and `t = eps / 1.3125`.

Hoeffding (Definition 2.16) with a union bound over the fifteen terms at total failure
probability `delta` gives, per term,

```
N >= (2 / t^2) ln(30 / delta) = 2 (1.3125 / eps)^2 ln(30 / delta) ~= 3.45 ln(30/delta) / eps^2
```

At `eps = 1e-9` and `delta = 1e-3`, `ln(30000) ~= 10.31`, so `N ~= 3.6e19` shots per term and
`~5e20` shots in total for one system's `fragility` — and there are seven systems. At an
optimistic `1e5` shots per second that is `~5e15` seconds, of order `1.7e8` years, to
reproduce a number that

```python
criticality * (1.0 - integrity * (1.0 - load)) * (1.0 - redundancy)
```

computes exactly in three multiplications and two subtractions.

The determinism rule is stricter still. AMF requires **bit-identical** output for identical
input; a double-precision `fragility` carries about `1e-16` of resolution. By Proposition 2.17
no finite shot budget delivers a fixed bit-pattern at all: a sampled estimator is a random
variable for every `N`. The gap is not quantitative, it is categorical. Only exact
state-vector evaluation — that is, classical simulation — can satisfy rule 3, and an exactly
simulated circuit is a classical function evaluation with extra steps.

### 5.10 Trainability and simulability at `n = 7`

At `n = 7` the state vector has `2^7 = 128` complex amplitudes. A single-qubit gate updates
all of them in `128` complex multiply–adds; a depth-`d` circuit with seven gates per layer
costs `~900 d` complex operations. For `d = 20` that is under `2e4` operations — microseconds
in pure Python, with no runtime dependency. Register A (`n = 28`) has `2^28 ~= 2.7e8`
amplitudes, which is `~4` GB in double-precision complex and no longer stdlib-feasible.

This produces the module's central structural tension, and it is not specific to AMF:

- At `n = 7` (Register B) the circuit is exactly simulable in microseconds, so the quantum
  hardware contributes nothing that a `for` loop does not.
- At `n = 28` (Register A) exact simulation is out of reach for a stdlib package, and the
  barren-plateau results ([14], [15], [16], [17], [18]) begin to bite: a hardware-efficient
  ansatz approaching a 2-design has gradient variance decaying exponentially in `n`, and the
  degree-4 observable of §5.7 is precisely the global kind of Theorem 2.19.

Cerezo, Larocca et al. [19] state the general form of this tension directly: the structural
conditions under which one can *prove* absence of barren plateaus are, in a broad class of
cases, the same conditions that permit efficient classical simulation of the loss. AMF sits
on the simulable side of that line by construction, because `SystemKind` has seven members and
the framework fixes that number.

### 5.11 "Quantum activation can model 'interference'"

To make the claim testable one must supply three things:
(a) an injection from market scenarios to computational-basis states `z`;
(b) a predicate separating "good" from "bad" scenarios;
(c) a circuit whose amplitudes carry a sign structure making the bad-scenario amplitudes
cancel.

(a) and (b) are modelling choices AMF has not made — the framework has no scenario space; it
has a stress trajectory `x_t in [0,1]^7` and a `SimulationTrace`. (c) is the entire design
problem of quantum algorithms, and in every known case where it succeeds (amplitude
amplification, the quantum Fourier transform, amplitude estimation as used by [44], [45]) the
sign structure comes from a *known* oracle or a *known* algebraic identity, never from a
trained variational ansatz. Under the natural AMF encoding there is no interference in the
readout at all (Lemma 5.3). The falsifiable restatement is P10 in §7.

### 5.12 "Entanglement captures global market dependencies"

The natural implementation is `H_W = sum_{i != j} W[i][j] Z_i Z_j` with the entangler
`exp(-i t H_W)`. Two obstructions, both structural.

**Obstruction 1 (Hermiticity destroys direction).** `Z_i Z_j = Z_j Z_i`, so the operator
depends only on `W[i][j] + W[j][i]`. Any two-body `ZZ` Hamiltonian encodes only the
*symmetric part* of the coupling. AMF's coupling is directed — that is its entire content,
and `graph.py` goes to some trouble to keep `(source, target, kind)` distinct. The map
`W -> H_W` is therefore not injective, and it discards exactly the information the
`DependencyGraph` exists to carry. Encoding a directed generator requires non-Hermitian
dynamics, i.e. the Lindblad route of module Q2, not a circuit.

**Obstruction 2 (diagonality makes it invisible).** `H_W` is diagonal, so by Lemma 2.29 and
Proposition 5.6 the entangler leaves every `Z`-basis expectation unchanged. It becomes visible
only after a basis-changing layer — at which point the model is a transverse-field Ising
model on seven sites, whose full spectrum is a `128 x 128` eigenproblem.

The compliant restatement: AMF already transmits stress through `W` in `ShockSimulator`,
directionally, deterministically, and with an explicit absorptive gate. That is a *model of
transmission*, not a validated claim about contagion, and it does not become one by being
unitary.

### 5.13 "Might be harder to overfit (quantum noise acts as regularization)"

**Global depolarising noise.** By Proposition 2.28 the entire model output — and its
gradient — is multiplied by `(1-p)^L`. A uniform rescaling of a layer's output is exactly
undone by the next dense layer's weights, so it imposes no capacity constraint of any kind. It
does divide the per-shot signal-to-noise ratio by `(1-p)^L`, multiplying the shot budget of
§5.9 by `(1-p)^{-2L}`.

**Local Pauli noise.** Here the story is more interesting and deserves a concession. Under
per-qubit depolarising noise with parameter `q` applied `L` times, the Pauli coefficient of a
weight-`|S|` term is damped by `(1-q)^{|S| L}`. That *is* a shrinkage — a fixed low-pass
filter on the Pauli spectrum that penalises high-weight (highly correlated) terms more than
low-weight ones, which is structurally analogous to a smoothness prior. Three reasons it does
not support the note's bullet:

1. It is not tunable. The shrinkage constant is a hardware calibration figure, not a
   hyper-parameter; changing it means changing device, and it drifts between calibrations —
   which is by itself a violation of rule 3.
2. It kills the terms AMF needs. The degree-4 coefficient `a_{c,i,l,r}` of Theorem 5.8 is
   damped by `(1-q)^{4L}`, the hardest of the sixteen, so the noise preferentially destroys
   the exact structure of the target function.
3. Theorem 2.21 [17] shows the same mechanism drives gradients to zero exponentially in
   depth, and unlike Theorem 2.18 this is not curable by initialisation. Noise is not a free
   regulariser; it is a trainability failure with a regulariser-shaped side effect.

If shrinkage of high-order interaction terms is genuinely wanted in AMF, the compliant version
is a *declared* multiplicative constant on the high-weight coefficients of Theorem 5.8, set in
a validated `DiagnosticConfig`-style dataclass, deterministic and documented — not sampled
from a device.

### 5.14 Gradient budgets, compared

| Quantity | Method | Circuit or function evaluations | Exact? | Deterministic? |
|---|---|---|---|---|
| `d(index)/d(metric)` for all 28 metric–system pairs | `SensitivityAnalyzer` at `step = 0.05` | 56 re-diagnoses (`baseline +/- step`), each `O(systems + edges + cycles)` | Yes, as a finite difference over the span actually explored | Yes, no seed involved |
| `d f_theta / d theta_k` for all `k` | parameter shift (Theorem 2.13) | `2 |theta|` circuits, each `N` shots | Exact in expectation; estimator is stochastic | No (Proposition 2.17) |

For Register B with a depth-`d` hardware-efficient ansatz, `|theta| ~= 3 n d = 21 d`; at
`d = 20` that is 420 parameters and 840 circuits per gradient step, each needing the shot
budget of §5.9 to be meaningful. `SensitivityAnalyzer` returns its 28 gradients and its ranked
`LeveragePoint`s in 56 exact evaluations, and the `span` it reports is the honest statement of
what a one-sided difference near a bound actually measured. The comparison is not close, and
it is not close by a factor that better engineering could recover.

### 5.15 The regime classifier has no labels

`variational_quantum_classifier.py` — "QNN for regime classification" — needs pairs
`(m, y)`. AMF has exactly one categorical output: `Severity`, obtained from a score by three
fixed thresholds (`0.25`, `0.50`, `0.75`), and `ResilienceScore.tipped_systems`, obtained by
comparing a stress value to `cascade_threshold`. Both are *deterministic total functions of
inputs already in hand*.

**Proposition 5.11.** For labels defined as `y = Severity.from_score(score(m))`, the Bayes
error of the classification problem is zero, the labelling function is known in closed form,
and any trained classifier with accuracy below 100% is strictly dominated by evaluating the
function. There is no generalisation question, because there is no noise and no unobserved
variable.

*Proof.* `score` and `Severity.from_score` are total deterministic functions of `m`; their
composition is the labelling function; a lookup of a known function has zero risk. ∎

What remains is function approximation of a piecewise-constant map — the case Corollary 5.10
notes is not exactly representable by any finite trigonometric polynomial. The exercise
therefore learns a smoothed version of a step function AMF already computes exactly, and
reports the smoothing error as "accuracy".

### 5.16 The classical surrogate of the entire architecture

Instantiate Theorem 2.24 [27] at AMF's size. For Register B with the product encoding of
Definition 5.1 and any `Z`-basis readout, Lemma 5.3 and Corollary 5.9 give

```
f_theta(m) = sum_{S subset {1..7}} b_S(theta) prod_{j in S} u(m_j)
```

a linear model over at most `2^7 = 128` explicit features. Allowing non-diagonal readout
(Proposition 5.7) extends the feature set to at most `4^7 = 16384` Pauli monomials in
`{1, u_j, sqrt-dispersion terms}`. Either way the surrogate is written down in closed form,
fitted by ordinary least squares, evaluated in at most a few thousand multiply–adds, is
exactly deterministic, and needs no hardware and no dependency. It is also, per [27], the
benchmark the quantum model must beat — and it *is* the quantum model, evaluated exactly.

### 5.17 Translation table

| Source-note element | What it becomes in AMF | Already in the repository? |
|---|---|---|
| `Input: x (classical data, e.g., market price)` | `m in [0,1]^28`, the structural metric vector | Yes: `Market`, `AnatomicalSystem` |
| `Classical layer 1: Dense neural network -> z` | any deterministic feature map of `m` | `health()`, `absorptive_capacity()` are two such maps |
| `Encode z as quantum state` | Definition 5.1, `R_Y(arccos(2x-1))` | No — and Lemma 5.2 shows what it would add |
| `Apply quantum circuit U (non-linear operation)` | a linear map (Theorem 2.4); the non-linearity is in the encoding and the Born rule | n/a |
| `Measure observable O (e.g. <sigma_z>)` | `<P_S> = prod u(m_j)` (Lemma 5.3) | Yes, implicitly: Theorem 5.8 says `fragility` *is* such a combination |
| entangling layer | invisible under `Z` readout (Prop. 5.6); a dispersion cross-term under `X` readout (Prop. 5.7) | Cross-terms: no. Directed coupling: yes, `CouplingMatrix` |
| `Classical layer 2 -> Final output: Forecast` | `DiagnosticReport`, `ResilienceScore`, `SensitivityReport` — none of them forecasts | Yes |
| `Training: parameter shift rule` | not applicable: there is no fitting target (Prop. 5.11) | `SensitivityAnalyzer` computes exact gradients without one |

---

## 6. Repository governance and boundary analysis

Every artefact, formula and phrase the source note proposes is reproduced below and
annotated. Nothing is silently dropped and nothing is silently accepted.

| Proposed artefact / formula / phrase | Conflicts with which hard rule | Compliant reformulation |
|---|---|---|
| `docs/research/quantum_neural_hybrid.md` — Architecture design | None directly. Must **not** be added to `SHA256SUMS` (rule 4) and must carry the illustrative-only banner (rule 2) | Keep, or fold into this module — §5 *is* the architecture design, with the arithmetic done. If kept separately, place it under `docs/`, ensure the `validate` job's Markdown link check reaches it, and open with the status banner used here |
| `src/amf/quantum_ml/quantum_activation.py` — Quantum activation functions | **Rule 3** three ways: `quantum_ml/` is a sub-package where the package is flat modules; a hardware backend (PennyLane, Qiskit) is a large dependency tree; a sampled activation cannot reach 100% deterministic branch coverage. **Rule 2** in "activation functions", which presupposes a network AMF does not have | Ship `src/amf/multilinear.py`: pure-`math`, exact, deterministic. `pauli_expansion(system) -> dict[frozenset[SystemMetric], float]` returning the sixteen coefficients of Theorem 5.8, and `evaluate_expansion(coefficients, system) -> float` reconstructing `fragility` from them. Zero dependency, three branches, exactly testable against `diagnostics.fragility` |
| `src/amf/quantum_ml/variational_quantum_classifier.py` — QNN for regime classification | **Rule 3** (sub-package, dependency, coverage, and a stochastic optimiser). **Rule 2** outright: "regime classification" asserts a capability. Proposition 5.11: the only available labels are a known deterministic function, so the Bayes error is zero | Nothing to ship. `Severity.from_score` already *is* the classifier, exactly, in four comparisons. If a *smoothed* severity is genuinely wanted, add a documented, validated `SeverityBlendConfig` with declared thresholds — deterministic, in-tree, no training |
| `examples/quantum_nn_market_forecast.py` — Compare to classical NN | **Rule 1** twice (`market_forecast` implies price/return input; the file name itself would need checking against `FORBIDDEN` if it ever became a public name). **Rule 2** outright: forecasting is a validated-performance claim. **Rule 3**: `tests/integration/test_examples.py` needs a deterministic, dependency-free case | `examples/multilinear_readout.py`: build the sample market in code, print the sixteen coefficients of Theorem 5.8 for each system, verify the reconstruction equals `fragility` to the last bit, print the `<X>` dispersion coordinate of Lemma 5.2 and the cross-term of Proposition 5.7, then the standard disclaimer. Deterministic, stdlib-only; add a case to `test_examples.py` |
| `src/amf/quantum_ml/` as a sub-package | **Rule 3** (the package is flat modules) plus a rule-1 tripwire on member names | Flat modules only. See the naming table below |
| `Input: x (classical data, e.g., market price)` | **Rule 1** outright — `price` is in `FORBIDDEN`, and price is not a thing AMF models | `m in [0,1]^28` (§5.1). The `MarketBoundary` records `asset_class`, `geography`, `timeframe`; nothing else about the instrument enters |
| `Apply quantum circuit U (non-linear operation)` | Not a rule conflict — a mathematical error | Theorem 2.4: `U` is linear by definition. Restate as: the non-linearity is the encoding `x -> \|phi(x)>` and the quadratic Born rule |
| `Measure observable O (e.g., ⟨σz⟩)` / `Extract result as classical activation` | **Rule 3**: measurement is sampling, and sampling is never bit-deterministic (Prop. 2.17) | Exact expectation, computed classically: Lemma 5.3 gives `prod u(m_j)` in closed form |
| `Classical layer 2 → Final output: Forecast` | **Rule 2** outright, and **rule 1** exposure in any member named `forecast_returns`, `price_head`, … | `DiagnosticReport`, `ResilienceScore`, `ResilienceDistribution`, `SensitivityReport`. None claims to forecast, and none may be described as doing so |
| `∂L/∂θ = [L(θ + π/2) - L(θ - π/2)] / 2` | Not a rule conflict — a scope error | Corollary 2.14: the identity holds for the circuit expectation, not for a composed non-linear loss. Counterexample given. The correct form applies the chain rule |
| `Quantum activation can model "interference" (amplify good scenarios, cancel bad ones)` | **Rule 2**: asserts a capability with no stated mechanism | §5.11 and P10. Under the natural AMF encoding there is no interference in the readout at all (Lemma 5.3) |
| `Entanglement in quantum layer captures global market dependencies` | **Rule 2**: asserts a validated capability | §5.12: `ZZ` couplings encode only the symmetric part of `W`, discarding the direction the `DependencyGraph` exists to record; and a diagonal entangler is invisible to `Z` readout (Prop. 5.6). Restate as P11 |
| `Might be harder to overfit (quantum noise acts as regularization)` | **Rule 2** (a generalisation claim) and **rule 3** (device noise is unseedable and drifts) | §5.13: global depolarising noise is a rescaling the next dense layer undoes exactly (Prop. 2.28); local noise shrinks precisely the high-weight terms `fragility` needs; and [17] shows the same mechanism kills gradients. Restate as P12 |
| `Classical neural networks: Sigmoid, ReLU activations are limited` | **Rule 2** exposure: "limited" relative to an unstated task | P8. Classical networks with any non-polynomial activation are universal approximators; the binding constraint in AMF is the absence of a fitting target, not the activation |
| `Research Leaders Needed: Quantum machine learning researcher` | **Rule 2** exposure: the field's default register is advantage claims | See §9. Necessary, not sufficient; three further roles are named there |

### 6.1 Determinism

Rule 3 requires bit-identical output for identical input, with randomness only behind an
explicit seed. Three distinct failures arise here, of increasing severity. (i) *Sampling*:
Proposition 2.17 — no shot budget yields a fixed bit-pattern. (ii) *Hardware drift*: a device's
noise parameters change between calibrations, so even the *distribution* is not fixed. (iii)
*Summation arrangement*: even an exact state-vector simulator must fix the arrangement in
which it accumulates amplitudes, because floating-point addition is not associative — the same
reason `Market.assemble` stores systems in `SystemKind` declaration order. Only (iii) is
fixable, and fixing it means the artefact is a deterministic classical function, which is what
`multilinear.py` would be.

### 6.2 Dependencies

`amf` has zero runtime dependencies. PennyLane [40] and Qiskit both pull large scientific
stacks. A pure-stdlib 7-qubit state-vector simulator using Python's built-in `complex` is
genuinely feasible — §5.10 puts a depth-20 circuit at under `2e4` complex operations — but it
would be a *simulator*, not a quantum computation, and by Corollary 5.9 the function it
computes is a multilinear polynomial that `multilinear.py` computes directly. Adding 400 lines
of simulator to compute a polynomial is not a defensible trade.

### 6.3 Coverage

The gate is 100% statement **and** branch coverage of `src/amf`. Every branch of a sampler,
every mitigation fallback, every convergence-failure path in a variational optimiser would
need a deterministic test. `multilinear.py` has a handful of branches and an exact oracle to
test against (`diagnostics.fragility`), which is the whole reason to prefer it.

### 6.4 Naming tripwires specific to this module

`tests/unit/test_non_trading_boundary.py` walks public names *and* members *and* dataclass
fields, matching `FORBIDDEN` as a **substring**. Quantum vocabulary is unusually dangerous:

| Natural name | Fails on | Use instead |
|---|---|---|
| `qubit_order`, `gate_order`, `measurement_order`, `pauli_ordering` | `order` | `qubit_index`, `gate_arrangement`, `readout_arrangement`, `_PAULI_ARRANGEMENT` |
| `disorder`, `disordered_hamiltonian` | `order` (substring of *dis-order*) | `inhomogeneity`, `inhomogeneous_generator` |
| `readout_signal`, `signal_to_noise` | `signal` | `readout`, `readout_to_noise_balance` |
| `expressibility_trainability_tradeoff` | `trade` (substring of *trade*off) | `expressibility_trainability_balance` |
| `returns_expectation`, `circuit_returns` | `returns` | `expectation`, `circuit_value` |
| `price_encoding`, `input_prices` | `price` | `metric_encoding`, `structural_inputs` |
| `backtest_ansatz` | `backtest` | not admissible in any form (rules 1 and 2) |

`CouplingMatrix.order` is the one documented `ALLOWLIST` exception and must stay the only one;
a meta-test asserts every allowlist entry still exists, so adding a second is a deliberate act
that must be argued for, not a convenience.

### 6.5 Validation-claim hygiene

Rule 2 forbids claims of predictive power or validated performance. This field's default
register violates it constantly: "advantage", "outperforms", "captures", "harder to overfit",
"quantum-enhanced". [52] argues the advantage framing distorts the research agenda even inside
the field; [51] supplies the empirical base rate. Any text added to this repository from this
literature must be rewritten in the conditional and attached to a falsifiable proposition in
§7 — the discipline the rest of the repository already applies to its own scores.

### 6.6 The out-of-tree sidecar

The three code deliverables have a legitimate home: a separate, private repository —
`amf-quantum-lab` — with its own CI, its own dependency set (PennyLane, NumPy), its own
`Private :: Do Not Upload` classifier, and no coverage or determinism coupling to `amf`. It
must not be a Release asset or an Actions artifact of the public repository (`RELEASING.md`),
and it must not import from `amf` in a way that creates a reverse dependency. What it may do
is *consume* `amf`'s public API: build markets, read metrics, and compare its circuit output
against `multilinear.py`'s exact answer. That comparison is the only experiment in the note
that would produce information.

---

## 7. Falsifiable propositions and open questions

Each proposition is stated so that it could be refuted, and each names the evidence that would
refute it. P8–P13 restate the source note's six research claims verbatim before testing them.

**P1 (Exact identity).** For every `AnatomicalSystem`, `fragility` equals the sixteen-term
Pauli expansion of Theorem 5.8 exactly. *Refuted by* one system whose reconstruction differs
from `diagnostics.fragility` by more than double-precision rounding. A unit test settles it.

**P2 (Kernel closed form).** The AMF quantum kernel is `prod_j cos^2((theta_j - theta'_j)/2)`
(Proposition 5.4) and is computable classically in `O(n)` operations. *Refuted by* an encoding
in `src/amf` for which the kernel is not a product of one-dimensional factors — which would
require a non-product encoding, i.e. an entangling encoder.

**P3 (Entangler invisibility).** Adding any computational-basis-diagonal entangler leaves every
`Z`-basis expectation unchanged (Proposition 5.6). *Refuted by* exhibiting a diagonal `E` and a
`P_S` with `E^dagger P_S E != P_S`. This is a theorem, so refutation means an error in it.

**P4 (Direction loss).** No two-body `ZZ` Hamiltonian distinguishes `W[i][j]` from `W[j][i]`
(§5.12). *Refuted by* a Hermitian two-body construction that is injective on directed weight
matrices — which would have to use non-commuting operators and would no longer be diagonal.

**P5 (Determinism impossibility).** No finite shot budget yields bit-identical output
(Proposition 2.17). *Refuted by* a measurement scheme whose output has zero variance for a
state that is not an eigenstate of the measured observable.

**P6 (Budget).** Reconstructing one system's `fragility` to `1e-9` with 99.9% confidence needs
of order `5e20` shots (§5.9). *Refuted by* an estimator with better than `1/eps^2` scaling for
this quantity — note that quadratic amplitude-estimation speedups ([45], [44]) would reduce the
exponent, at the cost of requiring fault-tolerant coherent access to the whole pipeline.

**P7 (Simulability window).** At `n = 7` the circuit is exactly simulable in microseconds and
barren plateaus are irrelevant; at `n = 28` simulation is out of stdlib reach and the plateau
results apply. There is no `n` at which AMF gets an untrainable-but-useful circuit. *Refuted
by* an ansatz on `7 <= n <= 28` qubits that provably resists classical simulation of its loss
*and* provably trains — the open question [19] frames.

**P8** — the note claims: *"Classical neural networks: Sigmoid, ReLU activations are limited"*.
Restated: the binding constraint on modelling AMF is the activation function. *Refuted by* the
observation that networks with any non-polynomial activation are universal approximators, and
by Proposition 5.11: AMF's obstacle is the absence of a fitting target, not the non-linearity.
*Would be supported by* a stated AMF task, with a stated generator, on which a ReLU network is
provably worse than an alternative.

**P9** — the note claims: *"Quantum circuits: Can implement rich non-linear operations"*.
Restated: a quantum circuit implements a non-linear map on states. *Refuted by* Theorem 2.4.
The salvageable version — the encoding and the Born rule together give a non-linear function of
the classical input — is true, and gives exactly the multilinear class of Corollary 5.9.

**P10** — the note claims: *"Quantum activation can model 'interference' (amplify good
scenarios, cancel bad ones)"*. Restated: there exists an encoding of AMF market scenarios into
basis states and a circuit whose amplitude signs suppress a stated class of scenarios.
*Refuted, as currently specified,* by Lemma 5.3: with product encoding and `Z` readout there
are no cross terms. *Would be supported by* exhibiting the injection, the predicate, and the
circuit — all three, explicitly.

**P11** — the note claims: *"Entanglement in quantum layer captures global market
dependencies"*. Restated: an entangled circuit represents AMF's dependency structure more
faithfully than `CouplingMatrix` does. *Refuted by* P3 and P4 together for the natural
construction, and by [51]'s empirical finding that removing entanglement often costs nothing.
*Would be supported by* a specific structural query — a feedback loop, an articulation point,
a centrality ranking — computed correctly by the circuit and not by `graph.py`.

**P12** — the note claims: *"Might be harder to overfit (quantum noise acts as
regularization)"*. Restated: device noise improves generalisation. *Refuted, for global
depolarising noise,* by Proposition 2.28: it is a rescaling that the next dense layer undoes.
*Partially supported, for local Pauli noise,* as a fixed non-tunable shrinkage of high-weight
Pauli coefficients — which §5.13 shows preferentially destroys the terms `fragility` needs, and
which [17] shows costs trainability exponentially. A decisive test would compare a noisy
device against the same circuit simulated exactly with an explicit, tunable shrinkage
constant; if the device never wins, the bullet is empty.

**P13** — the note's training formula. Restated: `[L(θ + π/2) - L(θ - π/2)] / 2` equals
`∂L/∂θ`. *Refuted by* the counterexample of Corollary 2.14. Correct for `L` replaced by the
circuit expectation, and only when the generator satisfies `G^2 = I`.

**P14 (Surrogate dominance).** Any Register-B model is exactly representable as a linear model
over at most 128 explicit multilinear features (§5.16), fitted by least squares. *Refuted by* a
Register-B readout whose function is not in that span — which requires a non-product encoding.

**P15 (No supervised target).** AMF admits no supervised objective that is not a known
deterministic function of its own inputs (Proposition 5.11). *Refuted by* naming an AMF
quantity that is (i) observed, (ii) not computed from `m` and `W`, and (iii) inside the
non-trading boundary. This is the proposition that, if refuted, unlocks most of the source
note — and it is the one nobody has refuted for any module in this series.

**Open questions.** (Q-a) Does the `<X>` dispersion coordinate `2 sqrt(m(1-m))` of Lemma 5.2,
or the cross term of Proposition 5.7, improve any *stated* structural diagnosis — and can that
be tested without a fitting target, e.g. by comparing rankings against an explicit generator?
(Q-b) Is there an AMF-relevant structural quantity whose classical evaluation is
super-polynomial in the number of systems, so that a larger `SystemKind` would matter? Cycle
enumeration is the only candidate, and seven is not large. (Q-c) Where exactly does the
simulability/trainability boundary of [19] fall for the specific ansatz class AMF would use?

---

## 8. Deliverables

The source note's deliverable list, reproduced exactly as written, with compliance status.

| Deliverable (verbatim) | Status | Compliance note |
|---|---|---|
| `docs/research/quantum_neural_hybrid.md` — Architecture design | **Accept with conditions** | Not to be added to `SHA256SUMS`; must carry the illustrative-only banner; must be reachable by the `validate` job's Markdown link check. Superseded in practice by this module, whose §5 is the architecture design with the arithmetic completed |
| `src/amf/quantum_ml/quantum_activation.py` — Quantum activation functions | **Reject in-tree** | Sub-package layout, runtime dependency, non-deterministic sampling, and a coverage gate that a sampler cannot meet. Replace with `src/amf/multilinear.py` (§6 table), which computes the same function exactly. The circuit version belongs in the sidecar of §6.6 |
| `src/amf/quantum_ml/variational_quantum_classifier.py` — QNN for regime classification | **Reject as vacuous** | Proposition 5.11: the only labels available are `Severity.from_score` composed with `score`, a known total function with zero Bayes error. Training a classifier on it approximates a step function AMF evaluates exactly in four comparisons |
| `examples/quantum_nn_market_forecast.py` — Compare to classical NN | **Reject** | Rule 1 (`market price` input) and rule 2 ("forecast"). Replace with `examples/multilinear_readout.py` (§6 table) and add a case to `tests/integration/test_examples.py` |

Additional deliverables this module recommends, none of which appear in the source note:

| Deliverable | Rationale |
|---|---|
| `src/amf/multilinear.py` — pure-`math` `pauli_expansion(system)` and `evaluate_expansion(...)`, with an `InvalidConfigError`-validated tolerance | Makes Theorem 5.8 computable and testable; also a genuine analytical tool, since the coefficient magnitudes say which metric interactions dominate a system's fragility |
| `tests/unit/test_multilinear.py::test_expansion_reconstructs_fragility_exactly` asserting P1 | The cheapest possible confirmation that the analysis in these docs matches the code |
| A `hypothesis` property in `tests/unit/test_properties.py`: reconstruction error is zero for any market | Guards P1 against future changes to `fragility` — the expansion is only valid while the closed form is multilinear |
| `examples/multilinear_readout.py` plus its `test_examples.py` case | Deterministic, stdlib-only demonstration of §5.3–§5.6 |
| A `CONTRIBUTING.md` note recording the naming tripwires of §6.4 (`order` inside *disorder*, `trade` inside *tradeoff*, `signal` inside *readout signal*) | The three substrings most likely to fail the boundary guard for anyone working in this vocabulary |
| A CHANGELOG entry under `## [Unreleased]` → *Added* | Required by the contributor checklist for any user-visible change |
| An `amf-quantum-lab` sidecar skeleton — separate private repository, own CI, own dependencies, no Release-asset distribution (§6.6) | The only place the note's three code deliverables can live without violating rules 1–4 |

---

## 9. Research leadership and prerequisites

The source note's line, verbatim:

> **Research Leaders Needed**: Quantum machine learning researcher

Necessary; not sufficient; and the single role most likely to import a rule-2 violation,
because "advantage over classical" is the currency of that field and AMF has no benchmark to
win. A skills matrix that would actually staff this module:

| Role | Must be able to | Owns which sections | Failure mode if absent |
|---|---|---|---|
| Quantum machine learning researcher | Derive the parameter-shift rule from `U = exp(-i theta G/2)` unaided; state Theorem 2.7's frequency set for a given ansatz; name the four distinct barren-plateau mechanisms and which each is cured by | §2.5–§2.31, §5.2–§5.7 | A deep hardware-efficient ansatz proposed for a degree-1 target (§5.7), with data re-uploading attached |
| Quantum information theorist | Distinguish unitary from CPTP; compute the action of a depolarising channel on a Pauli expectation; explain Gottesman–Knill and bounded-entanglement simulability | §2.4, §2.28–2.29, §5.12, §5.13 | "Entanglement" invoked as an explanatory primitive; noise described as regularisation |
| Numerical analyst / scientific-computing engineer | Cost a `2^n` state-vector update; fix a summation arrangement; reason about IEEE-754 non-associativity and reproducibility across runners | §5.9, §5.10, §6.1, §6.2 | A "deterministic" simulator whose output differs in the last bits between CI runners, breaking the permutation-invariance property test |
| Statistical-learning theorist | Distinguish approximation from estimation; state the representer theorem; explain why Theorem 2.25's bound and [26]'s counterexample coexist | §2.11–§2.12, §2.25–§2.26, §5.15, P12 | "Harder to overfit" asserted with no hypothesis class, no sample, and no risk functional |
| Repository maintainer | Recite the four hard rules and the `FORBIDDEN` list from memory; run the boundary guard on a proposed name before it is written | §6 in full | A `quantum_ml/` sub-package merged with a `price_encoding` member and a device-seeded test |

**Prerequisite ladder, undergraduate to frontier.**

1. *Undergraduate 2* — linear algebra over `C`, spectral theorem, tensor products (M1);
   probability and concentration inequalities (M2).
2. *Undergraduate 3–4* — quantum mechanics from the postulates (M3); neural networks and
   backpropagation (M8); statistical learning theory (M6).
3. *Postgraduate 1* — quantum computation: gate sets, universality, circuit identities (M4);
   channels, noise, error correction (M5); kernels and RKHS (M7); floating-point determinism
   (M17).
4. *Postgraduate 2* — parameterised circuits as models (M9); encoding and Fourier expressivity
   (M10); quantum gradients (M11); optimisation under shot noise (M13).
5. *Postgraduate 3 / frontier* — the barren-plateau taxonomy and its Lie-algebraic unification
   (M12); classical simulation and dequantisation (M14); the advantage question read critically
   (M15); quantum computing in finance, with the fault-tolerant/asymptotic caveats intact
   (M16).

A contributor who has completed steps 1–3 can check every derivation in §5. A contributor who
stops before step 5 will propose scaling the qubit count, which is the one move §5.10 shows
cannot help.

---

## References

Identifiers (DOI, arXiv id, volume, pages) are given only where confirmed; where a detail could
not be confirmed it is omitted rather than guessed.

- [1] J. Preskill, "Quantum computing in the NISQ era and beyond", *Quantum* **2**, 79 (2018).
- [2] M. A. Nielsen and I. L. Chuang, *Quantum Computation and Quantum Information*, 10th
  Anniversary Edition, Cambridge University Press (2010).
- [3] K. Mitarai, M. Negoro, M. Kitagawa and K. Fujii, "Quantum circuit learning", *Physical
  Review A* **98**, 032309 (2018).
- [4] M. Schuld, V. Bergholm, C. Gogolin, J. Izaac and N. Killoran, "Evaluating analytic
  gradients on quantum hardware", *Physical Review A* **99**, 032331 (2019).
- [5] G. E. Crooks, "Gradients of parameterized quantum gates using the parameter-shift rule and
  gate decomposition", arXiv:1905.13311 (2019).
- [6] D. Wierichs, J. Izaac, C. Wang and C. Y.-Y. Lin, "General parameter-shift rules for
  quantum gradients", *Quantum* **6**, 677 (2022).
- [7] M. Benedetti, E. Lloyd, S. Sack and M. Fiorentini, "Parameterized quantum circuits as
  machine learning models", *Quantum Science and Technology* **4**, 043001 (2019).
- [8] V. Havlíček, A. D. Córcoles, K. Temme, A. W. Harrow, A. Kandala, J. M. Chow and
  J. M. Gambetta, "Supervised learning with quantum-enhanced feature spaces", *Nature* **567**,
  209–212 (2019).
- [9] M. Schuld and N. Killoran, "Quantum machine learning in feature Hilbert spaces",
  *Physical Review Letters* **122**, 040504 (2019).
- [10] M. Schuld, "Supervised quantum machine learning models are kernel methods",
  arXiv:2101.11020 (2021).
- [11] M. Schuld, R. Sweke and J. J. Meyer, "Effect of data encoding on the expressive power of
  variational quantum-machine-learning models", *Physical Review A* **103**, 032430 (2021).
- [12] A. Pérez-Salinas, A. Cervera-Lierta, E. Gil-Fuster and J. I. Latorre, "Data re-uploading
  for a universal quantum classifier", *Quantum* **4**, 226 (2020).
- [13] T. Goto, Q. H. Tran and K. Nakajima, "Universal approximation property of quantum machine
  learning models in quantum-enhanced feature spaces", *Physical Review Letters* **127**, 090506
  (2021).
- [14] J. R. McClean, S. Boixo, V. N. Smelyanskiy, R. Babbush and H. Neven, "Barren plateaus in
  quantum neural network training landscapes", *Nature Communications* **9**, 4812 (2018).
- [15] M. Cerezo, A. Sone, T. Volkoff, L. Cincio and P. J. Coles, "Cost function dependent
  barren plateaus in shallow parametrized quantum circuits", *Nature Communications* **12**,
  1791 (2021).
- [16] Z. Holmes, K. Sharma, M. Cerezo and P. J. Coles, "Connecting ansatz expressibility to
  gradient magnitudes and barren plateaus", *PRX Quantum* **3**, 010313 (2022).
- [17] S. Wang, E. Fontana, M. Cerezo, K. Sharma, A. Sone, L. Cincio and P. J. Coles,
  "Noise-induced barren plateaus in variational quantum algorithms", *Nature Communications*
  **12**, 6961 (2021).
- [18] M. Ragone, B. N. Bakalov, F. Sauvage, A. F. Kemper, C. Ortiz Marrero, M. Larocca and
  M. Cerezo, "A Lie algebraic theory of barren plateaus for deep parameterized quantum
  circuits", *Nature Communications* **15**, 7172 (2024).
- [19] M. Cerezo, M. Larocca, D. García-Martín, N. L. Diaz, P. Braccia, E. Fontana et al., "Does
  provable absence of barren plateaus imply classical simulability?", *Nature Communications*
  **16**, 7907 (2025).
- [20] M. Cerezo, A. Arrasmith, R. Babbush, S. C. Benjamin, S. Endo, K. Fujii, J. R. McClean,
  K. Mitarai, X. Yuan, L. Cincio and P. J. Coles, "Variational quantum algorithms", *Nature
  Reviews Physics* **3**, 625–644 (2021).
- [21] L. Bittel and M. Kliesch, "Training variational quantum algorithms is NP-hard",
  *Physical Review Letters* **127**, 120502 (2021).
- [22] R. Sweke, F. Wilde, J. J. Meyer, M. Schuld, P. K. Fährmann, B. Meynard-Piganeau and
  J. Eisert, "Stochastic gradient descent for hybrid quantum-classical optimization", *Quantum*
  **4**, 314 (2020).
- [23] S. Sim, P. D. Johnson and A. Aspuru-Guzik, "Expressibility and entangling capability of
  parameterized quantum circuits for hybrid quantum-classical algorithms", *Advanced Quantum
  Technologies* **2**, 1900070 (2019).
- [24] H.-Y. Huang, M. Broughton, M. Mohseni, R. Babbush, S. Boixo, H. Neven and J. R. McClean,
  "Power of data in quantum machine learning", *Nature Communications* **12**, 2631 (2021).
- [25] M. C. Caro, H.-Y. Huang, M. Cerezo, K. Sharma, A. Sornborger, L. Cincio and P. J. Coles,
  "Generalization in quantum machine learning from few training data", *Nature Communications*
  **13**, 4919 (2022).
- [26] E. Gil-Fuster, J. Eisert and C. Bravo-Prieto, "Understanding quantum machine learning
  also requires rethinking generalization", *Nature Communications* **15**, 2277 (2024).
- [27] F. J. Schreiber, J. Eisert and J. J. Meyer, "Classical surrogates for quantum learning
  models", *Physical Review Letters* **131**, 100803 (2023).
- [28] J. M. Kübler, S. Buchholz and B. Schölkopf, "The inductive bias of quantum kernels",
  *Advances in Neural Information Processing Systems 34 (NeurIPS 2021)*, 12661–12673.
- [29] Y. Liu, S. Arunachalam and K. Temme, "A rigorous and robust quantum speed-up in
  supervised machine learning", *Nature Physics* **17**, 1013–1017 (2021).
- [30] A. Abbas, D. Sutter, C. Zoufal, A. Lucchi, A. Figalli and S. Woerner, "The power of
  quantum neural networks", *Nature Computational Science* **1**, 403–409 (2021).
- [31] J. Biamonte, P. Wittek, N. Pancotti, P. Rebentrost, N. Wiebe and S. Lloyd, "Quantum
  machine learning", *Nature* **549**, 195–202 (2017).
- [32] S. Aaronson, "Read the fine print", *Nature Physics* **11**, 291–293 (2015).
- [33] E. Tang, "A quantum-inspired classical algorithm for recommendation systems",
  *Proceedings of the 51st Annual ACM SIGACT Symposium on Theory of Computing (STOC 2019)*,
  217–228.
- [34] I. Cong, S. Choi and M. D. Lukin, "Quantum convolutional neural networks", *Nature
  Physics* **15**, 1273–1278 (2019).
- [35] K. Beer, D. Bondarenko, T. Farrelly, T. J. Osborne, R. Salzmann, D. Scheiermann and
  R. Wolf, "Training deep quantum neural networks", *Nature Communications* **11**, 808 (2020).
- [36] E. Farhi and H. Neven, "Classification with quantum neural networks on near term
  processors", arXiv:1802.06002 (2018).
- [37] K. Temme, S. Bravyi and J. M. Gambetta, "Error mitigation for short-depth quantum
  circuits", *Physical Review Letters* **119**, 180509 (2017).
- [38] Z. Cai, R. Babbush, S. C. Benjamin, S. Endo, W. J. Huggins, Y. Li, J. R. McClean and
  T. E. O'Brien, "Quantum error mitigation", *Reviews of Modern Physics* **95**, 045005 (2023).
- [39] M. Schuld and F. Petruccione, *Machine Learning with Quantum Computers*, 2nd edition,
  Springer, Quantum Science and Technology series (2021).
- [40] V. Bergholm et al., "PennyLane: Automatic differentiation of hybrid quantum-classical
  computations", arXiv:1811.04968.
- [41] D. Herman, C. Googin, X. Liu, Y. Sun, A. Galda, I. Safro, M. Pistoia and Y. Alexeev,
  "Quantum computing for finance", *Nature Reviews Physics* **5**, 450–465 (2023).
- [42] D. J. Egger, C. Gambella, J. Marecek, S. McFaddin, M. Mevissen, R. Raymond, A. Simonetto,
  S. Woerner and E. Yndurain, "Quantum computing for finance: state-of-the-art and future
  prospects", *IEEE Transactions on Quantum Engineering* **1** (2020).
- [43] R. Orús, S. Mugel and E. Lizaso, "Quantum computing for finance: overview and prospects",
  *Reviews in Physics* **4**, 100028 (2019).
- [44] N. Stamatopoulos, D. J. Egger, Y. Sun, C. Zoufal, R. Iten, N. Shen and S. Woerner,
  "Option pricing using quantum computers", *Quantum* **4**, 291 (2020).
- [45] A. Montanaro, "Quantum speedup of Monte Carlo methods", *Proceedings of the Royal Society
  A* **471**, 20150301 (2015).
- [46] N. Aronszajn, "Theory of reproducing kernels", *Transactions of the American Mathematical
  Society* **68**, 337–404 (1950).
- [47] B. Schölkopf and A. J. Smola, *Learning with Kernels: Support Vector Machines,
  Regularization, Optimization, and Beyond*, MIT Press (2002).
- [48] J. Shawe-Taylor and N. Cristianini, *Kernel Methods for Pattern Analysis*, Cambridge
  University Press (2004).
- [49] W. Hoeffding, "Probability inequalities for sums of bounded random variables", *Journal
  of the American Statistical Association* **58**(301), 13–30 (1963).
- [50] J. Watrous, *The Theory of Quantum Information*, Cambridge University Press (2018).
- [51] J. Bowles, S. Ahmed and M. Schuld, "Better than classical? The subtle art of benchmarking
  quantum machine learning models", arXiv:2403.07059 (2024).
- [52] M. Schuld and N. Killoran, "Is quantum advantage the right goal for quantum machine
  learning?", *PRX Quantum* **3**, 030101 (2022).
- [53] M. M. Wilde, *Quantum Information Theory*, 2nd edition, Cambridge University Press
  (2017).
- [54] D. Gottesman, "The Heisenberg representation of quantum computers",
  arXiv:quant-ph/9807006 (1998).
- [55] R. Jozsa and N. Linden, "On the role of entanglement in quantum-computational
  speed-up", *Proceedings of the Royal Society A* **459**, 2011–2032 (2003).
- [56] G. Vidal, "Efficient classical simulation of slightly entangled quantum computations",
  *Physical Review Letters* **91**, 147902 (2003).
- [57] F. Arute et al., "Quantum supremacy using a programmable superconducting processor",
  *Nature* **574**, 505–510 (2019).
- [58] J. Preskill, *Ph219/CS219 Quantum Computation*, lecture notes, California Institute of
  Technology.
