# I2: Validation, Backtesting & Generalization

> **Discussion category**: Research · **Labels**: `I2`, `validation`, `statistics`, `research`
> **Source**: `docs/QUANTUM_NEURAL_RESEARCH.md` § Discussion I2
> **Status**: Open for comment · **Nature**: Theoretical module, illustrative and not
> empirically validated

---

## 0. Abstract and reading guide

This is the gate module. Every other discussion in the set proposes a way of measuring market
structure; this one asks how anyone would ever know whether such a measurement is worth anything,
and the honest answer is harsher than the source note allows.

Three results organise the module.

**Result 1 — the sample is smaller than it looks (§5.1).** The note's own figure, "~20 major
crises in ~70 years", is the *effective* sample size, not the tens of thousands of daily
observations. Statistical power is governed by events, not by rows. With `N` model-and-parameter
configurations searched, the expected maximum `t`-statistic under a pure-noise null grows like
`√(2 ln N)`: at `N = 100` that is about `3.0`. A configuration reporting `t = 3` after a hundred
trials has reported nothing.

**Result 2 — cross-validation is invalid here without modification (§2.3).** Standard `k`-fold
cross-validation assumes exchangeability. Financial series are serially dependent and overlapping
labels leak across fold boundaries. Blocked, purged and embargoed schemes are the minimum; the
note's walk-forward design is correct in outline and under-specified in the details that matter.

**Result 3 — one metric in the note is disqualifying (§6).** *"Sharpe ratio (risk-adjusted
returns if traded on signals)"* is a trading-performance metric. It contains three separate
`FORBIDDEN` substrings (`returns`, `trade`, `signal`), and the `src/amf/backtest/` package path
contains a fourth (`backtest`). This is not a naming inconvenience to be worked around — a metric
that scores a strategy's profitability *is* the trading system the repository's charter excludes.

Against that, the module makes one constructive observation that reframes the whole discussion
(§5.4): **AMF already practises an unusually strict validation discipline — on its software.**
100% statement-and-branch coverage, Hypothesis property tests, a mechanical naming guard,
packaging invariants and byte-identical determinism checks are a serious *verification* regime.
What the repository explicitly does not have, and explicitly does not claim, is *validation*
against reality. Keeping those two words apart is the single most useful thing this module can
contribute.

**Prerequisites**: mathematical statistics (estimation, hypothesis testing), regression, basic
time-series. §2.1 references learning theory but does not depend on it.

---

## 1. Verbatim source specification

The following is the source note's specification for this discussion, reproduced word for
word without alteration:

````markdown
### Discussion I2: Validation, Backtesting & Generalization
**Theme**: How to rigorously test quantum-neural-topological approaches on real market data

**Challenges**:
1. Small sample size: Only ~20 major crises in ~70 years of data
2. Data leakage: Can't train on all data then test on same data
3. Non-stationarity: Market regimes change; 2008 ≠ 2020

**Backtesting Strategy**:
```
Walk-forward testing:
  For each year t in [2000, 2023]:
    1. Train on data [1990, t−1]
    2. Predict on [t, t+1]
    3. Compare forecast to actual
    4. Record error
    
Results: Time-series of prediction errors
  Plot: Does error increase before crises (less predictable)?
  
Metrics:
  - RMSE (accuracy)
  - Sharpe ratio (risk-adjusted returns if traded on signals)
  - Hit rate (% of crises detected 1–6 months early)
  - False alarm rate (% of false positives)
```

**Robustness Checks**:
```
1. Cross-market: Train on equities, test on bonds
2. Cross-asset: Train on developed markets, test on emerging
3. Cross-crisis: Train on 2008, test on 2020 (different mechanism)
4. Out-of-sample: Hidden test set (never seen during development)
```

**Deliverable**:
- `docs/research/validation_and_backtesting.md` — Methodology
- `src/amf/backtest/walk_forward_validator.py` — Walk-forward testing
- `src/amf/backtest/metrics.py` — Hit rate, false alarm rate, etc.
- `examples/backtest_crisis_detection.py` — Test all models
- `reports/model_performance_2024.md` — Annual results

**Research Leaders Needed**: Quantitative analyst, statistician
````

---

## 2. Formal foundations

### 2.1 Generalisation under dependence

**Definition 2.1 (Risk and empirical risk).** For a loss `ℓ`, hypothesis `h` and distribution `P`,
the risk is `R(h) = E_P[ℓ(h(X), Y)]` and the empirical risk on a sample of size `n` is
`R̂_n(h) = (1/n) Σ ℓ(h(X_i), Y_i)`. Empirical risk minimisation picks `ĥ = argmin_{h∈H} R̂_n(h)`.

**Theorem 2.2 (Uniform convergence, i.i.d. case).** With probability `≥ 1 − δ` over an i.i.d.
sample, `sup_{h ∈ H} |R(h) − R̂_n(h)| ≤ 2ℜ_n(H) + √(ln(1/δ)/(2n))`, where `ℜ_n(H)` is the
Rademacher complexity. See Vapnik [1] and Shalev-Shwartz & Ben-David [2].

**The i.i.d. hypothesis fails for every application contemplated in this module set.** Two
repairs exist in the literature, and both weaken the bound:

- **Mixing-based bounds.** For stationary `β`-mixing sequences, blocking arguments recover
  bounds with an *effective* sample size smaller than `n` by a factor determined by the mixing
  rate. See Yu (1994) [3] and Mohri & Rostamizadeh (2009) [4].
- **Non-stationary bounds.** Kuznetsov & Mohri (2015) [5] give bounds involving a *discrepancy*
  term measuring how far the future distribution is from the training one. That term does not
  vanish with more data — which is the formal statement of the note's Challenge 3.

