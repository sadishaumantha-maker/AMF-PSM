# Q3: Shannon Information Theory & Market Entropy

> **Discussion category**: Research · **Labels**: `theory`, `information-theory`, `entropy`,
> `mutual-information`, `channel-capacity`, `estimation`, `boundary-review`,
> `illustrative-only`
> **Source**: `docs/QUANTUM_NEURAL_RESEARCH.md` § Discussion Q3
> **Status**: Open for comment · **Nature**: Theoretical module, illustrative and not
> empirically validated

## 0. Abstract and reading guide

This module asks whether Shannon's theory says anything about AMF that AMF does not already
say about itself. The answer developed in §5 is: yes, and more sharply than expected, but
almost none of it is about market data. Four results carry the module. **(i)** AMF's
existing `concentration` score is *exactly* a Rényi-2 collision probability, `HHI = 2^-H_2`,
so the diagnostic engine has been computing an entropy since v1 without naming it
(Theorem 5.2). **(ii)** The normalised coupling weights define a joint distribution over
(transmitter, receiver) whose mutual information — `1.5809` bits on `examples/sample_market.json`
— is precisely the KL divergence from the maximum-entropy coupling with the same marginals
(Theorem 5.5), making "how much structure is there beyond out-strength and in-strength?" a
one-number question. **(iii)** The row-normalised coupling matrix is a genuine discrete
memoryless channel; its Blahut–Arimoto capacity is `2.0015` bits/step and its zero-error
capacity lies in `[2, 2.0015]` bits (§5.6). **(iv)** The normalised stress vector's entropy
converges to the entropy of the dominant left eigenvector of the step matrix — `2.301722`
bits, `4.93` effective systems — independently of shock magnitude and of *which* system in
the dominant class is shocked (Theorem 5.8).

This module does **not** claim that any of these numbers forecasts anything, that entropy
detects crises, that mutual information leads contagion, or that any threshold here is
calibrated. §6 names every point where the source note's deliverables collide with the
repository's hard rules and gives a compliant reformulation for each.

**Prerequisite ladder.** Discrete probability and Jensen's inequality → Shannon entropy,
chain rules, mutual information → relative entropy and its inequalities (Gibbs, Pinsker,
data processing, Fano) → AEP and source coding → channel coding and capacity computation →
maximum-entropy inference → Rényi/Tsallis generalisations → algorithmic information and
universal compression → directed information and transfer entropy → finite-sample
estimation theory. §3 maps each rung to courses and chapters; §5 uses roughly rungs 1–6 and
9, and is honest about why rungs 8 and 10 mostly do not apply here.

---

## 1. Verbatim source specification

The following is the complete text of Discussion Q3 as it appears in
`docs/QUANTUM_NEURAL_RESEARCH.md`, reproduced without alteration — including its typography,
its subscripted glyphs, its file paths, and the corrupted exponent on the channel-capacity
line, which §6 treats as a defect to be repaired rather than silently fixed here. It is a
quotation, not an endorsement; §5 and §6 comment on it.

````markdown
### Discussion Q3: Shannon Information Theory & Market Entropy
**Theme**: Claude Shannon's Information Theory applied to financial markets

**Shannon's Key Concepts**:
1. **Entropy H(X)** = measure of uncertainty/information content
   - H = -Σ pᵢ log₂(pᵢ)
   - Higher entropy = more uncertainty = less predictability
   
2. **Mutual Information I(X;Y)** = correlation between two variables
   - I = H(X) + H(Y) - H(X,Y)
   - High mutual information = variables are coupled

3. **Channel Capacity C** = max bits per second a noisy channel can reliably transmit
   - Shannon-Hartley theorem: C = B log₂(1 + S/N)
   - Application: How much policy signal can market absorb without breakdown?

**Application to AMF**:

**A. Market Entropy as Risk Metric**
```
Market states: {bull, bear, crisis, recovery, chaotic}
Price distribution: P(p) at time t
Information entropy: H(Market) = -Σ P(sᵢ) log P(sᵢ)

Interpretation:
  H ≈ 0: Deterministic market (one dominant state) — low risk
  H ≈ max: Chaotic market (all states equally likely) — maximum risk
  
Historical data: Measure H before/after crises
  Pre-crisis: Entropy rises gradually (increasing uncertainty)
  Crisis point: Entropy peaks
  Recovery: Entropy falls (market "settles" into new state)
```

**B. Mutual Information for Systemic Risk**
```
Two markets (e.g., US equities vs. Euro bonds):
I(Market_US; Market_EU) = H(US) + H(EU) - H(US, EU)

Pre-crisis baseline: I ≈ 0.3 bits/trade
During contagion: I → 0.8 bits/trade (highly coupled)
Post-crisis: I → 0.2 bits/trade (decoupled)

Application: Monitor I as leading indicator of contagion
Threshold: If I(t) > threshold, markets are vulnerable to cascade
```

**C. Information Flow & Policy Signal Capacity**
```
Fed announces rate cut: Signal = announcement strength
Market capacity: C = bandwidth × log₂(1 + signal_strength/noise)

Optimal rate cuts:
  Small cuts (weak signal) ≈ lost in market noise
  Large cuts (strong signal) ≈ processed, but may trigger overshooting
  
Theory: Central banks should calibrate rate cuts to market channel capacity
(too-large cuts saturate the channel; too-small cuts are inaudible)
```

**D. Compression & Predictability**
```
Lempel-Ziv compression: If market data is highly compressible,
  → Market has patterns/structure → Predictable
If market data is incompressible:
  → Market is random/chaotic → Unpredictable

Use case: Compress price histories pre/post-policy
  Compression ratio = marker of whether policy "worked" (reduced randomness)
```

**Mathematical Framework**:
```
Shannon entropy of market state:
  H(Market) = -Σᵢ P(Sᵢ|t) log P(Sᵢ|t)

Mutual information (two assets):
  I(A;B) = Σᵢⱼ P(aᵢ,bⱼ) log[P(aᵢ,bⱼ) / (P(aᵢ)P(bⱼ))]

Channel capacity for policy communication:
  C = B log₂(1 + (policy_signal)�� / (market_noise)²)

Kullback-Leibler divergence (market regime shift):
  D_KL(P||Q) = Σᵢ P(i) log[P(i)/Q(i)]
  Measures "distance" between pre- and post-shock distributions
```

**Deliverable**:
- `docs/research/shannon_information_markets.md` — Theory + applications
- `src/amf/information_theory/entropy_calculator.py` — H, I, KL divergence
- `src/amf/information_theory/channel_capacity.py` — Policy signal capacity
- `examples/entropy_as_risk_metric.py` — Backtests on 2008, 2020, etc.

**Research Leaders Needed**: Information theorist, complexity scientist
````

---

## 2. Formal foundations

Throughout, `X` is a random variable on a finite alphabet `X` with pmf `p`. All logarithms
are base 2 and all quantities are in bits unless a statement says otherwise; the convention
`0 log 0 := 0` is used everywhere, and is a *total* extension, not a limit taken on the fly.
Where a constant differs between bits and nats the statement says which.

### 2.1 Entropy, joint entropy, chain rules

**Definition 2.1 (Shannon entropy).** `H(X) = -Σ_x p(x) log p(x)` [1].

**Definition 2.2 (joint and conditional entropy).** `H(X,Y) = -Σ_{x,y} p(x,y) log p(x,y)` and
`H(Y|X) = Σ_x p(x) H(Y | X = x)`.

**Proposition 2.3 (range).** `0 ≤ H(X) ≤ log|X|`. The left equality holds iff `p` is a point
mass; the right iff `p` is uniform. *Proof.* Non-negativity is termwise. For the upper bound,
`log|X| - H(X) = Σ_x p(x) log(p(x)|X|) = D(p ‖ u) ≥ 0` by Theorem 2.7, with equality iff
`p = u`. ∎ This identity — *"divergence from uniform is exactly the entropy deficit"* — is
used verbatim in §5.7.

**Theorem 2.4 (chain rule).** `H(X_1,…,X_n) = Σ_{i=1}^n H(X_i | X_1,…,X_{i-1})` [49, §2.5].

**Theorem 2.5 (conditioning reduces entropy).** `H(Y|X) ≤ H(Y)`, with equality iff `X ⟂ Y`
[49, Thm 2.6.5]. Note the *average* is what shrinks: `H(Y | X = x)` can exceed `H(Y)` for a
particular `x`, a point that matters when a single AMF market is treated as one observation.

### 2.2 Relative entropy and mutual information

**Definition 2.6 (relative entropy).** For pmfs `P ≪ Q`, `D(P ‖ Q) = Σ_x P(x) log[P(x)/Q(x)]`,
with `D = +∞` if absolute continuity fails [6]. `D` is not symmetric and does not satisfy the
triangle inequality; it is not a metric.

