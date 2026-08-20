# P36 - Recovery dynamics, hysteresis and the persistent non-zero state

**Track F - Shock Propagation, Cascades & Resilience**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 1 week |
| **Lead role** | Dynamical systems analyst |
| **Upstream** | `SimulationConfig.recovery_rate`; cascade non-convergence caveat |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

Recovery is modelled as a constant subtractive healing term. Combined with cascade dynamics, the documentation notes trajectories that settle at a persistent non-zero state. That is hysteresis - the system does not return to where it started - and a constant healing rate is the simplest possible model of a process the resilience literature treats as strongly state-dependent.

## 2. Purpose

Test whether the framework exhibits genuine hysteresis, characterise it, and decide whether a state-dependent recovery term is warranted by the resilience literature.

## 3. Scope

**In scope**

- A hysteresis test: shock, release, and compare the settled state to the initial state.
- A characterisation of which markets and parameter settings produce a persistent non-zero state.
- A comparison of constant against state-dependent recovery.

**Out of scope**

- Any claim that a real market exhibits the same hysteresis.
- Adding stochastic recovery without a seed.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. Implement a shock-and-release protocol and measure the gap between the initial and final states.
2. Sweep recovery rate against cascade threshold and record where the gap is non-zero.
3. Read the resilience literature on alternative stable states and critical transitions; the persistent state is the framework's own version of a well-studied phenomenon.
4. Compare constant recovery against a state-dependent form where recovery slows as stress rises.
5. If the state-dependent form is adopted, keep the default reproducing existing behaviour exactly.
6. Report the hysteresis gap as an output quantity so it is visible rather than inferred.

## 5. Task board

- [ ] Implement the shock-and-release protocol.
- [ ] Sweep recovery against cascade threshold.
- [ ] Review the alternative-stable-states literature.
- [ ] Compare constant against state-dependent recovery.
- [ ] Report the hysteresis gap in the output.
- [ ] Publish `docs/simulation/recovery_hysteresis.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish the alternative-stable-states and critical-transition framing from primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary.
- **Stop condition:** Hysteresis and alternative stable states are defined from primary sources.

### `benchmark-runner`

- **Mandate:** Run the shock-and-release sweep and map where the gap is non-zero.
- **Inputs:** The simulator.
- **Output artifact:** A hysteresis map with seeds and commands.
- **Stop condition:** The map covers the admissible recovery and threshold ranges.

### `algorithm-implementer`

- **Mandate:** Implement the hysteresis gap output and any adopted recovery form.
- **Inputs:** The decision.
- **Output artifact:** A diff under `src/amf/simulation.py`.
- **Stop condition:** Default configuration reproduces existing traces exactly.

### `red-team-critic`

- **Mandate:** Check that no output wording implies a real market would behave this way.
- **Inputs:** Draft output text.
- **Output artifact:** A wording critique.
- **Stop condition:** Every sentence survives the illustrative-not-validated test.

**Hand-off order:** `literature-scout` -> `benchmark-runner` -> `algorithm-implementer` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-cascade-calibration` | Recovery interacts with cascade dynamics | Sweeps the joint parameter space and locates persistent-state regions. |
| `amf-invariant-spec` | A default-preservation claim is made | Writes it into the docstring and mirrors it as a regression test. |
| `amf-red-team` | Results are written up | Tests the wording against the illustrative-not-validated rule. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/simulation/recovery_hysteresis.md`
- A hysteresis map
- A reported hysteresis gap
- Any adopted recovery form

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The shock-and-release protocol is implemented and deterministic.
- [ ] Regions producing a persistent non-zero state are mapped.
- [ ] Default configuration reproduces existing traces exactly.
- [ ] No wording implies a validated claim about a real market.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Scheffer, M. (2009). *Critical Transitions in Nature and Society*. Princeton University Press.
- Scheffer, M., et al. (2009). "Early-warning signals for critical transitions." *Nature* 461, 53-59.
- Holling, C. S. (1973). "Resilience and Stability of Ecological Systems." *Annual Review of Ecology and Systematics* 4, 1-23.
- Strogatz, S. H. (2015). *Nonlinear Dynamics and Chaos* (2nd ed.). Westview Press.
- Khalil, H. K. (2002). *Nonlinear Systems* (3rd ed.). Prentice Hall.
- May, R. M. (1972). "Will a Large Complex System be Stable?" *Nature* 238, 413-414.
- Levin, S. A. (1998). "Ecosystems and the Biosphere as Complex Adaptive Systems." *Ecosystems* 1, 431-436.

## 11. Commit protocol

Commits from this project use the scope `p36`:

```text
docs(p36): frame the persistent non-zero state as hysteresis
test(p36): map hysteresis across the recovery and cascade parameter space
feat(p36): report the hysteresis gap as an explicit output
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).