**Consequence.** "More data" does not fix non-stationarity. A hundred years of daily observations
does not reduce the discrepancy between the 2008 mechanism and the 2020 mechanism, and no amount
of it converts `~20` events into a large sample.

### 2.2 Distribution shift, taxonomised

Following Quiñonero-Candela, Sugiyama, Schwaighofer & Lawrence [6]:

- **Covariate shift**: `P(X)` changes, `P(Y|X)` fixed. Correctable by importance weighting when
  supports overlap.
- **Label / prior shift**: `P(Y)` changes, `P(X|Y)` fixed. Correctable if the new prior is known.
- **Concept drift**: `P(Y|X)` itself changes. **Not correctable** — the relationship being learned
  has changed. The note's "2008 ≠ 2020 (different mechanism)" is a concept-drift claim, the one
  category with no statistical remedy.

### 2.3 Cross-validation and its failure modes on dependent data

**Theorem 2.4 (Why plain `k`-fold fails).** `k`-fold CV is (nearly) unbiased for i.i.d. data. Under
serial dependence, training and validation folds share information, so `R̂_CV` is optimistically
biased. Arlot & Celisse [7] survey the i.i.d. theory; Bergmeir & Benítez [8] document the failure
and the remedies for time series; Bergmeir, Hyndman & Koo [9] give the important refinement that
for purely autoregressive models with uncorrelated errors, standard CV can in fact remain valid —
so the blanket prohibition is too strong, and the correct statement is conditional on the model
class and the error structure.

**Valid designs.**

1. **Rolling-origin / walk-forward evaluation** (Tashman [10]; Hyndman & Athanasopoulos [11]).
   Train on `[1, t]`, predict `[t+1, t+h]`, advance `t`. This is precisely the note's
   "Walk-forward testing" and it is the right skeleton. Two variants must be distinguished
   explicitly, because they answer different questions: an **expanding window** (the note's
   `[1990, t−1]`) assumes parameter stability, while a **rolling fixed window** adapts to drift.
2. **Blocked CV.** Contiguous blocks as folds, preserving within-block dependence.
3. **Purging and embargoing** (López de Prado [12]). When labels are formed over a horizon `h`,
   any training observation whose label window overlaps a validation observation must be *purged*;
   an additional *embargo* of length proportional to the serial-correlation scale is applied after
   each validation block, because serial correlation leaks forward even without overlap. Combinatorial
   purged cross-validation extends this to multiple train/test splits.
4. **Nested CV.** Model *selection* must happen inside an inner loop. Reporting the best inner-loop
   score as a performance estimate is the most common leakage in applied work — the outer loop
   exists precisely to price the selection.

**Warning 2.5 (Preprocessing leakage).** Normalisation, imputation, feature scaling, outlier
removal and regime labelling must all be fitted **inside** the training fold. Fitting a scaler on
the full series before splitting is leakage, and it is silent — it inflates every downstream score
without producing any error message. The note's architecture diagram in **I1** places
"Data Preprocessing & Normalization" *above* the model branches, which is exactly the position
that invites this mistake.

### 2.4 Comparing predictive accuracy

**Theorem 2.6 (Diebold & Mariano, 1995 [13]).** For loss differentials `d_t = ℓ(e_{1t}) − ℓ(e_{2t})`
with mean `μ`, under `H₀ : μ = 0` and suitable regularity, `DM = d̄ / √(2πf̂_d(0)/n) → N(0,1)`,
where `f̂_d(0)` is a consistent estimate of the spectral density at frequency zero (a HAC estimator
is required — the autocorrelation of `d_t` is exactly the point).

**Remark 2.7 (Correct use).** Diebold [14] revisits the test twenty years on and is explicit: it
compares *forecasts*, not *models*, and it was never intended for nested model comparison, where
the statistic is non-standard under the null. For nested models use Clark & West [16]; for
conditional (as opposed to unconditional) predictive ability use Giacomini & White [15], which also
handles estimation uncertainty from a rolling scheme. West [17] gives the asymptotics for
predictive ability when parameters are estimated.

### 2.5 Multiple testing and data snooping — the dominant problem

**Proposition 2.8 (Expected maximum under the null).** Let `Z₁, …, Z_N` be independent standard
normals. Then `E[max_i Z_i] ≈ √(2 ln N)`, and more precisely
`√(2 ln N) − (ln ln N + ln 4π)/(2√(2 ln N)) ≤ E[max_i Z_i] ≤ √(2 ln N)`.

| `N` configurations searched | `√(2 ln N)` | Reading |
|---|---|---|
| 10 | 2.15 | A `t` of 2.1 is the *expected* best of ten worthless models |
| 100 | 3.03 | The conventional `t > 3` bar is met by noise |
| 1,000 | 3.72 | |
| 10,000 | 4.29 | |

Across eleven discussion modules, each with several tunable parameters, `N` in the thousands is
not a pessimistic estimate. Correlated trials reduce the effective `N` somewhat but never to one.

**Formal procedures.**

- **White's Reality Check** [18]: a bootstrap test of whether the best of `N` models beats a
  benchmark, correcting for the search.
- **Hansen's Test for Superior Predictive Ability** [19]: improves power by removing
  poor-performing models from the null.
- **Romano & Wolf stepwise multiple testing** [20]: identifies *which* models beat the benchmark
  with family-wise error control.
- **Benjamini & Hochberg** [21]: false-discovery-rate control — appropriate when the goal is a
  screening list rather than a single confirmed claim.

**Backtest overfitting specifically.** Bailey, Borwein, López de Prado & Zhu [22] show that with
enough trials an in-sample-optimal configuration is expected to underperform out of sample, derive
the minimum track-record length needed for a claim, and introduce the deflated performance
statistic that adjusts for the number of trials [23]. Harvey, Liu & Zhu [24] apply the same
multiple-testing logic to the published asset-pricing literature and conclude that a substantial
fraction of accepted findings would not survive an appropriate threshold. Ioannidis [25] gives the
general form of the argument.

