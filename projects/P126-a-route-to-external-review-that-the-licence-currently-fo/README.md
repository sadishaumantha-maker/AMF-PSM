# P126 - A route to external review that the licence currently forecloses

**Track U - Method, Epistemics and External Validation**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Maintainer |
| **Upstream** | `LICENSE.txt`; `RELEASING.md`; P125 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Independent validation requires people outside the project to examine the work. The package is all-rights-reserved and privately distributed, which is a deliberate protection of the intellectual property and is also, unavoidably, an obstacle to the external scrutiny P125 identifies as the largest gap. The two commitments are in genuine tension and neither has been given up.

## 2. Purpose

Find whether a route to external review exists that does not weaken the licence position, and if none does, state that the framework has chosen protection over validation.

## 3. Scope

**In scope**

- An enumeration of review routes compatible with the current licence.
- An assessment of each against what independence actually requires.
- A recommendation, including the option of accepting the trade-off explicitly.

**Out of scope**

- Changing the licence.
- Publishing the package or the framework document.
- Any route that would make the protected artifacts more retrievable.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Enumerate routes honestly: reviewer agreements under confidentiality, review of the method rather than the artifact, academic collaboration under contract, or publishing a derived description that is not the protected document.
2. Assess each against what independence requires - a reviewer who has no stake, sufficient access to find problems, and freedom to report them. A route failing the third is not review.
3. Note the sharpest constraint: a reviewer bound not to publish adverse findings provides assurance to the project and none to anyone else.
4. Recognise that the repository is already public, so the source is readable; what is protected is the framework document and the licence's use restriction, which may leave more room than assumed.
5. Recommend, and if the recommendation is that no adequate route exists, state the trade-off explicitly - protection has been chosen over validation, and the framework's claims should be read accordingly.
6. Verify any proposal against the integrity and distribution rules before recommending it.

## 5. Task board

- [ ] Enumerate licence-compatible review routes.
- [ ] Assess each against the three independence requirements.
- [ ] Test what the public repository already permits.
- [ ] Recommend, including the accept-the-trade-off option.
- [ ] Verify against integrity and distribution rules.
- [ ] Publish `docs/methods/external_review.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** Enumerate and assess the routes against the independence requirements.
- **Inputs:** `LICENSE.txt`, `RELEASING.md`, P125.
- **Output artifact:** `docs/methods/external_review.md`.
- **Stop condition:** Every route is assessed against all three requirements.

### `integrity-warden`

- **Mandate:** Verify no proposed route weakens the protection of the checksum-protected artifacts or the distribution rule.
- **Inputs:** The proposals.
- **Output artifact:** A compatibility attestation.
- **Stop condition:** Every recommended route is compatible, or is withdrawn.

### `red-team-critic`

- **Mandate:** Argue that no route provides genuine independence and force the recommendation to answer.
- **Inputs:** The assessment.
- **Output artifact:** A dissent section.
- **Stop condition:** The dissent is answered or the trade-off is accepted in writing.

**Hand-off order:** `spec-drafter` -> `integrity-warden` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-integrity-verify` | A route is proposed | Checks it against the protected artifacts and the private-distribution rule. |
| `amf-red-team` | A route is recommended | Tests whether it delivers genuine independence. |
| `amf-doc-page` | The recommendation is published | Enforces documentation conventions. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/methods/external_review.md`
- An enumeration of licence-compatible routes
- A three-requirement assessment
- A recommendation or an accepted trade-off

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every route is assessed against all three independence requirements.
- [ ] No recommended route weakens the licence or the integrity chain.
- [ ] If no adequate route exists, the trade-off is stated explicitly.
- [ ] The framework document is not published under any option.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Nosek, B. A., Ebersole, C. R., DeHaven, A. C., & Mellor, D. T. (2018). "The preregistration revolution." *PNAS* 115(11), 2600-2606.
- Ioannidis, J. P. A. (2005). "Why Most Published Research Findings Are False." *PLoS Medicine* 2(8), e124.
- Stodden, V., McNutt, M., Bailey, D. H., et al. (2016). "Enhancing reproducibility for computational methods." *Science* 354(6317), 1240-1241.
- Peng, R. D. (2011). "Reproducible Research in Computational Science." *Science* 334(6060), 1226-1227.
- Oreskes, N., Shrader-Frechette, K., & Belitz, K. (1994). "Verification, Validation, and Confirmation of Numerical Models in the Earth Sciences." *Science* 263(5147), 641-646.
- Board of Governors of the Federal Reserve System & OCC (2011). *Supervisory Guidance on Model Risk Management* (SR 11-7 / OCC Bulletin 2011-12).
- Wilkinson, M. D., et al. (2016). "The FAIR Guiding Principles for scientific data management and stewardship." *Scientific Data* 3, 160018.
- Popper, K. R. (1959). *The Logic of Scientific Discovery*. Hutchinson.

## 11. Commit protocol

Commits from this project use the scope `p126`:

```text
docs(p126): enumerate external review routes compatible with the licence
docs(p126): assess each route against what independence requires
docs(p126): recommend a route or record the protection-over-validation trade-off
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
