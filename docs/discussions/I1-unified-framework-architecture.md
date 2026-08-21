# I1: Unified Framework Architecture

> **Discussion category**: Research · **Labels**: `I1`, `ensembles`, `architecture`, `research`
> **Source**: `docs/QUANTUM_NEURAL_RESEARCH.md` § Discussion I1
> **Status**: Open for comment · **Nature**: Theoretical module, illustrative and not
> empirically validated

---

## 0. Abstract and reading guide

Combining several models is the oldest reliable trick in forecasting, and the theory explaining
*when* it works is precise: the ensemble's squared error decomposes into bias, a variance term
that shrinks like `1/M`, and a covariance term that does not shrink at all. Diversity is
therefore not a nice-to-have — it is the entire mechanism, and an ensemble of four models fitted
to the same data through the same preprocessing pipeline may capture almost none of it.

This module develops the combination theory the source note's architecture needs, and identifies
three specific technical defects in the note's proposal, each of which changes what should be
built:

1. **Inverse-RMSE weighting is not the optimal combination rule** (§5.2). Bates and Granger's
   optimal weights involve the *inverse error-covariance matrix*, not inverse individual error
   variances. Inverse-RMSE weighting silently assumes the four models make uncorrelated errors —
   the assumption least likely to hold here, since all four consume the same preprocessed input.
2. **"Confidence = combine all confidence intervals (union = conservative)" is incorrect**
   (§5.3). The union of intervals is not a confidence interval; if the intervals are disjoint it
   is not even an interval. The construction that *is* conservative and valid is the Bonferroni
   **intersection** at adjusted level, and the construction that gives finite-sample validity
   without distributional assumptions is conformal prediction.
3. **"If 3/4 models agree risk is high → Alert" imports the Condorcet Jury Theorem's
   independence assumption** (§5.4), which is false by construction for models sharing a data
   pipeline. Under positively correlated votes, majority accuracy can fall *below* single-voter
   accuracy.

It also observes something about AMF that is easy to miss: **the package already contains an
ensemble**. `DiagnosticEngine` blends `fragility`, `concentration` and `feedback_amplification`
under fixed weights `0.4 / 0.3 / 0.3`, normalised by their sum. The note's question — how should
component weights be chosen? — is therefore already live in the codebase, and §5.6 shows that the
note's proposed answer cannot be adopted, because learning weights from historical error requires
a validated target, and the repository forbids claiming one.

**Prerequisites**: probability, linear regression, basic decision theory. §2.5 (conformal
prediction) needs exchangeability but no heavy machinery.

---

## 1. Verbatim source specification

The following is the source note's specification for this discussion, reproduced word for
word without alteration:

````markdown
### Discussion I1: Unified Framework Architecture
**Theme**: How to integrate quantum, neural, topological, and Hamiltonian approaches into one system

**Architecture**:
```
                  [Raw Market Data]
                         ↓
          [Data Preprocessing & Normalization]
                         ↓
        ┌───────────────┬──────────────┬─────────────┐
        ↓               ↓              ↓             ↓
    [Quantum]      [Neural]      [Topology]    [Hamiltonian]
    Superposition  Embeddings     Persistence   Phase-space
    Markov         LSTM/Transformer TDA         Symplectic
    Shannon        GNN            Homology      Dynamics
        ↓               ↓              ↓             ↓
        └───────────────┬──────────────┬─────────────┘
                        ↓
                  [Ensemble Voting]
                (Average predictions)
                        ↓
           [Multi-Output: Forecast + Confidence + Pathways]
                        ↓
            [Human Interpretability Layer]
          (Explain via knowledge graphs, visualizations)
```

**Voting Mechanism**:
```
Each model (quantum, neural, topo, hamiltonian) produces:
  - Point forecast (e.g., +2% return)
  - Confidence interval (e.g., 95% CI: [−1%, +5%])
  - Risk indicators (e.g., crisis probability, contagion risk)

Ensemble voting:
  Forecast = weighted average of 4 models
  Weight = inverse of historical RMSE (better models get higher weight)
  
Confidence = combine all confidence intervals (union = conservative)
  
Risk consensus: If 3/4 models agree risk is high → Alert
```

**Interpretability**:
```
Why did model predict crash?
  - Quantum: "Superposition collapsed to crisis state (90% probability)"
  - Neural: "Embedding moved to historical crisis cluster"
  - Topology: "Betti number jumped; persistent homology fractured"
  - Hamiltonian: "Phase-space volume increased; Liouville theorem violated"
  
Consensus: Multiple independent methods agree → Strong signal
           Methods disagree → Ambiguous; need more data
```

**Deliverable**:
- `docs/research/unified_framework_architecture.md` — System design
- `src/amf/ensemble/voting_ensemble.py` — Ensemble voting
- `src/amf/ensemble/confidence_aggregation.py` — Combine confidence intervals
- `src/amf/interpretability/ensemble_explanation.py` — Why each model agreed/disagreed
- `examples/unified_crisis_prediction.py` — Full pipeline demo

**Research Leaders Needed**: Systems architect, ML engineer
````

---

## 2. Formal foundations

### 2.1 Why combining works: the error decomposition

Let `f₁, …, f_M` be predictors of a target `y`, and let `f̄ = (1/M) Σ_m f_m` be their simple
average. Write `e_m = f_m − y`.

**Proposition 2.1 (Ambiguity decomposition; Krogh & Vedelsby, 1995 [8]).** For squared error and
any convex combination with weights `w_m ≥ 0`, `Σ w_m = 1`,

```
( f̄_w − y )²  =  Σ_m w_m (f_m − y)²  −  Σ_m w_m (f_m − f̄_w)² .
```

