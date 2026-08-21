# H2: Topological Data Analysis (TDA) & Persistent Homology

> **Discussion category**: Research · **Labels**: `H2`, `topology`, `theory`, `research`
> **Source**: `docs/QUANTUM_NEURAL_RESEARCH.md` § Discussion H2
> **Status**: Open for comment · **Nature**: Theoretical module, illustrative and not
> empirically validated

---

## 0. Abstract and reading guide

Persistent homology assigns to a *filtered* topological space a complete discrete invariant —
a barcode — that records the scale at which each connected component, loop and void is born
and dies. Its appeal for a structural framework like AMF is precise and narrow: it is a
coordinate-free, deformation-invariant summary of shape, and the Stability Theorem
(Cohen-Steiner–Edelsbrunner–Harer, 2007) guarantees that a small perturbation of the input
produces a small perturbation of the barcode. That stability property is what makes the
invariant usable at all; without it, barcodes would be noise amplifiers.

This module claims that AMF's dependency graph carries a natural weight filtration whose
persistent homology has a direct structural reading: `β₀` counts coupling-connected blocks of
the seven systems, and `β₁` of the associated flag complex counts *independent feedback loops
that are not triangulated* — a quantity closely related to, but not identical with, the simple
cycles the `graph` module already enumerates. It further claims that the Stability Theorem
gives AMF something it currently lacks: a Lipschitz robustness statement relating dependency
weight perturbations to changes in a structural summary.

It does **not** claim that persistent homology predicts crises, that Betti numbers are an
early-warning indicator, or that the finance TDA literature has established either. §7 states
the propositions in refutable form; §4.5 cites the application literature *and* the reasons to
treat it cautiously.

**Prerequisites**: point-set topology (continuity, compactness, quotient spaces); linear
algebra over a field, including rank–nullity and Smith normal form; basic group theory. The
ladder is in §9.

---

## 1. Verbatim source specification

The following is the source note's specification for this discussion, reproduced word for
word without alteration:

````markdown
### Discussion H2: Topological Data Analysis (TDA) & Persistent Homology
**Theme**: Use algebraic topology to find hidden market structure

**Concept**:
- Topological data analysis: Map point clouds (market data) to topological features
- Persistent homology: Track which features survive across scales
- Application: Identify multi-scale market structure (cycles, clusters, voids)

**Example**:
```
Market data: 10,000 daily price points for 100 assets
Classical ML: Dimension reduction to 2D (t-SNE), plot
Problem: t-SNE loses information about global structure

TDA approach:
1. Compute pairwise distances between all data points
2. Build filtration: Connect points at increasing distance thresholds
3. Track topological features:
   - Connected components (market clusters)
   - Holes (market cycles/regimes)
   - Voids (market gaps/rare regions)
4. Plot persistence diagram: Which features are stable vs. noise?

Result: Discover that market has 3 stable regimes (robust across scales)
        and 2 intermediate transitions (ephemeral)
        
Interpretation: Market clusters into bull/bear/transition, not noise
```

**Application to Crisis Prediction**:
```
Pre-crisis: Topology smooth (few connected components)
Crisis arrival: Topology fractures (many disconnected clusters)
Post-crisis: Topology stabilizes (new connected structure)

Metric: Track Betti numbers (# of holes, components, voids)
  Threshold: If Betti number jumps, market topology is changing → crisis signal
```

**Deliverable**:
- `docs/research/topological_data_analysis.md` — TDA theory
- `src/amf/tda/persistent_homology.py` — Persistence computation
- `src/amf/tda/betti_numbers.py` — Topological metrics
- `examples/market_topology_crisis_detection.py` — Test on historical data

**Research Leaders Needed**: Topologist, computational geometry specialist
````

---

## 2. Formal foundations

### 2.1 Simplicial complexes

**Definition 2.1 (Abstract simplicial complex).** Let `V` be a finite set. An abstract
simplicial complex `K` on `V` is a collection of non-empty subsets of `V`, called *simplices*,
closed under passage to non-empty subsets: if `σ ∈ K` and `∅ ≠ τ ⊆ σ` then `τ ∈ K`. The
*dimension* of `σ` is `|σ| − 1`. The `k`-skeleton `K⁽ᵏ⁾` is the subcomplex of simplices of
dimension `≤ k`.

**Definition 2.2 (Vietoris–Rips complex).** For a finite metric space `(X, d)` and `ε ≥ 0`,

```
VR_ε(X) = { σ ⊆ X : σ ≠ ∅ and d(x, y) ≤ ε for all x, y ∈ σ }
```

`VR_ε` is the *flag* (or *clique*) complex of the graph with edge set
`{ {x,y} : d(x,y) ≤ ε }`: a simplex is present exactly when all of its edges are. This is the
construction the source note describes in its step 2, "Connect points at increasing distance
thresholds".

**Definition 2.3 (Čech complex).** `Č_ε(X) = { σ ⊆ X : ⋂_{x∈σ} B(x, ε) ≠ ∅ }`, where `B(x,ε)`
is the closed ball of radius `ε`.

**Theorem 2.4 (Nerve theorem).** If the sets of a finite cover of a paracompact space are open
and every non-empty finite intersection is contractible, the nerve of the cover is homotopy
equivalent to the union. Consequently `Č_ε(X)` is homotopy equivalent to the union of
`ε`-balls around `X` in Euclidean space, where balls are convex and intersections contractible.
The classical statements are due to Borsuk and to Leray; see Hatcher [10, §4.G] and
Edelsbrunner–Harer [6, §III.2].

