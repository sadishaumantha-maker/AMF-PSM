---
description: Establish verified time, scan CLAUDE.md for drift, and fix what is genuinely wrong.
---

Run the full CLAUDE.md maintenance pass, in this order. Do not skip or reorder.

1. **Time first.** Use the `chronos-warden` agent. If it reports anything other than
   VERIFIED, stop and report why. Do not widen the budget to force a pass.
2. **Establish the facts.** Use the `claude-md-auditor` agent to scan and to verify each
   finding against the source itself.
3. **Fix the mechanical sections** with `repo-cartographer`, and any CI-section drift with
   `ci-forensics`.
4. **Try to refute your own edits** with `doc-guard-verifier`. Any REFUTED line is dropped,
   not argued with.
5. **Record user-visible changes** with `changelog-scribe`.
6. **Check the hard rules** with `hard-rules-sentinel` before anything is committed.
7. Re-run `python -m tools.docsync scan` and confirm it reports no drift.

Open a **draft** pull request. Never auto-merge, never push to `main`, and never edit the
checksum-protected artifacts.
