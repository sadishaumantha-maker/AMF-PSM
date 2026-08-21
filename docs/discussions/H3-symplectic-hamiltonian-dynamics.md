# H3: Symplectic Geometry & Hamiltonian Dynamics

> **Discussion category**: Research · **Labels**: `H3`, `dynamical-systems`, `theory`, `research`
> **Source**: `docs/QUANTUM_NEURAL_RESEARCH.md` § Discussion H3
> **Status**: Open for comment · **Nature**: Theoretical module, illustrative and not
> empirically validated

---

## 0. Abstract and reading guide

Hamiltonian mechanics is the geometry of *conservative* systems. Its central structural facts —
Liouville's theorem on phase-space volume, Poincaré recurrence, Noether's theorem — are
theorems about flows that preserve a symplectic form, and every one of them fails, quietly and
completely, the moment dissipation enters.

This module takes the source note's proposal seriously enough to test it, and reaches two
sharp negative results and one strongly positive one.

**Negative 1 (§5.1).** AMF's stress state space is `ℝ⁷`. A symplectic form is a non-degenerate
alternating bilinear form, and no such form exists on an odd-dimensional vector space. AMF's
state space therefore **cannot carry a symplectic structure at all**, at any parameterisation.
This is not a modelling difficulty to be worked around; it is a dimension count.

**Negative 2 (§5.2).** Even after doubling the state space to `ℝ¹⁴` to fix the parity, AMF's
step map contracts phase-space volume by a factor `|det A| ≤ damping⁷ ≈ 0.32` per step at the
default `damping = 0.85`. Liouville conservation fails *by construction*, because damping,
retention and absorptive capacity are exactly the dissipative terms the model was built around.
The source note's "Total 'information volume' of market uncertainty is constant" is false for
AMF's dynamics, and the diagnostic it proposes — "if volume changes dramatically, crisis
imminent" — would fire on every single run.

**Positive (§5.4).** The correct generalisation is not Hamiltonian but **port-Hamiltonian**:
`ẋ = (J − R)∇H(x) + G u`, with `J` skew-symmetric (lossless internal exchange), `R ⪰ 0`
(dissipation), and `u` an external input. This framework was built for open, driven, dissipative
systems, and it maps onto AMF with unusual precision — `R` is absorptive capacity and damping,
`G u` is shock injection, `J` is coupling-mediated redistribution, and the resulting energy
balance `dH/dt ≤ yᵀu` is a *dissipativity* statement that would give AMF's `resilience` score
something it currently lacks: a physical interpretation as an `L₂` gain bound.

The module therefore recommends **rejecting the source note's Hamiltonian/Liouville proposal as
stated** and **adopting its port-Hamiltonian correction**. §7 states both in refutable form.

**Prerequisites**: multivariable calculus, linear algebra (bilinear forms, determinants,
eigenvalues), ODEs. Differential-forms fluency helps but §5 is written so it is not required.

---

## 1. Verbatim source specification

The following is the source note's specification for this discussion, reproduced word for
word without alteration:

````markdown
### Discussion H3: Symplectic Geometry & Hamiltonian Dynamics
**Theme**: Model market dynamics as phase-space trajectories conserving "information volume"

**Concept**:
- Symplectic geometry: Mathematical framework for conservative systems (energy-conserving)
- Hamiltonian: Total energy (kinetic + potential)
- Phase space: Position + momentum (price + velocity)

**Application to Markets**:
```
Analogy: Market = mechanical system
  Position q = asset price
  Momentum p = market velocity (dp/dt = price rate of change)
  
Hamiltonian H = kinetic energy + potential energy
  H = (1/2)p² + V(q)
  where V(q) = risk potential (friction, volatility, leverage)

Hamilton's equations:
  dq/dt = ∂H/∂p = p (velocity)
  dp/dt = -∂H/∂q = -∂V/∂q (force from risk potential)

Key property: Volume in phase space is conserved (Liouville's theorem)
  → Total "information volume" of market uncertainty is constant
  → Markets redistribute risk, not destroy it
```

**Insight**: 
- Quantitative easing (QE) = pushing market to lower-risk potential
- Trade wars = adding to risk potential
- Leverage = increasing momentum (price acceleration)

**Predictive Use**:
```
Compute market Hamiltonian trajectory
Track phase-space volume (should be constant)
If volume changes dramatically:
  → Market is "leaking" information → Crisis imminent
  
Example: Pre-2008, leverage was building (rising p)
         Risk potential was flat (policy too loose, V too low)
         This imbalance → Crash
```

**Deliverable**:
- `docs/research/symplectic_market_dynamics.md` — Theory
- `src/amf/dynamics/hamiltonian_market.py` — Hamiltonian solver
- `src/amf/dynamics/phase_space_volume.py` — Liouville check
- `examples/hamiltonian_crisis_detection.py` — Test on data

**Research Leaders Needed**: Mathematical physicist, dynamical systems expert
````

---

## 2. Formal foundations

### 2.1 Symplectic vector spaces and manifolds

**Definition 2.1 (Symplectic form).** A symplectic form on a real vector space `V` is a bilinear
map `ω : V × V → ℝ` that is

- **alternating**: `ω(u, u) = 0` for all `u` (equivalently `ω(u,v) = −ω(v,u)`), and
- **non-degenerate**: `ω(u, v) = 0` for all `v` implies `u = 0`.

**Theorem 2.2 (Parity).** A finite-dimensional vector space admitting a symplectic form has even
dimension.

*Proof.* Represent `ω` by a matrix `Ω` with `Ωᵀ = −Ω`. Then
`det Ω = det Ωᵀ = det(−Ω) = (−1)^{dim V} det Ω`. If `dim V` is odd this forces `det Ω = 0`,
contradicting non-degeneracy. ∎

