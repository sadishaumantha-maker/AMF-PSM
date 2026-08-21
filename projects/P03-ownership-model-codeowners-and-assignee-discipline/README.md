# P03 - Ownership model, CODEOWNERS and assignee discipline

**Track A - Governance, Ownership & Delivery Cadence**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 days |
| **Lead role** | Maintainer |
| **Upstream** | issues #103 (0.5), #148 (9.2), #110 (1.4) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Gap 4 records "no assignee clarity - ambiguous ownership". The unresolved question is whether ownership is *per module* (a code-owner model) or *per issue* (an assignee model). The two produce different review bottlenecks and different failure modes when a single maintainer is unavailable.

## 2. Purpose

Choose one ownership model on stated grounds, encode it in `CODEOWNERS`, and make ownership a hard precondition of the triaged predicate from P01.

## 3. Scope

**In scope**

- A written comparison of module-ownership versus issue-ownership against Conway's law and bus-factor risk.
- A `.github/CODEOWNERS` file matching the package architecture in `CLAUDE.md`.
- An escalation path when the owner is unavailable.

**Out of scope**

- Assigning real individuals without their consent; use role placeholders until acknowledged.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Map the module dependency order from `CLAUDE.md` onto candidate ownership boundaries.
2. Assess each boundary against Conway's law: does the ownership split match the coupling of the code?
3. Compute the current bus factor per module from `git log` authorship.
4. Choose the model and record the reasoning, including the rejected alternative.
5. Write `.github/CODEOWNERS` with role placeholders where a person has not yet acknowledged.
6. Wire ownership into the P01 triaged predicate as a required field.

## 5. Task board

- [ ] Compute per-module bus factor from repository history.
- [ ] Write the ownership model comparison note.
- [ ] Draft `.github/CODEOWNERS` aligned to `src/amf/` module boundaries.
- [ ] Define the unavailability escalation path.
- [ ] Collect governance-document acknowledgements (issue #110).
- [ ] Update the triaged predicate to require an owner.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** Write the ownership model comparison and the decision record.
- **Inputs:** Module map, bus-factor data.
- **Output artifact:** `docs/governance/ownership_model.md`.
- **Stop condition:** The rejected alternative is described as fairly as the chosen one.

### `api-surface-reviewer`

- **Mandate:** Verify that the proposed CODEOWNERS boundaries do not cut across the one-way dependency order.
- **Inputs:** `src/amf/`, draft CODEOWNERS.
- **Output artifact:** A boundary-alignment report.
- **Stop condition:** No owner boundary splits a module that must change atomically.

**Hand-off order:** `spec-drafter` -> `api-surface-reviewer`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-layering-check` | Ownership boundaries are proposed | Verifies the `errors/models -> systems/graph -> market -> diagnostics/simulation -> sensitivity -> report/viz/cli` order is unbroken. |
| `amf-doc-page` | Writing the decision record | Enforces documentation conventions. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/governance/ownership_model.md`
- `.github/CODEOWNERS`
- An updated triaged predicate.

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every open issue has an owner (metric 9.2 support).
- [ ] `CODEOWNERS` boundaries respect the module dependency order.
- [ ] Bus factor per module is recorded, and any module with bus factor 1 has a named mitigation.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Conway, M. E. (1968). "How Do Committees Invent?" *Datamation* 14(5), 28-31.
- Parnas, D. L. (1972). "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM* 15(12), 1053-1058.
- Brooks, F. P. (1995). *The Mythical Man-Month: Essays on Software Engineering* (Anniversary ed.). Addison-Wesley.
- Martin, R. C. (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.
- Forsgren, N., Humble, J., & Kim, G. (2018). *Accelerate: The Science of Lean Software and DevOps*. IT Revolution.

## 11. Commit protocol

Commits from this project use the scope `p03`:

```text
docs(p03): record bus factor per module and the ownership decision
chore(p03): add CODEOWNERS aligned to the package architecture
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
