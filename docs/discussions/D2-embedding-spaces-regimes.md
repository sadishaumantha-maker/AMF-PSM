# D2: Embedding Spaces & Latent Representations of Market Regimes

> **Discussion category**: Research · **Labels**: `theory`, `representation-learning`,
> `dimensionality-reduction`, `boundary-review`, `needs-reformulation`, `not-validated`
> **Source**: `docs/QUANTUM_NEURAL_RESEARCH.md` § Discussion D2
> **Status**: Open for comment · **Nature**: Theoretical module, illustrative and not
> empirically validated

## 0. Abstract and reading guide

This module asks whether learned latent representations give AMF anything its hand-designed
structural encoder does not. It claims four things. First, that AMF's ambient state space is
already small: a complete market is 28 metric coordinates plus at most 42 pair-aggregated
coupling weights, so the note's premise — "1000+ features → 128D" — is inverted, and a 128-
dimensional latent would be an *expansion* of the data by a factor of roughly two. Second,
that the diagnostic pipeline is itself an exact, deterministic, identifiable encoder, and
that it factors through a strict ladder `R^196 → R^70 → R^28 → R^14 → R` (Proposition 5.3).
Third, that three of the note's four interpretability wishes have exact closed-form answers
inside the boundary: per-system attribution is the Shapley value of an additive game and is
computable in seven terms with no sampling (Theorem 5.6); the "2D projection of embedding
space" is classical MDS, which on the sample market places 98.45% of the diagnostic variance
in two coordinates; and the coupling matrix has a five-dimensional exact spectral embedding.
Fourth, that the learned alternatives fail on data grounds, not on taste: unsupervised
disentanglement is provably impossible without inductive bias (Theorem 2.14), InfoNCE cannot
certify more than `log K` nats from `K` samples (Theorem 2.17), and analogue search over a
70-dimensional descriptor needs a library of order `10^48` markets (§5.9).

It does **not** claim that any construction here forecasts, diagnoses, or describes a real
market; that latent geometry corresponds to anything economic; or that any threshold, weight,
or dimension count below has been empirically validated. Nothing here is financial advice.

**Prerequisite ladder.** Linear algebra and the SVD ([95] Ch. 2, 7) → spectral theory of
symmetric and nonnegative matrices ([95] Ch. 4, 8) → measure-theoretic probability and
Kullback–Leibler divergence → classical dimensionality reduction ([88] Ch. 14; [89]; [90])
→ spectral graph theory and diffusion operators ([92]; [93]; [16]; [17]) → variational
inference ([27]; [28]; [85] Ch. 10) → the VAE and its pathologies ([25]; [26]; [33]; [34])
→ identifiability and nonlinear ICA ([36]; [37]; [38]) → contrastive estimation and its
information-theoretic ceiling ([43]; [48]; [49]; [50]) → cooperative game theory ([74];
[75]; [99]). §2 states what is needed; §5 assumes all of it; §§6–9 assume none of it.

## 1. Verbatim source specification

The following is the complete text of Discussion D2 as it appears in
`docs/QUANTUM_NEURAL_RESEARCH.md`, reproduced word for word, including its notation,
typography, arrows, spacing, and deliverable paths. It is quoted, not endorsed; §5 develops
it and §6 names where it collides with this repository's hard rules.

````markdown
### Discussion D2: Embedding Spaces & Latent Representations of Market Regimes
**Theme**: Learn compressed "embeddings" that capture market regime structure

**Concept**:
- High-dimensional data (1000+ features) → Low-dimensional embeddings (e.g., 128D)
- Embeddings capture "semantic meaning" (e.g., 2D plot shows bull/bear axis)
- Similar to: Word embeddings in NLP (word2vec, GPT)

**Application to Markets**:

1. **Regime Embeddings**
   ```
   Each market state (bull, bear, crisis, recovery, regime-shift) 
   → Compressed 128D vector
   
   Properties: Similar states → Similar embeddings (close in latent space)
   Example:
     bull_2000 ≈ bull_2016 (similar embeddings, different times)
     crisis_2008 ≠ crisis_2020 (different mechanisms, far apart)
   
   Benefit: Generalize across time; identify "new" crisis types
   ```

2. **Asset Embeddings**
   ```
   Each asset (AAPL, BND, EURUSD, Oil, ...)
   → Compressed 128D vector capturing its "role in system"
   
   Properties:
     Tech stocks cluster together
     Bond yields near Fed rate
     Commodities form separate group
   
   Interpretation: Show 2D projection of embedding space
   → Visual map of market structure
   ```

3. **Policy Embeddings**
   ```
   Each policy action (rate cut, QE, regulation change, ...)
   → Compressed vector encoding its effect
   
   Similar policies → Similar embeddings
   Example:
     Fed 50bp cut 2008 ≈ Fed 75bp cut 2020 (similar urgency/impact)
     ECB taper 2015 ≠ ECB taper 2022 (different contexts)
   ```

**Embedding Methods**:

1. **Variational Autoencoder (VAE)**
   - Learns probabilistic latent space
   - Can sample from latent space to generate new market scenarios
   ```
   Encoder: Market data → Latent distribution (mean, std)
   Reparameterization: Sample from distribution
   Decoder: Latent sample → Reconstructed market data
   
   Loss = Reconstruction error + KL divergence (regularization)
   ```

2. **Contrastive Learning**
   - Learn embeddings where similar regimes are close, different regimes far
   ```
   Training pairs:
     (bull_2000, bull_2016) → similarity = high → small distance
     (bull_2000, crisis_2008) → similarity = low → large distance
   
   Loss = Contrastive loss (e.g., triplet loss)
   ```

3. **Self-Supervised Pre-training**
   - Use unlabeled market data to pre-train embeddings
   - Then fine-tune on labeled data (crisis/non-crisis, etc.)
   ```
   Pre-training tasks:
     - Predict next price given past (next-token prediction)
     - Masked market modeling (mask some data, predict it)
     - Contrastive: Similar time periods have similar embeddings
   ```

**Interpretability**:
- **UMAP/t-SNE**: Project 128D embeddings to 2D for visualization
- **SHAP values**: Which features contributed most to each embedding
- **Nearest neighbors**: Find similar past regimes (analog forecasting)

**Deliverable**:
- `docs/research/embedding_spaces_market_regimes.md` — Theory + methods
- `src/amf/embeddings/regime_vae.py` — Variational autoencoder
- `src/amf/embeddings/contrastive_embeddings.py` — Contrastive learning
- `src/amf/embeddings/embedding_visualizer.py` — 2D projection + interpretation
- `examples/regime_embedding_analogues.py` — Find similar past regimes

**Research Leaders Needed**: Deep learning researcher, dimensionality reduction expert
````

---

## 2. Formal foundations

Throughout, `X` is a set of objects to be represented, `d_X` a (pseudo)metric on it, and
`f: X → R^k` a candidate representation. Vectors are columns; `||·||` is Euclidean unless
subscripted. `[n] = {1, …, n}`.

### 2.1 Embeddings, distortion, and what "low-dimensional" means

**Definition 2.1 (embedding, distortion).** A map `f: (X, d_X) → (R^k, ||·||)` has
*distortion* `D ≥ 1` if there is `c > 0` with

```
c · d_X(x, y)  ≤  ||f(x) − f(y)||  ≤  c · D · d_X(x, y)     for all x, y ∈ X.
```

`f` is an *isometry* when `D = 1`. Every statement below about "a 128-dimensional
embedding" is empty until `d_X` and the admissible `D` are fixed; the source note fixes
neither.

**Definition 2.2 (manifold hypothesis).** Data drawn from `R^D` are said to satisfy the
manifold hypothesis if their support is (close to) a smooth `d`-dimensional submanifold with
`d ≪ D`. Fefferman, Mitter and Narayanan [19] made this testable: they give an algorithm
that, from finitely many samples, decides with high probability whether the data lie within
`ε` of some `d`-manifold of bounded reach and volume, with sample complexity independent of
the ambient dimension `D`. The hypothesis is therefore a *falsifiable* claim about a dataset,
not a modelling convenience.

**Theorem 2.3 (Whitney embedding, easy version; Whitney 1936 [11]).** Every smooth,
second-countable `d`-manifold admits a smooth embedding into `R^{2d+1}`. (Whitney later
improved the target to `R^{2d}`.) *Consequence for practice*: `2d+1` coordinates always
suffice to represent a `d`-dimensional structure without self-intersection; a latent
dimension far above `2d+1` buys no expressive power, only unidentifiability.

**Theorem 2.4 (delay embedding; Takens 1981 [12], fractal version Sauer–Yorke–Casdagli
1991 [13]).** Let `φ_t` be a smooth flow on a compact `d`-manifold `M` and `h: M → R` a
generic observable. For `k > 2d` the delay map `x ↦ (h(x), h(φ_τ x), …, h(φ_{(k−1)τ} x))` is
generically an embedding of `M` into `R^k`. Sauer et al. weaken the hypothesis: `k > 2·box-
counting dimension` suffices for a set of fractal dimension. This is the theorem that
licenses "reconstruct the regime from a window of history" — and it requires a *deterministic
dynamical system on a compact attractor*, an assumption no one has established for markets.

**Theorem 2.5 (Johnson–Lindenstrauss 1984 [10]).** For any `0 < ε < 1` and any `n` points in
`R^D`, there is a linear map `f: R^D → R^k` with `k = O(ε^{−2} log n)` such that all pairwise
distances are preserved to within a factor `(1 ± ε)`. *Consequence*: random projection helps
only when `D ≫ ε^{−2} log n`. With the standard constant `k ≥ 8 ln n / ε²`, `n = 100` points
and `ε = 0.2` demand `k ≈ 921` — far above AMF's ambient dimension. JL is vacuous at this
scale, and §5.9 records that fact rather than invoking the theorem decoratively.

### 2.2 Classical (spectral) dimensionality reduction

**Theorem 2.6 (Eckart–Young 1936 [3]; Mirsky 1960 [4]).** Let `A ∈ R^{m×n}` have singular
value decomposition `A = Σ_i σ_i u_i v_i^T` with `σ_1 ≥ σ_2 ≥ …`. Then `A_k = Σ_{i≤k} σ_i u_i
v_i^T` minimises `||A − B||` over all `B` of rank `≤ k`, for the Frobenius norm (Eckart–Young)
and indeed for every unitarily invariant norm (Mirsky), with `||A − A_k||_F² = Σ_{i>k} σ_i²`.
PCA [1; 2] is the special case `A =` centred data matrix.

**Theorem 2.7 (classical MDS; Schoenberg 1935 [5], Young–Householder 1938 [6], algorithm
Torgerson 1952 [7]).** Let `Δ ∈ R^{n×n}` be symmetric with zero diagonal and `Δ^{(2)}` its
entrywise square. Put `J = I − (1/n)11^T` and `B = −½ J Δ^{(2)} J`. Then `Δ` is realisable as
the matrix of Euclidean distances among `n` points iff `B ⪰ 0`, and in that case, writing
`B = Σ_i λ_i q_i q_i^T` with `λ_1 ≥ … ≥ λ_n ≥ 0`, the rows of `[√λ_1 q_1, …, √λ_r q_r]`
(`r = rank B`) realise `Δ` exactly, and the truncation to the top `k` columns is the
`k`-dimensional configuration minimising the *strain* `||B − X X^T||_F`.

*Proof sketch.* If `Δ_{ij} = ||x_i − x_j||` then `Δ²_{ij} = ||x_i||² + ||x_j||² − 2⟨x_i, x_j⟩`;
double-centring annihilates the two rank-one terms and leaves `B = X_c X_c^T ⪰ 0`, the Gram
matrix of the centred configuration. Conversely `B ⪰ 0` factors as `X X^T`. The truncation
claim is Theorem 2.6 applied to `B`. ∎

This theorem matters here more than any other: it says that when the objects being embedded
*already* carry an explicit real-vector description, the "optimal 2-D embedding" is a closed-
form eigenproblem, not a training run. §5.7 applies it to AMF's seven systems.

**Theorem 2.8 (Laplacian eigenmaps; Belkin–Niyogi 2003 [16]).** Let `S ∈ R^{n×n}` be a
symmetric nonnegative similarity matrix, `D = diag(S1)`, `L = D − S` the graph Laplacian and
`L_sym = D^{−1/2} L D^{−1/2}` its normalised form. Then
`y^T L y = ½ Σ_{ij} S_{ij}(y_i − y_j)²`, so minimising `y^T L y` subject to `y^T D y = 1`
and `y ⊥ D1` yields the smoothest non-constant embedding coordinate; by Courant–Fischer the
`k` optimal coordinates are the eigenvectors of the generalised problem `L y = λ D y` with
the `k` smallest non-zero eigenvalues. The multiplicity of the eigenvalue `0` equals the
number of connected components [92, Ch. 1].

**Definition 2.9 (diffusion map; Coifman–Lafon 2006 [17]).** With `P = D^{−1} S` the random-
walk operator and right eigenpairs `(λ_i, ψ_i)`, the *diffusion map at time* `t` is
`Ψ_t(x) = (λ_1^t ψ_1(x), …, λ_k^t ψ_k(x))`, and Euclidean distance in `Ψ_t` equals the
diffusion distance at time `t`. Unlike Isomap [14] and LLE [15], which optimise a geometric
functional, the diffusion map's coordinates carry a dynamical meaning — which is why §5.6
prefers it for AMF, whose graph already generates a dynamic.

### 2.3 Autoencoders and the variational autoencoder

**Theorem 2.10 (linear autoencoders; Baldi–Hornik 1989 [22]).** For an autoencoder
`x ↦ B A x` with `A ∈ R^{k×D}`, `B ∈ R^{D×k}` and squared reconstruction loss, every local
minimum is a global minimum, and at any global minimum `BA` is the orthogonal projector onto
the span of the top `k` eigenvectors of the data covariance. The *subspace* is identified;
the *individual coordinates* are not — `A ↦ RA`, `B ↦ BR^{−1}` for invertible `R` leaves the
loss unchanged. Rotational unidentifiability is therefore present in the simplest possible
representation learner, before any nonlinearity is added.

**Definition 2.11 (VAE; Kingma–Welling 2014 [25], Rezende–Mohamed–Wierstra 2014 [26]).** A
latent-variable model `p_θ(x, z) = p(z) p_θ(x | z)` with an amortised variational family
`q_φ(z | x)`. The evidence lower bound is

```
ELBO(x; θ, φ) = E_{q_φ(z|x)}[ log p_θ(x | z) ]  −  KL( q_φ(z|x) || p(z) ).
```

**Proposition 2.12 (exact evidence gap).** For every `x`,

