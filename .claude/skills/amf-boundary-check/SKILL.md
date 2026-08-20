---
name: amf-boundary-check
description: Run the non-trading naming guard against a proposed name and supply a structural replacement on a hit. Use before adopting any public name, field or document term.
---

# amf-boundary-check

The `amf` package models market structure and resilience only. It must never gain orders, brokers, prices,
returns, P&L, trading signals or backtests.

## Forbidden substrings

`order`, `buy`, `sell`, `price`, `pnl`, `broker`, `backtest`, `ticker`, `trade`, `portfolio`,
`candlestick`, `returns`, `signal`.

## Procedure

1. Check the proposed name against every substring, case-insensitively.
2. On a hit, supply the structural alternative rather than only rejecting: `load`, `stress`,
   `absorptive_capacity`, `integrity`, `redundancy`, `criticality`, `coupling`, `dependency`.
3. Run `tests/unit/test_non_trading_boundary.py`. It walks every public class reachable from `amf.__all__`
   and checks public names, members and dataclass fields.
4. The `ALLOWLIST` holds exactly one documented exception, `CouplingMatrix.order`. A meta-test asserts every
   allowlist entry still exists, so stale exemptions fail. **Adding an entry requires human sign-off** and is
   a last resort, never a fix.
5. Apply the same check to prose in `docs/` and `projects/`. Documents that reason in market-data vocabulary
   produce code that does.

## Repository rules that always apply

- No trading vocabulary in any public name (see `amf-boundary-check`).
- No claim of predictive power or validated performance; AMF is illustrative.
- Never modify a checksum-protected artifact and never add source files to `SHA256SUMS`.
- Zero runtime dependencies; standard library only.
- Identical inputs must produce identical output, bit for bit.