**Remark 2.5.** The Vietoris–Rips complex enjoys *no* such theorem, which is the standard
trade-off: `VR_ε` is far cheaper to build (only pairwise distances are needed) but is only
sandwiched between Čech complexes, `Č_ε(X) ⊆ VR_{2ε}(X) ⊆ Č_{2ε}(X)` in Euclidean space with
the usual conventions. Everything below uses `VR`, so its topological readings are *interleaved
approximations*, not homotopy-equivalent models. This distinction is routinely elided in
applied papers and should not be elided here.

### 2.2 Simplicial homology

Fix a field `F` (in practice `F = 𝔽₂`, which removes orientation bookkeeping). Let `C_k(K)` be
the `F`-vector space with basis the `k`-simplices of `K`, and let

```
∂_k : C_k(K) → C_{k−1}(K),    ∂_k(v₀ … v_k) = Σ_{i=0}^{k} (−1)^i (v₀ … v̂_i … v_k)
```

(over `𝔽₂` the signs vanish).

**Lemma 2.6.** `∂_{k−1} ∘ ∂_k = 0`.

**Definition 2.7.** `Z_k = ker ∂_k` (cycles), `B_k = im ∂_{k+1}` (boundaries); by Lemma 2.6,
`B_k ⊆ Z_k`, and the `k`-th homology is `H_k(K; F) = Z_k / B_k`. The `k`-th **Betti number** is
`β_k = dim_F H_k(K; F)`.

Interpretation, matching the source note's step 3: `β₀` = number of connected components
("clusters"); `β₁` = number of independent 1-dimensional loops ("holes"); `β₂` = number of
enclosed cavities ("voids").

**Proposition 2.8 (Euler–Poincaré).** For a finite complex `K`,
`χ(K) = Σ_k (−1)^k |K_k| = Σ_k (−1)^k β_k`, where `|K_k|` is the number of `k`-simplices.
This gives a cheap consistency check on any implementation: the alternating simplex count must
equal the alternating Betti count.

**Proposition 2.9 (Graph case).** For a graph `G` with `n` vertices, `m` edges and `c`
connected components, `β₀(G) = c` and `β₁(G) = m − n + c`, the *cycle rank* (first Betti number
of the graph). If `X(G)` denotes the flag complex of `G`, then `β₀(X(G)) = c` and
`β₁(X(G)) ≤ m − n + c`, with the deficit accounted for by cycles that bound filled triangles
and higher simplices. This inequality is the precise sense in which "loops" in the flag complex
and "simple cycles" in the graph are *different* counts — see §5.3, where it matters for AMF.

### 2.3 Filtrations, persistence modules, barcodes

**Definition 2.10 (Filtration).** A filtration is a nested family `{K_a}_{a ∈ ℝ}` of
subcomplexes with `K_a ⊆ K_b` whenever `a ≤ b`. Inclusions induce linear maps
`H_k(K_a) → H_k(K_b)`, so `a ↦ H_k(K_a)` is a functor from `(ℝ, ≤)` to `F`-vector spaces — a
**persistence module**.

**Theorem 2.11 (Structure theorem / barcode decomposition).** A persistence module of finite
type over a field decomposes uniquely (up to isomorphism and reordering of summands) as a
finite direct sum of *interval modules* `F[b, d)`. The multiset of intervals `{[b_i, d_i)}` is
the **barcode**; plotted as points `(b_i, d_i)` in the plane it is the **persistence diagram**.
The finite-type statement and the algorithm are due to Zomorodian and Carlsson [2]; the
generalisation to pointwise finite-dimensional modules indexed by `ℝ` is Crawley-Boevey [14].

The quantity `d_i − b_i` is the *persistence* (lifetime) of a feature. The source note's
"Which features are stable vs. noise?" is exactly the question of which bars are long.

**Definition 2.12 (Bottleneck distance).** For diagrams `D, D'` (augmented with the diagonal
`Δ` with infinite multiplicity),

```
d_B(D, D') = inf_{η : D → D'}  sup_{x ∈ D}  ‖x − η(x)‖_∞
```

over bijections `η`. The `p`-Wasserstein distance replaces the sup by an `ℓ_p` sum.

**Theorem 2.13 (Stability; Cohen-Steiner, Edelsbrunner & Harer, 2007 [5]).** Let `f, g : X → ℝ`
be tame continuous functions on a triangulable space. Then the persistence diagrams of their
sublevel-set filtrations satisfy

```
d_B( D(f), D(g) )  ≤  ‖f − g‖_∞ .
```

This is the theorem the whole enterprise rests on: the map from data to barcode is
1-Lipschitz. Wasserstein-stability requires extra hypotheses and is *not* a corollary.

**Theorem 2.14 (Rips stability, consequence).** If `X, Y` are finite metric spaces, the
persistence diagrams of their Vietoris–Rips filtrations satisfy
`d_B(D(VR(X)), D(VR(Y))) ≤ 2 · d_{GH}(X, Y)`, where `d_{GH}` is the Gromov–Hausdorff distance.
See Chazal–de Silva–Glisse–Oudot [13] for the persistence-module formulation via interleaving.

**Definition 2.15 (Interleaving).** Persistence modules `M, N` are `δ`-interleaved if there are
maps `M_a → N_{a+δ}` and `N_a → M_{a+δ}` commuting with the structure maps and composing to the
internal maps of shift `2δ`. The **isometry theorem** states that the interleaving distance
equals the bottleneck distance of the corresponding diagrams [13].

### 2.4 Computation

**Algorithm 2.16 (Standard reduction).** Order the simplices compatibly with the filtration and
refining by dimension. Reduce the boundary matrix `∂` left-to-right by column additions,
recording the lowest non-zero entry of each column; pairs `(low(j), j)` give birth–death pairs.
Worst case `O(N³)` in the number of simplices `N`; in practice far faster. Milosavljević,
Morozov and Skraba showed a bound in matrix-multiplication time; Bauer's `Ripser` [17] gives
the strongest practical implementation for Vietoris–Rips. Otter, Porter, Tillmann, Grindrod and
Harrington [16] survey the computational landscape.