The ensemble error equals the weighted average individual error **minus** the weighted
"ambiguity" (spread of the members around the ensemble). Because ambiguity is non-negative, the
ensemble is never worse than the average member. Note carefully what this does *not* say: it does
not say the ensemble beats the *best* member.

**Proposition 2.2 (Bias–variance–covariance decomposition).** For the uniform average of `M`
predictors with expectation taken over training sets,

```
E[( f̄ − y )²]  =  bias̄²  +  (1/M)·var̄  +  (1 − 1/M)·covar̄
```

where `bias̄` is the mean bias, `var̄` the mean variance and `covar̄` the mean pairwise
covariance of the members' errors. See Ueda and Nakano (1996) and the treatment in Brown,
Wyatt, Harris and Yao (2005) [9].

**This is the load-bearing result for the source note's architecture.** With `M = 4`, the
variance term is divided by 4 — but the covariance term is multiplied by `3/4` and does not
shrink with `M` at all. Four models sharing the input pipeline shown at the top of the note's
diagram ("Raw Market Data" → "Data Preprocessing & Normalization" → four branches) will have
highly correlated errors, and `covar̄ → var̄` drives the decomposition back to the single-model
error. Diversity must be engineered deliberately: different data views, different resampling,
different inductive biases — not merely different mathematical vocabularies.

### 2.2 Optimal linear combination

**Theorem 2.3 (Bates & Granger, 1969 [1]).** Let `e = (e₁, …, e_M)ᵀ` be the vector of forecast
errors with mean zero and covariance `Σ`. Among unbiased linear combinations `w ᵀf` with
`wᵀ1 = 1`, the mean-squared-error-minimising weights are

```
w*  =  Σ⁻¹ 1 / ( 1ᵀ Σ⁻¹ 1 ) ,        MSE(w*) = 1 / ( 1ᵀ Σ⁻¹ 1 ) .
```

*Proof.* Minimise `wᵀΣw` subject to `wᵀ1 = 1` by Lagrange multipliers. ∎

**Corollary 2.4.** If `Σ` is diagonal — that is, **if and only if the models' errors are
uncorrelated** — then `w*_m ∝ 1/σ_m²`, inverse error *variance*. Even then it is not inverse
RMSE (`1/σ_m`); see §5.2.

**Remark 2.5 (Negative weights).** `w*` need not be non-negative: when two forecasts are strongly
positively correlated and one is more accurate, the optimum shorts the weaker one. Granger and
Ramanathan (1984) [3] formulate combination as a regression, making this explicit.

**The forecast combination puzzle.** Empirically, the simple average frequently outperforms
estimated optimal weights, because `Σ` must itself be estimated and the estimation error swamps
the theoretical gain. Documented by Stock and Watson (2004) [4]; Smith and Wallis (2009) [5]
give the estimation-error explanation; Clemen (1989) [2] and Timmermann (2006) [6] survey. The
practical implication for the note's proposal is direct: **an equal-weight average is a serious
baseline that estimated weights must beat, not a naive fallback.**

### 2.3 Families of combination

- **Bagging** (Breiman, 1996 [10]): bootstrap the data, average the fits. Reduces variance for
  high-variance/low-bias learners; provably does little for stable ones.
- **Boosting** (Freund & Schapire, 1997 [12]): fit sequentially to reweighted residuals; reduces
  bias. Not an ensemble of independently trained members.
- **Stacking / stacked generalisation** (Wolpert, 1992 [11]): learn the combiner itself from
  **out-of-fold** predictions. The out-of-fold requirement is not optional — stacking on in-sample
  predictions leaks and produces weights that favour the most overfitted member.
- **Bayesian model averaging** (Hoeting, Madigan, Raftery & Volinsky, 1999 [13]): weight by
  posterior model probability, `p(y|D) = Σ_m p(y|M_m, D) p(M_m|D)`. Coherent, but assumes the
  true model is in the set (the **M-closed** setting). Under **M-open** — no candidate is true,
  which is the honest assumption here — BMA concentrates on the single closest model as data
  accumulate, which is the opposite of what an ensemble is for. Stacking is the M-open-appropriate
  alternative.
- **Deep ensembles** (Lakshminarayanan, Pritzel & Blundell, 2017 [14]): independently initialised
  networks; a strong and simple uncertainty baseline.

**Theorem 2.6 (No Free Lunch; Wolpert & Macready, 1997 [15]).** Averaged uniformly over all
objective functions, all search algorithms have identical performance. The practical reading is
modest but real: superiority claims are claims about a *restricted problem class*, and must be
stated that way.

### 2.4 Scoring, calibration and sharpness

**Definition 2.7 (Proper scoring rule).** A scoring rule `S(F, y)` for a predictive distribution
`F` is **proper** if `E_{y∼G}[S(G, y)] ≤ E_{y∼G}[S(F, y)]` for all `F, G`, and **strictly proper**
if equality implies `F = G`. Propriety means honest reporting is optimal. Gneiting and Raftery
(2007) [16] is the definitive treatment; the log score, the Brier score and CRPS are proper,
whereas accuracy and RMSE-of-the-mean are not proper for distributional forecasts.

**Definition 2.8 (Brier score; Brier, 1950 [18]).** For binary outcomes, `BS = (1/n) Σ (p_i − y_i)²`.

**Theorem 2.9 (Murphy decomposition, 1973 [19]).** `BS = reliability − resolution + uncertainty`,
where reliability measures calibration error, resolution the ability to discriminate, and
uncertainty the base rate's variance. A model can improve its Brier score purely by being better
calibrated while discriminating no better — which is exactly the failure mode an ensemble
"consensus alert" is prone to.

**Principle 2.10 (Gneiting, Balabdaoui & Raftery, 2007 [17]).** Maximise sharpness *subject to*
calibration. Combining predictive distributions by linear pooling produces a mixture that is
generally **under-confident** (over-dispersed) even when every component is calibrated — so a
naively pooled ensemble usually needs recalibration.