Theorem 2.2 is elementary, and it is the hinge of this entire module — see §5.1.

**Definition 2.3 (Symplectic manifold).** A pair `(M, ω)` where `M` is a smooth manifold and `ω`
a closed (`dω = 0`), non-degenerate 2-form.

**Theorem 2.4 (Darboux).** Every point of a `2n`-dimensional symplectic manifold has a
coordinate neighbourhood in which `ω = Σ_{i=1}^{n} dq_i ∧ dp_i`. Symplectic manifolds have **no
local invariants** — locally they are all the same. See Arnold [1, §43] or Marsden and Ratiu
[4, Ch. 5].

**Definition 2.5 (Hamiltonian vector field, Poisson bracket).** Given `H : M → ℝ`, the
Hamiltonian vector field `X_H` is defined by `ω(X_H, ·) = dH`. In Darboux coordinates this is
Hamilton's equations,

```
dq_i/dt =  ∂H/∂p_i ,      dp_i/dt = − ∂H/∂q_i ,
```

exactly as written in the source note. The Poisson bracket is
`{F, G} = Σ_i ( ∂F/∂q_i ∂G/∂p_i − ∂F/∂p_i ∂G/∂q_i )`, and it satisfies bilinearity,
antisymmetry, the Leibniz rule and the Jacobi identity.

**Proposition 2.6 (Conservation of `H`).** `dH/dt = {H, H} = 0` along the flow: an autonomous
Hamiltonian is a constant of motion.

### 2.2 Liouville's theorem — statement and hypotheses

**Theorem 2.7 (Liouville).** The flow of a Hamiltonian vector field preserves the symplectic
volume `ω^n / n!`; equivalently, for any measurable region `Ω ⊆ M`, `vol(φ_t(Ω)) = vol(Ω)` for
all `t`. See Arnold [1, §16]; the result descends from Liouville's 1838 work on first-order
systems.

*Proof sketch.* A vector field preserves volume iff its divergence vanishes. For `X_H`,

```
div X_H = Σ_i [ ∂/∂q_i (∂H/∂p_i) + ∂/∂p_i (−∂H/∂q_i) ] = Σ_i [ ∂²H/∂q_i∂p_i − ∂²H/∂p_i∂q_i ] = 0
```

by equality of mixed partials. ∎

**The hypotheses matter and are routinely dropped in applied writing.** Liouville's theorem
requires (i) an even-dimensional phase space with a symplectic form, (ii) a flow generated by a
Hamiltonian with respect to that form, (iii) smoothness sufficient for mixed partials to commute.
Remove any one and the conclusion goes. In particular:

**Proposition 2.8 (Dissipative counterpart).** For a general smooth field `ẋ = f(x)` on `ℝ^d`,
volume evolves as `d/dt vol(φ_t(Ω)) = ∫_{φ_t(Ω)} div f`. For a linear system `ẋ = Ax`,
`vol(φ_t(Ω)) = e^{t·tr A} vol(Ω)`; for a linear *map* `x ↦ Ax` iterated, volume scales by
`|det A|` per step. Volume is preserved iff `tr A = 0` (flow) or `|det A| = 1` (map).

This proposition, not Liouville's theorem, is the one that applies to AMF (§5.2).

**Theorem 2.9 (Poincaré recurrence).** If `φ_t` preserves a finite measure on a bounded
invariant region, then almost every point returns arbitrarily close to itself infinitely often.
A frequently-invoked and frequently-misapplied companion to Liouville: it too needs measure
preservation, so a dissipative system need not recur at all — it may simply settle.

### 2.3 Noether, integrability, KAM

**Theorem 2.10 (Noether, 1918 [8]).** A continuous one-parameter symmetry of the action
corresponds to a conserved quantity — time-translation invariance to energy, spatial translation
to momentum, rotation to angular momentum.

**Theorem 2.11 (Liouville–Arnold).** If a `2n`-dimensional Hamiltonian system has `n`
independent, pairwise-Poisson-commuting integrals of motion whose common level sets are compact
and connected, those level sets are `n`-tori, and the motion on them is quasi-periodic in
action–angle coordinates [1, §49].

**Theorem 2.12 (KAM, informally).** Under a small perturbation of an integrable system, a
positive-measure set of invariant tori survives, provided a non-degeneracy condition and
sufficiently irrational frequency ratios hold. Due to Kolmogorov (1954), Arnold (1963) and
Moser (1962); see Arnold [1, Appendix 8].

Integrability is a *non-generic* property. Assuming a market model is integrable, or that it has
conserved quantities, requires an argument — it is not a default.

### 2.4 Symplectic integrators

**Definition 2.13.** A one-step map `Φ_h` is symplectic if it preserves `ω`. The Störmer–Verlet
(leapfrog) scheme is the canonical second-order example.

**Theorem 2.14 (Backward error analysis).** A symplectic integrator applied to `H` is,
to exponentially small remainder over exponentially long times, the *exact* flow of a nearby
"shadow" Hamiltonian `H̃ = H + O(h^r)`. This is why symplectic schemes exhibit bounded energy
error over long integrations while general-purpose schemes drift. See Hairer, Lubich and Wanner
[6, Ch. IX].

**Remark 2.15.** This is the strongest practical argument for symplectic structure and is worth
noting even though §5 concludes AMF is not symplectic: *if* a subsystem of a future AMF is
genuinely conservative, integrating it with a non-symplectic scheme will manufacture spurious
drift that could be mistaken for a structural finding.

### 2.5 Is a given system Hamiltonian at all?

