# P106 - The sovereign-financial loop as a cycle the framework should be able to see

**Track R - Geopolitics, Sanctions and Fragmentation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Policy researcher |
| **Upstream** | Discussion 7.2; `graph.py` feedback loops |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The mutual dependence between a sovereign and its banking system is one of the best-documented feedback loops in modern finance, and the framework's headline capability is feedback-loop enumeration. If the model cannot represent this loop, that is a sharp test failure on the framework's own strongest claim - and nobody has attempted it.

## 2. Purpose

Attempt to express the sovereign-financial loop in the seven-system vocabulary, and treat the result as a direct test of the feedback machinery's expressive power.

## 3. Scope

**In scope**

- An attempt to place both sides of the loop within the seven systems.
- A verdict on whether the loop is expressible.
- The consequence for the feedback-amplification component either way.

**Out of scope**

- Any sovereign's creditworthiness.
- Holdings, spreads or ratings.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Attempt the placement honestly. The sovereign is not one of the seven systems, so the first question is whether it is inside the market at all or is an exogenous influence under P82's convention.
2. If the sovereign is exogenous, the loop leaves and re-enters the boundary, and the framework's cycle enumeration operates only inside - so the loop is invisible by construction. Establish whether that is so.
3. Treat the result as a test of the machinery. A framework whose flagship capability cannot see the canonical loop has learned something important about its own scope.
4. State the consequence for `feedback_amplification`: if important loops leave the boundary, the component measures internal loops only, and should say so.
5. Use the documented mechanism from the peer-reviewed literature, described generically without naming sovereigns.
6. Feed the finding into P128's resolution-and-scope work.

## 5. Task board

- [ ] Attempt to place both sides within the seven systems.
- [ ] Determine whether the loop crosses the boundary.
- [ ] Rule on expressibility.
- [ ] State the consequence for feedback amplification.
- [ ] Describe the mechanism generically.
- [ ] Publish `docs/policy/sovereign_financial_loop.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish the mechanism from peer-reviewed sources, generically.
- **Inputs:** The reading list.
- **Output artifact:** An annotated mechanism summary.
- **Stop condition:** No sovereign is named as an example.

### `math-formalizer`

- **Mandate:** Attempt the placement and rule on expressibility within the boundary.
- **Inputs:** The seven systems and P82's semantics.
- **Output artifact:** A formal attempt with a verdict.
- **Stop condition:** The verdict follows from the boundary semantics.

### `spec-drafter`

- **Mandate:** State the consequence for the feedback-amplification component.
- **Inputs:** The verdict.
- **Output artifact:** `docs/policy/sovereign_financial_loop.md`.
- **Stop condition:** If loops can leave the boundary, the component's scope is restated where it is documented.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `spec-drafter`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-graph-algorithm` | Cycle enumeration scope is assessed | Confirms what the enumeration does and does not traverse. |
| `amf-invariant-spec` | The component's scope is restated | Writes it into the docstring and mirrors it as a test. |
| `amf-doc-page` | The finding is published | Enforces documentation conventions and neutrality. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/sovereign_financial_loop.md`
- A placement attempt
- An expressibility verdict
- A restated feedback-component scope

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The placement attempt is made concretely, not deferred.
- [ ] The verdict follows from the stated boundary semantics.
- [ ] The feedback component's scope is restated where it is documented.
- [ ] No sovereign is named.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Acharya, V., Drechsler, I., & Schnabl, P. (2014). "A Pyrrhic Victory? Bank Bailouts and Sovereign Credit Risk." *Journal of Finance* 69(6), 2689-2739.
- Brunnermeier, M. K., Garicano, L., Lane, P. R., Pagano, M., Reis, R., Santos, T., Thesmar, D., Van Nieuwerburgh, S., & Vayanos, D. (2016). "The Sovereign-Bank Diabolic Loop and ESBies." *American Economic Review* 106(5), 508-512.
- Reinhart, C. M., & Rogoff, K. S. (2009). *This Time Is Different: Eight Centuries of Financial Folly*. Princeton University Press.
- Gai, P., & Kapadia, S. (2010). "Contagion in financial networks." *Proceedings of the Royal Society A* 466(2120), 2401-2423.
- Allen, F., & Gale, D. (2000). "Financial Contagion." *Journal of Political Economy* 108(1), 1-33.
- Johnson, D. B. (1975). "Finding all the elementary circuits of a directed graph." *SIAM Journal on Computing* 4(1), 77-84.
- Minsky, H. P. (1986). *Stabilizing an Unstable Economy*. Yale University Press.

## 11. Commit protocol

Commits from this project use the scope `p106`:

```text
docs(p106): attempt the sovereign-financial loop in the seven-system vocabulary
docs(p106): rule on whether boundary-crossing loops are enumerable
docs(p106): restate the feedback component's scope to internal loops
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

