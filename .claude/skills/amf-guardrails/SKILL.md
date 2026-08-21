---
name: amf-guardrails
description: The AMF-PSM non-negotiable rules — the non-trading boundary, illustrative-not-validated, determinism, and the protected IP artifacts. Load this BEFORE writing any issue, research dossier, documentation, or code in this repository, every single time, no exceptions. Use it whenever source material mentions trading, prices, orders, forecasting, prediction, liquidity, returns, or market data, and whenever you are about to claim the toolkit can predict or diagnose a real market.
---

# AMF-PSM guardrails

Four rules. They are not style preferences — three of them are mechanically enforced by CI, and
breaking the fourth is a licensing problem.

## 1. No trading system

The `amf` package models market **structure and resilience** only. Every quantity is a
**dimensionless structural measure**.

`tests/unit/test_non_trading_boundary.py` walks every public class reachable from `amf.__all__` and
fails if any public name, member, or dataclass field contains one of these substrings:

```
order  buy  sell  price  pnl  broker  backtest  ticker  trade  portfolio  candlestick  returns  signal
```

One documented exception lives in that file's `ALLOWLIST`: `CouplingMatrix.order` (the matrix's
row/column ordering). A meta-test asserts every allowlist entry still exists, so stale exemptions fail.

**What this means in practice:**

- Matching is on *identifiers*, never on prose. Research documents and issue bodies may discuss
  trading concepts freely. `src/amf/` may not *name* them.
- When source material asks for a market-data quantity, do not transcribe it and do not silently
  drop it. Translate it. See `references/translation-table.md`.
- Pick structural vocabulary: `load`, `stress`, `absorptive_capacity`, `integrity`, `redundancy`,
  `criticality`, `concentration`.

## 2. Illustrative, not validated

Thresholds, weights, and scores in this toolkit are **not empirically validated**. Its output is
**not financial advice, not a diagnosis, and not a forecast of any real market.**

- Never add language claiming predictive power or validated performance.
- Keep every existing disclaimer: the package docstring, README, the CLI's `_DISCLAIMER`, and `viz`'s
  `_FOOTNOTE` baked into each rendered image.
- Source material that asks "can we predict X 6–12 months ahead?" is a **research question**, not a
  capability claim. Record it as a hypothesis to be tested, with the evidence that would be needed.
  Never let it migrate into user-facing package text.

## 3. Determinism

Identical inputs must produce bit-identical output.

- Iterate in canonical order — `SystemKind` declaration order for systems, `(source, target, kind)`
  declaration order for edges. A dict-insertion-order tie-break is a bug, not a detail: floating-point
  addition is not associative, so insertion-ordered traversal changes results in the last bits.
- Gate all randomness behind an explicit seed. `jitter` has no effect unless `seed` is also set.
- Renderers are pure: no I/O, no clock reads, no randomness.
- Validate tuning parameters on construction and raise `InvalidConfigError` — never normalise a
  nonsensical knob into a plausible-looking number.

## 4. Protected IP and private distribution

- **Never modify** the checksum-protected artifacts listed in `SHA256SUMS`:
  `AMF Framework v1.docx`, `AMF Framework v1.docx.ots`, `anatomical-market-framework`, `LICENSE.txt`.
  Do not add source files to `SHA256SUMS`.
- **Never read the framework document to generate output.** The CLI's `describe` text comes from
  paraphrased constants in `cli.py`, deliberately, so the software never touches the protected artifacts.
- `amf` is proprietary and all-rights-reserved: never publish to PyPI or any public index. The
  `Private :: Do Not Upload` classifier must stay. The repository is public, so a GitHub Release
  asset or Actions artifact is **not** a private channel.
- This repository is public. Never place secrets, credentials, or verbatim protected-framework text
  in any file under `.claude/`.

## The three-point gate

Guardrails are checked at three separate points, so no single agent's judgement is load-bearing:

| Point | Who | Action |
|---|---|---|
| Intake | `issue-cartographer` | **Flag** any source unit whose text requires forbidden framing |
| Authoring | `issue-researcher`, `issue-publisher` | **Reframe** via the translation table; apply the `guardrail-review` label |
| Verification | `issue-auditor` | **Verify** no forbidden vocabulary reached a published artifact |

## Handling a flagged unit

A source unit whose framing violates a guardrail is never silently transcribed *and* never silently
altered. Both hide the conflict. Instead, the issue gets:

1. The source text, quoted verbatim, under a clearly-marked heading — the record of what was asked.
2. A `## Structural reframing required` section stating the conflict and the compliant reading.
3. The `guardrail-review` label.

That way the human sees both the original intent and the translation, and can overrule either.

## Reference

`references/translation-table.md` — the phrasing-to-structure mapping. Read it whenever source
material uses market-data vocabulary. It is the difference between a compliant reframing and a guess.