### 2.6 Evaluating rare events

With roughly 20 positives against tens of thousands of periods, base rates dominate.

**Proposition 2.9 (ROC is misleading under extreme imbalance).** The false-positive rate has the
number of negatives in its denominator, so a large absolute number of false alarms yields a
negligible FPR. Precision — `TP/(TP+FP)` — has the number of *predicted positives* in its
denominator and is therefore the informative axis. Davis & Goadrich [26] establish the
dominance relationship between ROC and precision–recall space; Saito & Rehmsmeier [27] give the
empirical case for preferring PR curves under imbalance.

**Worked illustration.** 20 crises in 25,000 monthly-equivalent periods (base rate `0.08%`). A
detector with `80%` recall and a `5%` false-alarm rate produces `16` true positives and
`0.05 × 24,980 ≈ 1,249` false positives. Precision is `16/1,265 ≈ 1.3%`. Its ROC curve looks
excellent. It cries wolf 78 times for each real event.

**The early-warning literature reached this conclusion decades ago.** Kaminsky, Lizondo & Reinhart
[28] introduced the noise-to-signal ratio for exactly this reason; Berg & Pattillo [29] evaluated
those indicators out of sample and found materially weaker performance than in-sample results
suggested. Any new crisis-detection claim should be benchmarked against that literature rather
than against a naive baseline.

**Proper scoring.** Use the Brier score with its Murphy decomposition, or the log score, plus a
reliability diagram. Hit rate and false-alarm rate at one threshold discard the whole
calibration curve. A *utility-weighted* loss — stating the cost ratio of a missed crisis to a
false alarm — makes the implicit decision problem explicit and should accompany any threshold.

### 2.7 How many crises are there, actually?

The note says "~20 major crises in ~70 years". The number is definition-dependent and worth
pinning down, because it is the effective sample size:

- **Laeven & Valencia [30]** identify **151 systemic banking crises** worldwide over 1970–2017,
  alongside currency and sovereign-debt crisis counts, under explicit quantitative criteria.
- **Reinhart & Rogoff [31]** cover eight centuries and a wider taxonomy.
- Restricted to *major, globally systemic* events in advanced economies, a count in the range the
  note gives is reasonable.

The methodological point is that the count is a *choice*, that the choice determines power, and
that cross-country events are strongly correlated — 2008 was not `N` independent national
observations. Any power calculation must use an effective, not nominal, event count.

---

## 3. Academic curriculum modules

| Module | Level | Canonical courses | Core texts | What AMF needs from it |
|---|---|---|---|---|
| Mathematical statistics | Advanced undergraduate | Standard theory-of-statistics sequences | Casella & Berger, *Statistical Inference* | Estimation, testing, power, sampling distributions |
| Statistical learning & model selection | Graduate | Stanford STATS315 / CS229; CMU 10-701 | Hastie, Tibshirani & Friedman [32] **Ch. 7** | Bias–variance, CV, AIC/BIC, the optimism of the training error |
| Learning theory | Graduate | MIT 9.520; CMU 36-708 | Shalev-Shwartz & Ben-David [2]; Mohri, Rostamizadeh & Talwalkar | Uniform convergence; and the dependent-data extensions [3,4,5] |
| Time-series econometrics | Graduate | MIT 14.382; econometrics sequences at LSE, Oxford, Chicago | Hamilton, *Time Series Analysis*; Diebold, *Forecasting* | Stationarity, HAC estimation, forecast evaluation |
| Forecast evaluation | Graduate | Forecasting topics courses | Diebold & Mariano [13]; Diebold [14]; Giacomini & White [15] | DM and its correct scope; conditional predictive ability |
| Multiple testing | Graduate | Modern statistics sequences | Benjamini & Hochberg [21]; Romano & Wolf [20]; Efron, *Large-Scale Inference* | FWER, FDR, stepwise procedures, data snooping |
| Rare-event & imbalanced evaluation | Graduate | ML evaluation topics; epidemiology courses | Davis & Goadrich [26]; Gneiting & Raftery | PR vs ROC, calibration, utility-weighted loss |
| Simulation verification & validation | Graduate / practitioner | Simulation modelling courses | Sargent, "Verification and Validation of Simulation Models" (Winter Simulation Conference) | **The distinction §5.4 turns on** |
| Reproducible research | All | Increasingly embedded in methods courses | Ioannidis [25]; pre-registration literature | Pre-specification, hidden test sets, honest reporting |

---

## 4. Exact source material

### 4.1 Cross-validation and evaluation design

- **Arlot, S. and Celisse, A.** "A survey of cross-validation procedures for model selection."
  *Statistics Surveys* **4**, 40–79 (2010).
- **Bergmeir, C. and Benítez, J. M.** "On the use of cross-validation for time series predictor
  evaluation." *Information Sciences* **191**, 192–213 (2012).
- **Bergmeir, C., Hyndman, R. J. and Koo, B.** "A note on the validity of cross-validation for
  evaluating autoregressive time series prediction." *Computational Statistics & Data Analysis*
  **120**, 70–83 (2018). The important qualification to the blanket prohibition.
- **Tashman, L. J.** "Out-of-sample tests of forecasting accuracy: an analysis and review."
  *International Journal of Forecasting* **16**(4), 437–450 (2000). Rolling-origin evaluation.
- **Hyndman, R. J. and Athanasopoulos, G.** *Forecasting: Principles and Practice.* 3rd edition,
  OTexts, 2021. The time-series cross-validation section is the clearest practical treatment, and
  the book is freely available.
