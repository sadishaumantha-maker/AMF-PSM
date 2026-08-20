# P120 - H2 - persistent homology, and the one stability theorem that makes it usable

**Track T - The Promised Research Modules**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Applied topologist |
| **Upstream** | `docs/discussions/README.md` module H2 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

H2 promises topological data analysis. Unlike the other hybrid modules, this one has a result in its favour: persistence diagrams are provably stable under bounded perturbation of the input, which is exactly the property a diagnostic instrument needs and exactly what the framework's sensitivity analysis is groping toward with finite differences. The dispute is whether that theorem transfers to a seven-node graph, where the filtration has almost nothing to filter.

## 2. Purpose

State the stability theorem exactly, test whether a seven-node dependency graph supports a meaningful filtration, and rule on whether persistence tells the framework anything its existing queries do not.

## 3. Scope

**In scope**

- Simplicial homology and persistence stated exactly, at the level the index specifies.
- The stability theorem with its metric and its hypotheses.
- A concrete filtration on the framework's weighted dependency graph, worked through.
- A comparison against what feedback-loop enumeration and articulation points already report.

**Out of scope**

- Any topology library dependency - the assessment is on paper.
- Takens embedding of a market series, which requires a time series the framework does not hold.
- Claims that a persistence feature indicates a real market condition.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Build the filtration concretely before assessing it: sort the edge weights descending, add edges as the threshold falls, and record when connected components merge and when cycles appear. That is a real filtration on a real object in this repository, and the module should carry it end to end on `examples/sample_market.json`.
2. State the stability theorem with its metric - the bottleneck distance - and its hypotheses. Stability is the claim that a small change in the filtration function makes a small change in the diagram, and the module must state the norm in which each smallness is measured.
3. Compare against what already exists. Zero-dimensional persistence on this filtration tracks component merging, which is closely related to the articulation-point query; one-dimensional persistence tracks cycles, which is closely related to feedback-loop enumeration. Work out whether the relationship is identity, refinement or something else, and say which.
4. Report the size problem plainly. Seven nodes and a handful of edges give a diagram with a handful of points, and the machinery's asymptotic advantages do not arise at that scale.
5. Rule out Takens embedding here explicitly, on the ground that it needs a time series, and note that the only series the framework produces is a simulated stress trajectory - so applying it to that would measure the simulator, not a market.
6. Write section 7's propositions about the relationship to the existing queries, which is checkable by computation, rather than about market relevance, which is not.

## 5. Task board

- [ ] Build the descending-weight filtration on the sample market.
- [ ] State persistence and the stability theorem exactly.
- [ ] Compare zero- and one-dimensional persistence against existing queries.
- [ ] Report the small-graph size finding.
- [ ] Rule out Takens embedding with the reason stated.
- [ ] Publish `docs/discussions/H2-topological-data-analysis.md` and relink it.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Assemble the persistence and stability primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated bibliography.
- **Stop condition:** The stability theorem is cited to the paper that proved it.

### `math-formalizer`

- **Mandate:** State persistence and stability exactly and build the filtration on the sample market.
- **Inputs:** `graph.py`, `examples/sample_market.json`.
- **Output artifact:** A worked filtration and diagram.
- **Stop condition:** The diagram is computed by hand or by stdlib code, with no library dependency.

### `benchmark-runner`

- **Mandate:** Compare the persistence output against the existing loop and articulation queries.
- **Inputs:** The filtration, `graph.py`.
- **Output artifact:** A comparison with reproduction commands.
- **Stop condition:** The relationship is characterised as identity, refinement or neither.

### `spec-drafter`

- **Mandate:** Write the module including the size finding and the Takens exclusion.
- **Inputs:** All of the above.
- **Output artifact:** `docs/discussions/H2-topological-data-analysis.md`.
- **Stop condition:** The Takens exclusion states its reason.

### `red-team-critic`

- **Mandate:** Attack any claim that a persistence feature means something about a real market.
- **Inputs:** The draft.
- **Output artifact:** An adversarial report.
- **Stop condition:** No persistence feature is given a market interpretation.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `benchmark-runner` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-graph-algorithm` | The filtration is built | Verifies the construction against its source and states complexity. |
| `amf-invariant-spec` | Stability is stated | Records the metric and hypotheses the theorem requires. |
| `amf-literature-brief` | The sources are assembled | Produces the annotated brief. |
| `amf-doc-page` | The module is published | Enforces conventions and disclaimers. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/discussions/H2-topological-data-analysis.md`
- A worked filtration on the sample market
- A comparison against loop and articulation queries
- A stated size finding

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The filtration is carried end to end on a real repository example.
- [ ] The stability theorem is stated with metric and hypotheses.
- [ ] The relationship to existing queries is characterised, not gestured at.
- [ ] Takens embedding is excluded with its reason.
- [ ] No topology library is introduced.
- [ ] The index link resolves.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Carlsson, G. (2009). "Topology and Data." *Bulletin of the American Mathematical Society* 46(2), 255-308.
- Edelsbrunner, H., & Harer, J. L. (2010). *Computational Topology: An Introduction*. American Mathematical Society.
- Zomorodian, A., & Carlsson, G. (2005). "Computing Persistent Homology." *Discrete & Computational Geometry* 33(2), 249-274.
- Cohen-Steiner, D., Edelsbrunner, H., & Harer, J. (2007). "Stability of Persistence Diagrams." *Discrete & Computational Geometry* 37(1), 103-120.
- Ghrist, R. (2008). "Barcodes: The persistent topology of data." *Bulletin of the American Mathematical Society* 45(1), 61-75.
- Otter, N., Porter, M. A., Tillmann, U., Grindrod, P., & Harrington, H. A. (2017). "A roadmap for the computation of persistent homology." *EPJ Data Science* 6, 17.
- Perea, J. A., & Harer, J. (2015). "Sliding Windows and Persistence: An Application of Topological Methods to Signal Analysis." *Foundations of Computational Mathematics* 15(3), 799-838.
- Takens, F. (1981). "Detecting strange attractors in turbulence." In *Dynamical Systems and Turbulence, Warwick 1980*, Lecture Notes in Mathematics 898, 366-381. Springer.
- Gidea, M., & Katz, Y. (2018). "Topological data analysis of financial time series: Landscapes of crashes." *Physica A* 491, 820-834.
- Tarjan, R. (1972). "Depth-First Search and Linear Graph Algorithms." *SIAM Journal on Computing* 1(2), 146-160.

## 11. Commit protocol

Commits from this project use the scope `p120`:

```text
docs(p120): build the weight filtration and state the stability theorem
docs(p120): compare persistence against the existing structural queries
docs(p120): publish the H2 module and relink it from the index
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
