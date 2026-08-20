# P93 - Payment and settlement infrastructure as skeletal dependence

**Track P - Shadow Finance, Capital Flows and Currency**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Market structure researcher |
| **Upstream** | `SystemKind.skeleton`; CPMI-IOSCO principles |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The skeleton is described as market infrastructure and carries the highest criticality in the framework. Payment and settlement systems are the clearest real instance of that, and they have a published international standard describing exactly what makes them resilient. The framework has never been checked against it, so the highest-criticality system in the model is the least externally validated.

## 2. Purpose

Check the skeleton's representation against the published principles for financial market infrastructures, and correct the model where the standard identifies structure the framework omits.

## 3. Scope

**In scope**

- A mapping from the published principles to the framework's skeleton representation.
- Identification of resilience structure the standard requires and the framework cannot express.
- Correction or documented omission per gap.

**Out of scope**

- Assessing any real infrastructure's compliance.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Work from the standard itself, principle by principle, rather than from a summary.
2. Map each principle to the framework: several concern governance and risk management, which map to the nervous and immune systems, not the skeleton - and that split is itself a finding about whether the anatomy divides infrastructure correctly.
3. Identify what the framework cannot express. Settlement finality, default waterfalls and recovery plans are structural, precise and absent from the model.
4. For each gap, rule: extend the model, or record the omission where the skeleton's criticality is set.
5. Note the criticality question directly - if the skeleton is the highest-criticality system and its representation is the least detailed, the weighting and the detail are inconsistent.
6. Coordinate with P27 and P30, which own criticality's role in scoring.

## 5. Task board

- [ ] Map the principles to the framework principle by principle.
- [ ] Identify inexpressible resilience structure.
- [ ] Rule extend-or-omit per gap.
- [ ] Address the criticality-versus-detail inconsistency.
- [ ] Coordinate with P27 and P30.
- [ ] Publish `docs/taxonomies/market_infrastructure.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Work from the published standard, principle by principle.
- **Inputs:** The standard text.
- **Output artifact:** A principle inventory.
- **Stop condition:** Every principle is recorded from the source.

### `taxonomy-cartographer`

- **Mandate:** Map each principle onto the seven systems and mark the inexpressible ones.
- **Inputs:** The inventory.
- **Output artifact:** A mapping table with gaps.
- **Stop condition:** Every principle is mapped or marked inexpressible.

### `spec-drafter`

- **Mandate:** Rule extend-or-omit per gap and address the criticality inconsistency.
- **Inputs:** The mapping.
- **Output artifact:** `docs/taxonomies/market_infrastructure.md`.
- **Stop condition:** The criticality-versus-detail question is answered, not deferred.

### `boundary-sentinel`

- **Mandate:** Ensure proposed extensions stay structural.
- **Inputs:** The proposals.
- **Output artifact:** A boundary report.
- **Stop condition:** No extension requires market or exposure data.

**Hand-off order:** `literature-scout` -> `taxonomy-cartographer` -> `spec-drafter` -> `boundary-sentinel`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-taxonomy-builder` | The principles are mapped | Builds the mapping with per-principle citations. |
| `amf-boundary-check` | An extension is proposed | Runs the non-trading naming guard. |
| `amf-regime-profile` | Infrastructure oversight is cited | Records the supervisory instrument and its scope. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/taxonomies/market_infrastructure.md`
- A principle-by-principle mapping
- A gap list with rulings
- An answer on criticality versus detail

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every principle is mapped or marked inexpressible.
- [ ] Every gap has an extend-or-omit ruling.
- [ ] The criticality-versus-detail inconsistency is answered.
- [ ] No proposed extension requires market or exposure data.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- CPMI-IOSCO (2012). *Principles for Financial Market Infrastructures*. Bank for International Settlements & IOSCO.
- Committee on Payment and Settlement Systems (2003). *The Role of Central Bank Money in Payment Systems*. Bank for International Settlements.
- Duffie, D. (2011). *How Big Banks Fail and What to Do about It*. Princeton University Press.
- Basel Committee on Banking Supervision (2021). *Principles for Operational Resilience*. Bank for International Settlements.
- Kitano, H. (2004). "Biological robustness." *Nature Reviews Genetics* 5, 826-837.
- Perrow, C. (1984). *Normal Accidents: Living with High-Risk Technologies*. Princeton University Press.
- Csete, M. E., & Doyle, J. C. (2002). "Reverse Engineering of Biological Complexity." *Science* 295(5560), 1664-1669.

## 11. Commit protocol

Commits from this project use the scope `p93`:

```text
docs(p93): map the financial market infrastructure principles onto the skeleton
docs(p93): rule extend-or-omit on the inexpressible resilience structure
docs(p93): resolve the criticality-versus-detail inconsistency
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
