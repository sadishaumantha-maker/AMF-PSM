# P13 - Documentation build evaluation and the decision to add or refuse it

**Track B - Engineering Quality, CI & Reproducibility**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 3 days |
| **Lead role** | Documentation owner |
| **Upstream** | issue #116 (2.4), #154 (9.7) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

A documentation site is proposed. For a proprietary, all-rights-reserved package in a public repository, a generated site is a distribution surface: it publishes API detail more conveniently than the licence intends. The dispute is whether the maintenance and exposure cost is worth the navigation gain.

## 2. Purpose

Reach an evidence-based decision, recorded as an architecture decision record, and implement whichever option wins - including the option of deliberately refusing the site.

## 3. Scope

**In scope**

- A cost/exposure analysis of a generated documentation site under the current licence.
- An evaluation of at least two alternatives, including plain markdown in `docs/`.
- An ADR recording the decision and the conditions under which it should be revisited.

**Out of scope**

- Publishing any package artifact.
- Anything that would make the framework document more retrievable.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State what a documentation site would add that `docs/` markdown does not.
2. State what it exposes: rendered API surface, search indexing, and long-term maintenance load.
3. Check the interaction with `LICENSE.txt` and the private-distribution rule in `RELEASING.md`.
4. Write the ADR with both options fully argued.
5. Implement the winner. If the site is refused, close #116 with the ADR as the disposition.

## 5. Task board

- [ ] Write the gain analysis.
- [ ] Write the exposure analysis.
- [ ] Check licence and distribution interactions.
- [ ] Publish `docs/adr/0001-documentation-site.md`.
- [ ] Implement or refuse, and close #116 with the ADR linked.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** Write both sides of the ADR with equal effort before recommending.
- **Inputs:** Licence, `RELEASING.md`, `docs/`.
- **Output artifact:** `docs/adr/0001-documentation-site.md`.
- **Stop condition:** A reader cannot tell from the analysis sections which option the author prefers.

### `red-team-critic`

- **Mandate:** Argue the losing side as strongly as possible and record what would change the decision.
- **Inputs:** Draft ADR.
- **Output artifact:** A dissent section appended to the ADR.
- **Stop condition:** The ADR names the specific condition that would reverse it.

**Hand-off order:** `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-doc-page` | Writing the ADR | Enforces documentation conventions and link-check safety. |
| `amf-red-team` | Before the ADR is merged | Argues the rejected option and extracts the reversal condition. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/adr/0001-documentation-site.md`
- The implemented decision
- A disposition comment on #116

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Both options are argued to the same depth.
- [ ] The ADR states an explicit reversal condition.
- [ ] The decision is implemented, including the refusal case.
- [ ] Documentation page count is recorded for metric 9.7.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Martin, R. C. (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.
- Hunt, A., & Thomas, D. (2019). *The Pragmatic Programmer* (20th Anniversary ed.). Addison-Wesley.
- Brooks, F. P. (1995). *The Mythical Man-Month: Essays on Software Engineering* (Anniversary ed.). Addison-Wesley.
- Wilson, G., Bryan, J., Cranston, K., Kitzes, J., Nederbragt, L., & Teal, T. K. (2017). "Good enough practices in scientific computing." *PLoS Computational Biology* 13(6), e1005510.

## 11. Commit protocol

Commits from this project use the scope `p13`:

```text
docs(p13): add ADR 0001 evaluating a generated documentation site
docs(p13): implement the documentation decision and close the originating issue
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
