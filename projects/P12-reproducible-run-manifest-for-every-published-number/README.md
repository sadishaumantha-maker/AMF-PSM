# P12 - Reproducible-run manifest for every published number

**Track B - Engineering Quality, CI & Reproducibility**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Research engineer |
| **Upstream** | `CLAUDE.md` determinism rules; issues #137 (6.1), #139 (6.3) |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The package promises bit-identical output for identical input, but nothing published alongside a result records the input, the version, the configuration and the platform that produced it. A reader cannot currently reproduce any number quoted in the documentation.

## 2. Purpose

Define and implement a run manifest - a small, deterministic record emitted with every analytical output - so that any published figure can be regenerated exactly, in line with established reproducibility practice.

## 3. Scope

**In scope**

- A manifest schema: package version, input digest, configuration values, seed, Python version, platform.
- A helper that produces the manifest deterministically and a test that proves repeat runs match.
- A documentation rule that no number is published without its manifest.

**Out of scope**

- Adding runtime dependencies.
- Recording wall-clock time or anything else that breaks determinism.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Derive the manifest fields from the reproducibility literature, not from convenience; each field must answer "what would change this number?".
2. Hash the input market with a stable canonical serialisation - reuse `Market.to_dict` ordering guarantees.
3. Ensure the manifest itself contains nothing non-deterministic; no timestamps generated inside the library.
4. Add a property test asserting that two runs on the same input produce identical manifests.
5. Wire the manifest into the CLI output for `--format json` without breaking machine-parseability.
6. Document the rule in `CONTRIBUTING.md`: a published number without a manifest is a documentation bug.

## 5. Task board

- [ ] Write the manifest field justification table.
- [ ] Implement canonical input digesting on top of `to_dict`.
- [ ] Implement the manifest builder in the correct architectural layer.
- [ ] Add determinism tests for the manifest.
- [ ] Extend the CLI JSON output.
- [ ] Document the publication rule.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `spec-drafter`

- **Mandate:** Derive and justify the manifest schema from reproducibility standards.
- **Inputs:** The reading list.
- **Output artifact:** `docs/reproducibility.md` with a field justification table.
- **Stop condition:** Every field answers "what would change the number?" or is dropped.

### `algorithm-implementer`

- **Mandate:** Implement the manifest without adding dependencies and without breaking module layering.
- **Inputs:** Approved schema.
- **Output artifact:** A change under `src/amf/`.
- **Stop condition:** `mypy` strict passes and the one-way dependency order is unbroken.

### `determinism-prover`

- **Mandate:** Prove repeat runs and permuted-assembly runs produce identical manifests.
- **Inputs:** The implementation.
- **Output artifact:** Property tests in `tests/unit/test_properties.py`.
- **Stop condition:** Hypothesis finds no counterexample across the configured example budget.

### `api-surface-reviewer`

- **Mandate:** Check exports, `__all__` ordering and the non-trading naming guard.
- **Inputs:** The diff.
- **Output artifact:** An API review note.
- **Stop condition:** New public names are exported, sorted, and pass the boundary guard.

**Hand-off order:** `spec-drafter` -> `algorithm-implementer` -> `determinism-prover` -> `api-surface-reviewer`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-determinism-audit` | Any output-shaping change is made | Runs permutation and repeat-run invariance checks. |
| `amf-schema-roundtrip` | A serialised field is added | Proves `to_dict`/`from_dict` remains a fixed point. |
| `amf-property-harness` | A new invariant is claimed | Scaffolds a hypothesis property using the importable `build_market()` helper. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- A manifest implementation in `src/amf/`
- `docs/reproducibility.md`
- Determinism property tests
- Extended CLI JSON output

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Two runs on identical input produce byte-identical manifests.
- [ ] A permuted assembly order produces an identical manifest.
- [ ] `--format json` stdout remains machine-parseable.
- [ ] Zero new runtime dependencies; `mypy` strict and the 100% coverage gate both pass.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Peng, R. D. (2011). "Reproducible Research in Computational Science." *Science* 334(6060), 1226-1227.
- Sandve, G. K., Nekrutenko, A., Taylor, J., & Hovig, E. (2013). "Ten Simple Rules for Reproducible Computational Research." *PLoS Computational Biology* 9(10), e1003285.
- Stodden, V., McNutt, M., Bailey, D. H., et al. (2016). "Enhancing reproducibility for computational methods." *Science* 354(6317), 1240-1241.
- Wilkinson, M. D., et al. (2016). "The FAIR Guiding Principles for scientific data management and stewardship." *Scientific Data* 3, 160018.
- Wilson, G., et al. (2014). "Best Practices for Scientific Computing." *PLoS Biology* 12(1), e1001745.
- Wilson, G., Bryan, J., Cranston, K., Kitzes, J., Nederbragt, L., & Teal, T. K. (2017). "Good enough practices in scientific computing." *PLoS Computational Biology* 13(6), e1005510.
- NIST (2015). *FIPS PUB 180-4: Secure Hash Standard (SHS)*.

## 11. Commit protocol

Commits from this project use the scope `p12`:

```text
docs(p12): justify the reproducible-run manifest schema against FAIR practice
feat(p12): emit a deterministic run manifest with analytical output
test(p12): prove manifest identity under repeat and permuted runs
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