**Warning 2.17 (Combinatorial explosion).** `VR_ε` on `n` points can have up to `2ⁿ − 1`
simplices. The source note's example — "10,000 daily price points for 100 assets" — is
computationally serious in dimension `≥ 2` and is normally handled by capping the maximum
homological dimension and the maximum `ε`, or by using witness or alpha complexes. Any
implementation must state its truncation explicitly rather than silently capping.

### 2.5 Vectorisation and statistics

Persistence diagrams live in a metric space that is not a vector space: means are not defined
pointwise, and Fréchet means need not be unique (Turner, Mileyko, Mukherjee and Harer [15]).
Two standard remedies embed diagrams into a Banach or Hilbert space:

- **Persistence landscapes** (Bubenik [11]): the sequence of functions
  `λ_k(t) = k-th largest value of  min(t − b, d − t)_+`  over bars `[b,d)`. Landscapes are
  stable in the `∞`-norm and admit ordinary means and hypothesis tests.
- **Persistence images** (Adams et al. [12]): a stable, finite-dimensional vectorisation
  obtained by smoothing a weighted diagram and integrating over a grid.

Confidence sets for persistence diagrams via the bootstrap are given by Fasy, Lecci, Rinaldo,
Wasserman, Balakrishnan and Singh [18] — the reference to use when someone claims a bar is
"significant".

### 2.6 From a time series to a point cloud

**Theorem 2.18 (Takens embedding, 1981 [19]).** Let `M` be a compact manifold of dimension `m`,
`φ` a smooth diffeomorphism and `y : M → ℝ` a smooth observation function. For generic
`(φ, y)` and `k > 2m`, the delay map

```
Φ(x) = ( y(x), y(φ(x)), …, y(φ^{k−1}(x)) )  ∈ ℝ^k
```

is an embedding of `M` into `ℝ^k`.

This is what licenses turning a scalar structural time series into a point cloud at all.
Selecting the delay and the embedding dimension is a genuine and unsolved practical problem;
the theorem is generic, not constructive. **Sliding-window persistence** (Perea and Harer [20])
develops the periodicity-detection consequences and is the correct citation for "roundness of
the sliding-window cloud measures periodicity".

---

## 3. Academic curriculum modules

| Module | Level | Canonical courses | Core texts | What AMF needs from it |
|---|---|---|---|---|
| Point-set topology | Undergraduate 3rd year | General topology courses; Cambridge Part II Topological Spaces | Munkres, *Topology* | Continuity, compactness, quotient and metric topologies — the substrate for everything else |
| Algebraic topology I: homology | Advanced undergraduate / 1st-year graduate | Cambridge Part III Algebraic Topology; standard US first-year graduate topology | Hatcher [10] Ch. 2; Munkres, *Elements of Algebraic Topology* [9] | Chain complexes, simplicial and singular homology, exactness, Mayer–Vietoris |
| Computational topology | Graduate topics course | Stanford's computational-topology topics course (offered as CS 468 in several years); Duke's TDA courses; EPFL applied topology | Edelsbrunner & Harer [6]; Kaczynski–Mischaikow–Mrozek, *Computational Homology* | Filtrations, the reduction algorithm, alpha/Čech/Rips complexes, duality |
| Persistence theory | Graduate / research | ICERM and AIM workshop programmes; summer schools in applied topology | Chazal–de Silva–Glisse–Oudot [13]; Oudot, *Persistence Theory* | Structure theorem, interleaving, isometry theorem, stability |
| Statistical TDA | Graduate | Statistics departments' topological-inference seminars (CMU in particular) | Fasy et al. [18]; Bubenik [11]; Chazal & Michel [8] | Confidence sets, bootstrap, Fréchet means, multiple testing on bars |
| Dynamical systems & embedding | Graduate | Nonlinear dynamics / chaos courses | Takens [19]; Kantz & Schreiber, *Nonlinear Time Series Analysis* | Delay embedding, attractor reconstruction, parameter selection |
| Graph theory & combinatorics | Undergraduate | Discrete mathematics sequences | Diestel, *Graph Theory* | Cycle rank, connectivity, clique complexes — the AMF-sized case |

The efficient path for a reader who only wants AMF's use case: Hatcher Ch. 2 (homology of
simplicial complexes), then Edelsbrunner–Harer Ch. III–VII (persistence), then Chazal &
Michel [8] as the applied bridge, then Gidea & Katz [21] as the worked financial example.
Everything in §5 below is computable from that.

---

## 4. Exact source material

### 4.1 Primary and seminal papers

- **Edelsbrunner, H., Letscher, D. and Zomorodian, A.** "Topological Persistence and
  Simplification." *Discrete & Computational Geometry* **28**(4), 511–533 (2002). Introduces
  persistence for filtrations of complexes in `ℝ³` and the pairing algorithm. The origin point.
- **Zomorodian, A. and Carlsson, G.** "Computing Persistent Homology." *Discrete &
  Computational Geometry* **33**(2), 249–274 (2005). Recasts persistence as a graded module
  over a polynomial ring, proving the structure theorem over a field and giving the general
  algorithm. This is the paper that made barcodes a complete invariant.
- **Cohen-Steiner, D., Edelsbrunner, H. and Harer, J.** "Stability of Persistence Diagrams."
  *Discrete & Computational Geometry* **37**(1), 103–120 (2007). The 1-Lipschitz bound of
  Theorem 2.13. Without it, nothing downstream is defensible.
- **Carlsson, G.** "Topology and Data." *Bulletin of the American Mathematical Society*
  **46**(2), 255–308 (2009). The manifesto that defined the field's programme.