### 2.5 Distribution-free uncertainty: conformal prediction

**Theorem 2.11 (Split conformal validity).** Let `(X_i, Y_i)_{i=1}^{n}` and `(X_{n+1}, Y_{n+1})`
be **exchangeable**. Fit a model on a proper training split; on a held-out calibration set of size
`n` compute conformity scores `s_i`, and let `q̂` be the `⌈(n+1)(1−α)⌉/n` empirical quantile.
Then the set `C(X_{n+1}) = { y : s(X_{n+1}, y) ≤ q̂ }` satisfies

```
P( Y_{n+1} ∈ C(X_{n+1}) )  ≥  1 − α ,
```

with finite-sample validity, for any underlying model and any distribution. See Vovk, Gammerman
and Shafer [20] and the introduction by Angelopoulos and Bates [21].

**This is the correct replacement for the note's interval-combination step**, with one critical
caveat: exchangeability fails for time series. Barber, Candès, Ramdas and Tibshirani [22] quantify
the coverage loss under non-exchangeability and give reweighted variants; Gibbs and Candès [23]
give an adaptive online scheme that maintains long-run coverage under distribution shift. Any
application here must use those variants and say so.

### 2.6 Voting and the independence assumption

**Theorem 2.12 (Condorcet Jury Theorem, 1785 [24]).** If each of `M` voters is independently
correct with probability `p > 1/2`, the probability that a majority is correct is increasing in
`M` and tends to `1`.

**Theorem 2.13 (Correlated votes).** The conclusion fails under positive correlation. Ladha
(1992) [25] shows majority accuracy depends on the mean pairwise correlation of votes, and that
sufficiently strong positive correlation makes the majority *less* accurate than a single voter —
because correlated voters supply one effective vote plus noise.

The note's "If 3/4 models agree risk is high → Alert" is a `M = 4`, threshold-3 rule. It inherits
Theorem 2.12's independence hypothesis, which its own architecture diagram violates.

### 2.7 Aggregating intervals correctly

**Proposition 2.14 (Bonferroni / Boole).** If `C_1, …, C_M` each have coverage `≥ 1 − α_m`, then

```
P( Y ∈ ⋂_m C_m )  ≥  1 − Σ_m α_m .
```

So the **intersection** at levels summing to `α` gives simultaneous coverage `1 − α`. Šidák's
inequality gives a slightly sharper bound under independence.

**Proposition 2.15 (Why the union fails).** `P(Y ∈ ⋃_m C_m) ≥ max_m (1 − α_m)`, so the union is
*conservative in coverage* — but (i) it is not in general an interval (disjoint components), (ii)
its width is unbounded and grows with the number of disagreeing models, so it conveys no
information, and (iii) it is not a valid `1 − α` procedure for any `α` smaller than
`min_m α_m`, so it cannot be tightened. It is "conservative" only in the sense that a prediction
of `(−∞, ∞)` is conservative.

---

## 3. Academic curriculum modules

| Module | Level | Canonical courses | Core texts | What AMF needs from it |
|---|---|---|---|---|
| Statistical learning | Advanced undergraduate / graduate | Stanford CS229 and STATS315; CMU 10-701 | Hastie, Tibshirani & Friedman [26] Ch. 8, 15, 16 | Bagging, boosting, random forests, model averaging |
| Learning theory | Graduate | MIT 9.520; CMU 10-715 | Shalev-Shwartz & Ben-David, *Understanding Machine Learning* | Generalisation bounds, capacity control, why averaging helps |
| Forecasting & econometrics | Graduate | Econometrics sequences; time-series courses at LSE/Oxford | Timmermann [6]; Elliott & Timmermann, *Economic Forecasting* | Combination weights, the combination puzzle, evaluation |
| Decision theory & scoring | Graduate | Bayesian statistics sequences | Gneiting & Raftery [16]; Bernardo & Smith, *Bayesian Theory* | Proper scoring rules, calibration/sharpness, elicitability |
| Bayesian model averaging | Graduate | Bayesian statistics | Hoeting et al. [13]; Gelman et al., *Bayesian Data Analysis* Ch. 7 | M-open vs M-closed, posterior model probabilities |
| Conformal prediction | Graduate / research | Recent topics courses; the authors' tutorials | Vovk, Gammerman & Shafer [20]; Angelopoulos & Bates [21] | Distribution-free finite-sample intervals and their assumptions |
| Interpretable ML | Graduate | ML topics courses | Molnar, *Interpretable Machine Learning*; Lundberg & Lee [28] | Attribution, its axioms, and its limits |
| Software architecture | Practitioner | — | The repository's own layering rules in `CLAUDE.md` | One-way dependency order, determinism, testability |

---

## 4. Exact source material

### 4.1 Forecast combination — the econometrics lineage

- **Bates, J. M. and Granger, C. W. J.** "The Combination of Forecasts." *Operational Research
  Quarterly* **20**(4), 451–468 (1969). The founding paper; Theorem 2.3.
- **Granger, C. W. J. and Ramanathan, R.** "Improved methods of combining forecasts."
  *Journal of Forecasting* **3**(2), 197–204 (1984). Combination as regression.
- **Clemen, R. T.** "Combining forecasts: A review and annotated bibliography."
  *International Journal of Forecasting* **5**(4), 559–583 (1989).
- **Stock, J. H. and Watson, M. W.** "Combination forecasts of output growth in a seven-country
  data set." *Journal of Forecasting* **23**(6), 405–430 (2004). The combination puzzle in the
  wild.
- **Smith, J. and Wallis, K. F.** "A Simple Explanation of the Forecast Combination Puzzle."
  *Oxford Bulletin of Economics and Statistics* **71**(3), 331–355 (2009). Estimation error as
  the explanation.