**The inverse problem of the calculus of variations.** Given `ẋ = f(x)`, does there exist a
symplectic form and an `H` with `f = X_H`? The classical answer is the **Helmholtz conditions**
(self-adjointness of the variational derivative). They are restrictive: a generic vector field is
not Hamiltonian. Necessary consequences that are easy to check and immediately disqualifying:

1. `dim` must be even (Theorem 2.2);
2. `div f ≡ 0` (Theorem 2.7);
3. the spectrum of the linearisation at a fixed point must be symmetric under `λ ↦ −λ` and
   `λ ↦ λ̄` — eigenvalues come in quadruples `{λ, −λ, λ̄, −λ̄}`. In particular a Hamiltonian
   linear system **cannot have an asymptotically stable fixed point**.

Condition 3 is decisive for AMF, whose whole design intent is that a shocked market settles back
toward zero stress.

### 2.6 Port-Hamiltonian systems — the open-system generalisation

**Definition 2.16 (Input-state-output port-Hamiltonian system).**

```
ẋ = ( J(x) − R(x) ) ∇H(x)  +  G(x) u
y = G(x)ᵀ ∇H(x)
```

with `J = −Jᵀ` (skew-symmetric structure matrix, lossless internal power exchange),
`R = Rᵀ ⪰ 0` (dissipation matrix), `H` a lower-bounded storage function, `u` the input and `y`
the conjugate output. See van der Schaft and Jeltsema [10].

**Theorem 2.17 (Energy balance / passivity).**

```
dH/dt = ∇H(x)ᵀ ẋ = − ∇H(x)ᵀ R(x) ∇H(x)  +  yᵀ u   ≤   yᵀ u ,
```

since `R ⪰ 0`. The stored "energy" can only increase through the external port; internal
dynamics are lossless (`J`) or dissipative (`R`). The system is passive with storage `H`.

Setting `R = 0` and `u = 0` recovers the Hamiltonian case, and `dH/dt = 0` recovers Proposition
2.6. Port-Hamiltonian systems are thus a strict generalisation that *keeps the geometric
bookkeeping* while admitting exactly the dissipation and external driving that markets — and
AMF — actually have.

**Definition 2.18 (Dissipativity and `L₂` gain).** A system is dissipative with respect to supply
rate `s(u,y)` if there is `H ≥ 0` with `H(x(T)) − H(x(0)) ≤ ∫₀ᵀ s(u,y) dt`. With
`s = ½(γ²‖u‖² − ‖y‖²)`, the system has `L₂` gain `≤ γ`. See Khalil [12, Ch. 6] and van der
Schaft [11].

---

## 3. Academic curriculum modules

| Module | Level | Canonical courses | Core texts | What AMF needs from it |
|---|---|---|---|---|
| Classical mechanics I (Lagrangian) | Undergraduate 2nd–3rd year | MIT's classical mechanics sequence (8.09 at the advanced level); Cambridge Part II Classical Dynamics; Caltech Ph106 | Goldstein, Poole & Safko [2] Ch. 1–2; Landau & Lifshitz [3] §1–§5 | Action principle, Euler–Lagrange, generalised coordinates |
| Classical mechanics II (Hamiltonian) | Advanced undergraduate | Same courses, later terms | Goldstein [2] Ch. 8–9; Landau & Lifshitz [3] §40–§52 | Legendre transform, Hamilton's equations, Poisson brackets, canonical transformations |
| Symplectic geometry | Graduate | Graduate differential-geometry and geometric-mechanics courses | Arnold [1] Part III (§37–§49); Marsden & Ratiu [4]; Abraham & Marsden [5] | Symplectic manifolds, Darboux, momentum maps, reduction |
| Dynamical systems & stability | Graduate | Nonlinear dynamics / control theory sequences | Khalil, *Nonlinear Systems* [12] Ch. 3–4, 6; Guckenheimer & Holmes | Lyapunov functions, LaSalle invariance, dissipativity, `L₂` gain — **the tools AMF actually needs** |
| Geometric numerical integration | Graduate | Numerical-analysis topics courses | Hairer, Lubich & Wanner [6] Ch. I–II, VI, IX | Symplectic schemes, backward error analysis, shadow Hamiltonians |
| Port-Hamiltonian systems & passivity | Graduate / research | Systems-and-control graduate courses; European control summer schools | van der Schaft & Jeltsema [10]; van der Schaft [11] | The open-system formalism §5.4 recommends |
| Hamiltonian Monte Carlo | Graduate (statistics) | Bayesian computation courses | Neal [13]; Betancourt [14] | The one indisputably successful engineering use of this machinery outside physics |
| Physics-informed machine learning | Research | ML topics courses | Greydanus et al. [15]; Cranmer et al. [16]; Chen et al. [17] | Learning conserved structure from trajectories |

Efficient path for this module's argument: Goldstein Ch. 8 → Arnold §16 (Liouville) and §43
(Darboux) → Khalil Ch. 4 and 6 (Lyapunov, dissipativity) → van der Schaft & Jeltsema §1–§2. The
last two are where AMF's answer lives.

---

## 4. Exact source material

### 4.1 Canonical textbooks

- **Arnold, V. I.** *Mathematical Methods of Classical Mechanics.* 2nd edition, Graduate Texts in
  Mathematics 60, Springer, New York, 1989 (translated by K. Vogtmann and A. Weinstein). The
  reference. **§16** Liouville's theorem, **§37–§45** symplectic manifolds and Darboux,
  **§49** Liouville–Arnold integrability, **Appendix 8** KAM.
- **Goldstein, H., Poole, C. and Safko, J.** *Classical Mechanics.* 3rd edition, Addison-Wesley,
  2002. **Ch. 8** Hamilton's equations, **Ch. 9** canonical transformations and Poisson brackets.
  The standard graduate physics text.
