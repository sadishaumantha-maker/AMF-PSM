# P105 - Conflicting jurisdictional requirements as an unsatisfiable constraint set

**Track R - Geopolitics, Sanctions and Fragmentation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Comparative regulation researcher |
| **Upstream** | Discussion 1.1; Discussion 7.3 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The harmonisation discussion notes that data-sharing and disclosure regimes can require incompatible things of the same participant. The framework models the immune system as a stack of constraints, and a stack that cannot be simultaneously satisfied is a different object from a stack that is merely strict. The model currently has no way to be unsatisfiable.

## 2. Purpose

Give the framework a representation for constraint conflict, since an unsatisfiable immune stack is a real structural condition and currently renders as a merely high score.

## 3. Scope

**In scope**

- A structural definition of constraint conflict between tiers or jurisdictions.
- An assessment of what the current model renders when constraints conflict.
- A representation proposal.

**Out of scope**

- Legal advice on any actual conflict.
- Naming a live dispute between authorities.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Define conflict precisely: two binding requirements that cannot both be satisfied by the same participant at the same time. That is a property of the rule set, not of anyone's compliance.
2. Test what the framework currently does. If more constraints simply means a higher immune score, then a conflicting stack scores *better* than a coherent one, which would be a clear defect worth demonstrating numerically.
3. Propose the representation: conflict as a reduction in effective coverage rather than an addition to it, so that an unsatisfiable stack scores worse than a satisfiable one.
4. Use documented regime conflicts described in the scholarly and official literature rather than live disputes, and describe them generically.
5. Coordinate with P44's harmonisation work so conflict and harmonisability are two sides of one treatment.
6. State the consequence for any jurisdiction whose profile shows many overlapping tiers.

## 5. Task board

- [ ] Define constraint conflict formally.
- [ ] Demonstrate what the current model scores for a conflicting stack.
- [ ] Propose conflict as reduced effective coverage.
- [ ] Use generic rather than live examples.
- [ ] Coordinate with P44.
- [ ] Publish `docs/policy/constraint_conflict.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** Define conflict and express its effect on effective coverage.
- **Inputs:** The immune-stack model.
- **Output artifact:** A formal definition.
- **Stop condition:** Conflict is expressed as a property of the rule set.

### `benchmark-runner`

- **Mandate:** Demonstrate the current model's score for a conflicting stack.
- **Inputs:** The simulator and a constructed market.
- **Output artifact:** A demonstration.
- **Stop condition:** The perverse-scoring behaviour is shown numerically or shown not to occur.

### `regime-comparativist`

- **Mandate:** Document conflict types generically with scholarly citations.
- **Inputs:** The literature.
- **Output artifact:** A conflict-type table.
- **Stop condition:** No live dispute between named authorities is described.

**Hand-off order:** `math-formalizer` -> `benchmark-runner` -> `regime-comparativist`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-regime-profile` | A conflict type is recorded | Cites the instruments generically with vintages. |
| `amf-invariant-spec` | Effective coverage is redefined | Writes the invariant and mirrors it as a test. |
| `amf-red-team` | A representation is proposed | Constructs a stack the representation scores wrongly. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/constraint_conflict.md`
- A formal definition
- A numeric demonstration of current behaviour
- A representation proposal

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Conflict is defined as a property of the rule set.
- [ ] The current model's behaviour on a conflicting stack is demonstrated numerically.
- [ ] No live dispute between named authorities appears.
- [ ] The treatment is consistent with P44.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Committee of Wise Men (2001). *Final Report of the Committee of Wise Men on the Regulation of European Securities Markets* (the Lamfalussy Report). European Commission.
- European Union (2014). *Directive 2014/65/EU on markets in financial instruments (MiFID II)*. Official Journal of the European Union.
- United States Congress (2010). *Dodd-Frank Wall Street Reform and Consumer Protection Act*, Pub. L. 111-203.
- Djankov, S., La Porta, R., Lopez-de-Silanes, F., & Shleifer, A. (2008). "The law and economics of self-dealing." *Journal of Financial Economics* 88(3), 430-465.
- La Porta, R., Lopez-de-Silanes, F., Shleifer, A., & Vishny, R. W. (1998). "Law and Finance." *Journal of Political Economy* 106(6), 1113-1155.
- Ostrom, E. (2005). *Understanding Institutional Diversity*. Princeton University Press.
- International Monetary Fund (2023). "Geoeconomic Fragmentation and the Future of Multilateralism." IMF Staff Discussion Note SDN/2023/001.

## 11. Commit protocol

Commits from this project use the scope `p105`:

```text
docs(p105): define constraint conflict as an unsatisfiable immune stack
test(p105): demonstrate what the model scores for a conflicting stack
docs(p105): propose conflict as reduced rather than added coverage
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

