# D3: Neural Connection Pathways & Knowledge Graphs

> **Discussion category**: Research · **Labels**: `theory`, `knowledge-graphs`,
> `causal-inference`, `ontology`, `boundary-review`, `needs-reformulation`, `not-validated`
> **Source**: `docs/QUANTUM_NEURAL_RESEARCH.md` § Discussion D3
> **Status**: Open for comment · **Nature**: Theoretical module, illustrative and not
> empirically validated

## 0. Abstract and reading guide

This module asks what knowledge-graph engineering and causal inference contribute to AMF,
and answers with one observation and one theorem set. The observation is that AMF *is*
already a knowledge graph — a closed ontology of seven concepts, four typed relations, and
at most 168 admissible triples — and that it is small enough that every reasoning problem
which makes description logics and embedding models interesting is either trivial or
vacuous here (§§5.1–5.4). The theorem set is that AMF's stress recursion is a Markovian
structural causal model whose equations are *stipulated rather than estimated*, so the
identification apparatus the note reaches for — Granger causality, instrumental variables,
difference-in-differences — addresses a problem AMF does not have. Inside the boundary the
`do`-operator is exact: `SensitivityAnalyzer` already computes interventional, not
observational, gradients (Corollary 5.14); those gradients have closed forms verified to
machine precision (§5.6); the central difference carries an exactly predicted truncation
error (Theorem 5.15); and "counterfactual simulation through the graph" is Mason's gain
formula on the resolvent `(I − A)^-1`, verified on the sample market to six decimals
(§5.9).

It does **not** claim that any construction here forecasts, diagnoses, or describes a real
market, that AMF's weights correspond to any economic quantity, or that any threshold below
has been empirically validated. Nothing here is financial advice.

**Prerequisite ladder.** Sets, relations, first-order logic → RDF and description-logic
semantics ([1]; [5] Ch. 2–3) → decidability and complexity of DL reasoning ([6]; [7]; [8])
→ graph algorithms: cycles, cut vertices, walk counting ([61]; [62]; [59] Ch. 6) → linear
algebra: resolvents, spectral radius, Perron–Frobenius ([76] Ch. 5, 8) → probability and
conditional independence → Bayesian networks and d-separation ([9]; [10] Ch. 1) →
structural causal models and the do-calculus ([10] Ch. 3; [11]; [13]; [14]) → potential
outcomes, ignorability, propensity scores ([17]; [18]; [21] Ch. 1–3, 12–14) →
quasi-experimental identification: IV/LATE, DiD, RD ([22]; [23]; [26]; [30]; [33]) → time
series, VAR/SVAR, local projections ([36]; [37]; [40]; [41]) → information-theoretic
transfer ([69]; [70]). §2 states what is needed; §5 assumes all of it; §§6–9 assume none.

## 1. Verbatim source specification

The following is the complete text of Discussion D3 as it appears in
`docs/QUANTUM_NEURAL_RESEARCH.md`, reproduced word for word, including its notation,
typography, arrows, spacing, and deliverable paths. It is quoted, not endorsed; §5 develops
it, §6 names where it collides with this repository's hard rules, and §5.12 records one
place where its economics appears to be sign-reversed. (One byte-level caveat: the
repository's `trailing-whitespace` pre-commit hook strips trailing spaces from files under
`docs/`, so the excerpt below is word-exact but not necessarily whitespace-exact once
committed.)

````markdown
### Discussion D3: Neural Connection Pathways & Knowledge Graphs
**Theme**: Map the "wiring diagram" of how policy → markets → stability

**Concept**:
- Knowledge graph: Nodes = concepts (Fed, rate, stock, crisis, ...), Edges = relationships
- Neural connections: Learn which pathways are strongest/weakest

**Structure**:
```
Ontology: Define entity types
  - Actors: Fed, ECB, Treasury, BIS, ...
  - Instruments: Rate, QE, regulation, capital controls, ...
  - Outcomes: Inflation, unemployment, asset prices, volatility, ...
  - Properties: Strictness, transparency, independence, ...

Relations: Define edge types
  - affects (policy → outcome): "rate cut → inflation"
  - modulates (moderates intensity): "transparency → policy effectiveness"
  - conflicts (contradicts): "rate cut → currency devaluation (bad for exports)"
  - time-lag (delayed effect): "QE → inflation (with 6-month lag)"
```

**Knowledge Graph Construction**:

1. **Manual Construction** (domain experts)
   - Economists define relationships based on theory
   - Add edge weights: Strength of relationship
   - Add metadata: Time-lag, uncertainty, historical support

2. **Automatic Extraction** (NLP + ML)
   - Parse research papers, news, policy statements
   - Extract relationships: "Fed raises rate, stock market falls"
   - Link to knowledge graph entities
   - Learn edge weights from frequency + sentiment

3. **Hybrid**: Manual structure + automatic weights
   - Domain experts define node ontology + edge types
   - ML learns edge weights from data

**Neural Connection Learning**:

```
Goal: Learn strongest/weakest pathways from policy to stability

Method 1: Graph attention networks
  - Learn attention weights on each edge
  - High weight = strong influence
  - Low weight = weak/mediocre influence

Method 2: Causal inference
  - Granger causality: Does X help predict Y?
  - Instrumental variables: Exogenous policy shocks
  - Difference-in-differences: Compare markets with/without policy

Method 3: Counterfactual reasoning
  - "If Fed didn't cut rate, what would happen?"
  - Simulate through knowledge graph
  - Compare to actual outcome
```

**Example: Policy Cascade**
```
Fed announces rate cut
  → (affects) Mortgage rates ↓
    → (modulates) Housing demand
      → (time-lag: 3 months) Housing starts
        → (affects) Construction employment
          → (affects) Consumer spending
            → (affects) Corporate earnings
              → (affects) Stock prices ↑

Knowledge graph reveals:
  Strongest path: Fed rate → mortgage rates (immediate)
  Weakest path: Housing starts → stock prices (noisy, 6-month lag)
  Conflict: Rate cut → currency weakness (bad for exporters)
  
Policy insight: Rate cuts help housing/employment, but hurt exporters
  → Tradeoff analysis possible
```

**Interpretability & Transparency**:
- Visualize knowledge graph: Which paths dominate?
- Attribution: Which edges explain policy success/failure?
- Sensitivity: If we change edge weights, how does outcome change?

**Deliverable**:
- `docs/research/neural_knowledge_graphs.md` — Framework
- `docs/taxonomies/financial_policy_ontology.md` — Entity/relation types
- `src/amf/knowledge_graphs/knowledge_graph.py` — Graph structure
- `src/amf/knowledge_graphs/graph_attention_network.py` — Attention learning
- `src/amf/knowledge_graphs/causal_inference.py` — Granger/IV analysis
- `examples/policy_cascade_analysis.py` — Trace pathways

**Research Leaders Needed**: Knowledge engineer, causal inference specialist, NLP expert
````

## 2. Formal foundations

Two literatures meet in this module and they do not share a vocabulary. §§2.1–2.3 give the
knowledge-representation half — what an ontology *is*, what a knowledge graph *is*, what
embedding and attention models can and cannot express. §§2.4–2.7 give the causal half —
structural causal models, potential outcomes, quasi-experimental identification, and the
predictive (not structural) notion of causality that econometrics calls Granger's. §5 uses
both.

### 2.1 Ontologies, RDF graphs, and description logics

**Definition 2.1 (ontology, Gruber [1]).** An ontology is an *explicit specification of a
conceptualization*: a vocabulary of terms together with a body of formal axioms constraining
their interpretation. Studer, Benjamins and Fensel [2] sharpen this to "a formal, explicit
specification of a shared conceptualization" — *formal* meaning machine-readable, *shared*
meaning the commitment is social as well as logical. The note's `Ontology: Define entity
types` block is a conceptualization; it becomes an ontology only when the admissible
interpretations are pinned down by axioms.

**Definition 2.2 (RDF graph [3]).** Fix pairwise-disjoint sets `I` (IRIs), `B` (blank
nodes), `L` (literals). An RDF *triple* is an element of `(I ∪ B) × I × (I ∪ B ∪ L)`,
written `(subject, predicate, object)`. An RDF graph is a set of triples. RDF is a
*directed, edge-labelled multigraph*: parallel edges with distinct predicates between the
same pair of nodes are ordinary, not exceptional.

**Definition 2.3 (description-logic interpretation).** An interpretation `Ⅰ = (Δ^Ⅰ, ·^Ⅰ)`
consists of a non-empty domain `Δ^Ⅰ` and a function mapping each atomic concept `A` to
`A^Ⅰ ⊆ Δ^Ⅰ`, each role `r` to `r^Ⅰ ⊆ Δ^Ⅰ × Δ^Ⅰ`, and each individual `a` to `a^Ⅰ ∈ Δ^Ⅰ`.
The logic `ALC` closes concepts under `⊓`, `⊔`, `¬`, and the quantifiers, with

```
(C ⊓ D)^I = C^I ∩ D^I            (∃r.C)^I = { x : ∃y. (x,y) ∈ r^I and y ∈ C^I }
(C ⊔ D)^I = C^I ∪ D^I            (∀r.C)^I = { x : ∀y. (x,y) ∈ r^I implies y ∈ C^I }
(¬C)^I    = Δ^I \ C^I
```

A knowledge base is a TBox (terminological axioms `C ⊑ D`) plus an ABox (assertions `C(a)`,
`r(a,b)`). The basic reasoning problems are concept satisfiability, subsumption, ABox
consistency and instance checking; all four are interreducible in any logic closed under
negation.

**Theorem 2.4 (Schmidt-Schauß and Smolka [6]).** Concept satisfiability in `ALC` with
respect to the empty TBox is `PSPACE`-complete.

**Theorem 2.5 (Baader, Brandt and Lutz [7]).** Subsumption in `EL++` — the logic with `⊓`,
`⊤`, `∃r.C`, nominals, concrete domains and role inclusions, but *no* negation, disjunction
or universal restriction — is decidable in polynomial time, even with general TBoxes. This
is the tractability result that made OWL 2 EL the profile of choice for large biomedical
terminologies.

**Theorem 2.6 (Horrocks, Kutz and Sattler [8]).** `SROIQ`, the logic underlying OWL 2 DL,
has a decidable but `N2ExpTime`-complete knowledge-base consistency problem.

The point of quoting all three is the contrast in §5.1: this ladder is a statement about
*worst-case behaviour as the domain grows*. On a domain of fixed finite cardinality it
collapses.

**Definition 2.7 (open- vs closed-world assumption).** Under the **open-world assumption**
(OWA), a triple absent from a graph is *unknown*: an interpretation may or may not satisfy
it. Under the **closed-world assumption** (CWA), absence is *negation*: an absent triple is
false. RDF, OWL and every knowledge-graph-completion benchmark are OWA. A schema that
requires the author to enumerate all relations, and treats anything unlisted as absent, is
CWA. The two cannot be mixed without deciding which one the parser implements.

### 2.2 Knowledge-graph embeddings and their expressive limits

**Definition 2.8 (embedding model).** A knowledge-graph embedding assigns each entity `e` a
vector `v_e ∈ K^d` and each relation `r` a parameter `θ_r`, together with a scoring function
`f(h, r, t)` intended to be large on observed triples. The canonical families are

```
TransE   [50]  f(h,r,t) = − || v_h + v_r − v_t ||          (v ∈ R^d)
DistMult [51]  f(h,r,t) = <v_h, diag(v_r), v_t> = Σ_k v_h[k] v_r[k] v_t[k]
ComplEx  [52]  f(h,r,t) = Re <v_h, v_r, conj(v_t)>          (v ∈ C^d)
RotatE   [53]  f(h,r,t) = − || v_h ∘ v_r − v_t ||,  |v_r[k]| = 1  (v ∈ C^d)
```

**Proposition 2.9 (DistMult is relation-symmetric).** For every `h`, `r`, `t`,
`f_DistMult(h,r,t) = f_DistMult(t,r,h)`.

*Proof.* The trilinear form `Σ_k v_h[k] v_r[k] v_t[k]` is symmetric under exchange of `v_h`
and `v_t`. ∎

The corollary matters for AMF: a DistMult-scored graph cannot distinguish `a` depends on `b`
from `b` depends on `a`, and that antisymmetry is exactly what AMF's coupling matrix encodes
(stress flows target → source, the reverse of the dependency arrow). ComplEx repairs this by
scoring with the conjugate, so `f(h,r,t) ≠ f(t,r,h)` in general; RotatE additionally
represents inversion (`r₂ = r₁^-1` as conjugate rotation) and composition (`r₃ = r₁ ∘ r₂` as
composed rotation) [53]. TransE cannot represent symmetric relations except degenerately
(`v_r = 0` forces `v_h = v_t`) and handles one-to-many and many-to-one relations poorly
[50], [54].

**Remark 2.10 (the benchmark caveat).** Reported gains across this family are substantially
smaller than the original papers suggest. FB15k and WN18 leak inverse relations between
train and test, so a model that memorises `r` and `r^-1` scores near-perfectly without
learning anything relational; FB15k-237 [55] and WN18RR [56] were built to remove the leak.
Ruffinelli, Broscheit and Gemulla [57] show that older models under modern training
protocols match or beat later ones, i.e. much of the reported progress was hyperparameter
search. Sun *et al.* [58] document evaluation-protocol flaws that inflate ranking metrics.
Any proposal to bring these models into a repository should quote this literature, not only
the headline papers.

### 2.3 Graph attention and what an attention weight is not

**Definition 2.11 (graph attention coefficient [60]).** For node features `h_i` and a
learned `W`, `a`, the GAT coefficient on edge `(i, j)` is

```
e_ij = LeakyReLU( a^T [ W h_i || W h_j ] )
α_ij = exp(e_ij) / Σ_{k ∈ N(i)} exp(e_ik)
```

so that `Σ_{j ∈ N(i)} α_ij = 1`: the coefficients on a node's neighbourhood lie on the
probability simplex.

**Proposition 2.12 (attention is scale-blind).** Because `α_i·` is a softmax over the
neighbourhood, it is invariant to any transformation of the neighbourhood that preserves the
relative logits, and it carries no information about the *number* or *total magnitude* of
incident couplings beyond what the logits encode. A node with one strong neighbour and a
node with one weak neighbour receive the identical coefficient vector `(1)`.

This is the same degeneracy as a share-based Herfindahl index (§5.4), and AMF already
documents it: `DiagnosticEngine.concentration` scores a single coupling `1.0` at any weight,
which is why `DiagnosticConfig.scale_concentration_by_reliance` exists.

**Remark 2.13 (attention is not explanation).** Jain and Wallace [64] show that on standard
NLP tasks attention weights correlate poorly with gradient-based feature-importance measures
and that adversarial attention distributions can be found which leave predictions unchanged
— so a high attention weight is not evidence that the edge caused the output. Wiegreffe and
Pinter [65] qualify this: the conclusion depends on what "explanation" is being claimed and
on the baseline used, and attention can be a faithful component of a model-level
explanation. The honest reading is that the note's `High weight = strong influence` is a
claim requiring justification, not a definition. Rudin [66] argues the more general case:
where an interpretable model of comparable accuracy exists, post-hoc explanation of an
opaque one is the wrong engineering choice. §5.4 shows AMF is exactly that case.

### 2.4 Structural causal models and the do-calculus

**Definition 2.14 (structural causal model [10] Def. 1.3.1).** An SCM is a tuple
`M = (U, V, F, P(u))` where `U` are exogenous variables, `V = {V_1, …, V_n}` endogenous,
`F = {f_1, …, f_n}` assigns `V_i ← f_i(PA_i, U_i)` with `PA_i ⊆ V \ {V_i}`, and `P(u)` is a
distribution over `U`. The *causal diagram* `G(M)` has a node per variable and an arrow into
`V_i` from each member of `PA_i` and from `U_i`. `M` is **Markovian** if `G(M)` is acyclic
and the `U_i` are jointly independent; **semi-Markovian** if acyclic with dependent or shared
`U`.

**Definition 2.15 (submodel and the do-operator [10] Def. 3.2.1).** For `X ⊆ V` and value
`x`, the submodel `M_x` replaces `f_i` for every `V_i ∈ X` by the constant `x_i`, leaving all
other equations unchanged. The interventional distribution is `P(y | do(x)) := P_{M_x}(y)`.
Intervention is *surgery on the equations*, not conditioning on the observed distribution;
`P(y | do(x)) ≠ P(y | x)` in general.

**Definition 2.16 (d-separation [9]; [10] Def. 1.2.3).** A path `p` is *blocked* by `Z` if it
contains a chain `i → m → j` or fork `i ← m → j` with `m ∈ Z`, or a collider `i → m ← j`
with `m ∉ Z` and no descendant of `m` in `Z`. `Z` d-separates `X` from `Y` if it blocks every
path between them. In a Markovian model, d-separation implies conditional independence, and
the implication is complete for the class of distributions compatible with `G`.

**Theorem 2.17 (truncated factorisation / g-formula; Robins [16], Pearl [10] Thm. 3.2.1).**
In a Markovian model, for `v` consistent with `x`,

```
P(v | do(x)) = Π_{ V_i ∉ X } P(v_i | pa_i)
```

and zero otherwise. Every interventional distribution is therefore a functional of the
observational distribution *whenever every parent set is observed*.

**Theorem 2.18 (three rules of do-calculus; Pearl [11], [10] Thm. 3.4.1).** Let `G` be the
causal diagram, `G_X̄` the graph with all arrows *into* `X` deleted, `G_X̲` with all arrows
*out of* `X` deleted. For disjoint `X, Y, Z, W`:

```
Rule 1 (insert/delete observations)
  P(y | do(x), z, w) = P(y | do(x), w)          if (Y ⫫ Z | X, W) in G_X̄