- **Timmermann, A.** "Forecast Combinations." In *Handbook of Economic Forecasting*, Volume 1
  (eds. G. Elliott, C. W. J. Granger and A. Timmermann), Elsevier, 2006. The survey to read first.

### 4.2 Ensemble methods — the machine-learning lineage

- **Krogh, A. and Vedelsby, J.** "Neural Network Ensembles, Cross Validation, and Active
  Learning." *Advances in Neural Information Processing Systems* **7** (1995). The ambiguity
  decomposition.
- **Brown, G., Wyatt, J., Harris, R. and Yao, X.** "Diversity creation methods: a survey and
  categorisation." *Information Fusion* **6**(1), 5–20 (2005). The careful account of what
  "diversity" can and cannot be made to mean.
- **Breiman, L.** "Bagging Predictors." *Machine Learning* **24**(2), 123–140 (1996).
- **Wolpert, D. H.** "Stacked Generalization." *Neural Networks* **5**(2), 241–259 (1992).
- **Freund, Y. and Schapire, R. E.** "A Decision-Theoretic Generalization of On-Line Learning and
  an Application to Boosting." *Journal of Computer and System Sciences* **55**(1), 119–139 (1997).
- **Breiman, L.** "Random Forests." *Machine Learning* **45**(1), 5–32 (2001).
- **Dietterich, T. G.** "Ensemble Methods in Machine Learning." *Multiple Classifier Systems*,
  Lecture Notes in Computer Science 1857, Springer, 1–15 (2000).
- **Hoeting, J. A., Madigan, D., Raftery, A. E. and Volinsky, C. T.** "Bayesian Model Averaging:
  A Tutorial." *Statistical Science* **14**(4), 382–401 (1999).
- **Lakshminarayanan, B., Pritzel, A. and Blundell, C.** "Simple and Scalable Predictive
  Uncertainty Estimation using Deep Ensembles." *Advances in Neural Information Processing
  Systems* **30** (2017).
- **Wolpert, D. H. and Macready, W. G.** "No Free Lunch Theorems for Optimization."
  *IEEE Transactions on Evolutionary Computation* **1**(1), 67–82 (1997).

### 4.3 Scoring, calibration and uncertainty

- **Gneiting, T. and Raftery, A. E.** "Strictly Proper Scoring Rules, Prediction, and Estimation."
  *Journal of the American Statistical Association* **102**(477), 359–378 (2007).
- **Gneiting, T., Balabdaoui, F. and Raftery, A. E.** "Probabilistic forecasts, calibration and
  sharpness." *Journal of the Royal Statistical Society, Series B* **69**(2), 243–268 (2007).
- **Brier, G. W.** "Verification of Forecasts Expressed in Terms of Probability."
  *Monthly Weather Review* **78**(1), 1–3 (1950).
- **Murphy, A. H.** "A New Vector Partition of the Probability Score." *Journal of Applied
  Meteorology* **12**(4), 595–600 (1973).
- **Vovk, V., Gammerman, A. and Shafer, G.** *Algorithmic Learning in a Random World.* Springer,
  2005 (2nd edition 2022).
- **Angelopoulos, A. N. and Bates, S.** "Conformal Prediction: A Gentle Introduction."
  *Foundations and Trends in Machine Learning* **16**(4), 494–591 (2023).
- **Barber, R. F., Candès, E. J., Ramdas, A. and Tibshirani, R. J.** "Conformal prediction beyond
  exchangeability." *The Annals of Statistics* **51**(2), 816–845 (2023). **Essential** for any
  time-series use.
- **Gibbs, I. and Candès, E. J.** "Adaptive Conformal Inference Under Distribution Shift."
  *Advances in Neural Information Processing Systems* **34** (2021).

### 4.4 Voting, attribution and general reference

- **Condorcet, M. J. A. N. de Caritat, marquis de.** *Essai sur l'application de l'analyse à la
  probabilité des décisions rendues à la pluralité des voix.* Imprimerie Royale, Paris, 1785.
- **Ladha, K. K.** "The Condorcet Jury Theorem, Free Speech, and Correlated Votes."
  *American Journal of Political Science* **36**(3), 617–634 (1992). The correlated-vote
  correction that the note's `3/4` rule needs.
- **Hastie, T., Tibshirani, R. and Friedman, J.** *The Elements of Statistical Learning.*
  2nd edition, Springer, 2009. **Ch. 8** (model inference and averaging), **Ch. 15** (random
  forests), **Ch. 16** (ensemble learning).
- **Lundberg, S. M. and Lee, S.-I.** "A Unified Approach to Interpreting Model Predictions."
  *Advances in Neural Information Processing Systems* **30** (2017). SHAP.
- **Ribeiro, M. T., Singh, S. and Guestrin, C.** "'Why Should I Trust You?': Explaining the
  Predictions of Any Classifier." *KDD '16*, 1135–1144 (2016). LIME.

**Caution on the interpretability layer.** The note's example explanations ("Superposition
collapsed to crisis state (90% probability)") are *post-hoc narratives*, not attributions. Post-hoc
explanation methods have documented failure modes — they can be unfaithful to the model, unstable
under small input changes, and manipulable. An explanation that four differently-motivated models
"agree" is especially seductive and especially weak when their agreement is driven by a shared
input pipeline (§5.4).

---

## 5. Derivation for the AMF setting

### 5.1 AMF already has two things called "ensemble" — keep them distinct

| | `ShockSimulator.ensemble()` (existing) | The note's "Ensemble Voting" (proposed) |
|---|---|---|
| What varies across members | The random seed (`base_seed + i`) and jitter | The **model class** — quantum, neural, topological, Hamiltonian |
| What it estimates | Sampling variability of one model | Disagreement between different models |
| Output | `ResilienceDistribution` (percentiles by linear interpolation) | A combined point forecast plus interval |
| Statistical content | A Monte Carlo replication ensemble | A model-combination ensemble |