```
log p_θ(x) = ELBO(x; θ, φ) + KL( q_φ(z|x) || p_θ(z|x) )   ≥ ELBO(x; θ, φ).
```

*Proof.* `log p_θ(x) = E_{q}[log p_θ(x)] = E_q[log (p_θ(x,z)/p_θ(z|x))] = E_q[log
(p_θ(x,z)/q_φ(z|x))] + E_q[log (q_φ(z|x)/p_θ(z|x))]`, the two terms being the ELBO and the
posterior KL. ∎ The gap is *not* observable, so a higher ELBO does not certify a better
model — only a better `(model, posterior-approximation)` pair jointly [29].

**Proposition 2.13 (reparameterisation gradient).** If `q_φ(z|x) = N(μ_φ(x), diag σ_φ(x)²)`
and `z = μ_φ(x) + σ_φ(x) ⊙ ε` with `ε ~ N(0, I)`, then for integrable `f`,
`∇_φ E_{q_φ}[f(z)] = E_ε[ ∇_φ f(μ_φ(x) + σ_φ(x) ⊙ ε) ]`, an unbiased low-variance estimator;
and `KL(N(μ, diag σ²) || N(0, I)) = ½ Σ_j (μ_j² + σ_j² − 1 − log σ_j²)` in closed form. The
estimator is unbiased but *stochastic*: its value depends on the `ε` draw, hence on a seed.

**Theorem 2.14 (impossibility of unsupervised disentanglement; Locatello et al. 2019 [37],
building on Hyvärinen–Pajunen 1999 [36]).** Let `z ~ p(z)` have independent coordinates and
dimension `d ≥ 2`. Then there exist infinitely many bijections `f` of the support with
`p(f(z)) = p(z)` for all `z`, yet `∂f_i/∂z_j ≠ 0` almost everywhere for every pair `(i, j)`.
Consequently, for any generative model there is an entangled reparameterisation inducing the
same observation distribution, so no purely unsupervised objective can prefer the
"disentangled" one. Identification requires an inductive bias on the model *and* on the data
— an auxiliary observed variable [38], or paired observations differing in known factors [39].

**Theorem 2.15 (β-VAE; Higgins et al. 2017 [30] — an objective, not a guarantee).**
Replacing the ELBO's KL term by `β · KL` with `β > 1` trades reconstruction for rate. Alemi
et al. [33] show the ELBO alone does not pin the representation: the achievable
`(rate, distortion)` pairs form a frontier along which the ELBO is constant, so models with
identical ELBO can carry anywhere from zero to maximal information in `z`. Bowman et al. [31]
and Chen et al. [32] identify the degenerate end of that frontier as *posterior collapse*.

### 2.4 Contrastive objectives and their information ceiling

**Definition 2.16 (InfoNCE; van den Oord–Li–Vinyals 2018 [48]; ancestry Gutmann–Hyvärinen
2010 [43]).** Given a critic `f: X × Y → R`, one positive pair `(x, y_1) ~ p(x, y)` and
`K − 1` negatives `y_2, …, y_K ~ p(y)`,

```
I_NCE(f, K) = E[ log ( exp f(x, y_1) / ( (1/K) Σ_{k=1..K} exp f(x, y_k) ) ) ].
```

**Theorem 2.17 (bound and ceiling; Poole et al. 2019 [49]).** `I_NCE(f, K) ≤ I(X; Y)` for
every critic `f`, and `I_NCE(f, K) ≤ log K` for every `f` and every joint distribution. The
bound is tight as `K → ∞` for the optimal critic `f*(x,y) = log p(y|x)/p(y) + c(x)`.

*Why the ceiling is structural.* The argument inside the expectation is a ratio of one term
to the mean of `K` terms, hence at most `K`; its logarithm is at most `log K`. So an InfoNCE
objective evaluated with `K` samples can never *certify* more than `log K` nats, irrespective
of the true dependence.

**Theorem 2.18 (McAllester–Stratos 2020 [50]).** Any distribution-free lower bound on mutual
information that holds with high confidence given `N` samples is `O(log N)`. Together with
Theorem 2.17 this makes "we maximised mutual information" an unfalsifiable claim at small
`N`; Tschannen et al. [51] show empirically that contrastive representation quality is often
*not* explained by the mutual information attained.

**Definition 2.19 (triplet and margin losses; Chopra–Hadsell–LeCun 2005 [44], Hadsell et al.
2006 [45], Schroff et al. 2015 [46]).** For an anchor `a`, positive `p`, negative `n` and
margin `m > 0`, `L = max(0, ||f(a) − f(p)||² − ||f(a) − f(n)||² + m)`. Large-margin nearest
neighbour [47] is the linear-metric ancestor. Note that `L = 0` is achieved by *any* map
satisfying the margin — the loss constrains an ordering, not a geometry.

**Proposition 2.20 (collapse modes).** Contrastive families admit two degeneracies.
*Complete collapse*: `f ≡ const` satisfies every alignment term and is prevented only by the
negatives (or by architectural asymmetry — BYOL [54], SimSiam [55]). *Dimensional collapse*:
the embedding concentrates on a proper subspace of `R^k`, so the effective dimension is
`< k`; Jing et al. [59] attribute it to implicit regularisation along low-curvature
directions, and Wang–Isola [57] characterise the InfoNCE optimum as the balance of an
*alignment* and a *uniformity* term on the hypersphere. Barlow Twins [56] attacks the same
degeneracy through cross-correlation whitening.

### 2.5 Attribution

**Theorem 2.21 (Shapley 1953 [74]).** Let `N` be a finite player set and `v: 2^N → R` with
`v(∅) = 0`. There is exactly one map `φ` satisfying *efficiency* (`Σ_i φ_i = v(N)`),
*symmetry*, the *null-player* axiom and *additivity in* `v`, namely

```
φ_i(v) = Σ_{S ⊆ N \ {i}}  ( |S|! (|N| − |S| − 1)! / |N|! ) · ( v(S ∪ {i}) − v(S) ).
```

Young [75] replaces additivity by strong monotonicity and obtains the same map. SHAP [77],
following Štrumbelj–Kononenko [76], applies `φ` to a value function built from a model's
conditional expectations. The known caveats are that the choice of conditional vs.
interventional value function changes the answer [79; 80], and that Shapley values are
attributions to *model inputs*, not to causes [78; 80].

**Proposition 2.22 (additive games are trivial).** If `v(S) = Σ_{i∈S} c_i` then `φ_i = c_i`.
*Proof.* Each marginal contribution `v(S ∪ {i}) − v(S) = c_i` is independent of `S`, and the
Shapley coefficients sum to one. ∎ §5.6 shows AMF's overall index is exactly such a game.

### 2.6 Neighbour embeddings for visualisation

**Definition 2.23 (t-SNE; van der Maaten–Hinton 2008 [68]).** Define conditionals
`p_{j|i} ∝ exp(−||x_i − x_j||²/2σ_i²)` with `σ_i` chosen so the perplexity
`2^{H(p_{·|i})}` equals a user-set value `Perp`; symmetrise `p_{ij} = (p_{j|i} + p_{i|j})/2n`;
define low-dimensional affinities `q_{ij} ∝ (1 + ||y_i − y_j||²)^{−1}`; minimise
`KL(P || Q)` in `y`. Because `KL(P||Q)` penalises `q_{ij} → 0` where `p_{ij}` is large far
more than the converse, the objective is *local*: it constrains neighbourhoods and leaves
cluster sizes and inter-cluster distances essentially free. UMAP [69] optimises a
cross-entropy on fuzzy simplicial sets and behaves similarly.

**Proposition 2.24 (what a neighbour embedding does not certify).** Wattenberg, Viégas and
Johnson [70] demonstrate that in t-SNE (i) apparent cluster *size* carries no information
about the underlying variance, (ii) *distances between* clusters are not meaningful at
typical settings, and (iii) topologically trivial data can produce apparent clusters at low
perplexity. Kobak–Berens [71] and Kobak–Linderman [72] show initialisation, not the
objective, governs whatever global structure survives; Chari–Pachter [73] quantify the
distortion and argue that low-dimensional neighbour embeddings can be worse than a random
2-D projection on several global-structure measures. Finally, the method is *only defined*
for `Perp < n`: a neighbour embedding of `n = 7` points is not a hard problem, it is a
meaningless one.

---

## 3. Academic curriculum modules

The ladder below is what a graduate student would actually take before doing original work
in this area. "What AMF needs" is deliberately narrow: most of representation learning is
irrelevant to a seven-node, 70-coordinate system, and the table says so.

| # | Module | Level | Canonical course(s) | Core texts (exact units) | What AMF needs from it |
|---|--------|-------|---------------------|--------------------------|------------------------|
| M0 | Linear algebra, SVD, matrix analysis | UG→G | MIT 18.06 *Linear Algebra*; MIT 18.065 *Matrix Methods in Data Analysis, Signal Processing, and Machine Learning*; Stanford EE263 *Introduction to Linear Dynamical Systems* | Horn–Johnson [95] Ch. 1, 4 (Hermitian forms, Courant–Fischer), Ch. 7–8 (singular values, nonnegative matrices, Perron–Frobenius) | The SVD of the 7×7 `CouplingMatrix`; Perron–Frobenius for the stress step map; Courant–Fischer for spectral embeddings |
| M1 | Probability and statistical inference | UG→G | MIT 18.600 *Probability and Random Variables*; CMU 10-701 | Bishop [85] Ch. 1–2; Cover–Thomas [9] Ch. 2 (entropy, KL, mutual information), Ch. 8 | KL divergence as the VAE regulariser; why an unbiased stochastic gradient still needs a seed |
| M2 | Convex optimisation | G | Stanford EE364a; CMU 10-725 | Boyd–Vandenberghe [96] Ch. 2–5 (duality), Ch. 9–11 | The rate–distortion frontier of [33]; the Lagrangian reading of β-VAE |
| M3 | Classical dimensionality reduction | G | Berkeley CS189 (PCA unit); CMU 10-701 (unsupervised unit) | Hastie–Tibshirani–Friedman [88] §§14.5 (principal components, curves, surfaces), 14.8 (multidimensional scaling), 14.9 (nonlinear dimension reduction, local MDS); Jolliffe [89] Ch. 1–3, 6; Borg–Groenen [90] Ch. 7–9, 12 | Theorems 2.6–2.7; the exact 2-D projection of §5.7 and its stress diagnostic |
| M4 | Spectral graph theory and diffusion | G | Stanford CS168 *The Modern Algorithmic Toolbox* (spectral + JL units) | Chung [92] Ch. 1–2; von Luxburg [93] §§2–5 (all three Laplacians and their pitfalls); Belkin–Niyogi [16]; Coifman–Lafon [17] | Laplacian and diffusion embeddings of the seven systems (§5.6); connectedness from the zero eigenvalue's multiplicity |
| M5 | Graphical models and variational inference | G | CMU 10-708 *Probabilistic Graphical Models* | Koller–Friedman [94] Ch. 8, 11; Wainwright–Jordan [28] §§3–5; Bishop [85] Ch. 10 (§10.1 the ELBO, §10.2 mixtures) | Proposition 2.12; why the evidence gap is unobservable; mean-field factorisation as the source of collapse |
| M6 | Deep generative models | G | Stanford CS236 *Deep Generative Models*; Berkeley CS294-158 *Deep Unsupervised Learning* | Goodfellow–Bengio–Courville [86] Ch. 14 (autoencoders), Ch. 15 (representation learning), §20.10.3 (VAE); Murphy [87] Ch. 21 (variational autoencoders), Ch. 23 (normalizing flows); Tomczak [101] Ch. 4 | The full VAE derivation of §5.8; flows [40; 41; 42] as the exact-likelihood alternative |
| M7 | Self-supervised and contrastive learning | G / research | Berkeley CS294-158 (SSL unit); NYU *Deep Learning* (LeCun–Canziani, energy-based / joint-embedding unit) | Balestriero et al. [100] §§2–4; the primary papers [43; 46; 48; 52; 53; 54; 56] | Theorems 2.17–2.18; the `log K` ceiling that decides §5.9 |
| M8 | Statistical learning theory | G | MIT 9.520/6.7910 *Statistical Learning Theory and Applications* | Shalev-Shwartz–Ben-David [97] Ch. 3–6 (PAC, uniform convergence, VC), Ch. 13 (regularisation and stability) | Sample-complexity floors: what a 100-market library can and cannot support |
| M9 | Interpretability and cooperative games | G | (no single canonical course; taught within ML seminars) | Peleg–Sudhölter [99] Ch. 8 (the Shapley value); Molnar [98] Ch. 9 (Shapley, SHAP); primary [74; 75; 79; 80] | Theorem 2.21 and its exact seven-term specialisation, Theorem 5.6 |
| M10 | Regime econometrics | G | (taught inside financial-econometrics sequences) | Hamilton [103] Ch. 22 (time series with changes in regime); Hamilton [102]; Ang–Timmermann [104] | The meaning of "regime" before it is embedded; why a latent state needs a transition law to be a regime at all |
| M11 | Evaluation and the sceptical literature | G / research | (taught inside empirical-finance and reproducibility seminars) | López de Prado [121] Ch. 7, 11–12 (purged CV, backtest overfitting); White [118]; Bailey et al. [119]; Harvey–Liu–Zhu [120] | The discipline that keeps an embedding study from becoming a data-snooping exercise; the reason rule 2 exists |

**Sequencing.** M0–M2 are prerequisites for everything. M3–M4 alone suffice to build every
*compliant* construction in §5. M5–M6 are needed only to understand what the note's VAE would
do; M7 only to understand why its contrastive branch cannot be run at AMF's data scale. M8
and M11 are the gate: they say what evidence would be required before any of this could be
called validated, which under rule 2 it never is.

---

## 4. Exact source material

Every entry is annotated with the specific contribution relied on in this module.

### 4.1 Primary and seminal papers

Each entry names the exact contribution this module relies on. Full citations: References.

