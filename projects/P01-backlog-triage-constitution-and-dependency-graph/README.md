# P01 - Backlog triage constitution and dependency graph

**Track A - Governance, Ownership & Delivery Cadence**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Maintainer / release manager |
| **Upstream** | issues #111 (1.5), #106 (0.8), #104 (0.6), #147 (9.1) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The backlog is disputed at the level of *meaning*, not priority: nobody agrees whether an item such as #23 ("Creating whole new concepts for PSM") is a research question, an epic, or a duplicate of #21. Until a written triage constitution exists, every prioritisation argument re-opens from zero, and `0% triaged` (metric 9.1) cannot move because there is no agreed definition of "triaged".

## 2. Purpose

Produce a binding, written triage constitution - the admissible issue types, the labels that carry decision weight, the definition of done for triage, and a rendered dependency graph of every open item. The output is procedural, not analytical: it is the rule set that every later project in this catalogue is triaged under.

## 3. Scope

**In scope**

- A taxonomy of issue types (research question, specification, implementation, validation, governance).
- Label semantics: which labels are decision-bearing and which are descriptive only.
- A machine-checkable definition of "triaged" (type + priority + milestone + owner + acceptance criteria).
- A dependency graph of all open issues rendered as Mermaid in `docs/backlog_graph.md`.
- A de-duplication ruling for every pair flagged as overlapping.

**Out of scope**

- Changing any code under `src/amf/`.
- Deciding the technical content of any research dispute - that belongs to Tracks D-L.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Read `docs/ANALYSIS_AND_ROADMAP.md` end to end and extract every issue reference into a table.
2. Classify each issue against the type taxonomy; where the issue text does not determine the type, record the ambiguity rather than guessing.
3. Apply Ostrom's design principles for rule systems (clear boundaries, congruence, graduated sanctions) to the label set: every label must have a stated consequence or be deleted.
4. Build the dependency graph as a directed acyclic graph. If a cycle appears, that is a finding - record it and propose the edge to cut.
5. Write the constitution to `docs/governance/triage_constitution.md` with a version number.
6. Re-triage all open issues under the new rules in a single working session and record the diff.
7. Open a follow-up issue for every ambiguity that survived step 2.

## 5. Task board

- [ ] Extract the full issue inventory into a table (number, title, current labels, referenced-by).
- [ ] Draft the issue-type taxonomy with one worked example per type.
- [ ] Audit the existing label set; propose deletions with justification.
- [ ] Write the machine-checkable "triaged" predicate.
- [ ] Render the dependency DAG in Mermaid and verify acyclicity.
- [ ] Rule on every duplicate pair, including #21 vs #23.
- [ ] Publish `docs/governance/triage_constitution.md`.
- [ ] Run the re-triage session and record before/after counts for metric 9.1.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Collect the institutional-design literature that governs rule systems and issue taxonomies; reject management blogs.
- **Inputs:** The reading list in section 10.
- **Output artifact:** `docs/governance/_research/triage_sources.md` - annotated, one paragraph per source.
- **Stop condition:** Every rule proposed in the constitution has at least one cited source, or is explicitly marked `convention (uncited)`.

### `spec-drafter`

- **Mandate:** Turn the sourced findings into the triage constitution text, including the triaged predicate.
- **Inputs:** Scout output plus the issue inventory.
- **Output artifact:** `docs/governance/triage_constitution.md` v1.0.
- **Stop condition:** Every section has a testable statement; no section contains the word "should" without a consequence.

### `taxonomy-cartographer`

- **Mandate:** Render the issue dependency DAG and detect cycles.
- **Inputs:** The issue inventory table.
- **Output artifact:** `docs/backlog_graph.md` with a Mermaid graph.
- **Stop condition:** The graph is acyclic, or every cycle is documented with a proposed cut edge.

### `red-team-critic`

- **Mandate:** Attempt to triage three deliberately awkward issues (#21, #23, #26) under the draft rules and find where the rules fail.
- **Inputs:** The draft constitution.
- **Output artifact:** A falsification report appended to the constitution PR.
- **Stop condition:** Either a rule gap is found and fixed, or the critic certifies all three classify unambiguously.

**Hand-off order:** `literature-scout` -> `spec-drafter` -> `taxonomy-cartographer` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-source-vetting` | Any source is proposed for the constitution | Checks publisher standing, peer review status and citation count; rejects non-scholarly sources. |
| `amf-doc-page` | Writing any file under `docs/` | Applies the repository documentation rules - relative links only, disclaimer present, link-check safe. |
| `amf-red-team` | Before the constitution is merged | Runs an adversarial classification pass to find rules that admit two readings. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/governance/triage_constitution.md` (versioned).
- `docs/backlog_graph.md` with a Mermaid dependency DAG.
- `docs/governance/_research/triage_sources.md`.
- A recorded re-triage diff (before/after label and milestone counts).

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] 100% of open issues satisfy the machine-checkable triaged predicate (metric 9.1).
- [ ] The dependency graph renders and is acyclic, or every cycle carries a documented cut.
- [ ] Every duplicate pair has a written ruling with a linked issue comment.
- [ ] The red-team critic's report is attached and every finding is closed.
- [ ] No file under `src/amf/` changed.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Ostrom, E. (1990). *Governing the Commons: The Evolution of Institutions for Collective Action*. Cambridge University Press.
- Ostrom, E. (2005). *Understanding Institutional Diversity*. Princeton University Press.
- North, D. C. (1990). *Institutions, Institutional Change and Economic Performance*. Cambridge University Press.
- Bowker, G. C., & Star, S. L. (1999). *Sorting Things Out: Classification and Its Consequences*. MIT Press.
- Conway, M. E. (1968). "How Do Committees Invent?" *Datamation* 14(5), 28-31.
- Brooks, F. P. (1995). *The Mythical Man-Month: Essays on Software Engineering* (Anniversary ed.). Addison-Wesley.
- Forsgren, N., Humble, J., & Kim, G. (2018). *Accelerate: The Science of Lean Software and DevOps*. IT Revolution.

## 11. Commit protocol

Commits from this project use the scope `p01`:

```text
docs(p01): add issue inventory and dependency DAG
docs(p01): draft triage constitution v1.0 with sourced rule set
docs(p01): rule on duplicate issue pairs (#21/#23, #25/#43)
docs(p01): record re-triage diff for metric 9.1
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