- **Ghrist, R.** "Barcodes: The Persistent Topology of Data." *Bulletin of the American
  Mathematical Society* **45**(1), 61–75 (2008). The clearest short exposition of barcodes.
- **Crawley-Boevey, W.** "Decomposition of pointwise finite-dimensional persistence modules."
  *Journal of Algebra and its Applications* **14**(5), 1550066 (2015). Removes the finite-type
  hypothesis from the structure theorem.
- **Takens, F.** "Detecting strange attractors in turbulence." In *Dynamical Systems and
  Turbulence, Warwick 1980*, Lecture Notes in Mathematics **898**, Springer, 366–381 (1981).
  The embedding theorem.
- **Singh, G., Mémoli, F. and Carlsson, G.** "Topological Methods for the Analysis of High
  Dimensional Data Sets and 3D Object Recognition." *Eurographics Symposium on Point-Based
  Graphics* (2007). The Mapper algorithm — a different, complementary TDA tool that produces a
  graph summary rather than a barcode.

### 4.2 Canonical textbooks

- **Hatcher, A.** *Algebraic Topology.* Cambridge University Press, 2002. **Chapter 2** is the
  homology reference; §2.1 simplicial and singular homology, §2.2 computations and
  Mayer–Vietoris, §4.G the nerve theorem. Freely available from the author's page.
- **Munkres, J. R.** *Elements of Algebraic Topology.* Addison-Wesley, 1984. §1–§13 for
  simplicial homology done slowly and concretely; the better book if you intend to *implement*
  rather than to prove.
- **Edelsbrunner, H. and Harer, J.** *Computational Topology: An Introduction.* American
  Mathematical Society, 2010. The standard course text. **Ch. III** (complexes), **Ch. IV**
  (homology), **Ch. V** (duality), **Ch. VII** (persistence) are the load-bearing chapters.
- **Kaczynski, T., Mischaikow, K. and Mrozek, M.** *Computational Homology.* Applied
  Mathematical Sciences 157, Springer, 2004. Algorithmic homology with reduction algorithms
  spelled out — the reference for a from-scratch implementation.
- **Chazal, F., de Silva, V., Glisse, M. and Oudot, S.** *The Structure and Stability of
  Persistence Modules.* SpringerBriefs in Mathematics, 2016. Interleaving, the isometry
  theorem, and stability in their modern form.
- **Oudot, S.** *Persistence Theory: From Quiver Representations to Data Analysis.*
  Mathematical Surveys and Monographs 209, American Mathematical Society, 2015.

### 4.3 Vectorisation, statistics and computation

- **Bubenik, P.** "Statistical Topological Data Analysis using Persistence Landscapes."
  *Journal of Machine Learning Research* **16**, 77–102 (2015).
- **Adams, H. et al.** "Persistence Images: A Stable Vector Representation of Persistent
  Homology." *Journal of Machine Learning Research* **18**(8), 1–35 (2017).
- **Fasy, B. T., Lecci, F., Rinaldo, A., Wasserman, L., Balakrishnan, S. and Singh, A.**
  "Confidence sets for persistence diagrams." *The Annals of Statistics* **42**(6), 2301–2339
  (2014). Use this before calling any bar significant.
- **Mileyko, Y., Mukherjee, S. and Harer, J.** "Probability measures on the space of persistence
  diagrams." *Inverse Problems* **27**(12), 124007 (2011).
- **Turner, K., Mileyko, Y., Mukherjee, S. and Harer, J.** "Fréchet Means for Distributions of
  Persistence Diagrams." *Discrete & Computational Geometry* **52**(1), 44–70 (2014).
  Non-uniqueness of the mean diagram — the reason averaging barcodes is subtle.
- **Otter, N., Porter, M. A., Tillmann, U., Grindrod, P. and Harrington, H. A.** "A roadmap for
  the computation of persistent homology." *EPJ Data Science* **6**:17 (2017). Benchmarks and a
  survey of the software landscape.
- **Bauer, U.** "Ripser: efficient computation of Vietoris–Rips persistence barcodes."
  *Journal of Applied and Computational Topology* **5**, 391–423 (2021).
- **Edelsbrunner, H. and Mücke, E. P.** "Three-dimensional alpha shapes." *ACM Transactions on
  Graphics* **13**(1), 43–72 (1994). Alpha complexes.

### 4.4 Surveys, lecture notes and courseware

- **Chazal, F. and Michel, B.** "An Introduction to Topological Data Analysis: Fundamental and
  Practical Aspects for Data Scientists." *Frontiers in Artificial Intelligence* **4**:667963
  (2021). The best single entry point for a practitioner.
- **Wasserman, L.** "Topological Data Analysis." *Annual Review of Statistics and Its
  Application* **5**, 501–532 (2018). A statistician's appraisal — deliberately sober.
- **GUDHI** (INRIA) and **Ripser** documentation, plus the **`scikit-tda`** ecosystem, for
  reference implementations to check any in-house code against. Note these are *external*
  dependencies; see §6.

### 4.5 Application to markets — and the reasons for caution

- **Gidea, M. and Katz, Y.** "Topological data analysis of financial time series: Landscapes of
  crashes." *Physica A: Statistical Mechanics and its Applications* **491**, 820–834 (2018).
  The canonical financial TDA paper: sliding-window point clouds from multiple indices,
  persistence landscapes, and the observation that landscape norms rise ahead of the 2000 and
  2008 events.
- **Gidea, M., Goldsmith, D., Katz, Y., Roldan, P. and Shmalo, Y.** "Topological recognition of
  critical transitions in time series of cryptocurrencies." *Physica A* **548**, 123843 (2020).
- **Wasserman [4.4]** and **Otter et al. [16]** both note how strongly results depend on
  filtration choice, maximum dimension, normalisation and window length.