- **Landau, L. D. and Lifshitz, E. M.** *Mechanics.* Course of Theoretical Physics Vol. 1,
  3rd edition, Butterworth-Heinemann. Terse and complete; §40–§52 for the Hamiltonian formalism.
- **Marsden, J. E. and Ratiu, T. S.** *Introduction to Mechanics and Symmetry.* 2nd edition,
  Texts in Applied Mathematics 17, Springer, 1999. Geometric mechanics with symmetry and
  reduction done properly.
- **Abraham, R. and Marsden, J. E.** *Foundations of Mechanics.* 2nd edition, Benjamin/Cummings,
  1978. The encyclopaedic treatment.
- **Hairer, E., Lubich, C. and Wanner, G.** *Geometric Numerical Integration:
  Structure-Preserving Algorithms for Ordinary Differential Equations.* 2nd edition, Springer
  Series in Computational Mathematics 31, Springer, 2006. **Ch. VI** symplectic integrators,
  **Ch. IX** backward error analysis.
- **Khalil, H. K.** *Nonlinear Systems.* 3rd edition, Prentice Hall, 2002. **Ch. 4** Lyapunov
  stability and LaSalle, **Ch. 6** passivity and dissipativity.

### 4.2 Primary and seminal papers

- **Noether, E.** "Invariante Variationsprobleme." *Nachrichten von der Gesellschaft der
  Wissenschaften zu Göttingen, Mathematisch-Physikalische Klasse*, 235–257 (1918). Symmetry ⇒
  conservation law.
- **Poincaré, H.** "Sur le problème des trois corps et les équations de la dynamique."
  *Acta Mathematica* **13**, 1–270 (1890). Contains the recurrence theorem.
- **Duane, S., Kennedy, A. D., Pendleton, B. J. and Roweth, D.** "Hybrid Monte Carlo."
  *Physics Letters B* **195**(2), 216–222 (1987). Hamiltonian dynamics turned into a sampler.
- **van der Schaft, A. and Jeltsema, D.** "Port-Hamiltonian Systems Theory: An Introductory
  Overview." *Foundations and Trends in Systems and Control* **1**(2–3), 173–378 (2014). The
  reference for §2.6 and §5.4.
- **Greydanus, S., Dzamba, M. and Yosinski, J.** "Hamiltonian Neural Networks." *Advances in
  Neural Information Processing Systems* **32** (2019). Learn `H`, differentiate it to get the
  field, and conservation is built in rather than hoped for.
- **Cranmer, M., Greydanus, S., Hoyer, S., Battaglia, P., Spergel, D. and Ho, S.** "Lagrangian
  Neural Networks." arXiv:2003.04630 (2020). Drops the canonical-coordinates requirement.
- **Chen, Z., Zhang, J., Arjovsky, M. and Bottou, L.** "Symplectic Recurrent Neural Networks."
  *International Conference on Learning Representations* (2020).

### 4.3 Surveys and lecture notes

- **Neal, R. M.** "MCMC using Hamiltonian dynamics." Chapter 5 of *Handbook of Markov Chain Monte
  Carlo* (eds. S. Brooks, A. Gelman, G. Jones and X.-L. Meng), Chapman & Hall/CRC, 2011. The
  clearest exposition of why symplectic integration matters in practice.
- **Betancourt, M.** "A Conceptual Introduction to Hamiltonian Monte Carlo." arXiv:1701.02434
  (2017). Geometric intuition without the machinery.
- **van der Schaft, A.** *L₂-Gain and Passivity Techniques in Nonlinear Control.* 3rd edition,
  Springer, 2017.

### 4.4 Application to markets — and the reasons for caution

- **Baaquie, B. E.** *Quantum Finance: Path Integrals and Hamiltonians for Options and Interest
  Rates.* Cambridge University Press, 2004. Uses Hamiltonians as generators of pricing
  semigroups. Note what this is and is not: the "Hamiltonian" there is an operator in a
  Feynman–Kac representation of a *parabolic* (diffusive, dissipative) equation, **not** a
  generator of symplectic conservative dynamics. Borrowing the word does not import Liouville's
  theorem.
- **Ilinski, K.** *Physics of Finance: Gauge Modelling in Non-equilibrium Pricing.* Wiley, 2001.
  Gauge-theoretic formulation; explicitly non-equilibrium.
- **Bouchaud, J.-P. and Potters, M.** *Theory of Financial Risk and Derivative Pricing.* 2nd
  edition, Cambridge University Press, 2003. The econophysics standard, and notably *not* built
  on conservative dynamics — it is built on heavy tails, correlation structure and dissipative
  response.
- **Sornette, D.** *Why Stock Markets Crash: Critical Events in Complex Financial Systems.*
  Princeton University Press, 2003. Log-periodic power-law critical points. Cited here as the
  most developed physics-of-crashes programme; also as a cautionary case — its out-of-sample
  record is contested, and it is a *critical-phenomena* model, not a Hamiltonian one.

**Caution.** There is a persistent pattern in physics-of-finance writing of importing a word
(`Hamiltonian`, `entropy`, `phase transition`, `temperature`) together with its theorems, when
only the word transfers. Liouville's theorem is the most seductive case, because "information is
conserved, only redistributed" is a satisfying sentence that happens to require a symplectic
manifold to be true. This module's §5 is an attempt to check rather than to borrow.

---

## 5. Derivation for the AMF setting

### 5.1 AMF's state space is odd-dimensional, so it is not symplectic

`ShockSimulator` evolves a stress vector `x_t ∈ [0,1]⁷` — one component per `SystemKind`.

