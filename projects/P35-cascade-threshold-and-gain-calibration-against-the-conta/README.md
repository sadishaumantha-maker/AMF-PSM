# P35 - Cascade threshold and gain calibration against the contagion literature

**Track F - Shock Propagation, Cascades & Resilience**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1.5 weeks |
| **Lead role** | Complex systems analyst |
| **Upstream** | `SimulationConfig.cascade_threshold`, `cascade_gain`, `cascade_absorption_drop` |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Cascade dynamics are opt-in and parameterised by a threshold, a gain and an absorption drop, none of which has a source. The documentation warns that convergence is not guaranteed under cascade dynamics and that the trajectory may settle at a persistent non-zero state. Threshold-cascade models have a substantial published literature with known phase behaviour, and none of it is currently used.

## 2. Purpose

Anchor the cascade parameters in the threshold-cascade and financial-contagion literature, map the phase behaviour of the framework's own model, and warn the user when the configuration sits near a phase boundary.

## 3. Scope

**In scope**

- A mapping between AMF's cascade parameters and the parameters of published threshold-cascade models.
- A phase diagram of cascade extent over the threshold and gain plane for representative markets.
- A runtime warning or reported flag when the configuration sits in the sensitive region.

**Out of scope**

- Claiming that any parameter setting reproduces a real crisis.
- Making cascade dynamics the default.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Read the primary threshold-cascade and financial-contagion sources and identify what each parameter corresponds to.
2. Note the central published finding that cascade extent is non-monotonic in connectivity, with a window where global cascades are possible - this is the behaviour the phase diagram should reveal or fail to reveal.
3. Sweep threshold and gain across a grid for representative markets and record cascade extent and tipped-system count.
4. Identify the sensitive region where a small parameter change produces a large extent change.
5. Report a flag when a run's configuration falls in that region, so a user does not quote a knife-edge result as if it were robust.
6. Document the non-convergence caveat as a computed property, not only as prose.

## 5. Task board

- [ ] Map AMF cascade parameters onto published model parameters.
- [ ] Implement a deterministic parameter sweep harness.
- [ ] Produce phase diagrams for representative markets.
- [ ] Identify and encode the sensitive region.
- [ ] Report a knife-edge flag in the output.
- [ ] Publish `docs/simulation/cascade_calibration.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish the parameter correspondence with published cascade models from primary sources.
- **Inputs:** The reading list.
- **Output artifact:** A parameter correspondence table.
- **Stop condition:** Every AMF cascade parameter maps to a named quantity in a cited model, or is marked AMF-specific.

### `benchmark-runner`

- **Mandate:** Sweep the threshold-gain plane deterministically and record cascade extent.
- **Inputs:** The simulator.
- **Output artifact:** Phase-diagram data with seeds and commands.
- **Stop condition:** The grid covers the admissible parameter ranges at a stated resolution.

### `algorithm-implementer`

- **Mandate:** Encode the sensitive region and report the knife-edge flag.
- **Inputs:** Phase-diagram data.
- **Output artifact:** A diff under `src/amf/simulation.py`.
- **Stop condition:** The flag appears in `ResilienceScore` output and round-trips.

### `viz-designer`

- **Mandate:** Render the phase diagram deterministically as SVG with the mandatory footnote.
- **Inputs:** Phase-diagram data.
- **Output artifact:** A figure under `docs/simulation/`.
- **Stop condition:** Repeat renders are byte-identical and the footnote is present.

**Hand-off order:** `literature-scout` -> `benchmark-runner` -> `algorithm-implementer` -> `viz-designer`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-cascade-calibration` | Cascade parameters are set or changed | Sweeps the parameter plane, locates the sensitive region and flags knife-edge configurations. |
| `amf-figure-render` | A figure is produced | Renders deterministic SVG with the required footnote and verifies byte-identical repeats. |
| `amf-config-validator` | A cascade knob changes | Adds `InvalidConfigError` validation with boundary tests. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/simulation/cascade_calibration.md`
- A parameter correspondence table
- Phase diagrams
- A knife-edge configuration flag

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] Every cascade parameter maps to a cited model quantity or is marked AMF-specific.
- [ ] Phase behaviour is measured over a documented grid.
- [ ] Knife-edge configurations are flagged in the output.
- [ ] Defaults still reproduce the linear model exactly.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Watts, D. J. (2002). "A simple model of global cascades on random networks." *PNAS* 99(9), 5766-5771.
- Motter, A. E., & Lai, Y.-C. (2002). "Cascade-based attacks on complex networks." *Physical Review E* 66, 065102(R).
- Gai, P., & Kapadia, S. (2010). "Contagion in financial networks." *Proceedings of the Royal Society A* 466(2120), 2401-2423.
- Acemoglu, D., Ozdaglar, A., & Tahbaz-Salehi, A. (2015). "Systemic Risk and Stability in Financial Networks." *American Economic Review* 105(2), 564-608.
- Elliott, M., Golub, B., & Jackson, M. O. (2014). "Financial Networks and Contagion." *American Economic Review* 104(10), 3115-3153.
- Glasserman, P., & Young, H. P. (2016). "Contagion in Financial Networks." *Journal of Economic Literature* 54(3), 779-831.
- Battiston, S., Puliga, M., Kaushik, R., Tasca, P., & Caldarelli, G. (2012). "DebtRank: Too Central to Fail? Financial Networks, the FED and Systemic Risk." *Scientific Reports* 2, 541.
- Scheffer, M. (2009). *Critical Transitions in Nature and Society*. Princeton University Press.

## 11. Commit protocol

Commits from this project use the scope `p35`:

```text
docs(p35): map cascade parameters onto published threshold-cascade models
test(p35): sweep the cascade phase plane for representative markets
feat(p35): flag knife-edge cascade configurations in the reported score
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