**Read the application literature with these four caveats in front of you.** They are not
rhetorical hedges; each is a concrete reason a positive result may not replicate.

1. **Parameter multiplicity.** Window length, delay, embedding dimension, metric, maximum
   homological dimension, landscape level `k` and norm `p` are all analyst-chosen. The
   resulting garden of forking paths is large, and the literature rarely pre-registers.
2. **Sample size at the event level.** However many daily observations there are, the number of
   *crisis episodes* is of order tens. Every claim of the form "the indicator rose before the
   crash" is an `n ≈ 10` claim, and its effective degrees of freedom are governed by episodes,
   not by days. See module **I2**, which is the gate for exactly this failure.
3. **Non-stationarity.** Takens' theorem assumes a fixed compact manifold and a fixed
   diffeomorphism. A regime-shifting market violates the hypothesis outright. Delay embedding
   of a non-stationary series is a heuristic, not a licensed reconstruction.
4. **Absence of a null model.** A rise in a landscape norm means little without a distribution
   under a plausible null (a correlated random walk, a surrogate series with matched
   autocorrelation). Surrogate testing is standard in nonlinear time-series analysis and should
   be standard here.

---

## 5. Derivation for the AMF setting

AMF offers two genuinely different topological objects. The first is small, exact and
immediately computable; the second is the one the source note has in mind and is far more
speculative. Treat them separately.

### 5.1 Object A — the weight filtration of the dependency graph

`DependencyGraph` stores edges keyed `(source, target, kind)` with `weight ∈ (0,1]`. Every
structural query already aggregates across `kind`, capped at `1.0`; write `w(u,v) ∈ [0,1]` for
that aggregate, symmetrised as `w̄(u,v) = max(w(u,v), w(v,u))` since homology of an undirected
complex is what is on offer.

**Definition 5.1 (Coupling dissimilarity).** For systems `u ≠ v` set

```
δ(u, v) = 1 − w̄(u, v)     ∈ [0, 1],     δ(u, u) = 0.
```

Strong coupling ⇒ small dissimilarity. `δ` is symmetric and vanishes on the diagonal but need
**not** satisfy the triangle inequality, so `(SystemKind, δ)` is a *dissimilarity space*, not a
metric space. This is not fatal — the Vietoris–Rips construction only needs a symmetric
function — but it does void any theorem whose hypotheses include metricity, Theorem 2.14
included. State that explicitly wherever the barcode is used.

**Definition 5.2 (Weight filtration).** For `ε ∈ [0,1]` let `G_ε` be the graph on the seven
systems with edges `{u,v}` such that `δ(u,v) ≤ ε`, and let `K_ε = VR_ε` be its flag complex.
`{K_ε}` is a filtration indexed by `ε`, and `K_0 ⊆ … ⊆ K_1` is the full simplex on 7 vertices
whenever every pair is coupled.

Reading off the barcode:

- **`β₀(K_ε)`** is the number of coupling-connected blocks at strength `1 − ε`. Its barcode has
  exactly one infinite bar per component of the fully-coupled graph; the finite `H₀` bars record
  the coupling strengths at which blocks merge. This is single-linkage hierarchical clustering
  of the seven systems by coupling strength — `H₀` persistence and single-linkage dendrograms
  are the same information.
- **`β₁(K_ε)`** counts independent feedback loops *not filled in by triangles*.

### 5.2 Worked example on `examples/sample_market.json`

The sample market couples `circulatory → skeleton` at `0.8` and further edges among the seven
systems. Rather than assert numbers, the procedure to run is:

```
for each unordered pair {u,v} of the 7 SystemKinds:
    w̄ = min(1.0, aggregate weight across all kinds, both directions)
    δ  = 1 − w̄
sort the distinct δ values ascending           →  ε₀ < ε₁ < … < ε_r
for each ε_i:  build G_{ε_i}, take its flag complex, compute β₀, β₁, β₂
report the barcode as the ε-intervals over which each class survives
```

With `n = 7` the whole computation is trivial: at most `2⁷ − 1 = 127` simplices, at most
`21` edges, and the boundary matrices are tiny. The point is not computational — it is that the
barcode is a *complete* summary of how the market's coupling structure fragments as the
coupling threshold rises, and `β₀`'s merge heights are exactly the quantity a maintainer would
otherwise eyeball off the graph.

### 5.3 The relationship to AMF's existing feedback-loop enumeration

`graph.py` enumerates *simple cycles* and `diagnostics.py` sums their edge-weight products into
a `feedback` term. Persistent `H₁` counts something related but strictly different, and
conflating the two would be an error:

**Proposition 5.3.** Let `G` be the fully-coupled graph (`ε = 1`) with `n = 7` vertices, `m`
edges, `c` components. Then `β₁(G) = m − n + c` is the cycle rank, whereas
`β₁(X(G)) = β₁(G) − t`, where `t` is the rank of the subspace of `Z₁` generated by boundaries of
triangles present in `G` — that is, every 3-clique kills one independent cycle. Meanwhile the
number of *simple cycles* enumerated by `graph.py` can be exponential in `n` and is not a rank
at all.

Concretely: a triangle `A→B→C→A` contributes one simple cycle and one unit of cycle rank, but
contributes **zero** to `β₁` of the flag complex, because the 2-simplex `{A,B,C}` fills it.
So `H₁` should be read as *"feedback structure that is not merely local three-way mutual
reliance"* — arguably the more interesting signal for resilience, since a filled triangle is a
densely redundant sub-block rather than a long transmission loop. This is a genuine addition to
what AMF measures today, and it is the strongest argument in this module.

### 5.4 A stability statement AMF does not currently have

Theorem 2.13 applied to the weight filtration yields:

