# `.claude/` — agent operating system

Autonomous agents, skills, and durable memory for turning source documents into faithful GitHub
issues, and for researching those issues deeply enough to say what to actually do about them.

Nothing here is part of the `amf` package. The coverage gate (`--cov=amf`) does not see it.

## Why this exists

Two failures motivated it, both real:

1. A decomposition of `docs/RESEARCH_DISCUSSIONS.md` into 43 issues was verbatim-correct across all
   253 atomic source units — except issue **#62's title**, where `Feedback Loops: Markets ↔ Policy`
   silently became `Feedback Loops — Markets ↔ Policy`. Ad-hoc verification checked bodies and never
   thought to check titles. Fidelity has to be mechanical.
2. Two agent sessions decomposed overlapping material at the same time (#45–#92 and #77–#98) because
   nothing recorded what had already been done.

## Map

```
agents/     one job each; only issue-publisher may write to GitHub
skills/     procedures and deterministic scripts
memory/     durable state across sessions
manifests/  reviewable decomposition proposals (the approval gate)
```

### Agents

| Agent | Writes | Job |
|---|---|---|
| `issue-cartographer` | manifest | Source document → reviewable decomposition manifest |
| `issue-publisher` | **GitHub** | Executes an approved manifest; the only write path |
| `issue-auditor` | nothing | Independently verifies published issues against source |
| `issue-researcher` | dossiers | One issue → evidence-graded research dossier |
| `issue-strategist` | strategy doc | All issues → sequencing, duplicates, blockers |

The auditor is deliberately separate from the author. An agent that grades its own work would have
missed #62 exactly as the human review did.

### Skills

| Skill | Loaded when |
|---|---|
| `amf-guardrails` | Always, before writing anything |
| `issue-intake` | Decomposing a document |
| `issue-authoring` | Creating or updating an issue |
| `issue-audit` | Verifying fidelity or coverage |
| `research-dossier` | Researching how to solve an issue |

### Memory

| File | Contents |
|---|---|
| `memory/repo-facts.md` | Ground truth; auto-loaded via CLAUDE.md |
| `memory/issue-index.md` | Source unit ↔ issue registry; auto-loaded |
| `memory/source-registry.md` | Which documents are decomposed, with content hashes |
| `memory/decisions.md` | ADR log — why each rule exists |
| `memory/open-questions.md` | Items needing a human decision |

## The operating rule

**Propose → approve → publish.** The cartographer produces a manifest and stops. A human approves it.
Only then does the publisher write to GitHub. This is what makes re-runs idempotent and keeps a bad
frame from propagating across dozens of issues before anyone sees it.

An autonomous run may read anything, write manifests and dossiers, and post issue comments. It may
never close or delete an issue, edit an issue it did not create, touch `SHA256SUMS`, push to `main`,
or publish a package.
