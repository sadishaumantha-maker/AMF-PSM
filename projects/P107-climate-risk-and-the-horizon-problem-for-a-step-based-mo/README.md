# P107 - Climate risk and the horizon problem for a step-based model

**Track S - Climate, Nature and Long-Horizon Risk**

| | |
|---|---|
| **Status** | `proposed` |
| **Effort** | 2 weeks |
| **Lead role** | Research lead |
| **Upstream** | `docs/RESEARCH_DISCUSSIONS.md` Discussion 8.1 |

> **Illustrative, not validated.** AMF-PSM models market *structure and resilience* only. Nothing in this project may introduce orders, prices, P&L, trading signals or backtests, and no output of this work is financial advice, a diagnosis, or a forecast of any real market. See `CLAUDE.md` -> *Hard rules*.

---

## 1. The dispute this project settles

The framework's simulation runs for at most a few dozen steps of undefined duration, and its feedback loops operate within one structural configuration. Climate risk unfolds over decades, through repeated structural change. The mismatch is not a matter of parameter tuning; the model's temporal architecture and the phenomenon's timescale are different in kind.

## 2. Purpose

Establish honestly what a step-based structural model can contribute to a decades-long risk, and refuse the parts it cannot address rather than producing a plausible-looking number.

## 3. Scope

**In scope**

- A statement of the horizon mismatch in the framework's own terms.
- Identification of any climate-related structure that is present-tense and therefore representable.
- A refusal of the projection component.

**Out of scope**

- Any climate projection, scenario outcome or transition pathway.
- Emissions, temperature or physical-risk data.

## 4. Instructions

Execute in order. Do not start a step until the previous step's artifact is committed.

1. State the mismatch precisely: a step has no defined duration, so the model has no timescale at all, and a phenomenon defined by its timescale cannot be placed in it.
2. Separate the present-tense structure from the projection. Concentration of a required function in a physically exposed location is a structural fact today; what happens to it over thirty years is not.
3. Read the official-sector work on why this is hard - the tragedy-of-the-horizon framing exists precisely because the risk exceeds the horizon of the actors and the models.
4. Identify representable structure only: disclosure-regime tiers, supervisory expectations, and concentration of dependence. These are all present-tense.
5. Refuse the projection explicitly and prominently, because climate is the topic where a plausible-looking number would do the most damage to the framework's credibility.
6. Feed the horizon finding into P111, which owns long-horizon discounting, and P128, which owns resolution limits.

## 5. Task board

- [ ] State the horizon mismatch in the model's terms.
- [ ] Separate present-tense structure from projection.
- [ ] Review the official-sector framing.
- [ ] Identify representable structure.
- [ ] Write the explicit refusal.
- [ ] Publish `docs/research/climate_horizon.md`.

## 6. Autonomous agents

Each agent below runs unattended against this charter. An agent stops at its *stop condition* and hands its artifact to the next agent; no agent may widen its own mandate.

### `literature-scout`

- **Mandate:** Establish the horizon problem and the official-sector framing from primary sources.
- **Inputs:** The reading list.
- **Output artifact:** An annotated summary.
- **Stop condition:** The framing is sourced from official-sector and peer-reviewed work.

### `math-formalizer`

- **Mandate:** State the mismatch in terms of the model's own temporal semantics.
- **Inputs:** `simulation.py`.
- **Output artifact:** A formal statement.
- **Stop condition:** The absence of a defined step duration is stated as the root of the mismatch.

### `spec-drafter`

- **Mandate:** Identify representable structure and write the refusal.
- **Inputs:** The summary and statement.
- **Output artifact:** `docs/research/climate_horizon.md`.
- **Stop condition:** The refusal is prominent, not a closing caveat.

### `red-team-critic`

- **Mandate:** Attempt to derive a climate claim from any framework output.
- **Inputs:** Rendered output.
- **Output artifact:** A derivation attempt report.
- **Stop condition:** No climate claim can be derived.

**Hand-off order:** `literature-scout` -> `math-formalizer` -> `spec-drafter` -> `red-team-critic`

## 7. Skills this project creates or exercises

| Skill | Invoked when | What it does |
|-------|--------------|--------------|
| `amf-doc-page` | The refusal is published | Enforces the illustrative-not-validated rule and documentation conventions. |
| `amf-boundary-check` | A climate construct is proposed | Rejects emissions, temperature and physical-risk inputs. |
| `amf-red-team` | Any climate-adjacent output is drafted | Attempts to extract a projection claim. |

Skill definitions live in `.claude/skills/<name>/SKILL.md`. See [the skill catalogue](../SKILL_CATALOG.md).

## 8. Deliverables

- `docs/research/climate_horizon.md`
- A formal horizon-mismatch statement
- A list of representable present-tense structure
- A prominent refusal of projection

## 9. Acceptance criteria

The project is `done` only when every line below is objectively true.

- [ ] The mismatch is stated as a property of the model's temporal semantics.
- [ ] Present-tense structure is separated from projection explicitly.
- [ ] The refusal appears prominently, not as a closing caveat.
- [ ] No climate claim can be derived from any output.

## 10. Required reading

Primary literature and standard graduate texts. Every claim committed by this project must trace to one of these or to a source of equal standing.

- Carney, M. (2015). *Breaking the Tragedy of the Horizon - climate change and financial stability*. Speech at Lloyd's of London, Bank of England.
- Bolton, P., Despres, M., Pereira da Silva, L. A., Samama, F., & Svartzman, R. (2020). *The Green Swan: Central Banking and Financial Stability in the Age of Climate Change*. Bank for International Settlements.
- Network for Greening the Financial System (2019). *A call for action: Climate change as a source of financial risk*. NGFS First Comprehensive Report.
- Network for Greening the Financial System (2020). *NGFS Climate Scenarios for Central Banks and Supervisors*.
- Task Force on Climate-related Financial Disclosures (2017). *Recommendations of the Task Force on Climate-related Financial Disclosures*. Financial Stability Board.
- Battiston, S., Mandel, A., Monasterolo, I., Schutze, F., & Visentin, G. (2017). "A climate stress-test of the financial system." *Nature Climate Change* 7, 283-288.
- Campiglio, E., Dafermos, Y., Monnin, P., Ryan-Collins, J., Schotten, G., & Tanaka, M. (2018). "Climate change challenges for central banks and financial regulators." *Nature Climate Change* 8, 462-468.
- Weitzman, M. L. (2009). "On Modeling and Interpreting the Economics of Catastrophic Climate Change." *Review of Economics and Statistics* 91(1), 1-19.

## 11. Commit protocol

Commits from this project use the scope `p107`:

```text
docs(p107): state the climate horizon mismatch in the model's own terms
docs(p107): separate representable present-tense structure from projection
docs(p107): refuse the projection component prominently
```

Rules: one logical change per commit; the body states *what changed, why, and which reference justifies it*; every commit that changes a number in `src/amf/` cites the work that fixes that number. See [COMMIT_PROTOCOL.md](../COMMIT_PROTOCOL.md).

