# P09 - Dependency update policy and supply-chain review gates

**Track B - Engineering Quality, CI & Reproducibility**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 days |
| **Lead role** | CI owner |
| **Upstream** | issue #118 (2.6) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Auto-merging patch updates is argued to reduce toil and argued to be exactly the vector a supply-chain attack needs. The package has zero runtime dependencies, so the entire exposure is the development and CI toolchain - which is precisely what signs and verifies the integrity chain.

## 2. Purpose

Set a dependency policy proportional to blast radius: automation where a compromise cannot reach the integrity chain, human review where it can.

## 3. Scope

**In scope**

- A blast-radius classification of every development dependency and CI action.
- A Dependabot configuration implementing the classification.
- A review checklist for updates that touch the integrity or release path.

**Out of scope**

- Adding any runtime dependency to `amf`.
- Auto-merging anything in the release or integrity path.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. List every dev dependency and CI action and mark whether it can influence `SHA256SUMS` verification or tagging.
2. Classify each as `auto` (patch auto-merge allowed), `review` (human approval), or `pinned` (digest, manual only).
3. Write `.github/dependabot.yml` implementing the classification; keep it `yamllint`-clean.
4. Write the reviewer checklist for `review` and `pinned` classes, drawing on the SSDF and in-toto guidance.
5. Verify the policy by simulating a malicious patch bump on a scratch branch.

## 5. Task board

- [ ] Build the dependency blast-radius table.
- [ ] Write `.github/dependabot.yml`.
- [ ] Write `docs/governance/dependency_policy.md`.
- [ ] Simulate a hostile patch bump and confirm it requires review.
- [ ] Confirm `yamllint .` passes.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `red-team-critic`

- **Mandate:** Model a compromised transitive dev dependency and trace what it can reach.
- **Inputs:** Dependency table, workflow definitions.
- **Output artifact:** A reachability analysis.
- **Stop condition:** Every dependency that can reach the integrity or release path is classified `review` or `pinned`.

### `spec-drafter`

- **Mandate:** Write the dependency policy and reviewer checklist.
- **Inputs:** Reachability analysis.
- **Output artifact:** `docs/governance/dependency_policy.md`.
- **Stop condition:** Every dependency class has a stated approval rule.

**Hand-off order:** `red-team-critic` -> `spec-drafter`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-integrity-verify` | Any toolchain update lands | Re-verifies the protected artifacts after the update. |
| `amf-red-team` | Classifying a dependency | Traces what a compromised version could modify. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `.github/dependabot.yml`
- `docs/governance/dependency_policy.md`
- A reachability analysis

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every dev dependency and CI action has a written class.
- [ ] Nothing in the integrity or release path is eligible for auto-merge.
- [ ] `yamllint .` passes.
- [ ] `amf` still has zero runtime dependencies.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- NIST (2022). *SP 800-218: Secure Software Development Framework (SSDF) Version 1.1*.
- Torres-Arias, S., Afzali, H., Kuppusamy, T. K., Curtmola, R., & Cappos, J. (2019). "in-toto: Providing farm-to-table guarantees for bits and bytes." *USENIX Security Symposium*.
- Anderson, R. (2020). *Security Engineering: A Guide to Building Dependable Distributed Systems* (3rd ed.). Wiley.
- Humble, J., & Farley, D. (2010). *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Addison-Wesley.

## 11. Commit protocol

Commits from this project use the scope `p09`:

```text
ci(p09): add dependabot configuration keyed to dependency blast radius
docs(p09): publish the dependency update policy and reviewer checklist
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