- **Hastie, T., Tibshirani, R. and Friedman, J.** *The Elements of Statistical Learning.*
  2nd edition, Springer, 2009. **Chapter 7** — model assessment and selection; §7.10 on the right
  and wrong ways to cross-validate is the canonical statement of Warning 2.5.

### 4.2 Comparing forecasts

- **Diebold, F. X. and Mariano, R. S.** "Comparing Predictive Accuracy." *Journal of Business &
  Economic Statistics* **13**(3), 253–263 (1995).
- **Diebold, F. X.** "Comparing Predictive Accuracy, Twenty Years Later: A Personal Perspective on
  the Use and Abuse of Diebold–Mariano Tests." *Journal of Business & Economic Statistics*
  **33**(1), 1–9 (2015). Read this *with* the original; it is the author telling you what the test
  is not for.
- **Giacomini, R. and White, H.** "Tests of Conditional Predictive Ability." *Econometrica*
  **74**(6), 1545–1578 (2006).
- **Clark, T. E. and West, K. D.** "Approximately normal tests for equal predictive accuracy in
  nested models." *Journal of Econometrics* **138**(1), 291–311 (2007).
- **West, K. D.** "Asymptotic Inference about Predictive Ability." *Econometrica* **64**(5),
  1067–1084 (1996).

### 4.3 Data snooping and overfitting

- **White, H.** "A Reality Check for Data Snooping." *Econometrica* **68**(5), 1097–1126 (2000).
- **Hansen, P. R.** "A Test for Superior Predictive Ability." *Journal of Business & Economic
  Statistics* **23**(4), 365–380 (2005).
- **Romano, J. P. and Wolf, M.** "Stepwise Multiple Testing as Formalized Data Snooping."
  *Econometrica* **73**(4), 1237–1282 (2005).
- **Benjamini, Y. and Hochberg, Y.** "Controlling the False Discovery Rate: A Practical and
  Powerful Approach to Multiple Testing." *Journal of the Royal Statistical Society, Series B*
  **57**(1), 289–300 (1995).
- **Bailey, D. H., Borwein, J. M., López de Prado, M. and Zhu, Q. J.** "Pseudo-Mathematics and
  Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance."
  *Notices of the American Mathematical Society* **61**(5), 458–471 (2014). **The single most
  relevant paper to this module**, and the one whose argument the source note's strategy section
  is most exposed to.
- **Bailey, D. H. and López de Prado, M.** "The Deflated Sharpe Ratio: Correcting for Selection
  Bias, Backtest Overfitting and Non-Normality." *The Journal of Portfolio Management* **40**(5),
  94–107 (2014).
- **Harvey, C. R., Liu, Y. and Zhu, H.** "… and the Cross-Section of Expected Returns."
  *The Review of Financial Studies* **29**(1), 5–68 (2016).
- **Ioannidis, J. P. A.** "Why Most Published Research Findings Are False." *PLoS Medicine*
  **2**(8), e124 (2005).
- **López de Prado, M.** *Advances in Financial Machine Learning.* Wiley, 2018. The standard
  reference for purged `k`-fold and combinatorial purged CV (Ch. 7) and for backtest overfitting
  measures. **Cited with an explicit boundary flag**: the book is framed in trading vocabulary
  throughout — labels, bets, strategies, position sizing — and its methodological content must be
  extracted from that framing before any of it comes near this repository. Use it for the
  purging/embargo construction; do not import its problem statement.

### 4.4 Learning theory under dependence, and distribution shift

- **Vapnik, V. N.** *Statistical Learning Theory.* Wiley, 1998.
- **Shalev-Shwartz, S. and Ben-David, S.** *Understanding Machine Learning: From Theory to
  Algorithms.* Cambridge University Press, 2014.
- **Yu, B.** "Rates of Convergence for Empirical Processes of Stationary Mixing Sequences."
  *The Annals of Probability* **22**(1), 94–116 (1994).
- **Mohri, M. and Rostamizadeh, A.** "Rademacher Complexity Bounds for Non-I.I.D. Processes."
  *Advances in Neural Information Processing Systems* **21** (2009).
- **Kuznetsov, V. and Mohri, M.** "Learning Theory and Algorithms for Forecasting Non-Stationary
  Time Series." *Advances in Neural Information Processing Systems* **28** (2015).
- **Quiñonero-Candela, J., Sugiyama, M., Schwaighofer, A. and Lawrence, N. D. (eds.)**
  *Dataset Shift in Machine Learning.* MIT Press, 2009.

### 4.5 Rare events, crises and early warning

- **Davis, J. and Goadrich, M.** "The Relationship Between Precision-Recall and ROC Curves."
  *Proceedings of the 23rd International Conference on Machine Learning (ICML)*, 233–240 (2006).
- **Saito, T. and Rehmsmeier, M.** "The Precision-Recall Plot Is More Informative than the ROC
  Plot When Evaluating Binary Classifiers on Imbalanced Datasets." *PLoS ONE* **10**(3), e0118432
  (2015).
- **Kaminsky, G., Lizondo, S. and Reinhart, C. M.** "Leading Indicators of Currency Crises."
  *IMF Staff Papers* **45**(1), 1–48 (1998).
- **Berg, A. and Pattillo, C.** "Predicting currency crises: The indicators approach and an
  alternative." *Journal of International Money and Finance* **18**(4), 561–586 (1999). The
  out-of-sample reality check on the previous entry — read them as a pair.
- **Laeven, L. and Valencia, F.** "Systemic Banking Crises Database II." *IMF Economic Review*
  **68**, 307–361 (2020). The event counts of §2.7.
- **Reinhart, C. M. and Rogoff, K. S.** *This Time Is Different: Eight Centuries of Financial
  Folly.* Princeton University Press, 2009.

---

## 5. Derivation for the AMF setting