These answer different questions and their uncertainties do not compose by simple addition.
Conflating them would let jitter-induced spread masquerade as model disagreement. Any
implementation must name them differently — `replication_distribution` versus
`combination_weights`, say — and must never pool their variances.

### 5.2 The weighting rule the note proposes is not the optimal one

The note specifies: *"Weight = inverse of historical RMSE (better models get higher weight)"*.

**Proposition 5.1.** Inverse-RMSE weighting, `w_m ∝ 1/σ_m`, is optimal under **no** standard
assumption. Under uncorrelated errors the optimum is inverse *variance*, `w_m ∝ 1/σ_m²`
(Corollary 2.4); under correlated errors it is `w* ∝ Σ⁻¹1` (Theorem 2.3), which generally differs
from both and may be negative in some coordinates (Remark 2.5).

**Worked illustration.** Two members with `σ₁ = 1`, `σ₂ = 2` and error correlation `ρ`:

```
Σ = [[1,   2ρ],
     [2ρ,  4 ]]

Inverse-RMSE weights:      w = (1/1, 1/2)/(1 + 1/2)          = (0.667, 0.333)
Inverse-variance weights:  w = (1/1, 1/4)/(1 + 1/4)          = (0.800, 0.200)
Bates–Granger optimum:     w* = Σ⁻¹1 / (1ᵀΣ⁻¹1)
                              ρ = 0.0  →  (0.800, 0.200)
                              ρ = 0.5  →  (1.000, 0.000)
                              ρ = 0.9  →  (1.375, −0.375)
```

At `ρ = 0.5` the optimum discards member 2 entirely; at `ρ = 0.9` it takes a negative weight. The
inverse-RMSE rule assigns member 2 a third of the weight in every case, because it cannot see `ρ`.
Given that the note's four branches share the "Data Preprocessing & Normalization" stage, high `ρ`
is the expected regime, not an edge case.

**Recommendation.** If weights are to be estimated at all, estimate them by **stacking on
out-of-fold predictions** (Wolpert [11]) with a non-negativity constraint for stability, and
benchmark against the equal-weight average, which the combination-puzzle literature (§2.2) says
is hard to beat. Report both.

### 5.3 The interval-combination rule is incorrect as specified

The note specifies: *"Confidence = combine all confidence intervals (union = conservative)"*.

By Proposition 2.15 the union is not a valid confidence procedure: it need not be an interval, its
width is uncontrolled, and it cannot be tightened. Three correct alternatives, in increasing order
of what they demand:

1. **Bonferroni intersection** (Proposition 2.14). Compute each member's interval at level
   `1 − α/M` and intersect. Simultaneous coverage `≥ 1 − α`. Cheap, valid, and can be *empty* —
   which is informative, since an empty intersection is exactly the "methods disagree" case the
   note wants to detect, arriving as a mathematical consequence rather than a heuristic.
2. **Linear pooling with recalibration.** Average the predictive distributions, then recalibrate,
   since pooling over-disperses (Principle 2.10). Evaluate with a strictly proper score.
3. **Conformal prediction over the ensemble** (Theorem 2.11). Treat the whole ensemble as one
   black-box predictor and calibrate its residuals on held-out data. Finite-sample validity, no
   distributional assumptions — but **exchangeability is required**, so the non-exchangeable
   variants of Barber et al. [22] or Gibbs and Candès [23] are mandatory for any time-indexed
   application.

Option 1 is what a package under AMF's constraints should implement: it is deterministic,
dependency-free, and a dozen lines of arithmetic.

### 5.4 The consensus rule imports an assumption its own diagram violates

The note specifies: *"Risk consensus: If 3/4 models agree risk is high → Alert"*, justified as
*"Multiple independent methods agree → Strong signal"*.

The independence is asserted, not established, and the architecture diagram refutes it: all four
branches descend from a single "[Raw Market Data] → [Data Preprocessing & Normalization]" trunk.
Shared preprocessing induces shared errors — a normalisation artefact, a look-ahead leak or a
missing-data convention propagates to all four branches identically.

By Theorem 2.13, positively correlated votes degrade majority performance, and in the strongly
correlated limit four votes carry the information of roughly one. The honest procedure:

1. **Measure the correlation.** Estimate the pairwise error correlation matrix of the members on
   held-out data and report it alongside any consensus statistic. A consensus rule quoted without
   its members' correlation matrix is uninterpretable.
2. **Weight by effective sample size**, not by count. For exchangeably correlated votes with mean
   correlation `ρ̄`, the effective number of independent votes is roughly `M / (1 + (M−1)ρ̄)`. At
   `M = 4`, `ρ̄ = 0.8`, this is about `1.2` — so "3 of 4 agree" is close to "1 model says so".
3. **Diversify the trunk**, not just the branches. Different preprocessing, different data views
   and different resampling do more for `covar̄` in Proposition 2.2 than adding a fifth
   mathematical formalism.

### 5.5 What the architecture becomes under the repository's rules

The note's pipeline begins with "[Raw Market Data]" and ends with "[Multi-Output: Forecast +
Confidence + Pathways]". Both endpoints are outside the `amf` package boundary: the package takes
a structural `Market` as input and emits structural diagnostics, not market data in and forecasts
out. The structure-preserving analogue:

