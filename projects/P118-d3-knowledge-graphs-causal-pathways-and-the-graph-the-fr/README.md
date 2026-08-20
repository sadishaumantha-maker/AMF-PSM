# P118 - D3 - knowledge graphs, causal pathways, and the graph the framework already has

**Track T - The Promised Research Modules**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2.5 weeks |
| **Lead role** | Causal-inference researcher |
| **Upstream** | `docs/discussions/README.md` module D3 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

D3 promises knowledge graphs and causal pathways. The framework's `DependencyGraph` is already a labelled directed graph over seven typed nodes with four edge kinds, which is a knowledge graph with a very small schema. The sharp dispute is causal: the framework reads its edges as dependence and propagates stress along them as if they were causal channels, which is a causal reading of a structural graph nobody has identified. Whether that reading is licensed is the module's real subject.

## 2. Purpose

State exactly what causal claim the propagation step makes, test it against the identification conditions the causal literature requires, and rule on whether the framework may keep making it.

## 3. Scope

**In scope**

- The framework's existing graph stated as a knowledge graph, schema included.
- The causal claim implicit in stress propagation, written out as a claim.
- The identification conditions from primary sources, checked one by one.
- A ruling, with the required change to the documentation if the claim is unlicensed.

**Out of scope**

- Estimating any causal effect from data.
- Adding a causal-discovery algorithm to the package.
- Renaming `Dependency` - the naming question belongs to whichever charter owns it, not here.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Write the implicit claim out first, in one sentence: stress at a system's target raises stress at the system, in proportion to edge weight, because the dependency exists. That is a causal claim about a mechanism, and stating it plainly is most of the work.
2. State the identification conditions from primary sources - the causal Markov condition, faithfulness, no unmeasured confounding, and what an intervention means in a structural causal model. Check each against a seven-system market and write the verdict per condition.
3. Confront the confounding problem directly: two systems may covary because both depend on something the seven-system model does not contain, and the model has no way to represent that. Say so.
4. Distinguish the two defensible positions from the indefensible middle. The framework may say it propagates stress along declared structural couplings as a definitional consequence of the model - which is a claim about the model, not the world - or it may claim causal transmission and accept the identification burden. It may not do the first while sounding like the second, which is what the current documentation does.
5. Rule, and write the documentation change the ruling requires, since the wording in `simulation.py`'s docstrings is where the ambiguity lives.
6. Cover ontologies and schema properly - the knowledge-graph half is real work, and `SystemKind` plus `DependencyKind` is a schema that could be stated formally.

## 5. Task board

- [ ] State the framework's graph as a knowledge graph with an explicit schema.
- [ ] Write out the causal claim implicit in propagation.
- [ ] Check each identification condition and record a per-condition verdict.
- [ ] State the confounding problem in the seven-system model.
- [ ] Rule between the definitional and the causal reading.
- [ ] Specify the documentation change the ruling requires.
- [ ] Publish `docs/discussions/D3-knowledge-graphs-causal-pathways.md` and relink it.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Assemble the causal-inference and knowledge-graph primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated bibliography.
- **Stop condition:** Identification conditions are cited to primary texts, not to secondary summaries.

### `taxonomy-cartographer`

- **Mandate:** State `SystemKind` and `DependencyKind` as a formal knowledge-graph schema.
- **Inputs:** `models.py`, `graph.py`.
- **Output artifact:** A schema statement.
- **Stop condition:** Every node and edge type in the code appears in the schema.

### `math-formalizer`

- **Mandate:** Write the causal claim and check each identification condition against it.
- **Inputs:** `simulation.py`, the sources.
- **Output artifact:** A per-condition verdict table.
- **Stop condition:** Confounding is addressed with a concrete example, not in the abstract.

### `spec-drafter`

- **Mandate:** Write the ruling and the exact documentation change it requires.
- **Inputs:** The verdicts.
- **Output artifact:** `docs/discussions/D3-knowledge-graphs-causal-pathways.md` and a docstring change list.
- **Stop condition:** The change list names files and sentences, not areas.

### `red-team-critic`

- **Mandate:** Attack the ruling by reading the current docstrings in the most causal way available.
- **Inputs:** `simulation.py`, the ruling.
- **Output artifact:** An adversarial reading.
- **Stop condition:** Every sentence that reads as a causal claim is either defended or listed for change.

**Hand-off order:** `literature-scout` -> `taxonomy-cartographer` -> `math-formalizer` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-graph-algorithm` | The graph is stated formally | Verifies each structural query against its source and states complexity. |
| `amf-taxonomy-builder` | The schema is written | Builds the schema table against the published types. |
| `amf-literature-brief` | The sources are assembled | Produces the annotated brief. |
| `amf-red-team` | The ruling is drafted | Reads the documentation adversarially for unlicensed causal claims. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/discussions/D3-knowledge-graphs-causal-pathways.md`
- A formal schema for the framework's graph
- A per-condition identification verdict
- A docstring change list

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The causal claim implicit in propagation is written out in one sentence.
- [ ] Each identification condition receives its own verdict.
- [ ] The confounding problem is stated with a concrete example.
- [ ] The ruling forbids the ambiguous middle position explicitly.
- [ ] The docstring change list names files and sentences.
- [ ] The index link resolves.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Pearl, J. (2009). *Causality: Models, Reasoning, and Inference* (2nd ed.). Cambridge University Press.
- Peters, J., Janzing, D., & Scholkopf, B. (2017). *Elements of Causal Inference: Foundations and Learning Algorithms*. MIT Press.
- Spirtes, P., Glymour, C., & Scheines, R. (2000). *Causation, Prediction, and Search* (2nd ed.). MIT Press.
- Imbens, G. W., & Rubin, D. B. (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences*. Cambridge University Press.
- Hernan, M. A., & Robins, J. M. (2020). *Causal Inference: What If*. Chapman & Hall/CRC.
- Hogan, A., et al. (2021). "Knowledge Graphs." *ACM Computing Surveys* 54(4), 71.
- Granger, C. W. J. (1969). "Investigating Causal Relations by Econometric Models and Cross-spectral Methods." *Econometrica* 37(3), 424-438.
- Sugihara, G., et al. (2012). "Detecting Causality in Complex Ecosystems." *Science* 338(6106), 496-500.
- Gruber, T. R. (1993). "A translation approach to portable ontology specifications." *Knowledge Acquisition* 5(2), 199-220.
- Bowker, G. C., & Star, S. L. (1999). *Sorting Things Out: Classification and Its Consequences*. MIT Press.

## 11. Commit protocol

Commits from this project use the scope `p118`:

```text
docs(p118): state the causal claim implicit in stress propagation
docs(p118): check the identification conditions and rule on the reading
docs(p118): publish the D3 module and list the docstring changes it requires
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