### 5.1 The power calculation nobody runs

Take the note's premise at face value: `~20` events. Suppose an indicator is evaluated for whether
it rises in the 6 months before an event, and treat each event as one Bernoulli trial.

```
Events:                     n = 20
Null hit rate:              p₀ = 0.30   (the indicator rises before 30% of events by chance)
Alternative:                p₁ = 0.60
Two-sided α:                0.05
Approximate power at n=20:  ≈ 0.60
Events needed for 80% power: ≈ 33
```

Twenty events cannot reliably detect a *doubling* of the hit rate. And that is the single-test
calculation. Fold in Proposition 2.8 with `N = 100` configurations and the required effect size
grows further. Two structural consequences:

- **Cross-country events are correlated.** Counting 2008 as many national observations inflates
  `n` without adding information. Effective `n` is closer to the number of distinct global
  episodes.
- **Pre-registration is not optional at this sample size.** With `n ≈ 20` the difference between a
  pre-specified test and a post-hoc one is the difference between evidence and none.

### 5.2 What the note's walk-forward design gets right, and what it under-specifies

The skeleton — train `[1990, t−1]`, predict `[t, t+1]`, advance `t` — is a correct rolling-origin
design (Tashman [10]). Six details decide whether an implementation of it is valid:

| Detail | Note's specification | What is required |
|---|---|---|
| Window type | `[1990, t−1]` — expanding | State it and justify it. Expanding assumes parameter stability, which Challenge 3 denies. Report rolling-window results alongside |
| Purge / embargo | Not mentioned | Mandatory whenever labels span a horizon (López de Prado [12]). Without it, `[1990, t−1]` and `[t, t+1]` overlap in label space |
| Preprocessing fit | Diagram places it before the split (**I1**) | Must be fitted inside each training window (Warning 2.5) |
| Model selection | Not mentioned | Nested: an inner loop for selection, the outer loop for reporting |
| Multiple testing | Not mentioned | White [18] / Hansen [19] over the full configuration set; report `N` |
| Test statistic | "Record error" | A DM-type test with HAC variance [13,14], or Giacomini–White [15] for the rolling scheme |

The note's diagnostic question — *"Does error increase before crises (less predictable)?"* — is
genuinely good and is more defensible than crisis detection itself. It is a claim about
*predictability*, testable against a surrogate null, and it does not require the model to be right
about anything, only for its errors to be structured.

### 5.3 The metric list needs one deletion and several additions

| Note's metric | Verdict |
|---|---|
| RMSE (accuracy) | Fine as a point-forecast summary. Not a proper score for distributional forecasts; pair with CRPS or the log score |
| **Sharpe ratio (risk-adjusted returns if traded on signals)** | **Delete.** A trading-performance metric, and the clearest single boundary violation in the source note (§6) |
| Hit rate (% of crises detected 1–6 months early) | Keep, but report the full PR curve, not one threshold, and state the base rate |
| False alarm rate (% of false positives) | Keep, and add **precision**, which is the informative axis under imbalance (Proposition 2.9) |

Add: Brier score with the Murphy decomposition; a reliability diagram; the noise-to-signal ratio
of the early-warning literature [28] for comparability; and a utility-weighted loss with the
missed-crisis-to-false-alarm cost ratio stated explicitly.

### 5.4 The distinction this module exists to draw: verification is not validation

Standard terminology in simulation methodology:

- **Verification** — *did we build the thing right?* Does the implementation match the
  specification?
- **Validation** — *did we build the right thing?* Does the model correspond to reality?

Set against those definitions, the repository's position is unusual and worth stating precisely:

| | AMF's status |
|---|---|
| **Verification** | **Strong, and unusually so.** 100% statement-and-branch coverage; Hypothesis property tests asserting the invariants the docstrings promise (stress stays in `[0,1]`, scores stay in `[0,1]` for any weight blend, `to_dict`/`from_dict` is a fixed point, feedback-loop enumeration matches brute force, permutation-invariance of diagnosis); a mechanical non-trading naming guard with a meta-test that keeps its allowlist honest; packaging invariants; byte-identical determinism checks on renderers |
| **Validation** | **Absent, and explicitly disclaimed.** Thresholds, weights and scores are not empirically validated; output is not financial advice, not a diagnosis, not a forecast |

That is a coherent and defensible position for an educational instrument, and the repository is
unusual in stating it plainly rather than letting a reader assume otherwise. **The risk this
module guards against is the conflation**: a reader who sees "100% coverage, property-tested,
deterministic" may infer the *model* has been validated, when what has been verified is the
*code*. Every artefact produced under I2 should make the distinction explicit in its own text.

A further consequence: `reports/model_performance_2024.md`, the note's final deliverable, is a
validation artefact by name. Publishing a performance report from this repository would assert
exactly the claim the charter forbids — and the repository is public, so such a file is a public
claim regardless of intent.

### 5.5 What *can* be validated inside the boundary

Because AMF is a deterministic function from structural configurations to structural scores, a
great deal is testable without any market data at all — and none of it requires a predictive
claim:

1. **Metamorphic testing.** Properties of the form "if I change the input this way, the output
   must change that way": raising `redundancy` must not raise `fragility`; adding a dependency edge
   must not decrease `concentration` for the source system; raising `criticality` must not lower a
   system's contribution to the overall index. Metamorphic relations are the standard technique for
   systems with no test oracle, which is exactly AMF's situation.
2. **Monotonicity and boundary behaviour.** Every derived quantity should be checked at the corners
   of `[0,1]⁴` per system, and its monotonicity in each metric asserted or explicitly documented as
   non-monotone.