**Proposition 5.1.** There is no symplectic form on `ℝ⁷`. Consequently AMF's stress state space,
as currently defined, admits no Hamiltonian structure whatsoever, and neither Liouville's theorem
nor Poincaré recurrence has any content for it.

*Proof.* Immediate from Theorem 2.2: `7` is odd. ∎

This is worth stating plainly because it disposes of the source note's framing at the level of
arithmetic, before any modelling judgement is required. The note's own analogy — "Position `q` =
asset price, Momentum `p` = market velocity" — implicitly assumes a state space of *pairs*, which
is exactly the even-dimensional structure `ℝ⁷` lacks.

**The minimal repair** is to double the state space: track `(x, v)` where `v_t = x_t − x_{t−1}` is
a discrete stress velocity, giving `ℝ¹⁴`. Parity is then satisfied and a symplectic form
*exists*. Whether AMF's dynamics is Hamiltonian *with respect to* it is a separate question,
answered next — negatively.

### 5.2 AMF's dynamics is dissipative by construction

Ignore the clip for a moment. The documented step map is

```
x_{t+1}[j] = damping · ( x_t[j]·retention + Σ_i x_t[i]·W[i][j]·transmission·(1 − a_j) )
```

which is linear: `x_{t+1} = A x_t` with

```
A[j][i] = damping · ( retention·δ_{ij} + W[i][j]·transmission·(1 − a_j) ).
```

**Proposition 5.2 (Volume contraction).** Under one step, any region of state space has its
volume multiplied by `|det A|`. Writing `A = damping · (retention·I + B)` where
`B[j][i] = W[i][j]·transmission·(1 − a_j)`,

```
det A = damping⁷ · det( retention·I + B ) .
```

At the documented defaults `damping = 0.85`, `retention = 0.5`, `transmission = 1.0`, the
leading factor alone is `0.85⁷ ≈ 0.3206`. For a weakly coupled market (`B ≈ 0`),
`|det A| ≈ 0.85⁷ · 0.5⁷ ≈ 0.0025`: volume collapses by a factor of roughly 400 **per step**.

**Corollary 5.3.** AMF's stress dynamics preserves phase-space volume only in the measure-zero
parameter set where `|det A| = 1`. The default configuration is nowhere near it. The source
note's proposed diagnostic — *"Track phase-space volume (should be constant); if volume changes
dramatically → Market is 'leaking' information → Crisis imminent"* — would therefore report
"crisis imminent" on every run of every market, including a perfectly healthy one. As a
detector it has no discriminating power, because it is measuring the model's damping constant.

Three further obstructions, each independently fatal to a Hamiltonian reading:

1. **Asymptotic stability is forbidden for Hamiltonian systems** (§2.5, condition 3). AMF is
   *designed* so that a shocked market settles back toward zero stress — `converged`,
   `settling_time` and the `0.15·(1 − settle_penalty)` term in `resilience` all presuppose
   attraction to a fixed point. A linear Hamiltonian system's eigenvalues come in `±λ` pairs, so
   it can be stable but never asymptotically stable.
2. **The clip is not smooth or invertible.** `clip(·, 0, 1)` is piecewise linear with a kink, and
   once it binds it is many-to-one — it maps a set of positive volume to a boundary face of
   measure zero. No volume-preserving, invertible flow can do that.
3. **The optional extensions worsen it.** `recovery_rate` subtracts an active healing term,
   which is dissipation added on purpose; `jitter` (behind a seed) makes the map stochastic; and
   `cascade_threshold` makes it discontinuous.

None of this is a defect in AMF. It is what it means to model absorption and recovery. The
mismatch is with the source note's framing, not with the package.

### 5.3 What the note's mechanical analogy would actually require

Taking the note's own equations at face value in AMF's vocabulary, and being careful to keep
inside the repository's structural language:

| Note's term | Note's reading | Structural analogue in AMF | Problem |
|---|---|---|---|
| `q` (position) | asset price | system stress `x[j]` | The note's own term is a `FORBIDDEN` name (§6) |
| `p` (momentum) | "market velocity", `dp/dt` = rate of change | discrete stress velocity `v[j] = x_t[j] − x_{t−1}[j]` | The note uses `p` for both momentum and price in the same block — the symbol is overloaded |
| `V(q)` | "risk potential (friction, volatility, leverage)" | a potential built from `1 − absorptive_capacity` | Friction is *dissipation*, not potential energy; putting it in `V` is a category error |
| `H = ½p² + V(q)` | total energy | a candidate storage function | Requires unit mass; harmless |
| Liouville conservation | "information volume constant" | — | False here; Proposition 5.2 |

The `V(q)` row is the substantive one. In mechanics, friction is emphatically *not* part of the
potential: a potential force is `−∇V` and is conservative, whereas friction is a non-conservative
force that removes energy from the system. Encoding "friction, volatility, leverage" into `V`
would produce a system that conserves `H` while claiming to model loss — internally inconsistent.
This is the same confusion that Proposition 5.2 detects numerically.

### 5.4 The correct reformulation: AMF as a port-Hamiltonian system

Everything the source note wants — a geometric energy accounting, a conserved-or-not quantity, a
principled notion of the market "storing" and "shedding" stress — is available in the
port-Hamiltonian framework (§2.6), which was designed for open dissipative systems.

**Construction 5.4.** Take the state to be the stress vector `x ∈ [0,1]⁷` and define a storage
function weighted by how load-bearing each system is:

```
H(x) = ½ Σ_j  c_j · x_j²  ,        c_j = criticality of system j  ∈ [0,1] .
```

`H` is non-negative, zero exactly at zero stress, and radially unbounded on the compact state
space — a Lyapunov candidate. Now split the continuous-time generator implied by the step map,
`ẋ = (A − I)x =: Mx`, into its skew and symmetric parts with respect to the `c`-weighted inner
product `⟨u, v⟩_c = Σ_j c_j u_j v_j`:

