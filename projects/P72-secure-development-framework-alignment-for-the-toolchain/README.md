# P72 - Secure development framework alignment for the toolchain

**Track L - Intellectual Property, Provenance & Security**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Security engineer |
| **Upstream** | `.pre-commit-config.yaml`, CI workflows, `SECURITY.md` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The package has zero runtime dependencies, which is often taken to mean it has no supply-chain exposure. That is wrong: the development and CI toolchain is what produces the checksums, runs the integrity verification and creates the tags. The exposure has simply moved from runtime to build time, where it is less visible and no less consequential.

## 2. Purpose

Align the development and CI toolchain with an established secure development framework, focusing on the build-time exposure that the zero-dependency runtime does not eliminate.

## 3. Scope

**In scope**

- A mapping of the repository's practices onto the framework's practice groups.
- A gap list with a disposition per gap.
- Implementation of the gaps that are cheap and material.

**Out of scope**

- Adding runtime dependencies.
- Adopting practices whose cost exceeds the exposure they address - but the reasoning must be recorded.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Map current practice onto the framework's practice groups: prepare the organisation, protect the software, produce well-secured software, and respond to vulnerabilities.
2. Assess each practice as met, partially met or not met, with evidence from the repository rather than intent.
3. Prioritise gaps by build-time exposure: anything that can influence the integrity chain or the tag comes first.
4. Implement the cheap and material gaps; for the rest, record the disposition and the reasoning.
5. Check `SECURITY.md` against the framework's vulnerability-response practices and update it if it falls short.
6. Keep every change `yamllint`-clean and confirm CI stays green.

## 5. Task board

- [ ] Map current practice onto the framework's practice groups.
- [ ] Assess each practice with repository evidence.
- [ ] Prioritise gaps by build-time exposure.
- [ ] Implement the cheap and material gaps.
- [ ] Update `SECURITY.md` if response practices fall short.
- [ ] Publish `docs/integrity/ssdf_alignment.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Extract the framework's practice groups from the official publication.
- **Inputs:** The published framework document.
- **Output artifact:** A practice group summary.
- **Stop condition:** Practices are quoted from the official publication.

### `integrity-warden`

- **Mandate:** Assess each practice against repository evidence, not intent.
- **Inputs:** The repository configuration and workflows.
- **Output artifact:** An assessment table with evidence per row.
- **Stop condition:** Every assessment cites a file or a workflow step.

### `red-team-critic`

- **Mandate:** Model a build-time compromise and check which practices would have caught it.
- **Inputs:** The assessment.
- **Output artifact:** A compromise walkthrough.
- **Stop condition:** Every step of the walkthrough is either caught or listed as a gap.

### `spec-drafter`

- **Mandate:** Record the disposition and reasoning for every unimplemented gap.
- **Inputs:** The gap list.
- **Output artifact:** `docs/integrity/ssdf_alignment.md`.
- **Stop condition:** No gap is left without a disposition.

**Hand-off order:** `literature-scout` -> `integrity-warden` -> `red-team-critic` -> `spec-drafter`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-integrity-verify` | A toolchain practice is changed | Re-verifies the protected artifacts after the change. |
| `amf-red-team` | A practice is assessed as met | Models a compromise and checks the practice actually catches it. |
| `amf-doc-page` | The alignment is published | Enforces documentation conventions. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/integrity/ssdf_alignment.md`
- An evidence-based practice assessment
- A prioritised gap list with dispositions
- An updated `SECURITY.md` if required

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every practice assessment cites repository evidence, not intent.
- [ ] Gaps are prioritised by build-time exposure to the integrity chain.
- [ ] Every gap has a disposition and reasoning.
- [ ] `yamllint .` passes and CI remains green.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- NIST (2022). *SP 800-218: Secure Software Development Framework (SSDF) Version 1.1*.
- Torres-Arias, S., Afzali, H., Kuppusamy, T. K., Curtmola, R., & Cappos, J. (2019). "in-toto: Providing farm-to-table guarantees for bits and bytes." *USENIX Security Symposium*.
- Anderson, R. (2020). *Security Engineering: A Guide to Building Dependable Distributed Systems* (3rd ed.). Wiley.
- Schneier, B. (2015). *Applied Cryptography* (20th Anniversary ed.). Wiley.
- Humble, J., & Farley, D. (2010). *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Addison-Wesley.
- NIST (2015). *FIPS PUB 180-4: Secure Hash Standard (SHS)*.
- Nygard, M. T. (2018). *Release It! Design and Deploy Production-Ready Software* (2nd ed.). Pragmatic Bookshelf.

## 11. Commit protocol

Commits from this project use the scope `p72`:

```text
docs(p72): assess toolchain practice against the secure development framework
ci(p72): close the cheap and material build-time security gaps
docs(p72): record dispositions for the unimplemented gaps
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

