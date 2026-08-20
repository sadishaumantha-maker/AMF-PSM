# D1: Deep Learning Architectures for Multi-Asset Forecasting

> **Discussion category**: Research · **Labels**: `theory`, `deep-learning`, `graph-neural-networks`, `boundary-review`, `not-validated`, `needs-reformulation`
> **Source**: `docs/QUANTUM_NEURAL_RESEARCH.md` § Discussion D1
> **Status**: Open for comment · **Nature**: Theoretical module, illustrative and not
> empirically validated

## 0. Abstract and reading guide

This module asks what deep learning would contribute to AMF, and answers with one identity
and one accounting. The identity (Theorem 5.3) is that `ShockSimulator._advance` is *exactly*
a message-passing neural-network layer in the sense of Gilmer et al. [57]: node states are
scalars, messages are `x_i · W[i][j]`, aggregation is summation, the update is affine, and
the activation is a hardtanh on `[0, 1]`. Unrolled over `max_steps`, the simulator is a
weight-tied graph network of depth 50 with **zero learnable parameters**; the opt-in cascade
dynamics is the same layer with hard multiplicative gates, the non-differentiable limit of
GRU gating [33]. The accounting is that a market carries at most 196 real numbers, a minimal
two-layer graph convolution carries 1 249 parameters, AMF possesses no labelled corpus of
markets at all, and its diagnostic index is already available in closed form — so there is
nothing here for supervised learning to fit and nothing for it to improve on.

It does **not** claim that deep networks are useless for markets, that AMF should acquire
them, or that any construction here forecasts anything. Nothing below is financial advice,
a diagnosis, or a forecast.

**Prerequisite ladder.** Linear algebra and multivariable calculus → empirical risk
minimisation and the bias–variance decomposition ([110] Ch. 2, 7) → feedforward networks,
backpropagation, and stochastic optimisation ([104] Ch. 6, 8) → recurrence, BPTT, and gating
([104] Ch. 10; [30]) → attention and the transformer ([38]) → spectral graph theory and graph
convolution ([118]; [53], [54]) → message passing and Weisfeiler–Leman expressivity ([57],
[58]) → proper scoring rules ([87]). Section 5 assumes the whole ladder; Sections 6–9 assume
none of it.

## 1. Verbatim source specification

The following is reproduced word for word from `docs/QUANTUM_NEURAL_RESEARCH.md`, including
its notation, typography, code fences, and deliverable paths. It is quoted, not endorsed.
(One byte-level caveat is recorded in §6.5: the repository's `trailing-whitespace`
pre-commit hook strips trailing spaces from files under `docs/`, so the excerpt below is
word-exact but not necessarily whitespace-exact once committed.)

````markdown
### Discussion D1: Deep Learning Architectures for Multi-Asset Forecasting
**Theme**: Transformer networks, LSTMs, and graph neural networks for coupled market dynamics

**Architectural Options**:

1. **Transformer Networks (Attention Mechanism)**
   - Original use: NLP (language understanding)
   - Financial adaptation: Self-attention to identify which past prices matter most
   ```
   Architecture:
     Input: [price_t-n, ..., price_t, volume_t, sentiment_t, policy_t]
     Attention: Q,K,V matrices learn which features interact
     Output: Price forecast + uncertainty band
   
   Advantage: Parallel processing (fast), captures long-range dependencies
   Disadvantage: Black-box; hard to interpret "why"
   ```

2. **LSTM (Long Short-Term Memory)**
   - Designed to handle temporal dependencies
   - Gate mechanism: forget/remember past information
   ```
   Architecture:
     Input: Time-series [market state at t-n, ..., t]
     Cell state: "Memory" of past events (e.g., "we're in crisis")
     Hidden state: Transient info (e.g., "next tick likely up")
     Output: Multi-step forecast
   
   Advantage: Interpretable gates (can see what model remembers)
   Disadvantage: Sequential processing (slower)
   ```

3. **Graph Neural Networks (GNN)**
   - Model relationships between assets as graph edges
   - Nodes: Assets (stocks, bonds, forex, commodities)
   - Edges: Correlations, causality, shock transmission
   ```
   Architecture:
     Nodes: {Equity, Credit, Forex, Commodity, Policy}
     Edge features: [correlation, lag-lead relationship, shock direction]
     Graph convolution: Propagates information along edges
     Output: System-wide risk score + which node is vulnerable
   
   Advantage: Native model of systemic risk (contagion through graph)
   Disadvantage: Graph structure must be pre-specified (or learned)
   ```

**Key Innovation: Hybrid Architecture**
```
Transformer layer 1: Process market data (prices, volumes, spreads)
                     → Output: Feature embeddings per asset
                     
GNN layer: Connect assets via correlation graph
           → Output: Propagated risk signals across system
           
LSTM layer: Temporal forecasting with GNN features
            → Output: Multi-asset predictions + confidence
            
Attention mechanism: Which assets/policies matter most?
                     → Interpretability: Feature importance
```

**Training Strategy**:
- Supervised: Predict next-period returns (minimize MSE/MAE)
- Unsupervised: Anomaly detection (identify unusual market states)
- Semi-supervised: Pre-train on market microstructure; fine-tune on crises
- Reinforcement learning: Learn optimal policy responses to shocks

**Deliverable**:
- `docs/research/deep_learning_market_architectures.md` — Architecture comparison
- `src/amf/ml/transformer_market_model.py` — Transformer implementation
- `src/amf/ml/graph_neural_network.py` — GNN for systemic risk
- `src/amf/ml/hybrid_lstm_gnn.py` — Combined architecture
- `examples/ml_crisis_forecasting.py` — Test on historical data

**Research Leaders Needed**: Machine learning engineer, financial ML specialist
````

## 2. Formal foundations

Throughout, `sigma` denotes a scalar activation applied elementwise, `K` a compact subset of
`R^d`, and `||.||` the Euclidean norm unless subscripted. All theorems are stated with their
hypotheses; the hypotheses are the part that the source note omits and the part that decides
whether any of this transfers to AMF.

### 2.1 Approximation: what a network *can* represent

**Definition 2.1 (feedforward network).** A depth-`L` network with widths `d_0, ..., d_L` is
`f(x) = A_L o sigma o A_{L-1} o ... o sigma o A_1 (x)` with affine `A_l(z) = M_l z + b_l`,
`M_l in R^{d_l x d_{l-1}}`. Its parameter count is `sum_l (d_l d_{l-1} + d_l)`.

**Theorem 2.2 (universal approximation; Cybenko [1], Hornik–Stinchcombe–White [2]).** Let
`sigma` be continuous, bounded and non-constant (Cybenko: continuous sigmoidal). Then for
every `f in C(K)` and `eps > 0` there are `n`, `c_k`, `w_k`, `b_k` with
`sup_{x in K} |f(x) - sum_{k=1..n} c_k sigma(w_k . x + b_k)| < eps`.

**Theorem 2.3 (sharp condition; Leshno–Lin–Pinkus–Schocken [4]).** A single hidden layer with
activation `sigma` (locally bounded, piecewise continuous) is dense in `C(K)` **if and only
if** `sigma` is not a polynomial. This is the correct statement to quote: it makes clear that
universality is a property of *non-polynomiality*, not of depth, biology, or "learning".

**Theorem 2.4 (Barron rate [5]).** Let `f: R^d -> R` have Fourier representation with
`C_f = integral ||w|| |F(dw)| < infinity`. Then for every `n` there is a single-hidden-layer
sigmoidal network `f_n` with `n` units and `integral_K (f - f_n)^2 mu(dx) <= (2 r C_f)^2 / n`,
where `K` is a ball of radius `r`. The rate `O(1/n)` is *dimension-free* in `n`; the
dimension re-enters through `C_f`.

**Theorem 2.5 (depth separation; Eldan–Shamir [6]).** There is a universal constant `c` such
that for every `d` there exists a function `g: R^d -> R`, supported on a ball, expressible to
accuracy `eps` by a 3-layer network of width `poly(d, 1/eps)`, for which every 2-layer
network approximating `g` to constant `L^2(mu)` accuracy must have width at least
`c e^{cd}`.

**Theorem 2.6 (depth separation for ReLU; Telgarsky [7]).** For every `k` there is a function
on `[0,1]` computable exactly by a ReLU network with `Theta(k^3)` layers and constant width,
such that any ReLU network of depth `O(k)` approximating it to constant `L^1` accuracy needs
`2^{Omega(k)}` units.

*Reading for AMF.* Theorems 2.2–2.6 concern *existence of a representation*, never
*recoverability from data*. Every one of them is compatible with the situation in which AMF
actually finds itself: the target function is known exactly and the data set is empty.

### 2.2 Learnability: what it can be *trained* to represent

**Theorem 2.7 (Blum–Rivest [8]).** Deciding whether a 3-node threshold network exactly fits a
given labelled sample is NP-complete. Representability does not imply tractable fitting.

**Empirical result 2.8 (Zhang et al. [9]).** Standard convolutional architectures trained with
standard optimisers can fit uniformly random labels on standard image corpora to zero training
error. Consequently, no capacity measure that depends only on the architecture can explain
their generalisation, and "the model fits the data" carries no evidential weight on its own.

**Empirical result 2.9 (double descent; Belkin et al. [10]).** Test risk as a function of
model capacity is not U-shaped: past the interpolation threshold it can descend again. The
classical bias–variance picture ([110] Ch. 7) is a special case, not a law. (Note for §6: the
word "tradeoff" contains the `FORBIDDEN` substring `trade`, so this concept cannot be named in
a public identifier inside `src/amf`.)

### 2.3 Optimisation and its convergence caveats

**Definition 2.10 (SGD).** For `F(theta) = E_z[l(theta; z)]`, iterate
`theta_{t+1} = theta_t - eta_t g_t` with `E[g_t | theta_t] = grad F(theta_t)`.

**Theorem 2.11 (Robbins–Monro [11]).** If `sum_t eta_t = infinity`, `sum_t eta_t^2 <
infinity`, and the noise has bounded second moment, the iterates converge (a.s., under
regularity) to a root of the gradient. For non-convex `F` this is a statement about
stationary points only.

**Definition 2.12 (momentum, Nesterov acceleration).** Heavy ball [12]:
`v_{t+1} = beta v_t - eta g_t`, `theta_{t+1} = theta_t + v_{t+1}`. Nesterov [13] evaluates the
gradient at the extrapolated point and achieves `O(1/t^2)` on smooth convex objectives, versus
`O(1/t)` for plain gradient descent.

**Definition 2.13 (Adam [16]).** `m_t = beta_1 m_{t-1} + (1-beta_1) g_t`,
`v_t = beta_2 v_{t-1} + (1-beta_2) g_t^2`, bias-corrected, then
`theta_{t+1} = theta_t - eta m_hat_t / (sqrt(v_hat_t) + epsilon)`.

**Theorem 2.14 (Adam does not always converge; Reddi–Kale–Kumar [17]).** There is a convex
online problem on which Adam has non-vanishing average regret; the convergence proof in [16]
contains an error in the treatment of the effective step size. AMSGrad repairs it by enforcing
monotone `v_hat`. The practical lesson is that the default optimiser of the source note's
implicit plan is one whose published guarantee was wrong.

**Remark 2.15 (weight decay).** `L2` penalty and decoupled weight decay coincide for plain SGD
and *differ* for adaptive methods; AdamW [18] decouples them. See [19] for the full
large-scale optimisation survey.

### 2.4 Regularisation, normalisation, residual connections

**Definition 2.16 (dropout [20]).** During training multiply each unit by an independent
Bernoulli(`p`) mask; at test time scale by `p`. This makes the *training* map stochastic — a
determinism hazard flagged in §5.16.

**Definition 2.17 (batch normalisation [21]).** `BN(x) = gamma (x - mu_B)/sqrt(s_B^2 + eps) +
beta`, with `mu_B, s_B` the minibatch statistics. Batch statistics make the output of one
example depend on the other examples in its batch.

**Definition 2.18 (layer normalisation [22]).** Same form with `mu, s` computed across the
*feature* axis of a single example. Batch-independent, hence the normalisation used in
transformers.

**Result 2.19 (mechanism; Santurkar et al. [24]).** The "internal covariate shift"
explanation offered in [21] is not the operative mechanism; batch normalisation instead
improves the Lipschitz constants of the loss and its gradient. Cited here because the source
note's style of mechanism-by-analogy is exactly the failure mode [24] corrected.

**Definition 2.20 (residual block [23]).** `h_{l+1} = h_l + F(h_l)`. The identity path keeps
the layer-to-layer Jacobian near `I`, which is why very deep stacks train at all.

**Result 2.21 (Pre-LN vs Post-LN; Xiong et al. [25]).** Placing layer normalisation inside the
residual branch (Pre-LN) bounds the gradient at initialisation and removes the need for
learning-rate warm-up that Post-LN transformers require.

### 2.5 Recurrence, BPTT, and gating

**Definition 2.22 (simple RNN [26]).** `h_t = sigma(U x_t + V h_{t-1} + b)`.

**Definition 2.23 (BPTT [27]).** Unroll to depth `T` and apply the chain rule; the Jacobian
across `k` steps is `prod_{s} diag(sigma')V`.

**Theorem 2.24 (vanishing / exploding gradients; Bengio–Simard–Frasconi [29]; Hochreiter
[28]).** Let `lambda_1` be the spectral radius of `V` and `sigma` have `|sigma'| <= gamma`.
If `gamma lambda_1 < 1` the `k`-step Jacobian norm decays exponentially in `k` (gradients
vanish; long-range credit assignment fails). If the smallest singular value times `gamma`
exceeds `1`, norms grow exponentially. Latching information robustly over long horizons and
having non-vanishing gradients are, for a plain RNN, incompatible.

**Definition 2.25 (LSTM [30], with forget gate [31]).**
```
f_t = sigmoid(W_f [h_{t-1}, x_t] + b_f)        # forget
i_t = sigmoid(W_i [h_{t-1}, x_t] + b_i)        # input
o_t = sigmoid(W_o [h_{t-1}, x_t] + b_o)        # output
c~_t = tanh(W_c [h_{t-1}, x_t] + b_c)
c_t = f_t (*) c_{t-1} + i_t (*) c~_t           # constant-error carousel
h_t = o_t (*) tanh(c_t)
```
`(*)` is the Hadamard product. The cell recurrence `c_t = f_t (*) c_{t-1} + ...` has Jacobian
`diag(f_t)`; with `f_t ~ 1` the multiplicative decay of Theorem 2.24 is switched off. That is
the entire mechanism.

**Definition 2.26 (GRU [33]).** `z_t` (update) and `r_t` (reset) gates,
`h_t = (1 - z_t) (*) h_{t-1} + z_t (*) tanh(W [r_t (*) h_{t-1}, x_t])`. No separate cell state.

**Empirical result 2.27 ([34], [35]).** GRU and LSTM are statistically indistinguishable across
a broad sweep; the forget gate and the output activation are the components whose removal
hurts most, and the learning rate dominates every architectural hyper-parameter in an
fANOVA decomposition [35].

### 2.6 Attention and the transformer

**Definition 2.28 (additive attention [36]).** `e_{ij} = v^T tanh(W_1 s_i + W_2 h_j)`,
`alpha_{ij} = softmax_j(e_{ij})`, context `c_i = sum_j alpha_{ij} h_j`. Multiplicative
variants in [37].

