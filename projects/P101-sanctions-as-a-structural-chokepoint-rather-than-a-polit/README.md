# P101 - Sanctions as a structural chokepoint rather than a political act

**Track R - Geopolitics, Sanctions and Fragmentation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Comparative regulation researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 7.1 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Discussion 7.1 calls sanctions a financial weapon. That framing invites the framework into political judgement, which it must decline. The structural content underneath it is different and legitimate: sanctions work because certain nodes in the financial system are unavoidable, and unavoidability is a graph property. The dispute is whether the framework can express chokepoint structure without taking a position on its use.

## 2. Purpose

Express chokepoint structure - the concentration of a required function in nodes a participant cannot route around - and hold the treatment strictly to structure, never to policy.

## 3. Scope

**In scope**

- A structural definition of a chokepoint distinct from the framework's articulation point.
- An assessment of whether the seven-system model can represent unavoidability.
- A strict neutrality rule for the whole track.

**Out of scope**

- Any statement about whether a sanction is justified, effective or lawful.
- Naming any sanctioned party, jurisdiction or programme as an example.
- Any transaction or flow data.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Define first and distinguish: an articulation point disconnects a graph when removed; a chokepoint is a node whose function has no substitute for a particular participant. The second is relational and the first is not, and the framework only has the first.
2. Read the weaponised-interdependence literature for the structural mechanism, not the policy argument - the useful content is that network asymmetry creates leverage, which is a claim about topology.
3. Assess representability. The framework's graph is per-market with no participant-level detail, so a participant-relative property may be unrepresentable, and if so that is the finding.
4. Write the neutrality rule for the whole of Track R before writing any content: describe structure, never endorse, condemn or predict use.
5. Use no real programme as an illustration. Constructed examples carry the structural point without the political freight.
6. Have the red-team critic read for political content before merge, and treat any hit as blocking.

## 5. Task board

- [ ] Define chokepoint against articulation point formally.
- [ ] Extract the structural mechanism from the literature.
- [ ] Assess representability in a per-market model.
- [ ] Write the Track R neutrality rule.
- [ ] Build constructed rather than real examples.
- [ ] Publish `docs/policy/chokepoint_structure.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `math-formalizer`

- **Mandate:** Define the chokepoint formally and distinguish it from an articulation point.
- **Inputs:** `graph.py`, the literature.
- **Output artifact:** A formal definition with the distinction stated.
- **Stop condition:** The relational character of a chokepoint is expressed, not glossed.

### `literature-scout`

- **Mandate:** Extract the topological mechanism and leave the policy argument aside.
- **Inputs:** The reading list.
- **Output artifact:** An annotated mechanism summary.
- **Stop condition:** The summary contains no evaluative claim about sanctions.

### `spec-drafter`

- **Mandate:** Write the neutrality rule and the representability verdict.
- **Inputs:** The definition and summary.
- **Output artifact:** `docs/policy/chokepoint_structure.md`.
- **Stop condition:** The neutrality rule binds the whole track and is stated first.

### `red-team-critic`

- **Mandate:** Read for any political content and treat a hit as blocking.
- **Inputs:** The draft.
- **Output artifact:** A political-content report.
- **Stop condition:** No sentence endorses, condemns or predicts the use of any measure.

**Hand-off order:** `math-formalizer` -> `literature-scout` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-graph-algorithm` | A cut or chokepoint notion is defined | Verifies it against its source and states complexity. |
| `amf-red-team` | Any Track R document is drafted | Scans for political content and named parties. |
| `amf-doc-page` | The document is published | Enforces documentation conventions and neutrality. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/chokepoint_structure.md`
- A formal chokepoint definition
- A representability verdict
- The Track R neutrality rule

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Chokepoint and articulation point are formally distinguished.
- [ ] The representability verdict follows from the model's per-market scope.
- [ ] No real sanctions programme or party is named.
- [ ] No sentence endorses, condemns or predicts use.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Farrell, H., & Newman, A. L. (2019). "Weaponized Interdependence: How Global Economic Networks Shape State Coercion." *International Security* 44(1), 42-79.
- Hirschman, A. O. (1945). *National Power and the Structure of Foreign Trade*. University of California Press.
- Hufbauer, G. C., Schott, J. J., Elliott, K. A., & Oegg, B. (2007). *Economic Sanctions Reconsidered* (3rd ed.). Peterson Institute for International Economics.
- Drezner, D. W. (1999). *The Sanctions Paradox: Economic Statecraft and International Relations*. Cambridge University Press.
- McDowell, D. (2023). *Bucking the Buck: US Financial Sanctions and the International Backlash against the Dollar*. Oxford University Press.
- Freeman, L. C. (1977). "A Set of Measures of Centrality Based on Betweenness." *Sociometry* 40(1), 35-41.
- Albert, R., Jeong, H., & Barabasi, A.-L. (2000). "Error and attack tolerance of complex networks." *Nature* 406, 378-382.
- Newman, M. E. J. (2018). *Networks* (2nd ed.). Oxford University Press.

## 11. Commit protocol

Commits from this project use the scope `p101`:

```text
docs(p101): define chokepoint structure and distinguish it from articulation
docs(p101): adopt the track-wide neutrality rule for geopolitical structure
docs(p101): rule on representing participant-relative unavoidability
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

