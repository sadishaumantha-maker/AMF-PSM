# P02 - Branch protection ruleset design for main, develop and release

**Track A - Governance, Ownership & Delivery Cadence**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 3 days |
| **Lead role** | Repository administrator |
| **Upstream** | issues #107 (1.1), #108 (1.2), #109 (1.3), #153 (9.6) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

`.github/RULESET-POLICY.md` states an intent that no ruleset actually enforces - metric 9.6 records `rulesets active: 0`. The dispute is over strictness: two approvals plus signed commits is argued to be unworkable for a small team, and argued to be the minimum for a repository whose central asset is a timestamped, checksum-protected document.

## 2. Purpose

Design and activate three branch rulesets whose strictness is derived from what each branch protects, not from taste. `main` protects the integrity chain; `release/*` protects the private-distribution guarantee; `develop` protects only build health.

## 3. Scope

**In scope**

- Written threat model per branch: what a bad merge to this branch destroys.
- Ruleset configuration for `main`, `develop` and `release/*`, including required status checks.
- A documented, auditable break-glass procedure.
- Verification evidence that each ruleset is active and blocking.

**Out of scope**

- Any change to the protected artifacts listed in `SHA256SUMS`.
- Adding a publish workflow of any kind.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Write the per-branch threat model before touching any setting; strictness must follow from it.
2. Map each required status check to the CI job that produces it (`lint`, `typecheck`, `test`, `validate`, `integrity`).
3. Configure `main`: two approvals, signed commits, strict status checks, linear history, no force push.
4. Configure `release/*`: two approvals, signed commits, strict checks, plus the `integrity` job as a hard gate.
5. Configure `develop`: one approval, CI required, force push denied.
6. Document a break-glass procedure that leaves an audit record; an undocumented bypass is a security incident.
7. Prove enforcement by attempting a deliberately non-compliant push on a scratch branch and capturing the rejection.

## 5. Task board

- [ ] Write `docs/governance/branch_threat_model.md`.
- [ ] Enumerate required status check names exactly as CI emits them.
- [ ] Activate the `main` ruleset.
- [ ] Activate the `develop` ruleset.
- [ ] Activate the `release/*` ruleset with the integrity gate.
- [ ] Document and test the break-glass path.
- [ ] Capture enforcement evidence (rejected push transcript) in the PR.
- [ ] Update `.github/RULESET-POLICY.md` so the document and the configuration agree.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** Write the per-branch threat model and derive strictness from it.
- **Inputs:** `.github/RULESET-POLICY.md`, `SHA256SUMS`, `RELEASING.md`.
- **Output artifact:** `docs/governance/branch_threat_model.md`.
- **Stop condition:** Each of the three branches has a stated loss scenario and a control that addresses it.

### `integrity-warden`

- **Mandate:** Confirm the release ruleset makes the integrity workflow a hard, non-bypassable gate.
- **Inputs:** `.github/workflows/integrity.yml`, the proposed ruleset.
- **Output artifact:** An enforcement attestation in the PR body.
- **Stop condition:** A simulated tampering push to `release/*` is rejected.

### `red-team-critic`

- **Mandate:** Find every path that reaches `main` without passing the intended gates.
- **Inputs:** Live ruleset configuration.
- **Output artifact:** A bypass-path report.
- **Stop condition:** Every discovered path is either closed or documented as an accepted, logged break-glass route.

**Hand-off order:** `spec-drafter` -> `integrity-warden` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-integrity-verify` | Any ruleset touching `release/*` or `main` is changed | Re-runs `sha256sum --check --strict SHA256SUMS` and confirms the protected artifacts are byte-identical. |
| `amf-doc-page` | Writing the threat model | Enforces documentation conventions and link-check safety. |
| `amf-red-team` | Before declaring the rulesets active | Enumerates bypass paths and attempts each one on a scratch branch. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- Three active rulesets with captured configuration.
- `docs/governance/branch_threat_model.md`.
- A documented break-glass procedure with an audit trail.
- `.github/RULESET-POLICY.md` reconciled with reality.

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Metric 9.6 reads `rulesets active: 3`.
- [ ] A non-compliant push to each protected branch is demonstrably rejected.
- [ ] The `integrity` job blocks merges to `release/*`.
- [ ] Policy document and live configuration agree line for line.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Anderson, R. (2020). *Security Engineering: A Guide to Building Dependable Distributed Systems* (3rd ed.). Wiley.
- NIST (2022). *SP 800-218: Secure Software Development Framework (SSDF) Version 1.1*.
- Torres-Arias, S., Afzali, H., Kuppusamy, T. K., Curtmola, R., & Cappos, J. (2019). "in-toto: Providing farm-to-table guarantees for bits and bytes." *USENIX Security Symposium*.
- Humble, J., & Farley, D. (2010). *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Addison-Wesley.
- Forsgren, N., Humble, J., & Kim, G. (2018). *Accelerate: The Science of Lean Software and DevOps*. IT Revolution.
- Haber, S., & Stornetta, W. S. (1991). "How to time-stamp a digital document." *Journal of Cryptology* 3(2), 99-111.

## 11. Commit protocol

Commits from this project use the scope `p02`:

```text
docs(p02): add per-branch threat model deriving ruleset strictness
docs(p02): reconcile RULESET-POLICY.md with the activated rulesets
docs(p02): document the audited break-glass procedure
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