**Definition 2.29 (scaled dot-product self-attention [38]).** For `X in R^{n x d}`,
```
Q = X W_Q,  K = X W_K,  V = X W_V,   W_Q, W_K in R^{d x d_k}, W_V in R^{d x d_v}
A = softmax_row( Q K^T / sqrt(d_k) ) in R^{n x n},   Attn(X) = A V
```
The `1/sqrt(d_k)` scaling keeps the logits' variance `O(1)` when the entries of `Q, K` are
`O(1)` and independent, preventing softmax saturation.

**Property 2.30 (row-stochasticity).** Every row of `A` is a probability vector with **full
support**: `A_{ij} > 0` for all `i, j`, because `exp` is strictly positive. Softmax attention
therefore cannot represent an exactly absent coupling. This single fact does most of the work
in §5.7.

**Definition 2.31 (multi-head attention).** `MHA(X) = Concat(head_1, ..., head_h) W_O` with
`head_r = Attn_r(X)` on `d_k = d_v = d/h`. Heads are a partition of the same budget, not extra
capacity.

**Definition 2.32 (permutation equivariance and positional encoding).** `Attn(P X) = P
Attn(X)` for any permutation matrix `P`: self-attention is *set*-valued and knows nothing of
order. Sequence structure is injected by adding sinusoidal or learned position vectors [38],
by relative-position biases [39], or by rotating `Q, K` in fixed 2-planes (RoPE [40]).

**Definition 2.33 (transformer block).** Pre-LN form:
`X <- X + MHA(LN(X))`; `X <- X + FFN(LN(X))` with `FFN(z) = W_2 phi(W_1 z + b_1) + b_2`,
`W_1 in R^{d x d_ff}`, conventionally `d_ff = 4d`. The encoder stacks `N` such blocks; the
decoder adds causal masking and cross-attention to the encoder output.

### 2.7 Complexity, and why efficient attention exists

**Proposition 2.34 (cost of one attention layer).** Computing `Q, K, V` and the output
projection costs `4 n d^2` multiply-accumulates; forming `Q K^T`, the softmax, and `A V`
costs `2 n^2 d_k h + O(n^2 h) = O(n^2 d)`. Memory for `A` is `O(h n^2)`. Total
`O(n^2 d + n d^2)`.

**Corollary 2.35.** The quadratic term dominates only when `n >> d`. The efficient-attention
programme — sparse patterns [42], low-rank projection of `K, V` [44], kernel feature maps
[43], random features [45]; survey [46] — targets exactly the regime `n >> d`. Applying it
when `n << d` optimises the smaller term. See §5.9, where AMF has `n = 7`.

### 2.8 Graph neural networks: the spectral origin

**Definition 2.36 (graph Laplacian).** For a weighted undirected graph with adjacency `A` and
degree `D`, `L = D - A` and `L_sym = I - D^{-1/2} A D^{-1/2}`, symmetric positive
semi-definite with spectrum in `[0, 2]`; eigenvalue `0` has multiplicity equal to the number
of connected components ([118] Ch. 1).

**Definition 2.37 (spectral convolution [50]).** With `L_sym = U Lambda U^T`, a filter
`g_theta` acts as `g_theta * x = U g_theta(Lambda) U^T x`. Cost `O(n^2)` per application after
an `O(n^3)` eigendecomposition, and the filter is basis-dependent, hence not transferable
between graphs.

**Definition 2.38 (ChebNet [53]).** Approximate `g_theta(Lambda) ~ sum_{k=0..K} theta_k
T_k(Lambda_tilde)`, `T_k` Chebyshev polynomials, `Lambda_tilde = 2 Lambda / lambda_max - I`.
Because `T_k(L_tilde)` is a degree-`k` polynomial in `L`, the filter is *exactly* `K`-localised
and costs `O(K |E|)`. This is the step that converts spectral graph theory into a practical
layer; the wavelet construction of [51] and the graph-processing survey [52] are its
antecedents.

**Definition 2.39 (GCN [54]).** Take `K = 1`, `lambda_max ~ 2`, tie `theta_0 = -theta_1`, and
renormalise `A_hat = D_t^{-1/2}(A + I) D_t^{-1/2}` with `D_t = D + I`. One layer is
`H^{(l+1)} = sigma(A_hat H^{(l)} Theta^{(l)})`.

**Proposition 2.40 (spectrum of the renormalised operator).** `A_hat` is symmetric with
eigenvalues in `(-1, 1]`, and `lambda_1 = 1` with eigenvector `D_t^{1/2} 1`. The self-loop
renormalisation shrinks the spectral radius relative to `D^{-1/2} A D^{-1/2}`; this is the
stated purpose in [54].

**Definition 2.41 (GraphSAGE [55]).** `h_j^{(l+1)} = sigma(W^{(l)} [h_j^{(l)} ,
AGG({h_i^{(l)} : i in N(j)})])` with `AGG` mean, LSTM-over-a-random-permutation, or max-pool,
plus neighbourhood sampling. Inductive: applies to unseen nodes.

**Definition 2.42 (GAT [56]).** `alpha_{ji} = softmax_{i in N(j)}(LeakyReLU(a^T [W h_j, W
h_i]))`, `h_j' = sigma(sum_{i in N(j)} alpha_{ji} W h_i)`. Attention *masked to the graph*,
so unlike Property 2.30 a non-edge stays exactly zero.

### 2.9 Message passing and expressivity

**Definition 2.43 (MPNN [57]).**
```
m_j^{(t+1)} = sum_{i in N(j)} M_t( h_i^{(t)}, h_j^{(t)}, e_{ij} )
h_j^{(t+1)} = U_t( h_j^{(t)}, m_j^{(t+1)} )
y          = R( { h_j^{(T)} : j in V } )
```
GCN, GraphSAGE, GAT and ChebNet are all instances.

**Definition 2.44 (1-WL colour refinement [47]).** `c^{(0)}(v) = ` initial label;
`c^{(t+1)}(v) = HASH( c^{(t)}(v), {{ c^{(t)}(u) : u in N(v) }} )` with `{{.}}` a multiset.
Iterate to stability.

**Theorem 2.45 (expressive ceiling; Xu et al. [58]; Morris et al. [59]).** Any MPNN of the
form 2.43 with `T` rounds refines node labels no more finely than `T` rounds of 1-WL. There
exist non-isomorphic graphs no MPNN can distinguish. Conversely, if `M_t`, `U_t` and `R` are
injective on multisets — as in GIN, `h_j^{(t+1)} = MLP((1 + eps) h_j^{(t)} + sum_{i in N(j)}
h_i^{(t)})` — the MPNN attains the 1-WL bound exactly.

**Corollary 2.46.** Mean and max aggregation are strictly weaker than sum: mean loses multiset
multiplicity, max loses everything but the support.

### 2.10 Over-smoothing and over-squashing

**Theorem 2.47 (over-smoothing; Li–Han–Wu [60]; Oono–Suzuki [61]).** Repeated application of
`A_hat` is a Laplacian smoothing operator. Writing `1 = |lambda_1| > |lambda_2| >= ...` for its
spectrum, the component of `H^{(0)}` orthogonal to the dominant eigenvector contracts by at
least `|lambda_2|` per layer, so after `L` layers node representations lie within
`O(|lambda_2|^L)` of a subspace of dimension equal to the number of connected components. With
ReLU and bounded weight norms, [61] shows the distance to that invariant subspace decays
exponentially in depth.

**Definition 2.48 (over-squashing; Alon–Yahav [62]).** For a node to use information `r` hops
away an MPNN needs `L >= r` layers, but the number of nodes in the receptive field grows
exponentially in `r` while the representation width stays fixed; long-range information is
compressed into a bottleneck. [63] localises the bottleneck in edges of negative discrete
Ricci curvature and rewires accordingly.

**Remedy 2.49 (initial residual and identity mapping; GCNII [64]).**
`H^{(l+1)} = sigma( ((1-a) A_hat H^{(l)} + a H^{(0)}) ((1-b_l) I + b_l W^{(l)}) )`. The
`a H^{(0)}` term is exactly a *retention* of the input state at every layer.

### 2.11 Geometric deep learning as the unifying frame

**Principle 2.50 (Bronstein et al. [65], [66]).** An architecture is specified by a domain
`Omega`, a symmetry group `G` acting on it, and the requirement that layers be `G`-equivariant
and that pooling be `G`-invariant. Convolution is translation equivariance on a grid;
self-attention is permutation equivariance on a set (Definition 2.32); message passing is
permutation equivariance on a graph. Recurrence is time-translation equivariance with a causal
mask. Under this frame the three architectures the source note treats as alternatives are the
*same* construction applied to three different symmetry groups.

### 2.12 Temporal-graph hybrids

**Definition 2.51 (spatio-temporal graph network).** Interleave a spatial operator `S` (any of
2.39–2.43) with a temporal operator `T` (gated recurrence, dilated causal convolution, or
attention). DCRNN [67] replaces the matrix products inside a GRU with diffusion convolutions;
STGCN [68] alternates temporal gated convolutions and graph convolutions; Graph WaveNet [69]
adds a learned adaptive adjacency `A_adp = softmax(ReLU(E_1 E_2^T))`; TGN [70] maintains a
per-node memory updated by timestamped events.

**Remark 2.52.** Graph WaveNet's `A_adp` is the cleanest statement of "learn the graph": the
adjacency becomes a low-rank, row-stochastic, learned parameter. It inherits Property 2.30 —
a learned softmax adjacency is dense.

### 2.13 Probabilistic heads and proper scoring

**Definition 2.53 (proper scoring rule; Gneiting–Raftery [87]).** `S(F, y)` is proper if
`E_{y~G} S(G, y) >= E_{y~G} S(F, y)` for all `F, G`, and strictly proper if equality forces
`F = G`. Logarithmic score, CRPS [85], the Brier score [84] and the pinball loss [86] are
proper; MAE and MSE on a point forecast elicit the median and the mean respectively.

**Definition 2.54 (parametric head; DeepAR [71]).** Emit `theta_t = f(h_t)` parameterising a
likelihood `p(y_t | theta_t)`; train by NLL, i.e. by the logarithmic score; sample forward for
multi-step paths.

**Definition 2.55 (quantile head; TFT [72]).** Emit `q_hat_t^{(tau)}` for a finite set of
levels; train with the pinball loss `L_tau(y, q) = max(tau (y - q), (tau - 1)(y - q))`. TFT
adds variable-selection networks and interpretable multi-head attention over time.

**Remark 2.56 (uncertainty is not calibration).** Deep ensembles [91] and MC-dropout [90] give
predictive spread; [92] shows modern networks are systematically over-confident, so a spread
is not a calibrated interval until it has been checked against realised outcomes. Every one
of 2.53–2.56 presupposes an observable `y`. §5.15 is about what happens when there is none.

### 2.14 The honest empirical record

**Result 2.57 (Zeng et al. [77]).** On the standard long-horizon multivariate benchmarks, a
one-layer linear map from the lookback window to the forecast horizon (`DLinear`, `NLinear`)
matches or beats Informer [74], Autoformer [75] and their successors on most datasets and
horizons. The stated diagnosis is that permutation-equivariant self-attention (Definition
2.32) discards temporal order, which is precisely what the task needs.

**Result 2.58 (M competitions [79], [80], [81]).** In M4, pure machine-learning entries
underperformed simple statistical benchmarks; the winner [78] was a hybrid of exponential
smoothing with a dilated LSTM, and the runner-up was a weighted combination of statistical
methods. Combination, not architecture, carried the result. M5 was won by gradient-boosted
trees rather than by deep networks. [79] documents the same for a wide method sweep.

**Result 2.59 (tabular; Grinsztajn et al. [83]).** On typical tabular data, tree ensembles
still outperform deep networks; the identified causes are rotation-invariance of MLPs,
sensitivity to uninformative features, and irregular target functions.

**Result 2.60 (RNN forecasting; Hewamalage et al. [82]).** A controlled study finds RNNs
competitive only with careful preprocessing, validation design, and when the corpus contains
many related series; they are *not* competitive on isolated short series.

*Reading for AMF.* 2.57–2.60 are the prior this module adopts. They do not say deep learning
fails; they say the burden of proof sits with the architecture, that the correct baseline is
linear, and that data volume rather than depth is the operative variable. AMF has one market
at a time and no observed outcomes at all.

---
## 3. Academic curriculum modules

The ladder below is the sequence a graduate student would actually take. The final column is
deliberately narrow: most of each course is irrelevant to AMF, and the entry names the part
that is not. Course codes are given only where verified; where a code is uncertain the subject
is named instead.

