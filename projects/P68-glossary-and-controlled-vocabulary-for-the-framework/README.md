# P68 - Glossary and controlled vocabulary for the framework

**Track K - Communication, Visualisation & Documentation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Documentation owner |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Theme A; the non-trading naming rule |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The repository uses a deliberately anatomical vocabulary to avoid market-data terms, and the naming guard enforces that mechanically. But the anatomical terms themselves - skeleton, circulatory, immune - are metaphors whose intended referents are recorded only in `cli.py` constants and scattered docstrings. Two contributors can use the same word for different things.

## 2. Purpose

Build a controlled vocabulary: one definition per term, one term per concept, with the forbidden synonyms listed so contributors know what not to write.

## 3. Scope

**In scope**

- A glossary of every domain term with a single authoritative definition.
- A forbidden-synonym list mapping market-data terms to their structural replacements.
- A check that the glossary and the naming guard agree.

**Out of scope**

- Reading the protected framework document to source definitions - forbidden; use the paraphrased constants.
- Adding terms to the naming guard allowlist.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Source definitions from the paraphrased constants in `cli.py` and the module docstrings, never from the protected document.
2. Apply controlled-vocabulary practice: one preferred term per concept, with non-preferred terms mapped to it.
3. Build the forbidden-synonym mapping directly from the naming guard's substring list, so a contributor reaching for a market-data word finds the structural replacement immediately.
4. Cross-check that every term used in the public API appears in the glossary.
5. Add a check that a term added to the glossary does not collide with the forbidden list.
6. Link the glossary from the contributor documentation so it is found before a name is chosen, not after.

## 5. Task board

- [ ] Extract candidate terms from the public API and docstrings.
- [ ] Write one authoritative definition per term.
- [ ] Build the forbidden-synonym mapping from the naming guard.
- [ ] Cross-check public API coverage.
- [ ] Add the collision check.
- [ ] Publish `docs/glossary.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `taxonomy-cartographer`

- **Mandate:** Extract terms and build the controlled vocabulary with preferred and non-preferred forms.
- **Inputs:** `src/amf/` docstrings and `cli.py` constants.
- **Output artifact:** `docs/glossary.md`.
- **Stop condition:** Every public API term has exactly one definition.

### `boundary-sentinel`

- **Mandate:** Build the forbidden-synonym mapping from the naming guard's substring list.
- **Inputs:** `tests/unit/test_non_trading_boundary.py`.
- **Output artifact:** A synonym mapping table.
- **Stop condition:** Every forbidden substring has a structural replacement suggested.

### `integrity-warden`

- **Mandate:** Confirm no definition was sourced from a protected artifact.
- **Inputs:** The glossary and `SHA256SUMS`.
- **Output artifact:** A provenance attestation.
- **Stop condition:** Every definition traces to a paraphrased constant or a docstring.

**Hand-off order:** `taxonomy-cartographer` -> `boundary-sentinel` -> `integrity-warden`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-boundary-check` | A term is added to the glossary | Checks it against the forbidden substring list and suggests a structural alternative. |
| `amf-taxonomy-builder` | The vocabulary is assembled | Builds it with preferred and non-preferred term mapping. |
| `amf-integrity-verify` | Definitions are sourced | Confirms no protected artifact was read to produce output. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/glossary.md`
- A forbidden-synonym mapping
- A collision check
- A provenance attestation

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every public API term has exactly one authoritative definition.
- [ ] Every forbidden substring maps to a suggested structural replacement.
- [ ] No definition was sourced from a checksum-protected artifact.
- [ ] The glossary is linked from the contributor documentation.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Gruber, T. R. (1993). "A translation approach to portable ontology specifications." *Knowledge Acquisition* 5(2), 199-220.
- Bowker, G. C., & Star, S. L. (1999). *Sorting Things Out: Classification and Its Consequences*. MIT Press.
- Rosch, E. (1978). "Principles of Categorization." In Rosch, E. & Lloyd, B. B. (eds.), *Cognition and Categorization*. Lawrence Erlbaum.
- ISO (2022). *ISO 20022: Financial services - Universal financial industry message scheme*.
- EDM Council / Object Management Group. *Financial Industry Business Ontology (FIBO)*.
- Parnas, D. L. (1972). "On the Criteria To Be Used in Decomposing Systems into Modules." *Communications of the ACM* 15(12), 1053-1058.

## 11. Commit protocol

Commits from this project use the scope `p68`:

```text
docs(p68): publish the controlled vocabulary for framework terms
docs(p68): map forbidden market-data terms to structural replacements
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

