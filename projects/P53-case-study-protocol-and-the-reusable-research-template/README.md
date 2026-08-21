# P53 - Case study protocol and the reusable research template

**Track I - Empirical Case Studies & Forensic Structure**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Research lead |
| **Upstream** | issues #131 (5.1), #132 (5.2) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Case studies are proposed for several episodes, but no protocol exists for what a case study must contain, what counts as an admissible source, or how a structural reading is separated from a narrative one. Without a protocol the case files will be essays, and essays cannot be compared.

## 2. Purpose

Write the protocol and template that every AMF case study follows, so that case files are comparable, auditable, and free of the market-data quantities the framework forbids.

## 3. Scope

**In scope**

- A case study protocol: admissible sources, required sections, and the structural-reading rule.
- A reusable template file that new case studies copy.
- A worked pilot proving the template survives contact with a real episode.

**Out of scope**

- Conducting the substantive case studies - those are P54 to P57.
- Any narrative that attributes motive to named individuals.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Define admissible sources by rank: official filings and regulatory findings first, peer-reviewed analysis second, contemporaneous reporting third and only for dating.
2. Require every factual claim in a case file to carry a source and a date.
3. Define the structural-reading rule: a case study records which AMF systems and dependency edges were involved, never what the price did.
4. Require an explicit uncertainty section: what the sources disagree about, and what is unknown.
5. Forbid characterisation of named individuals; a case study describes structure, not conduct.
6. Pilot the template on one small, well-documented episode before declaring it ready.

## 5. Task board

- [ ] Write the source admissibility ranking.
- [ ] Write the required section list.
- [ ] Write the structural-reading rule.
- [ ] Create `docs/case_studies/_template.md`.
- [ ] Run the pilot case and revise the template.
- [ ] Publish `docs/case_studies/protocol.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** Write the protocol including source ranking and the structural-reading rule.
- **Inputs:** The reading list and the non-trading rule.
- **Output artifact:** `docs/case_studies/protocol.md`.
- **Stop condition:** Every required section has a stated purpose and a failure mode it prevents.

### `case-study-archivist`

- **Mandate:** Run the pilot case and report where the template failed.
- **Inputs:** The template and one documented episode.
- **Output artifact:** A pilot case file plus a template revision list.
- **Stop condition:** The pilot completes without needing a section the template does not have.

### `boundary-sentinel`

- **Mandate:** Verify the template cannot be filled in with market-data quantities.
- **Inputs:** The template.
- **Output artifact:** A boundary report.
- **Stop condition:** No template field invites a price, volume or return.

### `red-team-critic`

- **Mandate:** Attempt to write a defamatory or motive-attributing case file within the template.
- **Inputs:** The template.
- **Output artifact:** A misuse report.
- **Stop condition:** The template's rules block the attempt, or they are strengthened.

**Hand-off order:** `spec-drafter` -> `case-study-archivist` -> `boundary-sentinel` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-case-dossier` | Any case study is written | Applies the protocol: source ranking, dating, structural reading and the uncertainty section. |
| `amf-source-vetting` | A case source is proposed | Ranks it and rejects sources below the admissible threshold. |
| `amf-boundary-check` | A case field is defined | Rejects fields that invite market-data quantities. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/case_studies/protocol.md`
- `docs/case_studies/_template.md`
- A pilot case file
- A template revision record

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Source admissibility is ranked and enforced by the template.
- [ ] The structural-reading rule forbids market-data quantities explicitly.
- [ ] Every case file requires an uncertainty section.
- [ ] The pilot completed without inventing a new section.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.
- Morgan, M. G., & Henrion, M. (1990). *Uncertainty: A Guide to Dealing with Uncertainty in Quantitative Risk and Policy Analysis*. Cambridge University Press.
- Sandve, G. K., Nekrutenko, A., Taylor, J., & Hovig, E. (2013). "Ten Simple Rules for Reproducible Computational Research." *PLoS Computational Biology* 9(10), e1003285.
- Wilson, G., Bryan, J., Cranston, K., Kitzes, J., Nederbragt, L., & Teal, T. K. (2017). "Good enough practices in scientific computing." *PLoS Computational Biology* 13(6), e1005510.
- Grimm, V., et al. (2020). "The ODD Protocol for Describing Agent-Based and Other Simulation Models: A Second Update." *Journal of Artificial Societies and Social Simulation* 23(2), 7.
- Manski, C. F. (2013). *Public Policy in an Uncertain World: Analysis and Decisions*. Harvard University Press.
- Bowker, G. C., & Star, S. L. (1999). *Sorting Things Out: Classification and Its Consequences*. MIT Press.

## 11. Commit protocol

Commits from this project use the scope `p53`:

```text
docs(p53): write the case study protocol and source admissibility ranking
docs(p53): add the reusable case study template
docs(p53): revise the template from the pilot case findings
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
