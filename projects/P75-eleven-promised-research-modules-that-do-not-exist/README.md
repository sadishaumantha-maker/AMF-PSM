# P75 - Eleven promised research modules that do not exist

**Track M - Live Defects and the Green-Main Obligation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 3 days |
| **Lead role** | Documentation owner |
| **Upstream** | `docs/discussions/README.md`; the eleven dead links failing `Validate metadata` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

> [!IMPORTANT]
> **Status against `main`.** **Partly resolved on `main` while this charter was in review.** `docs/discussions/README.md` now renders the eleven module names as plain filenames rather than links, with a status callout saying the files are not committed yet, so `Validate metadata` passes without pretending the modules exist. That is exactly the immediate change section 3 asked for, and task 3 is done.
>
> The rest of the charter stands unchanged: the per-module write-or-retire ruling, the link-is-a-claim rule in the conventions, and the module-to-charter mapping. The mapping now has a concrete answer - Track T (P113-P123) writes all eleven, one charter per module - so record it in the index and turn each filename back into a link in the same pull request that adds its file.

---

## 1. The dispute this project settles

`docs/discussions/README.md` is an index linking to eleven module files - `Q1-quantum-market-superposition.md` through `I2-validation-backtesting-generalization.md` - and the directory contains only the index. Every one of those links is dead, which is what fails the `Validate metadata` job. The dispute is whether to write the eleven modules or to stop promising them, and it cannot be dodged: an index that links to nothing is worse than no index, because it advertises depth the repository does not have.

## 2. Purpose

Decide, per module, write-or-retire; then make the index true. Track T carries the eleven modules that are kept, so this charter's own job is the ruling and the immediate un-breaking of the build.

## 3. Scope

**In scope**

- A per-module ruling: write it (and which Track T charter owns it) or remove the link.
- An immediate change that makes `Validate metadata` pass without pretending the modules exist.
- A rule preventing an index from linking to an unwritten file again.

**Out of scope**

- Writing the module content - that is Tracks T (P113-P123).
- Suppressing the link check or adding the paths to an ignore list.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. List the eleven targets and confirm each is genuinely absent rather than misnamed; a typo and an unwritten file need different fixes.
2. For each, rule write-or-retire on one question: does the discussion behind it name a dispute the framework must settle, or is it a topic someone found interesting?
3. Un-break the build now. Convert links to unwritten modules into plain text with a stated status, so the index still communicates the plan without asserting a file exists.
4. Do not add the paths to `.github/mlc-config.json`. Ignoring a dead link hides the defect rather than fixing it; the config exists for hosts that rate-limit, not for our own missing files.
5. Add the rule to the documentation conventions: a relative link is a claim that the target exists, and the link check enforces it. Write the file first, or write plain text.
6. Hand each kept module to its Track T charter and record the mapping in the index.

## 5. Task board

- [ ] Confirm all eleven targets are absent, not misnamed.
- [ ] Rule write-or-retire per module.
- [ ] Convert unwritten-module links to status-bearing plain text.
- [ ] Verify `Validate metadata` passes.
- [ ] Add the link-is-a-claim rule to the conventions.
- [ ] Record the module-to-charter mapping in the index.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `docs-synthesizer`

- **Mandate:** Rule per module and rewrite the index so every remaining link resolves.
- **Inputs:** `docs/discussions/README.md`, `docs/QUANTUM_NEURAL_RESEARCH.md`.
- **Output artifact:** A rewritten index.
- **Stop condition:** Every relative link in the index resolves and every unwritten module is marked as planned, not linked.

### `red-team-critic`

- **Mandate:** Check the rewritten index cannot be read as claiming content that does not exist.
- **Inputs:** The draft index.
- **Output artifact:** A misreading report.
- **Stop condition:** No entry implies a document a reader could try to open.

### `spec-drafter`

- **Mandate:** Write the link-is-a-claim convention and the module-to-charter mapping.
- **Inputs:** The rulings.
- **Output artifact:** A conventions addition plus the mapping table.
- **Stop condition:** Every kept module names the charter that will write it.

**Hand-off order:** `docs-synthesizer` -> `red-team-critic` -> `spec-drafter`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-doc-page` | The index is rewritten | Enforces relative-link resolution and the documentation conventions. |
| `amf-red-team` | Before the index is merged | Tests whether any entry advertises content that does not exist. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- A per-module write-or-retire ruling
- A rewritten index whose links all resolve
- The link-is-a-claim convention
- A module-to-charter mapping

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] `Validate metadata` passes with zero dead links.
- [ ] No path is added to the link-check ignore list to achieve that.
- [ ] Every kept module names the Track T charter that will write it.
- [ ] The conventions state that a relative link asserts the target exists.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Wilson, G., Bryan, J., Cranston, K., Kitzes, J., Nederbragt, L., & Teal, T. K. (2017). "Good enough practices in scientific computing." *PLoS Computational Biology* 13(6), e1005510.
- Sandve, G. K., Nekrutenko, A., Taylor, J., & Hovig, E. (2013). "Ten Simple Rules for Reproducible Computational Research." *PLoS Computational Biology* 9(10), e1003285.
- Bowker, G. C., & Star, S. L. (1999). *Sorting Things Out: Classification and Its Consequences*. MIT Press.
- Hunt, A., & Thomas, D. (2019). *The Pragmatic Programmer* (20th Anniversary ed.). Addison-Wesley.
- Wilkinson, M. D., et al. (2016). "The FAIR Guiding Principles for scientific data management and stewardship." *Scientific Data* 3, 160018.

## 11. Commit protocol

Commits from this project use the scope `p75`:

```text
docs(p75): rule write-or-retire on the eleven promised research modules
fix(p75): stop the discussion index linking to unwritten files
docs(p75): record the link-is-a-claim documentation convention
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