**Corollary 5.4.** Let `M`, `M'` be two markets on the same seven systems whose aggregated
coupling weights differ by at most `η` in the sup norm, i.e. `max_{u,v} |w̄(u,v) − w̄'(u,v)| ≤ η`.
Then their weight-filtration persistence diagrams satisfy `d_B(D, D') ≤ η`.

*Proof sketch.* The filtration values are `δ = 1 − w̄` on edges and `0` on vertices, and the
flag-complex filtration value of a higher simplex is the max over its edges. Perturbing every
edge value by at most `η` perturbs every simplex's filtration value by at most `η`; apply the
sublevel-set stability theorem to the two filtration functions on the fixed simplex on 7
vertices. ∎

This matters for AMF specifically. `CLAUDE.md` demands determinism — equal markets give
bit-identical output — but says nothing about *near*-equal markets. Corollary 5.4 is a
Lipschitz continuity guarantee of exactly the kind the diagnostic index lacks: the barcode
cannot move faster than the weights do. It is worth contrasting with the sensitivity gradients
in `sensitivity.py`, which are finite-difference estimates with no such worst-case bound.

### 5.5 Object B — the stress trajectory

`ShockSimulator.propagate` produces `x_t ∈ [0,1]⁷`, a trajectory of the stress vector. Two
constructions follow:

1. **Trajectory point cloud.** Treat `{x_t}_{t=0..T}` as a point cloud in `[0,1]⁷` under the
   Euclidean or `ℓ∞` metric (this one *is* a metric space, so Theorem 2.14 applies). `H₁`
   detects whether the trajectory is (approximately) closed — a persistent limit cycle in the
   damped dynamics rather than settling. This is a meaningful structural question: the module
   docstrings note that the step map is *not* a contraction for every market, and that a cascade
   trajectory "may settle at a persistent non-zero state". A long `H₁` bar would be evidence of
   an oscillatory rather than monotone attractor.
2. **Sliding-window embedding of a scalar summary.** Apply Perea–Harer sliding-window
   persistence [20] to the scalar series of total system stress `Σ_j x_t[j]`, or to a
   `MetricStats` series from an ensemble run. Roundness of the resulting cloud measures
   periodicity.

Construction 1 is the honest one for AMF: the trajectory is *generated by the model*, so there
is no non-stationarity problem and no unknown attractor — Takens' hypotheses are not being
abused, because we are not reconstructing anything, merely measuring the shape of a known orbit.

**Construction 2 applied to real market data is a different proposition entirely**, and it is
the one the source note's example and its `examples/market_topology_crisis_detection.py`
deliverable describe. That is where every caveat in §4.5 binds, and where the repository's
rules bind too (§6).

### 5.6 Determinism: the filtration tie-break

Persistence pairing depends on a total order on simplices refining the filtration. AMF's sample
markets are full of ties — `musculature` and `metabolism` share a criticality of `0.60`, and
repeated dependency weights are routine — so distinct simplices will share a filtration value
constantly. **A tie broken by dict insertion order is a determinism bug**, precisely the class
of bug `CLAUDE.md` documents for the diagnostic HHI and the SPOF ranking.

The compliant rule: break ties by `(dimension, tuple of SystemKind declaration-order indices)`,
lexicographically. This is canonical, depends on no runtime state, and makes the barcode
invariant under permutation of assembly order — which is exactly the property
`tests/unit/test_properties.py` already asserts for diagnosis.

Note further that while the *diagram* is independent of the tie-break, the *pairing* of
individual simplices is not; anything that reports representative cycles must fix the order or
its output will not be reproducible.

---

## 6. Repository governance and boundary analysis

| Proposed artefact | Conflict | Compliant reformulation |
|---|---|---|
| `src/amf/tda/persistent_homology.py` | **None on naming.** Genuine risk on **zero runtime dependencies** if it wraps GUDHI/Ripser/`scikit-tda` | Implement `𝔽₂` boundary-matrix reduction in pure Python. On 7 systems the complex has `≤ 127` simplices — this is tens of lines of stdlib code and is exactly testable to 100% branch coverage. Validate once, offline, against GUDHI; do not import it |
| `src/amf/tda/betti_numbers.py` | **None on naming.** `β₀`/`β₁` are structural quantities | Ship as `betti_numbers()` returning a frozen, slotted result type with `to_dict()`; add to `amf.__all__` |
| Any public member named `*_order` (e.g. `filtration_order`, `simplex_order`) | **Non-trading boundary.** `order` is on the mechanically enforced `FORBIDDEN` substring list; `CouplingMatrix.order` is the single documented `ALLOWLIST` exception | Name it `filtration_sequence`, `simplex_ranking` or `traversal`. Do **not** extend the allowlist — the meta-test that keeps the allowlist honest is there to stop exactly this drift |
| `examples/market_topology_crisis_detection.py` — "Test on historical data" | **Non-trading boundary** (`price` in any public name), and **illustrative, not validated** — "crisis detection" on historical market data claims predictive power | Rename to a structural retrodiction example: replay historical *structural configurations* of the seven systems and report how `β₀`/`β₁` of the weight filtration change. Emit the `_DISCLAIMER`. Add the case to `tests/integration/test_examples.py` |
| `docs/research/topological_data_analysis.md` | None | This module supersedes it; the file may simply link here |
| Persistence over real multi-asset point clouds | Zero-dependency rule (`n = 10⁴` is not a stdlib workload); "illustrative, not validated" | Out-of-tree research sidecar with its own dependencies and its own disclaimers. The `amf` package stays standard-library only |

**Determinism.** See §5.6 — the tie-break rule is mandatory, not optional. A property test
should assert that a market and every permutation of its assembly order yield an identical
barcode, mirroring the existing permutation test for diagnosis.