| Module | Level | Canonical course(s) | Core texts (exact units) | What AMF needs from it |
|---|---|---|---|---|
| M1. Linear algebra and matrix analysis | UG2 | **MIT 18.06** *Linear Algebra*; any matrix-analysis course | Horn & Johnson [121] **Ch. 1, 5, 8**; [104] **Ch. 2** | Spectral radius, induced norms, Perron–Frobenius — the machinery of Propositions 5.5–5.6 |
| M2. Probability, statistics, and statistical learning | UG3 | **Stanford CS229** *Machine Learning*; any mathematical-statistics sequence | Hastie–Tibshirani–Friedman [110] **Ch. 2, 3, 7**; Shalev-Shwartz & Ben-David [111] **Ch. 2–6** | Empirical risk minimisation, the estimation/approximation split, why §5.10's parameter count matters |
| M3. Convex optimisation | UG4/PG1 | **Stanford EE364A** *Convex Optimization* | Boyd & Vandenberghe [119] **Ch. 2–5, 9**; Nocedal & Wright [120] **Ch. 3, 6** | The baseline against which Theorem 2.14's failure is legible |
| M4. Feedforward networks and backpropagation | UG4/PG1 | **Stanford CS230** *Deep Learning*; **MIT 6.S191** *Introduction to Deep Learning*; **CMU 11-785** *Introduction to Deep Learning* | Goodfellow–Bengio–Courville [104] **Ch. 6 (feedforward), Ch. 7 (regularisation), Ch. 8 (optimisation)**; Prince [109] **Ch. 3–7**; Bishop [105] **Ch. 5** | Definitions 2.1, 2.16–2.21; the reason a network is a composition of affine maps and nothing more |
| M5. Approximation theory for networks | PG2 | Theory-of-deep-learning topics courses | [1], [2], [4], [5]; Telgarsky [7]; Eldan & Shamir [6] | Theorems 2.2–2.6, and the discipline of separating representation from recovery |
| M6. Stochastic optimisation | PG1 | **Berkeley CS182/282A** *Designing, Visualizing and Understanding Deep Neural Networks*; large-scale-optimisation courses | Bottou–Curtis–Nocedal [19] **§3–5**; [104] **Ch. 8**; [11], [16], [17] | Why the default optimiser needs a fixed seed, a fixed step schedule, and a fixed reduction arrangement to be reproducible |
| M7. Convolutional architectures | PG1 | **Stanford CS231n** *Deep Learning for Computer Vision* | [104] **Ch. 9**; Prince [109] **Ch. 10** | Only as the source of the residual connection [23] and of the weight-sharing idea reused by MPNNs |
| M8. Sequence models and recurrence | PG1 | **Stanford CS224n** *Natural Language Processing with Deep Learning* (lectures on RNNs, LSTMs, seq2seq, attention) | [104] **Ch. 10 (§10.7 vanishing gradients, §10.10 LSTM/GRU)**; [30], [31], [33], [35] | Theorem 2.24 and Definitions 2.25–2.26 — the exact analogue of AMF's stress recurrence (§5.5) |
| M9. Attention and transformers | PG1/PG2 | **Stanford CS224n** (transformer lectures); **Stanford CS25** *Transformers United* seminar | [38]; [39]; [25]; Prince [109] **Ch. 12**; Bishop & Bishop [106] **Ch. 12** | Definitions 2.29–2.33 and Property 2.30, which is the crux of §5.7 |
| M10. Efficient attention and long context | PG2 | Advanced-NLP and systems-for-ML seminars | Tay et al. [46]; [42]–[45] | Only to know it is inapplicable at `n = 7` (§5.9) — the module a contributor is most likely to invoke wrongly |
| M11. Spectral graph theory | PG1 | Spectral-graph-theory and algebraic-graph-theory courses | Chung [118] **Ch. 1–2**; Shuman et al. [52] | Definition 2.36 and the eigenvalue arithmetic of §5.8 |
| M12. Graph representation learning | PG1/PG2 | **Stanford CS224W** *Machine Learning with Graphs* | Hamilton [112] **Ch. 5 (GNN model), Ch. 6 (GNNs in practice), Ch. 7 (theoretical motivations)**; [53], [54], [55], [56] | Definitions 2.37–2.42; the layer AMF turns out already to contain (Theorem 5.3) |
| M13. GNN expressivity | PG2/PG3 | Graph-learning theory seminars | [57], [58], [59]; Hamilton [112] **Ch. 7**; [47] | Theorem 2.45 and the 1-WL computation of §5.7 |
| M14. Depth pathologies on graphs | PG2/PG3 | Same seminars, later units | [60], [61], [62], [63], [64] | Theorem 2.47 and the receptive-field/over-smoothing arithmetic of §5.8 |
| M15. Geometric deep learning | PG3 | Geometric-deep-learning courses and the associated lecture series | Bronstein et al. [66] **Ch. 3–5**; [65] | Principle 2.50, which is what makes §5's translation table more than a metaphor |
| M16. Time-series forecasting, classical | PG1 | Forecasting and time-series-econometrics sequences | Hyndman & Athanasopoulos [115] **Ch. 3, 5, 8, 9**; Box et al. [116] **Ch. 3–5**; Hamilton [117] **Ch. 3–5** | The baselines of Results 2.57–2.60; the meaning of "seasonal naive" as a null |
| M17. Deep forecasting | PG2 | Applied-forecasting and time-series-ML topics courses | Benidis et al. [114]; [71], [72], [73], [74], [75], [76] | Probabilistic heads (Definitions 2.54–2.55) and the honest comparison in [77] |
| M18. Forecast evaluation and proper scoring | PG2 | Statistical-forecasting and probabilistic-forecasting courses | Gneiting & Raftery [87]; Hyndman & Koehler [88]; Diebold & Mariano [89] | Why AMF cannot score its own ensemble (§5.15), and why that is the decisive fact |
| M19. Interpretability and its limits | PG2 | Interpretable-ML and trustworthy-ML courses | Rudin [95]; Jain & Wallace [93]; Wiegreffe & Pinter [94] | The evidence that attention weights are not explanations — against which `sensitivity.py` compares favourably (§5.13) |
| M20. Machine learning in finance, critically | PG2/PG3 | Financial-machine-learning and empirical-asset-pricing topics courses | Gu–Kelly–Xiu [99]; Harvey–Liu–Zhu [100]; Bailey et al. [101]; López de Prado [102] **Ch. 7, 11–12**; Sezer et al. [103] | The base rate for claims of this kind, and the specific pathologies (multiple testing, leakage, overlapping samples) that make them fail |
| M21. Floating-point determinism | PG1 | Scientific-computing and numerical-analysis courses | Goldberg [123]; Higham [122] **Ch. 1–4** | Why any network in `src/amf` would have to fix its summation arrangement (§5.16) |

Sequencing note: M1, M2, M4, M8 and M12 suffice to read every result in §5. M13 and M14 are
what turn §5.7–§5.8 from arithmetic into argument. M10 is the module most likely to be
invoked by a contributor who has not checked `n`. A contributor who skips M18 will propose a
probabilistic head for a quantity that has no realisation to be scored against, which is the
single most likely way for this discussion to produce a rule-2 violation.

---

## 4. Exact source material

Every entry is annotated with the exact contribution relied on in this module. Identifiers are
given only where confirmed; where a page range or number could not be confirmed it is omitted
rather than guessed.

### 4.1 Primary and seminal papers

- **Approximation.** Cybenko [1] and Hornik–Stinchcombe–White [2] independently establish
  density of one-hidden-layer networks; Hornik [3] extends to derivatives;
  Leshno–Lin–Pinkus–Schocken [4] give the sharp non-polynomiality criterion (Theorem 2.3);
  Barron [5] supplies the `O(C_f^2/n)` rate (Theorem 2.4). Eldan–Shamir [6] and Telgarsky [7]
  are the two canonical depth-separation results.
- **Hardness and generalisation.** Blum–Rivest [8]: exact fitting of a 3-node network is
  NP-complete. Zhang et al. [9]: architectures memorise random labels, so architecture-only
  capacity bounds cannot explain generalisation. Belkin et al. [10]: double descent.