3. **Invariance.** Permutation invariance is already tested. Add: relabelling invariance, and
   invariance to splitting one coupling across `kind`s (the docs already promise this — "splitting
   one coupling across kinds never changes a score" — so it should be a property test).
4. **Sensitivity of the published weights.** The `0.4/0.3/0.3` and `0.6/0.25/0.15` blends are
   unvalidated choices. Perturbing them and measuring ranking stability is an *internal* validity
   study needing no market data, and it is the most consequential open question in the set
   (module **I1**, P5).
5. **Cross-module concordance.** Do the diagnostic index, the resilience score, the `H₂` barcode
   summaries and the `H₃` dissipativity certificate rank a corpus of synthetic markets
   concordantly? Rank correlation is computable, meaningful, and claims nothing about reality.
6. **Structural retrodiction, carefully framed.** Encode historical market *structures* — the
   documented configuration of infrastructure, liquidity provision, regulation — as AMF markets,
   and ask whether the resulting structural indices order them in a way domain experts endorse.
   This is expert-elicitation validation of a descriptive instrument, not forecasting, and it is
   the strongest form of validation available inside the charter. Its limits should be stated:
   expert agreement is not ground truth, and hindsight contaminates the encoding.

Items 1–5 belong in this repository. Item 6 is a research programme; the encoding step alone is
substantial and would need its own protocol to avoid hindsight bias.

### 5.6 A pre-registration template for any sidecar study

Anything in the out-of-tree sidecar that touches real data should fix, before looking at outcomes:

```
1. Hypothesis           — one sentence, directional, refutable
2. Event definition     — the crisis list and its source (e.g. Laeven & Valencia [30]);
                          fixed before analysis
3. Effective n          — number of independent episodes, not observations; with the power
                          calculation at the stated effect size
4. Configuration count  — N, fixed in advance; the multiple-testing correction named
5. Split protocol       — window type, purge length, embargo length, nesting
6. Metrics              — primary metric named in advance; PR curve and calibration reported
7. Null model           — surrogate construction (matched autocorrelation and tail index)
8. Stopping rule        — what would make the team abandon the hypothesis
9. Hidden test set      — sealed at the outset, opened once, result reported whatever it is
```

Item 9 is the note's own Robustness Check 4 and it is the only one that cannot be retrofitted. If
the hidden set is opened and the result is negative, that negative result is the deliverable.

### 5.7 On the note's four robustness checks

| Check | Assessment |
|---|---|
| 1. Cross-market: train on equities, test on bonds | Sound in principle; tests covariate shift. Note the two are strongly coupled, so it is a weaker independence test than it appears |
| 2. Cross-asset: developed → emerging | The strongest of the four — genuinely different microstructure and institutions |
| 3. Cross-crisis: 2008 → 2020 | Tests concept drift directly, and is `n = 1` in each direction. Suggestive at best; cannot support a quantitative claim |
| 4. Out-of-sample hidden test set | Essential, and must be *sealed before development begins*. A test set "not used during development" that was available to the team is not hidden — see §5.6 item 9 |

Check 3 deserves emphasis. Comparing two episodes is a case study, and a case study is a legitimate
form of evidence provided it is not reported with a `p`-value attached.

---

## 6. Repository governance and boundary analysis

This module has the most severe boundary conflicts in the set. They are listed exhaustively.

| Proposed artefact | Conflict | Compliant reformulation |
|---|---|---|
| `src/amf/backtest/walk_forward_validator.py` | **Non-trading boundary**: `backtest` is on the mechanically enforced `FORBIDDEN` substring list. The import path alone fails the guard | No compliant in-package form. Walk-forward evaluation of predictions against market outcomes is out of scope for a package that models structure. Move entirely to the sidecar |
| `src/amf/backtest/metrics.py` | Same `backtest` path conflict | Structural-consistency metrics (§5.5 items 1–5) belong in `tests/`, not in the shipped package. A metamorphic-property test suite is the right home |
| **"Sharpe ratio (risk-adjusted returns if traded on signals)"** | **Non-trading boundary, threefold**: `returns`, `trade`, `signal`. And substantively — a metric scoring a strategy's profitability is a trading system's evaluation criterion. This is the charter's central exclusion, not an edge case | **Delete.** No reformulation. If profitability is the question being asked, the question is outside this project |
| `examples/backtest_crisis_detection.py` | `backtest` in the filename; predictive claim over market data | `examples/structural_consistency_checks.py`: metamorphic relations and invariance properties over AMF markets. Emit the `_DISCLAIMER`; add to `tests/integration/test_examples.py` |
| `reports/model_performance_2024.md` | **Illustrative, not validated** — a performance report asserts validated performance. The repository is public, so publishing it is a public claim (§5.4) | If internal-consistency studies (§5.5) are run, report them as `docs/` studies with explicit "internal consistency, not predictive validation" framing, and no aggregate performance number |
| `docs/research/validation_and_backtesting.md` | Filename contains `backtest`, but it is a doc path, not a Python name, so the guard does not reach it. Still misleading | Superseded by this module |
| "train on data", "predict on" | Implies fitted parameters. AMF's parameters are fixed, documented and declared illustrative | Any learned-parameter work is sidecar work, gated by §5.6 |

**A note on how the guard actually works.** `tests/unit/test_non_trading_boundary.py` walks every
public class reachable from `amf.__all__` and checks public names *and* every member and dataclass
field against the `FORBIDDEN` list. A module at `src/amf/backtest/` is caught the moment anything
in it is exported. The one documented exception, `CouplingMatrix.order`, is protected by a
meta-test asserting every allowlist entry still exists — so stale exemptions fail the build. **Do
not add entries to that allowlist to accommodate this module.** The guard constrains naming
precisely so that it constrains scope; widening it to admit `backtest` would remove the
mechanism that keeps the charter enforceable.

**Determinism.** Any evaluation harness must be seeded explicitly, iterate in canonical order, and
produce byte-identical output for identical inputs — the same standard the renderers already meet.

---

## 7. Falsifiable propositions and open questions

**P1 (Power).** With `n ≈ 20` effective events, no study in this module set can detect an effect
smaller than roughly a doubling of the base hit rate at conventional levels. *Refuted if*: a
formal power calculation with a defensible effective `n` shows adequate power at a smaller effect
size — which would require either many more independent episodes or a much larger effect than the
early-warning literature has found.

**P2 (Multiple testing dominates).** Across the eleven modules and their parameters, `N` is large
enough that the expected best `t`-statistic under the null exceeds 3. *Refuted if*: the
configuration space is pre-registered and small, or the trials are correlated enough that the
effective `N` is an order of magnitude smaller — which is itself measurable.

**P3 (Plain CV is optimistic here).** For any model in this set evaluated on serially dependent
data, plain `k`-fold CV yields a materially better score than purged-and-embargoed CV on the same
data. *Refuted if*: the gap is negligible — which, per Bergmeir, Hyndman & Koo [9], is possible for
purely autoregressive models with uncorrelated errors, so the proposition is genuinely at risk and
worth testing rather than assuming.

**P4 (Precision collapses).** Any detector achieving useful recall on crises has precision below
10% at realistic base rates. *Refuted if*: a detector achieves both high recall and precision
above 10% out of sample with pre-registered parameters. This is the single most consequential
empirical claim in the set.

**P5 (Verification–validation conflation is real).** Readers shown AMF's coverage and
property-test discipline infer that the model has been empirically validated. *Refuted if*: a
structured reader study finds they do not. Unusual as a research proposition, but it is the risk
§5.4 is written to mitigate, and it is testable.

**P6 (Internal concordance).** The structural members of module **I1** rank a corpus of synthetic
markets concordantly. *Refuted if*: rank correlations are near zero — which would mean the modules
measure unrelated things and no composite index is meaningful.

**Open questions.**

1. What *is* the ground truth for a structural resilience instrument? If no observable exists,
   is expert elicitation (§5.5 item 6) the ceiling, and how should inter-rater reliability be
   reported?
2. Can metamorphic relations (§5.5 item 1) be made exhaustive enough to substitute for an oracle?
   What is the complete set of monotonicity claims AMF's design implies?
3. Should the repository add an explicit `VALIDATION.md` stating the verification/validation
   distinction of §5.4, so that the claim is documented rather than inferred from `CLAUDE.md`?
4. If a sidecar study returns a negative result under §5.6, where is it published? A negative
   result that is never written up recreates the file-drawer problem the whole module opposes.

---

## 8. Deliverables

Reproduced from the source note, with a compliance column:

| Deliverable (verbatim) | Status | Compliance note |
|---|---|---|
| `docs/research/validation_and_backtesting.md` — Methodology | Superseded by this module | Filename would be misleading; no code-level conflict |
| `src/amf/backtest/walk_forward_validator.py` — Walk-forward testing | **Blocked** | `backtest` is a `FORBIDDEN` substring; the concept is out of scope for a structural package. Sidecar only |
| `src/amf/backtest/metrics.py` — Hit rate, false alarm rate, etc. | **Blocked** | Same path conflict. Structural-consistency metrics belong in `tests/` |
| `examples/backtest_crisis_detection.py` — Test all models | **Blocked** | Reformulate as `examples/structural_consistency_checks.py` |
| `reports/model_performance_2024.md` — Annual results | **Blocked** | A performance report asserts validated performance, in a public repository |

**Research Leaders Needed**: Quantitative analyst, statistician

This module blocks more than it builds, and that is the correct outcome. Its value to the
repository is the discipline in §5.5 and §5.6 — the list of what genuinely *can* be checked inside
the boundary, and the protocol anything outside it must follow. A validation module that approved
everything would be worthless.

---

## 9. Research leadership and prerequisites

**Skills matrix.**

| Role | Must have | Should have | Will own |
|---|---|---|---|
| Statistician | Multiple testing; power analysis; proper scoring; rare-event evaluation | Learning theory under dependence | §5.1 power calculations; P1, P2, P4; the §5.6 protocol |
| Quantitative analyst | Rolling-origin evaluation; purging and embargoing; DM-family tests | The early-warning literature [28,29] | §5.2 split protocol; P3; benchmarking against prior work |
| Software engineer / SDET | Metamorphic testing; property-based testing; coverage discipline | Hypothesis; mutation testing | §5.5 items 1–3; the `tests/` suite |
| AMF maintainer | The hard rules and the naming guard's mechanics | The verification history in `CLAUDE.md` | §6 boundary calls; open question 3 |

**Prerequisite ladder.**

```
Mathematical statistics (estimation, testing, power)
                    │
                    ▼
        Model assessment & selection (ESL Ch. 7)
                    │
      ┌─────────────┼──────────────────┬────────────────────┐
      ▼             ▼                  ▼                    ▼
 Time-series   Cross-validation   Multiple testing    Rare-event
 econometrics  under dependence   [18,19,20,21]       evaluation
 (HAC, DM)     [8,9,10,12]              │             [26,27,28]
      │             │                   │                    │
      └─────────────┴─────────┬─────────┴────────────────────┘
                              ▼
              Backtest overfitting [22,23,24] + Ioannidis [25]
                              ▼
              Verification vs validation (§5.4) — the gate
                              ▼
                    Pre-registration protocol (§5.6)
```

**This module gates the other ten.** No proposition from Q1–Q3, D1–D3, H1–H3 or I1 that concerns
real markets should be tested before its protocol is agreed here. That ordering is why `I2` sits
last in the prerequisite map in `docs/discussions/README.md`, and it is the one sequencing
constraint in the whole set that should not be relaxed for convenience.

---

## References

[1] Vapnik, V. N. *Statistical Learning Theory.* Wiley, New York, 1998.

[2] Shalev-Shwartz, S. and Ben-David, S. *Understanding Machine Learning: From Theory to
Algorithms.* Cambridge University Press, Cambridge, 2014.

[3] Yu, B. "Rates of Convergence for Empirical Processes of Stationary Mixing Sequences."
*The Annals of Probability* **22**(1), 94–116 (1994).

[4] Mohri, M. and Rostamizadeh, A. "Rademacher Complexity Bounds for Non-I.I.D. Processes."
*Advances in Neural Information Processing Systems* **21** (2009).

[5] Kuznetsov, V. and Mohri, M. "Learning Theory and Algorithms for Forecasting Non-Stationary
Time Series." *Advances in Neural Information Processing Systems* **28** (2015).

[6] Quiñonero-Candela, J., Sugiyama, M., Schwaighofer, A. and Lawrence, N. D. (eds.)
*Dataset Shift in Machine Learning.* MIT Press, Cambridge, 2009.

[7] Arlot, S. and Celisse, A. "A survey of cross-validation procedures for model selection."
*Statistics Surveys* **4**, 40–79 (2010).

[8] Bergmeir, C. and Benítez, J. M. "On the use of cross-validation for time series predictor
evaluation." *Information Sciences* **191**, 192–213 (2012).

[9] Bergmeir, C., Hyndman, R. J. and Koo, B. "A note on the validity of cross-validation for
evaluating autoregressive time series prediction." *Computational Statistics & Data Analysis*
**120**, 70–83 (2018).

[10] Tashman, L. J. "Out-of-sample tests of forecasting accuracy: an analysis and review."
*International Journal of Forecasting* **16**(4), 437–450 (2000).

[11] Hyndman, R. J. and Athanasopoulos, G. *Forecasting: Principles and Practice.* 3rd edition,
OTexts, Melbourne, 2021.

[12] López de Prado, M. *Advances in Financial Machine Learning.* Wiley, Hoboken, 2018.

[13] Diebold, F. X. and Mariano, R. S. "Comparing Predictive Accuracy." *Journal of Business &
Economic Statistics* **13**(3), 253–263 (1995).

[14] Diebold, F. X. "Comparing Predictive Accuracy, Twenty Years Later: A Personal Perspective on
the Use and Abuse of Diebold–Mariano Tests." *Journal of Business & Economic Statistics*
**33**(1), 1–9 (2015).

[15] Giacomini, R. and White, H. "Tests of Conditional Predictive Ability." *Econometrica*
**74**(6), 1545–1578 (2006).

[16] Clark, T. E. and West, K. D. "Approximately normal tests for equal predictive accuracy in
nested models." *Journal of Econometrics* **138**(1), 291–311 (2007).

[17] West, K. D. "Asymptotic Inference about Predictive Ability." *Econometrica* **64**(5),
1067–1084 (1996).

[18] White, H. "A Reality Check for Data Snooping." *Econometrica* **68**(5), 1097–1126 (2000).

[19] Hansen, P. R. "A Test for Superior Predictive Ability." *Journal of Business & Economic
Statistics* **23**(4), 365–380 (2005).

[20] Romano, J. P. and Wolf, M. "Stepwise Multiple Testing as Formalized Data Snooping."
*Econometrica* **73**(4), 1237–1282 (2005).

[21] Benjamini, Y. and Hochberg, Y. "Controlling the False Discovery Rate: A Practical and Powerful
Approach to Multiple Testing." *Journal of the Royal Statistical Society, Series B* **57**(1),
289–300 (1995).

[22] Bailey, D. H., Borwein, J. M., López de Prado, M. and Zhu, Q. J. "Pseudo-Mathematics and
Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance."
*Notices of the American Mathematical Society* **61**(5), 458–471 (2014).

[23] Bailey, D. H. and López de Prado, M. "The Deflated Sharpe Ratio: Correcting for Selection
Bias, Backtest Overfitting and Non-Normality." *The Journal of Portfolio Management* **40**(5),
94–107 (2014).

[24] Harvey, C. R., Liu, Y. and Zhu, H. "… and the Cross-Section of Expected Returns."
*The Review of Financial Studies* **29**(1), 5–68 (2016).

[25] Ioannidis, J. P. A. "Why Most Published Research Findings Are False." *PLoS Medicine*
**2**(8), e124 (2005).

[26] Davis, J. and Goadrich, M. "The Relationship Between Precision-Recall and ROC Curves."
*Proceedings of the 23rd International Conference on Machine Learning*, 233–240 (2006).

[27] Saito, T. and Rehmsmeier, M. "The Precision-Recall Plot Is More Informative than the ROC Plot
When Evaluating Binary Classifiers on Imbalanced Datasets." *PLoS ONE* **10**(3), e0118432 (2015).

[28] Kaminsky, G., Lizondo, S. and Reinhart, C. M. "Leading Indicators of Currency Crises."
*IMF Staff Papers* **45**(1), 1–48 (1998).

[29] Berg, A. and Pattillo, C. "Predicting currency crises: The indicators approach and an
alternative." *Journal of International Money and Finance* **18**(4), 561–586 (1999).

[30] Laeven, L. and Valencia, F. "Systemic Banking Crises Database II." *IMF Economic Review*
**68**, 307–361 (2020).

[31] Reinhart, C. M. and Rogoff, K. S. *This Time Is Different: Eight Centuries of Financial
Folly.* Princeton University Press, Princeton, 2009.

[32] Hastie, T., Tibshirani, R. and Friedman, J. *The Elements of Statistical Learning: Data
Mining, Inference, and Prediction.* 2nd edition, Springer, New York, 2009.
