# P06 - Charter ratification for the phase-2 and new-concepts backlog items

**Track A - Governance, Ownership & Delivery Cadence**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 4 days |
| **Lead role** | Maintainer |
| **Upstream** | issues #145 (7.2, #21), #146 (7.3, #23) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

#21 ("Creating phase 2") and #23 ("Creating whole new concepts for PSM") are open-ended and cannot be closed by any finite amount of work. The dispute is whether they are charters (statements of direction that are ratified and then closed) or epics (containers that are decomposed and then closed).

## 2. Purpose

Rule that both are charters, ratify their content as roadmap text, decompose any executable residue into concrete issues, and close the originals with an explicit disposition note.

## 3. Scope

**In scope**

- A disposition ruling for #21 and #23 under the P01 taxonomy.
- Ratified charter text merged into `docs/roadmap.md`.
- Newly opened, bounded issues for any executable residue.

**Out of scope**

- Executing the research the charters describe - that is the rest of this catalogue.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Apply the P01 issue-type taxonomy to #21 and #23 and record the classification with reasons.
2. Extract from each issue every statement that is a *direction* and every statement that is a *task*.
3. Merge the directions into `docs/roadmap.md` as ratified charter text.
4. Open one bounded issue per task, each with acceptance criteria.
5. Close the originals with a disposition comment linking the charter text and the new issues.

## 5. Task board

- [ ] Classify #21 and #23 under the triage constitution.
- [ ] Split each issue body into directions and tasks.
- [ ] Write the ratified charter sections.
- [ ] Open the derived bounded issues.
- [ ] Close the originals with disposition notes.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** Separate direction from task and write the ratified charter text.
- **Inputs:** Issue bodies for #21 and #23.
- **Output artifact:** Charter sections for `docs/roadmap.md`.
- **Stop condition:** No sentence in the charter text describes work that a person could be assigned.

### `red-team-critic`

- **Mandate:** Attempt to prove the charter text is unfalsifiable padding.
- **Inputs:** Draft charter text.
- **Output artifact:** A critique with proposed deletions.
- **Stop condition:** Every retained sentence either constrains a future decision or is deleted.

**Hand-off order:** `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-doc-page` | Merging charter text into the roadmap | Enforces documentation conventions. |
| `amf-red-team` | Before ratification | Removes sentences that cannot constrain any future decision. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- Ratified charter sections in `docs/roadmap.md`
- Bounded derived issues
- Disposition comments on #21 and #23

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] #21 and #23 are closed with a linked disposition.
- [ ] Every task extracted from them exists as a bounded issue with acceptance criteria.
- [ ] The charter text contains no assignable work.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- North, D. C. (1990). *Institutions, Institutional Change and Economic Performance*. Cambridge University Press.
- Ostrom, E. (2005). *Understanding Institutional Diversity*. Princeton University Press.
- Brooks, F. P. (1995). *The Mythical Man-Month: Essays on Software Engineering* (Anniversary ed.). Addison-Wesley.
- Meadows, D. H. (2008). *Thinking in Systems: A Primer*. Chelsea Green.

## 11. Commit protocol

Commits from this project use the scope `p06`:

```text
docs(p06): ratify the phase-2 charter into the roadmap
docs(p06): decompose new-concepts residue into bounded issues
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

