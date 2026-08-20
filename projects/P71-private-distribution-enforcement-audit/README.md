# P71 - Private distribution enforcement audit

**Track L - Intellectual Property, Provenance & Security**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 4 days |
| **Lead role** | Release manager |
| **Upstream** | `RELEASING.md`, `pyproject.toml` classifier, `tests/unit/test_packaging.py` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The package must never reach a public index, and three mechanisms defend that: the classifier, the packaging test, and the absence of a publish workflow. But the repository itself is public, so the source is already readable by anyone. What exactly is being protected, and against what, has never been stated - which makes it impossible to tell whether the controls are adequate or theatrical.

## 2. Purpose

State the distribution threat model precisely, audit whether the controls address it, and close or document every gap.

## 3. Scope

**In scope**

- A distribution threat model: what a public index enables that a public repository does not.
- An audit of the three existing controls against that model.
- Identification of unprotected channels, including release assets and CI artifacts.

**Out of scope**

- Making the repository private - out of scope for this project.
- Weakening any existing control.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State what a public index enables: discoverability, `pip install` by name, dependency resolution, and an implied grant of use. A public repository enables reading; it does not enable those.
2. Audit each control against that model, and note the one already documented in `RELEASING.md`: a GitHub Release asset or an Actions artifact is not a private channel.
3. Enumerate every channel by which a built artifact could leave: index upload, release asset, Actions artifact, and any workflow that writes to an external service.
4. Check each channel against the controls and record which are open.
5. Close or document each open channel; the P08 anti-upload self-check is the model for closing them.
6. Confirm the packaging test still fails if the classifier is removed from either the config or the built wheel.

## 5. Task board

- [ ] Write the distribution threat model.
- [ ] Audit the three controls against it.
- [ ] Enumerate all artifact egress channels.
- [ ] Close or document each open channel.
- [ ] Verify the packaging test's dual assertion.
- [ ] Publish `docs/integrity/distribution.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** Write the distribution threat model distinguishing a public index from a public repository.
- **Inputs:** `LICENSE.txt`, `RELEASING.md`.
- **Output artifact:** `docs/integrity/distribution.md`.
- **Stop condition:** The model states what is protected and what is already public.

### `red-team-critic`

- **Mandate:** Enumerate every channel by which a built artifact could leave the repository.
- **Inputs:** All workflows and configuration.
- **Output artifact:** An egress channel list.
- **Stop condition:** Every channel is closed or documented as accepted.

### `release-marshal`

- **Mandate:** Verify the packaging invariants still hold in config and in the built wheel.
- **Inputs:** `pyproject.toml`, `tests/unit/test_packaging.py`.
- **Output artifact:** A verification record.
- **Stop condition:** Removing the classifier from either location turns the test red.

**Hand-off order:** `spec-drafter` -> `red-team-critic` -> `release-marshal`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-integrity-verify` | A distribution control is audited | Verifies the classifier in config and wheel and checks for publish steps. |
| `amf-red-team` | Egress channels are enumerated | Searches every workflow for artifact-producing or externally-writing steps. |
| `amf-doc-page` | The threat model is published | Enforces documentation conventions. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/integrity/distribution.md`
- A control audit
- An egress channel list with dispositions
- A packaging invariant verification record

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The threat model distinguishes a public index from a public repository.
- [ ] Every artifact egress channel is closed or documented as accepted.
- [ ] Removing the classifier from config or wheel turns the packaging test red.
- [ ] No publish workflow exists anywhere in the repository.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- NIST (2022). *SP 800-218: Secure Software Development Framework (SSDF) Version 1.1*.
- Torres-Arias, S., Afzali, H., Kuppusamy, T. K., Curtmola, R., & Cappos, J. (2019). "in-toto: Providing farm-to-table guarantees for bits and bytes." *USENIX Security Symposium*.
- Anderson, R. (2020). *Security Engineering: A Guide to Building Dependable Distributed Systems* (3rd ed.). Wiley.
- Humble, J., & Farley, D. (2010). *Continuous Delivery: Reliable Software Releases through Build, Test, and Deployment Automation*. Addison-Wesley.
- NIST (2015). *FIPS PUB 180-4: Secure Hash Standard (SHS)*.

## 11. Commit protocol

Commits from this project use the scope `p71`:

```text
docs(p71): state the private-distribution threat model
docs(p71): audit artifact egress channels and record dispositions
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