Rule 2 (action/observation exchange)
  P(y | do(x), do(z), w) = P(y | do(x), z, w)   if (Y ⫫ Z | X, W) in G_X̄Z̲

Rule 3 (insert/delete actions)
  P(y | do(x), do(z), w) = P(y | do(x), w)      if (Y ⫫ Z | X, W) in G_X̄ Z(W)‾
```

where `Z(W)` is the subset of `Z` that are not ancestors of any `W`-node in `G_X̄`.

**Theorem 2.19 (back-door criterion [11]).** `Z` satisfies the back-door criterion relative
to `(X, Y)` if no node of `Z` is a descendant of `X` and `Z` blocks every path from `X` to
`Y` containing an arrow into `X`. Then `P(y | do(x)) = Σ_z P(y | x, z) P(z)`.

**Theorem 2.20 (front-door criterion [11]).** `Z` satisfies the front-door criterion
relative to `(X, Y)` if `Z` intercepts every directed path `X → Y`, there is no unblocked
back-door path from `X` to `Z`, and `X` blocks every back-door path from `Z` to `Y`. Then
`P(y | do(x)) = Σ_z P(z | x) Σ_{x'} P(y | x', z) P(x')`. Front-door identifies an effect in
the presence of unmeasured confounding of `X` and `Y`, which back-door cannot.

**Theorem 2.21 (completeness of the do-calculus; Shpitser and Pearl [13], Huang and Valtorta
[14]).** For semi-Markovian models, `P(y | do(x))` is identifiable from `P(v)` and `G` if and
only if it can be derived by finitely many applications of the three rules; the `ID`
algorithm is a sound and complete decision procedure.

**Definition 2.22 (ladder of causation; counterfactuals [10] §7.1).** Rung 1 is association
`P(y|x)`; rung 2 intervention `P(y|do(x))`; rung 3 counterfactuals `P(Y_x = y | X = x', Y =
y')`. A counterfactual in an SCM is computed in three steps — **abduction** (update `P(u)` on
the evidence), **action** (form `M_x`), **prediction** (compute `Y` in `M_x` under the
updated `P(u)`).

### 2.5 Potential outcomes

**Definition 2.23 (potential outcomes; Neyman, Rubin [17]).** For unit `i` and binary
treatment `D_i`, `Y_i(1)` and `Y_i(0)` are the outcomes that *would* obtain under each arm;
the observed outcome is `Y_i = D_i Y_i(1) + (1 − D_i) Y_i(0)`. The unit-level effect
`Y_i(1) − Y_i(0)` is never observed — the *fundamental problem of causal inference*.

**Definition 2.24 (SUTVA).** The stable-unit-treatment-value assumption requires (i) no
interference: unit `i`'s potential outcomes do not depend on other units' treatments, and
(ii) no hidden versions of treatment.

**Theorem 2.25 (identification under ignorability).** If `(Y(1), Y(0)) ⫫ D | X` and
`0 < P(D = 1 | X) < 1` a.s., then `E[Y(1) − Y(0)] = E_X[ E[Y | D=1, X] − E[Y | D=0, X] ]`.

**Theorem 2.26 (propensity-score balancing; Rosenbaum and Rubin [18]).** With `e(X) = P(D =
1 | X)`, if treatment assignment is strongly ignorable given `X` then it is strongly
ignorable given `e(X)` alone, and `D ⫫ X | e(X)`. A scalar therefore suffices for
adjustment.

**Definition 2.27 (interference; Hudgens and Halloran [19]).** When SUTVA (i) fails,
potential outcomes are indexed by the whole assignment vector, `Y_i(d_1, …, d_n)`. Estimands
must then be defined relative to an *exposure mapping*; Aronow and Samii [20] give design-
based estimators under general interference, and Ogburn and VanderWeele [63] give the
graphical account. **A coupled system such as AMF violates SUTVA by construction** — that is
what a dependency graph *means* — so any transplanted potential-outcomes machinery must
carry an exposure mapping with it (§5.8).

### 2.6 Quasi-experimental identification

**Theorem 2.28 (LATE; Imbens and Angrist [22]; Angrist, Imbens and Rubin [23]).** Let `Z` be
a binary instrument. Under (i) independence, `(Y(·), D(·)) ⫫ Z`; (ii) the exclusion
restriction, `Z` affects `Y` only through `D`; (iii) relevance, `E[D|Z=1] ≠ E[D|Z=0]`; and
(iv) monotonicity, `D_i(1) ≥ D_i(0)` for all `i`; the Wald ratio identifies the effect on
compliers:

```
( E[Y|Z=1] − E[Y|Z=0] ) / ( E[D|Z=1] − E[D|Z=0] ) = E[ Y(1) − Y(0) | D(1) > D(0) ]
```

The exclusion restriction is an *assumption about absent arrows*, untestable from data.

**Definition 2.29 (difference-in-differences and parallel trends).** With two groups and two
periods, the DiD estimand is `(E[Y_{1,post}] − E[Y_{1,pre}]) − (E[Y_{0,post}] −
E[Y_{0,pre}])`; it equals the ATT if untreated potential outcomes would have moved in
parallel. Card and Krueger [26] is the canonical application.

**Theorem 2.30 (Goodman-Bacon decomposition [27]).** With staggered adoption, the two-way
fixed-effects estimator is a weighted average of all `2 × 2` DiD comparisons, including ones
using *already-treated* units as controls. When effects vary over time, those comparisons can
enter with **negative weights**, so the TWFE estimate can lie outside the convex hull of —
indeed carry the opposite sign to — every underlying group-time ATT.

Callaway and Sant'Anna [28] give group-time ATT estimators that avoid the forbidden
comparisons; Sun and Abraham [29] give the event-study analogue; de Chaisemartin and
D'Haultfœuille [30] characterise the negative-weight problem; Borusyak, Jaravel and Spiess
[31] give an efficient imputation estimator.

**Theorem 2.31 (sharp regression discontinuity; Hahn, Todd and van der Klaauw [33]).** If
treatment is `D = 1{X ≥ c}` and `x ↦ E[Y(d) | X = x]` is continuous at `c` for `d ∈ {0,1}`,
then `lim_{x↓c} E[Y|X=x] − lim_{x↑c} E[Y|X=x] = E[Y(1) − Y(0) | X = c]`. Thistlethwaite and
Campbell [32] originated the design; Calonico, Cattaneo and Titiunik [34] give robust
bias-corrected inference for the bandwidth choice.

### 2.7 Granger causality, SVARs, local projections, transfer entropy

**Definition 2.32 (Granger non-causality [36]).** Let `Ω_t` be an information set containing
`X_t` and its history. `X` does **not** Granger-cause `Y` if

```
σ²( Y_{t+1} | Ω_t )  =  σ²( Y_{t+1} | Ω_t \ {X_s : s ≤ t} )
```

that is, if removing `X`'s history leaves the optimal mean-square one-step forecast error of
`Y` unchanged. The definition is entirely about **predictive improvement in a specified
information set**.

**Proposition 2.33 (Granger causality is not structural causality).** Granger's criterion can
diverge from the structural effect for at least four distinct reasons, each documented:
(a) *omitted variables* — a common driver outside `Ω_t` induces spurious Granger causality,
which is why Granger himself insisted the concept is relative to `Ω_t` [38];
(b) *anticipation* — a forward-looking agent responding to expected future values reverses
the apparent direction, so a variable can Granger-cause its own cause;
(c) *temporal aggregation and sampling* — a causal chain fast relative to the sampling
interval can vanish or invert under aggregation;
(d) *non-stationarity* — standard Wald tests on levels of integrated series have
non-standard limits; Toda and Yamamoto [39] give a lag-augmented procedure that restores
asymptotic chi-square inference.
The name is a historical accident; the quantity is predictive.

**Definition 2.34 (SVAR and the identification problem [37]).** A reduced-form VAR
`y_t = Σ_{ℓ=1}^{p} B_ℓ y_{t−ℓ} + u_t`, `E[u_t u_t'] = Σ`, is estimable by OLS equation by
equation. The structural form `A_0 y_t = Σ A_ℓ y_{t−ℓ} + ε_t` with `E[ε_t ε_t'] = I` requires
`u_t = A_0^{-1} ε_t`; `Σ` has `n(n+1)/2` free elements while `A_0` has `n²`, so
**`n(n−1)/2` restrictions must be imposed from outside the data**. Recursive (Cholesky)
ordering, long-run restrictions [42], and sign restrictions [43] are three families of such
assumptions. The impulse-response function `∂ E[y_{t+h}] / ∂ ε_{j,t}` is defined only
relative to a chosen identification.

**Theorem 2.35 (local projections and VARs; Jordà [40]; Plagborg-Møller and Wolf [41]).**
Jordà's local projection estimates the horizon-`h` response by regressing `y_{t+h}` directly
on the impulse at `t` and controls, one regression per horizon. Plagborg-Møller and Wolf
prove that, at population level with the same information set and lag length unrestricted,
local projections and VARs estimate the *same* impulse responses; the estimators differ in
finite-sample bias–variance, not in estimand.

**Definition 2.36 (external-instrument / narrative identification).** Rather than restricting
`A_0`, one supplies an external series correlated with the structural shock of interest and
orthogonal to the others. Romer and Romer [44] construct a narrative measure of monetary
shocks from Federal Reserve records; Kuttner [45] uses federal-funds-futures surprises around
policy announcements; Gertler and Karadi [46] and Stock and Watson [48] embed such series as
proxies in a VAR; Nakamura and Steinsson [49] document that high-frequency surprises also
carry a central-bank *information* component, which violates the exclusion restriction the
design relies on. Ramey [47] surveys the whole apparatus and its fragility.

**Definition 2.37 (transfer entropy; Schreiber [69]).** For processes `X`, `Y` with
histories of order `l`, `k`,

```
T_{X→Y} = I( Y_{t+1} ; X_t^{(l)} | Y_t^{(k)} )
        = Σ p(y_{t+1}, y_t^{(k)}, x_t^{(l)}) log [ p(y_{t+1} | y_t^{(k)}, x_t^{(l)}) / p(y_{t+1} | y_t^{(k)}) ]
```

a conditional mutual information, hence non-negative and zero exactly under conditional
independence.

**Theorem 2.38 (Barnett, Barrett and Seth [70]).** For jointly Gaussian variables the
Granger causality statistic `F_{X→Y}` — the log ratio of restricted to unrestricted residual
variances — satisfies `F_{X→Y} = 2 · T_{X→Y}` in nats. The autoregressive and
information-theoretic notions of directed dependence coincide in the Gaussian case.

This theorem is the formal bridge from D3 to module Q3 (Shannon information and market
entropy): whatever D3 would compute by regression, Q3 would compute by entropy, and on
Gaussian data they are the same number up to a factor of two.

## 3. Academic curriculum modules

The ladder below is the sequence a graduate student would actually take to reach the
research frontier of this module. It has three strands — knowledge representation,
causal inference, and time-series identification — which meet only at the top. A reader
who intends to work on §5 needs the causal strand in full and the representation strand
only to §3 row 3.

| # | Module | Level | Canonical course(s) | Core texts (units that matter) | What AMF needs from it |
|---|--------|-------|---------------------|-------------------------------|------------------------|
| 1 | Logic, sets, relations | Undergraduate | Discrete mathematics / mathematical logic, any research university | Enderton, *A Mathematical Introduction to Logic*, Ch. 1–2 | The meaning of "an interpretation satisfies an axiom" — prerequisite to Def. 2.3 |
| 2 | Knowledge representation and the Semantic Web | Advanced UG / MSc | Stanford CS 520 *Knowledge Graphs*; Vienna/WU and Karlsruhe KR sequences | [5] Ch. 2 (basic DLs), Ch. 3 (complexity), Ch. 9 (ontology engineering); W3C [3], [4] | Why AMF's `SystemKind`/`DependencyKind` pair *is* a TBox, and what its closed vocabulary costs and buys (§5.1) |
| 3 | Description-logic complexity | PhD | KR&R seminars; ESSLLI DL courses | [5] Ch. 3; [6]; [7]; [8] | Theorems 2.4–2.6 and the finite-domain collapse (Prop. 5.2) |
| 4 | Machine learning with graphs | MSc / PhD | **Stanford CS224W, Machine Learning with Graphs** (Leskovec) — lectures on node embeddings, knowledge-graph embeddings, GNN expressivity | [54]; [50]–[53]; [60]; [68]; [78] | The expressivity taxonomy of Prop. 2.9 and Thm. 2.10, and the parameter accounting of §5.3 |
| 5 | Probability and mathematical statistics | Undergraduate → MSc | Any measure-theoretic probability sequence | Casella & Berger, *Statistical Inference*, Ch. 1–7 | Conditional independence, the object d-separation encodes |
| 6 | Graphical models | MSc / PhD | Stanford CS 228 *Probabilistic Graphical Models*; CMU 10-708 | Koller & Friedman, *Probabilistic Graphical Models*, Ch. 3 (Bayesian networks), Ch. 21 (causality) | d-separation (Def. 2.16); the Markov factorisation Thm. 2.17 truncates |
| 7 | Causal inference — graphical | PhD | **Stanford STATS 361 *Causal Inference*** (graphical-models and structural-model units); UCLA cognitive-systems causality seminars | [10] Ch. 1 (probabilities/graphs), Ch. 3 (do-calculus, back-/front-door), Ch. 7 (counterfactuals, structural semantics); [35] Ch. 3–6 | Everything in §5.5–§5.7 |
| 8 | Causal inference — potential outcomes | PhD | **Stanford STATS 361**; Harvard's graduate causal-inference sequence in the Department of Statistics | [21] Ch. 1–3 (framework), Ch. 12–14 (propensity score, matching), Ch. 23–25 (IV/LATE); [97] Part I–II | SUTVA and why a coupled system violates it (§5.8) |
| 9 | Applied econometrics — design-based | PhD | **MIT 14.387 *Applied Econometrics: Mostly Harmless Big Data*** (Angrist & Chernozhukov; prerequisite **14.382 *Econometrics***); Berkeley and Chicago applied-econometrics sequences | [96] Ch. 3 (regression/CIA), Ch. 4 (IV), Ch. 5 (DiD/panel), Ch. 6 (RD); [102] Ch. 5, 18, 21 | Why the note's Method 2 is an *estimation* toolkit, and what it would be estimating here (§5.13) |
| 10 | The staggered-adoption revision | PhD / frontier | Recent applied-metrics topics courses | [27]; [28]; [29]; [30]; [31] | Any AMF calibration exercise using policy-adoption panels must use these, not TWFE |
| 11 | Time-series econometrics | PhD | Chicago/Princeton macro-econometrics sequences | [100] Ch. 10–11 (VAR, structural VAR), Ch. 17 (unit roots); [101] Ch. 2–4, 9 | Def. 2.34 and the `n(n−1)/2`-restriction accounting |
| 12 | Empirical macro identification | PhD / frontier | Macro-econometrics field courses; NBER methods lectures | [47] (survey); [44]; [45]; [46]; [48]; [49]; [40]; [41] | What a "policy shock" is, and why identifying one is a research programme rather than a data field |
| 13 | Information theory | MSc / PhD | MIT 6.441-style information-theory courses; Stanford EE 376A | [71] Ch. 2 (entropy, mutual information), Ch. 8 (differential entropy) | Def. 2.37, Thm. 2.38, and the bridge to module Q3 |
| 14 | Network economics and systemic risk | PhD / frontier | Financial-networks topics courses | [79]; [80]; [81]; [82]; [83]; [84]; [85] | The honest external literature on exactly what AMF stylises: shock propagation on a weighted directed graph |

Two remarks on sequencing. First, rows 7 and 8 are *not* interchangeable presentations of one
theory. The graphical strand answers "is this effect identifiable from this diagram?"; the
potential-outcomes strand answers "what estimand does this design deliver, and at what
variance?". §5 needs the first almost entirely and the second only for §5.8. Second, row 9
is where most of the note's Method 2 lives, and row 10 is the reason a 2015-vintage reading
list would be actively misleading: the two-way fixed-effects estimator that the phrase
"difference-in-differences: compare markets with/without policy" most naturally denotes is
now known to be biased under staggered adoption with heterogeneous effects (Thm. 2.30).

## 4. Exact source material

### 4.1 Primary and seminal papers

**Causal structure and identification**

- **Wright (1921)** [12] — invents path analysis and the *path coefficient*; the product of
  coefficients along a path as the contribution of that path is the direct ancestor of
  Theorem 5.21.
- **Haavelmo (1943)** [15] — establishes the statistical meaning of a system of simultaneous
  structural equations, i.e. that structural parameters are not regression coefficients.
- **Verma and Pearl (1988)** [9] — introduces d-separation and proves it sound and complete
  for conditional independence in DAG models.
- **Pearl (1995)** [11] — the back-door and front-door criteria and the three rules of the
  do-calculus; the single most load-bearing citation in §5.6.
- **Robins (1986)** [16] — the g-formula for time-varying treatments; the general form of
  Theorem 2.17 and the correct treatment of a *sequence* of interventions, which is what a
  multi-wave AMF shock is.
- **Shpitser and Pearl (2006)** [13] and **Huang and Valtorta (2006)** [14] — independently
  prove the do-calculus complete, so "not derivable" and "not identifiable" coincide.
- **Rubin (1974)** [17] — the potential-outcomes formalism for randomised and non-randomised
  studies.
- **Rosenbaum and Rubin (1983)** [18] — the propensity score is a balancing score;
  adjustment can be one-dimensional.
- **Hudgens and Halloran (2008)** [19] — causal inference when SUTVA fails; direct, indirect,
  total and overall effects under interference.
- **Aronow and Samii (2017)** [20] — design-based estimation under general interference via
  exposure mappings; the technically correct way to define an estimand on a network.

**Quasi-experimental design**

- **Imbens and Angrist (1994)** [22] — the LATE theorem; monotonicity as the price of
  identification with heterogeneous effects.
- **Angrist, Imbens and Rubin (1996)** [23] — the IV assumptions restated in potential
  outcomes, with the exclusion restriction made explicit as a claim about absent arrows.
- **Bound, Jaeger and Baker (1995)** [25] and **Staiger and Stock (1997)** [24] — weak
  instruments bias 2SLS toward OLS and invalidate conventional inference.
- **Card and Krueger (1994)** [26] — the canonical DiD study; also the canonical target of
  the parallel-trends critique.
- **Goodman-Bacon (2021)** [27] — the decomposition theorem showing negative weights on
  already-treated comparisons.
- **Callaway and Sant'Anna (2021)** [28], **Sun and Abraham (2021)** [29], **de Chaisemartin
  and D'Haultfœuille (2020)** [30], **Borusyak, Jaravel and Spiess (2024)** [31] — the four
  standard repairs.
- **Thistlethwaite and Campbell (1960)** [32] — the first regression-discontinuity design.
- **Hahn, Todd and van der Klaauw (2001)** [33] — continuity conditions under which RD
  identifies a local effect; **Calonico, Cattaneo and Titiunik (2014)** [34] — robust
  bias-corrected confidence intervals.

**Time series and macro identification**

- **Granger (1969)** [36] — the predictive definition, Def. 2.32. **Sims (1972)** [112]
  applies it to money and income; **Granger (1980)** [38] is Granger's own restatement of
  what the concept does and does not claim.
- **Sims (1980)** [37] — the critique of incredible identifying restrictions and the VAR
  programme that followed.
- **Blanchard and Quah (1989)** [42] — long-run restrictions; **Uhlig (2005)** [43] — sign
  restrictions; two different ways to supply the missing `n(n−1)/2` equations.
- **Jordà (2005)** [40] — local projections; **Plagborg-Møller and Wolf (2021)** [41] — LPs
  and VARs estimate the same impulse responses in population.
- **Toda and Yamamoto (1995)** [39] — lag-augmented Granger tests valid under possible
  integration.
- **Romer and Romer (2004)** [44], **Kuttner (2001)** [45], **Gertler and Karadi (2015)**
  [46], **Stock and Watson (2018)** [48] — narrative, high-frequency and proxy-VAR
  identification of monetary shocks. **Nakamura and Steinsson (2018)** [49] — the information
  effect, which is a failure of the exclusion restriction the high-frequency design assumes.
- **Mertens and Ravn (2013)** [113] — the proxy-SVAR applied to tax shocks; a clean template
  for how an external instrument enters a VAR.
- **Lucas (1976)** [88] — reduced-form relations are not invariant to policy regimes; the
  reason a knowledge graph whose weights were fitted to one regime cannot be used to evaluate
  a change of regime.

**Knowledge representation and knowledge-graph learning**

- **Gruber (1993)** [1] — the definition of an ontology used in Def. 2.1.
- **Schmidt-Schauß and Smolka (1991)** [6], **Baader, Brandt and Lutz (2005)** [7],
  **Horrocks, Kutz and Sattler (2006)** [8] — the complexity ladder of Theorems 2.4–2.6.
- **Bordes *et al.* (2013)** [50] — TransE; translation in embedding space.
- **Yang *et al.* (2015)** [51] — DistMult; the symmetric bilinear-diagonal score of Prop. 2.9.
- **Trouillon *et al.* (2016)** [52] — ComplEx; complex embeddings recover antisymmetry.
- **Sun *et al.* (2019)** [53] — RotatE; relation as rotation, with an explicit account of
  which relational patterns each family can and cannot express.
- **Toutanova and Chen (2015)** [55] and **Dettmers *et al.* (2018)** [56] — inverse-relation
  leakage in FB15k/WN18 and the FB15k-237/WN18RR replacements.
- **Ruffinelli, Broscheit and Gemulla (2020)** [57] and **Sun *et al.* (2020)** [58] — much
  reported progress is training protocol and evaluation artefact.
- **Veličković *et al.* (2018)** [60] — graph attention networks.
- **Kipf and Welling (2017)** [68], **Gilmer *et al.* (2017)** [77], **Xu *et al.* (2019)**
  [78] — graph convolution, the message-passing abstraction, and the Weisfeiler–Leman
  expressivity ceiling.
- **Jain and Wallace (2019)** [64] and **Wiegreffe and Pinter (2019)** [65] — the two sides of
  whether an attention weight explains anything.

**Information theory and systems**

- **Schreiber (2000)** [69] — transfer entropy.
- **Barnett, Barrett and Seth (2009)** [70] — Granger causality equals twice the transfer
  entropy for Gaussian variables.
- **Mason (1956)** [72] — the gain formula for signal-flow graphs; the exact closed form used
  in §5.9.
- **Katz (1953)** [73] and **Bonacich (1987)** [74] — the attenuated-walk centrality that
  `DependencyGraph.centrality` implements.
- **Tarjan (1972)** [61] and **Hopcroft and Tarjan (1973)** [75] — articulation points and
  biconnected components; **Johnson (1975)** [62] — enumeration of elementary circuits, the
  problem `feedback_loops()` solves.

### 4.2 Canonical textbooks, with the chapters that matter

- **Pearl, *Causality: Models, Reasoning, and Inference*, 2nd ed., Cambridge University
  Press (2009)** [10]. Ch. 1 (§§1.2–1.4: graphs, d-separation, causal models), **Ch. 3
  (§3.2 the do-operator and truncated factorisation; §3.3 back-door and front-door; §3.4 the
  do-calculus)**, Ch. 4 (actions and plans), **Ch. 7 (§7.1 structural counterfactuals, the
  three-step abduction–action–prediction recipe)**, Ch. 11 (replies to critiques). Ch. 3 and
  Ch. 7 are the load-bearing chapters for §5.
- **Peters, Janzing and Schölkopf, *Elements of Causal Inference: Foundations and Learning
  Algorithms*, MIT Press (2017)** [35]. Open access. Ch. 3 (cause–effect models), Ch. 4
  (learning cause–effect), **Ch. 6 (multivariate SCMs, interventions, counterfactuals)**,
  Ch. 7 (structure identifiability), Ch. 10 (hidden variables). The cleanest modern
  statement of the SCM formalism used in Def. 5.7.
- **Imbens and Rubin, *Causal Inference for Statistics, Social, and Biomedical Sciences: An
  Introduction*, Cambridge University Press (2015)** [21]. **Ch. 1–3 (potential outcomes,
  assignment mechanisms, SUTVA)**, Ch. 12–14 (propensity score, subclassification,
  matching), **Ch. 23–25 (instrumental variables, LATE, non-compliance)**.
- **Angrist and Pischke, *Mostly Harmless Econometrics: An Empiricist's Companion*, Princeton
  University Press (2009)** [96]. Ch. 2 (the experimental ideal), **Ch. 3 (regression and the
  conditional-independence assumption)**, **Ch. 4 (instrumental variables: §4.1 the LATE
  framework, §4.4 weak instruments)**, **Ch. 5 (fixed effects and differences-in-differences)**,
  **Ch. 6 (regression discontinuity)**. Read together with [27]–[31], which post-date it and
  revise Ch. 5.
- **Hernán and Robins, *Causal Inference: What If*, Chapman & Hall/CRC (2020)** [97]. Part I
  (Ch. 1–3: definition, randomised experiments, observational studies), Part II (Ch. 11–15:
  models, g-methods), **Part III (Ch. 19–21: time-varying treatments and the g-formula)** —
  the right reference for multi-wave interventions.
- **Morgan and Winship, *Counterfactuals and Causal Inference: Methods and Principles for
  Social Research*, 2nd ed., Cambridge University Press (2015)** [98]. Ch. 3 (causal graphs),
  Ch. 6 (identification with a back-door), Ch. 9 (IV), Ch. 10 (mechanisms and front-door).
- **Baader, Calvanese, McGuinness, Nardi and Patel-Schneider (eds), *The Description Logic
  Handbook*, 2nd ed., Cambridge University Press (2007)** [5]. **Ch. 2 (basic description
  logics)**, **Ch. 3 (complexity of reasoning)**, Ch. 4 (relationships to other formalisms),
  Ch. 9 (ontology engineering), Ch. 14 (Semantic Web).
- **Hamilton, *Time Series Analysis*, Princeton University Press (1994)** [100]. Ch. 10
  (vector autoregressions), **Ch. 11 (§11.4 structural VARs, §11.6 impulse responses and
  variance decomposition)**, Ch. 17 (unit roots), Ch. 19 (cointegration).
- **Lütkepohl, *New Introduction to Multiple Time Series Analysis*, Springer (2005)** [101].
  Ch. 2 (stable VARs), Ch. 2.3.1 (Granger causality in a VAR), Ch. 3–4 (estimation and model
  checking), **Ch. 9 (structural VARs)**.
- **Wooldridge, *Econometric Analysis of Cross Section and Panel Data*, 2nd ed., MIT Press
  (2010)** [102]. Ch. 4–5 (single-equation IV), Ch. 10 (panel basics), Ch. 18 (treatment
  effects), Ch. 21 (difference-in-differences and related designs).
- **Spirtes, Glymour and Scheines, *Causation, Prediction, and Search*, 2nd ed., MIT Press
  (2000)** [99]. Ch. 3 (the causal Markov and faithfulness conditions), Ch. 5 (the PC and FCI
  algorithms), Ch. 6 (latent variables). The reference for what "learn the graph from data"
  would actually mean.
- **Cover and Thomas, *Elements of Information Theory*, 2nd ed., Wiley (2006)** [71]. Ch. 2
  (entropy, mutual information, chain rules), Ch. 8 (differential entropy) — the substrate for
  Def. 2.37 and the Q3 bridge.
- **Horn and Johnson, *Matrix Analysis*, 2nd ed., Cambridge University Press (2013)** [76].
  Ch. 5 (norms; the induced-norm bound used in Thm. 5.17), **Ch. 8 (nonnegative matrices,
  Perron–Frobenius)**. The correct reference for spectral radius versus induced-norm bounds.
- **Newman, *Networks*, 2nd ed., Oxford University Press (2018)** [59]. Ch. 6 (mathematics of
  networks: adjacency matrices, walks, cut vertices), Ch. 7 (measures and metrics, including
  Katz centrality), Ch. 8 (network structure algorithms).

### 4.3 Surveys and reviews

- **Hogan *et al.* (2021), "Knowledge Graphs"** [67], *ACM Computing Surveys* **54**(4),
  Article 71 — the standard reference survey: data models, schema and identity, deductive and
  inductive knowledge, construction, quality, publication. §§2–3 are the relevant part for
  §5.1.
- **Nickel, Murphy, Tresp and Gabrilovich (2016)** [54], *Proceedings of the IEEE* **104**(1),
  11–33 — relational machine learning for knowledge graphs; unifies latent-feature,
  graph-feature and Markov-random-field approaches, and is the clearest statement of what
  link prediction is *for*.
- **Wang, Mao, Wang and Guo (2017)** [109], *IEEE TKDE* **29**(12) — knowledge-graph
  embedding survey with the translational/semantic-matching taxonomy.
- **Ji, Pan, Cambria, Marttinen and Yu (2022)** [110], *IEEE TNNLS* **33**(2) — representation,
  acquisition and applications, including temporal knowledge graphs (the note's `time-lag`
  edge type).
- **Ramey (2016), "Macroeconomic Shocks and Their Propagation"** [47], *Handbook of
  Macroeconomics* **2**, Ch. 2, 71–162 — the survey to read before believing any "policy →
  outcome" edge weight. It shows how much estimated impulse responses move with the
  identification scheme.
- **Andrews, Stock and Sun (2019)** [107], *Annual Review of Economics* **11** — weak
  instruments: theory and current practice.
- **Guarino, Oberle and Staab (2009), "What Is an Ontology?"** [108] — the conceptual
  clean-up of Def. 2.1, distinguishing conceptualization, specification and commitment.
- **Berners-Lee, Hendler and Lassila (2001)** [111] — the programmatic statement of the
  Semantic Web that RDF, OWL and the knowledge-graph literature descend from; read for the
  motivating vision, not for technical content.

### 4.4 Open courseware and lecture notes

- **MIT OpenCourseWare, 14.387 *Applied Econometrics: Mostly Harmless Big Data*** (Angrist and
  Chernozhukov, Fall 2014) — complete lecture and recitation notes and problem sets, covering
  regression and matching, IV, DiD, RD and standard errors; the prerequisite is 14.382
  *Econometrics*. This is the note's Method 2, taught properly.
- **Stanford CS224W, *Machine Learning with Graphs*** (Leskovec) — slides and full lecture
  videos; the knowledge-graph-embedding and GNN-expressivity lectures cover [50]–[53], [60],
  [68], [78].
- **Stanford STATS 361, *Causal Inference*** (Wager) — publicly circulated lecture notes
  covering randomisation, observational studies, propensity methods, double robustness,
  instrumental variables, regression discontinuity, interference and graphical models; the
  single best free bridge between §§2.4 and 2.5.
- **Peters, Janzing and Schölkopf [35]** is itself open access from MIT Press, and is the
  recommended self-study text for the SCM strand.
- **Hernán and Robins [97]** is distributed freely by the authors in draft and is the
  recommended self-study text for the g-methods strand.

### 4.5 Domain application to markets — including the sceptical literature

**Networks and propagation (the honest analogue of what AMF stylises)**

- **Acemoglu, Carvalho, Ozdaglar and Tahbaz-Salehi (2012)** [79] — sectoral input–output
  networks; when the degree distribution is heavy-tailed, idiosyncratic shocks do not wash out
  and aggregate volatility inherits network structure. The rigorous version of "shocks
  propagate along edges".
- **Acemoglu, Ozdaglar and Tahbaz-Salehi (2015)** [80] — financial contagion is *non-monotone*
  in connectivity: denser interbank networks absorb small shocks better and large shocks
  worse. Directly relevant to §5.8, where AMF's diagnostic response to a strengthened coupling
  is also non-monotone, for an unrelated (index-shape) reason.
- **Elliott, Golub and Jackson (2014)** [81] — integration versus diversification in
  cross-holding networks; two distinct axes that a single edge weight conflates.
- **Eisenberg and Noe (2001)** [82] — the clearing-vector fixed point; the canonical
  existence/uniqueness result for a settlement cascade.
- **Gai and Kapadia (2010)** [83] — contagion in financial networks as a percolation problem;
  "robust-yet-fragile" behaviour.
- **Diebold and Yılmaz (2014)** [84] — connectedness measured from forecast-error variance
  decompositions of a VAR. This is the *methodologically honest* version of "learn edge
  weights from data": the weights are defined as variance shares under an explicit
  identification, not extracted from prose.
- **Billio, Getmansky, Lo and Pelizzon (2012)** [85] — builds a directed network of financial
  institutions from pairwise Granger-causality tests. The closest published relative of the
  note's Method 2, and worth reading precisely because the authors are explicit that the
  resulting arrows are predictive, not structural.

**Policy transmission, and where the note's example goes wrong**

- **Bernanke and Kuttner (2005)** [86] — an unanticipated 25-basis-point cut in the federal
  funds target is associated with roughly a one percent rise in broad equity indices,
  operating mainly through expected excess returns rather than expected real rates. This is
  the empirical content behind the note's `Fed rate → … → Stock prices ↑`, and it required
  high-frequency identification [45] to obtain.
- **Gopinath *et al.* (2020)** [87] — under dominant-currency pricing, exchange-rate
  pass-through to a country's export prices in its own currency is low and trade volumes
  respond mainly to the *dollar* exchange rate, not the bilateral one. Relevant to §5.12: the
  note's `rate cut → currency devaluation (bad for exports)` has the textbook
  expenditure-switching sign reversed, and the modern literature says the true sign is
  regime-dependent rather than simply opposite.

**Scepticism about the method itself**

- **Leamer (1983)** [89] — specification searches make reported standard errors meaningless;
  the origin of the credibility critique.
- **Freedman (1991)** [90] — statistical models do not substitute for design and subject-matter
  knowledge ("shoe leather"); the standing objection to path models estimated from
  observational data, which is exactly what an automatically-weighted knowledge graph is.
- **Sims (1980)** [37] — "incredible" identifying restrictions in large structural models.
- **Deaton (2010)** [91] and **Heckman and Urzúa (2010)** [92] — LATE answers a question
  defined by the instrument, which may not be the policy question; **Imbens (2010)** [93]
  replies. Read all three: this is the live methodological disagreement about whether
  design-based identification buys credibility at the cost of relevance.
- **Manski (1993)** [94] — the reflection problem: with linear-in-means social interactions,
  endogenous and contextual effects are not separately identified. The general warning for any
  attempt to estimate influence weights on a network from equilibrium outcomes; **Angrist
  (2014)** [95] extends the sceptical case to peer-effect regressions.
- **Lucas (1976)** [88] — the deepest objection to the note's whole programme: a graph whose
  weights are fitted to historical policy behaviour is not invariant to a change in policy
  behaviour, so it cannot answer the counterfactual it was built to answer.
- **Rudin (2019)** [66] and **Miller (2019)** [114] — on why post-hoc explanation of an opaque
  model is the wrong choice when an interpretable model is available, and on what
  "explanation" means to the humans consuming it.

## 5. Derivation for the AMF setting

Throughout, `K = (k_0, …, k_6)` is `tuple(SystemKind)` in declaration order — `skeleton`,
`circulatory`, `nervous`, `musculature`, `organs`, `immune`, `metabolism`. Per system,
`g` is integrity, `r` redundancy, `c` criticality, `l` load, `h = g(1 − l)` health, and
`a = 0.5 r + 0.3 g + 0.2 (1 − l)` absorptive capacity. Every numerical result quoted below
was computed with `amf` 0.1.0 against `examples/sample_market.json` at default
configuration; §7 states how to falsify each one.

### 5.1 AMF is already a knowledge graph, and its ontology is closed

**Definition 5.1 (the AMF ontology).** AMF's TBox is the pair of closed vocabularies

```
Concepts (unary):   SystemKind  = { skeleton, circulatory, nervous, musculature,
                                     organs, immune, metabolism }          |C| = 7
Roles   (binary):   DependencyKind = { structural, informational, capital,
                                        regulatory }                        |R| = 4
Attributes:         SystemMetric = { integrity, redundancy, criticality, load } -> [0,1]
Axioms:             (i)  the seven concepts partition the domain (Market.require_complete)
                    (ii) every role is irreflexive              (no self-loops, graph.add)
                    (iii) every role instance carries a weight in (0, 1]
```

The ABox is a `Market`: seven individuals, one per concept, plus role assertions. The
*maximal* ABox has `7 × 6 × 4 = 168` role assertions; `examples/sample_market.json` asserts
eight. In RDF terms (Def. 2.2) the dependency set is an edge-labelled multigraph on seven
nodes, which is exactly the `(source, target, kind)` key of `DependencyGraph._edges`. The
note's request to "define entity types" and "define edge types" is therefore not a proposal
for new work; it is a description of `amf.models`.

**Proposition 5.2 (finite-domain collapse).** Fix `|Δ^Ⅰ| = 7` with the seven concepts named
by nominals and pairwise disjoint. Then concept satisfiability, subsumption, ABox consistency
and instance checking are decidable in time bounded by a constant independent of the
knowledge base's syntactic size beyond a linear scan.

*Proof sketch.* With the domain fixed at seven named elements and every concept a subset of
it, there are `2^7 = 128` possible concept extensions and `2^49` possible role extensions;
the interpretation is determined by the ABox because the partition axiom fixes each
individual's concept membership and the closed-world clause (Prop. 5.3) fixes each role.
Every reasoning problem reduces to evaluating a formula on one fixed finite structure, which
is model checking, not satisfiability. ∎

The practical consequence is blunt: Theorems 2.4–2.6 — `PSPACE`, `PTIME`, `N2ExpTime` — are
statements about how reasoning cost scales with an *unbounded* domain. AMF's domain is
literally seven elements and is fixed by the framework, so the entire complexity ladder is
inert. Adopting OWL, an RDF store or a DL reasoner here would import a large dependency and a
large conceptual surface to solve a problem that a `dict[SystemKind, AnatomicalSystem]`
already solves in one hash lookup. That is a rule-3 (zero-dependency) matter as much as a
modelling one.

### 5.2 The closed-world clause makes link prediction vacuous

**Proposition 5.3 (AMF is closed-world).** `Market.from_dict` reads `dependencies` as an
exhaustive list. A pair `(s, t)` absent from that list yields `edge_weight(s, t) == 0.0`, and
every downstream functional — `dependencies_of`, `concentration`, `feedback_loops`,
`articulation_points`, `coupling_matrix`, `centrality` — treats `0.0` as *absence of
coupling*, not as *unknown coupling*. There is no third truth value anywhere in the package.

**Corollary 5.4 (link prediction has no target).** Knowledge-graph completion (Def. 2.8) is
defined under the open-world assumption (Def. 2.7): the task is to rank *plausible unobserved
triples*, and its evaluation protocol assumes the test triples are true-but-missing. In a
closed-world ABox there are no true-but-missing triples by definition. Any model trained to
predict AMF edges would be trained to contradict the analyst's own assertions — which is not
a completion task but a *disagreement* task, and would need a wholly different evaluation
design and a wholly different justification.

This is the single most important boundary observation in the module, and it is a semantic
one rather than a matter of scale. Even given a corpus of a million markets, "predict the
missing edge" would remain ill-posed under `from_dict`'s semantics. What *is* well-posed is
elicitation support — "analysts who asserted `A` usually also asserted `B`" — and that is a
statement about analysts, not about markets, and belongs outside the package (§6).

### 5.3 Why an embedding cannot help at this scale

**Proposition 5.5 (parameter accounting).** A `d`-dimensional embedding of the AMF ontology
carries `7d` entity parameters plus `4d` relation parameters (`8d` real parameters for
ComplEx or RotatE, which use complex vectors), i.e. `11d` real numbers under DistMult or
TransE. The sample market supplies **8 positive triples**. At the field-conventional
`d = 200`, that is `2 200` free parameters fitted to 8 observations — a ratio of 275 to 1.
Even at `d = 1` the model has 11 parameters for 8 observations. There is no regime in which
the fit is determined.

**Proposition 5.6 (the information content of the whole ontology).** The complete
specification of a market's *relational* content is at most 168 numbers in `(0, 1]` plus the
28 metric coordinates: at most **196 real numbers**, and 8 + 28 = 36 in the sample market.
Any embedding of dimension `d ≥ 18` is a strict *expansion* of the data rather than a
compression of it. (Module D2 reaches the same accounting from the metric side; the two
counts agree because they are the same 196 numbers.)

Set against Prop. 2.9 and Thm. 2.10, the conclusion is that the expressivity taxonomy still
*matters* — a DistMult-scored AMF would destroy the antisymmetry on which `coupling_matrix`
depends, since stress flows target → source and the reverse edge means something different —
but it matters as a reason to *not* embed, not as a criterion for choosing among embeddings.

### 5.4 Graph attention degenerates to the reliance-share vector

Suppose a GAT layer (Def. 2.11) is placed over the seven systems with the AMF edge weights as
the only edge feature and `SystemMetric` values as node features. Because the graph is fixed
and tiny, and because attention normalises over each node's neighbourhood, the learned
coefficient vector on system `k`'s outgoing couplings lies on the simplex over
`dependencies_of(k)` — a set of size at most 6, in the sample market at most 2.

**Proposition 5.7 (attention has nothing to add to `concentration`).** Define the *reliance
share* of `k` on `t` as `p_k(t) = w(k,t) / Σ_u w(k,u)`. Then:

1. `p_k` is already the simplex-valued object attention would learn, computed exactly and
   without parameters.
2. `DiagnosticEngine.concentration(k) = Σ_t p_k(t)²` is the collision probability of `p_k`,
   i.e. `exp(−H_2(p_k))` where `H_2` is Rényi entropy of order 2.
3. Both are invariant to the scale of `k`'s couplings (Prop. 5.8), which is why
   `DiagnosticConfig.scale_concentration_by_reliance` exists and why the note's
   `High weight = strong influence` is unavailable from a normalised coefficient alone.

**Proposition 5.8 (HHI is degree-zero homogeneous; exact derivative).** With
`T = Σ_u w_u` and `C = Σ_u (w_u/T)²`,

```
∂C/∂w_v = (2/T) ( w_v/T − C ) ,      and      Σ_v w_v ∂C/∂w_v = 0 .
```

*Proof.* `∂/∂w_v Σ_u w_u²/T² = 2 w_v/T² − 2 T^{-3} Σ_u w_u² = (2/T)(w_v/T − C)`. Summing
against `w_v` gives `(2/T)(Σ w_v²/T − C Σ w_v) = (2/T)(T C − T C) = 0`, which is Euler's
identity for a degree-0 homogeneous function. ∎

Verified on the sample market: for `circulatory` (targets `skeleton` 0.8, `nervous` 0.5;
`T = 1.30`, `C = 0.526627`) the derivatives are `+0.136550` and `−0.218480`, summing against
the weights to `−1.4e−17`; for `nervous` (targets `skeleton` 0.5, `musculature` 0.6;
`T = 1.10`, `C = 0.504132`) they are `−0.090158` and `+0.075131`, summing to `+1.9e−16`. The
sign rule is exact and interpretable: **strengthening a coupling whose share already exceeds
the index raises concentration; strengthening an under-represented coupling lowers it.**

### 5.5 The AMF structural causal model

**Definition 5.9 (the unrolled AMF SCM).** Fix a market `M`, a configuration
`(max_steps, damping d, retention ρ, transmission τ, jitter, seed)`, and the coupling matrix
`W` with `W[i][j] = edge_weight(j, i)` (stress flows target → source). Let
`V = { x_t[j] : 0 ≤ t ≤ T, j ∈ K }` and `U = { s_t[j] }` the injected shock magnitudes
(plus the seeded jitter draws when `jitter > 0`). The structural equations are

```
x_0[j]      <- clip( s_0[j], 0, 1 )
x_{t+1}[j]  <- clip( d ( ρ x_t[j] + τ (1 − a_j) Σ_i x_t[i] W[i][j] ) + s_{t+1}[j], 0, 1 )
```

with the opt-in cascade, recovery and intervention terms entering as additional deterministic
arguments of the same `f_j`.

**Proposition 5.10 (the AMF SCM is Markovian and acyclic).** The causal diagram of Def. 5.9
has an arrow `x_t[i] → x_{t+1}[j]` whenever `W[i][j] > 0` or `i = j`, and `s_t[j] → x_t[j]`.
Every arrow strictly increases `t`, so the diagram is a DAG even though the *contemporaneous*
coupling graph contains cycles (the sample market contains the cycle
`circulatory → nervous → musculature → circulatory`). With `jitter = 0` the exogenous set
carries a point mass; with `jitter > 0` and a seed, the draws are independent by construction.
Hence the model is Markovian in the sense of Def. 2.14: **there are no unobserved
confounders, because there are no unobserved variables at all.**

**Corollary 5.11 (identification is trivial; estimation is vacuous).** By Theorem 2.17 every
interventional distribution factorises as a truncated product over the known equations. No
back-door set need be found (Thm. 2.19), no front-door path need exist (Thm. 2.20), no
instrument need be located (Thm. 2.28), no parallel-trends assumption need be defended
(Def. 2.29), and the `ID` algorithm (Thm. 2.21) would return the answer on its first call.
The reason is not that AMF has solved the identification problem but that it never posed it:
**the structural coefficients are stipulated by the analyst in the market JSON, not estimated
from data.** Everything the note's Method 2 offers is machinery for recovering coefficients
one does not know; AMF's coefficients are inputs.

This also disposes of the note's Method 3 as a research task. With `jitter = 0` the SCM is
deterministic, so abduction (Def. 2.22) is trivial — the exogenous state is a point — and the
three rungs of the ladder collapse: association, intervention and counterfactual are the same
computation. "If the Fed had not cut the rate, what would happen?" becomes, inside the
boundary, "re-run `propagate` on the market with one metric replaced", which
`examples/where_to_intervene.py` already does.

### 5.6 The do-operator on markets

**Definition 5.12 (atomic structural intervention).** For `k ∈ SystemKind`,
`m ∈ SystemMetric` and `v ∈ [0, 1]`, define

```
do(k.m := v) :  Market -> Market
                M  |->  M.with_system( M.system(k).with_metric(m, v) )
```

and for an edge, `do(e(s,t) := w)`, the market whose dependency set has the `(s, t)` pair
replaced by total weight `w`. The *causal effect on the diagnostic index* of an intervention
`σ` is `Δ(σ) = I(σ(M)) − I(M)` where `I = DiagnosticEngine().diagnose(·).overall_index`.

Two asymmetries in the current API are worth recording. `do(k.m := v)` is expressible today —
`with_system` and `with_metric` are exactly it — but `do(e(s,t) := w)` is **not**, because
`DependencyGraph.add` *aggregates* rather than replaces and there is no removal operation. An
edge do-operator therefore needs a `with_dependency` / `without_dependency` pair on `Market`.
That is the one genuinely missing primitive this module identifies (§8, D3-4).

**Theorem 5.13 (exact interventional gradients).** Write `w_f, w_c, w_b` for the diagnostic
blend weights, `w_Σ = w_f + w_c + w_b`, `D = Σ_j c_j`. Because `concentration` and
`feedback_amplification` are functionals of the graph alone and do not read any
`SystemMetric`, and because `I = (Σ_j c_j S_j)/D` with
`S_k = (w_f c_k (1 − h_k)(1 − r_k) + w_c C_k + w_b B_k)/w_Σ`:

```
∂I/∂g_k = − (w_f/w_Σ) · c_k² (1 − l_k)(1 − r_k) / D
∂I/∂l_k = + (w_f/w_Σ) · c_k²  g_k    (1 − r_k) / D
∂I/∂r_k = − (w_f/w_Σ) · c_k² (1 − h_k)          / D
∂I/∂c_k = [ (w_f/w_Σ) · 2 c_k (1 − h_k)(1 − r_k) + (w_c C_k + w_b B_k)/w_Σ − I ] / D
```

*Proof.* For the first three, `c_k S_k` is affine in each of `g_k`, `r_k`, `l_k` separately
with the stated slope, and every other `c_j S_j` and `D` are constant in them. For the fourth,
`c_k S_k = [w_f c_k²(1 − h_k)(1 − r_k) + c_k(w_c C_k + w_b B_k)]/w_Σ` is quadratic in `c_k`
while `D` is affine, so `∂I/∂c_k = (∂N/∂c_k · D − N)/D²` with `N = I D`; substituting gives
the display. ∎

**Corollary 5.14 (`SensitivityAnalyzer` computes causal, not associational, quantities).**
`SensitivityAnalyzer.analyse` perturbs a metric and *re-diagnoses*. By Def. 5.12 that is the
`do`-operator, not conditioning. The reported `gradient` is therefore an interventional
derivative in Pearl's rung-2 sense — no observational data, no confounding, no adjustment set.

The claim is checkable and was checked. Against `examples/sample_market.json` at
`DiagnosticConfig()` and `SensitivityConfig(step=0.05)`, the closed forms above and the
package's finite differences agree to **`5.8e−16`** — floating-point exactness — on all 21
integrity, redundancy and load entries. Selected values:

| system | metric | closed form | `SensitivityAnalyzer` | abs. difference |
|--------|--------|------------:|----------------------:|----------------:|
| `skeleton` | `integrity` | −0.040420 | −0.040420 | 1.7e−16 |
| `skeleton` | `load` | +0.031438 | +0.031438 | 3.4e−16 |
| `circulatory` | `redundancy` | −0.029758 | −0.029758 | 4.8e−16 |
| `circulatory` | `integrity` | −0.027469 | −0.027469 | 4.9e−17 |
| `musculature` | `redundancy` | −0.005418 | −0.005418 | 5.8e−16 |

**Theorem 5.15 (exact truncation error for criticality).** `I` is *not* polynomial in `c_k`
but a rational function of Möbius type: writing `α = (w_f/w_Σ)(1 − h_k)(1 − r_k)`,
`β = (w_c C_k + w_b B_k)/w_Σ`, `δ = D − c_k`, `γ = Σ_{j≠k} c_j S_j` and
`κ = γ − βδ + αδ²`, we have `I(c) = α(c + δ) + (β − 2αδ) + κ/(c + δ)`. Hence the central
difference at half-step `η` satisfies **exactly**

```
CD(η) − ∂I/∂c_k  =  − κ η² / [ (c_k + δ)² ( (c_k + δ)² − η² ) ] .
```

*Proof.* `CD(η) = α − κ/((c+δ)² − η²)` by direct substitution, while `I'(c) = α − κ/(c+δ)²`;
subtract. ∎

At `step = 0.05` (so `η = 0.05`) on the sample market, predicted and observed discrepancies
agree to every digit printed, for all seven systems:

| system | closed form `∂I/∂c` | `SensitivityAnalyzer` | observed error | predicted by Thm. 5.15 |
|--------|--------------------:|----------------------:|---------------:|-----------------------:|
| `skeleton` | −0.01844724 | −0.01845920 | −1.1965e−05 | −1.1965e−05 |
| `circulatory` | +0.03039794 | +0.03038869 | −9.2551e−06 | −9.2551e−06 |
| `nervous` | +0.00257448 | +0.00256924 | −5.2378e−06 | −5.2378e−06 |
| `musculature` | +0.02192504 | +0.02192495 | −8.5781e−08 | −8.5781e−08 |
| `organs` | +0.01381415 | +0.01381178 | −2.3712e−06 | −2.3712e−06 |
| `immune` | +0.01306167 | +0.01305997 | −1.6998e−06 | −1.6998e−06 |
| `metabolism` | +0.01306167 | +0.01305923 | −2.4449e−06 | −2.4449e−06 |

**Corollary 5.16 (raising criticality can *lower* the index).** `∂I/∂c_k < 0` exactly when
`(w_f/w_Σ) 2 c_k (1 − h_k)(1 − r_k) + (w_c C_k + w_b B_k)/w_Σ < I`, i.e. when system `k`'s own
marginal contribution is below the market average. On the sample market this holds for
`skeleton`: `∂I/∂c_skeleton = −0.0184`, and `do(skeleton.criticality := 1.0)` moves the index
from `0.27963856` to `0.27803082`. Declaring infrastructure *more* load-bearing makes the
market look *less* structurally weak — because criticality is both a per-system multiplier
and the weight in the roll-up, and `skeleton` scores far below average (`0.0932` against
`0.2796`). This is a genuine property of the index, not a bug, and it is a good argument for
`SystemMetric.improving_direction()` returning `0` for criticality: the quantity does not
behave like a lever in either direction.

### 5.7 Interference structure: what is additive and what is not

**Theorem 5.17 (separability of the diagnostic layer).** Holding the dependency graph fixed,
interventions on `integrity`, `redundancy` or `load` of *distinct* systems have **exactly zero
interaction** on `I`:

```
Δ( do(k.m := v) ∘ do(k'.m' := v') )  =  Δ( do(k.m := v) ) + Δ( do(k'.m' := v') )     for k ≠ k'
```

*Proof.* `I = (Σ_j c_j S_j)/D`; with the graph and all criticalities fixed, `D` is constant
and each `c_j S_j` depends only on system `j`'s own metrics. The map is a fixed-weight sum of
independent terms. ∎

Three measured contrasts on the sample market make the boundary of the theorem precise:

| intervention pair | joint effect | sum of atomic | interaction |
|-------------------|-------------:|--------------:|------------:|
| `skeleton.integrity := 0.9` and `nervous.load := 0.4` (cross-system) | −0.0034265347 | −0.0034265347 | **0.0e+00** |
| `skeleton.redundancy := 0.6` and `circulatory.redundancy := 0.8` (cross-system) | −0.0190249505 | −0.0190249505 | **5.6e−17** |
| `circulatory.integrity := 0.9` and `circulatory.redundancy := 0.8` (same system) | −0.0146502970 | −0.0201441584 | **+5.49e−03** |
| `skeleton.criticality := 1.0` and `nervous.criticality := 0.9` (cross-system) | −0.0006429221 | −0.0006857918 | **+4.29e−05** |

Same-system pairs interact because `c(1 − h)(1 − r)` is bilinear in `(g, r)`; criticality
pairs interact because criticality also enters the denominator `D`. Everything else is exactly
additive.

**Remark 5.18 (SUTVA holds at one layer and fails at the other).** Theorem 5.17 says the
*diagnostic* layer satisfies SUTVA (Def. 2.24) trivially — no interference across systems.
The *simulation* layer does not, and cannot: `x_{t+1}[j]` reads `x_t[i]` for every `i` with
`W[i][j] > 0`, which is interference by construction. So a potential-outcomes analysis of AMF
must use two different frameworks for two different modules, and any transplanted estimator
for the dynamic layer needs an explicit exposure mapping in the sense of Aronow and Samii [20]
or the graphical treatment of Ogburn and VanderWeele [63]. Applying an off-the-shelf
SUTVA-assuming estimator to the stress dynamics would be a specification error, not an
approximation.

### 5.8 Edge interventions and the non-monotone regulatory coupling

The note asks: "Sensitivity: If we change edge weights, how does outcome change?" The AMF
answer is exact and mildly surprising. Consider `do(e(circulatory, immune) := w)`, i.e.
asserting that liquidity provision relies on the risk-control system with weight `w`. No new
cycle is created (nothing depends on `immune`, so `feedback_amplification` is unchanged) and
no fragility term moves; the only channel is `circulatory`'s concentration index.

**Proposition 5.19 (HHI-minimising new coupling).** Adding a coupling of weight `w` to a
system whose existing couplings are `w_1, …, w_n` gives
`C(w) = (Σ w_i² + w²)/(Σ w_i + w)²`, minimised at

```
w*  =  ( Σ_i w_i² ) / ( Σ_i w_i )
```

the weight-weighted mean of the existing couplings.

*Proof.* `C'(w) = 0 ⟺ 2w(Σw_i + w)² = 2(Σw_i + w)(Σw_i² + w²) ⟺ w Σw_i + w² = Σw_i² + w²`. ∎

For `circulatory` with `w_1 = 0.8`, `w_2 = 0.5`: `w* = (0.64 + 0.25)/1.30 = 0.684615`. Sweeping
the actual engine over `w ∈ {0.01, …, 1.00}` reproduces this: `I` falls from `0.27963856` at
`w → 0` to a minimum of `0.27046550` at `w = 0.68`, then *rises* again to `0.27108725` at
`w = 1.00`.

```
w      0.10       0.30       0.50       0.68       0.80       1.00
I      0.2762330  0.2723766  0.2708133  0.2704655  0.2705652  0.2710873
Δ     -0.0034056 -0.0072619 -0.0088253 -0.0091731 -0.0090734 -0.0085513
```

**The causal effect of strengthening a coupling is non-monotone with an interior optimum.**
The mechanism here is index-shape, not economics: HHI rewards *balance*, so a third coupling
helps until it becomes the dominant one. It is nonetheless a concrete instance of the note's
"tradeoff analysis", obtained exactly, and it is a warning that any narrative reading of "a
stronger regulatory link is better" is unsupported by the index that would score it. It is
also a formal cousin of Acemoglu, Ozdaglar and Tahbaz-Salehi's non-monotonicity of contagion
in connectivity [80], though the two arise for unrelated reasons and should not be conflated.

### 5.9 The transmission algebra: powers, resolvent, and Mason's gain formula

**Definition 5.20 (effective transmission matrix).** In the unclipped, jitter-free, linear
regime, define

```
A[i][j]  =  d ρ · 1{i = j}  +  d τ (1 − a_j) · W[i][j]
```

so that the row-vector recursion of Def. 5.9 is `x_{t+1} = x_t A`, hence `x_t = x_0 A^t`.

**Theorem 5.21 (path decomposition = exact attribution).** For every horizon `L`,

```
(A^L)[i][j]  =  Σ over walks i = v_0 → v_1 → … → v_L = j   Π_{u=0}^{L−1} A[v_u][v_{u+1}]
```

so the `L`-step response of system `j` to a unit impulse at `i` decomposes *exactly* into a
sum of path products. Each walk splits into off-diagonal hops (edge transmission) and
self-loop steps (weight `dρ` each, the retention term). This is the AMF-internal impulse
response, and it is Wright's path coefficient [12] specialised to a linear dynamical system —
i.e. precisely the note's "Attribution: which edges explain?", computed rather than learned.

**Theorem 5.22 (all-horizon gain via the resolvent).** If `ρ(A) < 1` then
`Σ_{t ≥ 0} A^t = (I − A)^{-1}`, and the cumulative stress delivered to `j` by a unit impulse
at `i` is `(I − A)^{-1}[i][j]`. By Mason's gain formula [72], each such entry equals

```
(I − A)^{-1}[i][j]  =  ( 1/Δ ) · Σ_k P_k Δ_k ,
Δ = 1 − Σ_m L_m + Σ_{non-touching m,n} L_m L_n − … ,
```

where `P_k` runs over forward paths from `i` to `j` with self-loops absorbed, `L_m` over the
loop gains of the graph, and `Δ_k` is `Δ` restricted to the subgraph untouched by `P_k`.

**Worked example (`examples/sample_market.json`, defaults `d = 0.85`, `ρ = 0.5`, `τ = 1`).**
The coupling matrix has six non-zero entries; the effective matrix `A` is

```
A[skeleton  ][circulatory ] = 0.85 · (1 − 0.54) · 0.80 = 0.31280
A[skeleton  ][nervous     ] = 0.85 · (1 − 0.67) · 0.50 = 0.14025
A[skeleton  ][immune      ] = 0.85 · (1 − 0.75) · 0.30 = 0.06375
A[circulatory][musculature] = 0.85 · (1 − 0.80) · 0.70 = 0.11900
A[circulatory][organs     ] = 0.85 · (1 − 0.70) · 0.60 = 0.15300
A[nervous   ][circulatory ] = 0.85 · (1 − 0.54) · 0.50 = 0.19550
A[musculature][nervous    ] = 0.85 · (1 − 0.67) · 0.60 = 0.16830
A[organs    ][metabolism  ] = 0.85 · (1 − 0.70) · 0.40 = 0.10200
diagonal (retention)        = 0.85 · 0.5             = 0.42500
```

The transmission graph has exactly one directed cycle,
`circulatory → musculature → nervous → circulatory`, with off-diagonal gain

```
G = 0.11900 × 0.16830 × 0.19550 = 0.00391541535 .
```

Absorbing the three self-loops gives the reduced loop gain
`L̃ = G / (1 − dρ)³ = 0.00391542 / 0.575³ = 0.02059562`, so `Δ = 1 − L̃ = 0.97940438`. Mason's
formula then predicts, for the self-gain of a loop member and for the `circulatory →
musculature` path:

```
(I − A)^{-1}[circulatory][circulatory] = (1/0.575) / Δ            = 1.7757022…
(I − A)^{-1}[circulatory][musculature] = (0.119/0.575²) / Δ       = 0.3674932…
```

Direct exact rational inversion of `I − A` gives `1.775702` and `0.367493`. The agreement is
to every digit computed. The full resolvent (cumulative gain, source in rows):

```
                skeleton  circulatory  nervous  musculature   organs   immune  metabolism
skeleton        1.739130    1.113242  0.491632     0.230393  0.296219  0.192817   0.052547
circulatory     0.000000    1.775702  0.107564     0.367493  0.472491  0.000000   0.083816
nervous         0.000000    0.603739  1.775702     0.124948  0.160647  0.000000   0.028497
musculature     0.000000    0.176712  0.519740     1.775702  0.047021  0.000000   0.008341
organs          0.000000    0.000000  0.000000     0.000000  1.739130  0.000000   0.308507
immune          0.000000    0.000000  0.000000     0.000000  0.000000  1.739130   0.000000
metabolism      0.000000    0.000000  0.000000     0.000000  0.000000  0.000000   1.739130
```

Reading the note's questions off this table is immediate. *Which paths dominate?* The
strongest non-trivial transmission is `skeleton → circulatory` at `1.113`, then
`nervous → circulatory` at `0.604`, then `musculature → nervous` at `0.520`. *Which is
weakest?* `musculature → metabolism` at `0.0083`, a four-hop path through two absorbing
systems. The isolated diagonal `1.739130 = 1/(1 − dρ)` is the pure retention gain of a system
that transmits to nothing.

**Proposition 5.23 (spectrum from cycle structure).** Write `A = dρ I + N` with `N` strictly
off-diagonal. Then `spec(A) = dρ + spec(N)`, and `N`'s spectrum is determined entirely by the
cycle structure of the transmission graph: a graph whose only cycle is a single `L`-cycle of
gain `G` has `spec(N) = {0} ∪ { ω G^{1/L} : ω^L = 1 }`, hence

```
ρ(A) = d ρ + G^{1/L} .
```

On the sample market `ρ(A) = 0.42500 + 0.00391541535^{1/3} = 0.42500 + 0.15761 = 0.5826132`,
matching power iteration to `0.5826132096`.

### 5.10 An exact contraction criterion

CLAUDE.md records, correctly, that the step map "is *not* a contraction for every market".
Definition 5.20 lets that be made precise.

**Theorem 5.24 (sufficient contraction condition).** In the unclipped regime,
`‖x A‖_1 ≤ (max_i Σ_j A[i][j]) ‖x‖_1`. Hence the stress dynamics contracts in the 1-norm if

```
for every transmitter i :     Σ_j W[i][j] (1 − a_j)  <  (1 − d ρ) / (d τ) .
```

With the default `d = 0.85`, `ρ = 0.5`, `τ = 1`, the right-hand side is
`0.575 / 0.85 = 0.6764706`.

*Proof.* `‖xA‖_1 = Σ_j |Σ_i x_i A_ij| ≤ Σ_i |x_i| Σ_j A_ij ≤ (max_i Σ_j A_ij) ‖x‖_1`. Expand
`Σ_j A[i][j] = dρ + dτ Σ_j W[i][j]·(1 − a_j)` and require it below 1. ∎

On the sample market the binding transmitter is `skeleton`, with
`0.8 × 0.46 + 0.5 × 0.33 + 0.3 × 0.25 = 0.608 < 0.676`, a margin of `0.0685`; its row sum is
`0.94180`, and every other row sum is smaller. The market is therefore a 1-norm contraction
with factor `0.9418`, while its actual spectral radius (Prop. 5.23) is the far smaller
`0.5826` — the gap between an induced-norm bound and the spectral radius, exactly as
Horn and Johnson [76] Ch. 5 describes. **This criterion is checkable from the market JSON
alone, without running a simulation**, and it is the compliant, exact answer to any question
of the form "will this wiring diagram blow up?".

### 5.11 The policy cascade, re-encoded structurally

The note's cascade runs `Fed rate → mortgage rates → housing demand → housing starts →
construction employment → consumer spending → corporate earnings → stock prices`. Every node
is a price or a quantity time series, so the chain is not expressible inside the boundary
(§6). Its *structural shadow* is, however, and it exposes a modelling gap.

**Proposition 5.25 (`immune` is a stress sink in the sample market).** In
`examples/sample_market.json` the only regulatory edge is `immune → skeleton` (immune *relies
on* infrastructure). Since stress flows target → source, this yields `W[skeleton][immune] =
0.3` and `W[immune][·] = 0` for every column. The out-degree of `immune` in the transmission
graph is zero, and the resolvent's `immune` row is `(0,0,0,0,0,1.739130,0)`: **regulation
receives stress and transmits none.**

Consequently the note's premise — that policy is the *source* of a cascade — cannot be
expressed in the sample market at all. To make "policy → markets → stability" representable,
some system must be asserted to *depend on* `immune`. That is a modelling choice the schema
permits and the sample market declines to make, and it is a more interesting finding than any
edge weight: **AMF's convention makes regulation a constraint that other systems lean on, not
a driver that pushes them.** A worked policy-transmission example must therefore begin by
adding a dependency with `target: immune` (§8, D3-6).

Doing so is instructive. `do(e(circulatory, immune) := 0.3)` — liquidity provision relies on
risk controls — moves the index from `0.27963856` to `0.27237662`, an effect of `−0.00726`,
and turns `immune` into a transmitter with a two-hop path `immune → circulatory →
musculature`. The structural cascade is then `immune → circulatory → {musculature, organs} →
{nervous, metabolism}`, with path products readable from Theorem 5.21.

**Remark 5.26 (a sign error in the source, preserved by the ontology).** The note lists
`conflicts (contradicts): "rate cut → currency devaluation (bad for exports)"` and concludes
`Rate cuts help housing/employment, but hurt exporters`. Under the textbook
expenditure-switching channel a domestic depreciation makes exports *cheaper* abroad and is
conventionally taken to *help* exporters; the modern literature complicates this — under
dominant-currency pricing, pass-through to export prices in the exporter's own currency is
low and volumes respond mainly to the dollar exchange rate rather than the bilateral one [87]
— but does not restore the note's sign as a general matter. The relevant point for this module
is not who is right about exchange rates. It is that **a hand-authored ontology encodes its
author's beliefs, including erroneous ones, and nothing in a graph-attention or
counterfactual-simulation pipeline detects a sign error in an asserted edge.** That is the
precise operational content of hard rule 2 ("illustrative, not validated").

### 5.12 Why Granger causality is undefined here, and what would be needed

**Proposition 5.27.** At default configuration (`jitter = 0.0`), the AMF stress process is
deterministic given the market and the shock. Every conditional forecast-error variance in
Def. 2.32 is identically zero, so the Granger criterion `σ²(Y|Ω) = σ²(Y|Ω \ X)` holds
degenerately for every pair, and the usual `F` statistic is a `0/0` form. **Granger causality
is not merely uninformative on AMF trajectories; it is undefined.** By Theorem 2.38 the same
is true of transfer entropy: a deterministic process carries zero conditional mutual
information in the relevant sense.

Switching on `jitter > 0` with a `seed` produces a genuine stochastic process, and
`ShockSimulator.ensemble` produces replications of it. But the noise is a *stipulated
numerical perturbation of the analyst's own model*, not a data-generating process for any
market, so a Granger test on those replications would be testing the `jitter` parameter. It
would recover, up to sampling error, the sparsity pattern of `A` — which was an input.

The honest reformulation is therefore that Granger causality, IV, DiD and RD are tools for
**calibrating** AMF's coupling weights against external evidence, an activity that requires
market time series and therefore lives outside the package (§6). Even there, the difficulties
are severe and well documented: what an "exogenous policy shock" *is* requires narrative or
high-frequency identification [44], [45], [46], [48]; those identifications are themselves
contested by the information effect [49]; the resulting impulse responses move substantially
with the identification scheme [47]; a staggered-adoption DiD run as TWFE can be sign-reversed
(Thm. 2.30); an influence weight estimated from equilibrium outcomes on a network faces the
reflection problem [94]; and weights fitted to one policy regime are not invariant to a change
of regime [88]. A calibration sidecar that quoted only the headline papers and not this list
would be producing numbers with unstated uncertainty, which is the failure mode hard rule 2
exists to prevent.

### 5.13 A compliant construction: `amf.causal`

Everything §§5.5–5.10 needs can be added without a single new runtime dependency, without a
learned parameter, and without a name from the `FORBIDDEN` list. Sketch:

```
amf/causal.py     (depends on: market, diagnostics, simulation — sits beside sensitivity)

  @dataclass(frozen=True, slots=True)
  class StructuralContrast:
      baseline_index: float
      adjusted_index: float
      effect: float                       # adjusted − baseline
      adjustments: tuple[Adjustment, ...] # what was set, per system/metric or edge
      def to_dict(self) -> dict[str, Any]: ...

  @dataclass(frozen=True, slots=True)
  class PathAttribution:
      path: tuple[SystemKind, ...]
      transmission_product: float         # Theorem 5.21
      share_of_total: float

  class InterventionAnalyzer:
      def apply(self, market, *adjustments) -> Market            # Definition 5.12
      def contrast(self, market, *adjustments) -> StructuralContrast
      def attribute(self, market, source, target, horizon) -> tuple[PathAttribution, ...]
      def cumulative_gain(self, market) -> dict[...]             # Theorem 5.22
      def contraction_margin(self, market) -> float              # Theorem 5.24
```

Notes on compliance. `transmission_product`, `cumulative_gain`, `contraction_margin` and
`share_of_total` are structural vocabulary; none contains `order`, `price`, `trade`,
`returns`, `signal` or any other `FORBIDDEN` substring. All results are frozen slotted
dataclasses with `to_dict()`, per the CLAUDE.md checklist. Path enumeration on seven nodes is
bounded by `Σ_{m=0}^{5} P(5, m) = 326` simple paths per ordered pair of systems, so exhaustive
enumeration is cheap and needs no sampling and therefore no seed. Resolvent inversion is a `7 × 7` Gaussian
elimination — about forty lines of standard library. Singularity (`ρ(A) ≥ 1`, so the
cumulative gain diverges) must raise `InvalidConfigError` rather than return `inf`, matching
the existing treatment of out-of-range knobs. `Market` gains `with_dependency` and
`without_dependency` so `do(e(s,t) := w)` becomes expressible (§8, D3-4); note that these must
*replace* rather than aggregate, unlike `DependencyGraph.add`.

## 6. Repository governance and boundary analysis

The note proposes six artefacts. Two are admissible as written with a disclaimer; one is
admissible only with its content rewritten; three collide directly with the hard rules. None
is silently dropped below — each is reproduced and annotated.

### 6.1 Artefact-by-artefact analysis

| Proposed artefact | Conflicts with | Why | Compliant reformulation |
|---|---|---|---|
| `docs/research/neural_knowledge_graphs.md` — Framework | Rule 2 (illustrative, not validated) — soft | A docs file is outside the `test_non_trading_boundary` scan, but framework prose that says a graph "reveals" the strongest policy path asserts validated empirical content | Admit as `docs/discussions/D3-…` (this file), carrying the standing not-validated banner and §5.11's explicit statement that asserted edges encode beliefs, not findings |
| `docs/taxonomies/financial_policy_ontology.md` — Entity/relation types | Rules 1 and 2 | Its entity list (`Rate`, `QE`, `asset prices`) is market-data vocabulary and would become the naming source for package objects; it also names real institutions (Fed, ECB, Treasury, BIS) and asserts relations among them, i.e. unvalidated claims about real bodies | Replace with `docs/taxonomies/structural-coupling-taxonomy.md`: role-abstract actors (`oversight authority`, `settlement operator`), the four existing `DependencyKind` values, and an explicit note that the taxonomy is a modelling vocabulary, not an empirical claim |
| `src/amf/knowledge_graphs/knowledge_graph.py` — Graph structure | Rule 3 (architecture/duplication) | `DependencyGraph` **is** this module (§5.1); a second graph type would duplicate it, open the closed 7-concept vocabulary that `require_complete` enforces, and create ambiguity in the one-way dependency order | No new module. Extend `DependencyGraph` with pure, dependency-free queries: `simple_paths`, `transmission_matrix`, `cumulative_gain`, `contraction_margin` (§5.13) |
| `src/amf/knowledge_graphs/graph_attention_network.py` — Attention learning | **Rule 3 (zero runtime dependencies), Rule 3 (determinism), Rule 3 (100 % coverage)** | Attention requires learned parameters, hence an optimiser, hence in practice a tensor library; SGD is non-deterministic without careful seeding; a training loop's branches cannot realistically be covered to 100 % | None needed inside the package: by Prop. 5.7 the attention coefficients over a fixed 7-node graph reduce to the reliance-share vector, which is `graph.reliance_shares(system)` — pure, deterministic, parameter-free — and its Rényi-2 collision probability is `DiagnosticEngine.concentration` |
| `src/amf/knowledge_graphs/causal_inference.py` — Granger/IV analysis | **Rule 1 (non-trading boundary), Rule 2, Rule 3** | Granger/IV consume time series of prices and returns; the natural API names (`returns`, `price_series`, `signal_strength`) contain three `FORBIDDEN` substrings; and by Prop. 5.27 Granger causality is undefined on AMF's deterministic trajectories | Split. Inside: `amf/causal.py` implementing the *intervention algebra* of §5.13 — `do`, `contrast`, `attribute`, `cumulative_gain` — with no estimation. Outside: an optional, separately licensed research sidecar (`amf-calibration`, out of tree, not imported by `amf`, free to depend on numpy/statsmodels) that estimates coupling weights from external data and emits a market JSON as its only interface |
| `examples/policy_cascade_analysis.py` — Trace pathways | Rule 1 | The cascade's nodes are mortgage rates, housing starts, corporate earnings, stock prices | `examples/transmission_path_analysis.py`: add `circulatory → immune`, then trace `immune → circulatory → {musculature, organs}` with Theorem 5.21 path products and the Theorem 5.22 cumulative gains (§5.11) |

### 6.2 Sub-artefact collisions inside the note's prose

Six further collisions live in the body text rather than in the deliverable list.

1. **"Parse research papers, news, policy statements"** — an offline, zero-dependency package
   cannot ingest a corpus. This requires network access, an NLP stack, and a licence review
   of the sources. Sidecar only.
2. **"Learn edge weights from frequency + sentiment"** — frequency of co-occurrence in news is
   not an estimate of a structural coefficient; asserting it as an edge weight would give the
   diagnostic index an unvalidated empirical input while leaving its output presented as a
   structural measure. This is the exact confusion rule 2 prohibits.
3. **`Tradeoff analysis possible`** — note that the string `tradeoff` **contains the
   `FORBIDDEN` substring `trade`**. A public name such as `tradeoff_analysis` or a dataclass
   field `tradeoffs` would be rejected by `tests/unit/test_non_trading_boundary.py`. Use
   `contrast`, `balance_of_effects`, or `StructuralContrast` as in §5.13.
4. **"Nodes = concepts (Fed, rate, stock, crisis, …)"** — `stock` is not on the `FORBIDDEN`
   list but `price` is, and every one of these concepts is a market-data entity. Opening the
   node vocabulary also breaks `Market.require_complete`, which is what guarantees the seven
   systems are all present and correctly filed.
5. **"time-lag (delayed effect): QE → inflation (with 6-month lag)"** — AMF *does* have a
   lag mechanism: `Shock.at_step` injects at a later timestep and the horizon extends to cover
   it. A lag is therefore a property of an injection, not of an edge. Adding a per-edge lag
   attribute would change the coupling matrix from a matrix to an operator-valued kernel and
   would alter every existing resilience score, so it is a breaking change requiring a
   CHANGELOG entry under `Changed` and a version bump, not an addition.
6. **`Policy insight: Rate cuts help housing/employment, but hurt exporters`** — presented as
   an output of the tool. This is a claim about the real economy, of contested sign (§5.11
   Remark 5.26), and rule 2 forbids exactly this framing.

### 6.3 Cross-cutting implications

**Determinism.** Nothing proposed in §5.13 introduces randomness. Path enumeration must
iterate in `SystemKind` declaration order and break ties by it, as `dependencies_of` and
`DiagnosticEngine.diagnose` already do; the reason is the one CLAUDE.md gives — floating-point
addition is not associative, and a resolvent computed by summing path products in insertion
order would differ in the last bits between two equal markets. Gaussian elimination must
choose its pivot deterministically (first non-zero in declaration order), not by magnitude
alone, or two equal markets could pivot differently. `tests/unit/test_properties.py` should
gain a permutation-invariance case for any new path or gain query.

**Dependencies.** The sidecar boundary is the whole design. `amf` imports nothing but the
standard library; `amf-calibration` may import whatever it needs but must not be importable
*from* `amf`, must not be listed in `[project.dependencies]` or in any extra that CI installs
for the `test` job, and must communicate solely through the market JSON schema. That keeps
`pyproject.toml`'s `Private :: Do Not Upload` classifier and `tests/unit/test_packaging.py`
untouched. The sidecar is likewise private-distribution-only (rule 4): a public GitHub
Release asset would not be a private channel.

**Coverage.** The 100 % statement-and-branch gate is the binding constraint on scope.
Deterministic, closed-form code — path enumeration, resolvent inversion, a contraction margin
— is fully coverable with a handful of hand-checked fixtures, including the singular case.
A training loop is not. This is a mechanical reason, independent of any of the others, why
`graph_attention_network.py` cannot live in this repository.

**Validation claims.** Every artefact must carry the standing disclaimer. In particular
`InterventionAnalyzer.contrast` returns a difference of two indices *of the same stipulated
model*; its docstring must say so, in the manner of `LeveragePoint`'s existing "They rank
candidate interventions within the supplied model; they are not recommendations about any real
market."

**Naming guard.** Before adding any public name, check it against `FORBIDDEN` = {`order`,
`buy`, `sell`, `price`, `pnl`, `broker`, `backtest`, `ticker`, `trade`, `portfolio`,
`candlestick`, `returns`, `signal`} as *substrings* of the class name and of every member and
dataclass field. Three traps in this module's vocabulary: `tradeoff` (contains `trade`),
`returns` (a natural name for a gain series), and `order` — note that a `PathAttribution.order`
field would need a new entry in the `ALLOWLIST` beside `CouplingMatrix.order`, and the
meta-test asserts every allowlist entry still exists, so the exemption must be justified in
the test file, not assumed.

**Protected artefacts.** Nothing here touches `AMF Framework v1.docx`, its `.ots`,
`anatomical-market-framework`, `LICENSE.txt` or `SHA256SUMS`, and no new file may be added to
`SHA256SUMS`.

## 7. Falsifiable propositions and open questions

Discussion D3, unlike Q1, carries no explicit **Key Research Questions** block. Its research
questions are the three bullets under **Interpretability & Transparency** — "Which paths
dominate?", "Which edges explain policy success/failure?", "If we change edge weights, how does
outcome change?" — reproduced verbatim in §1 and answered in substance by P1, P4 and P7 below.
Each proposition states what would refute it.

**P1 (path dominance is exactly computable).** For any market, the all-horizon transmission
gain from `i` to `j` equals `(I − A)^{-1}[i][j]` with `A` as in Def. 5.20, and this equals the
Mason gain-formula expansion over paths and loops.
*Refuted by*: a market and a pair `(i, j)` with `ρ(A) < 1` for which the exact resolvent entry
differs from the Mason expansion by more than `1e−12`, or for which either differs from
`Σ_{t=0}^{T} (A^t)[i][j]` as `T → ∞`. Verified here on `examples/sample_market.json` to six
decimals for the `circulatory` row.

**P2 (closed-form interventional gradients).** The four expressions of Theorem 5.13 equal
`SensitivityAnalyzer`'s finite differences to floating-point exactness for integrity,
redundancy and load, and differ for criticality by exactly the quantity of Theorem 5.15.
*Refuted by*: any market, any system, any of the three linear metrics where the discrepancy
exceeds `1e−12`; or any criticality entry where the observed error differs from the predicted
error by more than one part in `1e3`. Verified: max discrepancy `5.8e−16` over 21 linear
entries, and predicted/observed criticality errors agreeing to all printed digits over all
seven systems.

**P3 (exact separability of the diagnostic layer).** Interventions on the linear metrics of
distinct systems have exactly zero interaction on `I` (Thm. 5.17).
*Refuted by*: any market and any cross-system pair of integrity/redundancy/load interventions
whose joint effect differs from the sum of atomic effects by more than floating-point noise.
Verified at `0.0` and `5.6e−17` on two disjoint pairs.

**P4 (non-monotone edge sensitivity).** The causal effect of an added coupling on the
diagnostic index is non-monotone in its weight, with the concentration channel minimised at
`w* = (Σ w_i²)/(Σ w_i)` (Prop. 5.19).
*Refuted by*: a market in which adding a coupling with no other channel active moves the
index monotonically in `w` over `(0, 1]`, or in which the interior optimum lies away from
`w*` by more than the sweep resolution. Verified: argmin at `w = 0.68` against a closed form
of `0.684615`.

**P5 (spectrum from cycles).** For a transmission graph whose only cycle is a single `L`-cycle
of gain `G`, `ρ(A) = dρ + G^{1/L}` (Prop. 5.23).
*Refuted by*: any such market where power iteration converges to a different value beyond
`1e−9`. Verified: `0.5826132` predicted, `0.5826132096` observed.

**P6 (contraction criterion).** If `Σ_j W[i][j]·(1 − a_j) < (1 − dρ)/(dτ)` for every `i`, the
unclipped stress map is a 1-norm contraction (Thm. 5.24).
*Refuted by*: a market satisfying the inequality whose unclipped trajectory has
`‖x_{t+1}‖_1 > ‖x_t‖_1` at any step. Note the converse is deliberately not claimed — the
sample market's row-sum bound is `0.9418` while `ρ(A) = 0.5826`, so the criterion is
sufficient and loose.

**P7 (Granger causality is undefined at defaults).** With `jitter = 0.0` the AMF process is
deterministic, all conditional forecast-error variances vanish, and both the Granger statistic
and the transfer entropy are degenerate (Prop. 5.27, Thm. 2.38).
*Refuted by*: a default-configuration AMF trajectory exhibiting non-zero one-step conditional
forecast-error variance.

**P8 (link prediction is ill-posed under `from_dict`).** Because absence of a dependency is
read as weight `0.0` and not as "unknown", there is no set of true-but-missing triples for a
completion model to target (Cor. 5.4).
*Refuted by*: a reading of `Market.from_dict` or any downstream functional under which an
unlisted pair is treated as unknown rather than absent.

**P9 (embedding is an expansion, not a compression).** A market's complete relational and
metric content is at most 196 real numbers, so any embedding with `d ≥ 18` expands it
(Prop. 5.6).
*Refuted by*: a market representation requiring more than `168 + 28` numbers under the current
schema.

**P10 (attention adds nothing over reliance shares).** Over a fixed 7-node graph with the
existing edge weights, a GAT coefficient vector on a node's outgoing couplings is a
reparameterisation of the reliance-share simplex, and its collision probability is the existing
concentration index (Prop. 5.7).
*Refuted by*: a GAT configuration over this graph producing edge coefficients not expressible
as a softmax over a function of the same fixed inputs, or a demonstration that the learned
coefficients carry information about total reliance that the shares do not.

**Open questions.** (i) Does an exact Shapley decomposition of `(I − A)^{-1}[i][j]` over edges
exist in closed form, as it does for the additive diagnostic game (module D2, Thm. 5.6)?
(ii) What is the sharp (necessary and sufficient) contraction criterion under the `[0,1]`
clip, where the map is piecewise affine and Thm. 5.24 is only sufficient? (iii) Under the
opt-in cascade dynamics the map is no longer affine and Def. 5.20 does not apply — what
replaces the resolvent, and does a Mason-type expansion survive the threshold nonlinearity?
(iv) Can the note's `time-lag` edge type be added as a per-edge delay without breaking the
round-trip guarantee and without changing any existing score? (v) If a calibration sidecar
did estimate coupling weights, what uncertainty representation would let the diagnostic index
report an interval rather than a point, without any part of that interval being read as a
forecast?

## 8. Deliverables

The note's list, reproduced exactly, with a status and compliance column.

| # | Deliverable (verbatim from the note) | Status | Compliance |
|---|---|---|---|
| — | `docs/research/neural_knowledge_graphs.md` — Framework | **Superseded** by this file | Admissible as documentation; must carry the not-validated banner and must not assert that the graph "reveals" empirical policy findings |
| — | `docs/taxonomies/financial_policy_ontology.md` — Entity/relation types | **Rejected as specified** | Entity list is market-data vocabulary and names real institutions; see §6.1 for the role-abstract replacement |
| — | `src/amf/knowledge_graphs/knowledge_graph.py` — Graph structure | **Rejected as redundant** | `DependencyGraph` already is this (§5.1); duplicating it would open the closed 7-concept vocabulary and blur the one-way dependency order |
| — | `src/amf/knowledge_graphs/graph_attention_network.py` — Attention learning | **Rejected** | Violates zero-runtime-dependency, determinism, and the 100 % coverage gate; and by Prop. 5.7 the learned object is the existing reliance-share vector |
| — | `src/amf/knowledge_graphs/causal_inference.py` — Granger/IV analysis | **Rejected in-tree; admissible as a sidecar** | Ingests prices/returns (rule 1); natural API names hit three `FORBIDDEN` substrings; Granger causality is undefined on AMF trajectories (Prop. 5.27) |
| — | `examples/policy_cascade_analysis.py` — Trace pathways | **Rejected as specified; reformulated** | Cascade nodes are prices and quantities; see D3-6 |

Compliant replacements, in dependency order:

| ID | Deliverable | Layer | Notes |
|---|---|---|---|
| D3-1 | `docs/discussions/D3-knowledge-graphs-causal-pathways.md` | docs | This file. |
| D3-2 | `docs/taxonomies/structural-coupling-taxonomy.md` | docs | Role-abstract actors, the four existing `DependencyKind` values, explicit statement that the taxonomy is modelling vocabulary and not an empirical claim. |
| D3-3 | `DependencyGraph.simple_paths`, `.transmission_matrix`, `.cumulative_gain`, `.contraction_margin` | `graph.py` | Pure, stdlib-only, deterministic; canonical ordering; `InvalidConfigError` when `ρ(A) ≥ 1` makes the cumulative gain divergent. Theorems 5.21–5.24. |
| D3-4 | `Market.with_dependency` / `Market.without_dependency` | `market.py` | The missing primitive: `DependencyGraph.add` aggregates, so `do(e(s,t) := w)` is currently inexpressible (§5.6). These must *replace*. Round-trip through `to_dict`/`from_dict` must stay a fixed point. |
| D3-5 | `amf/causal.py`: `InterventionAnalyzer`, `StructuralContrast`, `PathAttribution`, `Adjustment` | new module beside `sensitivity` | §5.13. Frozen slotted dataclasses with `to_dict()`; exported from `amf/__init__.py` and added to the sorted `__all__`; `report._to_jsonable` and the text/Markdown renderers extended. |
| D3-6 | `examples/transmission_path_analysis.py` | examples | Adds `circulatory → immune` so regulation transmits (Prop. 5.25), then traces path products and cumulative gains. Add a case to `tests/integration/test_examples.py`. |
| D3-7 | `tests/unit/test_causal.py`, plus permutation-invariance cases in `test_properties.py` | tests | The 100 % gate applies. Cover the singular resolvent, the isolated-system row, the single-cycle spectrum, and the Thm. 5.15 truncation identity. |
| D3-8 | `amf-calibration` (out-of-tree, optional, private) | sidecar | May depend on numpy/statsmodels. Not importable from `amf`; not in `[project.dependencies]` or any CI-installed extra; communicates solely by emitting market JSON. Must reproduce §5.12's sceptical reading list in its own documentation. |
| D3-9 | `CHANGELOG.md` under `## [Unreleased]` | metadata | `Added` for D3-3/4/5; note that a future per-edge lag attribute (§6.2 item 5) would be a `Changed` entry requiring a version bump. |

## 9. Research leadership and prerequisites

The note states, verbatim:

> **Research Leaders Needed**: Knowledge engineer, causal inference specialist, NLP expert

That list is right for the note's programme and only partly right for the compliant one. The
knowledge-engineering role shrinks almost to nothing (the ontology has seven concepts and four
roles, and it already exists); the causal-inference role grows and splits in two, because the
in-tree work is *structural* — resolvents, path algebra, exact gradients — while the sidecar
work is *econometric*; and the NLP role moves entirely out of tree, where it becomes an
information-extraction and licensing problem rather than a modelling one. A fourth role the
note does not name is the binding one in practice: a Python engineer who can hold `mypy
--strict`, zero dependencies and 100 % branch coverage while the mathematics changes.

### 9.1 Skills matrix

| Role | Core competence | Must be able to | Owns | In tree? |
|------|-----------------|-----------------|------|----------|
| Structural-causal theorist | SCMs, do-calculus, identification | Prove Theorems 5.13–5.24; state precisely what `contrast` does and does not identify | `amf/causal.py` semantics, §§5.5–5.10 | Yes |
| Applied econometrician | IV/LATE, modern DiD, RD, SVAR, local projections, proxy/narrative identification | Explain why TWFE is unsafe under staggered adoption; defend or reject an exclusion restriction in writing | `amf-calibration`, and the uncertainty statement attached to any weight it emits | Sidecar |
| Numerical/graph engineer | Linear algebra, graph algorithms, floating-point determinism | Write a deterministic `7 × 7` solve and a canonical path enumerator in the standard library; reason about associativity | D3-3, D3-4 | Yes |
| Knowledge engineer | Ontology design, RDF/OWL, DL semantics | Recognise that the ontology is already closed and finite (Prop. 5.2) and argue *against* importing a reasoner | D3-2 | Yes (small) |
| Information-extraction specialist | IE, relation extraction, corpus licensing | Quantify extraction precision and recall; treat corpus licence and provenance as first-class | Sidecar ingestion only | No |
| Python maintainer | `ruff`, `mypy --strict`, pytest, hypothesis, packaging | Keep the boundary test, coverage gate and packaging invariants green through every change | D3-7, D3-9, review | Yes |
| Framework owner | AMF v1.0, the hard rules | Reject a deliverable on rule grounds before it reaches review | §6 | Yes |

### 9.2 Prerequisite ladder

```
Undergraduate
  1. Linear algebra (matrix powers, eigenvalues, Neumann series)
  2. Probability and mathematical statistics through conditional expectation
  3. Discrete mathematics: relations, graphs, first-order logic
  4. Algorithms: DFS, cycle enumeration, biconnected components  ......  [61], [62], [75]

Masters
  5. Graphical models: Bayesian networks, d-separation, factorisation  ...  [9], Koller & Friedman Ch. 3
  6. Econometrics I–II: OLS, panel data, instrumental variables  .........  [102] Ch. 4–5, 10
  7. Numerical linear algebra: norms, conditioning, spectral radius  .....  [76] Ch. 5, 8
  8. Knowledge representation: RDF, OWL profiles, DL semantics  ..........  [5] Ch. 2–3; [3], [4]
  9. Machine learning with graphs (only to know when not to use it)  .....  Stanford CS224W; [54]

Doctoral
 10. Structural causal models, do-calculus, identification  ..............  [10] Ch. 3, 7; [35] Ch. 6
 11. Potential outcomes, ignorability, interference  ....................  [21] Ch. 1–3; [19]; [20]
 12. Design-based applied econometrics  .................................  MIT 14.387; [96] Ch. 3–6
 13. Time-series identification: SVAR, local projections, proxies  ......  [100] Ch. 11; [40]; [41]; [48]
 14. Information theory and directed information  .......................  [71] Ch. 2, 8; [69]; [70]

Research frontier
 15. Completeness of the do-calculus and the ID algorithm  ..............  [13]; [14]
 16. Modern staggered-adoption DiD  .....................................  [27]–[31]
 17. Causal discovery and its identifiability limits  ...................  [99]; [103]; [105]; [106]; [104]
 18. Causal inference under network interference  .......................  [19]; [20]; [63]; [94]
 19. Financial-network propagation and systemic risk  ...................  [79]–[85]
 20. The credibility debate itself  .....................................  [88]; [89]; [90]; [91]; [92]; [93]
```

Sections 6 through 9 assume none of this ladder; sections 2 and 5 assume all of it.

## References

- [1] T. R. Gruber, "A translation approach to portable ontology specifications", *Knowledge Acquisition* **5**(2), 199–220 (1993).
- [2] R. Studer, V. R. Benjamins and D. Fensel, "Knowledge engineering: Principles and methods", *Data & Knowledge Engineering* **25**(1–2), 161–197 (1998).
- [3] R. Cyganiak, D. Wood and M. Lanthaler (eds), *RDF 1.1 Concepts and Abstract Syntax*, W3C Recommendation, 25 February 2014.
- [4] W3C OWL Working Group, *OWL 2 Web Ontology Language Document Overview*, 2nd ed., W3C Recommendation, 11 December 2012.
- [5] F. Baader, D. Calvanese, D. McGuinness, D. Nardi and P. F. Patel-Schneider (eds), *The Description Logic Handbook: Theory, Implementation and Applications*, 2nd ed., Cambridge University Press (2007).
- [6] M. Schmidt-Schauß and G. Smolka, "Attributive concept descriptions with complements", *Artificial Intelligence* **48**(1), 1–26 (1991).
- [7] F. Baader, S. Brandt and C. Lutz, "Pushing the EL envelope", in *Proceedings of the 19th International Joint Conference on Artificial Intelligence (IJCAI-05)*, 364–369 (2005).
- [8] I. Horrocks, O. Kutz and U. Sattler, "The even more irresistible SROIQ", in *Proceedings of the 10th International Conference on Principles of Knowledge Representation and Reasoning (KR 2006)*, 57–67 (2006).
- [9] T. Verma and J. Pearl, "Causal networks: Semantics and expressiveness", in *Proceedings of the 4th Workshop on Uncertainty in Artificial Intelligence (UAI)*, 352–359 (1988).
- [10] J. Pearl, *Causality: Models, Reasoning, and Inference*, 2nd ed., Cambridge University Press (2009).
- [11] J. Pearl, "Causal diagrams for empirical research", *Biometrika* **82**(4), 669–688 (1995).
- [12] S. Wright, "Correlation and causation", *Journal of Agricultural Research* **20**(7), 557–585 (1921).
- [13] I. Shpitser and J. Pearl, "Identification of joint interventional distributions in recursive semi-Markovian causal models", in *Proceedings of the 21st National Conference on Artificial Intelligence (AAAI-06)*, 1219–1226 (2006).
- [14] Y. Huang and M. Valtorta, "Pearl's calculus of intervention is complete", in *Proceedings of the 22nd Conference on Uncertainty in Artificial Intelligence (UAI 2006)*, 217–224 (2006).
- [15] T. Haavelmo, "The statistical implications of a system of simultaneous equations", *Econometrica* **11**(1), 1–12 (1943).
- [16] J. Robins, "A new approach to causal inference in mortality studies with a sustained exposure period — application to control of the healthy worker survivor effect", *Mathematical Modelling* **7**(9–12), 1393–1512 (1986).
- [17] D. B. Rubin, "Estimating causal effects of treatments in randomized and nonrandomized studies", *Journal of Educational Psychology* **66**(5), 688–701 (1974).
- [18] P. R. Rosenbaum and D. B. Rubin, "The central role of the propensity score in observational studies for causal effects", *Biometrika* **70**(1), 41–55 (1983).
- [19] M. G. Hudgens and M. E. Halloran, "Toward causal inference with interference", *Journal of the American Statistical Association* **103**(482), 832–842 (2008).
- [20] P. M. Aronow and C. Samii, "Estimating average causal effects under general interference, with application to a social network experiment", *The Annals of Applied Statistics* **11**(4), 1912–1947 (2017).
- [21] G. W. Imbens and D. B. Rubin, *Causal Inference for Statistics, Social, and Biomedical Sciences: An Introduction*, Cambridge University Press (2015).
- [22] G. W. Imbens and J. D. Angrist, "Identification and estimation of local average treatment effects", *Econometrica* **62**(2), 467–475 (1994).
- [23] J. D. Angrist, G. W. Imbens and D. B. Rubin, "Identification of causal effects using instrumental variables", *Journal of the American Statistical Association* **91**(434), 444–455 (1996).
- [24] D. Staiger and J. H. Stock, "Instrumental variables regression with weak instruments", *Econometrica* **65**(3), 557–586 (1997).
- [25] J. Bound, D. A. Jaeger and R. M. Baker, "Problems with instrumental variables estimation when the correlation between the instruments and the endogenous explanatory variable is weak", *Journal of the American Statistical Association* **90**(430), 443–450 (1995).
- [26] D. Card and A. B. Krueger, "Minimum wages and employment: A case study of the fast-food industry in New Jersey and Pennsylvania", *American Economic Review* **84**(4), 772–793 (1994).
- [27] A. Goodman-Bacon, "Difference-in-differences with variation in treatment timing", *Journal of Econometrics* **225**(2), 254–277 (2021).
- [28] B. Callaway and P. H. C. Sant'Anna, "Difference-in-differences with multiple time periods", *Journal of Econometrics* **225**(2), 200–230 (2021).
- [29] L. Sun and S. Abraham, "Estimating dynamic treatment effects in event studies with heterogeneous treatment effects", *Journal of Econometrics* **225**(2), 175–199 (2021).
- [30] C. de Chaisemartin and X. D'Haultfœuille, "Two-way fixed effects estimators with heterogeneous treatment effects", *American Economic Review* **110**(9), 2964–2996 (2020).
- [31] K. Borusyak, X. Jaravel and J. Spiess, "Revisiting event-study designs: Robust and efficient estimation", *The Review of Economic Studies* **91**(6), 3253–3285 (2024).
- [32] D. L. Thistlethwaite and D. T. Campbell, "Regression-discontinuity analysis: An alternative to the ex post facto experiment", *Journal of Educational Psychology* **51**(6), 309–317 (1960).
- [33] J. Hahn, P. Todd and W. van der Klaauw, "Identification and estimation of treatment effects with a regression-discontinuity design", *Econometrica* **69**(1), 201–209 (2001).
- [34] S. Calonico, M. D. Cattaneo and R. Titiunik, "Robust nonparametric confidence intervals for regression-discontinuity designs", *Econometrica* **82**(6), 2295–2326 (2014).
- [35] J. Peters, D. Janzing and B. Schölkopf, *Elements of Causal Inference: Foundations and Learning Algorithms*, MIT Press (2017).
- [36] C. W. J. Granger, "Investigating causal relations by econometric models and cross-spectral methods", *Econometrica* **37**(3), 424–438 (1969).
- [37] C. A. Sims, "Macroeconomics and reality", *Econometrica* **48**(1), 1–48 (1980).
- [38] C. W. J. Granger, "Testing for causality: A personal viewpoint", *Journal of Economic Dynamics and Control* **2**, 329–352 (1980).
- [39] H. Y. Toda and T. Yamamoto, "Statistical inference in vector autoregressions with possibly integrated processes", *Journal of Econometrics* **66**(1–2), 225–250 (1995).
- [40] Ò. Jordà, "Estimation and inference of impulse responses by local projections", *American Economic Review* **95**(1), 161–182 (2005).
- [41] M. Plagborg-Møller and C. K. Wolf, "Local projections and VARs estimate the same impulse responses", *Econometrica* **89**(2), 955–980 (2021).
- [42] O. J. Blanchard and D. Quah, "The dynamic effects of aggregate demand and supply disturbances", *American Economic Review* **79**(4), 655–673 (1989).
- [43] H. Uhlig, "What are the effects of monetary policy on output? Results from an agnostic identification procedure", *Journal of Monetary Economics* **52**(2), 381–419 (2005).
- [44] C. D. Romer and D. H. Romer, "A new measure of monetary shocks: Derivation and implications", *American Economic Review* **94**(4), 1055–1084 (2004).
- [45] K. N. Kuttner, "Monetary policy surprises and interest rates: Evidence from the Fed funds futures market", *Journal of Monetary Economics* **47**(3), 523–544 (2001).
- [46] M. Gertler and P. Karadi, "Monetary policy surprises, credit costs, and economic activity", *American Economic Journal: Macroeconomics* **7**(1), 44–76 (2015).
- [47] V. A. Ramey, "Macroeconomic shocks and their propagation", in J. B. Taylor and H. Uhlig (eds), *Handbook of Macroeconomics*, Vol. 2, Ch. 2, Elsevier, 71–162 (2016).
- [48] J. H. Stock and M. W. Watson, "Identification and estimation of dynamic causal effects in macroeconomics using external instruments", *The Economic Journal* **128**(610), 917–948 (2018).
- [49] E. Nakamura and J. Steinsson, "High-frequency identification of monetary non-neutrality: The information effect", *The Quarterly Journal of Economics* **133**(3), 1283–1330 (2018).
- [50] A. Bordes, N. Usunier, A. García-Durán, J. Weston and O. Yakhnenko, "Translating embeddings for modeling multi-relational data", in *Advances in Neural Information Processing Systems 26 (NIPS 2013)*, 2787–2795 (2013).
- [51] B. Yang, W.-t. Yih, X. He, J. Gao and L. Deng, "Embedding entities and relations for learning and inference in knowledge bases", in *Proceedings of the 3rd International Conference on Learning Representations (ICLR)* (2015); arXiv:1412.6575.
- [52] T. Trouillon, J. Welbl, S. Riedel, É. Gaussier and G. Bouchard, "Complex embeddings for simple link prediction", in *Proceedings of the 33rd International Conference on Machine Learning (ICML)*, PMLR **48**, 2071–2080 (2016).
- [53] Z. Sun, Z.-H. Deng, J.-Y. Nie and J. Tang, "RotatE: Knowledge graph embedding by relational rotation in complex space", in *Proceedings of the 7th International Conference on Learning Representations (ICLR)* (2019); arXiv:1902.10197.
- [54] M. Nickel, K. Murphy, V. Tresp and E. Gabrilovich, "A review of relational machine learning for knowledge graphs", *Proceedings of the IEEE* **104**(1), 11–33 (2016).
- [55] K. Toutanova and D. Chen, "Observed versus latent features for knowledge base and text inference", in *Proceedings of the 3rd Workshop on Continuous Vector Space Models and their Compositionality*, 57–66 (2015).
- [56] T. Dettmers, P. Minervini, P. Stenetorp and S. Riedel, "Convolutional 2D knowledge graph embeddings", in *Proceedings of the 32nd AAAI Conference on Artificial Intelligence (AAAI-18)*, 1811–1818 (2018).
- [57] D. Ruffinelli, S. Broscheit and R. Gemulla, "You CAN teach an old dog new tricks! On training knowledge graph embeddings", in *Proceedings of the 8th International Conference on Learning Representations (ICLR)* (2020).
- [58] Z. Sun, S. Vashishth, S. Sanyal, P. Talukdar and Y. Yang, "A re-evaluation of knowledge graph completion methods", in *Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics (ACL)*, 5516–5522 (2020).
- [59] M. E. J. Newman, *Networks*, 2nd ed., Oxford University Press (2018).
- [60] P. Veličković, G. Cucurull, A. Casanova, A. Romero, P. Liò and Y. Bengio, "Graph attention networks", in *Proceedings of the 6th International Conference on Learning Representations (ICLR)* (2018); arXiv:1710.10903.
- [61] R. E. Tarjan, "Depth-first search and linear graph algorithms", *SIAM Journal on Computing* **1**(2), 146–160 (1972).
- [62] D. B. Johnson, "Finding all the elementary circuits of a directed graph", *SIAM Journal on Computing* **4**(1), 77–84 (1975).
- [63] E. L. Ogburn and T. J. VanderWeele, "Causal diagrams for interference", *Statistical Science* **29**(4), 559–578 (2014).
- [64] S. Jain and B. C. Wallace, "Attention is not Explanation", in *Proceedings of the 2019 Conference of the North American Chapter of the Association for Computational Linguistics (NAACL-HLT)*, 3543–3556 (2019).
- [65] S. Wiegreffe and Y. Pinter, "Attention is not not Explanation", in *Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP-IJCNLP)*, 11–20 (2019).
- [66] C. Rudin, "Stop explaining black box machine learning models for high stakes decisions and use interpretable models instead", *Nature Machine Intelligence* **1**, 206–215 (2019).
- [67] A. Hogan, E. Blomqvist, M. Cochez, C. d'Amato, G. de Melo, C. Gutiérrez, S. Kirrane, J. E. Labra Gayo, R. Navigli, S. Neumaier, A.-C. Ngonga Ngomo, A. Polleres, S. M. Rashid, A. Rula, L. Schmelzeisen, J. Sequeda, S. Staab and A. Zimmermann, "Knowledge Graphs", *ACM Computing Surveys* **54**(4), Article 71 (2021).
- [68] T. N. Kipf and M. Welling, "Semi-supervised classification with graph convolutional networks", in *Proceedings of the 5th International Conference on Learning Representations (ICLR)* (2017); arXiv:1609.02907.
- [69] T. Schreiber, "Measuring information transfer", *Physical Review Letters* **85**(2), 461–464 (2000).
- [70] L. Barnett, A. B. Barrett and A. K. Seth, "Granger causality and transfer entropy are equivalent for Gaussian variables", *Physical Review Letters* **103**(23), 238701 (2009).
- [71] T. M. Cover and J. A. Thomas, *Elements of Information Theory*, 2nd ed., Wiley (2006).
- [72] S. J. Mason, "Feedback theory — Further properties of signal flow graphs", *Proceedings of the IRE* **44**(7), 920–926 (1956).
- [73] L. Katz, "A new status index derived from sociometric analysis", *Psychometrika* **18**(1), 39–43 (1953).
- [74] P. Bonacich, "Power and centrality: A family of measures", *American Journal of Sociology* **92**(5), 1170–1182 (1987).
- [75] J. Hopcroft and R. Tarjan, "Algorithm 447: Efficient algorithms for graph manipulation", *Communications of the ACM* **16**(6), 372–378 (1973).
- [76] R. A. Horn and C. R. Johnson, *Matrix Analysis*, 2nd ed., Cambridge University Press (2013).
- [77] J. Gilmer, S. S. Schoenholz, P. F. Riley, O. Vinyals and G. E. Dahl, "Neural message passing for quantum chemistry", in *Proceedings of the 34th International Conference on Machine Learning (ICML)*, PMLR **70**, 1263–1272 (2017).
- [78] K. Xu, W. Hu, J. Leskovec and S. Jegelka, "How powerful are graph neural networks?", in *Proceedings of the 7th International Conference on Learning Representations (ICLR)* (2019); arXiv:1810.00826.
- [79] D. Acemoglu, V. M. Carvalho, A. Ozdaglar and A. Tahbaz-Salehi, "The network origins of aggregate fluctuations", *Econometrica* **80**(5), 1977–2016 (2012).
- [80] D. Acemoglu, A. Ozdaglar and A. Tahbaz-Salehi, "Systemic risk and stability in financial networks", *American Economic Review* **105**(2), 564–608 (2015).
- [81] M. Elliott, B. Golub and M. O. Jackson, "Financial networks and contagion", *American Economic Review* **104**(10), 3115–3153 (2014).
- [82] L. Eisenberg and T. H. Noe, "Systemic risk in financial systems", *Management Science* **47**(2), 236–249 (2001).
- [83] P. Gai and S. Kapadia, "Contagion in financial networks", *Proceedings of the Royal Society A* **466**(2120), 2401–2423 (2010).
- [84] F. X. Diebold and K. Yılmaz, "On the network topology of variance decompositions: Measuring the connectedness of financial firms", *Journal of Econometrics* **182**(1), 119–134 (2014).
- [85] M. Billio, M. Getmansky, A. W. Lo and L. Pelizzon, "Econometric measures of connectedness and systemic risk in the finance and insurance sectors", *Journal of Financial Economics* **104**(3), 535–559 (2012).
- [86] B. S. Bernanke and K. N. Kuttner, "What explains the stock market's reaction to Federal Reserve policy?", *The Journal of Finance* **60**(3), 1221–1257 (2005).
- [87] G. Gopinath, E. Boz, C. Casas, F. J. Díez, P.-O. Gourinchas and M. Plagborg-Møller, "Dominant currency paradigm", *American Economic Review* **110**(3), 677–719 (2020).
- [88] R. E. Lucas, Jr., "Econometric policy evaluation: A critique", *Carnegie-Rochester Conference Series on Public Policy* **1**, 19–46 (1976).
- [89] E. E. Leamer, "Let's take the con out of econometrics", *American Economic Review* **73**(1), 31–43 (1983).
- [90] D. A. Freedman, "Statistical models and shoe leather", *Sociological Methodology* **21**, 291–313 (1991).
- [91] A. Deaton, "Instruments, randomization, and learning about development", *Journal of Economic Literature* **48**(2), 424–455 (2010).
- [92] J. J. Heckman and S. Urzúa, "Comparing IV with structural models: What simple IV can and cannot identify", *Journal of Econometrics* **156**(1), 27–37 (2010).
- [93] G. W. Imbens, "Better LATE than nothing: Some comments on Deaton (2009) and Heckman and Urzua (2009)", *Journal of Economic Literature* **48**(2), 399–423 (2010).
- [94] C. F. Manski, "Identification of endogenous social effects: The reflection problem", *The Review of Economic Studies* **60**(3), 531–542 (1993).
- [95] J. D. Angrist, "The perils of peer effects", *Labour Economics* **30**, 98–108 (2014).
- [96] J. D. Angrist and J.-S. Pischke, *Mostly Harmless Econometrics: An Empiricist's Companion*, Princeton University Press (2009).
- [97] M. A. Hernán and J. M. Robins, *Causal Inference: What If*, Chapman & Hall/CRC (2020).
- [98] S. L. Morgan and C. Winship, *Counterfactuals and Causal Inference: Methods and Principles for Social Research*, 2nd ed., Cambridge University Press (2015).
- [99] P. Spirtes, C. Glymour and R. Scheines, *Causation, Prediction, and Search*, 2nd ed., MIT Press (2000).
- [100] J. D. Hamilton, *Time Series Analysis*, Princeton University Press (1994).
- [101] H. Lütkepohl, *New Introduction to Multiple Time Series Analysis*, Springer (2005).
- [102] J. M. Wooldridge, *Econometric Analysis of Cross Section and Panel Data*, 2nd ed., MIT Press (2010).
- [103] S. Shimizu, P. O. Hoyer, A. Hyvärinen and A. Kerminen, "A linear non-Gaussian acyclic model for causal discovery", *Journal of Machine Learning Research* **7**, 2003–2030 (2006).
- [104] J. Peters, P. Bühlmann and N. Meinshausen, "Causal inference by using invariant prediction: Identification and confidence intervals", *Journal of the Royal Statistical Society: Series B* **78**(5), 947–1012 (2016).
- [105] D. M. Chickering, "Optimal structure identification with greedy search", *Journal of Machine Learning Research* **3**, 507–554 (2002).
- [106] P. O. Hoyer, D. Janzing, J. M. Mooij, J. Peters and B. Schölkopf, "Nonlinear causal discovery with additive noise models", in *Advances in Neural Information Processing Systems 21 (NIPS 2008)*, 689–696 (2008).
- [107] I. Andrews, J. H. Stock and L. Sun, "Weak instruments in instrumental variables regression: Theory and practice", *Annual Review of Economics* **11**, 727–753 (2019).
- [108] N. Guarino, D. Oberle and S. Staab, "What is an ontology?", in S. Staab and R. Studer (eds), *Handbook on Ontologies*, 2nd ed., Springer, 1–17 (2009).
- [109] Q. Wang, Z. Mao, B. Wang and L. Guo, "Knowledge graph embedding: A survey of approaches and applications", *IEEE Transactions on Knowledge and Data Engineering* **29**(12), 2724–2743 (2017).
- [110] S. Ji, S. Pan, E. Cambria, P. Marttinen and P. S. Yu, "A survey on knowledge graphs: Representation, acquisition, and applications", *IEEE Transactions on Neural Networks and Learning Systems* **33**(2), 494–514 (2022).
- [111] T. Berners-Lee, J. Hendler and O. Lassila, "The Semantic Web", *Scientific American* **284**(5), 34–43 (2001).
- [112] C. A. Sims, "Money, income, and causality", *American Economic Review* **62**(4), 540–552 (1972).
- [113] K. Mertens and M. O. Ravn, "The dynamic effects of personal and corporate income tax changes in the United States", *American Economic Review* **103**(4), 1212–1247 (2013).
- [114] T. Miller, "Explanation in artificial intelligence: Insights from the social sciences", *Artificial Intelligence* **267**, 1–38 (2019).
