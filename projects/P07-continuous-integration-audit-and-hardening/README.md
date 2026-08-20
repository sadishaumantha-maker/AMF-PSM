# P07 - Continuous integration audit and hardening

**Track B - Engineering Quality, CI & Reproducibility**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 4 days |
| **Lead role** | CI owner |
| **Upstream** | issues #114 (2.2), #152 (9.5) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

`ci.yml` is asserted to run lint, type-check, test and validate on every push and pull request, but no evidence has been produced that each gate actually *fails the build* when violated. A green badge that cannot go red is worse than no badge.

## 2. Purpose

Prove, by deliberate injection, that every declared CI gate blocks. Then harden the pipeline: pinned action digests, least-privilege permissions, and a documented job-to-guarantee mapping.

## 3. Scope

**In scope**

- A negative test per gate: a deliberately broken change that must turn that job red.
- Action pinning by commit digest and minimal `permissions:` blocks.
- A written mapping from each CI job to the property it guarantees.

**Out of scope**

- Adding a publish workflow.
- Weakening the 100% coverage gate for any reason.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Enumerate every guarantee the repository claims (lint, format, types, tests, coverage, YAML, citation, links, integrity).
2. For each, write a one-line deliberate violation on a scratch branch and record which job caught it.
3. Any guarantee that no job catches is a gap - open an issue and close it in this project.
4. Pin every third-party action to a full commit SHA with a version comment.
5. Set `permissions:` to the minimum each job needs.
6. Publish the job-to-guarantee table in `docs/ci.md`.

## 5. Task board

- [ ] Write the guarantee inventory.
- [ ] Run the negative-test matrix and capture evidence per gate.
- [ ] Fix any uncaught guarantee.
- [ ] Pin all actions by digest.
- [ ] Apply least-privilege permissions per job.
- [ ] Publish `docs/ci.md` with the job-to-guarantee mapping.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `red-team-critic`

- **Mandate:** Break each guarantee deliberately and record whether CI notices.
- **Inputs:** The guarantee inventory.
- **Output artifact:** A negative-test evidence table.
- **Stop condition:** Every guarantee is demonstrated to fail the build when violated.

### `integrity-warden`

- **Mandate:** Confirm `integrity.yml` still verifies all four protected artifacts after any workflow edit.
- **Inputs:** `SHA256SUMS`, `integrity.yml`.
- **Output artifact:** An integrity attestation.
- **Stop condition:** `sha256sum --check --strict SHA256SUMS` passes and the workflow runs on the same triggers as before.

### `docs-synthesizer`

- **Mandate:** Publish the CI documentation page.
- **Inputs:** Evidence table.
- **Output artifact:** `docs/ci.md`.
- **Stop condition:** Each job row names the guarantee, the failure mode and the negative test that proved it.

**Hand-off order:** `red-team-critic` -> `integrity-warden` -> `docs-synthesizer`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-coverage-gate` | The test job is modified | Confirms `--cov-fail-under=100` remains active and diagnoses uncovered branches. |
| `amf-integrity-verify` | Any workflow file changes | Re-verifies the checksum-protected artifacts. |
| `amf-red-team` | Auditing a CI gate | Injects a minimal violation and reports whether the gate blocks. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- A negative-test evidence table
- Digest-pinned workflows with least-privilege permissions
- `docs/ci.md`

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every declared guarantee has a recorded negative test that turned CI red.
- [ ] All third-party actions are pinned to a commit SHA.
- [ ] Every job declares an explicit minimal `permissions:` block.
- [ ] `yamllint .` passes.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Humble, J., & Farley, D. (2010). *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Addison-Wesley.
- Forsgren, N., Humble, J., & Kim, G. (2018). *Accelerate: The Science of Lean Software and DevOps*. IT Revolution.
- NIST (2022). *SP 800-218: Secure Software Development Framework (SSDF) Version 1.1*.
- Torres-Arias, S., Afzali, H., Kuppusamy, T. K., Curtmola, R., & Cappos, J. (2019). "in-toto: Providing farm-to-table guarantees for bits and bytes." *USENIX Security Symposium*.
- Beck, K. (2002). *Test-Driven Development: By Example*. Addison-Wesley.
- Wilson, G., Bryan, J., Cranston, K., Kitzes, J., Nederbragt, L., & Teal, T. K. (2017). "Good enough practices in scientific computing." *PLoS Computational Biology* 13(6), e1005510.

## 11. Commit protocol

Commits from this project use the scope `p07`:

```text
ci(p07): pin third-party actions to commit digests
ci(p07): apply least-privilege permissions per job
docs(p07): publish the CI job-to-guarantee mapping with negative-test evidence
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