**Numerical care.** `δ = 1 − w̄` on floats introduces representation error; two weights that are
equal as inputs must remain equal as filtration values. Compare filtration values exactly (they
are derived by a single subtraction from the stored weights) rather than with a tolerance, or
the tie-break becomes input-order dependent again.

**Validation-claim discipline.** Every statement in an implementation docstring must say what
the barcode *is* (a summary of coupling structure), never what it *predicts*. "Betti number
jumps → crisis signal", the source note's phrasing, is precisely the formulation the repository
forbids; §7 restates it as a refutable hypothesis instead.

**Layering.** TDA over the dependency graph belongs beside `graph.py` in the dependency order
(`errors`/`models` ← `systems`/`graph` ← `market` ← `diagnostics`/`simulation`). It must not
import `report`, `viz` or `cli`. If it consumes `SimulationTrace` (Object B, §5.5) it sits at
the `simulation` layer instead. Pick one and document it; do not let it straddle both.

---

## 7. Falsifiable propositions and open questions

The source note's claims, restated so they can fail.

**P1 (Non-triviality).** Across a corpus of assembled AMF markets, the flag complex of the
weight filtration has `β₁ > 0` for a non-negligible fraction at some `ε`.
*Refuted if*: `β₁ ≡ 0` almost everywhere, i.e. every feedback loop in practice is triangulated.
Then `H₁` adds nothing to `graph.py`'s cycle enumeration and Object A reduces to `H₀`
(= single-linkage clustering), which is worth knowing and worth saying.

**P2 (Independence from existing diagnostics).** The barcode carries information not already in
`DiagnosticReport`. *Refuted if*: barcode summaries (landscape norms, total persistence) are
near-perfectly predictable from the existing `fragility`, `concentration` and `feedback` scores
across a large sample of synthetic markets — regress one on the other and look at the residual.

**P3 (Stability is tight).** Corollary 5.4's bound `d_B ≤ η` is attained. *Refuted if*: no
market perturbation achieves it, in which case a sharper AMF-specific constant exists.

**P4 (Trajectory topology distinguishes dynamical regimes).** Under `cascade_threshold`, the
`H₁` of the stress trajectory point cloud (§5.5, Object B) distinguishes markets that settle
from those that reach a persistent non-zero state. *Refuted if*: trajectories in both regimes
have indistinguishable `H₁` barcodes under a surrogate-calibrated null.

