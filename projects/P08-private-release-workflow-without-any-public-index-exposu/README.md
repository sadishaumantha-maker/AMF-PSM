# P08 - Private release workflow without any public index exposure

**Track B - Engineering Quality, CI & Reproducibility**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 3 days |
| **Lead role** | Release manager |
| **Upstream** | issue #115 (2.3), `RELEASING.md` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

A release workflow is wanted for repeatable tagging, but the repository is public and the package is all-rights-reserved. Any workflow that produces a downloadable artifact through a Release asset or an Actions artifact defeats the private-distribution rule. The dispute is whether automation is possible at all.

## 2. Purpose

Build a release workflow that automates *version discipline* - tag, changelog, version-string agreement, integrity re-verification - and deliberately produces no distributable artifact.

## 3. Scope

**In scope**

- A tag-and-verify workflow: version sync check, CHANGELOG check, integrity check, packaging-invariant test.
- An explicit negative test proving no wheel or sdist leaves CI.
- A `RELEASING.md` update describing the automated and the manual halves.

**Out of scope**

- Uploading to PyPI or any other index - forbidden.
- Attaching build outputs to a GitHub Release or Actions artifact.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Read `RELEASING.md` and `tests/unit/test_packaging.py` and list every invariant the release must preserve.
2. Design the workflow so its only outputs are a tag, a verification log, and a failure if anything disagrees.
3. Assert the `Private :: Do Not Upload` classifier in both `pyproject.toml` and the built wheel metadata as a gate.
4. Add a step that fails if any artifact-upload action appears in the workflow file.
5. Re-run the integrity check as the final gate before the tag is created.
6. Update `RELEASING.md` and record what remains manual and why.

## 5. Task board

- [ ] Inventory release invariants from `RELEASING.md` and the packaging tests.
- [ ] Implement `.github/workflows/release.yml` (tag-and-verify only).
- [ ] Add the version-string agreement gate.
- [ ] Add the classifier gate for config and built wheel.
- [ ] Add the anti-upload self-check.
- [ ] Update `RELEASING.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `release-marshal`

- **Mandate:** Implement the tag-and-verify workflow and the version-agreement gate.
- **Inputs:** `pyproject.toml`, `amf/__init__.py`, `CHANGELOG.md`.
- **Output artifact:** `.github/workflows/release.yml`.
- **Stop condition:** The workflow fails on a deliberately mismatched version pair.

### `integrity-warden`

- **Mandate:** Make integrity verification the last gate before tagging.
- **Inputs:** `SHA256SUMS`, `integrity.yml`.
- **Output artifact:** An ordered gate list in the workflow.
- **Stop condition:** No tag can be created while the integrity check is failing.

### `red-team-critic`

- **Mandate:** Attempt to exfiltrate a build artifact through the release path.
- **Inputs:** The workflow definition.
- **Output artifact:** An exfiltration attempt report.
- **Stop condition:** No path produces a downloadable package artifact.

**Hand-off order:** `release-marshal` -> `integrity-warden` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-integrity-verify` | Before a tag is created | Verifies the four protected artifacts against `SHA256SUMS`. |
| `amf-changelog-entry` | Preparing a release | Moves `## [Unreleased]` content into a dated version section. |
| `amf-red-team` | Reviewing the release workflow | Searches for any artifact-producing or index-publishing step. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `.github/workflows/release.yml`
- An updated `RELEASING.md`
- An exfiltration attempt report

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The workflow creates tags and never produces a downloadable artifact.
- [ ] A mismatched version pair fails the workflow.
- [ ] `tests/unit/test_packaging.py` still passes and the classifier gate is enforced twice.
- [ ] No publish step exists anywhere in `.github/workflows/`.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Humble, J., & Farley, D. (2010). *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Addison-Wesley.
- NIST (2022). *SP 800-218: Secure Software Development Framework (SSDF) Version 1.1*.
- Torres-Arias, S., Afzali, H., Kuppusamy, T. K., Curtmola, R., & Cappos, J. (2019). "in-toto: Providing farm-to-table guarantees for bits and bytes." *USENIX Security Symposium*.
- NIST (2015). *FIPS PUB 180-4: Secure Hash Standard (SHS)*.
- Haber, S., & Stornetta, W. S. (1991). "How to time-stamp a digital document." *Journal of Cryptology* 3(2), 99-111.

## 11. Commit protocol

Commits from this project use the scope `p08`:

```text
ci(p08): add tag-and-verify release workflow with no artifact output
ci(p08): gate releases on version-string agreement and integrity verification
docs(p08): document the automated and manual halves of the private release
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