```
                  [Market  — seven systems + DependencyGraph]
                                     │
                     [Canonical assembly: SystemKind order]
                                     │
        ┌───────────────┬────────────┴────────────┬──────────────────┐
        ▼               ▼                         ▼                  ▼
  DiagnosticEngine  ShockSimulator          TDA (module H2)    Dissipativity
  weakness index    resilience score        β₀ / β₁ barcode    certificate (H3)
        │               │                         │                  │
        └───────────────┴────────────┬────────────┴──────────────────┘
                                     ▼
                      [Combination — fixed, documented weights]
                                     ▼
       [Multi-output: structural index + Bonferroni interval + drivers]
                                     ▼
              [Renderers: report.render_* / viz.render_*  (pure, no I/O)]
```

Every box is a structural computation over a user-supplied configuration. The final row already
exists — `report.py` and `viz.py` are the "Human Interpretability Layer", and `viz.render_graph_svg`
already colours nodes by severity, which is the note's "Explain via ... visualizations".

Note also that `WeaknessFinding.drivers` — plain-language strings emitted when a component crosses
its explanation threshold — is a *faithful* explanation in a sense post-hoc attribution is not: it
reports which term of a known closed-form score crossed a known threshold. That is a better
interpretability primitive than SHAP-on-a-black-box, and it should be the model for anything added
here.

### 5.6 The decisive constraint: there is no target to fit weights to

The note's weighting rule requires "historical RMSE" — an error measured against a ground truth.

**Proposition 5.2.** Within the `amf` package, no such quantity exists or may be created. The
package's own documentation states that its thresholds, weights and scores are not empirically
validated, and that its output is not a diagnosis or forecast of any real market. There is
therefore no observable `y` against which a member's error could be computed, and any weight
estimated from one would constitute exactly the validated-performance claim the repository
forbids.

**Consequences, and they are constructive rather than merely prohibitive:**

- Combination weights inside the package must be **fixed, documented and declared illustrative** —
  precisely as `DiagnosticConfig`'s `0.4 / 0.3 / 0.3` already are. This is not a shortcoming to be
  fixed later; it is the honest form of the thing.
- What *can* be studied inside the boundary is **internal consistency**: do the members rank a
  corpus of synthetic markets concordantly? Rank correlation between the diagnostic index, the
  resilience score, the `H₂` barcode summaries and the `H₃` dissipativity certificate is
  computable, meaningful and claims nothing about real markets.
- Weight *learning* against real outcomes belongs to the out-of-tree research sidecar, gated by
  module **I2**.

**Observation 5.3.** `DiagnosticEngine` is already a three-member weighted ensemble
(`fragility`, `concentration`, `feedback`) with weights normalised by their sum, and
`ResilienceScore` is already a three-member combination (`0.6·absorbed + 0.25·(1 − amp_penalty) +
0.15·(1 − settle_penalty)`). The genuinely open architectural question I1 should be discussing is
therefore not "how do we bolt four new model families together" but **"are the weights we already
ship defensible, and how would we know?"** — a question this repository can actually answer,
because it is a question about internal consistency and sensitivity, not about market outcomes.
`SensitivityAnalyzer` is most of the apparatus for it already.

### 5.7 Determinism of the combination step

Weighted averaging is floating-point summation, and floating-point addition is not associative —
the same hazard `CLAUDE.md` records for the diagnostic HHI, where insertion-ordered traversal made
a diagnosis differ in its last bits. Any combiner must therefore:

- iterate members in a **canonical declaration order**, never dict-insertion order;
- normalise weights by their exact sum once, in a fixed order;
- validate weights on construction — finite, non-negative, not all zero — raising
  `InvalidConfigError`, exactly as `DiagnosticConfig` does;
- break ranking ties by `SystemKind` declaration order, as both existing rankings do.

A property test asserting that a market and every permutation of its assembly order produce a
bit-identical combined output should accompany the code, mirroring the existing permutation test.

---

## 6. Repository governance and boundary analysis

| Proposed artefact | Conflict | Compliant reformulation |
|---|---|---|
| `src/amf/ensemble/voting_ensemble.py` | **Non-trading boundary**: the note's members emit "+2% return" and "Point forecast" — `returns` and `signal` are on the `FORBIDDEN` substring list. Also **illustrative, not validated**: `Forecast` claims predictive power | `src/amf/composite/structural_index.py`: combine structural scores under fixed, validated, documented weights. Members are structural measures, never forecasts |
| Weighting by "inverse of historical RMSE" | **Illustrative, not validated** (Proposition 5.2) — requires a ground-truth target the package must not claim. Also statistically wrong (Proposition 5.1) | Fixed documented weights, declared illustrative; study internal rank-concordance instead. Any error-based weighting lives in the sidecar behind module **I2** |
| `src/amf/ensemble/confidence_aggregation.py` — "union = conservative" | **Mathematically incorrect** (Proposition 2.15) | Implement the Bonferroni intersection (Proposition 2.14). Deterministic, stdlib-only, and its empty case is the meaningful "members disagree" signal |
| `src/amf/interpretability/ensemble_explanation.py` | Naming is clean; risk is **unfaithful post-hoc narrative** | Follow the `WeaknessFinding.drivers` pattern: emit strings tied to a known closed-form term crossing a known threshold. Frozen slotted result type with `to_dict()`; extend `report._to_jsonable` and the text/Markdown renderers |
| `examples/unified_crisis_prediction.py` | **Non-trading boundary** and **predictive-claim rule** — "crisis prediction" over market data | `examples/composite_structural_index.py`: assemble a market, compute each structural member, combine, show the Bonferroni interval and the drivers. Emit the `_DISCLAIMER`; add to `tests/integration/test_examples.py` |
| "Raw Market Data", "Data Preprocessing & Normalization" | Outside the package boundary entirely — `amf` consumes a structural `Market`, not market data | Belongs to the sidecar. The package entry point stays `Market.from_dict` |
| Any SHAP/LIME dependency | **Zero runtime dependencies** | Threshold-crossing drivers need no dependency at all |

