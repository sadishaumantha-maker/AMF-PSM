# P70 - Integrity chain verification for the protected artifacts

**Track L - Intellectual Property, Provenance & Security**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Integrity owner |
| **Upstream** | `SHA256SUMS`, `.github/workflows/integrity.yml`, the OpenTimestamps proof |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Four artifacts are protected by a checksum file, a pre-commit hook, workflow verification and `.gitattributes` byte-stability rules. That is four mechanisms with no single document explaining what each one catches and what would slip past all of them. Defence in depth without an assurance argument is a collection of controls, not a guarantee.

## 2. Purpose

Write the assurance argument: what each control catches, what the combination guarantees, and what it does not - then test each control by deliberate violation.

## 3. Scope

**In scope**

- An assurance argument covering all four controls and the timestamp proof.
- A deliberate-violation test per control.
- A documented verification procedure a third party could follow.

**Out of scope**

- Modifying any protected artifact for any reason.
- Adding source files to `SHA256SUMS`.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Enumerate the controls: the checksum file, the `protect-ip-artifacts` pre-commit hook, the whitespace-hook exclusions, the `.gitattributes` binary and EOL rules, and the workflow verification.
2. For each, state the threat it addresses and the threat it does not.
3. Explain the timestamp proof's role: it establishes that the document existed in this form at a point in time, which is a different guarantee from integrity in the repository.
4. Test each control by deliberate violation on a scratch branch, and record which control fired.
5. Identify any threat that no control addresses, and either add a control or document the accepted risk.
6. Write the third-party verification procedure so the proof is checkable by someone who does not trust the repository.

## 5. Task board

- [ ] Enumerate all controls and their threats.
- [ ] State what the timestamp proof does and does not establish.
- [ ] Run the deliberate-violation test per control.
- [ ] Identify unaddressed threats.
- [ ] Write the third-party verification procedure.
- [ ] Publish `docs/integrity/assurance.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `integrity-warden`

- **Mandate:** Enumerate controls, state their threat coverage and write the verification procedure.
- **Inputs:** `SHA256SUMS`, hooks, `.gitattributes`, workflows.
- **Output artifact:** `docs/integrity/assurance.md`.
- **Stop condition:** Every control has a stated threat and a stated gap.

### `red-team-critic`

- **Mandate:** Attempt to modify a protected artifact without any control firing.
- **Inputs:** The repository on a scratch branch.
- **Output artifact:** A violation attempt report.
- **Stop condition:** No modification path avoids every control, or the gap is documented and closed.

### `literature-scout`

- **Mandate:** Establish what cryptographic timestamping guarantees from primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary.
- **Stop condition:** The guarantee is stated from the originating literature, not from product marketing.

**Hand-off order:** `integrity-warden` -> `red-team-critic` -> `literature-scout`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-integrity-verify` | Any control or protected path is touched | Runs the strict checksum verification and refuses edits to protected artifacts. |
| `amf-red-team` | The assurance argument is written | Attempts a modification that avoids every control. |
| `amf-doc-page` | The assurance argument is published | Enforces documentation conventions. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/integrity/assurance.md`
- A per-control threat and gap statement
- Deliberate-violation evidence
- A third-party verification procedure

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every control has a stated threat coverage and a stated gap.
- [ ] Each control is proven to fire by deliberate violation.
- [ ] No modification path avoids all controls, or the gap is documented and closed.
- [ ] The protected artifacts are byte-identical at the end of the project.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Haber, S., & Stornetta, W. S. (1991). "How to time-stamp a digital document." *Journal of Cryptology* 3(2), 99-111.
- Merkle, R. C. (1980). "Protocols for Public Key Cryptosystems." *IEEE Symposium on Security and Privacy*, 122-134.
- NIST (2015). *FIPS PUB 180-4: Secure Hash Standard (SHS)*.
- Anderson, R. (2020). *Security Engineering: A Guide to Building Dependable Distributed Systems* (3rd ed.). Wiley.
- Schneier, B. (2015). *Applied Cryptography* (20th Anniversary ed.). Wiley.
- Torres-Arias, S., Afzali, H., Kuppusamy, T. K., Curtmola, R., & Cappos, J. (2019). "in-toto: Providing farm-to-table guarantees for bits and bytes." *USENIX Security Symposium*.
- NIST (2022). *SP 800-218: Secure Software Development Framework (SSDF) Version 1.1*.

## 11. Commit protocol

Commits from this project use the scope `p70`:

```text
docs(p70): write the integrity assurance argument for the protected artifacts
docs(p70): record deliberate-violation evidence per integrity control
docs(p70): publish a third-party verification procedure
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