```
M = J − R ,      J = ½(M − M*) ,     R = − ½(M + M*) ,
```

where `M*` is the `⟨·,·⟩_c`-adjoint. Then `J` is skew-adjoint and `R` is self-adjoint, and

```
dH/dt = ⟨x, Mx⟩_c = − ⟨x, R x⟩_c  +  ⟨x, G u⟩_c ,
```

with `G u` the shock injection (`Shock`, including multi-wave `at_step` injections) and
`Intervention` acting as a time-varying increase in `R` via `absorptive_capacity`.

**Interpretation, and what it buys AMF.**

- **`J` is redistribution.** The skew part moves stress *between* systems without changing `H`.
  This is the honest version of the note's "Markets redistribute risk, not destroy it" — true of
  the skew part only.
- **`R` is absorption.** `R ⪰ 0` iff the market genuinely dissipates stress. `R` losing positive
  semi-definiteness is a **precise, checkable, structural condition** for a market that amplifies
  rather than absorbs — and it is exactly the regime the `simulation` docstrings warn about, where
  "the per-step gain exceeds one and stress grows until it saturates at the `1.0` clip".
  Checking `R ⪰ 0` is a stdlib-computable eigenvalue test on a `7×7` symmetric matrix.
- **`L₂` gain is resilience with units.** Theorem 2.17 and Definition 2.18 give
  `‖y‖_{L₂} ≤ γ ‖u‖_{L₂}`: the smallest such `γ` is a worst-case amplification over *all*
  shock sequences, not just the one that happened to be simulated. AMF's current
  `amplification_factor` is a single-trajectory ratio; `γ` is its supremum. That is a strictly
  stronger, and arguably more useful, structural statement — and it is a **bound**, which the
  existing metric is not.

**Proposition 5.5 (Dissipativity certificate).** If `R ⪰ 0` in the `c`-weighted inner product,
then along any unshocked trajectory `H(x_t)` is non-increasing, so `H` is a Lyapunov function and
the origin is stable. If additionally `R ≻ 0`, the origin is asymptotically stable and
`converged` is guaranteed for every initial condition — the settling-time budget cannot be
exhausted. *Proof.* Immediate from `dH/dt = −⟨x, Rx⟩_c ≤ 0` and LaSalle's invariance principle
[12, §4.2]. ∎

Proposition 5.5 answers an open question the package documentation currently leaves open. The
docstrings state that the step map "is *not* a contraction for every market" and that `converged`
"reports whether the trajectory settled within `max_steps`, not whether it is stable". A positive
`R` gives a *sufficient condition for stability that can be checked without simulating*. That is
the single most valuable thing in this module.

### 5.5 What "phase-space volume" should be replaced by

Rather than `phase_space_volume.py` computing a quantity that is trivially non-constant
(§5.2), the compliant and informative diagnostics are:

1. **`|det A|` per step** — reported once, as a structural descriptor of the market's aggregate
   contraction rate. Not a crisis detector; a characterisation.
2. **Spectral abscissa / spectral radius of `A`** — `ρ(A) < 1` is the exact condition for the
   unclipped linear map to be a contraction, and it is the sharp version of the informal warning
   in the docstrings.
3. **Eigenvalues of `R`** — the dissipativity certificate of Proposition 5.5.
4. **`L₂` gain `γ`** — worst-case structural amplification, computable via the bounded-real lemma
   as a small linear-matrix-inequality feasibility problem. Note honestly that a general LMI
   solver is a dependency; for `7×7` a bisection on `γ` with a Hamiltonian-matrix
   imaginary-eigenvalue test is stdlib-feasible but numerically delicate, and would need care to
   meet the determinism rule.

---

## 6. Repository governance and boundary analysis

| Proposed artefact | Conflict | Compliant reformulation |
|---|---|---|
| `src/amf/dynamics/hamiltonian_market.py` — "Hamiltonian solver" | **Substantively wrong**, per §5.1–§5.2: AMF is not Hamiltonian. Also risks a determinism issue if it uses an iterative eigen-solver | Replace with `dynamics/storage_function.py` implementing Construction 5.4: the `c`-weighted storage `H`, the `J`/`R` split, and the `R ⪰ 0` certificate. Structural vocabulary throughout |
| `src/amf/dynamics/phase_space_volume.py` — "Liouville check" | The check is vacuous (§5.2, Corollary 5.3) — it fails always, by design | Replace with `contraction_metrics()`: `|det A|`, `ρ(A)`, and the eigenvalues of `R`. Report them as descriptors, never as an alarm |
| `examples/hamiltonian_crisis_detection.py` — "Test on data" | **Non-trading boundary** and **illustrative, not validated** — "crisis detection" on market data claims predictive power | Reformulate as `examples/dissipativity_certificate.py`: build a market, split `M` into `J` and `R`, report whether the dissipativity certificate holds, and contrast a healthy with a stressed market. Emit the `_DISCLAIMER`; add to `tests/integration/test_examples.py` |
| The note's `q = asset price`, `V(q) = ... volatility, leverage` | **Non-trading boundary.** `price` is on the mechanically enforced `FORBIDDEN` substring list | Use `stress`, `load`, `absorptive_capacity`, `transmission`. Never expose a public name or dataclass field containing `price` |
| `docs/research/symplectic_market_dynamics.md` | None | Superseded by this module |
| Any eigenvalue / LMI computation | **Zero runtime dependencies** — NumPy and SciPy are both out | `7×7` symmetric eigenvalues via cyclic Jacobi rotations in pure Python are tractable and deterministic; a general LMI solver is not. Prefer certificates that need only a symmetric eigenvalue routine |