**Layering.** A combiner consumes `DiagnosticReport`, `ResilienceScore` and any new structural
summaries, so it sits above `diagnostics`/`simulation` and below `report`/`viz`/`cli` — the same
tier as `sensitivity`. It must not import `report`, `viz` or `cli`. Keep the graph acyclic.

**Coverage.** The 100% statement-and-branch gate applies. A combiner with `M` configurable members
has combinatorial branch structure — empty member set, single member, all-zero weights, empty
Bonferroni intersection. Each needs a test; the fix for a failing gate is a test, never a lower
threshold.

---

## 7. Falsifiable propositions and open questions

**P1 (Inverse-RMSE is suboptimal).** On simulated members with known error covariance,
inverse-RMSE weighting has strictly higher MSE than the Bates–Granger optimum whenever `ρ ≠ 0` or
the variances differ. *Status: proved* (Proposition 5.1); *refuted if* a counterexample covariance
makes them coincide other than in the trivial equal-variance, zero-correlation case.

**P2 (Correlation destroys the consensus rule).** For AMF's structural members computed from a
common `Market`, the mean pairwise rank correlation `ρ̄` is high enough that the effective number
of independent members is below 2. *Refuted if*: measured on a corpus of synthetic markets, the
members' disagreements are close to independent. Directly testable **inside** the package, since
it concerns internal consistency and needs no market data.

**P3 (Equal weights are hard to beat).** On synthetic markets with a stipulated structural target,
stacked weights estimated out-of-fold do not beat the equal-weight average by a margin exceeding
their own estimation error. *Refuted if*: a stacking scheme shows a stable, replicated advantage.

**P4 (Bonferroni intervals are informative, not vacuous).** The intersection interval is non-empty
for most markets and empty precisely for markets whose members genuinely disagree. *Refuted if*:
it is almost always empty (members are inconsistent, and the composite index is not meaningful) or
almost never empty (the members carry the same information — which would also confirm P2).

**P5 (Existing weights are defensible).** The `0.4 / 0.3 / 0.3` diagnostic blend and the
`0.6 / 0.25 / 0.15` resilience blend produce rankings that are stable under perturbation of those
weights. *Refuted if*: `SensitivityAnalyzer`-style perturbation of the weights themselves reorders
the findings substantially — which would mean the published rankings are artefacts of an
unvalidated choice, and would be the most important finding in this whole module set.

**Open questions.**

1. Is there a structural target that is *internal* to AMF and legitimate to fit against — for
   example, "does the composite index predict the simulated resilience score of a market it has
   not seen?" That is a statement about the model, not about markets, and may be admissible.
2. Should members be combined at the level of scores, of rankings (rank aggregation, Kemeny), or
   of severity bands? Rank aggregation is scale-free and would sidestep the normalisation
   question entirely.
3. Does an empty Bonferroni intersection deserve its own `Severity` treatment, or a distinct
   result type meaning "members inconsistent"?
4. How should a combiner behave when a member is undefined for a given market — for instance when
   `centrality` raises `InvalidDependencyError` on a graph with no dominant mode? Dropping the
   member changes `M` and thus the Bonferroni level; that must be explicit, not silent.

---

## 8. Deliverables

Reproduced from the source note, with a compliance column:

| Deliverable (verbatim) | Status | Compliance note |
|---|---|---|
| `docs/research/unified_framework_architecture.md` — System design | Superseded by this module | No conflict |
| `src/amf/ensemble/voting_ensemble.py` — Ensemble voting | **Blocked as specified** | Forecast/return vocabulary and predictive claims. Reformulate as `composite/structural_index.py` with fixed illustrative weights |
| `src/amf/ensemble/confidence_aggregation.py` — Combine confidence intervals | **Rejected as specified**, feasible when corrected | The union rule is invalid (Proposition 2.15). Implement the Bonferroni intersection; stdlib-only, deterministic |
| `src/amf/interpretability/ensemble_explanation.py` — Why each model agreed/disagreed | Proposed, feasible | Threshold-crossing drivers in the `WeaknessFinding.drivers` style; no SHAP/LIME dependency; frozen slotted type with `to_dict()` |
| `examples/unified_crisis_prediction.py` — Full pipeline demo | **Blocked as specified** | Non-trading boundary and predictive-claim rule. Reformulate as `composite_structural_index.py` |

**Research Leaders Needed**: Systems architect, ML engineer

To that list this module would add a **statistician**, since the three defects identified in §5.2,
§5.3 and §5.4 are statistical rather than architectural, and none of them would be caught by a
systems review.

---

## 9. Research leadership and prerequisites

**Skills matrix.**

| Role | Must have | Should have | Will own |
|---|---|---|---|
| Systems architect | Layered dependency design; determinism; API design | The repository's one-way module order and its history | §5.5 architecture; layering; result-type design |
| ML engineer | Ensembles, stacking, out-of-fold discipline | Calibration; uncertainty quantification | The combiner; the internal-consistency study for P2 |
| Statistician | Combination theory; proper scoring; multiple comparisons | Conformal prediction and its exchangeability limits | §5.2–§5.4 corrections; P1, P3, P4; the interval procedure |
| AMF maintainer | `DiagnosticConfig`, `SimulationConfig`, `SensitivityAnalyzer`; the hard rules | The determinism incidents recorded in `CLAUDE.md` | §6 boundary calls; P5, which concerns weights already shipped |

**Prerequisite ladder.**

```
Probability + linear regression
            │
            ▼
   Bias–variance (ESL Ch. 7)  ──►  Bias–variance–covariance (Prop. 2.2)
            │                                   │
            ▼                                   ▼
  Bagging / boosting / stacking       Optimal combination (Bates–Granger)
     (ESL Ch. 8, 15, 16)                        │
            │                                   ▼
            │                        The combination puzzle [4,5,6]
            └───────────────┬───────────────────┘
                            ▼
             Proper scoring & calibration [16,17]
                            ▼
             Conformal prediction [20,21] ──► beyond exchangeability [22,23]
                            ▼
                  Module I2 — evaluation discipline
```

