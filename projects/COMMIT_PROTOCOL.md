# Commit protocol

Commits produced by a charter in this section follow one convention, so the history reads as a record of
decisions rather than a record of keystrokes.

## Subject line

```text
<type>(<project-id>): <what changed, imperative, lower case>
```

`<type>` is one of `feat`, `fix`, `docs`, `test`, `ci`, `chore`, `refactor`. `<project-id>` is the charter's
id in lower case, for example `p14`. Append `!` after the scope for a change that moves a published number
or breaks an interface: `fix(p28)!: set the methodologically justified concentration default`.

## Body

Three things, in this order:

1. **What changed** - the substance, not the file list. The diff already lists the files.
2. **Why** - the dispute it settles, or the measurement that forced it.
3. **Which reference justifies it** - for any commit that changes a number, a threshold or a weight in
   `src/amf/`, name the work that fixes it. A number without a source is the thing this whole section
   exists to eliminate.

## Rules

- **One logical change per commit.** A commit that both refactors and changes behaviour cannot be reverted
  cleanly, and cannot be reviewed at all.
- **Every commit passes the gates.** `ruff check .`, `ruff format --check .`, `mypy`, and `pytest` with the
  100% statement and branch coverage gate. A commit that needs the next commit to be green is not a commit.
- **User-visible changes carry a CHANGELOG entry** under `## [Unreleased]`, categorised Added, Changed,
  Fixed or Security.
- **Never** modify a checksum-protected artifact, add a source file to `SHA256SUMS`, weaken a coverage or
  lint gate, add an entry to the non-trading allowlist without human sign-off, or add a publish workflow.

## Worked example

```text
fix(p22): guard Katz centrality against series divergence

centrality() returned NaN for every system on densely coupled markets, because
the influence series diverges before max-normalisation whenever alpha exceeds
the inverse of the graph's spectral radius. The default alpha of 0.4 satisfies
the condition on a sparse market and violates it on a dense one.

centrality() now estimates the spectral radius by power iteration and raises
InvalidConfigError naming the largest admissible alpha, rather than returning
NaN. The estimate is deliberately conservative: borderline graphs are refused.

Justified by Katz (1953) for the influence series and Horn & Johnson (2012)
chapter 5 for the convergence condition on the attenuation factor.
```

## Relationship to the pull request template

The repository's `.github/pull_request_template.md` governs the pull request. This protocol governs the
commits inside it. A pull request from a charter names the charter and links it.