**P5 (The source note's crisis claim).** On real market data, a jump in Betti numbers precedes
systemic stress episodes more often than a matched surrogate null predicts.
*Refuted if*: with pre-registered parameters, blocked/purged cross-validation (module **I2**),
and surrogate series matched on autocorrelation and heavy tails, the excess hit rate is not
distinguishable from zero. **This proposition sits outside the `amf` package boundary by
construction** — it concerns market data, which the package does not model. It belongs to the
research sidecar, and this repository takes no position on its truth.

**Open questions.**

1. Is there a *directed* persistence theory appropriate to AMF's directed dependencies? Ordinary
   homology symmetrises and throws away direction, which for a stress-transmission graph is a
   real loss. Directed clique complexes and path homology are candidate answers; assess whether
   their theory is mature enough to rely on.
2. Should the filtration run on `δ = 1 − w̄` (coupling strength) or on a stress-weighted
   dissimilarity that also involves `absorptive_capacity`? The second is more faithful to the
   simulation's `W[i][j]·(1 − a_j)` term and would produce a barcode of the *effective*
   transmission structure rather than the nominal one.
3. With `n = 7`, is the asymptotic statistical machinery (§2.5, §4.3) applicable at all, or
   should inference be exact and combinatorial — enumerate all permutations, compute an exact
   null?
4. Does the `H₀` barcode reproduce, or contradict, the articulation points already reported as
   single points of failure? A vertex whose removal raises `β₀` is a cut vertex; the two notions
   should agree, and if they do not, one implementation is wrong.

---

## 8. Deliverables

Reproduced from the source note, with a compliance column:

| Deliverable (verbatim) | Status | Compliance note |
|---|---|---|
| `docs/research/topological_data_analysis.md` — TDA theory | Superseded by this module | No conflict |
| `src/amf/tda/persistent_homology.py` — Persistence computation | Proposed, feasible | Pure-stdlib `𝔽₂` reduction only; no GUDHI/Ripser import; canonical tie-break (§5.6); avoid any public name containing `order` |
| `src/amf/tda/betti_numbers.py` — Topological metrics | Proposed, feasible | Frozen slotted result type with `to_dict()`; export from `amf.__all__`; extend `report._to_jsonable` if serialised |
| `examples/market_topology_crisis_detection.py` — Test on historical data | **Blocked as specified** | Violates the non-trading boundary and the illustrative-not-validated rule. Reformulate as structural retrodiction over AMF market configurations (§6), or move to the sidecar |

**Research Leaders Needed**: Topologist, computational geometry specialist

---

## 9. Research leadership and prerequisites

**Skills matrix.**

| Role | Must have | Should have | Will own |
|---|---|---|---|
| Topologist | Simplicial and singular homology; persistence modules and the structure theorem | Interleaving/isometry theorem; quiver representations | Correctness of §2 and §5.3; the directed-persistence question |
| Computational geometry specialist | Boundary-matrix reduction; complex construction; complexity analysis | Ripser/GUDHI internals for cross-validation | The stdlib implementation, the tie-break, and 100% branch coverage |
| Statistician | Multiple testing; bootstrap; surrogate data methods | Statistical TDA (Fasy et al.) | P2, P4, P5 inference design — jointly with module **I2** |
| AMF maintainer | The seven systems, `DependencyGraph`, `CouplingMatrix`, the hard rules | The determinism history in `CLAUDE.md` | §6 boundary decisions; layering |

**Prerequisite ladder.**

```
Linear algebra over a field  ──►  Point-set topology  ──►  Simplicial homology (Hatcher Ch.2)
                                                                    │
                                                                    ▼
                              Filtrations & the reduction algorithm (Edelsbrunner–Harer VII)
                                                                    │
                            ┌───────────────────────────────────────┼──────────────────────┐
                            ▼                                       ▼                      ▼
              Stability & interleaving [5,13]        Vectorisation [11,12]      Takens & sliding
                                                                                 windows [19,20]
                            │                                       │                      │
                            └───────────────────────────────────────┴──────────────────────┘
                                                    │
                                                    ▼
                                    Statistical inference on diagrams [18]
                                                    │
                                                    ▼
                                        Module I2 (validation) — the gate
```

Nothing in P5 should be attempted before module **I2** is agreed. That ordering is the whole
point of the prerequisite map in `docs/discussions/README.md`.

---

## References

[1] Edelsbrunner, H., Letscher, D. and Zomorodian, A. "Topological Persistence and
Simplification." *Discrete & Computational Geometry* **28**(4), 511–533 (2002).

[2] Zomorodian, A. and Carlsson, G. "Computing Persistent Homology." *Discrete & Computational
Geometry* **33**(2), 249–274 (2005).

[3] Carlsson, G. "Topology and Data." *Bulletin of the American Mathematical Society* **46**(2),
255–308 (2009).

[4] Ghrist, R. "Barcodes: The Persistent Topology of Data." *Bulletin of the American
Mathematical Society* **45**(1), 61–75 (2008).

[5] Cohen-Steiner, D., Edelsbrunner, H. and Harer, J. "Stability of Persistence Diagrams."
*Discrete & Computational Geometry* **37**(1), 103–120 (2007).

[6] Edelsbrunner, H. and Harer, J. *Computational Topology: An Introduction.* American
Mathematical Society, Providence, 2010.

[7] Kaczynski, T., Mischaikow, K. and Mrozek, M. *Computational Homology.* Applied Mathematical
Sciences 157, Springer, New York, 2004.

[8] Chazal, F. and Michel, B. "An Introduction to Topological Data Analysis: Fundamental and
Practical Aspects for Data Scientists." *Frontiers in Artificial Intelligence* **4**:667963
(2021).

[9] Munkres, J. R. *Elements of Algebraic Topology.* Addison-Wesley, Menlo Park, 1984.

[10] Hatcher, A. *Algebraic Topology.* Cambridge University Press, Cambridge, 2002.

[11] Bubenik, P. "Statistical Topological Data Analysis using Persistence Landscapes."
*Journal of Machine Learning Research* **16**, 77–102 (2015).

[12] Adams, H. et al. "Persistence Images: A Stable Vector Representation of Persistent
Homology." *Journal of Machine Learning Research* **18**(8), 1–35 (2017).

[13] Chazal, F., de Silva, V., Glisse, M. and Oudot, S. *The Structure and Stability of
Persistence Modules.* SpringerBriefs in Mathematics, Springer, 2016.

[14] Crawley-Boevey, W. "Decomposition of pointwise finite-dimensional persistence modules."
*Journal of Algebra and its Applications* **14**(5), 1550066 (2015).

[15] Turner, K., Mileyko, Y., Mukherjee, S. and Harer, J. "Fréchet Means for Distributions of
Persistence Diagrams." *Discrete & Computational Geometry* **52**(1), 44–70 (2014).

[16] Otter, N., Porter, M. A., Tillmann, U., Grindrod, P. and Harrington, H. A. "A roadmap for
the computation of persistent homology." *EPJ Data Science* **6**:17 (2017).

[17] Bauer, U. "Ripser: efficient computation of Vietoris–Rips persistence barcodes."
*Journal of Applied and Computational Topology* **5**, 391–423 (2021).

[18] Fasy, B. T., Lecci, F., Rinaldo, A., Wasserman, L., Balakrishnan, S. and Singh, A.
"Confidence sets for persistence diagrams." *The Annals of Statistics* **42**(6), 2301–2339
(2014).

[19] Takens, F. "Detecting strange attractors in turbulence." In *Dynamical Systems and
Turbulence, Warwick 1980*, Lecture Notes in Mathematics **898**, Springer, Berlin, 366–381
(1981).

[20] Perea, J. A. and Harer, J. "Sliding Windows and Persistence: An Application of Topological
Methods to Signal Analysis." *Foundations of Computational Mathematics* **15**(3), 799–838
(2015).

[21] Gidea, M. and Katz, Y. "Topological data analysis of financial time series: Landscapes of
crashes." *Physica A: Statistical Mechanics and its Applications* **491**, 820–834 (2018).

[22] Gidea, M., Goldsmith, D., Katz, Y., Roldan, P. and Shmalo, Y. "Topological recognition of
critical transitions in time series of cryptocurrencies." *Physica A: Statistical Mechanics and
its Applications* **548**, 123843 (2020).

[23] Singh, G., Mémoli, F. and Carlsson, G. "Topological Methods for the Analysis of High
Dimensional Data Sets and 3D Object Recognition." *Eurographics Symposium on Point-Based
Graphics*, 91–100 (2007).

[24] Wasserman, L. "Topological Data Analysis." *Annual Review of Statistics and Its
Application* **5**, 501–532 (2018).

[25] Edelsbrunner, H. and Mücke, E. P. "Three-dimensional alpha shapes." *ACM Transactions on
Graphics* **13**(1), 43–72 (1994).

[26] Oudot, S. *Persistence Theory: From Quiver Representations to Data Analysis.* Mathematical
Surveys and Monographs 209, American Mathematical Society, Providence, 2015.

[27] Mileyko, Y., Mukherjee, S. and Harer, J. "Probability measures on the space of persistence
diagrams." *Inverse Problems* **27**(12), 124007 (2011).