**Determinism.** Any eigenvalue routine must have a fixed sweep order, a fixed convergence
tolerance validated as `InvalidConfigError` if out of range, and a documented iteration cap whose
exhaustion returns a partial result rather than raising — mirroring how
`DependencyGraph.centrality` already handles its budget. Floating-point summation order must be
canonical (`SystemKind` declaration order), for exactly the reason `CLAUDE.md` records for the
diagnostic HHI: addition is not associative, and insertion-ordered traversal changed a result in
the last bits once already.

**Layering.** `dynamics` consumes the `CouplingMatrix` and per-system `absorptive_capacity`, so it
sits at the `simulation` layer: `errors`/`models` ← `systems`/`graph` ← `market` ←
`diagnostics`/`simulation`(+`dynamics`) ← `sensitivity` ← `report`/`viz`/`cli`. It must not import
`report`, `viz` or `cli`.

**Validation-claim discipline.** Nothing in this area may be described as detecting, predicting or
forecasting a crisis. `R ⪰ 0` is a statement about a matrix derived from a user-supplied
structural configuration — not about any real market.

---

## 7. Falsifiable propositions and open questions

**P1 (Non-symplecticity).** AMF's stress space admits no symplectic structure.
*Status: proved* (Proposition 5.1, from Theorem 2.2). Refutable only by changing the state space
definition to even dimension — which §5.1 describes as the minimal repair.

**P2 (Volume non-conservation).** `|det A| ≠ 1` for the default configuration and for
substantially all markets. *Refuted if*: a non-negligible set of admissible parameter
combinations yields `|det A| = 1`. Given `damping ∈ (0,1]` appears as `damping⁷`, this would
require `damping = 1` together with a finely tuned coupling structure — check whether that corner
is reachable and whether it is meaningful.