**Geometry and classical reduction.** [1] Pearson (1901) and [2] Hotelling (1933) — the two
independent origins of PCA (best-fitting subspace; maximal variance). [3] Eckart–Young (1936)
— optimality of the truncated SVD in Frobenius norm, extended by [4] Mirsky (1960) to every
unitarily invariant norm. [5] Schoenberg (1935) — the negative-type criterion for Euclidean
realisability; [6] Young–Householder (1938) — the double-centring identity; [7] Torgerson
(1952) — the resulting algorithm, classical MDS; [8] Kruskal (1964) — nonmetric MDS and the
*stress* functional, the honest residual that neighbour embeddings lack. [10]
Johnson–Lindenstrauss (1984) — random projection at rate `O(ε^{−2} log n)`. [11] Whitney
(1936) — `2d+1` ambient coordinates always suffice. [12] Takens (1981) and [13]
Sauer–Yorke–Casdagli (1991) — delay embeddings, the theorem that would license "reconstruct
the regime from history" if its hypotheses held. [14] Isomap, [15] LLE, [16] Laplacian
eigenmaps, [17] diffusion maps, [18] kernel PCA — the five constructions that make
"manifold learning" a spectral problem. [19] Fefferman–Mitter–Narayanan (2016) — the manifold
hypothesis as a testable statement with ambient-dimension-free sample complexity. [20]
Levina–Bickel (2004) and [21] Grassberger–Procaccia (1983) — intrinsic-dimension estimators.

**Autoencoders, VAEs, identifiability.** [22] Baldi–Hornik (1989) — linear autoencoders have
no spurious local minima and identify the principal *subspace*, not the axes. [23]
Hinton–Salakhutdinov (2006) — deep autoencoders as nonlinear PCA. [24] Vincent et al. (2008)
— denoising autoencoders, the first widely used pretext task. [25] Kingma–Welling (2014) and
[26] Rezende–Mohamed–Wierstra (2014) — the VAE and the reparameterisation estimator, arrived
at independently. [27] Jordan et al. (1999) and [28] Wainwright–Jordan (2008) — the
variational framework the ELBO sits in; [29] Blei et al. (2017) — the statistician's review.
[30] Higgins et al. (2017) — β-VAE. [31] Bowman et al. (2016) — the first clear report of
posterior collapse; [32] Chen et al. (2017) — collapse explained as the optimal use of a
powerful decoder; [33] Alemi et al. (2018) — the rate–distortion frontier along which the
ELBO is constant; [34] Dai–Wipf (2019) — VAE optima and recovery of the intrinsic dimension.
[35] Loaiza-Ganem–Cunningham (2019) — the continuous Bernoulli, i.e. the correct likelihood
for data in `[0,1]` and the bias of the usual misspecification. [36] Hyvärinen–Pajunen (1999)
— nonlinear ICA is unidentifiable; [37] Locatello et al. (2019) — Theorem 2.14 plus a
12 000-model study; [38] Khemakhem et al. (2020) and [39] Locatello et al. (2020) —
identifiability recovered from an auxiliary variable and from weak supervision respectively.
[40] Rezende–Mohamed (2015), [41] Dinh et al. (2017), [42] Papamakarios et al. (2021) —
normalising flows: exact likelihoods, no evidence gap.

**Contrastive and self-supervised learning.** [43] Gutmann–Hyvärinen (2010) — noise-
contrastive estimation, the ancestor. [44] Chopra et al. (2005) and [45] Hadsell et al. (2006)
— the contrastive/siamese loss; [46] Schroff et al. (2015) — the triplet loss with hard-
negative mining; [47] Weinberger–Saul (2009) — the linear-metric ancestor. [48] van den Oord
et al. (2018) — CPC and InfoNCE; [49] Poole et al. (2019) — the family of variational MI
bounds and the `log K` ceiling; [50] McAllester–Stratos (2020) — the formal limitation on any
distribution-free MI lower bound; [51] Tschannen et al. (2020) — MI attained does not explain
representation quality. [52] SimCLR (augmentation composition, projection head), [53] MoCo
(a momentum queue decouples negatives from batch size), [54] BYOL (no negatives), [55]
SimSiam (the stop-gradient is what prevents collapse), [56] Barlow Twins (redundancy
reduction). [57] Wang–Isola (2020) — alignment and uniformity; [58] Arora et al. (2019) — the
first generalisation theory; [59] Jing et al. (2022) — dimensional collapse. [60] BERT and
[61] MAE — masked modelling, the note's "masked market modeling" analogue.

