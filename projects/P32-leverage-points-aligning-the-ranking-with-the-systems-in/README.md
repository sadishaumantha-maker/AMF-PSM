# P32 - Leverage points: aligning the ranking with the systems-intervention literature

**Track E - Diagnostics, Sensitivity & Leverage**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Systems methodologist |
| **Upstream** | `LeveragePoint`; `SystemMetric.improving_direction()` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The framework ranks leverage points by the index improvement achievable by moving a metric in its improving direction, and excludes criticality on the grounds that it describes how load-bearing a system *is* rather than a lever. The systems literature that gives "leverage points" its name ranks intervention types in almost the opposite order - parameters are the weakest leverage, rules and goals the strongest. The framework's leverage points are all parameters.

## 2. Purpose

Reconcile the framework's parameter-level leverage ranking with the established hierarchy of intervention leverage, and state honestly which kinds of intervention AMF can and cannot see.

## 3. Scope

**In scope**

- A mapping of AMF's metric levers onto the established intervention hierarchy.
- A statement of the intervention classes AMF is structurally blind to.
- A presentation change so that a top-ranked leverage point is not read as the most powerful intervention available.

**Out of scope**

- Adding intervention types the framework cannot model.
- Claiming predictive power for any intervention.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Place each of the four metrics on the intervention hierarchy; all four are parameters or close to it.
2. Identify what the hierarchy calls higher leverage - feedback loop structure, rules, goals, paradigms - and check which of those AMF represents at all.
3. Note that AMF does represent dependency structure and feedback loops, so some higher-leverage classes are within reach and simply are not surfaced as levers.
4. Decide whether structural levers (adding redundancy paths, cutting a dependency) should be first-class leverage points alongside metric levers.
5. Change the presentation so that the ranking states its own scope: these are the strongest *parameter* levers, not the strongest levers.
6. Where a metric has no headroom in its improving direction, keep producing no leverage point, and document why that is correct.

## 5. Task board

- [ ] Map the four metrics onto the intervention hierarchy.
- [ ] Identify representable higher-leverage classes.
- [ ] Decide on structural levers as first-class leverage points.
- [ ] Update the presentation to state the ranking's scope.
- [ ] Document the blind spots.
- [ ] Publish `docs/sensitivity/leverage_alignment.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish the intervention-leverage hierarchy from its primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated hierarchy summary.
- **Stop condition:** The hierarchy is quoted from a primary source, not paraphrased from memory.

### `spec-drafter`

- **Mandate:** Map AMF levers onto the hierarchy and state the blind spots plainly.
- **Inputs:** The hierarchy and `sensitivity.py`.
- **Output artifact:** `docs/sensitivity/leverage_alignment.md`.
- **Stop condition:** Every intervention class is marked representable, partially representable or invisible.

### `algorithm-implementer`

- **Mandate:** Implement structural levers if adopted, without breaking the existing ranking.
- **Inputs:** The decision.
- **Output artifact:** A diff under `src/amf/sensitivity.py`.
- **Stop condition:** `mypy` strict passes and the existing leverage output is preserved or explicitly migrated.

### `docs-synthesizer`

- **Mandate:** Rewrite the rendered leverage section so its scope is unmistakable.
- **Inputs:** The alignment document.
- **Output artifact:** A `report.py` text change.
- **Stop condition:** The rendered heading states that these are parameter-level levers.

**Hand-off order:** `literature-scout` -> `spec-drafter` -> `algorithm-implementer` -> `docs-synthesizer`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-doc-page` | Publishing the alignment document | Enforces documentation conventions and the illustrative-not-validated rule. |
| `amf-invariant-spec` | The no-headroom rule is documented | Writes it into the docstring and mirrors it as a test. |
| `amf-red-team` | The leverage presentation is drafted | Checks whether a reader could take a parameter lever for the strongest available intervention. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/sensitivity/leverage_alignment.md`
- A representability map of intervention classes
- A scope-stating presentation change
- Structural levers if adopted

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every intervention class is classified as representable, partial or invisible.
- [ ] The rendered leverage ranking states that it covers parameter-level levers.
- [ ] The no-headroom rule remains correct and tested.
- [ ] No claim of predictive power is introduced.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Meadows, D. H. (1999). *Leverage Points: Places to Intervene in a System*. The Sustainability Institute.
- Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green.
- Bertalanffy, L. von (1968). *General System Theory: Foundations, Development, Applications*. George Braziller.
- Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall. (Law of Requisite Variety)
- Beer, S. (1972). *Brain of the Firm: The Managerial Cybernetics of Organization*. Allen Lane.
- Simon, H. A. (1962). "The Architecture of Complexity." *Proceedings of the American Philosophical Society* 106(6), 467-482.
- Arthur, W. B. (2015). *Complexity and the Economy*. Oxford University Press.

## 11. Commit protocol

Commits from this project use the scope `p32`:

```text
docs(p32): map AMF metric levers onto the intervention leverage hierarchy
docs(p32): state the intervention classes AMF cannot see
feat(p32): report leverage points with explicit parameter-level scope
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
