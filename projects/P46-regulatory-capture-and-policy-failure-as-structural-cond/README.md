# P46 - Regulatory capture and policy failure as structural conditions

**Track G - Policy Architecture & Regulatory Regimes**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Policy researcher |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 4.3 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Regulatory capture is proposed as a research topic, but capture is an accusation as often as it is a finding. The framework needs a definition that can be evaluated from structure - who depends on whom, and who can veto - rather than from imputed motive, or the topic will produce polemic instead of analysis.

## 2. Purpose

Define capture structurally in AMF terms, distinguish it from the ordinary and legitimate dependence of regulators on regulated-entity information, and identify which structural conditions the framework can actually detect.

## 3. Scope

**In scope**

- A structural definition of capture: dependency asymmetry between the regulatory tier and the entities it binds.
- A distinction between informational dependence and capture.
- An assessment of which conditions AMF can represent and which it cannot.

**Out of scope**

- Naming any real regulator or firm as captured.
- Any claim about individual motive or corruption.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Start from the economic theory of regulation and the later corrective literature; both are needed, because the strong capture thesis has been substantially qualified.
2. Define capture structurally: the regulated systems supply the information, expertise and personnel on which the regulatory system depends, producing a dependency edge that runs the wrong way relative to authority.
3. Distinguish this sharply from ordinary informational dependence, which is universal and not itself capture.
4. Identify which structural conditions the AMF graph could represent - reversed dependency edges, low regulator redundancy, articulation-point regulators.
5. State clearly that a structural condition is a susceptibility, not a finding about any real body.
6. Write the whole document with no named accusations.

## 5. Task board

- [ ] Summarise the capture literature including its qualifications.
- [ ] Write the structural definition.
- [ ] Distinguish informational dependence from capture.
- [ ] Assess AMF representability of each condition.
- [ ] Write the susceptibility-not-finding rule.
- [ ] Publish `docs/policy/capture.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Collect both the original capture thesis and its later qualifications from primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary presenting both.
- **Stop condition:** The qualifications are given equal weight to the original thesis.

### `spec-drafter`

- **Mandate:** Write the structural definition and the susceptibility rule.
- **Inputs:** The literature summary and the AMF graph model.
- **Output artifact:** `docs/policy/capture.md`.
- **Stop condition:** The definition can be evaluated from structure alone, with no reference to motive.

### `red-team-critic`

- **Mandate:** Check that no sentence names or implicates a real body.
- **Inputs:** The draft.
- **Output artifact:** A defamation-risk critique.
- **Stop condition:** No real regulator or firm is characterised.

### `boundary-sentinel`

- **Mandate:** Verify no proposed measure requires market or entity-level data.
- **Inputs:** Proposed measures.
- **Output artifact:** A boundary report.
- **Stop condition:** All measures are structural and dimensionless.

**Hand-off order:** `literature-scout` -> `spec-drafter` -> `red-team-critic` -> `boundary-sentinel`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-red-team` | Capture conditions are written up | Scans for imputed motive and named accusation. |
| `amf-source-vetting` | A capture claim is cited | Requires peer-reviewed or official-sector sourcing. |
| `amf-boundary-check` | A structural condition is proposed | Confirms it needs no market or entity data. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/policy/capture.md`
- A structural definition
- A representability assessment
- A susceptibility-not-finding rule

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Capture is defined so it can be evaluated from structure without reference to motive.
- [ ] Informational dependence and capture are clearly distinguished.
- [ ] No real regulator or firm is named or characterised.
- [ ] The qualifying literature is presented alongside the original thesis.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Stigler, G. J. (1971). "The Theory of Economic Regulation." *Bell Journal of Economics and Management Science* 2(1), 3-21.
- Peltzman, S. (1976). "Toward a More General Theory of Regulation." *Journal of Law and Economics* 19(2), 211-240.
- Carpenter, D., & Moss, D. A. (eds.) (2014). *Preventing Regulatory Capture: Special Interest Influence and How to Limit It*. Cambridge University Press.
- Kydland, F. E., & Prescott, E. C. (1977). "Rules Rather than Discretion: The Inconsistency of Optimal Plans." *Journal of Political Economy* 85(3), 473-491.
- Alesina, A., & Summers, L. H. (1993). "Central Bank Independence and Macroeconomic Performance." *Journal of Money, Credit and Banking* 25(2), 151-162.
- North, D. C. (1990). *Institutions, Institutional Change and Economic Performance*. Cambridge University Press.
- Ostrom, E. (2005). *Understanding Institutional Diversity*. Princeton University Press.

## 11. Commit protocol

Commits from this project use the scope `p46`:

```text
docs(p46): define regulatory capture as a structural condition
docs(p46): distinguish informational dependence from capture
docs(p46): assess which capture conditions AMF can represent
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