`I1` and `I2` should be read as one unit: `I1` says how to combine, `I2` says how you would ever
know whether the combination helped. Neither is safe alone.

---

## References

[1] Bates, J. M. and Granger, C. W. J. "The Combination of Forecasts." *Operational Research
Quarterly* **20**(4), 451–468 (1969).

[2] Clemen, R. T. "Combining forecasts: A review and annotated bibliography."
*International Journal of Forecasting* **5**(4), 559–583 (1989).

[3] Granger, C. W. J. and Ramanathan, R. "Improved methods of combining forecasts."
*Journal of Forecasting* **3**(2), 197–204 (1984).

[4] Stock, J. H. and Watson, M. W. "Combination forecasts of output growth in a seven-country data
set." *Journal of Forecasting* **23**(6), 405–430 (2004).

[5] Smith, J. and Wallis, K. F. "A Simple Explanation of the Forecast Combination Puzzle."
*Oxford Bulletin of Economics and Statistics* **71**(3), 331–355 (2009).

[6] Timmermann, A. "Forecast Combinations." In *Handbook of Economic Forecasting*, Volume 1
(eds. G. Elliott, C. W. J. Granger and A. Timmermann), Elsevier, Amsterdam, 2006.

[7] Elliott, G. and Timmermann, A. *Economic Forecasting.* Princeton University Press, 2016.

[8] Krogh, A. and Vedelsby, J. "Neural Network Ensembles, Cross Validation, and Active Learning."
*Advances in Neural Information Processing Systems* **7** (1995).

[9] Brown, G., Wyatt, J., Harris, R. and Yao, X. "Diversity creation methods: a survey and
categorisation." *Information Fusion* **6**(1), 5–20 (2005).

[10] Breiman, L. "Bagging Predictors." *Machine Learning* **24**(2), 123–140 (1996).

[11] Wolpert, D. H. "Stacked Generalization." *Neural Networks* **5**(2), 241–259 (1992).

[12] Freund, Y. and Schapire, R. E. "A Decision-Theoretic Generalization of On-Line Learning and
an Application to Boosting." *Journal of Computer and System Sciences* **55**(1), 119–139 (1997).

[13] Hoeting, J. A., Madigan, D., Raftery, A. E. and Volinsky, C. T. "Bayesian Model Averaging:
A Tutorial." *Statistical Science* **14**(4), 382–401 (1999).

[14] Lakshminarayanan, B., Pritzel, A. and Blundell, C. "Simple and Scalable Predictive
Uncertainty Estimation using Deep Ensembles." *Advances in Neural Information Processing Systems*
**30** (2017).

[15] Wolpert, D. H. and Macready, W. G. "No Free Lunch Theorems for Optimization."
*IEEE Transactions on Evolutionary Computation* **1**(1), 67–82 (1997).

[16] Gneiting, T. and Raftery, A. E. "Strictly Proper Scoring Rules, Prediction, and Estimation."
*Journal of the American Statistical Association* **102**(477), 359–378 (2007).

[17] Gneiting, T., Balabdaoui, F. and Raftery, A. E. "Probabilistic forecasts, calibration and
sharpness." *Journal of the Royal Statistical Society, Series B* **69**(2), 243–268 (2007).

[18] Brier, G. W. "Verification of Forecasts Expressed in Terms of Probability."
*Monthly Weather Review* **78**(1), 1–3 (1950).

[19] Murphy, A. H. "A New Vector Partition of the Probability Score." *Journal of Applied
Meteorology* **12**(4), 595–600 (1973).

[20] Vovk, V., Gammerman, A. and Shafer, G. *Algorithmic Learning in a Random World.* Springer,
New York, 2005.

[21] Angelopoulos, A. N. and Bates, S. "Conformal Prediction: A Gentle Introduction."
*Foundations and Trends in Machine Learning* **16**(4), 494–591 (2023).

[22] Barber, R. F., Candès, E. J., Ramdas, A. and Tibshirani, R. J. "Conformal prediction beyond
exchangeability." *The Annals of Statistics* **51**(2), 816–845 (2023).

[23] Gibbs, I. and Candès, E. J. "Adaptive Conformal Inference Under Distribution Shift."
*Advances in Neural Information Processing Systems* **34** (2021).

[24] Condorcet, M. J. A. N. de Caritat, marquis de. *Essai sur l'application de l'analyse à la
probabilité des décisions rendues à la pluralité des voix.* Imprimerie Royale, Paris, 1785.

[25] Ladha, K. K. "The Condorcet Jury Theorem, Free Speech, and Correlated Votes."
*American Journal of Political Science* **36**(3), 617–634 (1992).

[26] Hastie, T., Tibshirani, R. and Friedman, J. *The Elements of Statistical Learning: Data
Mining, Inference, and Prediction.* 2nd edition, Springer, New York, 2009.

[27] Dietterich, T. G. "Ensemble Methods in Machine Learning." *Multiple Classifier Systems*,
Lecture Notes in Computer Science 1857, Springer, 1–15 (2000).

[28] Lundberg, S. M. and Lee, S.-I. "A Unified Approach to Interpreting Model Predictions."
*Advances in Neural Information Processing Systems* **30** (2017).

[29] Ribeiro, M. T., Singh, S. and Guestrin, C. "'Why Should I Trust You?': Explaining the
Predictions of Any Classifier." *Proceedings of the 22nd ACM SIGKDD International Conference on
Knowledge Discovery and Data Mining*, 1135–1144 (2016).

[30] Breiman, L. "Random Forests." *Machine Learning* **45**(1), 5–32 (2001).