- **Optimisation.** Robbins–Monro [11] (the origin of SGD); Polyak [12] (heavy ball);
  Nesterov [13] (accelerated gradient); Rumelhart–Hinton–Williams [14] (backpropagation as a
  learning procedure); Duchi–Hazan–Singer [15] (AdaGrad); Kingma–Ba [16] (Adam);
  Reddi–Kale–Kumar [17] (Adam's published proof is wrong; AMSGrad); Loshchilov–Hutter [18]
  (decoupled weight decay).
- **Normalisation and residuals.** Srivastava et al. [20] (dropout); Ioffe–Szegedy [21] (batch
  norm); Ba–Kiros–Hinton [22] (layer norm); He et al. [23] (residual learning);
  Santurkar et al. [24] (the mechanism of batch norm is smoothing, not covariate shift);
  Xiong et al. [25] (Pre-LN removes the warm-up requirement).
- **Recurrence.** Elman [26]; Werbos [27] (BPTT); Hochreiter [28] (the original vanishing-
  gradient analysis, in German); Bengio–Simard–Frasconi [29] (Theorem 2.24);
  Hochreiter–Schmidhuber [30] (LSTM); Gers–Schmidhuber–Cummins [31] (the forget gate, absent
  from the 1997 paper); Pascanu–Mikolov–Bengio [32] (gradient clipping and the exploding
  regime); Cho et al. [33] (GRU and the encoder–decoder); Chung et al. [34];
  Greff et al. [35] (the ablation that ranks the components).
- **Attention.** Bahdanau–Cho–Bengio [36] (attention as a differentiable alignment);
  Luong–Pham–Manning [37]; Vaswani et al. [38] (the transformer); Shaw et al. [39] (relative
  positions); Su et al. [40] (rotary positions); Martins–Astudillo [41] (sparsemax — the
  projection that *can* return exact zeros, unlike softmax).
- **Efficient attention.** Child et al. [42]; Katharopoulos et al. [43]; Wang et al. [44];
  Choromanski et al. [45].
- **Graphs.** Weisfeiler–Leman [47]; Gori et al. [48] and Scarselli et al. [49] (the original
  GNN as a contraction fixed point); Bruna et al. [50] (spectral networks);
  Hammond et al. [51] (graph wavelets); Defferrard et al. [53] (ChebNet); Kipf–Welling [54]
  (GCN); Hamilton et al. [55] (GraphSAGE); Veličković et al. [56] (GAT);
  Gilmer et al. [57] (the MPNN abstraction used verbatim in Theorem 5.3);
  Xu et al. [58] and Morris et al. [59] (the 1-WL ceiling); Li–Han–Wu [60] and
  Oono–Suzuki [61] (over-smoothing); Alon–Yahav [62] and Topping et al. [63]
  (over-squashing); Chen et al. [64] (GCNII's initial residual).
- **Temporal graphs.** Li et al. [67] (DCRNN); Yu et al. [68] (STGCN); Wu et al. [69] (Graph
  WaveNet and its learned adaptive adjacency); Rossi et al. [70] (TGN).
- **Deep forecasting.** Salinas et al. [71] (DeepAR); Lim et al. [72] (TFT);
  Oreshkin et al. [73] (N-BEATS, a pure-MLP basis-expansion model that beat the M4 winner);
  Zhou et al. [74] (Informer); Wu et al. [75] (Autoformer); Nie et al. [76] (PatchTST).
- **Scoring.** Brier [84]; Matheson–Winkler [85] (CRPS); Koenker–Bassett [86] (quantile
  regression, hence the pinball loss); Gneiting–Raftery [87] (the definitive treatment);
  Hyndman–Koehler [88] (MASE and the case against MAPE); Diebold–Mariano [89] (testing
  whether two forecast records differ at all).
- **Uncertainty and interpretability.** Gal–Ghahramani [90]; Lakshminarayanan et al. [91];
  Guo et al. [92] (modern networks are miscalibrated); Jain–Wallace [93] and
  Wiegreffe–Pinter [94] (the two sides of "is attention explanation?"); Rudin [95] (the case
  for interpretable models in high-stakes settings).

### 4.2 Canonical textbooks

- **[104] Goodfellow, Bengio & Courville, *Deep Learning*, MIT Press 2016.** Ch. 6 feedforward
  networks and the chain rule; Ch. 7 regularisation; Ch. 8 optimisation (§8.2 ill-conditioning,
  §8.5 adaptive methods); Ch. 9 convolution; **Ch. 10 sequence modelling — §10.2 (BPTT), §10.7
  (long-term dependencies), §10.10 (LSTM and gated units)** is the chapter this module leans on
  hardest; Ch. 11 practical methodology.
- **[105] Bishop, *Pattern Recognition and Machine Learning*, Springer 2006.** Ch. 3 linear
  models (the baseline of Result 2.57), Ch. 5 neural networks (§5.3 backpropagation, §5.5
  regularisation), Ch. 1 for decision theory and the loss/estimand correspondence.
- **[106] Bishop & Bishop, *Deep Learning: Foundations and Concepts*, Springer 2024.** Ch. 12
  is the cleanest textbook derivation of the transformer.
- **[109] Prince, *Understanding Deep Learning*, MIT Press 2023.** Ch. 3–7 (shallow and deep
  networks, loss, fitting, gradients), Ch. 12 (transformers), Ch. 13 (graph networks).
  Openly available and the best single entry point for a contributor starting from M4.
- **[107], [108] Murphy, *Probabilistic Machine Learning*, MIT Press 2022 / 2023.** Volume 1
  Ch. 13 (feedforward), Ch. 15 (sequences); Volume 2 for the probabilistic heads of §2.13.
- **[110] Hastie, Tibshirani & Friedman, *The Elements of Statistical Learning*, 2nd ed.,
  Springer 2009.** Ch. 2, 3, 7 for the estimation/approximation split; Ch. 10, 15 for the tree
  ensembles that win in Results 2.58–2.59.
- **[111] Shalev-Shwartz & Ben-David, *Understanding Machine Learning*, CUP 2014.** Ch. 2–6 for
  the formal learning framework; Ch. 20 for neural networks and their hardness.
- **[112] Hamilton, *Graph Representation Learning*, Morgan & Claypool 2020.** Ch. 5 the GNN
  model, Ch. 6 practice, **Ch. 7 theoretical motivations** (the WL connection).
- **[115] Hyndman & Athanasopoulos, *Forecasting: Principles and Practice*, 3rd ed., OTexts
  2021.** Ch. 3 (benchmarks and residual diagnostics), Ch. 5 (evaluation), Ch. 8–9
  (exponential smoothing, ARIMA). Openly available; the baseline discipline of M16.
- **[116] Box, Jenkins, Reinsel & Ljung, *Time Series Analysis: Forecasting and Control*, 5th
  ed., Wiley 2015**, and **[117] Hamilton, *Time Series Analysis*, Princeton UP 1994.**
- **[118] Chung, *Spectral Graph Theory*, AMS 1997.** Ch. 1–2 for the normalised Laplacian and
  its spectrum.
- **[119] Boyd & Vandenberghe, *Convex Optimization*, CUP 2004**; **[120] Nocedal & Wright,
  *Numerical Optimization*, 2nd ed., Springer 2006.**
- **[121] Horn & Johnson, *Matrix Analysis*, 2nd ed., CUP 2013.** Ch. 5 (norms), Ch. 8
  (nonnegative matrices) for Propositions 5.5–5.6.
- **[122] Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM 2002.**

### 4.3 Surveys and reviews

- **[46] Tay, Dehghani, Bahri & Metzler, "Efficient Transformers: A Survey".** The taxonomy of
  everything in §2.7; read it to conclude that AMF needs none of it.
- **[113] Wu, Pan, Chen, Long, Zhang & Yu, "A Comprehensive Survey on Graph Neural Networks".**
  The standard taxonomy: recurrent, convolutional, autoencoder, spatio-temporal.
- **[114] Benidis et al., "Deep Learning for Time Series Forecasting: Tutorial and Literature
  Survey".** The single best map of the deep-forecasting field, including the local/global
  distinction that explains Result 2.60.
- **[65], [66] Bronstein et al.** The 2017 magazine article and the 2021 monograph;
  Principle 2.50.
- **[103] Sezer, Gudelek & Ozbayoglu.** 2005–2019 systematic review of deep learning on
  financial time series — useful precisely because it shows how rarely the papers it surveys
  report a competitive statistical baseline.

### 4.4 Open courseware and lecture notes

- **Stanford CS231n**, *Deep Learning for Computer Vision* — notes and assignments; the
  reference implementation of backpropagation from scratch.
- **Stanford CS224n**, *Natural Language Processing with Deep Learning* — the RNN, seq2seq,
  attention and transformer lecture sequence; lecture videos and notes are public.
- **Stanford CS224W**, *Machine Learning with Graphs* — the course this module's §5.7–§5.8
  most directly draws on; slides and the accompanying Colab notebooks are public.
- **Stanford CS229** *Machine Learning* and **CS230** *Deep Learning*; **CS25** *Transformers
  United* seminar.
- **MIT 6.S191**, *Introduction to Deep Learning* — a one-week intensive; the best fast path
  through M4.
- **MIT 18.06**, *Linear Algebra* (OCW) — for M1.
- **UC Berkeley CS182 / CS282A**, *Designing, Visualizing and Understanding Deep Neural
  Networks* — lecture videos public; the strongest treatment of optimisation pathologies.
- **CMU 11-785**, *Introduction to Deep Learning*, and **CMU 10-707**, *Advanced Deep
  Learning* — the recommended sequence is 11-785 first.
- **NYU DS-GA 1008**, *Deep Learning* — materials public.
- **University of Oxford**, Department of Computer Science *Machine Learning* course, and the
  associated deep-learning lecture series; **University of Cambridge**, the MPhil in Machine
  Learning and Machine Intelligence and the Part III / Part II machine-learning courses.
  (Course codes for the Oxford and Cambridge offerings are omitted deliberately: the subject
  is named where the number could not be confirmed.)

### 4.5 Domain application to markets — including the sceptical literature

- **[99] Gu, Kelly & Xiu, "Empirical Asset Pricing via Machine Learning".** The most careful
  large-scale comparison; trees and neural networks improve out-of-sample fit, and the paper
  is scrupulous about the multiple-testing and sample-overlap issues. Read alongside [100].
- **[100] Harvey, Liu & Zhu.** Hundreds of published factors; after a multiple-testing
  correction most do not survive. The base-rate paper.
- **[101] Bailey, Borwein, López de Prado & Zhu.** Formalises how quickly repeated trials
  produce a spuriously good historical simulation; the arithmetic of the minimum number of
  trials needed to manufacture one.
- **[102] López de Prado, *Advances in Financial Machine Learning*, Wiley 2018.** Ch. 7
  (cross-validation under overlapping samples), Ch. 11–12 (the pathologies of repeated
  historical evaluation). Note that the entire book operates inside the vocabulary rule 1
  forbids, which is exactly why it belongs in a boundary discussion.
- **[96] Fama (1970)**, **[97] Timmermann & Granger (2004)**, **[98] Lo (2004)**. The
  efficiency question stated by its principals: [97] is the direct statement of what
  forecastability would have to mean, and [98] the adaptive reformulation.
- **[77] Zeng et al.**, **[79]–[82] the M-competition literature**, **[83] Grinsztajn et al.**
  The sceptical core of §2.14. These are not contrarian outliers; they are the mainstream
  evaluation record of the forecasting community.
- **[95] Rudin.** The argument that in high-stakes settings a black box plus a post-hoc
  explanation is worse than an interpretable model. AMF is, by construction, the interpretable
  model; §5.13 shows what it would give up.

---
## 5. Derivation for the AMF setting

This section does the actual mathematics. Every numerical value quoted is a computed fact
about `examples/sample_market.json` under the default `SimulationConfig`, reproducible from
the repository with the standard library alone; none of it is a statement about any real
market.

### 5.1 Notation fixed to the codebase

Let `V = (skeleton, circulatory, nervous, musculature, organs, immune, metabolism)` in
`SystemKind` declaration order, `n = |V| = 7`. For system `j`:

```
m_j = (integrity_j, redundancy_j, criticality_j, load_j) in [0,1]^4
h_j = integrity_j * (1 - load_j)                                  # health
a_j = 0.5*redundancy_j + 0.3*integrity_j + 0.2*(1 - load_j)       # absorptive_capacity
```

Let `W in [0,1]^{n x n}` be `DependencyGraph.coupling_matrix()`, so that `W[i][j]` is the
weight with which stress flows from transmitter `i` to receiver `j` — the *reverse* of the
dependency edge, since a dependent is loaded by a stressed provider. Let
`Theta = damping = 0.85`, `rho = retention = 0.5`, `tau = transmission = 1.0`, and
`phi(z) = min(1, max(0, z))`.

### 5.2 The market as an attributed directed multigraph

A `Market` is `G = (V, E, m, w)` with `E subset V x V x DependencyKind`, `|V| = 7` fixed,
`|E| <= 7*6*4 = 168`, node attributes `m: V -> [0,1]^4`, and edge weights `w: E -> (0,1]`.
Every structural query in `graph.py` first projects the multigraph onto its pair-level
aggregate `W`, capped at `1.0`. So the object a graph network would consume is a *labelled*,
*typed*, *directed*, *small* graph with a fixed vertex set — a regime the GNN literature
barely addresses, because that literature is built for large graphs with anonymous vertices.

### 5.3 The simulator step is exactly a message-passing layer

**Theorem 5.3.** Fix `cascade_threshold = None`, `recovery_rate = 0`, `jitter = 0` and no
interventions — the documented defaults. Set node states `h_j^{(t)} = x_t[j] in R`, and

```
M_t( h_i, h_j, e_{ij} )  =  W[i][j] * h_i                       # message
U_t( h_j, m_j )          =  phi( Theta*rho*h_j + Theta*tau*(1 - a_j)*m_j )   # update
```

Then `ShockSimulator._advance` computes exactly `h^{(t+1)} = U_t(h^{(t)}, sum_i M_t(...))`,
i.e. one MPNN layer in the sense of Definition 2.43, with sum aggregation.

*Proof.* `_advance` computes, for each receiver `j`,
`incoming = sum_i x_t[i] * W[i][j] * tau` and then
`value = Theta * (x_t[j]*rho + incoming*(1 - a_j))`, clipped to `[0,1]`. Substituting the two
displayed maps reproduces this expression term for term. Aggregation is a sum over
transmitters; the guard `if weight <= 0.0: continue` restricts the sum to `N(j)`, which is
what `sum_{i in N(j)}` means. `phi` is the elementwise clip. `[]`

**Corollary 5.3.1 (it is a GCN in the sense of Definition 2.39).** Writing
`D_a = diag(1 - a_j)`, one step of the linear part is `x <- Theta(rho I + tau D_a W^T) x`,
which has the shape `sigma(A_hat H Theta_l)` of Kipf–Welling with (i) hidden width `d = 1`,
(ii) the learned matrix `Theta_l` replaced by the scalar `Theta*tau`, (iii) the symmetric
renormalisation `D^{-1/2}(A+I)D^{-1/2}` replaced by the asymmetric, absorption-gated
`rho/tau * I + D_a W^T`, and (iv) ReLU replaced by hardtanh on `[0,1]`.

**Corollary 5.3.2 (the retention term is an initial-residual connection).** The `rho*x_j` term
is structurally the `a H^{(0)}` term GCNII [64] introduces to defeat over-smoothing
(Remedy 2.49) — except that AMF applies it to the *previous* state rather than the input, i.e.
it is the residual connection of [23] with coefficient `Theta*rho = 0.425`.

### 5.4 The unrolled simulator is a parameter-free, weight-tied graph network

**Corollary 5.4.** `propagate` with `max_steps = T` is a weight-tied MPNN of depth `T`
(default `T = 50`) over a 7-node graph, with one-dimensional node states, non-learned edge
weights, sum aggregation, hardtanh activation, and **zero learnable parameters**. `stress_test`
runs it `n` times with different one-hot inputs; `ensemble` runs it `runs` times with jittered
edge weights and a fixed base seed.

This is the central structural claim of this module. The source note proposes adding a graph
neural network to AMF. AMF already *is* one; what it lacks is not the architecture but the
training data, and adding parameters without data converts an exactly specified model into an
under-determined one.

### 5.5 The linear regime: spectral radius, and what the clip is doing

**Proposition 5.5.** Define `B = Theta (rho I + tau D_a W^T) in R_{>=0}^{7x7}`, i.e.
`B[j][i] = Theta*(rho*[i=j] + tau*(1 - a_j)*W[i][j])`. While no coordinate saturates,
`x_{t+1} = B x_t`, hence `x_t = B^t x_0`. The trajectory decays to `0` iff the spectral radius
`r(B) < 1`; it grows until the clip binds iff `r(B) > 1`. For a nonnegative matrix,
`min_j sum_i B[j][i] <= r(B) <= max_j sum_i B[j][i]` ([121] Ch. 8).

**Fact 5.5.1 (the sample market).** Computed from `examples/sample_market.json`:

| receiver `j` | `a_j` | `sum_i W[i][j]` | row sum of `B` = `Theta(rho + (1-a_j) sum_i W[i][j])` |
|---|---|---|---|
| skeleton | 0.540 | 0.00 | 0.425000 |
| circulatory | 0.540 | 1.30 | 0.933300 |
| nervous | 0.670 | 1.10 | 0.733550 |
| musculature | 0.800 | 0.70 | 0.544000 |
| organs | 0.700 | 0.60 | 0.578000 |
| immune | 0.750 | 0.30 | 0.488750 |
| metabolism | 0.700 | 0.40 | 0.527000 |

`||B||_inf = 0.933300`, `||B||_1 = 0.941800`, and power iteration gives
`r(B) = 0.582613`. The sample market's step map is therefore a contraction, its stress decays
geometrically at rate `~0.58` per step, and 50 steps is a generous horizon.

**Proposition 5.6 (non-contraction is constructible, and is the exploding regime).** Take
every system with `redundancy = 0`, `integrity = 0`, `load = 1`, so `a_j = 0` for all `j` —
all admissible under `systems.py` validation — and couple every ordered pair at weight `1.0`,
so `sum_i W[i][j] = 6`. Every row of `B` then sums to `0.85*(0.5 + 6) = 5.525`, hence
`r(B) >= 5.525 > 1`. Stress grows geometrically until every coordinate saturates at `1.0`.

**Remark 5.6.1.** Propositions 5.5–5.6 are Theorem 2.24 with the sign of the inequality
carried over verbatim: `r(B) < 1` is the *vanishing* regime and `r(B) > 1` the *exploding*
regime of a recurrent map, here with fixed rather than learned weights. AMF handles the
exploding regime the way Pascanu–Mikolov–Bengio [32] handle it — by clipping — except that AMF
clips the **state** rather than the gradient, and the clip is not a heuristic but the
definition of the `[0,1]` stress scale. This is also why `converged` in `SimulationTrace`
reports whether the trajectory settled within budget and not whether it is stable: the
saturated state `x = 1` is a fixed point of `phi o B` whenever `r(B) > 1`, and it is
perfectly "settled".

**Remark 5.6.2 (what an LSTM would change).** Definition 2.25 replaces the fixed scalar `rho`
with a learned, state-dependent `f_t in (0,1)^n`. Applied to AMF, that would make retention a
function of current stress — an entirely reasonable *modelling* choice, expressible without
any learning as a fixed function `rho(x)`. What it would not do is give AMF anything to fit.

### 5.6 The opt-in cascade dynamics is hard multiplicative gating

**Proposition 5.7.** With `cascade_threshold = theta`, `cascade_gain = gamma`,
`cascade_absorption_drop = delta`, define
`g_i(x) = 1 + gamma*1[x_i > theta]` and `k_j(x) = 1 - delta*1[x_j > theta]`. Then

```
x_{t+1}[j] = phi( Theta * ( rho*x_t[j] + tau*(1 - a_j*k_j(x_t)) * sum_i g_i(x_t)*W[i][j]*x_t[i] ) )
```

which is Theorem 5.3's layer with a multiplicative **transmit gate** `g_i` on each outgoing
message and a multiplicative **receive gate** `k_j` on the absorption term.

**Corollary 5.7.1.** Replacing `1[z > theta]` by `sigmoid(beta (z - theta))` yields a
differentiable gated MPNN that converges pointwise to AMF's cascade dynamics as
`beta -> infinity`. AMF's cascade is therefore the zero-temperature limit of exactly the
gating mechanism of Definition 2.26 (GRU) applied on edges rather than on a hidden vector.
`recovery_rate` plays the role of the bias term `b` in `sigma(Wx + b)`, applied before the
clip. `Intervention.absorptive_boost` is a scheduled additive modification of `a_j`.

The practical consequence is that the source note's three architectures are not three
alternatives for AMF: two of the three are already present in `simulation.py`, in their
non-learned, non-differentiable, deterministic form. That form is what satisfies rules 2 and 3.

### 5.7 Self-attention is a learned `CouplingMatrix`, and softmax is the wrong prior

Let `H in R^{7 x d}` embed the four structural metrics of each system. Definition 2.29 gives
`A = softmax_row(H W_Q (H W_K)^T / sqrt(d_k)) in R^{7x7}`. This is the same *type* of object as
`CouplingMatrix.data`: a `7 x 7` array of directed influence weights over the same index set.
The note's "Transformer layer 1" is, stripped of market data, precisely the proposal to
*learn* `W` instead of specifying it.

**Proposition 5.8 (softmax cannot express AMF's couplings).** For any finite `Q, K`,
`A_{ij} > 0` for every pair (Property 2.30), and every row sums to `1`. But in
`examples/sample_market.json` the rows of `W` for `immune` and `metabolism` are identically
zero (they transmit to nothing), the row for `organs` sums to `0.40`, and the row for
`circulatory` sums to `1.30`. Hence `A` can reproduce neither the exact zeros nor the
non-unit row masses of `W`. Softmax self-attention imposes the prior "every system transmits
exactly one unit of influence to a strictly positive extent everywhere", which is false of
every market AMF can express.

**Corollary 5.8.1 (the correct form is GAT, or a sparse projection).** Two in-boundary
repairs: (i) mask attention to the existing edge set, which is exactly Definition 2.42 (GAT) —
then non-edges stay zero and only *existing* couplings are re-weighted; (ii) replace softmax
by sparsemax [41], whose Euclidean projection onto the simplex returns exact zeros. Neither
repairs the row-sum constraint, which only an unnormalised gate (a sigmoid per edge) removes.

**Remark 5.8.2.** The learned adaptive adjacency of Graph WaveNet [69],
`A_adp = softmax(ReLU(E_1 E_2^T))`, has the same defect and adds a low-rank constraint. If a
future contributor wants a learned coupling structure, the honest specification is a
per-edge sigmoid gate on a *fixed* candidate edge set, which keeps `W` in `[0,1]` and keeps
absent couplings absent.

### 5.8 Expressivity: 1-WL separates all seven systems in two rounds

Running Definition 2.44 on the undirected skeleton of the sample market's dependency graph,
from *constant* initial colours:

```
round 1:  4 classes   {immune, metabolism} | {musculature, organs} | {skeleton, nervous} | {circulatory}
round 2:  7 classes   all systems distinct
round 3:  7 classes   stable
```

**Proposition 5.9.** By Theorem 2.45, a 2-layer sum-aggregation MPNN with injective update
(GIN) already distinguishes every pair of systems in this market even with anonymous nodes.
A fortiori, AMF's nodes are *not* anonymous: each carries a distinct `SystemKind` and a
4-dimensional real feature vector, so the initial colouring is already discrete and 1-WL is
stable at round `0`.

**Corollary 5.9.1.** The central limitation of the MPNN literature — the 1-WL ceiling, and the
higher-order architectures [59] built to escape it — buys AMF exactly nothing. This is a
positive finding and should be recorded as such: whatever else is wrong with putting a GNN in
AMF, expressivity is not it.

### 5.9 Receptive field versus over-smoothing at diameter 4

The undirected skeleton of the sample market has diameter `4` (e.g. `immune` to `metabolism`
via `skeleton -> circulatory -> organs`). The renormalised GCN operator
`A_hat = D_t^{-1/2}(A + I) D_t^{-1/2}` of the symmetrised graph has spectrum

```
{ -0.094935, 0.138334, 0.360606, 0.420829, 0.778108, 0.862365, 1.000000 }
```

so `lambda_1 = 1` and `|lambda_2| = 0.862365`. The normalised Laplacian `L_sym` of the
weighted graph has spectrum `{0, 0.372489, 0.681020, 1.186610, 1.299317, 1.619244, 1.841320}`;
the single zero confirms connectivity, and `lambda_2(L_sym) = 0.372489` is the spectral gap.

**Proposition 5.10 (the depth window is empty-ish).** By Definition 2.48 a GCN needs
`L >= 4` layers for `immune` to influence `metabolism` at all. By Theorem 2.47 the component
orthogonal to the dominant eigenvector has already contracted by `|lambda_2|^L`:

| `L` | 1 | 2 | 3 | 4 | 6 | 8 | 12 | 50 |
|---|---|---|---|---|---|---|---|---|
| `|lambda_2|^L` | 0.862 | 0.744 | 0.641 | 0.553 | 0.411 | 0.306 | 0.169 | 0.00061 |

At the minimum depth that covers the graph, 45 % of the discriminative signal component is
already gone; at `L = 8` it is 69 %. On a 7-node graph the diameter is a large fraction of the
graph, so over-smoothing bites at shallower depth than on the large graphs [61] studies.

**Corollary 5.10.1.** Any graph network added to AMF must carry an initial-residual term
([64], Remedy 2.49). AMF's simulator already does (Corollary 5.3.2), with `Theta*rho = 0.425`
retained per step — which is why 50 steps of AMF's own propagation do not collapse to a
constant vector: the retention term is not a stylistic choice but the thing that keeps the
trajectory informative.

### 5.10 Attention cost at `n = 7`: the quadratic term is 2.7 % of the work

By Proposition 2.34, one attention layer with `n = 7` and `d = 64` costs
`n^2 d = 49 * 64 = 3 136` multiply-accumulates for the score matrix and `4 n d^2 =
4 * 7 * 4096 = 114 688` for the `Q, K, V, O` projections. The quadratic term is
`3136 / 117824 = 2.66 %` of the layer.

**Corollary 5.11.** Every technique in §2.7 — sparse attention, Linformer, Performer, linear
attention — reduces the term that accounts for 2.7 % of an AMF-sized attention layer, at the
cost of an approximation error. Proposing one for AMF is a category error, and this module
records it in advance because it is the single most predictable review comment on any future
architecture proposal here.

### 5.11 Parameter budget versus the size of AMF's state space

A complete AMF market is at most `7*4 = 28` metric scalars plus at most `168` typed edge
weights: `<= 196` real numbers, of which `examples/sample_market.json` uses `28 + 8 = 36`.
A minimal two-layer GCN with hidden width `32`, 4-dimensional node inputs and a scalar readout
has `4*32 + 32 + 32*32 + 32 + 32*1 + 1 = 1 249` parameters. One transformer block with
`d = 64`, `h = 4`, `d_ff = 256` has `4*64*64 + 2*64*256 + 4*64 = 49 408`.

**Proposition 5.12.** The parameter-to-observation ratio for a single market is `1249/36 ~ 35`
for the smallest useful graph network and `~1372` for one transformer block. AMF has no corpus
of markets: `examples/sample_market.json` is one hand-written file, `tests/conftest.py`
generates markets from a factory whose distribution *is* the model, and no observed outcome is
attached to any of them. There is therefore no `(x, y)` pair anywhere in the repository, and
`E_{(x,y)} l(f(x), y)` is undefined. This is the arithmetic behind hard rule 2, stated without
appeal to policy.

### 5.12 The diagnostic index is closed form, so approximating it is a strict loss

`DiagnosticEngine.diagnose` computes `D: R^{<=196} -> [0,1]` in closed form: per-system
`fragility = criticality*(1-health)*(1-redundancy)`, an HHI `concentration` over outgoing
weights, a `feedback` term summing edge-weight products over simple cycles, blended at
`0.4/0.3/0.3` and aggregated as a criticality-weighted mean. Cost is
`O(|V| + |E| + sum over simple cycles)`; on 7 nodes it is microseconds.

**Proposition 5.13.** By Theorem 2.3 there exists a one-hidden-layer network approximating `D`
uniformly to any `eps > 0` on the compact cube; by Theorem 2.4 the `L^2` rate is `O(C_D^2/n)`.
Both are useless here. Approximating a function one already possesses exactly, using
parameters one cannot fit, is dominated in every respect — accuracy, cost, determinism,
auditability — by evaluating it. A network can therefore never be a *substitute* for AMF's
diagnosis.

**Corollary 5.13.1 (the only non-vacuous role for learning).** Learning could only be used to
*choose* the free constants that AMF currently fixes by fiat — the `0.4/0.3/0.3` diagnostic
blend, the `0.6/0.25/0.15` resilience blend, the `Severity` cut-points, the coefficients
`0.5/0.3/0.2` in `absorptive_capacity`, and the entries of `W`. Fitting them requires labelled
markets. None exist. This is the whole of the deep-learning question for AMF, and it is a data
question, not an architecture question.

### 5.13 The note's hybrid architecture, translated line by line

| Note's layer | Its stated role | AMF object that already plays it | What learning would add |
|---|---|---|---|
| `Transformer layer 1` → feature embeddings per asset | encode raw per-node data | `AnatomicalSystem` metrics with derived `health()` and `absorptive_capacity()` | a learned nonlinear re-encoding of four numbers; nothing without a fitting target |
| `GNN layer` → propagated risk across the system | one round of neighbourhood aggregation | one `ShockSimulator._advance` step (Theorem 5.3) | learned edge weights in place of the specified `W` (§5.7) |
| `LSTM layer` → temporal forecast + confidence | the recurrence over `t` | the unrolled simulator (Corollary 5.4); confidence from `ensemble()` | learned gates in place of fixed `rho`, `Theta`, and the cascade indicator (Corollary 5.7.1) |
| `Attention mechanism` → which assets/policies matter most | feature importance | `SensitivityAnalyzer`: exact finite-difference `gradient = index_delta / span` per `(system, metric)`, plus ranked `LeveragePoint`s | a *less* reliable answer — see below |

**Proposition 5.14 (on the last row).** `sensitivity.py` reports, for each of the 28
`(system, metric)` pairs, the actual change in the overall index under a `+/- step`
perturbation, with the traversed `span` reported alongside because the interval shrinks near a
bound. That is a directly interpretable counterfactual with a stated perturbation size.
Attention weights are not: [93] shows attention distributions frequently fail to correlate
with gradient-based importance and that adversarial distributions with different attention but
identical output exist; [94] argues the negative claim is over-stated but concedes attention
is not a *faithful* explanation without task-specific validation. On AMF's interpretability
axis the existing module strictly dominates, which is Rudin's [95] argument instantiated.

### 5.14 Reinforcement learning replaced by exhaustive deterministic search

The note proposes "Reinforcement learning: Learn optimal policy responses to shocks". AMF's
action space is already finite and small. An `Intervention` is
`(target: SystemKind, absorptive_boost: float in [0,1], at_step: int)`. On a grid of 11 boost
levels (`0.0, 0.1, ..., 1.0`) and 51 admissible steps (`0..max_steps`), the single-intervention
space has `7 * 11 * 51 = 3 927` elements. Each `propagate` costs at most
`51 * 7 * 7 ~ 2 500` multiply-adds, so exhaustive evaluation of every single intervention
against a fixed shock costs on the order of `10^7` operations — trivially feasible in pure
Python, exactly deterministic, and it returns the *global* optimum rather than a policy that
approximates one.

**Proposition 5.15.** For `k = 1`, exhaustive search dominates any learned policy: it is
exact, deterministic, dependency-free, and auditable. For `k = 2` the space is
`C(3927, 2) ~ 7.7 * 10^6` pairs and exhaustive search is no longer cheap; a documented
deterministic greedy or beam extension (fixed width, fixed tie-break by `SystemKind`
declaration order) is the in-boundary answer. Reinforcement learning becomes attractive only
when the action space is large *and* the environment is not simulable — AMF's is small and
fully simulable, so the premise of the method fails.

**Corollary 5.15.1.** This generalises `LeveragePoint` from static metric adjustments to timed
interventions, uses the existing `Intervention` type, adds no dependency, and introduces no
learned parameter. It is the compliant version of the note's fourth training strategy.

### 5.15 Probabilistic heads and the missing observable

DeepAR [71] fits a likelihood by NLL; TFT [72] fits quantiles by pinball loss; both are proper
scoring rules (Definition 2.53) and both require realised observations `y`.
`ShockSimulator.ensemble` already produces a predictive spread — `ResilienceDistribution` with
`MetricStats` over `value`, `amplification_factor`, `peak_stress` and `absorbed_fraction`,
percentiles by linear interpolation, replication `i` seeded at `base_seed + i`.

**Proposition 5.16.** No proper scoring rule can be evaluated on AMF's ensemble, because there
is no realised `y`. The ensemble spread is a statement about the *jitter distribution* the
user supplied, not about uncertainty in any market. Consequently: (i) the note's "Output:
Price forecast + uncertainty band" reduces, in-boundary, to an object AMF already has; (ii)
any calibration language attached to it ([92], Remark 2.56) would be a rule-2 violation; and
(iii) the correct docstring register is the one `Sensitivity` already uses — "describes the
model's local behaviour around the market as supplied".

### 5.16 Determinism requirements for any implementation

If any of §5 were implemented in `src/amf`, the following are load-bearing, not stylistic.

1. **No learned weights.** Any weight that is not a checked-in constant makes the output
   depend on a training run. If constants are checked in, they must be exact decimal literals,
   not the result of a fit performed at import time.
2. **Fixed summation arrangement.** Every aggregation must iterate in `SystemKind` declaration
   order and, for edges, in `(source, target, kind)` declaration order. Floating-point addition
   is not associative [123], and `tests/unit/test_properties.py` asserts that a market and any
   permutation of it diagnose identically — a matrix-multiplication routine that reorders
   accumulation will fail that test correctly.
3. **No `exp`/`softmax` without a fixed reduction.** `softmax` requires a max-subtraction for
   stability and a summation whose arrangement is fixed; both must be explicit.
4. **No dropout, no batch statistics.** Definitions 2.16 and 2.17 both make an output depend
   on something other than its own input. Layer normalisation (2.18) is admissible.
5. **No adaptive stopping.** Any iterative routine needs a documented absolute tolerance plus a
   hard iteration cap, both `InvalidConfigError`-validated, exactly as
   `DependencyGraph.centrality` already does.
6. **Fixed precision.** Python floats are IEEE-754 binary64 throughout; no float32 path, no
   BLAS, no fused multiply-add.
7. **Seeds.** Any stochastic element must be gated behind an explicit seed, as
   `SimulationConfig.jitter` already is.
8. **Pure Python.** Rule 3 forbids runtime dependencies, so a network in `src/amf` would be
   nested `math` loops. That is feasible for a `7 x 7 x d` model and absurd for anything
   larger — which is itself the argument for the out-of-tree sidecar of §6.

---
## 6. Repository governance and boundary analysis

Every artefact, formula and phrase the source note proposes is reproduced below and annotated.
Nothing is silently dropped and nothing is silently accepted.

| Proposed artefact / formula / phrase | Conflicts with which hard rule | Compliant reformulation |
|---|---|---|
| `docs/research/deep_learning_market_architectures.md` — Architecture comparison | None directly. Must **not** be added to `SHA256SUMS` (rule 4) and must carry the illustrative-only banner (rule 2) | Keep, or fold into this module. If kept, place under `docs/`, ensure the `validate` job's Markdown link check covers it, and open with the status banner used here |
| `src/amf/ml/transformer_market_model.py` — Transformer implementation | **Rule 1** in the name (`market_model` is fine, but the file's stated content is a model over prices) and in every plausible member (`price_embedding`, `attention_over_prices`). **Rule 3** three ways: `ml/` is a sub-package where the package is flat modules; a transformer needs tensor algebra the standard library does not provide; 100 % branch coverage of an attention implementation is achievable but every branch must be tested | Do not ship a transformer in-tree. If a *learned coupling* is genuinely wanted, ship `src/amf/coupling_gate.py` exposing a pure-`math`, per-edge sigmoid gate over the **existing** edge set with checked-in constants, plus `CouplingGateConfig` validated to `InvalidConfigError`. Anything larger belongs in the sidecar below |
| `src/amf/ml/graph_neural_network.py` — GNN for systemic risk | **Rule 3** (sub-package layout; runtime dependency if implemented with tensors). **Rule 2** in the phrase "for systemic risk", which asserts a validated capability | Nothing to ship: Theorem 5.3 shows `simulation.py` already contains the layer. If a *documented* re-presentation is wanted, add a docstring cross-reference in `ShockSimulator` naming the MPNN correspondence, and a `docs/` note. Zero new code |
| `src/amf/ml/hybrid_lstm_gnn.py` — Combined architecture | **Rule 3** (as above). **Rule 2**: the hybrid's claimed output is "Multi-asset predictions + confidence" | Corollary 5.4 plus §5.13: the hybrid, stripped of market data, *is* `ShockSimulator` + `SensitivityAnalyzer` + `ensemble()`. Ship no module; ship the translation table of §5.13 in `docs/` |
| `examples/ml_crisis_forecasting.py` — Test on historical data | **Rule 1** twice (`historical data` means price/return history; "forecasting" invites `signal`/`returns` naming). **Rule 2** outright: forecasting crises is a validated-performance claim. **Rule 3**: `tests/integration/test_examples.py` would need a case and the example would need to be deterministic and dependency-free | `examples/message_passing_view.py`: build the sample market in code, print the coupling matrix `W`, the derived matrix `B`, its row sums and spectral radius by power iteration with a fixed tolerance and cap, and the 1-WL colour refinement — then the standard disclaimer. No external data, deterministic output, add a case to `test_examples.py` |
| `src/amf/ml/` as a sub-package | **Rule 3** (the package is flat modules) and a rule 1 tripwire on member names | Flat modules only. See the naming table below |
| `Input: [price_t-n, ..., price_t, volume_t, sentiment_t, policy_t]` | **Rule 1** outright — `price` is `FORBIDDEN`, and volume/sentiment are market data AMF does not model | The 28-dimensional structural state `m_j = (integrity, redundancy, criticality, load)` over the seven systems (§5.1). "Policy" enters as `SystemKind.IMMUNE` metrics or as an `Intervention`, never as an exogenous series |
| `Attention: Q,K,V matrices learn which features interact` | **Rule 2**: "learn" presupposes a fitting target AMF does not have (Proposition 5.12) | State it as §5.7 does: attention *is* a learned `CouplingMatrix`; AMF specifies `W` instead. Then Proposition 5.8 explains why softmax is the wrong parameterisation even if a target existed |
| `Output: Price forecast + uncertainty band` | **Rule 1** (`price`) and **rule 2** (a forecast claim) | `ResilienceScore` plus `ResilienceDistribution` from `ensemble()`. Both exist; neither carries a forecast claim, and Proposition 5.16 says why no proper score can be attached |
| `Advantage: Parallel processing (fast)` / `Disadvantage: Sequential processing (slower)` | No rule conflict; but vacuous at AMF's scale | True for training over long sequences. At `n = 7` and `T = 50` the whole simulator is microseconds (§5.10); the parallelism argument does not apply |
| `Disadvantage: Black-box; hard to interpret "why"` | No rule conflict; correct, and the reason to keep AMF's closed forms | `SensitivityAnalyzer` already answers "why" exactly (§5.13, Proposition 5.14) |
| `Advantage: Interpretable gates (can see what model remembers)` | **Rule 2**: an interpretability claim that the literature contests | Restate as falsifiable proposition P9. [93], [94] and [95] are the required reading before this sentence is repeated anywhere in the repository |
| `Cell state: "Memory" of past events (e.g. "we're in crisis")` / `Hidden state: … "next tick likely up"` | **Rule 1** (`tick`-level direction is market data) and **rule 2** (a regime label and a directional forecast AMF neither defines nor estimates) | `SimulationTrace.steps` is the state trajectory; `ResilienceScore.tipped_systems` is the only regime-like object AMF defines, and it is an explicit threshold crossing, not an inferred label |
| `Nodes: {Equity, Credit, Forex, Commodity, Policy}` | Not a rule conflict, but a different model: AMF's nodes are the seven anatomical systems within **one** market, fixed by `SystemKind`, with the asset class recorded in `MarketBoundary.asset_class` | Cross-asset structure, if ever wanted, is several `Market` objects, not extra `SystemKind` members. Adding members changes `SHA256SUMS`-adjacent framework semantics and breaks the seven-system contract everywhere |
| `Edge features: [correlation, lag-lead relationship, shock direction]` | **Rule 1** for `correlation` and `lag-lead` (both are functions of return series). `shock direction` is already modelled | `DependencyKind` in `{structural, informational, capital, regulatory}` plus `weight in (0,1]`. That *is* the edge-feature vector, and it round-trips through `to_dict`/`from_dict` |
| `Output: System-wide risk score + which node is vulnerable` | **Rule 2** in "risk score" | `DiagnosticReport.overall_index` and the ranked `single_points_of_failure`, both already present and both documented as structural, not predictive |
| `Advantage: Native model of systemic risk (contagion through graph)` | **Rule 2** outright — asserts a validated capability | Restate as P10. AMF's stress propagation is a *model of transmission*, deliberately not a claim that it matches any market |
| `Supervised: Predict next-period returns (minimize MSE/MAE)` | **Rule 1** (`returns` is `FORBIDDEN`) and **rule 2** (a forecast objective) | There is no supervised objective available (Proposition 5.12). If a fitting target is ever wanted, it must be a *stated structural* target with a stated generator, and the resulting numbers are facts about the generator |
| `Unsupervised: Anomaly detection (identify unusual market states)` | **Rule 2**: "unusual" is relative to a reference distribution AMF does not have | Admissible only in the explicit form: given a *user-supplied* population of markets, report the Mahalanobis-free, dependency-free distance of one market's 28-vector from that population's coordinatewise median. Documented as a statement about the supplied population |
| `Semi-supervised: Pre-train on market microstructure; fine-tune on crises` | **Rule 1** (microstructure and crisis data are market data) and **rule 2** | Drop. There is no in-boundary version |
| `Reinforcement learning: Learn optimal policy responses to shocks` | **Rule 2** ("optimal" without a validated objective) and **rule 3** (an RL loop is stochastic and would need a seed for every element) | §5.14: exhaustive deterministic search over the finite `Intervention` grid for `k = 1`, and a fixed-width deterministic beam for `k = 2`. Exact, seedless, dependency-free, and it returns the global optimum |
| `Research Leaders Needed: Machine learning engineer, financial ML specialist` | **Rule 2** exposure: a financial-ML specialist's default register is validated performance | See §9. The pair is necessary and not sufficient; a repository maintainer and a forecast-evaluation statistician are the two roles that keep the module inside the rules |

**Naming tripwires specific to this module.** `test_non_trading_boundary.py` walks public names
*and* members *and* dataclass fields, matching `FORBIDDEN` as a **substring**. The vocabulary of
this field is unusually dangerous:

| Natural name | Fails on | Use instead |
|---|---|---|
| `graph_signal`, `signal_propagation`, `SignalEncoder` | `signal` | `stress_field`, `propagation`, `StressEncoder` |
| `bias_variance_tradeoff`, `accuracy_tradeoff` | `trade` (substring of *tradeoff*) | `bias_variance_balance`, `accuracy_cost_balance` |
| `canonical_ordering`, `layer_order`, `hop_order`, `sort_order`, `reorder` | `order` | `arrangement`, `layer_index`, `hop_index`, `_ORDER` (module-private, therefore not walked) |
| `price_embedding`, `input_prices` | `price` | `metric_embedding`, `structural_inputs` |
| `predicted_returns`, `returns_head` | `returns` | `predicted_stress`, `stress_head` |
| `backtest_window` | `backtest` | not admissible in any form (rules 1 and 2) |

`CouplingMatrix.order` is the single documented `ALLOWLIST` entry and must not be joined by
undocumented ones; a meta-test asserts every allowlist entry still exists.

### 6.1 Dependency implications

This is the decisive constraint. A transformer or a trained GNN needs dense linear algebra;
`numpy` alone would violate rule 3, and `torch` would add hundreds of megabytes and a
non-deterministic GPU path. Nothing in the source note's deliverables can be implemented
in-tree as specified.

Two admissible shapes:

1. **In-tree, no learning.** Everything in §5 that is *analysis* rather than *fitting* is pure
   `math`: the matrix `B` and its row sums, power iteration for `r(B)` with a fixed tolerance
   and cap, 1-WL colour refinement, the `A_hat` spectrum by cyclic Jacobi on a `7 x 7`
   symmetric matrix, and exhaustive intervention search. All of it is `O(n^3)` on `n = 7`.
   This is the recommended scope.
2. **Out-of-tree research sidecar.** A separate, clearly-marked, *not installed by default*
   repository or optional extra — `amf-research`, never `src/amf/ml/` — carrying the
   experimental architectures, their dependencies, and their own CI. It must not be importable
   from `amf`, must not appear in `pyproject.toml`'s runtime dependencies, and must carry the
   same licence and the same `Private :: Do Not Upload` posture. The dependency arrow points
   sidecar `->` `amf`, never the reverse, so the one-way layering of `errors`/`models` `->`
   `systems`/`graph` `->` `market` `->` `diagnostics`/`simulation` `->` `sensitivity` `->`
   `report`/`viz`/`cli` is untouched.

### 6.2 Determinism implications

§5.16 enumerates the eight requirements. Three deserve repeating at governance level. First,
`tests/unit/test_properties.py` asserts that a market and any permutation of it diagnose
identically; any matrix routine that accumulates in a different arrangement will break that in
the last bits, correctly. Second, power iteration and Jacobi would be the first iterative
numerical routines in `src/amf` after `DependencyGraph.centrality`; they must copy its
contract exactly — validated absolute tolerance, validated hard cap, `InvalidConfigError`.
Third, any trained weight is a hidden global input: two contributors running the same CLI on
the same market must get byte-identical output, which is impossible if the weights came from a
fit rather than from a literal.

### 6.3 Coverage implications

The gate is 100 % statement **and** branch coverage of `src/amf`. A training loop has branches
that only execute under conditions a unit test must manufacture — early stopping, gradient
clipping thresholds, NaN guards, learning-rate schedule boundaries. Each is a branch, each
needs a test, and several are only reachable with contrived inputs. The analysis-only scope of
option 1 above has no such branches: power iteration has exactly three (converged, exhausted,
zero vector), all trivially reachable.

### 6.4 Validation-claim implications

Nothing in §5 is calibrated against anything. The identity of Theorem 5.3 is a fact about the
code, not about markets; `r(B) = 0.582613` is a fact about one JSON file. Neural-network
vocabulary carries an unearned authority that makes over-reading easy, so the following are
rule-2 violations however they are dressed: *"the GNN detects contagion"*, *"attention shows
which system matters"*, *"the model forecasts systemic stress"*, *"trained on historical
crises"*, *"achieves X % accuracy"*. The permitted register is the one §5 uses throughout:
*this market, this file, this matrix, this number, this proof.*

### 6.5 A byte-level caveat on §1

The `trailing-whitespace` pre-commit hook applies to everything except the four
checksum-protected artifacts, so trailing spaces inside the quoted block of §1 are stripped on
commit. The quotation is word-exact, bullet-exact, formula-exact and path-exact; it is not
byte-exact in trailing whitespace, and the difference is invisible inside a fenced block. This
is recorded rather than worked around: adding an exclusion for `docs/discussions/**` would
weaken a hygiene hook for a cosmetic gain.

### 6.6 Private-distribution implications

Rule 4 forbids publishing to PyPI or any public index, and `RELEASING.md` notes that the
repository is public, so a GitHub Release asset or an Actions artifact is *not* a private
channel. Trained model weights are a distributable artefact of exactly that kind. Any sidecar
must therefore never attach weights to a Release, upload them as a CI artifact, or commit them
to the public tree.

---
## 7. Falsifiable propositions and open questions

The source note for D1 has no "Key Research Questions" heading — unlike its quantum siblings,
its research programme is stated implicitly in the three "Advantage / Disadvantage" pairs, the
"Key Innovation: Hybrid Architecture" block, and the four "Training Strategy" bullets. Those
implicit claims are restated below in refutable form as P1–P8; P9–P16 extend them. Each names
the evidence that would settle it.

**P1 (the simulator step is an MPNN layer).** *Claim (Theorem 5.3):* under the documented
defaults, `ShockSimulator._advance` computes exactly `phi(Theta*rho*x_j + Theta*tau*(1-a_j) *
sum_i W[i][j]*x_i)` for every `j`. *Falsifier:* any market and any default-configuration step
where the two differ by more than floating-point noise. This is the cheapest test in the
module and should be written first; it is a pure identity and belongs in
`tests/unit/test_simulation.py`.

**P2 (the network has zero parameters).** *Claim (Corollary 5.4):* the unrolled simulator's
learnable-parameter count is `0`; every constant in the recurrence is either a
`SimulationConfig` field or a function of the market. *Falsifier:* a quantity in
`simulation.py` that is neither.

**P3 (the sample market contracts).** *Claim (Fact 5.5.1):* for
`examples/sample_market.json` under defaults, `||B||_inf = 0.933300`, `||B||_1 = 0.941800`,
and `r(B) = 0.582613` to six places. *Falsifier:* an independent computation disagreeing
beyond `1e-6`.

**P4 (contraction is not guaranteed).** *Claim (Proposition 5.6):* there is an admissible
market with `r(B) >= 5.525`. *Falsifier:* a proof that `systems.py` validation forbids
`redundancy = integrity = 0, load = 1`, or that `graph.py` forbids all 42 ordered pairs at
weight `1.0`. Neither holds, so P4 is expected to survive; it is stated because it makes
CLAUDE.md's warning about non-contraction precise and testable.

**P5 (expressivity is not the binding constraint).** *Claim (Proposition 5.9):* 1-WL from
constant colours separates all seven systems of the sample market in two rounds; with
`SystemKind` labels it separates them in zero. *Falsifier:* a market whose dependency graph has
two systems 1-WL cannot separate *and* whose node features are identical — the second
conjunct is impossible while `SystemKind` is part of the state, which is the point.

**P6 (the depth window is narrow).** *Claim (Proposition 5.10):* the sample market's undirected
diameter is `4` and `|lambda_2(A_hat)| = 0.862365`, so a GCN deep enough to cover the graph has
already contracted the non-dominant component to `0.553`. *Falsifier:* a recomputation of the
diameter or the spectrum disagreeing.

**P7 (softmax attention cannot express AMF's couplings).** *Claim (Proposition 5.8):* no
softmax self-attention matrix reproduces the sample market's `W`, because `W` has two
identically-zero rows and non-unit row masses. *Falsifier:* a finite `Q, K` producing an exact
zero entry, which contradicts strict positivity of `exp`. Expected to survive; the useful
consequence is Corollary 5.8.1, that GAT-style masked attention is the only admissible form.

**P8 (attention costs less than the projections at `n = 7`).** *Claim (§5.10):* at `n = 7`,
`d = 64` the score matrix is 2.66 % of a layer's multiply-accumulates. *Falsifier:* a
measurement on a concrete implementation showing the quadratic term dominating — which would
require `n > d/4`, i.e. `n > 16` at `d = 64`.

**P9 (gates are not automatically interpretable).** *The note claims:* "Advantage:
Interpretable gates (can see what model remembers)." *Refutable form:* on any AMF-derived task,
the ranking of systems by LSTM forget-gate magnitude agrees with the ranking by exact
finite-difference sensitivity (Spearman `> 0.8`). *Falsifier:* it does not, which is the
outcome [93] reports for attention weights and [94] declines to overturn.

**P10 (a GNN is a "native model of systemic risk").** *The note claims* the GNN's advantage is
"Native model of systemic risk (contagion through graph)". *Refutable form:* a GNN trained on
markets sampled from AMF's own generator recovers `DiagnosticReport.overall_index` to within
`1e-3` on held-out samples. *Falsifier:* it does not. *Important:* even if it succeeds, the
result is a statement about AMF's generator, not about markets — and it is strictly worse than
calling `diagnose()` (Proposition 5.13).

**P11 (learned structure recovers specified structure).** *The note claims* the GNN's
disadvantage is that "Graph structure must be pre-specified (or learned)". *Refutable form:*
from an ensemble of stress trajectories generated by a known `W`, a per-edge sigmoid gate
fitted by least squares recovers `W` to within `0.05` per entry. *Falsifier:* it does not, or
it does only when the number of trajectories exceeds the number of free edges by a factor the
repository cannot supply.

**P12 (the linear baseline is not beaten).** *Refutable form:* on markets sampled from AMF's
own generator with a fixed seed, no deep architecture predicts `overall_index` better than
ridge regression on the raw 196-vector by more than the seed-to-seed standard deviation.
*Falsifier:* a deep model that does, reported with the seed sweep. This is Result 2.57
transposed, and it is the single most useful experiment anyone could run for this discussion.

**P13 (exhaustive search dominates a learned policy).** *Refutable form (Proposition 5.15):*
for `k = 1` interventions, exhaustive evaluation over the `7 x 11 x 51` grid returns the global
optimum in under one second of pure Python and is bit-reproducible. *Falsifier:* a timing
measurement showing otherwise, or an RL policy that finds a *better* single intervention —
impossible by construction, since the search is exhaustive.

**P14 (residual connections are load-bearing on a 7-node graph).** *Refutable form:* a 4-layer
GCN without residual connections, applied to the sample market, produces node representations
whose pairwise cosine distances are all below `0.15`; the same network with GCNII-style initial
residual does not. *Falsifier:* the distances do not collapse, which would contradict
Theorem 2.47's rate at `|lambda_2| = 0.862365`.

**P15 (jitter ensembles are not calibrated uncertainty).** *Refutable form (Proposition 5.16):*
there exists no realised observable in the repository against which
`ResilienceDistribution`'s percentiles can be scored by any proper scoring rule. *Falsifier:*
exhibiting one. Producing such an observable would be the largest single change in the
repository's epistemic status, and it would have to survive rule 1.

**P16 (open).** Could a labelled corpus of markets exist *at all* that is compatible with rules
1 and 2 — that is, a population of AMF markets with an attached structural outcome that is
neither a price, a return, nor an expert's post-hoc label? The honest current answer is that
nobody knows, and a negative answer would settle this entire discussion more decisively than
any architecture comparison. Candidate directions worth exactly one paragraph each in a follow-
up: infrastructure-outage records as `skeleton` integrity events; published venue-outage
post-mortems as `SPOF` ground truth; regulatory enforcement counts as `immune` load. Each
would need its own boundary review before a single byte is written.

---

## 8. Deliverables

The source note's deliverable list, reproduced exactly as written, with compliance status.

| Deliverable (verbatim) | Status | Compliance note |
|---|---|---|
| `docs/research/deep_learning_market_architectures.md` — Architecture comparison | **Accept with conditions** | Not to be added to `SHA256SUMS`; must carry the illustrative-only banner; must be reachable by the `validate` job's Markdown link check. Superseded in practice by this module, whose §2 and §5.13 are the architecture comparison |
| `src/amf/ml/transformer_market_model.py` — Transformer implementation | **Reject in-tree** | `ml/` violates the flat-module layout; a transformer violates the zero-runtime-dependency rule; the stated inputs (`price`, `volume`, `sentiment`) violate the non-trading boundary; and Proposition 5.8 shows softmax attention cannot even represent an AMF coupling matrix. If pursued, it belongs in the out-of-tree `amf-research` sidecar (§6.1) |
| `src/amf/ml/graph_neural_network.py` — GNN for systemic risk | **Reject as redundant** | Theorem 5.3: `simulation.py` already implements the layer, with zero parameters and full determinism. The compliant deliverable is documentation, not code — a docstring cross-reference in `ShockSimulator` plus §5.3–§5.4 of this module |
| `src/amf/ml/hybrid_lstm_gnn.py` — Combined architecture | **Reject as redundant** | Corollary 5.4 and the translation table of §5.13: the hybrid's four layers map onto `AnatomicalSystem`, `_advance`, the unrolled recurrence, and `SensitivityAnalyzer`, all of which exist |
| `examples/ml_crisis_forecasting.py` — Test on historical data | **Reject** | Historical market data violates rule 1; "crisis forecasting" violates rule 2. Replace with `examples/message_passing_view.py` (§6 table) and add a case to `tests/integration/test_examples.py` |

Additional deliverables this module recommends, none of which appear in the source note:

| Deliverable | Rationale |
|---|---|
| `tests/unit/test_simulation.py::test_advance_is_a_message_passing_layer` asserting P1 as an exact identity | The cheapest possible confirmation that the analytical description in the docs matches the code |
| `src/amf/spectral.py` — pure-`math` `propagation_matrix(market, config)`, `spectral_radius(matrix, tolerance, max_iterations)`, `SpectralConfig` validated to `InvalidConfigError` | Makes Fact 5.5.1 computable from the CLI; three branches, all reachable; no dependency; deterministic given a fixed arrangement and cap |
| `amf spectral <market.json>` reporting `||B||_inf`, `||B||_1`, `r(B)`, and whether the step map contracts | One number that tells a reader whether a `simulate` run will settle at all — currently discoverable only by running it |
| Exhaustive single-`Intervention` search (§5.14) as `sensitivity.py`'s timed analogue of `LeveragePoint` | Replaces the note's reinforcement-learning bullet with an exact, deterministic, dependency-free global optimum |
| A `CONTRIBUTING.md` note recording the naming tripwires of §6 (`signal`, *trade*off, *order*ing) | The three substrings most likely to fail `test_non_trading_boundary.py` for anyone working in this vocabulary |
| A CHANGELOG entry under `## [Unreleased]` → *Added* | Required by the contributor checklist for any user-visible change |
| An `amf-research` sidecar skeleton — separate repository, own CI, `Private :: Do Not Upload`, no weights in any Release asset (§6.6) | The only place the note's three model files can legally and technically live |

---

## 9. Research leadership and prerequisites

The source note's line, verbatim:

> **Research Leaders Needed**: Machine learning engineer, financial ML specialist

Both are necessary. Neither is sufficient, and the second is the role most likely to import a
rule-2 violation, because validated out-of-sample performance is the currency of that field and
AMF has no sample. A skills matrix that would actually staff this module:

| Role | Must be able to | Owns which sections | Failure mode if absent |
|---|---|---|---|
| Machine learning engineer | Derive backpropagation for a 2-layer network by hand; state Theorem 2.24 with its hypotheses; implement scaled dot-product attention from Definition 2.29 without a framework | §2.1–§2.7, §5.7 | A transformer proposed for a 7-token sequence, with an efficient-attention variant attached (§5.10) |
| Graph-learning researcher | Run 1-WL by hand; state the GIN condition of Theorem 2.45; explain over-smoothing in terms of `|lambda_2|` | §2.8–§2.11, §5.8–§5.9 | Higher-order GNNs proposed to fix an expressivity problem that does not exist (Corollary 5.9.1) |
| Numerical analyst / linear algebraist | Spectral radius versus induced norms; power iteration with a fixed stopping rule; floating-point non-associativity | §5.5, §5.6, §5.16, §6.2 | A spectral radius that differs in the last bits between CI runners, breaking the permutation-invariance property test |
| Forecast-evaluation statistician | Distinguish proper from improper scores; know what MASE fixes about MAPE; run a Diebold–Mariano test and say when it is invalid | §2.13, §5.15, P12, P15 | An "uncertainty band" reported as calibrated with nothing to calibrate against |
| Financial ML specialist | Know [99], [100], [101] and the multiple-testing arithmetic; recite the M4/M5 outcomes without prompting | §4.5, §2.14, P12 | Historical crisis "validation", which is rule 1 and rule 2 simultaneously |
| Interpretability researcher | State what [93] actually showed and what [94] conceded; argue [95]'s position | §5.13, P9 | "Attention shows which system matters" shipped as a feature |
| Repository maintainer | Know the `FORBIDDEN` list, the single `ALLOWLIST` entry, the one-way dependency layering, the 100 % branch gate, and `RELEASING.md` | §6, §8 | A PR that fails `test_non_trading_boundary.py` on the word *trade*off, or a Release asset carrying model weights |

**Prerequisite ladder, undergraduate to frontier.**

1. *UG2* — Linear algebra: eigenvalues, induced norms, spectral radius. MIT 18.06; [121] Ch. 5.
   Needed for anything in §5.5 onward.
2. *UG3* — Probability and statistical learning: empirical risk, the estimation/approximation
   split. [110] Ch. 2, 7; [111] Ch. 2–6. This is the rung at which Proposition 5.12 becomes
   obvious rather than surprising.
3. *UG4* — Feedforward networks and backpropagation. [104] Ch. 6; MIT 6.S191 or CMU 11-785.
4. *PG1* — Optimisation for deep learning, including Theorem 2.14. [104] Ch. 8; [19]; Berkeley
   CS182.
5. *PG1* — Recurrence, BPTT, gating. [104] Ch. 10; [30], [31], [33]. Required to read §5.5–§5.6
   as anything more than matrix arithmetic.
6. *PG1* — Attention and the transformer. [38]; Stanford CS224n; [109] Ch. 12.
7. *PG1* — Spectral graph theory: the normalised Laplacian and its spectrum. [118] Ch. 1–2.
8. *PG2* — Graph representation learning: ChebNet, GCN, GraphSAGE, GAT, MPNN. Stanford CS224W;
   [112] Ch. 5–6.
9. *PG2* — GNN theory: the WL ceiling, over-smoothing, over-squashing. [112] Ch. 7; [58], [61],
   [62]. Required to read §5.8–§5.9.
10. *PG2* — Forecast evaluation and proper scoring. [87], [88], [89]. The rung most often
    skipped and the one that prevents the module's most likely rule-2 violation.
11. *PG3* — Geometric deep learning as the unifying frame. [66] Ch. 3–5. This is what turns
    §5.13's table from an analogy into a statement about symmetry groups.
12. *PG3* — The critical literature on machine learning in markets. [99]–[103], and the M
    competitions [79]–[81]. Calibration of expectation; the sceptical prior this module adopts.
13. *Frontier* — P16: whether a rule-1-compatible labelled corpus of markets can exist at all.
    Nobody currently knows, and a well-argued negative answer would be worth more to this
    repository than any of the note's five deliverables.

A contributor who has completed rungs 1–9 can verify every claim in §5. A contributor who stops
at rung 6 will propose the transformer of the source note and will be wrong for the reason in
Proposition 5.8. A contributor who skips rung 10 will attach a confidence interval to an
unobservable and will be wrong for the reason in Proposition 5.16.

---
## References

Identifiers (DOI, arXiv id, volume, pages) are given only where confirmed; where a detail could
not be confirmed it is omitted rather than guessed.

- [1] G. Cybenko, "Approximation by superpositions of a sigmoidal function", *Mathematics of
  Control, Signals and Systems* **2**(4), 303–314 (1989).
- [2] K. Hornik, M. Stinchcombe and H. White, "Multilayer feedforward networks are universal
  approximators", *Neural Networks* **2**(5), 359–366 (1989).
- [3] K. Hornik, "Approximation capabilities of multilayer feedforward networks", *Neural
  Networks* **4**(2), 251–257 (1991).
- [4] M. Leshno, V. Y. Lin, A. Pinkus and S. Schocken, "Multilayer feedforward networks with a
  nonpolynomial activation function can approximate any function", *Neural Networks* **6**(6),
  861–867 (1993).
- [5] A. R. Barron, "Universal approximation bounds for superpositions of a sigmoidal function",
  *IEEE Transactions on Information Theory* **39**(3), 930–945 (1993).
- [6] R. Eldan and O. Shamir, "The power of depth for feedforward neural networks", *Proceedings
  of the 29th Conference on Learning Theory (COLT)*, PMLR **49**, 907–940 (2016).
- [7] M. Telgarsky, "Benefits of depth in neural networks", *Proceedings of the 29th Conference
  on Learning Theory (COLT)*, PMLR **49**, 1517–1539 (2016).
- [8] A. L. Blum and R. L. Rivest, "Training a 3-node neural network is NP-complete", *Neural
  Networks* **5**(1) (1992).
- [9] C. Zhang, S. Bengio, M. Hardt, B. Recht and O. Vinyals, "Understanding deep learning
  requires rethinking generalization", *International Conference on Learning Representations
  (ICLR)* (2017).
- [10] M. Belkin, D. Hsu, S. Ma and S. Mandal, "Reconciling modern machine-learning practice and
  the classical bias–variance trade-off", *Proceedings of the National Academy of Sciences*
  **116**(32), 15849–15854 (2019).
- [11] H. Robbins and S. Monro, "A stochastic approximation method", *The Annals of Mathematical
  Statistics* **22**(3), 400–407 (1951).
- [12] B. T. Polyak, "Some methods of speeding up the convergence of iteration methods", *USSR
  Computational Mathematics and Mathematical Physics* **4**(5), 1–17 (1964).
- [13] Y. Nesterov, "A method for solving the convex programming problem with convergence rate
  O(1/k^2)", *Doklady Akademii Nauk SSSR* **269** (1983).
- [14] D. E. Rumelhart, G. E. Hinton and R. J. Williams, "Learning representations by
  back-propagating errors", *Nature* **323**, 533–536 (1986).
- [15] J. Duchi, E. Hazan and Y. Singer, "Adaptive subgradient methods for online learning and
  stochastic optimization", *Journal of Machine Learning Research* **12**, 2121–2159 (2011).
- [16] D. P. Kingma and J. Ba, "Adam: A method for stochastic optimization", *International
  Conference on Learning Representations (ICLR)* (2015); arXiv:1412.6980.
- [17] S. J. Reddi, S. Kale and S. Kumar, "On the convergence of Adam and beyond",
  *International Conference on Learning Representations (ICLR)* (2018).
- [18] I. Loshchilov and F. Hutter, "Decoupled weight decay regularization", *International
  Conference on Learning Representations (ICLR)* (2019).
- [19] L. Bottou, F. E. Curtis and J. Nocedal, "Optimization methods for large-scale machine
  learning", *SIAM Review* **60**(2), 223–311 (2018).
- [20] N. Srivastava, G. Hinton, A. Krizhevsky, I. Sutskever and R. Salakhutdinov, "Dropout: A
  simple way to prevent neural networks from overfitting", *Journal of Machine Learning
  Research* **15**, 1929–1958 (2014).
- [21] S. Ioffe and C. Szegedy, "Batch normalization: Accelerating deep network training by
  reducing internal covariate shift", *Proceedings of the 32nd International Conference on
  Machine Learning (ICML)*, PMLR **37**, 448–456 (2015).
- [22] J. L. Ba, J. R. Kiros and G. E. Hinton, "Layer normalization", arXiv:1607.06450 (2016).
- [23] K. He, X. Zhang, S. Ren and J. Sun, "Deep residual learning for image recognition",
  *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 770–778 (2016).
- [24] S. Santurkar, D. Tsipras, A. Ilyas and A. Madry, "How does batch normalization help
  optimization?", *Advances in Neural Information Processing Systems (NeurIPS) 31* (2018).
- [25] R. Xiong, Y. Yang, D. He, K. Zheng, S. Zheng, C. Xing, H. Zhang, Y. Lan, L. Wang and
  T.-Y. Liu, "On layer normalization in the transformer architecture", *Proceedings of the 37th
  International Conference on Machine Learning (ICML)*, PMLR **119** (2020).
- [26] J. L. Elman, "Finding structure in time", *Cognitive Science* **14**(2), 179–211 (1990).
- [27] P. J. Werbos, "Backpropagation through time: what it does and how to do it",
  *Proceedings of the IEEE* **78**(10), 1550–1560 (1990).
- [28] S. Hochreiter, *Untersuchungen zu dynamischen neuronalen Netzen*, Diploma thesis,
  Institut für Informatik, Technische Universität München (1991).
- [29] Y. Bengio, P. Simard and P. Frasconi, "Learning long-term dependencies with gradient
  descent is difficult", *IEEE Transactions on Neural Networks* **5**(2), 157–166 (1994).
- [30] S. Hochreiter and J. Schmidhuber, "Long short-term memory", *Neural Computation*
  **9**(8), 1735–1780 (1997).
- [31] F. A. Gers, J. Schmidhuber and F. Cummins, "Learning to forget: Continual prediction with
  LSTM", *Neural Computation* **12**(10), 2451–2471 (2000).
- [32] R. Pascanu, T. Mikolov and Y. Bengio, "On the difficulty of training recurrent neural
  networks", *Proceedings of the 30th International Conference on Machine Learning (ICML)*,
  PMLR **28** (2013).
- [33] K. Cho, B. van Merriënboer, C. Gulcehre, D. Bahdanau, F. Bougares, H. Schwenk and
  Y. Bengio, "Learning phrase representations using RNN encoder–decoder for statistical machine
  translation", *Proceedings of the 2014 Conference on Empirical Methods in Natural Language
  Processing (EMNLP)*, 1724–1734 (2014).
- [34] J. Chung, C. Gulcehre, K. Cho and Y. Bengio, "Empirical evaluation of gated recurrent
  neural networks on sequence modeling", arXiv:1412.3555 (2014).
- [35] K. Greff, R. K. Srivastava, J. Koutník, B. R. Steunebrink and J. Schmidhuber, "LSTM: A
  search space odyssey", *IEEE Transactions on Neural Networks and Learning Systems* **28**(10),
  2222–2232 (2017).
- [36] D. Bahdanau, K. Cho and Y. Bengio, "Neural machine translation by jointly learning to
  align and translate", *International Conference on Learning Representations (ICLR)* (2015);
  arXiv:1409.0473.
- [37] M.-T. Luong, H. Pham and C. D. Manning, "Effective approaches to attention-based neural
  machine translation", *Proceedings of the 2015 Conference on Empirical Methods in Natural
  Language Processing (EMNLP)* (2015).
- [38] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser and
  I. Polosukhin, "Attention is all you need", *Advances in Neural Information Processing Systems
  (NIPS) 30* (2017).
- [39] P. Shaw, J. Uszkoreit and A. Vaswani, "Self-attention with relative position
  representations", *Proceedings of NAACL-HLT 2018* (2018).
- [40] J. Su, M. Ahmed, Y. Lu, S. Pan, W. Bo and Y. Liu, "RoFormer: Enhanced transformer with
  rotary position embedding", *Neurocomputing* **568**, 127063 (2024); arXiv:2104.09864.
- [41] A. F. T. Martins and R. F. Astudillo, "From softmax to sparsemax: A sparse model of
  attention and multi-label classification", *Proceedings of the 33rd International Conference
  on Machine Learning (ICML)*, PMLR **48** (2016).
- [42] R. Child, S. Gray, A. Radford and I. Sutskever, "Generating long sequences with sparse
  transformers", arXiv:1904.10509 (2019).
- [43] A. Katharopoulos, A. Vyas, N. Pappas and F. Fleuret, "Transformers are RNNs: Fast
  autoregressive transformers with linear attention", *Proceedings of the 37th International
  Conference on Machine Learning (ICML)*, PMLR **119** (2020).
- [44] S. Wang, B. Z. Li, M. Khabsa, H. Fang and H. Ma, "Linformer: Self-attention with linear
  complexity", arXiv:2006.04768 (2020).
- [45] K. Choromanski, V. Likhosherstov, D. Dohan, X. Song, A. Gane, T. Sarlós, P. Hawkins,
  J. Davis, A. Mohiuddin, Ł. Kaiser, D. Belanger, L. Colwell and A. Weller, "Rethinking
  attention with Performers", *International Conference on Learning Representations (ICLR)*
  (2021).
- [46] Y. Tay, M. Dehghani, D. Bahri and D. Metzler, "Efficient transformers: A survey", *ACM
  Computing Surveys* **55**(6), Article 109 (2022).
- [47] B. Weisfeiler and A. A. Leman, "The reduction of a graph to canonical form and the algebra
  which appears therein", *Nauchno-Technicheskaya Informatsia*, Series 2, No. 9, 12–16 (1968).
- [48] M. Gori, G. Monfardini and F. Scarselli, "A new model for learning in graph domains",
  *IEEE International Joint Conference on Neural Networks (IJCNN)* (2005).
- [49] F. Scarselli, M. Gori, A. C. Tsoi, M. Hagenbuchner and G. Monfardini, "The graph neural
  network model", *IEEE Transactions on Neural Networks* **20**(1), 61–80 (2009).
- [50] J. Bruna, W. Zaremba, A. Szlam and Y. LeCun, "Spectral networks and locally connected
  networks on graphs", *International Conference on Learning Representations (ICLR)* (2014).
- [51] D. K. Hammond, P. Vandergheynst and R. Gribonval, "Wavelets on graphs via spectral graph
  theory", *Applied and Computational Harmonic Analysis* **30**(2), 129–150 (2011).
- [52] D. I. Shuman, S. K. Narang, P. Frossard, A. Ortega and P. Vandergheynst, "The emerging
  field of signal processing on graphs", *IEEE Signal Processing Magazine* **30**(3), 83–98
  (2013).
- [53] M. Defferrard, X. Bresson and P. Vandergheynst, "Convolutional neural networks on graphs
  with fast localized spectral filtering", *Advances in Neural Information Processing Systems
  (NIPS) 29* (2016).
- [54] T. N. Kipf and M. Welling, "Semi-supervised classification with graph convolutional
  networks", *International Conference on Learning Representations (ICLR)* (2017).
- [55] W. L. Hamilton, R. Ying and J. Leskovec, "Inductive representation learning on large
  graphs", *Advances in Neural Information Processing Systems (NIPS) 30* (2017).
- [56] P. Veličković, G. Cucurull, A. Casanova, A. Romero, P. Liò and Y. Bengio, "Graph attention
  networks", *International Conference on Learning Representations (ICLR)* (2018).
- [57] J. Gilmer, S. S. Schoenholz, P. F. Riley, O. Vinyals and G. E. Dahl, "Neural message
  passing for quantum chemistry", *Proceedings of the 34th International Conference on Machine
  Learning (ICML)*, PMLR **70**, 1263–1272 (2017).
- [58] K. Xu, W. Hu, J. Leskovec and S. Jegelka, "How powerful are graph neural networks?",
  *International Conference on Learning Representations (ICLR)* (2019).
- [59] C. Morris, M. Ritzert, M. Fey, W. L. Hamilton, J. E. Lenssen, G. Rattan and M. Grohe,
  "Weisfeiler and Leman go neural: Higher-order graph neural networks", *Proceedings of the AAAI
  Conference on Artificial Intelligence* **33** (2019).
- [60] Q. Li, Z. Han and X.-M. Wu, "Deeper insights into graph convolutional networks for
  semi-supervised learning", *Proceedings of the AAAI Conference on Artificial Intelligence*
  **32** (2018).
- [61] K. Oono and T. Suzuki, "Graph neural networks exponentially lose expressive power for node
  classification", *International Conference on Learning Representations (ICLR)* (2020).
- [62] U. Alon and E. Yahav, "On the bottleneck of graph neural networks and its practical
  implications", *International Conference on Learning Representations (ICLR)* (2021).
- [63] J. Topping, F. Di Giovanni, B. P. Chamberlain, X. Dong and M. M. Bronstein,
  "Understanding over-squashing and bottlenecks on graphs via curvature", *International
  Conference on Learning Representations (ICLR)* (2022).
- [64] M. Chen, Z. Wei, Z. Huang, B. Ding and Y. Li, "Simple and deep graph convolutional
  networks", *Proceedings of the 37th International Conference on Machine Learning (ICML)*,
  PMLR **119** (2020).
- [65] M. M. Bronstein, J. Bruna, Y. LeCun, A. Szlam and P. Vandergheynst, "Geometric deep
  learning: going beyond Euclidean data", *IEEE Signal Processing Magazine* **34**(4), 18–42
  (2017).
- [66] M. M. Bronstein, J. Bruna, T. Cohen and P. Veličković, "Geometric deep learning: Grids,
  groups, graphs, geodesics, and gauges", arXiv:2104.13478 (2021).
- [67] Y. Li, R. Yu, C. Shahabi and Y. Liu, "Diffusion convolutional recurrent neural network:
  Data-driven traffic forecasting", *International Conference on Learning Representations
  (ICLR)* (2018).
- [68] B. Yu, H. Yin and Z. Zhu, "Spatio-temporal graph convolutional networks: A deep learning
  framework for traffic forecasting", *Proceedings of the 27th International Joint Conference on
  Artificial Intelligence (IJCAI)* (2018).
- [69] Z. Wu, S. Pan, G. Long, J. Jiang and C. Zhang, "Graph WaveNet for deep spatial-temporal
  graph modeling", *Proceedings of the 28th International Joint Conference on Artificial
  Intelligence (IJCAI)* (2019).
- [70] E. Rossi, B. Chamberlain, F. Frasca, D. Eynard, F. Monti and M. Bronstein, "Temporal graph
  networks for deep learning on dynamic graphs", arXiv:2006.10637 (2020).
- [71] D. Salinas, V. Flunkert, J. Gasthaus and T. Januschowski, "DeepAR: Probabilistic
  forecasting with autoregressive recurrent networks", *International Journal of Forecasting*
  **36**(3), 1181–1191 (2020).
- [72] B. Lim, S. Ö. Arık, N. Loeff and T. Pfister, "Temporal Fusion Transformers for
  interpretable multi-horizon time series forecasting", *International Journal of Forecasting*
  **37**(4), 1748–1764 (2021).
- [73] B. N. Oreshkin, D. Carpov, N. Chapados and Y. Bengio, "N-BEATS: Neural basis expansion
  analysis for interpretable time series forecasting", *International Conference on Learning
  Representations (ICLR)* (2020).
- [74] H. Zhou, S. Zhang, J. Peng, S. Zhang, J. Li, H. Xiong and W. Zhang, "Informer: Beyond
  efficient transformer for long sequence time-series forecasting", *Proceedings of the AAAI
  Conference on Artificial Intelligence* **35** (2021).
- [75] H. Wu, J. Xu, J. Wang and M. Long, "Autoformer: Decomposition transformers with
  auto-correlation for long-term series forecasting", *Advances in Neural Information Processing
  Systems (NeurIPS) 34* (2021).
- [76] Y. Nie, N. H. Nguyen, P. Sinthong and J. Kalagnanam, "A time series is worth 64 words:
  Long-term forecasting with transformers", *International Conference on Learning
  Representations (ICLR)* (2023).
- [77] A. Zeng, M. Chen, L. Zhang and Q. Xu, "Are transformers effective for time series
  forecasting?", *Proceedings of the AAAI Conference on Artificial Intelligence* **37**(9),
  11121–11128 (2023).
- [78] S. Smyl, "A hybrid method of exponential smoothing and recurrent neural networks for time
  series forecasting", *International Journal of Forecasting* **36**(1), 75–85 (2020).
- [79] S. Makridakis, E. Spiliotis and V. Assimakopoulos, "Statistical and machine learning
  forecasting methods: Concerns and ways forward", *PLoS ONE* **13**(3), e0194889 (2018).
- [80] S. Makridakis, E. Spiliotis and V. Assimakopoulos, "The M4 Competition: 100,000 time
  series and 61 forecasting methods", *International Journal of Forecasting* **36**(1), 54–74
  (2020).
- [81] S. Makridakis, E. Spiliotis and V. Assimakopoulos, "M5 accuracy competition: Results,
  findings, and conclusions", *International Journal of Forecasting* **38**(4), 1346–1364 (2022).
- [82] H. Hewamalage, C. Bergmeir and K. Bandara, "Recurrent neural networks for time series
  forecasting: Current status and future directions", *International Journal of Forecasting*
  **37**(1), 388–427 (2021).
- [83] L. Grinsztajn, E. Oyallon and G. Varoquaux, "Why do tree-based models still outperform
  deep learning on typical tabular data?", *Advances in Neural Information Processing Systems
  (NeurIPS) 35, Datasets and Benchmarks Track* (2022).
- [84] G. W. Brier, "Verification of forecasts expressed in terms of probability", *Monthly
  Weather Review* **78**(1), 1–3 (1950).
- [85] J. E. Matheson and R. L. Winkler, "Scoring rules for continuous probability
  distributions", *Management Science* **22**(10), 1087–1096 (1976).
- [86] R. Koenker and G. Bassett Jr., "Regression quantiles", *Econometrica* **46**(1), 33–50
  (1978).
- [87] T. Gneiting and A. E. Raftery, "Strictly proper scoring rules, prediction, and
  estimation", *Journal of the American Statistical Association* **102**(477), 359–378 (2007).
- [88] R. J. Hyndman and A. B. Koehler, "Another look at measures of forecast accuracy",
  *International Journal of Forecasting* **22**(4), 679–688 (2006).
- [89] F. X. Diebold and R. S. Mariano, "Comparing predictive accuracy", *Journal of Business &
  Economic Statistics* **13**(3), 253–263 (1995).
- [90] Y. Gal and Z. Ghahramani, "Dropout as a Bayesian approximation: Representing model
  uncertainty in deep learning", *Proceedings of the 33rd International Conference on Machine
  Learning (ICML)*, PMLR **48** (2016).
- [91] B. Lakshminarayanan, A. Pritzel and C. Blundell, "Simple and scalable predictive
  uncertainty estimation using deep ensembles", *Advances in Neural Information Processing
  Systems (NIPS) 30* (2017).
- [92] C. Guo, G. Pleiss, Y. Sun and K. Q. Weinberger, "On calibration of modern neural
  networks", *Proceedings of the 34th International Conference on Machine Learning (ICML)*,
  PMLR **70** (2017).
- [93] S. Jain and B. C. Wallace, "Attention is not explanation", *Proceedings of NAACL-HLT 2019*
  (2019).
- [94] S. Wiegreffe and Y. Pinter, "Attention is not not explanation", *Proceedings of the 2019
  Conference on Empirical Methods in Natural Language Processing and the 9th International Joint
  Conference on Natural Language Processing (EMNLP-IJCNLP)* (2019).
- [95] C. Rudin, "Stop explaining black box machine learning models for high stakes decisions and
  use interpretable models instead", *Nature Machine Intelligence* **1**, 206–215 (2019).
- [96] E. F. Fama, "Efficient capital markets: A review of theory and empirical work", *The
  Journal of Finance* **25**(2), 383–417 (1970).
- [97] A. Timmermann and C. W. J. Granger, "Efficient market hypothesis and forecasting",
  *International Journal of Forecasting* **20**(1), 15–27 (2004).
- [98] A. W. Lo, "The adaptive markets hypothesis: Market efficiency from an evolutionary
  perspective", *The Journal of Portfolio Management* **30**(5), 15–29 (2004).
- [99] S. Gu, B. Kelly and D. Xiu, "Empirical asset pricing via machine learning", *The Review of
  Financial Studies* **33**(5), 2223–2273 (2020).
- [100] C. R. Harvey, Y. Liu and H. Zhu, "…and the cross-section of expected returns", *The
  Review of Financial Studies* **29**(1), 5–68 (2016).
- [101] D. H. Bailey, J. M. Borwein, M. López de Prado and Q. J. Zhu, "Pseudo-mathematics and
  financial charlatanism: The effects of backtest overfitting on out-of-sample performance",
  *Notices of the American Mathematical Society* **61**(5), 458–471 (2014).
- [102] M. López de Prado, *Advances in Financial Machine Learning*, John Wiley & Sons (2018).
- [103] O. B. Sezer, M. U. Gudelek and A. M. Ozbayoglu, "Financial time series forecasting with
  deep learning: A systematic literature review: 2005–2019", *Applied Soft Computing* **90**,
  106181 (2020).
- [104] I. Goodfellow, Y. Bengio and A. Courville, *Deep Learning*, MIT Press (2016).
- [105] C. M. Bishop, *Pattern Recognition and Machine Learning*, Springer (2006).
- [106] C. M. Bishop and H. Bishop, *Deep Learning: Foundations and Concepts*, Springer (2024).
- [107] K. P. Murphy, *Probabilistic Machine Learning: An Introduction*, MIT Press (2022).
- [108] K. P. Murphy, *Probabilistic Machine Learning: Advanced Topics*, MIT Press (2023).
- [109] S. J. D. Prince, *Understanding Deep Learning*, MIT Press (2023).
- [110] T. Hastie, R. Tibshirani and J. Friedman, *The Elements of Statistical Learning*, 2nd
  ed., Springer (2009).
- [111] S. Shalev-Shwartz and S. Ben-David, *Understanding Machine Learning: From Theory to
  Algorithms*, Cambridge University Press (2014).
- [112] W. L. Hamilton, *Graph Representation Learning*, Synthesis Lectures on Artificial
  Intelligence and Machine Learning, Morgan & Claypool (2020).
- [113] Z. Wu, S. Pan, F. Chen, G. Long, C. Zhang and P. S. Yu, "A comprehensive survey on graph
  neural networks", *IEEE Transactions on Neural Networks and Learning Systems* **32**(1), 4–24
  (2021).
- [114] K. Benidis, S. S. Rangapuram, V. Flunkert, Y. Wang, D. Maddix, C. Türkmen, J. Gasthaus,
  M. Bohlke-Schneider, D. Salinas, L. Stella, F.-X. Aubet, L. Callot and T. Januschowski, "Deep
  learning for time series forecasting: Tutorial and literature survey", *ACM Computing Surveys*
  **55**(6), Article 121 (2022).
- [115] R. J. Hyndman and G. Athanasopoulos, *Forecasting: Principles and Practice*, 3rd ed.,
  OTexts (2021).
- [116] G. E. P. Box, G. M. Jenkins, G. C. Reinsel and G. M. Ljung, *Time Series Analysis:
  Forecasting and Control*, 5th ed., John Wiley & Sons (2015).
- [117] J. D. Hamilton, *Time Series Analysis*, Princeton University Press (1994).
- [118] F. R. K. Chung, *Spectral Graph Theory*, CBMS Regional Conference Series in Mathematics
  **92**, American Mathematical Society (1997).
- [119] S. Boyd and L. Vandenberghe, *Convex Optimization*, Cambridge University Press (2004).
- [120] J. Nocedal and S. J. Wright, *Numerical Optimization*, 2nd ed., Springer (2006).
- [121] R. A. Horn and C. R. Johnson, *Matrix Analysis*, 2nd ed., Cambridge University Press
  (2013).
- [122] N. J. Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed., SIAM (2002).
- [123] D. Goldberg, "What every computer scientist should know about floating-point arithmetic",
  *ACM Computing Surveys* **23**(1), 5–48 (1991).

---

*This module is a theoretical exercise about the `amf` package's structure. It is illustrative
and not empirically validated. Nothing in it is financial advice, a diagnosis, or a forecast of
any real market.*