**Theorem 2.7 (Gibbs' inequality / non-negativity).** `D(P ‖ Q) ≥ 0`, with equality iff `P = Q`.
*Proof.* `-D(P‖Q) = Σ_x P(x) log[Q(x)/P(x)] ≤ log Σ_x P(x)·Q(x)/P(x) = log Σ_{x: P(x)>0} Q(x) ≤ 0`
by Jensen applied to the strictly concave `log`; strict concavity forces `Q/P` constant, hence
`P = Q`. ∎

**Definition 2.8 (mutual information).**
`I(X;Y) = Σ_{x,y} p(x,y) log[ p(x,y) / (p(x)p(y)) ]` [1].

**Corollary 2.9.** `I(X;Y) = D(P_{XY} ‖ P_X ⊗ P_Y) = H(X) + H(Y) - H(X,Y) = H(X) - H(X|Y) ≥ 0`,
with equality iff `X ⟂ Y`. The first equality is the one §5.5 exploits: mutual information
*is* the divergence from the product (maximum-entropy) coupling.

**Theorem 2.10 (Pinsker's inequality).** In nats, `‖P - Q‖_TV ≤ sqrt(D(P‖Q)/2)`, where
`‖P-Q‖_TV = ½ Σ_x |P(x)-Q(x)|`. *Attribution:* Pinsker [16] proved the inequality with a
weaker constant; the sharp constant above was obtained independently by Csiszár [17] and
Kullback [18]. In bits, replace `D` by `D·ln 2`.

**Definition 2.11 (Jensen–Shannon divergence).** With `M = ½(P+Q)`,
`JSD(P,Q) = ½D(P‖M) + ½D(Q‖M)`. It is symmetric, finite for every pair (absolute continuity
holds by construction), and bounded by `1` bit [19]. **Theorem 2.12.** `sqrt(JSD)` is a metric
on the simplex [20].

**Theorem 2.13 (data processing inequality).** If `X → Y → Z` is a Markov chain then
`I(X;Z) ≤ I(X;Y)` [49, Thm 2.8.1]. *Proof.* Expand `I(X;Y,Z)` by the chain rule two ways:
`I(X;Y) + I(X;Z|Y) = I(X;Z) + I(X;Y|Z)`. Markovianity gives `I(X;Z|Y) = 0`, and
`I(X;Y|Z) ≥ 0`. ∎ **Corollary 2.14.** A deterministic function of `Y` is a special case, so
no post-processing of a report can increase what it says about the market.

**Theorem 2.15 (Fano's inequality).** Let `X̂ = g(Y)` estimate `X ∈ X`, `P_e = Pr[X̂ ≠ X]`.
Then `H(P_e) + P_e log(|X| - 1) ≥ H(X|Y)`, hence `P_e ≥ (H(X|Y) - 1)/log(|X| - 1)` [15;
49, §2.10].

### 2.3 Asymptotics, source coding, channels

**Theorem 2.16 (AEP).** For i.i.d. `X_1,…,X_n ~ p`, `-(1/n) log p(X_1,…,X_n) → H(X)` in
probability; the typical set `A_ε^(n)` has probability `> 1-ε` for large `n` and cardinality
between `(1-ε)2^{n(H-ε)}` and `2^{n(H+ε)}` [1; 49, Ch. 3]. The stationary-ergodic extension
is the Shannon–McMillan–Breiman theorem [11, 12].

**Theorem 2.17 (Kraft–McMillan).** A prefix code with lengths `l_i` over a `D`-ary alphabet
exists iff `Σ_i D^{-l_i} ≤ 1` [14]; the same inequality is necessary for any uniquely
decodable code [13].

**Theorem 2.18 (source coding).** The optimal expected length `L*` of a binary prefix code
satisfies `H(X) ≤ L* < H(X) + 1` [1; 49, Thm 5.4.1].

**Theorem 2.19 (noisy channel coding).** For a discrete memoryless channel `p(y|x)`, the
supremum of achievable rates with vanishing error is `C = max_{p(x)} I(X;Y)`; rates above `C`
have error bounded away from zero [1; 49, Ch. 7]. `C` is a concave maximisation over the input
simplex and is computed by the alternating algorithm of Arimoto [22] and Blahut [21].

**Theorem 2.20 (Shannon–Hartley).** For a *band-limited* channel of bandwidth `B` with
*additive white Gaussian* noise of power `N`, under an *average input power* constraint `S`,
`C = B log(1 + S/N)` bits per second [2]; the `log(1+SNR)` factor traces to Hartley's earlier
counting argument [5]. All three italicised hypotheses are load-bearing: without a noise
model, a power constraint, and a bandwidth, the formula is not merely inexact, it is
undefined. §5.6 is where this matters for AMF.

**Definition 2.21 (zero-error capacity).** `C_0` is the supremum of rates achievable with
*exactly* zero error [3]. With `G` the confusability graph on inputs, `C_0 ≥ log α(G)` where
`α` is the independence number, and `C_0 ≤ C`; the tightest general upper bound is Lovász's
`log ϑ(G)` [23].

**Definition 2.22 (rate–distortion).** `R(D) = min { I(X;X̂) : E d(X,X̂) ≤ D }` is the least
rate that reconstructs `X` within average distortion `D` [4; 54; 49, Ch. 10].

### 2.4 Continuous, maximum-entropy, and generalised entropies

**Definition 2.23 (differential entropy).** `h(X) = -∫ f log f`. It is not a limit of `H`, can
be negative, and is not invariant under reparameterisation — only *differences* such as
`I(X;Y)` are [49, Ch. 8].

**Theorem 2.24 (Gaussian maximises differential entropy).** Among densities on `R` with
variance `σ²`, `h` is maximised uniquely by `N(0,σ²)`, with `h = ½log(2πeσ²)` [49, Thm 8.6.5].

**Theorem 2.25 (maximum-entropy inference).** Maximising `H(p)` subject to `Σ_x p(x) = 1` and
`Σ_x p(x) f_k(x) = μ_k` (`k = 1..K`) yields, when a feasible interior point exists, the unique
`p*(x) ∝ exp(Σ_k λ_k f_k(x))`, the `λ_k` fixed by the constraints. *Proof sketch.* The
objective is strictly concave and the constraints affine; stationarity of the Lagrangian
`H(p) + Σ_k λ_k(Σ_x p f_k - μ_k) + λ_0(Σ_x p - 1)` gives `-log p(x) - 1/ln2 + Σ_k λ_k f_k(x) + λ_0 = 0`.
∎ Jaynes [7, 8] argues this is the *only* assignment that adds no information beyond the
constraints; §5.5 uses the two-marginal case, where `p*` is the product distribution.

**Definition 2.26 (Rényi entropy and Hill numbers).** For `α ≥ 0`, `α ≠ 1`,
`H_α(p) = (1/(1-α)) log Σ_x p(x)^α` [9]; `H_α → H` as `α → 1`. `H_0 = log |supp p|`,
`H_2 = -log Σ_x p(x)²` (collision entropy), `H_∞ = -log max_x p(x)` (min-entropy).
**Proposition 2.27.** `H_α` is non-increasing in `α`, so `H_0 ≥ H_1 ≥ H_2 ≥ H_∞`. The
*Hill numbers* (effective counts) `D_α = 2^{H_α}` inherit the same ordering.

**Definition 2.28 (Tsallis entropy).** `S_q(p) = (1 - Σ_x p(x)^q)/(q-1)` [10]. `S_q` is
non-additive for `q ≠ 1` — the reason it does **not** compose over AMF's seven systems and is
not used in §5.

### 2.5 Algorithmic information

**Definition 2.29 (Kolmogorov complexity).** `K_U(x)` is the length of a shortest program for
universal machine `U` printing `x` [24, 25, 26]. **Theorem 2.30 (invariance).** For universal
`U, V` there is `c_{U,V}` with `|K_U(x) - K_V(x)| ≤ c_{U,V}` for all `x`. **Theorem 2.31
(uncomputability).** `K` is not computable [26]; it is upper semicomputable only.

**Theorem 2.32 (universality of Lempel–Ziv).** The LZ78 compression ratio of a stationary
ergodic source converges almost surely to its entropy rate [29; 49, Ch. 13]. The
finite-sequence complexity measure `c(x)` of Lempel & Ziv [27] and the sliding-window scheme
of [28] are its ancestors.

**Definition 2.33 (normalised compression distance).**
`NCD(x,y) = [C(xy) - min(C(x),C(y))] / max(C(x),C(y))`, where `C` is a real compressor
approximating `K` [30, 31]. It is a *quasi*-metric in practice: the metric axioms hold for the
idealised `K`-based version [30] and only approximately for any real `C`.

### 2.6 Directed measures

**Definition 2.34 (transfer entropy).** With histories `x_t^{(k)}, y_t^{(l)}`,
`T_{Y→X} = I(X_{t+1} ; Y_t^{(l)} | X_t^{(k)})` [32]. It is a conditional mutual information,
hence non-negative, and is zero iff the future of `X` is conditionally independent of `Y`'s
history given `X`'s own.

**Definition 2.35 (directed information).**
`I(X^n → Y^n) = Σ_{i=1}^n I(X^i ; Y_i | Y^{i-1})` [34], anticipated by Marko's bidirectional
theory [33].

**Theorem 2.36 (Gaussian equivalence).** For jointly Gaussian, stationary processes, transfer
entropy equals one half the Granger-causality statistic [35] in nats: `T_{Y→X} = ½ F_{Y→X}`
[36].

**Caution 2.37.** Transfer entropy measures *predictive* conditional dependence, not
mechanism. James, Barnett & Crutchfield [37] show it can both overestimate flow and
underestimate influence; Smirnov [38] catalogues the standard spurious-detection routes
(latent drivers, coarse sampling, observation error). Any AMF-adjacent use must state which
of the two it means, and neither is causal identification.

### 2.7 Estimation from finite samples

**Proposition 2.38 (plug-in bias).** For `N` i.i.d. draws over `m` occupied cells, the
maximum-likelihood entropy estimate satisfies `E[Ĥ_MLE] = H - (m-1)/(2N) + O(N^{-2})` nats;
adding `(m̂-1)/(2N)` is the Miller–Madow correction [44]. The bias is *systematically
downward*: entropy is under-reported from small samples.

**Refinements.** Grassberger's `ψ`-function corrections [40]; Chao–Shen's coverage-adjusted
estimator for unseen cells [43]; the NSB mixture-of-Dirichlet prior [42]; Paninski's minimax
analysis, which shows no estimator is consistent uniformly over distributions when `m/N` is
not small [41]. For *continuous* variables the standard nonparametric mutual-information
estimator is the `k`-nearest-neighbour construction of Kraskov, Stögbauer & Grassberger [39],
which cancels the individual entropy biases by using matched neighbourhood scales.

**Ordinal and regularity statistics.** Permutation entropy replaces values by their ordinal
patterns of embedding dimension `D`, giving a robust, tie-free-by-assumption statistic in
`[0, log D!]` [47]. Approximate entropy [45] and sample entropy [46] measure the rate at which
short template matches fail to extend; sample entropy removes ApEn's self-match bias.

---

## 3. Academic curriculum modules

The ladder below is the sequence a graduate student would actually take. The final column is
deliberately narrow: most of each course is irrelevant to AMF, and the entry names the part
that is not. Course codes are given only where verified; where a code is uncertain the
subject is named instead.

| Module | Level | Canonical course(s) | Core texts (exact units) | What AMF needs from it |
|---|---|---|---|---|
| M1. Discrete probability and convexity | UG2 | Any first probability sequence; a convex-optimisation course for Jensen and Lagrange duality | Cover & Thomas [49] **Ch. 2**; Boyd & Vandenberghe, *Convex Optimization*, CUP 2004, **Ch. 3–5** | Jensen's inequality, strict concavity of `log`, KKT conditions — the engine behind Theorems 2.7 and 2.25 |
| M2. Core information theory | UG4/PG1 | **MIT 6.441** *Information Theory* (OCW, Spring 2010 and Spring 2016); **Stanford EE376A / STATS376A** *Information Theory* (Weissman; renumbered EE276) | Cover & Thomas [49] **Ch. 2 (entropy, MI, DPI, Fano), Ch. 3 (AEP), Ch. 5 (source coding, Kraft), Ch. 7 (channel capacity)**; MacKay [50] **Ch. 1–6, 8–10** | Every definition in §2.1–§2.3; the DPI argument of §5.7 |
| M3. Channel capacity computation | PG1 | **Caltech EE/Ma/CS 126 ab** *Information Theory*; **UC Berkeley EECS/ELENG 229A** *Information Theory and Coding* | Cover & Thomas [49] **Ch. 7, §10.8** (Blahut–Arimoto); Arimoto [22]; Blahut [21]; Csiszár & Körner [51] **Part I** | The alternating maximisation used to obtain `C* = 2.0015` bits in §5.6 |
| M4. Rate–distortion and quantisation | PG1 | The second half of a two-term information-theory sequence (e.g. Berkeley 229B) | Cover & Thomas [49] **Ch. 10**; Berger [54] **Ch. 2–4** | The correct frame for AMF's four-band `Severity` quantiser (§5.9) |
| M5. Continuous and Gaussian information | PG1 | Same sequences as M2, later units | Cover & Thomas [49] **Ch. 8, Ch. 9**; MacKay [50] **Ch. 11** | Why differential entropy is not "entropy", and why `C = B log(1+S/N)` needs its hypotheses |
| M6. Maximum-entropy inference | PG1 | Bayesian-inference and statistical-mechanics courses; **Cambridge Part III** *Information Theory*, and MacKay's Cambridge lectures on information theory, inference and neural networks | Jaynes [7, 8]; MacKay [50] **Ch. 22–23**; Cover & Thomas [49] **Ch. 12** | Theorem 2.25 and the product-form maxent coupling of §5.5 |
| M7. Generalised entropies | PG2 | Statistical-physics and diversity-measurement topics courses | Rényi [9]; Tsallis [10] | The identification `HHI = 2^{-H_2}` (Theorem 5.2) and the Hill-number ordering |
| M8. Ergodic theory and entropy rate | PG2 | Ergodic-theory or advanced-probability courses | Gray [52] **Ch. 3–4, 7–8**; Cover & Thomas [49] **Ch. 4, Ch. 13** | The exact conditions under which "compression ratio ≈ entropy rate" is a theorem rather than a hope |
| M9. Algorithmic information theory | PG2/PG3 | Kolmogorov-complexity topics courses | Li & Vitányi [55] **Ch. 2 (Kolmogorov complexity), Ch. 3 (algorithmic randomness), Ch. 8 (applications)**; Cilibrasi & Vitányi [31] | Why an NCD number has no error bar and cannot be a score (§5.10) |
| M10. Network information / multiterminal | PG3 | Advanced information-theory seminars | Csiszár & Körner [51] **Part II**; Yeung [53] **Ch. 14–16** | Only if AMF ever models simultaneous multi-system drive; flagged as out of scope today |
| M11. Directed information and transfer entropy | PG3 | Computational-neuroscience and complex-systems courses | Bossomaier et al. [56] **Ch. 3–5**; Schreiber [32]; Massey [34]; Barnett et al. [36] | The vocabulary AMF would need *if* it ever ingested time series — and the reasons in §6 why it should not |
| M12. Entropy estimation | PG2 | Statistical-inference and comp-neuro method courses | Paninski [41] **§2–4**; Kraskov et al. [39]; Nemenman et al. [42]; Grassberger [40]; Chao & Shen [43] | The bias arithmetic in §5.11 that decides whether an ensemble entropy is reportable |
| M13. Ordinal and regularity statistics | PG2 | Nonlinear time-series analysis courses | Bandt & Pompe [47]; Pincus [45]; Richman & Moorman [46] | The exact prediction that AMF's default trajectory has permutation entropy `0` (P7) |
| M14. Nonnegative matrices and Perron–Frobenius | UG4 | Advanced linear algebra; matrix analysis | Horn & Johnson, *Matrix Analysis*, 2nd ed., CUP 2013, **Ch. 8**; Seneta, *Non-negative Matrices and Markov Chains*, Springer, **Ch. 1–2** | Theorem 5.8's convergence argument and the basic-class decomposition |
| M15. Floating-point determinism | PG1 | Scientific-computing courses | Goldberg [69]; Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM 2002, **Ch. 1–4** | Why every entropy sum in `src/amf` must run in `SystemKind` declaration order |
| M16. Information in financial economics | PG2 | Asset-pricing and market-microstructure sequences | Fama [61]; Grossman & Stiglitz [62]; Lo [63]; Cont [64] | What "market information" already means to economists before a physicist redefines it |
| M17. Critical reading of econophysics | PG3 | Reading groups | Gallegati et al. [67]; Sornette [68]; James et al. [37]; Smirnov [38] | Calibration of expectation; the sceptical prior this module adopts |

Sequencing note: M1–M3 suffice to read all of §5 except §5.9–§5.11. M12 is the module a
contributor most often skips and most needs: nearly every published "market entropy rises
before a crisis" claim is separated from its null hypothesis by exactly the bias term of
Proposition 2.38. M11 and M13 are needed only to evaluate the source note's items B and D.

---

## 4. Exact source material

### 4.1 Primary and seminal papers

- **Shannon (1948)** [1] — defines entropy, mutual information, the source-coding theorem and
  the noisy-channel coding theorem in one paper; §7 of Part I is the channel-capacity result.
- **Hartley (1928)** [5] — the pre-Shannon counting measure `log s^n`; the ancestor of the
  `log(1 + SNR)` factor.
- **Shannon (1949)** [2] — "Communication in the Presence of Noise": the band-limited
  Gaussian-channel capacity, i.e. the Shannon–Hartley formula the source note invokes.
- **Shannon (1956)** [3] — zero-error capacity and the confusability graph; the object §5.6
  computes for AMF's coupling kernel.
- **Shannon (1959)** [4] — coding with a fidelity criterion: rate–distortion theory.
- **Kullback & Leibler (1951)** [6] — relative entropy as a measure of discrimination
  information, with the sufficiency connection.
- **Jaynes (1957)** [7, 8] — maximum entropy as the inference principle that adds nothing
  beyond stated constraints; Part II extends to the density matrix.
- **Rényi (1961)** [9] — the one-parameter family of entropies satisfying all of Shannon's
  axioms except additivity over conditioning.
- **Tsallis (1988)** [10] — the non-additive `q`-entropy.
- **McMillan (1953)** [11], **Breiman (1957)** [12] — the AEP for stationary ergodic sources.
- **McMillan (1956)** [13] — the Kraft inequality is necessary for unique decipherability.
- **Kraft (1949)** [14] — the original prefix-length inequality (MIT master's thesis).
- **Csiszár (1967)** [17], **Kullback (1967)** [18] — the sharp constant in Pinsker's
  inequality, obtained independently.
- **Lin (1991)** [19] — the Jensen–Shannon divergence and its bounds; **Endres & Schindelin
  (2003)** [20] — its square root is a true metric.
- **Arimoto (1972)** [22] and **Blahut (1972)** [21] — the alternating algorithm for channel
  capacity (and, in [21], for `R(D)`); the exact algorithm run in §5.6.
- **Lovász (1979)** [23] — the `ϑ` upper bound on zero-error capacity.
- **Solomonoff (1964)** [24], **Kolmogorov (1965)** [25], **Chaitin (1966)** [26] — the three
  independent formulations of algorithmic complexity.
- **Lempel & Ziv (1976)** [27], **Ziv & Lempel (1977, 1978)** [28, 29] — sequence complexity
  and the two universal compression algorithms.
- **Li, Chen, Li, Ma & Vitányi (2004)** [30] and **Cilibrasi & Vitányi (2005)** [31] — the
  similarity metric and normalised compression distance.
- **Schreiber (2000)** [32] — transfer entropy; the nonparametric conditional-dependence
  measure the source note's item B gestures at.
- **Marko (1973)** [33], **Massey (1990)** [34] — bidirectional and directed information.
- **Granger (1969)** [35] — predictive causality in econometrics.
- **Barnett, Barrett & Seth (2009)** [36] — Granger causality and transfer entropy coincide
  for Gaussians, up to the factor of two.
- **Kraskov, Stögbauer & Grassberger (2004)** [39] — the `k`-NN mutual-information estimator.
- **Pincus (1991)** [45], **Richman & Moorman (2000)** [46], **Bandt & Pompe (2002)** [47] —
  approximate entropy, sample entropy, permutation entropy.
- **Kelly (1956)** [48] — information rate and the log-optimal growth criterion. **Cited for
  completeness and explicitly out of bounds for this repository:** Kelly's result is about
  sizing wagers from side information and is inseparable from betting returns, which rule 1
  forbids. It is listed so nobody proposes it as "the finance application of Shannon" without
  the caveat.

### 4.2 Canonical textbooks

- **Cover & Thomas, *Elements of Information Theory*, 2nd ed., Wiley-Interscience, 2006** [49].
  The spine of this module: **Ch. 2** (entropy, mutual information, chain rules, DPI §2.8,
  Fano §2.10), **Ch. 3** (AEP), **Ch. 5** (Kraft, source coding), **Ch. 7** (channel capacity),
  **Ch. 8–9** (differential entropy, Gaussian channel), **Ch. 10** (rate–distortion, with
  Blahut–Arimoto in §10.8), **Ch. 11** (information theory and statistics, Sanov, large
  deviations), **Ch. 13** (universal source coding, Lempel–Ziv), **Ch. 14** (Kolmogorov
  complexity).
- **MacKay, *Information Theory, Inference, and Learning Algorithms*, CUP, 2003** [50].
  **Ch. 1–6** for the same core from a coding-first angle, **Ch. 8–10** for dependent variables
  and noisy channels, **Ch. 22–23** for maximum entropy and exponential families. Freely
  available from the author's Cambridge page.
- **Csiszár & Körner, *Information Theory: Coding Theorems for Discrete Memoryless Systems*,
  2nd ed., CUP, 2011** [51]. The rigorous method-of-types treatment; **Part I** for
  single-user capacity.
- **Gray, *Entropy and Information Theory*, 2nd ed., Springer, 2011** [52]. The measure- and
  ergodic-theoretic foundations; the right reference for when "entropy rate" is well defined.
- **Yeung, *Information Theory and Network Coding*, Springer, 2008** [53]. **Ch. 12–13** for
  the information-inequality machinery (Shannon-type inequalities and the `Γ*` cone).
- **Berger, *Rate Distortion Theory: A Mathematical Basis for Data Compression*, Prentice-Hall,
  1971** [54]. The monograph behind §5.9.
- **Li & Vitányi, *An Introduction to Kolmogorov Complexity and Its Applications*, 3rd ed.,
  Springer, 2008** [55]. **Ch. 2–3** for the theory, **Ch. 8** for the applications including
  the similarity metric.
- **Bossomaier, Barnett, Harré & Lizier, *An Introduction to Transfer Entropy: Information
  Flow in Complex Systems*, Springer, 2016** [56]. The book-length statement of §2.6 with
  estimator practice.

### 4.3 Surveys and reviews

- **Paninski (2003)**, *Neural Computation* [41] — the definitive survey-plus-theory of entropy
  and mutual-information estimation, including the minimax lower bounds that kill naive
  plug-in reporting in the undersampled regime.
- **James, Barnett & Crutchfield (2016)**, *Physical Review Letters* [37] — a short, sharp
  critique showing transfer entropy does not measure what its name promises.
- **Smirnov (2013)**, *Physical Review E* [38] — the catalogue of spurious causality routes.
- **Sornette (2014)**, *Reports on Progress in Physics* [68] — a physicist's audit of what
  physics has and has not contributed to financial economics.
- **Gallegati, Keen, Lux & Ormerod (2006)**, *Physica A* [67] — "Worrying trends in
  econophysics": unawareness of the prior economics literature, weak statistical methodology,
  unjustified universality claims, theoretical over-reach. All four apply to the source note
  as drafted.

### 4.4 Open courseware and lecture notes

- **MIT OpenCourseWare 6.441, *Information Theory*** — full lecture notes and problem sets for
  the Spring 2010 and Spring 2016 offerings; the Spring 2016 course notes are a single
  self-contained PDF covering §2.1–§2.3 of this module at full rigour.
- **Stanford EE376A / STATS376A, *Information Theory*** (renumbered **EE276**) — scribed
  lecture notes are public on the course site; the units on the DPI, Fano's inequality and
  channel capacity are the relevant ones.
- **Caltech EE/Ma/CS 126 ab, *Information Theory*** — a two-term sequence running from source
  and channel coding through rate–distortion to network and universal coding.
- **UC Berkeley EECS/ELENG 229A, *Information Theory and Coding*** — graduate sequence with
  public lecture notes; 229A covers Shannon theory, the follow-on term the coding side.
- **Cambridge Part III of the Mathematical Tripos, *Information Theory*** — the Part III
  course covering entropy, typicality, source and channel coding; David MacKay's Cambridge
  lecture course on information theory, inference and neural networks, and its videos, remain
  the best free companion to [50]. (Cambridge course codes are omitted deliberately: they are
  not stable across years, and this module cites nothing it has not verified.)

### 4.5 Domain application to finance and markets — including the sceptical literature

- **Marschinski & Kantz (2002)**, *European Physical Journal B* [57] — the founding
  application of transfer entropy to two financial index series, and — importantly — the
  paper that had to *invent a bias correction* ("effective transfer entropy") because the raw
  estimator returned spurious positive flow between independent series. Read it as evidence
  for Proposition 2.38, not as evidence that the flow is real.
- **Kwon & Yang (2008)**, *EPL* [58] — transfer entropy between 25 stock indices; reports the
  US as the dominant source. Note the estimator and the symbolisation choice do most of the
  work, and the result is not accompanied by a null-model calibration.
- **Dionisio, Menezes & Mendes (2004)**, *Physica A* [59] — mutual information as a nonlinear
  dependence measure for financial series, contrasted with linear correlation.
- **Zunino, Zanin, Tabak, Pérez & Rosso (2009)**, *Physica A* [60] — permutation entropy and
  forbidden ordinal patterns as market-efficiency proxies; the cleanest published statement of
  the source note's item D, and it reports a *ranking* of markets, not a forecast.
- **Fama (1970)** [61] and **Grossman & Stiglitz (1980)** [62] — the economics of information
  in prices, and the impossibility argument that a fully informative price system destroys the
  incentive to gather information. Any "market entropy" claim must be positioned against these
  before it is positioned against Shannon.
- **Lo (2004)** [63] — the adaptive-markets framing under which informational efficiency is
  time-varying rather than binary.
- **Cont (2001)** [64] — the stylised facts (heavy tails, volatility clustering, aggregational
  Gaussianity) that make i.i.d.-based entropy estimators inappropriate for return series.
- **Billio, Getmansky, Lo & Pelizzon (2012)** [65] and **Diebold & Yılmaz (2014)** [66] — the
  mainstream connectedness-measurement literature (Granger-causality networks; variance-
  decomposition networks). These are what a referee will compare an AMF "contagion indicator"
  against, and they are estimated from data AMF deliberately does not hold.
- **Gallegati et al. (2006)** [67], **Sornette (2014)** [68], **James et al. (2016)** [37],
  **Smirnov (2013)** [38] — the sceptical prior. Adopt it.

---

## 5. Derivation for the AMF setting

This section does the mathematics. Every numerical value quoted is computed from
`examples/sample_market.json` with the package's default configuration
(`DiagnosticConfig()`, `SimulationConfig()`), and every one is reproducible from the public
API using the standard library alone.

### 5.1 Notation fixed to the codebase

Let `S = (s_1,…,s_7)` be `SystemKind` in declaration order
`(skeleton, circulatory, nervous, musculature, organs, immune, metabolism)`; `_INDEX` in
`graph.py` and `diagnostics.py` is this order and it is normative. For system `i`:
`ι_i` integrity, `r_i` redundancy, `κ_i` criticality, `ℓ_i` load,
`h_i = ι_i(1-ℓ_i)` health, `a_i = 0.5 r_i + 0.3 ι_i + 0.2(1-ℓ_i)` absorptive capacity.
`w(i,j) ∈ (0,1]` is the aggregated pair weight of the dependency `i → j` ("`i` relies on
`j`"), i.e. `DependencyGraph.edge_weight`. `W[t][r] = w(r,t)` is the `CouplingMatrix`: stress
flows *from* the depended-upon system `t` *to* the depending system `r`.

Two derived quantities recur.

```
E[i][j] = damping * ( retention * [i = j] + W[i][j] * transmission * (1 - a_j) )
```

is the linear part of one `ShockSimulator` step, so that `x_{t+1} = x_t E` while the `[0,1]`
clip is inactive; and

```
P(t, r) = W[t][r] / Z,        Z = Σ_{t,r} W[t][r]
```

is the **coupling distribution**: the pair weights normalised to a joint pmf over
(transmitter, receiver). On the sample market `Z = 4.4`.

### 5.2 AMF already computes a Rényi entropy

`DiagnosticEngine.concentration` forms, for each system `i` with at least one outgoing
dependency, the share vector `π_i(j) = w(i,j) / Σ_k w(i,k)` and returns the
Herfindahl–Hirschman index `HHI_i = Σ_j π_i(j)²`.

**Theorem 5.2.** For every system `i` with non-empty reliance,
`HHI_i = 2^{-H_2(π_i)}`, where `H_2` is the Rényi-2 (collision) entropy of Definition 2.26.
Equivalently `H_2(π_i) = -log HHI_i` and the reciprocal `1/HHI_i = D_2(π_i)` is the Hill
number of order 2 — the *effective number of couplings* system `i` relies on.
*Proof.* Immediate from `H_2(p) = -log Σ p²`. ∎

**Corollary 5.3 (the ordering AMF is missing).** By Proposition 2.27,
`D_0(π_i) ≥ D_1(π_i) ≥ D_2(π_i) ≥ D_∞(π_i)`, where `D_0` is the raw out-degree, `D_1 = 2^{H(π_i)}`
the Shannon perplexity, `D_2 = 1/HHI_i`, and `D_∞ = 1/max_j π_i(j)`. AMF currently reports
`α = 2` only. On the sample market:

| system | out-degree `D_0` | reliance shares | `HHI = 2^{-H_2}` | `H_1` (bits) | `D_1` | `D_2 = 1/HHI` |
|---|---|---|---|---|---|---|
| `skeleton` | 0 | — | `0` (by convention) | — | — | — |
| `circulatory` | 2 | `0.6154, 0.3846` | `0.526627` | `0.961237` | `1.9470` | `1.8989` |
| `nervous` | 2 | `0.4545, 0.5455` | `0.504132` | `0.994030` | `1.9917` | `1.9836` |
| `musculature` | 1 | `1.0` | `1.000000` | `0` | `1` | `1` |
| `organs` | 1 | `1.0` | `1.000000` | `0` | `1` | `1` |
| `immune` | 1 | `1.0` | `1.000000` | `0` | `1` | `1` |
| `metabolism` | 1 | `1.0` | `1.000000` | `0` | `1` | `1` |

Two consequences follow immediately, and both are actionable.

First, the discontinuity documented in `concentration`'s docstring — an isolated system scores
`0` (best) but acquires score `1` (worst) the moment it gains a single trivial coupling — is
not an artefact of the HHI choice. It is the discontinuity of *every* Hill number at the empty
support, because `π_i` is undefined there. The honest repair is not `scale_concentration_by_reliance`
(which multiplies by `min(1, Σ_j w(i,j))` and merely damps the jump) but to report the pair
`(D_0, D_α)` and let the empty case be reported as "no reliance" rather than folded into a
`[0,1]` score at all.

Second, `α = 2` is a *choice*, and a pessimistic one: `H_2 ≤ H_1` means AMF systematically
reports concentration at least as severe as a Shannon-based index would. For `circulatory`,
`D_2 = 1.899` against `D_1 = 1.947` — a 2.5 % difference here, but the gap widens with skew,
and for a system with shares `(0.9, 0.05, 0.05)` it is `D_1 = 1.483` against `D_2 = 1.227`. A
`DiagnosticConfig.concentration_alpha: float = 2.0` knob validated to `α ≥ 0`, with `α = 1`
handled by the Shannon limit and `InvalidConfigError` otherwise, is a three-line change that
makes the existing behaviour the documented default rather than an unexamined one. Note the
name: the natural choice, `concentration_order`, is a dataclass field containing the
`FORBIDDEN` substring `order` and would fail `tests/unit/test_non_trading_boundary.py` on the
first commit. This is not a hypothetical trap — it is the single most likely way an
information-theoretic contribution breaks the boundary guard, since `order` is the standard
word for the parameter `α` in the Rényi family.

### 5.3 The weakness profile as a distribution

`DiagnosticReport.findings` carries seven scores `σ_i ∈ [0,1]`. Normalising,
`q_i = σ_i / Σ_k σ_k`, gives a pmf over systems: *where in the market is the weakness?*

On the sample market `Σ_k σ_k = 2.020728`, `H(q) = 2.726662` bits against a maximum of
`log 7 = 2.807355`, so `D_1(q) = 6.619` of a possible `7`. By Proposition 2.3,

```
D(q ‖ uniform) = log 7 - H(q) = 2.807355 - 2.726662 = 0.080693 bits
```

and by Pinsker (Theorem 2.10, converting to nats), `‖q - u‖_TV ≤ sqrt(0.080693·ln2/2) = 0.1672`.
The interpretation is exact and unglamorous: **the sample market's weakness is almost perfectly
uniform across its seven systems.** The diagnostic index of `0.2796` is not concentrated in one
place; whatever the report's ranking says, the ranking is nearly flat, and 0.08 bits is the
entire amount of "where" information the report contains. This single number is a useful
guard against over-reading a ranking, and it is one line of arithmetic over existing output.

### 5.4 The coupling distribution and its entropies

Take `P(t,r) = W[t][r]/Z` from §5.1. Its marginals are the normalised **out-strength**
(as a transmitter, i.e. how much stress a system exports) and **in-strength** (as a receiver).
On the sample market, with `T` the transmitter and `R` the receiver:

```
H(T)   = 2.113406 bits      (5 systems ever transmit; log 5 = 2.321928)
H(R)   = 2.412259 bits      (6 systems ever receive;  log 6 = 2.584963)
H(T,R) = 2.944768 bits      (8 couplings;             log 8 = 3.000000)
I(T;R) = H(T) + H(R) - H(T,R) = 1.580897 bits
```

`H(T,R) = 2.9448` against `log 8 = 3` says the eight couplings are close to equal in weight —
the market's structure is in *which* pairs exist, not in how unequal the weights are.

### 5.5 Mutual information is the divergence from the maximum-entropy coupling

**Theorem 5.5.** Among all joint pmfs on (transmitter, receiver) with the observed marginals
`P_T` and `P_R`, the entropy-maximising one is the product `P_T ⊗ P_R`, and
`I(T;R) = D(P ‖ P_T ⊗ P_R)`.
*Proof.* The constraint set is the transportation polytope, affine and compact; `H` is strictly
concave, so the maximiser is unique. Theorem 2.25 with `f` the two sets of marginal indicators
gives `p*(t,r) ∝ exp(λ_t + μ_r)`, i.e. a product form, and matching the marginals fixes it as
`P_T ⊗ P_R`. The identity is Corollary 2.9. ∎

This makes a vague question sharp. "How much of the market's coupling structure is *not*
explained by knowing how much each system exports and imports?" Answer: exactly `I(T;R)`. On
the sample market that is **`1.580897` bits** — more than half of `H(T,R) = 2.9448`. The
sample market is therefore strongly *assortative*: knowing the transmitter tells you a great
deal about the receiver beyond what the marginals imply, which is exactly what one expects of
a sparse graph in which most systems have a single outgoing coupling.

Two derived instruments follow, both deterministic, both stdlib-only, both inside the
non-trading boundary.

1. **`structural_coupling_information(market) -> float`** returning `I(T;R)` in bits.
   Zero exactly when the coupling is a product of its marginals; large when reliance is
   channelled through specific pairs.
2. **`maxent_coupling(market) -> CouplingMatrix`** returning `Z · P_T ⊗ P_R`, a
   *null-model market* with the same import/export profile and no pair structure.
   Re-running `DiagnosticEngine.diagnose` on it gives a principled baseline for "how much of
   this market's diagnosis is attributable to pair structure rather than to strength
   totals?" — a comparison AMF currently cannot make.

Neither name contains a `FORBIDDEN` substring. Both are pure functions of the graph.

### 5.6 Structural transmission capacity: the correct replacement for Shannon–Hartley

The source note's item C applies `C = B log₂(1 + S/N)` to "policy signal" and "market noise".
Theorem 2.20 requires a bandwidth, an additive white Gaussian noise process, and an average
power constraint. AMF has none of the three: its state is a bounded stress vector with no
noise model (`SimulationConfig.jitter` defaults to `0.0` and is inert without a seed), no
spectral representation, and no power. The formula is not approximately wrong here; it is
inapplicable. The correct object is the finite-alphabet capacity of Theorem 2.19, and AMF
already contains a channel.

**Construction.** Restrict to transmitters `t` with `Σ_r W[t][r] > 0` and set
`K(r | t) = W[t][r] / Σ_{r'} W[t][r']`. `K` is a bona fide discrete memoryless channel: input
alphabet "which system is stressed", output alphabet "which system receives that stress",
transition law given by the normalised coupling row. Its capacity `C* = max_{p} I(T;R)` is
computed by Blahut–Arimoto [21, 22], an alternating maximisation that converges from any
interior start and needs nothing but `math.log` and `math.exp`.

On the sample market, with `K` as below:

```
skeleton    -> circulatory 0.50000,  nervous 0.31250,  immune 0.18750
circulatory -> musculature 0.53846,  organs  0.46154
nervous     -> circulatory 1.00000
musculature -> nervous     1.00000
organs      -> metabolism  1.00000

C*        = 2.001532 bits/step        (log 5 = 2.321928, the no-noise ceiling)
argmax p* = skeleton 0.005660, circulatory 0.249735, nervous 0.246905,
            musculature 0.247966, organs 0.249735
```

Two readings, one of which is a genuine finding.

*The capacity-achieving input almost deletes `skeleton`.* `skeleton` is the market's most
depended-upon system, yet the input distribution that maximises information throughput gives
it weight `0.0057`. The reason is confusability: `skeleton` transmits into `{circulatory,
nervous, immune}`, and `circulatory` is also the sole output of `nervous` while `nervous` is
also the sole output of `musculature`. Only `immune` distinguishes `skeleton` unambiguously.
A hub whose outputs overlap with everyone else's is, informationally, the *least* useful thing
to excite — which is a structural statement about the market and not about any policy.

*Zero-error capacity is essentially the whole capacity.* The confusability graph on
`{skeleton, circulatory, nervous, musculature, organs}` has exactly two edges
(`skeleton–nervous`, `skeleton–musculature`), so its independence number is
`α = |{circulatory, nervous, musculature, organs}| = 4`. By Definition 2.21,

```
log α = 2.000000  ≤  C_0  ≤  C* = 2.001532   bits/step
```

The gap is `0.0015` bits. Almost all of this market's transmission capacity is achievable with
*zero* ambiguity, and the entire ambiguity budget is the single hub `skeleton`. That is a
crisp, falsifiable structural claim (P4 in §7), and it is the kind of statement the
Shannon–Hartley formula could never have produced because it has no notion of which systems
are confusable.

**Naming.** `channel_capacity` is clean, but *`signal` is on the `FORBIDDEN` substring list*,
so `policy_signal_capacity`, `signal_strength` and `SignalCapacityConfig` all fail
`tests/unit/test_non_trading_boundary.py`. Use `drive`, `stimulus`, `load` or
`transmission` instead: `structural_transmission_capacity`, `DriveCapacityConfig`.

### 5.7 The data processing inequality applied to AMF's own pipeline

The CLI's reporting path is a chain of deterministic maps:

```
Market  ->  DiagnosticReport (7 real scores)  ->  ranking (a permutation)  ->  Severity bands  ->  overall Severity
```

Each arrow is a function of its input alone, so the chain is Markov and Theorem 2.13 applies at
every stage. The information about the market available downstream is non-increasing, and
Corollary 2.14 says no renderer can recover it.

The magnitudes are stark. Identifying *which* system is weakest requires `log 7 = 2.807355`
bits; the full ranking carries up to `log 7! = 12.299208` bits. On the sample market the
severity profile is six `moderate` and one `low`, so

```
H(severity profile) = 0.591673 bits
```

Now apply Fano (Theorem 2.15). Suppose an analyst sees only the bands and must name the weakest
system. Conditioned on the band `moderate`, the six candidates are indistinguishable, so
`H(X|Y) = log 6 = 2.584963` bits with `|X| = 6`, and

```
P_e  >=  (H(X|Y) - 1) / log(|X| - 1)  =  (2.584963 - 1) / log 5  =  1.584963 / 2.321928  =  0.6826
```

**At least a 68 % error rate identifying the weakest system from severity bands alone.**
(Uniform guessing achieves `5/6 = 0.833`, consistent with the bound.) The scores that would
settle it differ in the third decimal — `organs 0.324700`, `immune 0.322800`,
`metabolism 0.322800` — which is why `--format json` exists and why `render_text`'s bands must
never be the only output an analyst sees. This is not a defect to fix; it is a quantified
argument for a documentation sentence, and it generalises: **any quantiser AMF adds should
publish the Fano bound its bands imply.**

### 5.8 Stress dispersion entropy and its exact limit

Define, for a `SimulationTrace` step `x_t` with `‖x_t‖_1 > 0`, the **dispersion distribution**
`x̂_t(j) = x_t(j)/‖x_t‖_1` and the **dispersion entropy** `H_disp(t) = H(x̂_t)`. This measures
how widely stress is spread across the seven systems, is dimensionless, is a pure function of
structure, and contains no market data whatsoever.

For `Shock(circulatory, 0.8)` under default configuration:

| `t` | `‖x_t‖_1` | `H_disp(t)` (bits) | `D_1 = 2^{H_disp}` |
|---|---|---|---|
| 0 | `0.800000` | `0.000000` | `1.000` |
| 1 | `0.557600` | `1.350791` | `2.551` |
| 2 | `0.357967` | `1.900826` | `3.734` |
| 3 | `0.218803` | `2.127473` | `4.370` |
| 5 | `0.076052` | `2.273434` | `4.835` |
| 8 | `0.014847` | `2.304988` | `4.942` |
| 16 | `0.000195` | `2.301625` | `4.930` |
| 30 | `0.000000` | `2.301723` | `4.931` |

**Theorem 5.8 (asymptotic dispersion entropy).** Let `E` be as in §5.1 and let the `[0,1]` clip
be inactive for `t ≥ 1` (guaranteed when `ρ(E) < 1` and `‖x_0‖_∞ ≤ 1`). Decompose `E` into its
basic classes. Suppose there is a unique basic class `C` attaining `ρ(E)`, that `E|_C` is
primitive, and that the shock's support can reach `C`. Then `x̂_t → v`, the normalised dominant
left eigenvector of `E`, and hence `H_disp(t) → H(v)`, **independently of the shock magnitude
and of which reaching system is shocked.**
*Proof sketch.* `x_t = x_0 E^t`. Perron–Frobenius for primitive nonnegative matrices gives
`(E|_C)^t / ρ^t → v_C u_C^T` with `v_C > 0`; states outside `C` that are downstream of it are
forced at geometric rate `ρ` and, having local Perron roots `< ρ`, converge to fixed multiples
of the class amplitudes, while states not reachable from `C` decay at their own strictly
smaller rates and vanish in the normalised limit. Normalisation removes `ρ^t`, and `H` is
continuous on the simplex. ∎

On the sample market `E` has diagonal `0.425` throughout and the basic classes are
`{skeleton}`, `{circulatory, nervous, musculature}`, `{organs}`, `{immune}`, `{metabolism}`,
with the 3-cycle uniquely attaining

```
rho(E) = 0.5826132096
v      = (skeleton 0, circulatory 0.240375, nervous 0.193792, musculature 0.181486,
          organs 0.233340, immune 0, metabolism 0.151007)
H(v)   = 2.301722 bits,   D_1(v) = 4.9305 effective systems
```

matching the observed limit to six decimals. The predicted target-independence is exact:

| shocked system | `H_disp(∞)` | reaches the dominant class? |
|---|---|---|
| `skeleton` | `2.301723` | yes (via `circulatory`, `nervous`) |
| `circulatory` | `2.301722` | yes |
| `nervous` | `2.301722` | yes |
| `musculature` | `2.301722` | yes |
| `organs` | `0.346731` | no — reaches only `{organs, metabolism}` |
| `immune` | `0.000000` | no — pure sink |
| `metabolism` | `0.000000` | no — pure sink |

This is the closest thing in this module to the source note's item A ("market entropy as a risk
metric"), and it differs from it in every respect that matters: it is computed from structure
rather than prices, it is fully deterministic, it has a proof rather than a stylised narrative,
and it does not rise before anything. What it does say is genuinely useful — *a market has a
characteristic terminal stress-dispersion, fixed by its dominant cycle, that no shock location
inside that cycle can change.* A market whose `H_disp(∞)` is near `log 7` disperses stress
across everything; one near `0` funnels it into a sink.

### 5.9 The `Severity` map is a quantiser, and rate–distortion is its theory

`Severity.from_score` partitions `[0,1]` into four cells at `0.25, 0.50, 0.75`. Definition 2.22
gives the right frame: what is the least rate needed to preserve a chosen distortion on the
score? The nominal rate is `2` bits per finding; the *achieved* rate on the sample market is
`H(severity profile) = 0.591673` bits, because six of seven findings fall in one cell. A
uniform-in-`[0,1]` score would give the full `2` bits, so the current thresholds are badly
matched to the empirical range of scores AMF actually produces (all seven here lie in
`[0.093, 0.377]`). Rate–distortion says nothing about whether the thresholds are *right* — that
is a domain judgement — but it says precisely what they cost, and it makes "should the bands be
quantiles rather than fixed cut-points?" a question with a computable answer rather than a
matter of taste.

### 5.10 Algorithmic information: what NCD can and cannot do here

`Market.to_dict()` emits systems in `SystemKind` order and dependencies in declaration order, so
`json.dumps(market.to_dict(), sort_keys=True, separators=(",",":"))` is a canonical, byte-stable
string per market. `NCD` (Definition 2.33) with `C = zlib.compress` is then a computable
structural distance between two markets, needs no new dependency, and clusters families of
markets sensibly.

It is nonetheless the weakest instrument in this module and must be labelled as such.
`K` is uncomputable (Theorem 2.31), so `NCD` has no error bar and no convergence guarantee;
worse, the number it returns is a property of the *serialisation*, not of the market. Renaming
a component from `"NYSE"` to `"New York Stock Exchange"` changes it; adding whitespace changes
it; the `components` lists — free-text strings that no other part of AMF scores — dominate the
compressed length. Theorem 2.32 does not rescue this: LZ universality is an asymptotic
statement about stationary ergodic *sources*, and a single 2 kB JSON document is not a sample
from one. The defensible use is exploratory clustering of many markets with the `components`
fields stripped; the indefensible use is any per-market number reported as a score.

This is the honest verdict on the source note's item D. "Compressible ⇒ predictable" is a
theorem about entropy rate under hypotheses no market document satisfies, and using a
compression ratio as a marker of whether a policy "worked" is a validation claim (rule 2) built
on a statistic with no sampling distribution.

### 5.11 Where AMF actually has samples: the ensemble, and the bias that eats it

AMF has exactly one sampling mechanism: `ShockSimulator.ensemble(...)`, which runs `N` seeded,
jittered replications (replication `i` uses `base_seed + i`) into a `ResilienceDistribution`.
This is the only place a finite-sample entropy is even meaningful, and it is where
Proposition 2.38 bites.

Binning `N = 100` replications into `m = 20` cells and reporting the plug-in entropy carries a
downward bias of

```
(m - 1) / (2 N) = 19/200 = 0.095 nats = 0.137 bits
```

Compare that with §5.3's *entire* structural signal, `D(q ‖ u) = 0.0807` bits. **The estimator's
bias is 1.7× the quantity of interest.** Any ensemble-derived entropy that is reported without
the Miller–Madow correction `+(m̂-1)/(2N)` [44], or better a Grassberger [40], Chao–Shen [43] or
NSB [42] estimator, and without a bootstrap interval over seeds, is noise dressed as a finding.
For continuous quantities the `k`-NN estimator of Kraskov et al. [39] is the standard choice
precisely because it cancels the matched biases rather than correcting them afterwards.

This is also the reason §5.2–§5.9 are all *exact* rather than *estimated*: every one of them is
a function of the market's declared structure, computed with no sampling at all. That is a
design property worth protecting.

### 5.12 What items A–D of the source note become

| Source note | Status | Compliant AMF statement |
|---|---|---|
| **A.** Market entropy over `{bull, bear, crisis, recovery, chaotic}` from `P(p)` at time `t`; rises pre-crisis, peaks at crisis | Requires a price distribution and a regime labelling AMF does not have; the pre/peak/post narrative is an unvalidated empirical claim | Dispersion entropy `H_disp(t)` (§5.8) and weakness-profile entropy `H(q)` (§5.3): both exact, both structural, neither predictive |
| **B.** `I(Market_US; Market_EU)` in "bits/trade"; `0.3 → 0.8 → 0.2` as a contagion indicator | `trade` is `FORBIDDEN`; the three numbers are invented; "leading indicator" is a forecast claim | Structural coupling information `I(T;R)` (§5.5) between transmitter and receiver *within one market*; and, for two markets, `sqrt(JSD)` between their coupling distributions (Theorem 2.12) — symmetric, bounded, finite |
| **C.** `C = B log₂(1 + S/N)` for policy transmission; calibrate rate cuts to channel capacity | Shannon–Hartley's three hypotheses are all absent (§5.6); `signal` is `FORBIDDEN` | Blahut–Arimoto capacity `C*` of the normalised coupling kernel, plus the zero-error bracket (§5.6) |
| **D.** Lempel–Ziv compressibility of price histories as a predictability marker | Prices are `FORBIDDEN`; entropy-rate universality does not apply to a single document | `NCD` over canonicalised market JSON, for exploratory clustering only, with the caveats of §5.10 stated in the docstring |
| `D_KL(P‖Q)` for regime shift | Correct in form. Fails on support mismatch: `D = ∞` whenever a system's stress goes to exactly zero, which is routine (`skeleton`, `immune` in §5.8) | `JSD` or `sqrt(JSD)`; or `D` with an explicitly documented, config-validated smoothing floor |

### 5.13 Determinism requirements for any implementation

These are hard requirements, not style notes. Each has already been the cause of a
reproducibility bug in some information-theory codebase.

1. **Fix the base and state it.** Use base 2 everywhere and name it in the docstring. Mixing
   `math.log` and `math.log2` across modules is the classic source of factor-`ln 2` disputes.
2. **`0 log 0 := 0` as a total function.** Write `_xlogx(p)` returning `0.0` for `p <= 0.0`;
   never let `math.log2(0.0)` be reached. A negative `p` from floating-point drift must raise
   `InvalidConfigError`, not silently return `nan`.
3. **Sum in `SystemKind` declaration order.** Floating-point addition is not associative;
   `CLAUDE.md` already records that insertion-ordered traversal changed a diagnosis in its last
   bits. Every entropy sum here iterates `_ORDER`, and every joint sum iterates
   `(source, target, kind)` declaration order.
4. **Normalise once, explicitly.** Compute `Z` in canonical order, then divide; do not
   accumulate normalised terms.
5. **No iterative solver without a fixed stopping rule.** Blahut–Arimoto (§5.6) must run to a
   documented absolute tolerance *and* a documented iteration cap, with the cap a validated
   config field, and must return the same bits on every platform. Do not use a relative
   tolerance keyed to machine epsilon.
6. **Every threshold is an `InvalidConfigError`-validated knob.** `concentration_alpha α ≥ 0`;
   `capacity_tolerance > 0`; `capacity_max_iterations >= 1`; `smoothing_floor` in `[0, 1)`.
7. **Sampling stays behind a seed.** Anything estimated from `ensemble()` inherits
   `SimulationConfig.seed`; nothing new may introduce unseeded randomness.
8. **100 % statement and branch coverage.** Every guard above ships with the test that exercises
   it, in the same change. The fix for a failing gate is a test, never a lower threshold.

---

## 6. Repository governance and boundary analysis

Every artefact, formula and phrase the source note proposes is reproduced below and annotated.
Nothing is silently dropped and nothing is silently accepted.

| Proposed artefact / formula / phrase | Conflicts with which hard rule | Compliant reformulation |
|---|---|---|
| `docs/research/shannon_information_markets.md` — Theory + applications | None directly. Must **not** be added to `SHA256SUMS` (rule 4) and must carry the illustrative-only banner (rule 2) | Keep, or fold into this module. If kept, place under `docs/`, ensure the Markdown link-check job covers it, and open with the same status banner used here |
| `src/amf/information_theory/entropy_calculator.py` — H, I, KL divergence | **Rule 3** on layout and coverage, not on names: the package is flat modules, not sub-packages, and every branch of a new module must be covered. No forbidden substring in the path | `src/amf/information.py`, placed at the `graph`/`systems` layer (it depends only on `errors`, `models` and `graph`), exporting `entropy`, `relative_entropy`, `jensen_shannon`, `coupling_distribution`, `structural_coupling_information`, `dispersion_entropy`. Pure `math`, zero dependencies. Add each name to `__all__` (kept sorted) |
| `src/amf/information_theory/channel_capacity.py` — Policy signal capacity | **Rule 1** on the *contents*: `signal` is a `FORBIDDEN` substring, so `policy_signal_capacity`, `signal_strength`, `SignalCapacity` all fail `test_non_trading_boundary.py`. **Rule 3**: an iterative maximiser needs a fixed stopping rule to stay deterministic (§5.13 item 5) | `src/amf/capacity.py` exporting `structural_transmission_capacity(market, config)` and `CapacityConfig(tolerance, max_iterations)`, both `InvalidConfigError`-validated. Implements Blahut–Arimoto over the normalised `CouplingMatrix` (§5.6). Also expose `zero_error_bracket()` returning `(log α, C*)` |
| `examples/entropy_as_risk_metric.py` — Backtests on 2008, 2020, etc. | **Rule 1** three times over (`backtest` is `FORBIDDEN`; "2008, 2020" means price/return history; the file would need market data). **Rule 2**: "risk metric" validated against crises is a validated-performance claim. **Rule 3**: `tests/integration/test_examples.py` would need a case | `examples/structural_entropy.py`: build a market in code, print `H(q)`, `D(q‖u)`, `I(T;R)`, `C*`, and the `H_disp` trajectory for one shock, then the standard disclaimer. No external data, deterministic output, add a case to `test_examples.py` |
| `Price distribution: P(p) at time t` | **Rule 1** outright — `price` is `FORBIDDEN` | The dispersion distribution `x̂_t` of §5.8, or the normalised weakness profile `q` of §5.3 |
| `Market states: {bull, bear, crisis, recovery, chaotic}` | **Rule 2**: a regime labelling AMF neither defines nor estimates | `Severity` bands over structural scores; or, if genuinely needed, an explicit user-supplied partition documented as an input, never inferred |
| `H ≈ 0: … — low risk` / `H ≈ max: … — maximum risk` | **Rule 2**: asserts a risk semantics for entropy with no evidence. It is also *not obviously true*: §5.8 shows maximum dispersion entropy means stress spread thinly, which is the resilient case, not the dangerous one | State the direction as a falsifiable proposition (P5), or report `H` without a risk gloss |
| `Historical data: Measure H before/after crises` … `Pre-crisis: Entropy rises gradually` | **Rule 2** outright: an empirical regularity asserted as fact, and **rule 1** (historical market data) | Delete, or restate as P5/P6 in §7 with the refuting evidence named |
| `I ≈ 0.3 bits/trade` → `0.8` → `0.2` | **Rule 1** (`trade` is `FORBIDDEN`) and **rule 2** (three fabricated numbers presented as measurements) | Report `I(T;R)` in bits per coupling of a *given, hand-specified* market (§5.5). The sample market's value is `1.580897` bits and is a computed fact about that file |
| `Application: Monitor I as leading indicator of contagion` / `Threshold: If I(t) > threshold, markets are vulnerable to cascade` | **Rule 2** outright: "leading indicator" and "vulnerable to cascade" are forecast claims, and the threshold is uncalibrated | AMF already has a threshold mechanism with the right semantics: `SimulationConfig.cascade_threshold`, documented as an opt-in modelling choice, not a detector |
| `Fed announces rate cut: Signal = announcement strength` | **Rule 1** (`signal`) and **rule 2** (a monetary-policy transmission claim) | `Shock.magnitude` on the system in question; the note's "calibration" idea survives as the capacity bracket of §5.6, with no policy interpretation |
| `C = B log₂(1 + (policy_signal)?? / (market_noise)²)` | Mathematically inapplicable (§5.6); also literally corrupt — the exponent on the numerator is two `U+FFFD` replacement characters | `C* = max_p I(T;R)` over the normalised coupling kernel, by Blahut–Arimoto |
| `Lempel-Ziv compression … Market is random/chaotic → Unpredictable` | **Rule 1** (price histories) and **rule 2** (predictability claim). Also a misuse of Theorem 2.32, which is asymptotic and needs a stationary ergodic source | `NCD` over canonicalised market JSON for exploratory clustering only, with §5.10's caveats in the docstring; never a per-market score |
| `Compression ratio = marker of whether policy "worked"` | **Rule 2** outright | Drop. If a before/after structural comparison is wanted, use `sqrt(JSD)` between the two markets' coupling distributions — bounded, symmetric, and a metric [20] |
| Kelly (1956) as "the finance application" | **Rule 1**: the Kelly criterion is a bet-sizing rule defined through returns | Cite for intellectual history only, as §4.1 does, with the boundary note attached |
| `information_theory/` as a sub-package | **Rule 3** (layout convention) and a rule 1 tripwire on member names: the boundary test walks public members *and dataclass fields*, so `entropy_order`, `sort_order`, `byte_order`, `concentration_order` and anything `*_order` fail — and `order` is the conventional name for the Rényi parameter `α`, which makes this the likeliest single point of failure for this module. `CouplingMatrix.order` is the one documented `ALLOWLIST` entry and must not be joined by undocumented ones | Flat modules `src/amf/information.py` and `src/amf/capacity.py`; use `arrangement`, `sequence` or `_ORDER` (module-private, hence not walked) rather than a public `order` |

### 6.1 Dependency implications

Everything in §5 is computable with `math` alone. Entropies are sums of `p*log2(p)`;
Blahut–Arimoto is an alternating exponential-family update on a `5 × 7` array; the Perron
vector of Theorem 5.8 is a power iteration on a `7 × 7` matrix. No numpy, no scipy, no
compression library beyond `zlib` (standard library) for the optional, clearly-labelled NCD
helper. The zero-runtime-dependency rule is therefore not in tension with any of this
module's content — which is a strong argument for keeping it in-tree, in contrast with the
sidecar recommended for other modules in this series.

The one genuine risk is `zlib`: its output is not guaranteed byte-identical across zlib
versions, so any `NCD` value is only reproducible against a pinned implementation. That alone
disqualifies it from any output the CLI prints as a score, and is why §5.10 confines it to an
exploratory helper documented as version-dependent.

### 6.2 Determinism implications

§5.13 enumerates the eight requirements. Two deserve repeating at governance level. First,
`tests/unit/test_properties.py` asserts that a market and any permutation of its assembly order
diagnose *identically*; every quantity added by this module is a sum over systems or couplings
and must therefore iterate in `SystemKind` (and `(source, target, kind)`) declaration order, or
that property test will fail in the last bits and correctly so. Second, Blahut–Arimoto is the
first iterative numerical routine that would enter `src/amf`. Its stopping rule must be a
documented absolute tolerance plus a hard iteration cap, both validated config fields; an
adaptive or epsilon-keyed tolerance would make the published capacity platform-dependent.

### 6.3 Validation-claim implications

Nothing in §5 is calibrated against anything. `α = 2`, the `Severity` cut-points, the
`0.4/0.3/0.3` diagnostic blend and the `0.6/0.25/0.15` resilience blend are all free parameters
chosen for convenience. Adding entropies to the report does not change that and must not be
allowed to imply otherwise: entropy carries a physics-adjacent authority that makes
over-reading easy. Concretely, the following sentences are rule-2 violations however they are
dressed — *"entropy rises before instability"*, *"mutual information leads contagion"*,
*"capacity tells you how large an intervention can be"*, *"low compressibility means
unpredictable"*. The permitted register is the one §5 uses throughout: *this market, this
file, this number, this proof.*

---

## 7. Falsifiable propositions and open questions

The source note for Q3 contains no "Key Research Questions" heading — unlike its siblings, its
research programme is stated implicitly inside items A–D and the "Mathematical Framework"
block. Those implicit claims are restated below in refutable form as P1–P6, with P7–P15
extending them. Each names the evidence that would settle it.

**P1 (concentration is a Rényi-2 entropy).** *Claim (Theorem 5.2):* for every market and every
system with non-empty reliance, `DiagnosticEngine.concentration` returns exactly
`2^{-H_2(π_i)}`. *Falsifier:* a market where the two differ by more than floating-point noise.
This is the cheapest test in this module and should be written first; it is a pure identity.

**P2 (the Hill ordering constrains any re-parameterisation).** *Claim:* for every reliance
profile, `D_0 ≥ D_1 ≥ D_2 ≥ D_∞`, so replacing HHI by any `α > 2` reports *more* concentration
and any `α < 2` reports less, monotonically. *Falsifier:* a profile violating the ordering,
which would indicate a bug in the implementation of `H_α`, since the inequality is a theorem
[9].

**P3 (mutual information is the maxent divergence).** *Claim (Theorem 5.5):* `I(T;R)` computed
from the coupling distribution equals `D(P ‖ P_T ⊗ P_R)` computed independently, and equals
`1.580897` bits on `examples/sample_market.json`. *Falsifier:* disagreement beyond tolerance
between the two computations, or a different value from the shipped sample file.

**P4 (the sample market's transmission is almost zero-error).** *Claim (§5.6):* `C* = 2.001532`
bits/step and the confusability graph has independence number `4`, so
`2.000000 ≤ C_0 ≤ 2.001532`. *Falsifier:* a Blahut–Arimoto implementation converging to a
different `C*`, or an independent set of size `5` in the confusability graph. Stronger open
form: is the near-coincidence `C_0 ≈ C*` generic for sparse AMF markets, or an accident of this
one? Compute both over a family of generated markets and report the distribution of `C* - log α`.

**P5 (entropy and risk point the same way).** *Claim, restating the source note's item A:*
higher structural entropy indicates higher risk. *Falsifier:* §5.8 already refutes the naive
form — maximum dispersion entropy means stress spread thinly across all seven systems, which
under AMF's own `resilience` metric scores *better*, not worse. The claim survives only if
restated for a specific entropy and a specific risk quantity, with the sign predicted in
advance. *Concrete test:* over a generated family of markets, is the correlation between
`H_disp(∞)` and `ResilienceScore.value` positive or negative? Whichever it is, the note asserts
the opposite for at least one of them.

**P6 (mutual information tracks coupling, monotonically).** *Claim, restating item B:* higher
`I` means "more coupled". *Falsifier:* a pair of markets where the more strongly coupled one
(larger total edge weight) has *lower* `I(T;R)`. This is easy to construct — `I` is a function
of the *shape* of the coupling distribution, invariant to a global rescaling of every weight —
so the claim as stated is false and must be replaced by "higher `I` means coupling is more
channelled through specific pairs". Confirming that the counterexample exists is a two-market
test.

**P7 (default AMF trajectories have zero permutation entropy).** *Claim:* under default
`SimulationConfig`, the total-stress trajectory `‖x_t‖_1` is strictly decreasing after `t = 0`,
so its permutation entropy at embedding dimension `D = 3` is exactly `0` bits and only `1` of
the `6` ordinal patterns occurs. *Falsifier:* a market and a shock whose default trajectory is
non-monotone. (Verified `0.000000` on the sample market; a cascade-threshold or recovery-rate
configuration is expected to break monotonicity, which is precisely the interesting case.)

**P8 (dispersion entropy has a shock-independent limit).** *Claim (Theorem 5.8):* `H_disp(∞)`
depends only on which basic class the shock reaches, not on the shocked system within that
class nor on the magnitude. *Falsifier:* two shocks reaching the same dominant class whose
limits differ by more than tolerance, or a magnitude-dependence. Note the theorem's hypotheses:
the clip must stay inactive, the dominant basic class must be unique and primitive. A market
with two basic classes tied at `ρ(E)` is the designed counterexample and would be worth
exhibiting.

**P9 (Fano bound on band-only inference).** *Claim (§5.7):* an analyst restricted to the
`Severity` bands of the sample market cannot identify the weakest system with error below
`0.6826`. *Falsifier:* an inference procedure using only the bands that beats it — impossible,
since Fano is a theorem, so a claimed counterexample necessarily uses information beyond the
bands. The productive version is empirical: across generated markets, how often does the modal
band contain `≥ 5` systems? If usually, the current cut-points are the wrong quantiser.

**P10 (severity bands under-use their nominal rate).** *Claim (§5.9):* over any realistic family
of markets, `H(Severity profile) ≪ 2` bits. *Falsifier:* a generated family whose band profile
approaches `2` bits, which would mean the fixed cut-points are well matched after all.
Sample-market value: `0.591673` bits.

**P11 (structural information is not explained by strengths).** *Claim:* for realistic markets
`I(T;R)` is a substantial fraction of `H(T,R)` — `53.7 %` on the sample market. *Falsifier:* a
family of markets where `I(T;R)/H(T,R)` is near zero, i.e. the coupling really is a product of
its marginals. This would mean `maxent_coupling` is a sufficient statistic for the market and
the pair structure is decorative — an important negative result if true.

**P12 (estimator bias dominates ensemble entropy).** *Claim (§5.11):* at `N = 100`, `m = 20`,
the plug-in bias `0.137` bits exceeds the structural signal `0.081` bits. *Falsifier:* a
bias-corrected ensemble entropy whose bootstrap interval over seeds excludes the corrected
plug-in value by less than the correction — i.e. show the correction does not matter at AMF's
ensemble sizes. Until then, no uncorrected ensemble entropy may be reported.

**P13 (transfer entropy has no referent in AMF).** *Claim, deliberately stated so it can lose:*
there is no pair of AMF-representable quantities for which transfer entropy is both computable
and informative, because AMF's only time series is deterministic given the market, so all
conditional mutual informations among its components are exactly `0`. *Falsifier:* exhibit a
seeded ensemble configuration under which `T_{Y→X}` between two systems' stress trajectories is
significantly non-zero against a shuffled null. Note the estimator warning of Caution 2.37 and
the bias history of [57] before believing any positive result.

**P14 (NCD is a serialisation artefact).** *Claim (§5.10):* `NCD` between two markets changes
by more than `0.05` under a pure renaming of `components` strings that leaves every metric and
every dependency untouched. *Falsifier:* an invariant canonicalisation for which it does not.
If someone finds one, `NCD` becomes usable; until then it does not.

**P15 (open question: is there a market-side referent for "market entropy" at all?).** The
economics literature already has a theory of information in prices [61, 62] under which a fully
informative price system is self-defeating, and an adaptive refinement [63]. The econophysics
literature has entropy-based efficiency proxies [60] and transfer-entropy flow maps [57, 58].
These two literatures rarely cite each other, and the source note cites neither. *Open
question:* for any structural entropy defined in §5, is there a market-observable quantity it
is even in principle a proxy for — and if so, does the mapping survive the four failure modes
catalogued in [67]? A negative answer would be a perfectly good result and would justify
keeping every quantity in this module explicitly structural, which is where §6 leaves them.

---

## 8. Deliverables

The source note's deliverable list, reproduced exactly as written, with compliance status.

| Deliverable (verbatim) | Status | Compliance note |
|---|---|---|
| `docs/research/shannon_information_markets.md` — Theory + applications | **Accept with conditions** | Not to be added to `SHA256SUMS`; must carry the illustrative-only banner; covered by the Markdown link-check job. Superseded in practice by this module |
| `src/amf/information_theory/entropy_calculator.py` — H, I, KL divergence | **Accept, relocated and renamed** | Ship as `src/amf/information.py` (flat module, `errors`/`models`/`graph` layer). Exports `entropy`, `relative_entropy`, `jensen_shannon`, `coupling_distribution`, `structural_coupling_information`, `dispersion_entropy`, `maxent_coupling`. Pure `math`; 100 % branch coverage; results in bits; `0 log 0 := 0` |
| `src/amf/information_theory/channel_capacity.py` — Policy signal capacity | **Reject as named; accept the mathematics** | `signal` is a `FORBIDDEN` substring, and Shannon–Hartley does not apply (§5.6). Ship as `src/amf/capacity.py` with `structural_transmission_capacity` + `CapacityConfig(tolerance, max_iterations)` and `zero_error_bracket`, implementing Blahut–Arimoto with a fixed stopping rule |
| `examples/entropy_as_risk_metric.py` — Backtests on 2008, 2020, etc. | **Reject** | `backtest` is `FORBIDDEN`; the example requires price history; "risk metric" validated on crises is a rule-2 claim. Replace with `examples/structural_entropy.py` (§6 table) and add a case to `tests/integration/test_examples.py` |

Additional deliverables this module recommends, none of which appear in the source note:

| Deliverable | Rationale |
|---|---|
| `tests/unit/test_information.py` with the identity `concentration == 2^{-H_2}` (P1) | The cheapest possible check that the new module and the old one agree |
| `tests/unit/test_properties.py`: hypothesis property that every entropy returned lies in `[0, log 7]` and is permutation-invariant | Matches the existing invariants the docstrings promise |
| `DiagnosticConfig.concentration_alpha: float = 2.0` (**not** `concentration_order` — `order` is `FORBIDDEN`) | Makes the current `α = 2` an explicit, validated default rather than an unexamined constant (§5.2) |
| A `render_text` line reporting `D(q ‖ uniform)` alongside the overall index | One number that tells a reader whether the ranking above it is meaningful at all (§5.3) |
| A CHANGELOG entry under `## [Unreleased]` → *Added* | Required by the contributor checklist for any user-visible change |

---

## 9. Research leadership and prerequisites

The source note's line, verbatim:

> **Research Leaders Needed**: Information theorist, complexity scientist

That is the right pair, and it is incomplete for this repository. The work in §5 is
information theory; the work in §6 is software governance; the work in §7 is statistics. A
skills matrix that would actually staff this module:

| Role | Must be able to | Owns which sections | Failure mode if absent |
|---|---|---|---|
| Information theorist | State Theorems 2.13, 2.15, 2.19, 2.20 with hypotheses; run Blahut–Arimoto by hand on a `3 × 3` channel; explain why differential entropy is not entropy | §2, §5.4–§5.7 | Shannon–Hartley applied to a system with no noise model — exactly the source note's item C |
| Complexity scientist | Distinguish Kolmogorov complexity from compression ratio, and entropy rate from single-document compressibility | §5.10, §2.5 | "Compressible ⇒ predictable" shipped as a feature |
| Applied statistician / estimation specialist | Derive the `(m-1)/2N` bias; choose between Miller–Madow, Grassberger, Chao–Shen, NSB and `k`-NN and say why | §5.11, P12 | Ensemble entropies reported with bias larger than the effect |
| Numerical analyst | Reason about floating-point non-associativity and fixed stopping rules | §5.13, §6.2 | A capacity that differs in the last bits between CI runners |
| Graph theorist / linear algebraist | Perron–Frobenius, basic-class decomposition, independence number | Theorem 5.8, §5.6 | A dispersion-entropy limit asserted without its hypotheses |
| Financial economist | Know [61, 62, 63] and what "information" already means in that literature | §4.5, P15 | Rediscovering the Grossman–Stiglitz paradox under a new name |
| Repository maintainer | Know the `FORBIDDEN` list, the `ALLOWLIST`, the one-way dependency order, and the 100 % gate | §6, §8 | A PR that fails `test_non_trading_boundary.py` on the word `signal` |

**Prerequisite ladder, undergraduate to frontier.**

1. *UG2* — Discrete probability; Jensen's inequality; convexity. Cover & Thomas [49] Ch. 2 is
   readable at this point with effort.
2. *UG3* — Linear algebra of nonnegative matrices; Perron–Frobenius. Needed for Theorem 5.8.
3. *UG4* — Core information theory: entropy, mutual information, chain rules, DPI, Fano, AEP,
   source coding. MIT 6.441 or Stanford EE376A; [49] Ch. 2–5, [50] Ch. 1–6.
4. *PG1* — Channel coding and capacity computation; Blahut–Arimoto; rate–distortion. [49] Ch. 7,
   Ch. 10; Caltech EE/Ma/CS 126 or Berkeley 229A.
5. *PG1* — Differential entropy and the Gaussian channel; the exact hypotheses of
   Shannon–Hartley. [49] Ch. 8–9.
6. *PG2* — Maximum-entropy inference and exponential families; Jaynes [7, 8]; [50] Ch. 22–23.
7. *PG2* — Generalised entropies and Hill numbers; Rényi [9]. Needed to read §5.2 as more than
   an identity.
8. *PG2* — Estimation theory for entropy and mutual information; Paninski [41] is the gate.
9. *PG3* — Algorithmic information theory; Li & Vitányi [55] Ch. 2–3, 8.
10. *PG3* — Directed information, transfer entropy, and the critiques [37, 38]; Bossomaier et
    al. [56].
11. *Frontier* — The open question of P15: whether any structural entropy has a market-side
    referent that survives [67]'s four failure modes. Nobody currently knows, and answering it
    negatively would be as valuable as answering it positively.

A contributor who has completed rungs 1–4 can implement all of §5 correctly. A contributor who
stops at rung 3 will implement §5.6 as Shannon–Hartley and will be wrong.

---

## References

- [1] C. E. Shannon, "A mathematical theory of communication", *The Bell System Technical
  Journal* **27**(3), 379–423 and **27**(4), 623–656 (1948).
- [2] C. E. Shannon, "Communication in the presence of noise", *Proceedings of the IRE*
  **37**(1), 10–21 (1949).
- [3] C. E. Shannon, "The zero error capacity of a noisy channel", *IRE Transactions on
  Information Theory* **2**(3), 8–19 (1956).
- [4] C. E. Shannon, "Coding theorems for a discrete source with a fidelity criterion", *IRE
  National Convention Record*, Part 4, 142–163 (1959).
- [5] R. V. L. Hartley, "Transmission of information", *The Bell System Technical Journal*
  **7**(3), 535–563 (1928).
- [6] S. Kullback and R. A. Leibler, "On information and sufficiency", *The Annals of
  Mathematical Statistics* **22**(1), 79–86 (1951).
- [7] E. T. Jaynes, "Information theory and statistical mechanics", *Physical Review*
  **106**(4), 620–630 (1957).
- [8] E. T. Jaynes, "Information theory and statistical mechanics. II", *Physical Review*
  **108**(2), 171–190 (1957).
- [9] A. Rényi, "On measures of entropy and information", in *Proceedings of the Fourth Berkeley
  Symposium on Mathematical Statistics and Probability*, Volume 1, University of California
  Press, 547–561 (1961).
- [10] C. Tsallis, "Possible generalization of Boltzmann-Gibbs statistics", *Journal of
  Statistical Physics* **52**(1–2), 479–487 (1988).
- [11] B. McMillan, "The basic theorems of information theory", *The Annals of Mathematical
  Statistics* **24**(2), 196–219 (1953).
- [12] L. Breiman, "The individual ergodic theorem of information theory", *The Annals of
  Mathematical Statistics* **28**(3), 809–811 (1957).
- [13] B. McMillan, "Two inequalities implied by unique decipherability", *IRE Transactions on
  Information Theory* **2**(4), 115–116 (1956).
- [14] L. G. Kraft, *A Device for Quantizing, Grouping, and Coding Amplitude-Modulated Pulses*,
  M.Sc. thesis, Massachusetts Institute of Technology (1949).
- [15] R. M. Fano, *Transmission of Information: A Statistical Theory of Communications*, MIT
  Press and John Wiley & Sons (1961).
- [16] M. S. Pinsker, *Information and Information Stability of Random Variables and Processes*,
  Holden-Day (1964), translated and edited by A. Feinstein.
- [17] I. Csiszár, "Information-type measures of difference of probability distributions and
  indirect observations", *Studia Scientiarum Mathematicarum Hungarica* **2**, 299–318 (1967).
- [18] S. Kullback, "A lower bound for discrimination information in terms of variation",
  *IEEE Transactions on Information Theory* **13**(1), 126–127 (1967).
- [19] J. Lin, "Divergence measures based on the Shannon entropy", *IEEE Transactions on
  Information Theory* **37**(1), 145–151 (1991).
- [20] D. M. Endres and J. E. Schindelin, "A new metric for probability distributions", *IEEE
  Transactions on Information Theory* **49**(7), 1858–1860 (2003).
- [21] R. E. Blahut, "Computation of channel capacity and rate-distortion functions", *IEEE
  Transactions on Information Theory* **18**(4), 460–473 (1972).
- [22] S. Arimoto, "An algorithm for computing the capacity of arbitrary discrete memoryless
  channels", *IEEE Transactions on Information Theory* **18**(1), 14–20 (1972).
- [23] L. Lovász, "On the Shannon capacity of a graph", *IEEE Transactions on Information
  Theory* **25**(1), 1–7 (1979).
- [24] R. J. Solomonoff, "A formal theory of inductive inference. Part I", *Information and
  Control* **7**(1), 1–22 (1964).
- [25] A. N. Kolmogorov, "Three approaches to the quantitative definition of information",
  *Problems of Information Transmission* **1**(1), 1–7 (1965).
- [26] G. J. Chaitin, "On the length of programs for computing finite binary sequences",
  *Journal of the ACM* **13**(4), 547–569 (1966).
- [27] A. Lempel and J. Ziv, "On the complexity of finite sequences", *IEEE Transactions on
  Information Theory* **22**(1), 75–81 (1976).
- [28] J. Ziv and A. Lempel, "A universal algorithm for sequential data compression", *IEEE
  Transactions on Information Theory* **23**(3), 337–343 (1977).
- [29] J. Ziv and A. Lempel, "Compression of individual sequences via variable-rate coding",
  *IEEE Transactions on Information Theory* **24**(5), 530–536 (1978).
- [30] M. Li, X. Chen, X. Li, B. Ma and P. M. B. Vitányi, "The similarity metric", *IEEE
  Transactions on Information Theory* **50**(12), 3250–3264 (2004).
- [31] R. Cilibrasi and P. M. B. Vitányi, "Clustering by compression", *IEEE Transactions on
  Information Theory* **51**(4), 1523–1545 (2005).
- [32] T. Schreiber, "Measuring information transfer", *Physical Review Letters* **85**(2),
  461–464 (2000).
- [33] H. Marko, "The bidirectional communication theory — a generalization of information
  theory", *IEEE Transactions on Communications* **21**(12), 1345–1351 (1973).
- [34] J. L. Massey, "Causality, feedback and directed information", in *Proceedings of the 1990
  International Symposium on Information Theory and its Applications (ISITA-90)*, 303–305 (1990).
- [35] C. W. J. Granger, "Investigating causal relations by econometric models and cross-spectral
  methods", *Econometrica* **37**(3), 424–438 (1969).
- [36] L. Barnett, A. B. Barrett and A. K. Seth, "Granger causality and transfer entropy are
  equivalent for Gaussian variables", *Physical Review Letters* **103**(23), 238701 (2009).
- [37] R. G. James, N. Barnett and J. P. Crutchfield, "Information flows? A critique of transfer
  entropies", *Physical Review Letters* **116**(23), 238701 (2016).
- [38] D. A. Smirnov, "Spurious causalities with transfer entropy", *Physical Review E*
  **87**(4), 042917 (2013).
- [39] A. Kraskov, H. Stögbauer and P. Grassberger, "Estimating mutual information", *Physical
  Review E* **69**(6), 066138 (2004).
- [40] P. Grassberger, "Finite sample corrections to entropy and dimension estimates", *Physics
  Letters A* **128**(6–7), 369–373 (1988).
- [41] L. Paninski, "Estimation of entropy and mutual information", *Neural Computation*
  **15**(6), 1191–1253 (2003).
- [42] I. Nemenman, F. Shafee and W. Bialek, "Entropy and inference, revisited", in *Advances in
  Neural Information Processing Systems 14*, MIT Press (2002).
- [43] A. Chao and T.-J. Shen, "Nonparametric estimation of Shannon's index of diversity when
  there are unseen species in sample", *Environmental and Ecological Statistics* **10**(4),
  429–443 (2003).
- [44] G. A. Miller, "Note on the bias of information estimates", in H. Quastler (ed.),
  *Information Theory in Psychology: Problems and Methods*, Free Press (1955).
- [45] S. M. Pincus, "Approximate entropy as a measure of system complexity", *Proceedings of the
  National Academy of Sciences of the USA* **88**(6), 2297–2301 (1991).
- [46] J. S. Richman and J. R. Moorman, "Physiological time-series analysis using approximate
  entropy and sample entropy", *American Journal of Physiology — Heart and Circulatory
  Physiology* **278**(6), H2039–H2049 (2000).
- [47] C. Bandt and B. Pompe, "Permutation entropy: a natural complexity measure for time
  series", *Physical Review Letters* **88**(17), 174102 (2002).
- [48] J. L. Kelly, Jr., "A new interpretation of information rate", *The Bell System Technical
  Journal* **35**(4), 917–926 (1956). *Cited for history only; its betting framing lies outside
  this repository's non-trading boundary.*
- [49] T. M. Cover and J. A. Thomas, *Elements of Information Theory*, 2nd ed.,
  Wiley-Interscience (2006).
- [50] D. J. C. MacKay, *Information Theory, Inference, and Learning Algorithms*, Cambridge
  University Press (2003).
- [51] I. Csiszár and J. Körner, *Information Theory: Coding Theorems for Discrete Memoryless
  Systems*, 2nd ed., Cambridge University Press (2011).
- [52] R. M. Gray, *Entropy and Information Theory*, 2nd ed., Springer (2011).
- [53] R. W. Yeung, *Information Theory and Network Coding*, Springer (2008).
- [54] T. Berger, *Rate Distortion Theory: A Mathematical Basis for Data Compression*,
  Prentice-Hall (1971).
- [55] M. Li and P. M. B. Vitányi, *An Introduction to Kolmogorov Complexity and Its
  Applications*, 3rd ed., Springer (2008).
- [56] T. Bossomaier, L. Barnett, M. Harré and J. T. Lizier, *An Introduction to Transfer
  Entropy: Information Flow in Complex Systems*, Springer (2016).
- [57] R. Marschinski and H. Kantz, "Analysing the information flow between financial time
  series — an improved estimator for transfer entropy", *The European Physical Journal B*
  **30**(2), 275–281 (2002).
- [58] O. Kwon and J.-S. Yang, "Information flow between stock indices", *EPL (Europhysics
  Letters)* **82**(6), 68003 (2008).
- [59] A. Dionisio, R. Menezes and D. A. Mendes, "Mutual information: a measure of dependency for
  nonlinear time series", *Physica A: Statistical Mechanics and its Applications* **344**(1),
  326–329 (2004).
- [60] L. Zunino, M. Zanin, B. M. Tabak, D. G. Pérez and O. A. Rosso, "Forbidden patterns,
  permutation entropy and stock market inefficiency", *Physica A: Statistical Mechanics and its
  Applications* **388**(14), 2854–2864 (2009).
- [61] E. F. Fama, "Efficient capital markets: a review of theory and empirical work", *The
  Journal of Finance* **25**(2), 383–417 (1970).
- [62] S. J. Grossman and J. E. Stiglitz, "On the impossibility of informationally efficient
  markets", *The American Economic Review* **70**(3), 393–408 (1980).
- [63] A. W. Lo, "The adaptive markets hypothesis", *The Journal of Portfolio Management*
  **30**(5), 15–29 (2004).
- [64] R. Cont, "Empirical properties of asset returns: stylized facts and statistical issues",
  *Quantitative Finance* **1**(2), 223–236 (2001).
- [65] M. Billio, M. Getmansky, A. W. Lo and L. Pelizzon, "Econometric measures of connectedness
  and systemic risk in the finance and insurance sectors", *Journal of Financial Economics*
  **104**(3), 535–559 (2012).
- [66] F. X. Diebold and K. Yılmaz, "On the network topology of variance decompositions:
  measuring the connectedness of financial firms", *Journal of Econometrics* **182**(1),
  119–134 (2014).
- [67] M. Gallegati, S. Keen, T. Lux and P. Ormerod, "Worrying trends in econophysics", *Physica
  A: Statistical Mechanics and its Applications* **370**(1), 1–6 (2006).
- [68] D. Sornette, "Physics and financial economics (1776–2014): puzzles, Ising and agent-based
  models", *Reports on Progress in Physics* **77**(6), 062001 (2014).
- [69] D. Goldberg, "What every computer scientist should know about floating-point arithmetic",
  *ACM Computing Surveys* **23**(1), 5–48 (1991).

---

*Standing disclaimer for this module, as for the whole repository: the `amf` package is an
illustrative, educational toolkit. Its thresholds, weights and scores are not empirically
validated. Nothing here is financial advice, and nothing here is a diagnosis or forecast of any
real market. Every number quoted in §5 is a computed property of a file committed to this
repository, not a measurement of the world.*