**Word embeddings (the note's stated analogy).** [62] and [63] Mikolov et al. (2013) —
skip-gram/CBOW, then negative sampling; [64] Mikolov–Yih–Zweig (2013) — the linear-analogy
regularities; [65] GloVe — a log-bilinear factorisation of co-occurrence counts; [66]
Levy–Goldberg (2014) — skip-gram with negative sampling *is* implicit factorisation of a
shifted PMI matrix, i.e. the celebrated method is a matrix factorisation. [67]
Bengio–Courville–Vincent (2013) — the review that named the field's desiderata.

**Attribution.** [74] Shapley (1953) — Theorem 2.21; [75] Young (1985) — the monotonicity
characterisation; [76] Štrumbelj–Kononenko (2014) and [77] Lundberg–Lee (2017) — Shapley
attribution for predictive models; [78], [79], [80] — the three principal critiques: axiom
mismatch, value-function ambiguity, and the association/causation gap.

**Analogue forecasting.** [81] Lorenz (1969) — five years of hemispheric data contained no
analogue pair close enough to be useful, and the pairs found diverged; [82] van den Dool
(1994) — how long a record a useful hemispheric analogue would require; [83]
Farmer–Sidorowich (1987) and [84] Sugihara–May (1990) — nearest-neighbour prediction in
deterministic nonlinear systems.


### 4.2 Canonical textbooks (with the chapters that matter)

Full citations are in the References; only the load-bearing units are listed here.

- [85] Bishop, *PRML* — §10.1 the variational lower bound; §10.2 variational mixtures; Ch. 12
  continuous latent variables (§12.1 PCA, §12.2 probabilistic PCA, the exact-solution baseline
  for any AMF encoder).
- [86] Goodfellow–Bengio–Courville — Ch. 14 autoencoders (§14.5 denoising, §14.6 the manifold
  view); Ch. 15 representation learning; §20.10.3 the VAE.
- [87] Murphy, *Advanced Topics* — Ch. 21 variational autoencoders; Ch. 23 normalizing flows;
  the representation-learning chapter for identifiability.
- [88] Hastie–Tibshirani–Friedman, *ESL* — §14.5 principal components, curves and surfaces;
  §14.7 ICA and projection pursuit; §14.8 multidimensional scaling; §14.9 nonlinear dimension
  reduction and local MDS.
- [89] Jolliffe — Ch. 1–3 (definitions and properties); Ch. 6 (how many components to keep —
  the question the note's "128D" answers by assertion).
- [90] Borg–Groenen — Ch. 7 (stress and its interpretation); Ch. 8–9 (SMACOF); Ch. 12
  (classical scaling).
- [91] Lee–Verleysen — Ch. 2 (intrinsic dimension); Ch. 4 (distance preservation); Ch. 5
  (topology preservation).
- [92] Chung — Ch. 1–2: the normalised Laplacian, its spectrum, and the component-count
  theorem used in §5.6.
- [94] Koller–Friedman — Ch. 8 (exponential families); Ch. 11 (inference as optimisation).
- [95] Horn–Johnson — Ch. 4 (Hermitian matrices, Courant–Fischer); Ch. 7 (PSD matrices,
  singular values); Ch. 8 (nonnegative matrices, Perron–Frobenius).
- [96] Boyd–Vandenberghe — Ch. 5 (duality), for the Lagrangian reading of rate–distortion.
- [97] Shalev-Shwartz–Ben-David — Ch. 3–6 (PAC, uniform convergence, VC); Ch. 13
  (regularisation and stability).
- [98] Molnar — Ch. 9: Shapley values and SHAP, including the known failure modes.
- [99] Peleg–Sudhölter — Ch. 8: the Shapley value and its axiomatisations.
- [101] Tomczak — Ch. 4: VAEs and their practical failure modes.
- [103] Hamilton, *Time Series Analysis* — Ch. 22: modelling time series with changes in
  regime, i.e. the formal definition of the word the note uses informally throughout.
- [121] López de Prado — Ch. 7 (cross-validation under dependence); Ch. 11–12 (backtest
  overfitting, the deflated Sharpe ratio); read as the discipline rule 2 encodes.


### 4.3 Surveys and reviews

[67] Bengio–Courville–Vincent (2013), *IEEE TPAMI* — the canonical survey; §3 on the
manifold view and §4 on disentangling remain the reference statement of the goal.
[29] Blei–Kucukelbir–McAuliffe (2017), *JASA* — variational inference for statisticians.
[28] Wainwright–Jordan (2008) — the exponential-family variational framework in full.
[42] Papamakarios et al. (2021), *JMLR* — normalising flows, with a clean taxonomy.
[93] von Luxburg (2007), *Statistics and Computing* — spectral clustering, and specifically
§8 on which Laplacian to use and why the choice matters.
[100] Balestriero et al. (2023) — a practitioner's survey of self-supervised methods,
including the collapse taxonomy of Proposition 2.20.
[104] Ang–Timmermann (2012), *Annual Review of Financial Economics* — regime switching in
financial markets, and an honest account of what it does and does not deliver.

### 4.4 Open courseware and lecture notes

- **Stanford CS236, *Deep Generative Models*** — lectures on latent-variable models and the
  ELBO, on normalising flows, and on evaluation of generative models. Public lecture notes.
- **Berkeley CS294-158, *Deep Unsupervised Learning*** — lectures on autoregressive models,
  flows, latent-variable models and self-supervised learning; slides and recordings public.
- **CMU 10-708, *Probabilistic Graphical Models*** — the mean-field and variational-inference
  lectures are the cleanest derivation route to Proposition 2.12.
- **MIT 9.520/6.7910, *Statistical Learning Theory and Applications*** — the
  regularisation-and-stability lectures give the generalisation frame for M8.
- **MIT 18.065, *Matrix Methods in Data Analysis, Signal Processing, and Machine Learning***
  (OCW) — the SVD, low-rank approximation and randomised linear algebra lectures.
- **Stanford CS168, *The Modern Algorithmic Toolbox*** — the lecture notes on PCA, the SVD,
  spectral graph methods and Johnson–Lindenstrauss are unusually direct and self-contained.
- **Distill, [70] "How to Use t-SNE Effectively"** — an interactive article, and the single
  most useful teaching artefact for Proposition 2.24; assign it before anyone plots anything.

### 4.5 Domain application to markets — including the sceptical literature

*Where low-dimensional structure in market data is real and documented.*
[105] Bai–Ng (2002) — consistent criteria for the number of factors in approximate factor
models; the disciplined answer to "how many latent dimensions?". [106] Stock–Watson (2002) —
diffusion-index forecasting from principal components of many predictors. [109]
Marčenko–Pastur (1967) — the limiting spectral distribution that says which eigenvalues of a
sample correlation matrix are noise; [107] Laloux et al. (1999) and [108] Plerou et al. (2002)
apply it and find that the overwhelming majority of eigenvalues of a financial correlation
matrix are indistinguishable from noise. [110] Mantegna (1999) — hierarchical structure from
a correlation-derived metric, the ancestor of "assets cluster into groups".
[111] Kritzman et al. (2011) — the absorption ratio, a principal-component statistic proposed
as a systemic-risk measure. [102] Hamilton (1989) — the Markov-switching model that gives
"regime" a testable definition; [104] Ang–Timmermann (2012) survey what followed.
[112] Billio et al. (2012) and [113] Diebold–Yılmaz (2014) — connectedness measures built on
Granger-causal and variance-decomposition networks: the closest published analogue to AMF's
dependency graph. [114] Acemoglu et al. (2012) — how network structure converts idiosyncratic
shocks into aggregate fluctuations. [115] Battiston et al. (2012) — DebtRank, a centrality
measure explicitly designed for systemic importance.

*The sceptical literature, which must be read alongside the above.*
[117] Cont (2001) — the stylised facts (heavy tails, volatility clustering, non-stationarity)
that break the i.i.d. assumption every embedding method above silently makes.
[118] White (2000) — the reality check for data snooping. [119] Bailey, Borwein, López de
Prado and Zhu (2014) — with enough trials, an impressive-looking result is guaranteed; the
paper gives the minimum backtest length implied by a number of trials.
[120] Harvey, Liu and Zhu (2016) — most published cross-sectional findings do not survive an
appropriate multiple-testing correction. [116] Gu, Kelly and Xiu (2020) — a careful,
positive machine-learning study whose value lies in its evaluation protocol as much as its
results. [73] Chari–Pachter (2023) — from genomics, not finance, but the most direct
statement anywhere of the claim that 2-D embeddings can misrepresent global structure so
badly that a random projection scores better.

*The honest reading.* [105]–[111] establish that market covariance matrices have a small
number of statistically identifiable directions above the noise floor. They do **not**
establish that a 128-dimensional learned latent of a market's *structural* description means
anything, and nothing in this literature applies to AMF's inputs, which are analyst-declared
structural metrics rather than observed data.

---
## 5. Derivation for the AMF setting

Every number quoted in this section was computed from `examples/sample_market.json` using the
committed `amf` package plus a 60-line pure-Python Jacobi eigensolver; no third-party
library was involved. That is itself part of the argument: every construction proposed as
*compliant* below is closed-form and reproducible with the standard library alone.

### 5.1 The ambient space is not high-dimensional

**Definition 5.1 (market descriptor).** Fix the declaration order
`K = (skeleton, circulatory, nervous, musculature, organs, immune, metabolism)`. For a
complete `Market` `M` define

```
  m(M) = ( integrity_k, redundancy_k, criticality_k, load_k )_{k ∈ K}          ∈ [0,1]^28
  e(M) = ( w(s, t) )_{(s,t) : s ≠ t}         pair-aggregated edge weights      ∈ [0,1]^42
  ê(M) = ( w(s, t, κ) )_{(s,t) : s ≠ t, κ ∈ DependencyKind}                    ∈ [0,1]^168
  φ(M) = ( m(M), e(M) ) ∈ [0,1]^70,     φ̂(M) = ( m(M), ê(M) ) ∈ [0,1]^196.
```

`φ̂` is the JSON schema's full content; `φ` is what every structural query actually reads,
because `DependencyGraph` aggregates across `DependencyKind` and caps at `1.0`.

**Remark 5.2 (the note's premise inverts).** The source note opens with
"High-dimensional data (1000+ features) → Low-dimensional embeddings (e.g., 128D)". For AMF,
`dim φ = 70 < 128`. A 128-dimensional latent is therefore not a compression but an
*expansion* by a factor of `128/70 ≈ 1.83`; even against the kind-resolved `φ̂` it recovers
only a factor of `196/128 ≈ 1.53`, and `φ̂ → φ` already achieves `2.8×` losslessly for every
structural query. Whatever else is true, "128D" is not a dimensionality *reduction* of an AMF
market, and no claim in the note survives that observation unmodified.

### 5.2 AMF already contains an exact, identifiable encoder

**Proposition 5.3 (the diagnostic factorisation ladder).** Let
`w = (w_f, w_c, w_b)` be the `DiagnosticConfig` weights, `W = w_f + w_c + w_b > 0`, and for
each `k ∈ K` let `f_k` be fragility, `c_k` concentration and `b_k` feedback amplification.
Then the per-system score and the overall index satisfy

```
  s_k     = ( w_f f_k + w_c c_k + w_b b_k ) / W                    (linear in (f, c, b))
  index   = ( Σ_k crit_k · s_k ) / ( Σ_k crit_k )                  (a weighted mean)
```

and consequently the maps

```
  φ̂ ∈ R^196  ──aggregate──▶  φ ∈ R^70  ──D──▶  (crit_k, f_k, c_k, b_k)_k ∈ R^28
              ──blend──▶  (crit_k, s_k)_k ∈ R^14  ──mean──▶  index ∈ R
```

commute with `DiagnosticEngine.diagnose`: the overall index and the per-system scores are
functions of the 28-dimensional statistic `D(φ)` alone.

*Proof.* Aggregation across kinds is by construction (`DependencyGraph._pair_weights`).
`f_k = crit_k (1 − h_k)(1 − red_k)` with `h_k = int_k (1 − load_k)` reads only system `k`'s
four metrics; `c_k` is a Herfindahl index over `k`'s outgoing pair weights; `b_k` sums
edge-weight products over the simple cycles containing `k` — all three are functions of `φ`.
The blend is linear by definition and the index is a `crit`-weighted mean of the `s_k`. ∎

**Remark 5.4 (what the ladder does *not* carry).** The single-points-of-failure list and each
finding's `drivers` strings are **not** functions of `D(φ)`: articulation points depend on
the graph's global connectivity and the SPOF test additionally reads `redundancy_k` directly.
Any latent model trained to reproduce "the diagnosis" must therefore be told which
diagnosis — the scalar index (rank 1), the score vector (rank 7), or the full
`DiagnosticReport` (which is not a vector at all). The note never says.

**Corollary 5.5 (the honest dimension budget).** A latent representation intended to preserve
AMF's *diagnostic* content needs at most 28 coordinates and at least 7; a representation
intended to preserve the *ranking* of findings needs at most 7; one intended to preserve the
index alone needs 1. Anything above 28 is provably redundant for that purpose. The note's
`128` exceeds the maximum by `4.6×`.

### 5.3 The exact per-system attribution: Shapley without SHAP

The note asks for "SHAP values: which features contributed most to each embedding". Inside
the boundary this has a closed form requiring no sampling, no model and no dependency.

**Theorem 5.6 (exact Shapley decomposition of the overall index).** Let the player set be the
seven systems `K`. For a coalition `S ⊆ K`, define the value function by evaluating the index
on the market in which every system outside `S` is replaced by its *reference* state
(`integrity = 1`, `load = 0`, `redundancy = 1`, and all of its outgoing couplings removed),
so that `s_k = 0` for `k ∉ S` while `crit_k` is held fixed:

```
  v(S) = ( Σ_{k ∈ S} crit_k · s_k ) / ( Σ_{j ∈ K} crit_j ),        v(∅) = 0,  v(K) = index.
```

Then the unique attribution satisfying efficiency, symmetry, the null-player axiom and
additivity (Theorem 2.21) is

```
  φ_k  =  crit_k · s_k / Σ_{j ∈ K} crit_j ,          with  Σ_k φ_k = index  exactly.
```

*Proof.* `v` is an additive game: `v(S) = Σ_{k∈S} c_k` with `c_k = crit_k s_k / Σ_j crit_j`.
Apply Proposition 2.22. ∎

**Numerical check (sample market, default config).** `Σ_j crit_j = 5.05`; the per-system
scores are `musculature 0.3767`, `circulatory 0.3271`, `organs 0.3247`, `immune 0.3228`,
`metabolism 0.3228`, `nervous 0.2534`, `skeleton 0.0932`. The Shapley shares are

```
  circulatory  0.05505      immune      0.04794      musculature 0.04475
  organs       0.04179      metabolism  0.03835      nervous     0.03513
  skeleton     0.01662
  ------------------------------------------------------------------
  Σ φ_k = 0.2796385563   =   overall index 0.2796385563   (to 10 d.p.)
```

Three consequences worth stating plainly. (i) The attribution is exact, not estimated: no
Monte-Carlo coalition sampling, no `2^7 = 128` enumeration, seven multiplications.
(ii) It is *not* the same as the ranking of scores — `immune` outranks `musculature` in
attributed share while ranking below it in score, because `crit(immune) = 0.75` exceeds
`crit(musculature) = 0.60`. This is exactly the information a practitioner wants and the raw
finding list does not show. (iii) The exactness is a consequence of additivity, which holds
because `DiagnosticEngine` uses a *weighted mean*. Any future change that makes the index
non-additive in the per-system scores — a max, a soft-max, a product — destroys Theorem 5.6
and forces either `128`-coalition enumeration or sampling. That is a design constraint worth
recording in `CLAUDE.md`.

**Remark 5.7 (what this does not do).** Theorem 5.6 attributes the index to *systems*, i.e.
to declared inputs. It says nothing causal about any real market: the value function is a
counterfactual *inside the model*, and the critique of [78; 79; 80] applies in full — a
different reference state gives a different `v` and hence different shares. The reference
state above must be documented, not assumed.

### 5.4 Structural distance and the geometry of a market library

**Definition 5.8 (three candidate structural pseudometrics).** For markets `M, M'`:

```
  d_φ(M, M')     = || φ(M) − φ(M') ||₂                       (descriptor distance, 70-D)
  d_score(M, M') = || s(M) − s(M') ||₂                       (diagnostic profile, 7-D)
  d_index(M, M') = | index(M) − index(M') |                  (scalar, 1-D)
```

`d_φ` is a metric on descriptors; `d_score` and `d_index` are pseudometrics (distinct markets
can share a profile). By Proposition 5.3 they are ordered by information content:
`d_index` factors through `d_score`, which factors through `d_φ`.

**Proposition 5.9 (an isometric embedding exists, and its dimension is 7).** `s: M ↦ s(M) ∈
R^7` is by definition an isometry from `(Markets, d_score)` into `R^7`; and by Theorem 2.7
any finite library `{M_1, …, M_n}` under `d_score` embeds *exactly* into `R^{r}` with
`r = rank(−½ J Δ^{(2)} J) ≤ min(n − 1, 7)`. No optimisation is required and no distortion is
incurred. A learned 128-dimensional embedding under `d_score` supervision would therefore
have `121` provably unconstrained directions — precisely the setting in which dimensional
collapse (Proposition 2.20) is the expected, not the pathological, outcome.

### 5.5 Exact spectral embedding of the seven systems from the coupling matrix

The note's "asset embeddings … capturing its role in system" has a well-posed structural
analogue: embed the seven `SystemKind`s using the stress-transmission matrix.

Let `W ∈ R^{7×7}` be `DependencyGraph.coupling_matrix()`, with `W[i][j]` the weight with
which stress flows from transmitter `i` to receiver `j` (the reverse of the dependency edge).
On the sample market, in declaration order,

```
                skel  circ  nerv  musc  orga  immu  meta
  skeleton    [ 0.0   0.8   0.5   0.0   0.0   0.3   0.0 ]
  circulatory [ 0.0   0.0   0.0   0.7   0.6   0.0   0.0 ]
  nervous     [ 0.0   0.5   0.0   0.0   0.0   0.0   0.0 ]
  musculature [ 0.0   0.0   0.6   0.0   0.0   0.0   0.0 ]
  organs      [ 0.0   0.0   0.0   0.0   0.0   0.0   0.4 ]
  immune      [ 0.0   0.0   0.0   0.0   0.0   0.0   0.0 ]
  metabolism  [ 0.0   0.0   0.0   0.0   0.0   0.0   0.0 ]
```

**Construction 5.10 (transmitter/receiver coordinates).** Take the SVD `W = Σ_i σ_i u_i v_i^T`
and set, for a chosen rank `r`,

```
  transmitter_coords(k) = ( √σ_1 u_1[k], …, √σ_r u_r[k] )
  receiver_coords(k)    = ( √σ_1 v_1[k], …, √σ_r v_r[k] )
```

so that `⟨transmitter_coords(i), receiver_coords(j)⟩` is the best rank-`r` approximation of
`W[i][j]` in Frobenius norm (Theorem 2.6). On the sample market the singular values are

```
  σ = (1.1149, 0.9220, 0.5719, 0.4000, 0.1412, 0, 0),   rank W = 5
  Σ_{i≤2} σ_i² / Σ σ_i² = 0.805        Σ_{i≤3} σ_i² / Σ σ_i² = 0.931
```

so a rank-2 embedding reproduces `80.5%` of the coupling energy and rank 3 reproduces
`93.1%`. This is the *entire* content of the note's "128D vector capturing its role in
system", computed exactly, in a space of dimension at most 5, with a stated approximation
error. Note also that `rank W ≤ 5 < 7` for this market: two of the seven systems (`immune`,
`metabolism`) transmit to nobody, so their transmitter coordinates are the zero vector — a
fact the embedding reports rather than hides.

**Construction 5.11 (diffusion embedding).** Symmetrise `S = (W + Wᵀ)/2`, form the normalised
Laplacian `L_sym = I − D^{−1/2} S D^{−1/2}` and take the eigenvectors of its smallest non-zero
eigenvalues (Theorem 2.8, Definition 2.9). On the sample market:

```
  spec(L_sym) = (0, 0.3725, 0.6810, 1.1866, 1.2993, 1.6192, 1.8413)
```

The eigenvalue `0` has multiplicity one, so the symmetrised coupling graph is connected — a
structural fact the module reports for free. The first two non-trivial coordinates are

```
  skeleton    (−0.2722, −0.4844)      musculature (−0.1861,  0.4876)
  circulatory (−0.0167,  0.1262)      organs      ( 0.6241, −0.0502)
  nervous     (−0.2654,  0.2583)      immune      (−0.1878, −0.6576)
  metabolism  ( 0.6291, −0.0996)
```

The first non-trivial coordinate isolates `organs` and `metabolism` — the tail of the pendant
chain `circulatory → organs → metabolism` — from the rest, leaving `circulatory` itself near
the boundary at `−0.0167`. The second separates the feedback triangle
`circulatory → musculature → nervous → circulatory` (all positive) from the peripheral
`skeleton`/`immune` pair (both strongly negative). That is a legible, reproducible "visual map
of market structure" in the note's sense — and it is a two-line eigenproblem.

### 5.6 The dynamical embedding: the stress step map is already a linear operator

**Proposition 5.12.** With `a_j = absorptive_capacity(j)`, damping `δ`, retention `ρ` and
transmission `τ`, the linear part of `ShockSimulator`'s update is `x_{t+1} = A x_t` (before
clipping) with

```
  A = δ ( ρ I + τ · diag(1 − a) · Wᵀ ),      i.e.   A[j][i] = δ ρ 1{i=j} + δ τ (1 − a_j) W[i][j].
```

Hence the eigenpairs of `A` *are* the natural regime coordinates of AMF's dynamics: the
dominant right eigenvector is the asymptotic shape of the stress vector, and `ρ(A)` decides
whether the linearised dynamic contracts.

**Numerical instance (sample market, default `SimulationConfig`: `δ = 0.85`, `ρ = 0.5`,
`τ = 1.0`).** Power iteration gives

```
  ρ(A) = 0.582613 < 1                        (so the linearised step map contracts here)
  column gains Σ_j A[j][i] = (0.9418, 0.6970, 0.6205, 0.5933, 0.5270, 0.4250, 0.4250)
  dominant right eigenvector (normalised):
     skeleton 0.0000   circulatory 0.5302   nervous 0.4275   musculature 0.4003
     organs   0.5147   immune      0.0000   metabolism 0.3331
```

Two readings. First, the two zero entries are structural, not numerical: no dependency points
*into* `skeleton`, and `immune` is reachable only from `skeleton`, so neither can carry
persistent stress in the asymptotic shape. Second, `ρ(A) < 1` on this market is consistent
with `CLAUDE.md`'s warning that the step map is *not* a contraction for every market: the
Perron bound `ρ(A) ≤ max_i Σ_j A[j][i] = 0.9418` here leaves headroom, but a market with
larger incoming weights and smaller absorptive capacity pushes the same bound above one.
A one-number "regime coordinate" with a genuine dynamical meaning is therefore available
today: `ρ(A)`, computable by power iteration in the standard library.

### 5.7 The 2-D projection, done exactly

**Construction 5.13 (exact classical MDS of the seven systems).** Represent system `k` by its
diagnostic triple `t_k = (f_k, c_k, b_k) ∈ R^3`, centre, form the `7 × 7` Gram matrix
`G = T_c T_cᵀ`, and take the top-2 eigenpairs (Theorem 2.7). On the sample market:

```
  spec(G) = (0.95307, 0.07523, 0.01618, 0, 0, 0, 0)              (rank 3, as it must be)
  variance captured by the first two coordinates:  0.9845
  coordinates:
     skeleton    (−0.7246, −0.1150)      musculature ( 0.2878,  0.1264)
     circulatory (−0.2215,  0.1227)      organs      ( 0.2891, −0.0802)
     nervous     (−0.2107,  0.1073)      immune      ( 0.2900, −0.0806)
     metabolism  ( 0.2900, −0.0806)
```

`98.45%` of the diagnostic variance lies in two coordinates, and — unlike a neighbour
embedding — the residual `1.55%` is *reported*, the map is linear, distances are meaningful,
and repeated runs are bit-identical. Three honest caveats belong with the plot. (i) `immune`
and `metabolism` coincide *exactly*, because their diagnostic triples are identical
(`f = 0.0570`, `c = 1.0000`, `b = 0.0000`); `organs` is nearly coincident, differing only in
fragility (`0.0617`). Their attributed shares nevertheless differ, through `criticality`,
which this projection deliberately does not encode. A neighbour embedding would have
separated the identical pair by an arbitrary amount at any perplexity. (ii) The dominant axis
is essentially the concentration coordinate: concentration ranges over `[0, 1]` on this
market while fragility ranges over `[0.034, 0.265]` and feedback over `[0, 0.21]`, so the
unstandardised Gram matrix is dominated by the widest-ranging component. Standardising the
triple changes the picture — which is a property of the data, not a defect of the method, and
must be stated whenever the plot is shown. (iii) `rank G = 3` exactly, so any embedding
dimension above three is void here.

**Proposition 5.14 (neighbour embeddings are inapplicable at `n = 7`).** t-SNE requires a
perplexity `Perp` with `Perp < n`; its default `Perp = 30` is undefined for `n = 7`, and at
`Perp ≲ 6` Proposition 2.24(iii) applies with full force — apparent clusters among seven
points carry no evidence. UMAP's `n_neighbors` faces the same constraint. For a library of
`n` markets the constraint softens but the guarantees do not appear: [70; 71; 72; 73]
between them establish that cluster size, inter-cluster distance and global topology are not
recoverable from the plot. **Recommendation**: AMF should render exact linear projections
with a reported residual, never a neighbour embedding.

### 5.8 What a VAE would actually optimise here

Take `x = φ(M) ∈ [0,1]^70`, prior `p(z) = N(0, I_d)`, encoder
`q_φ(z|x) = N(μ(x), diag σ(x)²)`, decoder `p_θ(x|z)`. Then (Definition 2.11, Proposition
2.12) the training objective is

```
  ELBO(x) = E_{ε ~ N(0,I)}[ log p_θ( x | μ(x) + σ(x) ⊙ ε ) ]
            − ½ Σ_{j=1..d} ( μ_j(x)² + σ_j(x)² − 1 − log σ_j(x)² )
```

with `log p_θ(x) = ELBO(x) + KL(q_φ(z|x) || p_θ(z|x))`, the second term unobservable.

**Issue 1 — likelihood misspecification.** `x` lives in `[0,1]^70` and its coordinates
saturate: on the sample market, six of the seven `load` values are exactly `0.1`, four
`integrity` values are exactly `0.9`, and 34 of the 42 pair weights are exactly `0`. A
Gaussian decoder places mass outside `[0,1]` and, worse, a Bernoulli decoder applied to
continuous `[0,1]` data — still common practice — is not a normalised density at all;
Loaiza-Ganem and Cunningham [35] quantify the resulting bias and give the continuous-Bernoulli
correction. A Beta or continuous-Bernoulli likelihood is mandatory, and the near-atomic mass
at `0` in `e(M)` argues for a zero-inflated mixture rather than any of them.

**Proposition 5.15 (mandatory collapse at `d = 128`).** Suppose `q_φ(z|x) = Π_j q_φ(z_j|x)`
and `p(z) = Π_j p(z_j)`, so that `ELBO(x) = E_q[log p_θ(x|z)] − Σ_j KL(q_φ(z_j|x) ‖ p(z_j))`.
If the decoder is invariant to coordinate `j` — `p_θ(x|z)` does not depend on `z_j` — then the
distortion term is independent of `q_φ(z_j|x)` while the rate term is maximised (at `0`)
precisely when `q_φ(z_j|x) = p(z_j)`. Hence at every ELBO optimum, `z_j` carries zero
information about `x`. ∎

*Consequence.* Since `dim φ = 70`, a `d = 128` latent has at least `58` coordinates that a
sufficient decoder need not use, and Proposition 5.15 says the objective *rewards* switching
them off. What is usually reported as a pathology [31; 32] is, at `d > dim x`, the correct
behaviour of the objective. Dai and Wipf [34] make the stronger point that a suitably
flexible VAE optimum recovers the intrinsic dimension and collapses the surplus; the note's
`128` therefore either collapses (and was never 128-dimensional) or fails to converge.

**Issue 2 — the ELBO does not determine the representation.** Alemi et al. [33] show the
achievable `(rate R, distortion D)` pairs trace a frontier along which `R + D` — and hence
the ELBO — is constant. Two AMF encoders with identical ELBO can therefore place *all* or
*none* of the market's structure in `z`. Model selection by ELBO is, for representation
purposes, no selection at all.

**Issue 3 — identifiability.** The note wants axes with meaning: "2D plot shows bull/bear
axis". Theorem 2.14 states that no unsupervised objective can prefer an axis-aligned
factorisation over any of infinitely many entangled reparameterisations with identical
likelihood. AMF's saving grace is that it *has* labels: the 28 metric coordinates are named,
declared, and semantically fixed by construction. This puts AMF in the weakly-supervised
regime of [38; 39], where identifiability is recoverable — but it also removes the motive,
because the named axes are already the representation (Proposition 5.3).

**Issue 4 — sample complexity.** A `70 → 128 → 70` encoder–decoder with two hidden layers of
width 256 carries of order `10^5` parameters. AMF's realistic corpus is a curated library of
assembled `Market` objects; the repository ships one. Under any uniform-convergence bound
[97, Ch. 4–6] this is not an estimation problem, it is interpolation.

**What survives.** One thing does. `SimulationConfig` already supports seeded stochastic
`ensemble(...)` runs; a *generative* latent model over markets — sample `z ~ p(z)`, decode to
`φ`, assemble, diagnose — would give AMF a principled scenario generator with an explicit
sampling density, provided the density is one AMF *declares* rather than one it *learns*.
That is a normalising-flow or copula construction over `[0,1]^70` [40; 41; 42], parameterised
by the analyst, seeded, and deterministic given the seed. It requires no training data and
breaks no rule.

### 5.9 Contrastive learning and analogue search at AMF's data scale

**Proposition 5.16 (the InfoNCE ceiling for a market library).** Let a library contain `N`
markets. Any InfoNCE objective (Definition 2.16) evaluated with `K ≤ N` samples satisfies
`I_NCE ≤ log K ≤ log N` nats (Theorem 2.17), and by Theorem 2.18 no distribution-free
high-confidence lower bound from `N` samples can exceed `O(log N)` either. For `N = 100`,
`log N = 4.61` nats `= 6.64` bits.

*Scale of the gap.* Discretise `φ(M) ∈ [0,1]^70` at a resolution of `0.05`; the descriptor
then ranges over `20^70` configurations, i.e. `70 log₂ 20 = 302.5` bits. A contrastive
objective run over a hundred-market library can therefore certify at most `6.64` of those
`302.5` bits — about `2.2%` — and that is an upper bound achieved only by the optimal critic.
The note's contrastive branch is not merely unvalidated; it is information-theoretically
incapable of doing what it is asked to do at any library size AMF could plausibly curate.

**Proposition 5.17 (the analogue-search budget).** To guarantee that every point of `[0,1]^d`
has a library member within `ℓ∞` distance `ε`, a volume argument gives `N ≥ (2ε)^{−d}`. At
`ε = 0.1`:

| Descriptor used for the analogue search | `d` | Minimum library size `N` |
|---|---|---|
| overall index alone | 1 | 5 |
| per-system diagnostic triple of one system | 3 | 125 |
| per-system score vector `s(M)` | 7 | `7.8 × 10^4` |
| `(crit_k, s_k)` pairs | 14 | `6.1 × 10^9` |
| `(f_k, c_k, b_k)` triples | 21 | `4.8 × 10^14` |
| the diagnostic statistic `D(φ)` | 28 | `3.7 × 10^19` |
| the full descriptor `φ` | 70 | `8.5 × 10^48` |

This is the exact structure of Lorenz's 1969 finding [81]: searching five years of hemispheric
observations, he found no analogue pair close enough to be useful, and van den Dool [82]
later quantified how long a record would be needed. The note's central promise —
"`bull_2000 ≈ bull_2016`", "Nearest neighbours: find similar past regimes" — is the analogue
method, and the analogue method has a known, brutal, dimension-exponential data requirement.
**The compliant conclusion is not that analogue search is useless but that it must be run in
the smallest sufficient descriptor** — `d_index` or `d_score`, `d ≤ 7` — where the budget is
`10^4`–`10^5` rather than `10^48`, and where the embedding is exact by Proposition 5.9.

### 5.10 A compliant construction: `amf.latent`

Collecting the above, the following module sits inside every hard rule: standard library
only, closed-form, deterministic, structural vocabulary, `InvalidConfigError` on out-of-range
knobs, and fully coverable because it contains no training loop.

```
src/amf/latent.py                     # sits between diagnostics/simulation and report/viz

  LatentConfig(rank: int = 2, tolerance: float = 1e-12, iterations: int = 200)
      # validated: 1 <= rank <= 7, tolerance finite and > 0, iterations >= 1
      # -> InvalidConfigError otherwise

  @dataclass(frozen=True, slots=True)
  class SystemCoordinates:            # NOTE: no field named `order` -- see §6
      axis: tuple[SystemKind, ...]
      transmitter: dict[SystemKind, tuple[float, ...]]
      receiver: dict[SystemKind, tuple[float, ...]]
      singular_values: tuple[float, ...]
      captured_fraction: float        # Σ_{i<=r} σ_i² / Σ σ_i²   (Theorem 2.6)
      def to_dict(self) -> dict[str, Any]: ...

  @dataclass(frozen=True, slots=True)
  class DiffusionCoordinates:
      axis: tuple[SystemKind, ...]
      coordinates: dict[SystemKind, tuple[float, ...]]
      spectrum: tuple[float, ...]
      components: int                 # multiplicity of eigenvalue 0  (Chung [92] Ch. 1)

  @dataclass(frozen=True, slots=True)
  class StructuralProjection:         # exact classical MDS of a market library
      residual_fraction: float        # the reported, non-negotiable honesty term
      coordinates: tuple[tuple[float, ...], ...]

  class LatentAnalyzer:
      def system_coordinates(self, market: Market) -> SystemCoordinates: ...
      def diffusion_coordinates(self, market: Market) -> DiffusionCoordinates: ...
      def attribution(self, market: Market) -> dict[SystemKind, float]:   # Theorem 5.6
          ...
      def project(self, markets: Sequence[Market]) -> StructuralProjection: ...
      def analogues(self, market: Market, library: Sequence[Market], top: int = 3
                    ) -> tuple[tuple[int, float], ...]:                   # d_score, §5.9
          ...
```

Determinism notes: the symmetric eigenproblems are solved by cyclic Jacobi rotations with a
fixed sweep order and a fixed tolerance, so repeated runs are bit-identical; the power
iteration for `ρ(A)` uses a fixed start vector `1/√7 · 1`; ties in `analogues` break by
library index, which the caller controls. Nothing reads the clock, the filesystem, or an
unseeded RNG. `amf.viz` gains one pure renderer, `render_projection_svg`, which draws a
`StructuralProjection` and prints `residual_fraction` into the image next to the existing
`_FOOTNOTE` — so the plot cannot be shown without its own error bar.

---
## 6. Repository governance and boundary analysis

The source note proposes four Python modules under `src/amf/embeddings/`, one example, and one
research document. Three of the four modules cannot be admitted as written. This section names
each collision precisely and gives a reformulation that keeps the intent.

### 6.1 Artefact-by-artefact analysis

| Proposed artefact (verbatim) | Collides with | Precise nature of the collision | Compliant reformulation |
|---|---|---|---|
| `docs/research/embedding_spaces_market_regimes.md` — Theory + methods | Rule 2 only | Documentation is unconstrained by rules 1, 3, 4, but its prose must not claim predictive power or validated performance; the note's "identify 'new' crisis types" and "encoding its effect" do exactly that. | Admit at the proposed path **or** treat this module (`docs/discussions/D2-embedding-spaces-regimes.md`) as its realisation. Either way the file carries the standard `Nature: illustrative and not empirically validated` header and drops every predictive verb. |
| `src/amf/embeddings/regime_vae.py` — Variational autoencoder | **Rules 1, 2, 3** | (a) Rule 3: a VAE needs autodiff and dense linear algebra; `amf` has *zero* runtime dependencies. (b) Rule 3: SGD training is stochastic and non-reproducible across BLAS/threading configurations, breaking bit-identical determinism. (c) Rule 3: 100% statement **and branch** coverage of a training loop is not achievable honestly. (d) Rule 1: the note's own framing trains on "market data" and its pre-training task says "Predict next **price** given past" — `price` is on the `FORBIDDEN` list and `tests/unit/test_non_trading_boundary.py` rejects it in any public name, member, or dataclass field. (e) Rule 2: "sample from latent space to generate new market scenarios" invites reading generated scenarios as forecasts. | Split. **In tree**: `src/amf/latent.py` (§5.10) — closed-form spectral and MDS coordinates, exact attribution, no training, no dependencies, fully coverable. Plus an optional *declared* (not learned) seeded scenario sampler over `[0,1]^70`, mirroring `ShockSimulator.ensemble(seed=…)`. **Out of tree**: an optional research sidecar, e.g. `amf-research-latent`, in its own repository, never a runtime or extra dependency of `amf`, never installed by CI, and explicitly out of scope for the coverage gate. |
| `src/amf/embeddings/contrastive_embeddings.py` — Contrastive learning | **Rules 1, 2, 3** | Same dependency and determinism collisions as above, plus a substantive one: Proposition 5.16 shows InfoNCE over a library of `N` markets cannot certify more than `log N` nats — `6.6` bits out of `~302` at `N = 100`. Training it would be compliant-looking and informationally empty. | Do not implement. Where a *learned* metric was wanted, use the exact `d_score` isometry of Proposition 5.9. If contrastive study is desired for its own sake, it belongs in the out-of-tree sidecar with the ceiling stated in its README. |
| `src/amf/embeddings/embedding_visualizer.py` — 2D projection + interpretation | **Rule 3**, and Rule 2 by implication | t-SNE and UMAP require third-party libraries and (for UMAP) a stochastic optimiser; `amf.viz` draws SVG with the standard library alone and its tests assert byte-identical repeat renders. Proposition 5.14 adds that neighbour embeddings are *undefined* at `n = 7` and uninterpretable in the ways the note wants at any `n` [70–73]. | `amf.viz.render_projection_svg(projection, …)` — a pure renderer for the exact classical-MDS `StructuralProjection` of §5.10, printing `residual_fraction` into the image beside the existing `_FOOTNOTE`, so the error term travels with the picture. |
| `examples/regime_embedding_analogues.py` — Find similar past regimes | Rule 1 (vocabulary), Rule 2 | "Analogue" and "regime" are safe words; the risk is the example's *content*. Anything reading historical prices, returns, or tickers is rejected mechanically and, more importantly, is not something `amf` can consume — the package's only input is an assembled `Market`. | `examples/structural_analogues.py`: build a small library of assembled `Market` objects that differ in declared structure, rank them by `d_score` (Proposition 5.9), and print the exact attribution shares (Theorem 5.6) for the closest match. No external data of any kind. |

### 6.2 Sub-artefact collisions inside the note's prose

| Note text (verbatim fragment) | Collides with | Compliant reformulation |
|---|---|---|
| "Predict next price given past (next-token prediction)" | **Rule 1** — `price` is `FORBIDDEN`. | "Reconstruct a masked structural metric from the remaining descriptor" — masked structural modelling in the sense of [60; 61], stated over `φ(M)`, never over observed data. |
| "Each asset (AAPL, BND, EURUSD, Oil, …)" | **Rule 1** — instrument identifiers are `ticker`-class content; and structurally, `amf` has no per-instrument layer at all. Its finest granularity is `SystemKind` (7 members) and `AnatomicalSystem.components` (free-text labels that no computation reads). | *System* embeddings over the seven `SystemKind`s (Constructions 5.10–5.11). "Tech stocks cluster together" has no representable analogue and should be dropped, not renamed. |
| "Each policy action (rate cut, QE, regulation change, …) → Compressed vector encoding its effect" | **Rule 2** — asserts a real-world causal effect. | `Intervention` embeddings. AMF's `Intervention` already has exactly three degrees of freedom — `target ∈ SystemKind` (7), `absorptive_boost ∈ [0,1]`, `at_step ∈ N` — so the entire "policy" space embeds losslessly in `≤ 9` coordinates (one-hot target plus two scalars). What is embeddable is the *effect on the modelled stress trajectory*, i.e. `Δ resilience` under `propagate(...)`; not the effect on any real economy. |
| "→ Compressed 128D vector" (three times) | Not a rule violation, but false as arithmetic. | `dim φ = 70`; the diagnostic statistic is 28-dimensional; the score vector is 7-dimensional; `rank W ≤ 7` (5 on the sample market); the diagnostic-triple Gram has `rank ≤ 3`. Corollary 5.5 fixes the budget at `≤ 28`. |
| "Benefit: Generalize across time; identify 'new' crisis types" | **Rule 2** — a discovery claim about real markets. | "Report which declared structural configurations in a supplied library are closest to a supplied market under a stated pseudometric, with the distance printed." |
| "SHAP values" | **Rule 3** — `shap` is a third-party package. | Theorem 5.6: exact Shapley shares in seven multiplications, standard library only. |

### 6.3 Cross-cutting implications

**Determinism.** Everything proposed in §5.10 is closed-form. The two numerical routines
involved — cyclic Jacobi for symmetric eigenproblems and power iteration for `ρ(A)` — must be
written with a fixed sweep order, a fixed tolerance, a fixed iteration cap and a fixed start
vector; then repeated runs are bit-identical, as `viz`'s existing tests already demand. Any
*learned* embedding would fail this outright: SGD, dropout, data-loader shuffling and
non-deterministic reductions all break bit-reproducibility, and none of them is fixable by
seeding alone. This is the single strongest technical reason the note's three learned modules
belong out of tree.

**Dependencies.** `amf` declares no runtime dependencies and `tests/unit/test_packaging.py`
guards its metadata. `numpy`, `torch`, `scikit-learn`, `umap-learn` and `shap` are all
excluded by that policy, and adding any of them as an *optional extra* would still put them on
some users' resolution graph. The sidecar route keeps the boundary crisp: a separate
distribution that depends on `amf`, never the reverse.

**Coverage.** The gate is 100% statement *and branch* coverage of `src/amf`. A closed-form
eigensolver is fully coverable — every branch (convergence reached, iteration cap hit,
zero-degree node, rank-deficient Gram, `n = 1` library) can be driven by a small fixture. A
training loop cannot be, and pretending otherwise by lowering the threshold is explicitly
ruled out by `CLAUDE.md` ("the fix for a failing gate is a test, never a lower threshold").

**Naming guard.** `tests/unit/test_non_trading_boundary.py` walks every public class reachable
from `amf.__all__` and checks its members and dataclass fields. Two concrete traps in this
design: (i) a field named `order` (the obvious name for "the systems in row/column order")
would trip the guard — `CouplingMatrix.order` is the *one* documented `ALLOWLIST` entry and a
second one should not be added; §5.10 therefore uses `axis`. (ii) Anything named
`*_signal`, `*_price` or `*_returns` is rejected; the structural vocabulary
(`transmitter`, `receiver`, `spectrum`, `captured_fraction`, `residual_fraction`) is chosen to
be safe by construction.

**Validation claims.** Every construction in §5 is a *re-parameterisation of declared inputs*.
It discovers nothing, predicts nothing and diagnoses nothing about any real market. The
`_DISCLAIMER` in `cli.py` and the `_FOOTNOTE` in `viz.py` must be extended, not bypassed, by
any new renderer; §5.10's `residual_fraction`-in-the-image rule is the specific extension this
module argues for, on the grounds that a projection without its residual is a claim without
its error bar.

**API layering.** `amf.latent` reads `Market`, `DependencyGraph` and `DiagnosticEngine`, and is
read by `report`/`viz`/`cli`. It therefore sits at the `sensitivity` tier of the one-way
dependency order `errors/models ← systems/graph ← market ← diagnostics/simulation ←
sensitivity ← report/viz/cli`, and must not import `report`, `viz` or `cli`. New frozen,
slotted result types with `to_dict()` go in `models.py` or stay local to `latent.py`; if they
are serialised, `report._to_jsonable` and the text/Markdown renderers must be extended, and
`CHANGELOG.md` updated under `## [Unreleased]`.

---

## 7. Falsifiable propositions and open questions

The source note carries no heading named "Key Research Questions" — unlike Q1–Q3, D2 states
its claims inside its **Concept**, **Application to Markets**, **Embedding Methods** and
**Interpretability** blocks. Those claims are reproduced below in substance, each recast so
that it *could* be refuted, with the refuting evidence named. `F1`–`F6` restate the note;
`F7`–`F13` extend it.

**F1 (the note: "High-dimensional data (1000+ features) → Low-dimensional embeddings (e.g.,
128D)").** *Recast*: every numeric output of `amf` is a function of `φ̂(M) ∈ [0,1]^196`, and
every output of `diagnostics`, `simulation` and `sensitivity` is a function of
`φ(M) ∈ [0,1]^70`. **Refuted by**: exhibiting any numeric output that changes between two
markets with identical `φ̂` (or identical `φ`, for the second clause). Free-text `name` and
`components` do not count, since no computation reads them.

**F2 (the note: "Similar states → Similar embeddings (close in latent space)"; "bull_2000 ≈
bull_2016").** *Recast*: as written this is unfalsifiable — no metric, no threshold and no
data are specified. Made falsifiable: *under `d_score` with threshold `θ`, two markets whose
declared structures agree to within `ε` in `ℓ∞` have `d_score ≤ Lε` for a stated Lipschitz
constant `L`.* **Refuted by**: a market pair violating the bound, which would demonstrate that
the diagnostic map is not Lipschitz on the relevant region — a genuinely useful negative.

**F3 (the note: "crisis_2008 ≠ crisis_2020 (different mechanisms, far apart)").** *Recast*:
distinct structural mechanisms produce descriptors that are far apart under `d_φ` **but not
necessarily** under `d_score` or `d_index`, because Proposition 5.3's ladder is many-to-one.
**Refuted by**: showing `d_score` (or `d_index`) separates every pair that `d_φ` separates —
i.e. that the ladder's fibres are trivial. Constructing an explicit pair with equal scores and
different structure refutes the converse and is a five-minute exercise, which is the point.

**F4 (the note: "Tech stocks cluster together; Bond yields near Fed rate").** *Recast*: not
representable. AMF has seven systems and no instrument layer, so no proposition about
instrument clustering can be stated in the package's vocabulary at all. **Refuted by**:
exhibiting an `amf` public API through which per-instrument structure can be declared. There
is none, and rule 1 says there will not be.

**F5 (the note: VAE "Can sample from latent space to generate new market scenarios").**
*Recast*: a VAE with `d = 128` trained on AMF descriptors has at most `70` latent coordinates
carrying non-vanishing information at any ELBO optimum (Proposition 5.15). **Refuted by**: a
trained model in which `> 70` coordinates simultaneously have per-coordinate KL bounded away
from zero across the corpus *and* an ablation showing distortion rises when each is zeroed.

**F6 (the note: "Loss = Contrastive loss (e.g., triplet loss)"; "Similar time periods have
similar embeddings").** *Recast*: contrastive pre-training on a library of `N ≤ 10^3` AMF
markets cannot improve any downstream diagnostic-ranking metric over the exact `d_score`
embedding by more than the comparison's own confidence interval. **Refuted by**: a
pre-registered comparison, with the split declared before training, showing a significant
improvement. Proposition 5.16 says the improvement would have to come from somewhere other
than the `≤ log N` nats the objective can certify.

**F7 (dimension budget).** No representation preserving the overall index and the per-system
score vector requires more than 28 coordinates. **Refuted by**: two markets with equal
`D(φ) ∈ R^28` and different scores.

**F8 (exact attribution).** For every complete market and every valid `DiagnosticConfig`,
`Σ_k crit_k s_k / Σ_j crit_j` equals `DiagnosticReport.overall_index` to floating-point
tolerance, so Theorem 5.6's shares are the unique axiomatic attribution. **Refuted by**: any
market where the identity fails beyond rounding, which would indicate the index is no longer a
criticality-weighted mean.

**F9 (spectral rank).** For markets whose dependency graph has `m` edges among 7 systems,
`rank W ≤ min(7, #{systems with at least one outgoing dependency})`. **Refuted by**: a
counterexample; the bound is elementary, so a violation would indicate a bug in
`coupling_matrix()`.

**F10 (projection adequacy).** For markets in the sample family, at least `95%` of the
variance of the diagnostic triples lies in two classical-MDS coordinates. On the shipped
sample the figure is `98.45%`. **Refuted by**: a plausible market whose figure falls below
`95%` — which would be a useful discovery, since it would identify a structural regime the
2-D projection cannot show.

**F11 (neighbour-embedding inapplicability).** No t-SNE or UMAP configuration produces a
reproducible 2-D map of AMF's seven systems. **Refuted by**: a stated `(perplexity,
initialisation, seed policy)` under which repeated runs agree to a tolerance declared in
advance — noting that with `n = 7`, `Perp < 7` is forced.

**F12 (analogue budget).** Nearest-neighbour analogue retrieval in `d_φ` over any library of
`N < 10^6` hand-assembled markets returns neighbours whose distance exceeds half the library
diameter. **Refuted by**: an actual library where mean nearest-neighbour distance is small —
which would show the corpus is concentrated on a low-dimensional subset, i.e. that the
manifold hypothesis holds for AMF markets. That is the single most valuable experiment this
module suggests, and [19] gives the test.

**F13 (determinism).** A cyclic-Jacobi solver with a fixed sweep order, tolerance and
iteration cap produces bit-identical eigenvectors for a fixed `7×7` input across CPython
versions and platforms. **Refuted by**: a platform pair producing different bits, which would
mean floating-point contraction differences reach the output and the routine needs an explicit
summation order.

**Open questions, in order of value to the repository.**
1. Is the manifold hypothesis true for realistic AMF markets? Run [19]'s test, or estimate
   intrinsic dimension with [20]/[21], on a curated library. A low answer justifies latent
   modelling; a high answer closes the question permanently.
2. What is the diameter and covering number of the *plausible* region of `[0,1]^70`? Rule 2
   forbids fitting this to data, but an analyst-declared plausible region is admissible and
   would turn Proposition 5.17's table from a bound into a budget.
3. Is `D(φ) ↦ index` injective on the plausible region, or are its fibres large? This decides
   whether `d_score` is an adequate analogue metric or discards essential structure.
4. Does `ρ(A)` (Proposition 5.12) predict `converged` in `SimulationTrace` better than the
   existing settling-time heuristic? This is checkable entirely within the package, requires
   no data, and would give the simulator a principled stability flag.
5. Should the standardisation of the diagnostic triples before classical MDS be a
   `LatentConfig` knob, and if so, does that break the determinism guarantee for previously
   published projections? (It changes every published figure — the same argument that keeps
   `scale_concentration_by_reliance` off by default.)

---

## 8. Deliverables

The source note's deliverable list, reproduced exactly:

```markdown
**Deliverable**:
- `docs/research/embedding_spaces_market_regimes.md` — Theory + methods
- `src/amf/embeddings/regime_vae.py` — Variational autoencoder
- `src/amf/embeddings/contrastive_embeddings.py` — Contrastive learning
- `src/amf/embeddings/embedding_visualizer.py` — 2D projection + interpretation
- `examples/regime_embedding_analogues.py` — Find similar past regimes
```

Status and compliance:

| # | Deliverable (as written) | Status | Compliance verdict | Replacement / condition |
|---|---|---|---|---|
| 1 | `docs/research/embedding_spaces_market_regimes.md` — Theory + methods | **Superseded** | Admissible with rule-2 wording | Realised by this module, `docs/discussions/D2-embedding-spaces-regimes.md`. If the original path is also wanted, it must carry the illustrative-only header and drop every predictive verb. |
| 2 | `src/amf/embeddings/regime_vae.py` — Variational autoencoder | **Rejected in tree** | Violates rules 1, 2, 3 (§6.1) | In tree: `src/amf/latent.py` closed-form coordinates + a *declared*, seeded scenario sampler. Out of tree: optional `amf-research-latent` sidecar, never a dependency of `amf`. |
| 3 | `src/amf/embeddings/contrastive_embeddings.py` — Contrastive learning | **Rejected** | Violates rules 1, 2, 3; and informationally empty at AMF's data scale (Proposition 5.16) | Use the exact `d_score` isometry (Proposition 5.9). Sidecar only, with the `log K` ceiling stated in its README. |
| 4 | `src/amf/embeddings/embedding_visualizer.py` — 2D projection + interpretation | **Rejected as specified** | Violates rule 3 (t-SNE/UMAP dependencies); Proposition 5.14 rules out the method at `n = 7` | `amf.viz.render_projection_svg` over an exact classical-MDS `StructuralProjection`, with `residual_fraction` rendered into the image. |
| 5 | `examples/regime_embedding_analogues.py` — Find similar past regimes | **Admissible, renamed** | Safe vocabulary; content must touch no external data | `examples/structural_analogues.py`, plus a case in `tests/integration/test_examples.py` as `CLAUDE.md` requires. |

Additional deliverables this module proposes, all inside the boundary:

| # | Deliverable | Nature | Gate it must pass |
|---|---|---|---|
| 6 | `src/amf/latent.py` | `LatentConfig`, `LatentAnalyzer`, `SystemCoordinates`, `DiffusionCoordinates`, `StructuralProjection` (§5.10) | Zero deps; frozen slotted dataclasses with `to_dict()`; `InvalidConfigError` on bad knobs; 100% branch coverage; naming guard (no field called `order`) |
| 7 | `tests/unit/test_latent.py` | Closed-form fixtures with hand-checked eigenvalues; degenerate cases (`n = 1`, disconnected graph, rank-deficient Gram, zero-degree node) | Part of the 100% gate |
| 8 | `tests/unit/test_properties.py` additions | Hypothesis properties: `Σ_k φ_k = index`; `captured_fraction ∈ [0,1]`; permutation-invariance of every coordinate set up to sign and axis order | Uses the importable `build_market()` helper, not the fixture |
| 9 | `amf.viz.render_projection_svg` | Pure renderer; byte-identical repeat renders; `_FOOTNOTE` plus `residual_fraction` in the image | `tests/unit/test_viz.py` |
| 10 | `amf latent` CLI subcommand | `--format text\|json\|md`, `--rank N`, `--top N` | `tests/integration/test_cli.py` and `test_console_script.py`; `_DISCLAIMER` to stderr |
| 11 | `CHANGELOG.md` under `## [Unreleased]` | Added / Changed entries for 6–10 | Required by `CLAUDE.md`'s change checklist |

---

## 9. Research leadership and prerequisites

The source note's line, reproduced exactly:

```markdown
**Research Leaders Needed**: Deep learning researcher, dimensionality reduction expert
```

Two roles are named. In the boundary-compliant reading, the second is load-bearing and the
first is optional: nothing admitted into `src/amf` requires deep learning, and everything
admitted requires numerical linear algebra done exactly. The matrix below therefore adds the
roles the work actually needs.

### 9.1 Skills matrix

| Role | Non-negotiable skills | Owns | Curriculum modules (§3) | Why the role exists here |
|---|---|---|---|---|
| **Dimensionality-reduction lead** (the note's "dimensionality reduction expert") | Spectral methods; classical and nonmetric MDS; intrinsic-dimension estimation; the distortion literature and its honest reporting | Constructions 5.10–5.13, `src/amf/latent.py`, the residual-reporting rule | M0, M3, M4 | Every *compliant* construction in this module is theirs; nothing here needs a neural network |
| **Numerical-methods engineer** | Floating-point reproducibility; Jacobi/QR eigensolvers; summation-order control; branch-complete testing of iterative routines | The stdlib eigensolver, `F13`, the 100% coverage of iterative code | M0, plus numerical analysis | Determinism is a hard rule and a hand-written solver is where it is won or lost |
| **Deep-learning researcher** (the note's first role) | VAEs, flows, contrastive objectives, and — critically — their failure modes and identifiability limits | The out-of-tree sidecar; the negative results of §5.8–5.9; adjudicating `F5`, `F6` | M5, M6, M7 | Needed to establish what the learned route *cannot* do, which is this module's main finding about it |
| **Statistician / learning theorist** | Sample-complexity bounds; MI estimation limits; pre-registration and multiple-testing discipline | `F6`, `F10`, `F12`; the evaluation protocol for any sidecar experiment | M1, M8, M11 | Without this role the sidecar becomes a data-snooping exercise ([118]–[120]) |
| **Cooperative-game theorist** *(part-time)* | Shapley axiomatics; value-function design and its sensitivity to the reference state | Theorem 5.6, the documented reference state, Remark 5.7 | M9 | The exactness result depends on additivity; someone must own the axioms if the index ever changes shape |
| **Market-structure domain expert** | Market infrastructure, clearing, liquidity provision, supervision | The declared descriptors of any market library; the plausible-region question (Open question 2) | M10 | AMF's inputs are *declared*, not measured; the library's realism is a domain judgement, not a statistical one |
| **Repository maintainer** | `ruff`/`mypy --strict`; the coverage gate; the naming guard; packaging invariants | §6 enforcement; `CHANGELOG.md`; keeping the sidecar out of `amf`'s dependency graph | — | Three of the note's five deliverables are rejected here on repository grounds; someone must hold that line |

### 9.2 Prerequisite ladder

```
  UNDERGRADUATE
    linear algebra (MIT 18.06)              ─┐
    probability (MIT 18.600)                 ├─▶  vectors, eigenvalues, KL, expectation
    multivariable calculus                  ─┘
        │
        ▼
  ADVANCED UNDERGRADUATE / EARLY GRADUATE
    matrix analysis (MIT 18.065; Horn–Johnson [95] Ch. 4, 7, 8)
    convex optimisation (Stanford EE364a; Boyd–Vandenberghe [96] Ch. 5)
    classical dimensionality reduction (ESL [88] §§14.5, 14.8, 14.9; Jolliffe [89])
        │                                    ← everything admitted into src/amf stops here
        ▼
  GRADUATE CORE
    spectral graph theory (Chung [92]; von Luxburg [93])
    graphical models & variational inference (CMU 10-708; Koller–Friedman [94])
    statistical learning theory (MIT 9.520/6.7910; Shalev-Shwartz–Ben-David [97])
        │
        ▼
  GRADUATE SPECIALISATION
    deep generative models (Stanford CS236; Berkeley CS294-158; Murphy [87] Ch. 21, 23)
    self-supervised & contrastive learning (Balestriero et al. [100]; [48; 52; 53; 54])
    identifiability and nonlinear ICA ([36; 37; 38; 39])
        │
        ▼
  RESEARCH FRONTIER
    what the ELBO does and does not determine ([33; 34])
    limits of MI estimation ([49; 50; 51])
    honest evaluation of low-dimensional embeddings ([70; 71; 72; 73])
    evaluation discipline for market claims ([117; 118; 119; 120])
```

**Reading order for a new contributor.** Theorems 2.6 and 2.7 first; then §5.1–5.3, which
contain everything needed to implement deliverables 6–11 and nothing else. §5.8–5.9 and
Theorems 2.14, 2.17, 2.18 only matter to someone arguing for the sidecar. §6 is mandatory for
everyone, because it is the part that decides what may be committed.

---

## References

- [1] K. Pearson, "On lines and planes of closest fit to systems of points in space", *The
  London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science*, Series 6,
  **2**(11), 559–572 (1901).
- [2] H. Hotelling, "Analysis of a complex of statistical variables into principal
  components", *Journal of Educational Psychology* **24**, 417–441 and 498–520 (1933).
- [3] C. Eckart and G. Young, "The approximation of one matrix by another of lower rank",
  *Psychometrika* **1**(3), 211–218 (1936).
- [4] L. Mirsky, "Symmetric gauge functions and unitarily invariant norms", *The Quarterly
  Journal of Mathematics* **11**(1), 50–59 (1960).
- [5] I. J. Schoenberg, "Remarks to Maurice Fréchet's article 'Sur la définition axiomatique
  d'une classe d'espaces distanciés vectoriellement applicable sur l'espace de Hilbert'",
  *Annals of Mathematics* **36**(3), 724–732 (1935).
- [6] G. Young and A. S. Householder, "Discussion of a set of points in terms of their mutual
  distances", *Psychometrika* **3**(1), 19–22 (1938).
- [7] W. S. Torgerson, "Multidimensional scaling: I. Theory and method", *Psychometrika*
  **17**(4), 401–419 (1952).
- [8] J. B. Kruskal, "Multidimensional scaling by optimizing goodness of fit to a nonmetric
  hypothesis", *Psychometrika* **29**(1), 1–27 (1964).
- [9] T. M. Cover and J. A. Thomas, *Elements of Information Theory*, 2nd ed., Wiley
  (2006).
- [10] W. B. Johnson and J. Lindenstrauss, "Extensions of Lipschitz mappings into a Hilbert
  space", in *Conference in Modern Analysis and Probability*, Contemporary Mathematics **26**,
  American Mathematical Society, 189–206 (1984).
- [11] H. Whitney, "Differentiable manifolds", *Annals of Mathematics* **37**(3), 645–680 (1936).
- [12] F. Takens, "Detecting strange attractors in turbulence", in *Dynamical Systems and
  Turbulence, Warwick 1980*, Lecture Notes in Mathematics **898**, Springer, 366–381 (1981).
- [13] T. Sauer, J. A. Yorke and M. Casdagli, "Embedology", *Journal of Statistical Physics*
  **65**(3–4), 579–616 (1991).
- [14] J. B. Tenenbaum, V. de Silva and J. C. Langford, "A global geometric framework for
  nonlinear dimensionality reduction", *Science* **290**(5500), 2319–2323 (2000).
- [15] S. T. Roweis and L. K. Saul, "Nonlinear dimensionality reduction by locally linear
  embedding", *Science* **290**(5500), 2323–2326 (2000).
- [16] M. Belkin and P. Niyogi, "Laplacian eigenmaps for dimensionality reduction and data
  representation", *Neural Computation* **15**(6), 1373–1396 (2003).
- [17] R. R. Coifman and S. Lafon, "Diffusion maps", *Applied and Computational Harmonic
  Analysis* **21**(1), 5–30 (2006).
- [18] B. Schölkopf, A. Smola and K.-R. Müller, "Nonlinear component analysis as a kernel
  eigenvalue problem", *Neural Computation* **10**(5), 1299–1319 (1998).
- [19] C. Fefferman, S. Mitter and H. Narayanan, "Testing the manifold hypothesis", *Journal
  of the American Mathematical Society* **29**(4), 983–1049 (2016).
- [20] E. Levina and P. J. Bickel, "Maximum likelihood estimation of intrinsic dimension", in
  *Advances in Neural Information Processing Systems 17* (2004).
- [21] P. Grassberger and I. Procaccia, "Measuring the strangeness of strange attractors",
  *Physica D: Nonlinear Phenomena* **9**(1–2), 189–208 (1983).
- [22] P. Baldi and K. Hornik, "Neural networks and principal component analysis: Learning
  from examples without local minima", *Neural Networks* **2**(1), 53–58 (1989).
- [23] G. E. Hinton and R. R. Salakhutdinov, "Reducing the dimensionality of data with neural
  networks", *Science* **313**(5786), 504–507 (2006).
- [24] P. Vincent, H. Larochelle, Y. Bengio and P.-A. Manzagol, "Extracting and composing
  robust features with denoising autoencoders", in *Proceedings of the 25th International
  Conference on Machine Learning (ICML)* (2008).
- [25] D. P. Kingma and M. Welling, "Auto-encoding variational Bayes", in *Proceedings of the
  2nd International Conference on Learning Representations (ICLR)* (2014); arXiv:1312.6114.
- [26] D. J. Rezende, S. Mohamed and D. Wierstra, "Stochastic backpropagation and approximate
  inference in deep generative models", in *Proceedings of the 31st International Conference
  on Machine Learning (ICML)*, PMLR **32** (2014); arXiv:1401.4082.
- [27] M. I. Jordan, Z. Ghahramani, T. S. Jaakkola and L. K. Saul, "An introduction to
  variational methods for graphical models", *Machine Learning* **37**(2), 183–233 (1999).
- [28] M. J. Wainwright and M. I. Jordan, "Graphical models, exponential families, and
  variational inference", *Foundations and Trends in Machine Learning* **1**(1–2), 1–305 (2008).
- [29] D. M. Blei, A. Kucukelbir and J. D. McAuliffe, "Variational inference: A review for
  statisticians", *Journal of the American Statistical Association* **112**(518), 859–877 (2017).
- [30] I. Higgins, L. Matthey, A. Pal, C. Burgess, X. Glorot, M. Botvinick, S. Mohamed and
  A. Lerchner, "beta-VAE: Learning basic visual concepts with a constrained variational
  framework", in *Proceedings of the 5th International Conference on Learning Representations
  (ICLR)* (2017).
- [31] S. R. Bowman, L. Vilnis, O. Vinyals, A. M. Dai, R. Jozefowicz and S. Bengio,
  "Generating sentences from a continuous space", in *Proceedings of the 20th SIGNLL
  Conference on Computational Natural Language Learning (CoNLL)* (2016).
- [32] X. Chen, D. P. Kingma, T. Salimans, Y. Duan, P. Dhariwal, J. Schulman, I. Sutskever and
  P. Abbeel, "Variational lossy autoencoder", in *Proceedings of the 5th International
  Conference on Learning Representations (ICLR)* (2017).
- [33] A. A. Alemi, B. Poole, I. Fischer, J. V. Dillon, R. A. Saurous and K. Murphy, "Fixing a
  broken ELBO", in *Proceedings of the 35th International Conference on Machine Learning
  (ICML)*, PMLR **80** (2018).
- [34] B. Dai and D. Wipf, "Diagnosing and enhancing VAE models", in *Proceedings of the 7th
  International Conference on Learning Representations (ICLR)* (2019).
- [35] G. Loaiza-Ganem and J. P. Cunningham, "The continuous Bernoulli: fixing a pervasive
  error in variational autoencoders", in *Advances in Neural Information Processing Systems
  32* (2019).
- [36] A. Hyvärinen and P. Pajunen, "Nonlinear independent component analysis: Existence and
  uniqueness results", *Neural Networks* **12**(3), 429–439 (1999).
- [37] F. Locatello, S. Bauer, M. Lucic, G. Rätsch, S. Gelly, B. Schölkopf and O. Bachem,
  "Challenging common assumptions in the unsupervised learning of disentangled
  representations", in *Proceedings of the 36th International Conference on Machine Learning
  (ICML)*, PMLR **97** (2019).
- [38] I. Khemakhem, D. P. Kingma, R. P. Monti and A. Hyvärinen, "Variational autoencoders and
  nonlinear ICA: A unifying framework", in *Proceedings of the 23rd International Conference
  on Artificial Intelligence and Statistics (AISTATS)*, PMLR **108** (2020).
- [39] F. Locatello, B. Poole, G. Rätsch, B. Schölkopf, O. Bachem and M. Tschannen,
  "Weakly-supervised disentanglement without compromises", in *Proceedings of the 37th
  International Conference on Machine Learning (ICML)*, PMLR **119** (2020).
- [40] D. J. Rezende and S. Mohamed, "Variational inference with normalizing flows", in
  *Proceedings of the 32nd International Conference on Machine Learning (ICML)*, PMLR **37**
  (2015).
- [41] L. Dinh, J. Sohl-Dickstein and S. Bengio, "Density estimation using Real NVP", in
  *Proceedings of the 5th International Conference on Learning Representations (ICLR)* (2017).
- [42] G. Papamakarios, E. Nalisnick, D. J. Rezende, S. Mohamed and B. Lakshminarayanan,
  "Normalizing flows for probabilistic modeling and inference", *Journal of Machine Learning
  Research* **22**(57), 1–64 (2021).
- [43] M. Gutmann and A. Hyvärinen, "Noise-contrastive estimation: A new estimation principle
  for unnormalized statistical models", in *Proceedings of the 13th International Conference
  on Artificial Intelligence and Statistics (AISTATS)*, PMLR **9** (2010).
- [44] S. Chopra, R. Hadsell and Y. LeCun, "Learning a similarity metric discriminatively,
  with application to face verification", in *Proceedings of the IEEE Conference on Computer
  Vision and Pattern Recognition (CVPR)* (2005).
- [45] R. Hadsell, S. Chopra and Y. LeCun, "Dimensionality reduction by learning an invariant
  mapping", in *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition
  (CVPR)* (2006).
- [46] F. Schroff, D. Kalenichenko and J. Philbin, "FaceNet: A unified embedding for face
  recognition and clustering", in *Proceedings of the IEEE Conference on Computer Vision and
  Pattern Recognition (CVPR)*, 815–823 (2015).
- [47] K. Q. Weinberger and L. K. Saul, "Distance metric learning for large margin nearest
  neighbor classification", *Journal of Machine Learning Research* **10**, 207–244 (2009).
- [48] A. van den Oord, Y. Li and O. Vinyals, "Representation learning with contrastive
  predictive coding", arXiv:1807.03748 (2018).
- [49] B. Poole, S. Ozair, A. van den Oord, A. A. Alemi and G. Tucker, "On variational bounds
  of mutual information", in *Proceedings of the 36th International Conference on Machine
  Learning (ICML)*, PMLR **97**, 5171–5180 (2019).
- [50] D. McAllester and K. Stratos, "Formal limitations on the measurement of mutual
  information", in *Proceedings of the 23rd International Conference on Artificial
  Intelligence and Statistics (AISTATS)*, PMLR **108** (2020).
- [51] M. Tschannen, J. Djolonga, P. K. Rubenstein, S. Gelly and M. Lucic, "On mutual
  information maximization for representation learning", in *Proceedings of the 8th
  International Conference on Learning Representations (ICLR)* (2020).
- [52] T. Chen, S. Kornblith, M. Norouzi and G. Hinton, "A simple framework for contrastive
  learning of visual representations", in *Proceedings of the 37th International Conference on
  Machine Learning (ICML)*, PMLR **119** (2020).
- [53] K. He, H. Fan, Y. Wu, S. Xie and R. Girshick, "Momentum contrast for unsupervised
  visual representation learning", in *Proceedings of the IEEE/CVF Conference on Computer
  Vision and Pattern Recognition (CVPR)* (2020).
- [54] J.-B. Grill, F. Strub, F. Altché, C. Tallec, P. H. Richemond, E. Buchatskaya, C. Doersch,
  B. Ávila Pires, Z. D. Guo, M. G. Azar, B. Piot, K. Kavukcuoglu, R. Munos and M. Valko,
  "Bootstrap your own latent: A new approach to self-supervised learning", in *Advances in
  Neural Information Processing Systems 33* (2020).
- [55] X. Chen and K. He, "Exploring simple Siamese representation learning", in *Proceedings
  of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)* (2021).
- [56] J. Zbontar, L. Jing, I. Misra, Y. LeCun and S. Deny, "Barlow Twins: Self-supervised
  learning via redundancy reduction", in *Proceedings of the 38th International Conference on
  Machine Learning (ICML)*, PMLR **139** (2021).
- [57] T. Wang and P. Isola, "Understanding contrastive representation learning through
  alignment and uniformity on the hypersphere", in *Proceedings of the 37th International
  Conference on Machine Learning (ICML)*, PMLR **119** (2020).
- [58] S. Arora, H. Khandeparkar, M. Khodak, O. Plevrakis and N. Saunshi, "A theoretical
  analysis of contrastive unsupervised representation learning", in *Proceedings of the 36th
  International Conference on Machine Learning (ICML)*, PMLR **97** (2019).
- [59] L. Jing, P. Vincent, Y. LeCun and Y. Tian, "Understanding dimensional collapse in
  contrastive self-supervised learning", in *Proceedings of the 10th International Conference
  on Learning Representations (ICLR)* (2022); arXiv:2110.09348.
- [60] J. Devlin, M.-W. Chang, K. Lee and K. Toutanova, "BERT: Pre-training of deep
  bidirectional transformers for language understanding", in *Proceedings of NAACL-HLT* (2019).
- [61] K. He, X. Chen, S. Xie, Y. Li, P. Dollár and R. Girshick, "Masked autoencoders are
  scalable vision learners", in *Proceedings of the IEEE/CVF Conference on Computer Vision and
  Pattern Recognition (CVPR)* (2022).
- [62] T. Mikolov, K. Chen, G. Corrado and J. Dean, "Efficient estimation of word
  representations in vector space", arXiv:1301.3781 (2013).
- [63] T. Mikolov, I. Sutskever, K. Chen, G. Corrado and J. Dean, "Distributed representations
  of words and phrases and their compositionality", in *Advances in Neural Information
  Processing Systems 26* (2013).
- [64] T. Mikolov, W.-t. Yih and G. Zweig, "Linguistic regularities in continuous space word
  representations", in *Proceedings of NAACL-HLT*, 746–751 (2013).
- [65] J. Pennington, R. Socher and C. D. Manning, "GloVe: Global vectors for word
  representation", in *Proceedings of the 2014 Conference on Empirical Methods in Natural
  Language Processing (EMNLP)*, 1532–1543 (2014).
- [66] O. Levy and Y. Goldberg, "Neural word embedding as implicit matrix factorization", in
  *Advances in Neural Information Processing Systems 27* (2014).
- [67] Y. Bengio, A. Courville and P. Vincent, "Representation learning: A review and new
  perspectives", *IEEE Transactions on Pattern Analysis and Machine Intelligence* **35**(8),
  1798–1828 (2013).
- [68] L. van der Maaten and G. Hinton, "Visualizing data using t-SNE", *Journal of Machine
  Learning Research* **9**, 2579–2605 (2008).
- [69] L. McInnes, J. Healy and J. Melville, "UMAP: Uniform manifold approximation and
  projection for dimension reduction", arXiv:1802.03426 (2018).
- [70] M. Wattenberg, F. Viégas and I. Johnson, "How to use t-SNE effectively", *Distill*
  (2016), doi:10.23915/distill.00002.
- [71] D. Kobak and P. Berens, "The art of using t-SNE for single-cell transcriptomics",
  *Nature Communications* **10**, 5416 (2019).
- [72] D. Kobak and G. C. Linderman, "Initialization is critical for preserving global data
  structure in both t-SNE and UMAP", *Nature Biotechnology* **39**, 156–157 (2021).
- [73] T. Chari and L. Pachter, "The specious art of single-cell genomics", *PLOS
  Computational Biology* **19**(8), e1011288 (2023).
- [74] L. S. Shapley, "A value for n-person games", in *Contributions to the Theory of Games,
  Volume II*, Annals of Mathematics Studies **28**, Princeton University Press, 307–317 (1953).
- [75] H. P. Young, "Monotonic solutions of cooperative games", *International Journal of Game
  Theory* **14**(2), 65–72 (1985).
- [76] E. Štrumbelj and I. Kononenko, "Explaining prediction models and individual predictions
  with feature contributions", *Knowledge and Information Systems* **41**(3), 647–665 (2014).
- [77] S. M. Lundberg and S.-I. Lee, "A unified approach to interpreting model predictions",
  in *Advances in Neural Information Processing Systems 30* (2017).
- [78] I. E. Kumar, S. Venkatasubramanian, C. Scheidegger and S. Friedler, "Problems with
  Shapley-value-based explanations as feature importance measures", in *Proceedings of the
  37th International Conference on Machine Learning (ICML)*, PMLR **119** (2020).
- [79] M. Sundararajan and A. Najmi, "The many Shapley values for model explanation", in
  *Proceedings of the 37th International Conference on Machine Learning (ICML)*, PMLR **119**
  (2020).
- [80] D. Janzing, L. Minorics and P. Blöbaum, "Feature relevance quantification in explainable
  AI: A causal problem", in *Proceedings of the 23rd International Conference on Artificial
  Intelligence and Statistics (AISTATS)*, PMLR **108** (2020).
- [81] E. N. Lorenz, "Atmospheric predictability as revealed by naturally occurring analogues",
  *Journal of the Atmospheric Sciences* **26**(4), 636–646 (1969).
- [82] H. M. van den Dool, "Searching for analogues, how long must we wait?", *Tellus A*
  **46**(3), 314–324 (1994).
- [83] J. D. Farmer and J. J. Sidorowich, "Predicting chaotic time series", *Physical Review
  Letters* **59**(8), 845–848 (1987).
- [84] G. Sugihara and R. M. May, "Nonlinear forecasting as a way of distinguishing chaos from
  measurement error in time series", *Nature* **344**, 734–741 (1990).
- [85] C. M. Bishop, *Pattern Recognition and Machine Learning*, Springer (2006).
- [86] I. Goodfellow, Y. Bengio and A. Courville, *Deep Learning*, MIT Press (2016).
- [87] K. P. Murphy, *Probabilistic Machine Learning: Advanced Topics*, MIT Press (2023).
- [88] T. Hastie, R. Tibshirani and J. Friedman, *The Elements of Statistical Learning: Data
  Mining, Inference, and Prediction*, 2nd ed., Springer (2009).
- [89] I. T. Jolliffe, *Principal Component Analysis*, 2nd ed., Springer (2002).
- [90] I. Borg and P. J. F. Groenen, *Modern Multidimensional Scaling: Theory and
  Applications*, 2nd ed., Springer (2005).
- [91] J. A. Lee and M. Verleysen, *Nonlinear Dimensionality Reduction*, Springer (2007).
- [92] F. R. K. Chung, *Spectral Graph Theory*, CBMS Regional Conference Series in Mathematics
  **92**, American Mathematical Society (1997).
- [93] U. von Luxburg, "A tutorial on spectral clustering", *Statistics and Computing*
  **17**(4), 395–416 (2007).
- [94] D. Koller and N. Friedman, *Probabilistic Graphical Models: Principles and Techniques*,
  MIT Press (2009).
- [95] R. A. Horn and C. R. Johnson, *Matrix Analysis*, 2nd ed., Cambridge University Press
  (2013).
- [96] S. Boyd and L. Vandenberghe, *Convex Optimization*, Cambridge University Press (2004).
- [97] S. Shalev-Shwartz and S. Ben-David, *Understanding Machine Learning: From Theory to
  Algorithms*, Cambridge University Press (2014).
- [98] C. Molnar, *Interpretable Machine Learning: A Guide for Making Black Box Models
  Explainable*, 2nd ed. (2022).
- [99] B. Peleg and P. Sudhölter, *Introduction to the Theory of Cooperative Games*, 2nd ed.,
  Springer (2007).
- [100] R. Balestriero, M. Ibrahim, V. Sobal, A. Morcos, S. Shekhar, T. Goldstein, F. Bordes,
  A. Bardes, G. Mialon, Y. Tian, A. Schwarzschild, A. G. Wilson, J. Geiping, Q. Garrido,
  P. Fernandez, A. Bar, H. Pirsiavash, Y. LeCun and M. Goldblum, "A cookbook of
  self-supervised learning", arXiv:2304.12210 (2023).
- [101] J. M. Tomczak, *Deep Generative Modeling*, Springer (2022).
- [102] J. D. Hamilton, "A new approach to the economic analysis of nonstationary time series
  and the business cycle", *Econometrica* **57**(2), 357–384 (1989).
- [103] J. D. Hamilton, *Time Series Analysis*, Princeton University Press (1994).
- [104] A. Ang and A. Timmermann, "Regime changes and financial markets", *Annual Review of
  Financial Economics* **4**, 313–337 (2012).
- [105] J. Bai and S. Ng, "Determining the number of factors in approximate factor models",
  *Econometrica* **70**(1), 191–221 (2002).
- [106] J. H. Stock and M. W. Watson, "Forecasting using principal components from a large
  number of predictors", *Journal of the American Statistical Association* **97**(460),
  1167–1179 (2002).
- [107] L. Laloux, P. Cizeau, J.-P. Bouchaud and M. Potters, "Noise dressing of financial
  correlation matrices", *Physical Review Letters* **83**(7), 1467–1470 (1999).
- [108] V. Plerou, P. Gopikrishnan, B. Rosenow, L. A. N. Amaral, T. Guhr and H. E. Stanley,
  "Random matrix approach to cross correlations in financial data", *Physical Review E*
  **65**, 066126 (2002).
- [109] V. A. Marčenko and L. A. Pastur, "Distribution of eigenvalues for some sets of random
  matrices", *Mathematics of the USSR-Sbornik* **1**(4), 457–483 (1967).
- [110] R. N. Mantegna, "Hierarchical structure in financial markets", *The European Physical
  Journal B* **11**(1), 193–197 (1999).
- [111] M. Kritzman, Y. Li, S. Page and R. Rigobon, "Principal components as a measure of
  systemic risk", *The Journal of Portfolio Management* **37**(4), 112–126 (2011).
- [112] M. Billio, M. Getmansky, A. W. Lo and L. Pelizzon, "Econometric measures of
  connectedness and systemic risk in the finance and insurance sectors", *Journal of Financial
  Economics* **104**(3), 535–559 (2012).
- [113] F. X. Diebold and K. Yılmaz, "On the network topology of variance decompositions:
  Measuring the connectedness of financial firms", *Journal of Econometrics* **182**(1),
  119–134 (2014).
- [114] D. Acemoglu, V. M. Carvalho, A. Ozdaglar and A. Tahbaz-Salehi, "The network origins of
  aggregate fluctuations", *Econometrica* **80**(5), 1977–2016 (2012).
- [115] S. Battiston, M. Puliga, R. Kaushik, P. Tasca and G. Caldarelli, "DebtRank: Too
  central to fail? Financial networks, the FED and systemic risk", *Scientific Reports* **2**,
  541 (2012).
- [116] S. Gu, B. Kelly and D. Xiu, "Empirical asset pricing via machine learning", *The Review
  of Financial Studies* **33**(5), 2223–2273 (2020).
- [117] R. Cont, "Empirical properties of asset returns: stylized facts and statistical
  issues", *Quantitative Finance* **1**(2), 223–236 (2001).
- [118] H. White, "A reality check for data snooping", *Econometrica* **68**(5), 1097–1126 (2000).
- [119] D. H. Bailey, J. M. Borwein, M. López de Prado and Q. J. Zhu, "Pseudo-mathematics and
  financial charlatanism: The effects of backtest overfitting on out-of-sample performance",
  *Notices of the American Mathematical Society* **61**(5), 458–471 (2014).
- [120] C. R. Harvey, Y. Liu and H. Zhu, "… and the cross-section of expected returns", *The
  Review of Financial Studies* **29**(1), 5–68 (2016).
- [121] M. López de Prado, *Advances in Financial Machine Learning*, Wiley (2018).

---

> **Reminder.** `amf` models market *structure and resilience* only. Nothing in this module is
> a trading system, a forecast, a diagnosis of any real market, or financial advice; its
> thresholds, weights, dimensions and scores are illustrative and have not been empirically
> validated.
