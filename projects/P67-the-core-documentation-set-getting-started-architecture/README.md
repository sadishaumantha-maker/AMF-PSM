# P67 - The core documentation set: getting started, architecture and examples

**Track K - Communication, Visualisation & Documentation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Documentation owner |
| **Upstream** | issues #140 (6.4), #141 (6.5), #142 (6.6), #154 (9.7) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Three documentation pages are requested. The dispute is what a contributor actually needs first: the `CLAUDE.md` file is already a detailed contributor guide, so a getting-started page that repeats it adds maintenance burden without adding information. The pages must be scoped to what is genuinely missing.

## 2. Purpose

Write the three pages so that each has a distinct audience and contains nothing already stated elsewhere, and establish a rule against duplication that keeps them maintainable.

## 3. Scope

**In scope**

- `docs/getting_started.md` for a new contributor's first hour.
- `docs/architecture.md` for the module structure and data flow.
- `docs/examples.md` for workflows and use cases.
- A non-duplication rule and a check for it.

**Out of scope**

- Restating `CLAUDE.md` content.
- Any link that the markdown link check cannot resolve.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Define the audience for each page in one sentence before writing anything.
2. Audit `CLAUDE.md` and `README.md` for what is already covered, and write only what is missing.
3. For architecture, show the one-way dependency order as a diagram, since prose is a poor medium for a layering constraint.
4. For examples, cover the runnable scripts in `examples/` and state which are exercised by the integration tests.
5. Establish the non-duplication rule: a fact lives in exactly one place and other pages link to it.
6. Verify every relative link resolves, since the CI link check will fail the build otherwise.

## 5. Task board

- [ ] Write the one-sentence audience definition per page.
- [ ] Audit existing documentation for coverage.
- [ ] Write `docs/getting_started.md`.
- [ ] Write `docs/architecture.md` with a layering diagram.
- [ ] Write `docs/examples.md` covering the runnable scripts.
- [ ] Establish and check the non-duplication rule.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `docs-synthesizer`

- **Mandate:** Write the three pages to their stated audiences with no duplication.
- **Inputs:** `CLAUDE.md`, `README.md`, `src/amf/`, `examples/`.
- **Output artifact:** Three pages under `docs/`.
- **Stop condition:** No fact appears in two pages.

### `api-surface-reviewer`

- **Mandate:** Verify the architecture page matches the actual module dependency order.
- **Inputs:** `src/amf/` and the draft.
- **Output artifact:** An accuracy report.
- **Stop condition:** The documented layering matches the imports exactly.

### `red-team-critic`

- **Mandate:** Follow the getting-started page literally as a new contributor and record where it fails.
- **Inputs:** The draft page.
- **Output artifact:** A first-hour walkthrough report.
- **Stop condition:** The walkthrough completes without needing information from outside the page.

**Hand-off order:** `docs-synthesizer` -> `api-surface-reviewer` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-doc-page` | Any documentation page is written | Enforces conventions, relative-link resolution and the disclaimer rules. |
| `amf-layering-check` | The architecture page is written | Verifies the documented dependency order against the actual imports. |
| `amf-red-team` | A walkthrough is published | Follows it literally and reports every gap. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/getting_started.md`
- `docs/architecture.md`
- `docs/examples.md`
- A non-duplication rule

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Each page states its audience and contains nothing already in `CLAUDE.md` or `README.md`.
- [ ] The architecture page's layering matches the actual imports.
- [ ] The getting-started walkthrough completes without external information.
- [ ] Every relative link resolves and the CI link check passes.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Martin, R. C. (2017). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.
- Parnas, D. L. (1972). "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM* 15(12), 1053-1058.
- Evans, E. (2003). *Domain-Driven Design: Tackling Complexity in the Heart of Software*. Addison-Wesley.
- Hunt, A., & Thomas, D. (2019). *The Pragmatic Programmer* (20th Anniversary ed.). Addison-Wesley.
- Wilson, G., Bryan, J., Cranston, K., Kitzes, J., Nederbragt, L., & Teal, T. K. (2017). "Good enough practices in scientific computing." *PLoS Computational Biology* 13(6), e1005510.
- Brooks, F. P. (1995). *The Mythical Man-Month: Essays on Software Engineering* (Anniversary ed.). Addison-Wesley.

## 11. Commit protocol

Commits from this project use the scope `p67`:

```text
docs(p67): add getting-started page scoped to a contributor's first hour
docs(p67): add architecture page with the one-way dependency diagram
docs(p67): add examples page covering the runnable scripts
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
