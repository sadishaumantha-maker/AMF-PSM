# P117 - D2 - embedding spaces, regimes, and the two-dimensional picture that lies

**Track T - The Promised Research Modules**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Representation-learning researcher |
| **Upstream** | `docs/discussions/README.md` module D2 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

D2 promises latent representations of market regimes. The framework has a regime notion already, buried and unnamed: a market configuration either settles or saturates at the clip, and those are qualitatively different states. The dispute is whether a learned embedding adds anything to a seven-system description that is already low-dimensional, and whether the projection plots such work always produces are legitimate evidence or decorative artefacts that invite conclusions the geometry does not support.

## 2. Purpose

Assess embeddings against a description that is already twenty-eight dimensional, and write the projection warning the repository will need the first time someone draws a two-dimensional picture of anything.

## 3. Scope

**In scope**

- Manifold learning, the variational objective and contrastive objectives stated exactly.
- The dimensionality argument: what an embedding of a twenty-eight-number description could compress.
- The projection-pitfall section, with the distortions named and sourced.
- A regime definition the framework can actually state - settling versus saturating.

**Out of scope**

- Training an embedding on market data.
- Any regime label attached to a real market or period.
- Adding a plotting dependency - `viz.py` draws SVG with the standard library.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Do the dimensionality arithmetic first and let it drive the module. Twenty-eight metrics plus a sparse edge set is not high-dimensional data, and compression is what embeddings are for, so the burden is on the proposal to say what is being compressed.
2. State the objectives exactly - the evidence lower bound, the contrastive loss - rather than describing them. A module that gestures at a VAE without writing its objective cannot be checked.
3. Write the projection-pitfall section as the module's most useful contribution. Neighbourhood-preserving projections distort global structure by construction, cluster separation in the picture is not cluster separation in the data, and inter-cluster distances in such plots carry no meaning. Source each claim.
4. Define the regime notion the framework can support without learning anything: the trajectory either settles inside the step budget or hits the clip and stays there, and `tipped_systems` already records the second case. That is a two-state regime classification obtained by running the model.
5. Connect the warning to `viz.py` explicitly, since the repository's own figures are the place where a misleading projection would actually appear.
6. Write section 7's propositions about what an embedding would have to demonstrate to earn its place - a structural distinction the metric description misses - and state that no such distinction is currently known.

## 5. Task board

- [ ] Do the dimensionality arithmetic.
- [ ] State the variational and contrastive objectives exactly.
- [ ] Write the projection-pitfall section with sourced claims.
- [ ] Define the settling-versus-saturating regime notion.
- [ ] Connect the warning to `viz.py`'s figure conventions.
- [ ] Publish `docs/discussions/D2-embedding-spaces-regimes.md` and relink it.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Assemble representation-learning sources and the projection-criticism literature.
- **Inputs:** The reading list.
- **Output artifact:** An annotated bibliography with the criticism separated.
- **Stop condition:** The projection criticism is cited to work that measures the distortion.

### `math-formalizer`

- **Mandate:** Write the objectives exactly and do the dimensionality arithmetic.
- **Inputs:** The sources, `models.py`.
- **Output artifact:** An objectives-and-dimension note.
- **Stop condition:** The bound is written, not named.

### `viz-designer`

- **Mandate:** Turn the projection warning into a rule for the repository's own figures.
- **Inputs:** `viz.py`, the warning.
- **Output artifact:** A figure rule with the footnote requirement restated.
- **Stop condition:** The rule says what a figure may not imply, concretely.

### `spec-drafter`

- **Mandate:** Write the module with the regime definition the framework can support.
- **Inputs:** All of the above.
- **Output artifact:** `docs/discussions/D2-embedding-spaces-regimes.md`.
- **Stop condition:** The regime definition is operational - it names what to run and what to read.

### `red-team-critic`

- **Mandate:** Attack any claim that a learned regime label means something about a real market.
- **Inputs:** The draft.
- **Output artifact:** An adversarial report.
- **Stop condition:** No regime label is attached to a real market or period.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `viz-designer` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-figure-render` | The figure rule is written | Enforces the visual grammar and the mandatory footnote. |
| `amf-literature-brief` | The sources are assembled | Produces the annotated brief. |
| `amf-invariant-spec` | The regime definition is stated | Records what must hold for the classification to be well defined. |
| `amf-doc-page` | The module is published | Enforces conventions and disclaimers. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/discussions/D2-embedding-spaces-regimes.md`
- A dimensionality argument
- A sourced projection-pitfall section
- A figure rule for `viz.py` output

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The dimensionality arithmetic is shown and drives the assessment.
- [ ] The variational objective is written out.
- [ ] Every projection-distortion claim carries a source.
- [ ] The regime definition is operational without learning anything.
- [ ] No plotting dependency is introduced.
- [ ] The index link resolves.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Bengio, Y., Courville, A., & Vincent, P. (2013). "Representation Learning: A Review and New Perspectives." *IEEE Transactions on Pattern Analysis and Machine Intelligence* 35(8), 1798-1828.
- Mikolov, T., Sutskever, I., Chen, K., Corrado, G., & Dean, J. (2013). "Distributed Representations of Words and Phrases and their Compositionality." *Advances in Neural Information Processing Systems 26*.
- van der Maaten, L., & Hinton, G. (2008). "Visualizing Data using t-SNE." *Journal of Machine Learning Research* 9, 2579-2605.
- McInnes, L., Healy, J., & Melville, J. (2018). "UMAP: Uniform Manifold Approximation and Projection for Dimension Reduction." arXiv:1802.03426.
- Chari, T., & Pachter, L. (2023). "The specious art of single-cell genomics." *PLOS Computational Biology* 19(8), e1011288. (on the distortions of two-dimensional embeddings)
- Goodfellow, I., Bengio, Y., & Courville, A. (2016). *Deep Learning*. MIT Press.
- Murphy, K. P. (2022). *Probabilistic Machine Learning: An Introduction*. MIT Press.
- Hastie, T., Tibshirani, R., & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer.
- Munzner, T. (2014). *Visualization Analysis and Design*. CRC Press.
- Tufte, E. R. (2001). *The Visual Display of Quantitative Information* (2nd ed.). Graphics Press.

## 11. Commit protocol

Commits from this project use the scope `p117`:

```text
docs(p117): argue the dimensionality case for and against embeddings
docs(p117): write the projection-pitfall section and the figure rule
docs(p117): publish the D2 module and relink it from the index
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