**P3 (The note's detector has no discriminating power).** A phase-space-volume alarm as specified
fires identically on healthy and stressed markets. *Refuted if*: on a corpus of markets, the
volume-change statistic separates markets that AMF's `resilience` scores as low-severity from
those it scores as critical, better than chance.

**P4 (Dissipativity certificate is informative).** The condition `R ⪰ 0` (Construction 5.4)
partitions markets meaningfully — it holds for markets whose trajectories converge and fails for
those that saturate at the clip. *Refuted if*: a substantial fraction of markets with `R ⪰ 0`
still fail to converge within `max_steps`, or markets with `R` indefinite reliably converge
anyway. This is the module's central empirical claim about the *package* (not about any market)
and it is cheaply testable by simulation over synthetic markets.

**P5 (`L₂` gain dominates the trajectory metric).** The worst-case gain `γ` is an upper bound on
the observed `amplification_factor` for every shock sequence, and the bound is attained for some
sequence. *Refuted if*: a counterexample trajectory exceeds `γ`, which would indicate an error in
the `J`/`R` split or in the discrete-to-continuous passage.

**Open questions.**

1. The passage from the discrete map `x_{t+1} = A x_t` to a continuous generator `M = A − I` is
   the crude one. Is the matrix logarithm `M = log A` the right generator, does it exist for
   admissible `A` (it needs no negative real eigenvalues), and does the `J`/`R` split differ
   materially between the two choices?
2. Does the clip destroy the certificate? Proposition 5.5 is proved for the unclipped linear
   system. A saturated system is a *constrained* one; projected dynamical systems and
   Lur'e-type absolute-stability theory are the right tools. Does `R ⪰ 0` survive the projection?
3. Should `H` weight by `criticality` (Construction 5.4) or by `1 − absorptive_capacity`? The
   first says "stress in a load-bearing system is worse"; the second says "stress in a system that
   cannot absorb it is worse". They rank markets differently and the choice is substantive.
4. Under `cascade_threshold`, the dynamics is discontinuous and may settle at a persistent
   non-zero state. Is there a piecewise storage function certifying the *existence* of that
   equilibrium, and can multiple equilibria be enumerated?
5. Is there any AMF subsystem that is genuinely conservative and would justify a symplectic
   integrator (Remark 2.15)? The current answer appears to be no; a negative result stated once
   is worth more than the question staying open.

---

## 8. Deliverables

Reproduced from the source note, with a compliance column:

| Deliverable (verbatim) | Status | Compliance note |
|---|---|---|
| `docs/research/symplectic_market_dynamics.md` — Theory | Superseded by this module | No conflict |
| `src/amf/dynamics/hamiltonian_market.py` — Hamiltonian solver | **Rejected as specified** | AMF is not Hamiltonian (§5.1, §5.2). Replace with the port-Hamiltonian storage function and `J`/`R` split |
| `src/amf/dynamics/phase_space_volume.py` — Liouville check | **Rejected as specified** | The check is vacuous (Corollary 5.3). Replace with `contraction_metrics()`: `|det A|`, `ρ(A)`, eigenvalues of `R` |
| `examples/hamiltonian_crisis_detection.py` — Test on data | **Blocked as specified** | Non-trading boundary plus predictive-claim rule. Reformulate as a dissipativity-certificate example over AMF market configurations |

**Research Leaders Needed**: Mathematical physicist, dynamical systems expert

Note the shape of this table. H3 is the one module in the set whose central proposal this
analysis recommends **rejecting** rather than reformulating at the margins. That conclusion is
itself the deliverable: a documented negative result, with the constructive alternative in §5.4,
is more valuable than an implementation of a diagnostic that cannot discriminate.

---

## 9. Research leadership and prerequisites

**Skills matrix.**

| Role | Must have | Should have | Will own |
|---|---|---|---|
| Mathematical physicist | Symplectic geometry; Liouville and its hypotheses; Noether | Geometric mechanics with symmetry; integrability | Correctness of §2 and §5.1–§5.3; open question 5 |
| Dynamical systems expert | Lyapunov and LaSalle; dissipativity; `L₂` gain; linear stability | Port-Hamiltonian theory; absolute stability / Lur'e systems | Construction 5.4, Proposition 5.5, open questions 2 and 4 |
| Numerical analyst | Symmetric eigenvalue algorithms; conditioning; backward error | Structure-preserving integration | The stdlib Jacobi eigensolver, determinism, the iteration budget |
| AMF maintainer | `SimulationConfig` semantics; the determinism history; the hard rules | The cascade/recovery extensions | §6 boundary decisions; layering |

**Prerequisite ladder.**

```
Multivariable calculus + linear algebra (bilinear forms, det, eigenvalues)
                              │
                              ▼
              Lagrangian mechanics (Goldstein Ch. 1–2)
                              │
                              ▼
              Hamiltonian mechanics (Goldstein Ch. 8–9)
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
  Symplectic geometry   Liouville, Poincaré   Nonlinear stability
  (Arnold §37–§49)      (Arnold §16)          (Khalil Ch. 4)
        │                     │                     │
        └─────────────────────┴──────────┬──────────┘
                                         ▼
                        Dissipativity & passivity (Khalil Ch. 6)
                                         ▼
                    Port-Hamiltonian systems (van der Schaft & Jeltsema)
                                         ▼
                          ►  Construction 5.4 — where AMF's answer lives
```

The shortest honest route to this module's conclusion skips symplectic geometry almost entirely
and goes Goldstein Ch. 8 → Arnold §16 → Khalil Ch. 4 and 6. Symplectic geometry is needed to
understand *why* the note's proposal fails; control theory is needed to build what replaces it.

---

## References

[1] Arnold, V. I. *Mathematical Methods of Classical Mechanics.* 2nd edition, Graduate Texts in
Mathematics 60, Springer, New York, 1989. Translated by K. Vogtmann and A. Weinstein.

[2] Goldstein, H., Poole, C. and Safko, J. *Classical Mechanics.* 3rd edition, Addison-Wesley,
San Francisco, 2002.

[3] Landau, L. D. and Lifshitz, E. M. *Mechanics.* Course of Theoretical Physics, Volume 1,
3rd edition, Butterworth-Heinemann, Oxford.

[4] Marsden, J. E. and Ratiu, T. S. *Introduction to Mechanics and Symmetry.* 2nd edition, Texts
in Applied Mathematics 17, Springer, New York, 1999.

[5] Abraham, R. and Marsden, J. E. *Foundations of Mechanics.* 2nd edition, Benjamin/Cummings,
Reading, 1978.

[6] Hairer, E., Lubich, C. and Wanner, G. *Geometric Numerical Integration: Structure-Preserving
Algorithms for Ordinary Differential Equations.* 2nd edition, Springer Series in Computational
Mathematics 31, Springer, Berlin, 2006.

[7] Poincaré, H. "Sur le problème des trois corps et les équations de la dynamique."
*Acta Mathematica* **13**, 1–270 (1890).

[8] Noether, E. "Invariante Variationsprobleme." *Nachrichten von der Gesellschaft der
Wissenschaften zu Göttingen, Mathematisch-Physikalische Klasse*, 235–257 (1918).

[9] Duane, S., Kennedy, A. D., Pendleton, B. J. and Roweth, D. "Hybrid Monte Carlo."
*Physics Letters B* **195**(2), 216–222 (1987).

[10] van der Schaft, A. and Jeltsema, D. "Port-Hamiltonian Systems Theory: An Introductory
Overview." *Foundations and Trends in Systems and Control* **1**(2–3), 173–378 (2014).

[11] van der Schaft, A. *L₂-Gain and Passivity Techniques in Nonlinear Control.* 3rd edition,
Springer, Cham, 2017.

[12] Khalil, H. K. *Nonlinear Systems.* 3rd edition, Prentice Hall, Upper Saddle River, 2002.

[13] Neal, R. M. "MCMC using Hamiltonian dynamics." In *Handbook of Markov Chain Monte Carlo*
(eds. S. Brooks, A. Gelman, G. L. Jones and X.-L. Meng), Chapman & Hall/CRC, Boca Raton, 2011,
Chapter 5.

[14] Betancourt, M. "A Conceptual Introduction to Hamiltonian Monte Carlo." arXiv:1701.02434
(2017).

[15] Greydanus, S., Dzamba, M. and Yosinski, J. "Hamiltonian Neural Networks." *Advances in
Neural Information Processing Systems* **32** (2019).

[16] Cranmer, M., Greydanus, S., Hoyer, S., Battaglia, P., Spergel, D. and Ho, S. "Lagrangian
Neural Networks." arXiv:2003.04630 (2020).

[17] Chen, Z., Zhang, J., Arjovsky, M. and Bottou, L. "Symplectic Recurrent Neural Networks."
*International Conference on Learning Representations* (2020).

[18] Baaquie, B. E. *Quantum Finance: Path Integrals and Hamiltonians for Options and Interest
Rates.* Cambridge University Press, Cambridge, 2004.

[19] Ilinski, K. *Physics of Finance: Gauge Modelling in Non-equilibrium Pricing.* Wiley,
Chichester, 2001.

[20] Bouchaud, J.-P. and Potters, M. *Theory of Financial Risk and Derivative Pricing.*
2nd edition, Cambridge University Press, Cambridge, 2003.

[21] Sornette, D. *Why Stock Markets Crash: Critical Events in Complex Financial Systems.*
Princeton University Press, Princeton, 2003.
