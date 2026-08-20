# Repository Ruleset Policy

**Version**: 1.0  
**Last Updated**: August 20, 2026  
**Owner**: sadishaumantha-maker

## Overview

This document defines the GitHub repository ruleset configuration for **AMF-PSM** and the rationale behind each protection rule.

---

## 🎯 Objectives

1. **Code Quality**: Enforce consistent code standards across all branches
2. **Stability**: Prevent accidental breaks to production/main branches
3. **Security**: Require signed commits and code reviews
4. **Traceability**: Maintain clear audit trail through PRs and signed commits
5. **Collaboration**: Enable team reviews while maintaining velocity

---

## 📋 Ruleset Specifications

### Ruleset 1: Main Branch Protection

| Setting | Configuration | Reason |
|---------|---------------|--------|
| **Target** | Branch: `main` | Primary production branch |
| **Require PRs** | Yes, 2 approvals | Prevents single-person merges |
| **Code Owners** | Required | Critical file changes reviewed by experts |
| **Status Checks** | Required | All CI/CD/tests must pass |
| **Up-to-date** | Required | Prevents merge conflicts in production |
| **Dismiss stale reviews** | Yes | New commits require fresh approvals |
| **Signed commits** | Required | Cryptographic proof of authorship |
| **Force push** | Blocked | Prevents history rewriting |
| **Deletion** | Blocked | Prevents accidental branch removal |
| **Bypass** | Admins only | Emergency hotfixes require admin intervention |

**When used**: Merging release branches, hotfixes, documentation updates

---

### Ruleset 2: Development Branch Protection

| Setting | Configuration | Reason |
|---------|---------------|--------|
| **Target** | Branch: `develop`, `dev` | Integration branch for features |
| **Require PRs** | Yes, 1 approval | Faster iteration than main |
| **Status Checks** | Required | Ensures code quality before main |
| **Dismiss stale reviews** | Yes | Keeps review process current |
| **Signed commits** | No | Faster for development |
| **Force push** | Blocked | Maintains branch history |
| **Deletion** | Allowed | Lower risk than main |
| **Bypass** | Admins + CI/CD | Automated processes can push |

**When used**: Feature branches merge here first, integration testing occurs

---

### Ruleset 3: Release Branch Protection

| Setting | Configuration | Reason |
|---------|---------------|--------|
| **Target** | Pattern: `release/*` | Release candidate branches |
| **Require PRs** | Yes, 2 approvals | Extra scrutiny for releases |
| **Status Checks** | Required | Release build must succeed |
| **Signed commits** | Required | Releases must be cryptographically verified |
| **Force push** | Blocked | Release history is immutable |
| **Deletion** | Blocked | Release branches are archives |
| **Bypass** | Admins only | No automated bypass |

**When used**: Version releases, release candidate testing

---

## 🔑 Key Decisions Explained

### Why 2 Approvals on Main?
- **Risk Level**: High - affects all users
- **Impact**: Production code quality
- **Mitigation**: Requires consensus before merge

### Why Signed Commits?
- **Traceability**: Proves commit author identity
- **Security**: Prevents unauthorized code injection
- **Compliance**: Required for audited projects

### Why Dismiss Stale Reviews?
- **Safety**: Ensures reviewers see latest code
- **Prevents drift**: Catches last-minute changes
- **Encourages thoroughness**: No "rubber stamping"

### Why Different Rules per Branch?
- **Risk-based**: Main (high) > Develop (medium) > Feature (low)
- **Velocity**: Allows fast iteration in feature branches
- **Quality gates**: Tightens constraints as code approaches production

---

## 👥 Permissions Matrix

| Role | Main | Develop | Release | Feature |
|------|------|---------|---------|---------|
| **Admin** | Can merge + bypass all rules | Can merge + bypass | Can merge + bypass | Can merge |
| **Maintainer** | Can review + request changes | Can review + merge | Can review | Can merge |
| **Developer** | Can open PR + review | Can open PR + merge (with approval) | Can open PR | Can commit |
| **Contributor** | Can open PR | Can open PR | Cannot push | Can commit |

---

## 🚨 Emergency Procedures

### Hotfix to Production
1. Admin creates `hotfix/` branch from `main`
2. Fix is implemented and tested
3. **Bypass required**: Admin merges directly with explanation
4. Backport fix to `develop` immediately

### Critical Security Issue
1. Use private branch initially
2. Create focused PR with minimal diff
3. Use bypass if absolutely necessary
4. Document in commit message: `[SECURITY]`

### Rollback Procedure
1. Revert problematic commit on `main`
2. Create PR for the revert
3. Merge with standard approval process
4. Post-mortem analysis in issue

---

## 📊 Monitoring & Compliance

### Rule Violations
- Track in repository insights
- Review weekly/monthly
- Identify patterns of bypasses
- Adjust rules if needed

### Metrics to Track
- Average PR review time
- Bypass frequency and reasons
- Test pass rate
- Mean time to merge

### Audit Trail
- All commits signed and attributed
- All merges require PR (documented)
- Bypass reasons logged
- Review decisions recorded

---

## 🔄 Rule Modification Process

**To propose changes**:
1. Create issue: `[RULESET-CHANGE]` title
2. Justify: Why current rules aren't working
3. Propose: Specific rule changes
4. Discuss: Team feedback in comments
5. Approve: 2 maintainers agree
6. Implement: Update settings and this document

**Review cycle**: Quarterly (every 3 months)

---

## 📚 Related Documents

- [CONTRIBUTING.md](./CONTRIBUTING.md) — Workflow and guidelines
- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) — Community standards
- [SECURITY.md](./SECURITY.md) — Security reporting
- [pull_request_template.md](./.github/pull_request_template.md) — PR requirements

---

## ✅ Implementation Checklist

- [ ] All rulesets configured in GitHub Settings → Rules
- [ ] Team members notified of new rules
- [ ] CONTRIBUTING.md shared with team
- [ ] Branch protection rules documented
- [ ] First 5 PRs reviewed with feedback on new process
- [ ] Adjust rules based on feedback
- [ ] Schedule monthly rule review meetings

---

**For questions or issues with these policies, please open a discussion in the repository.**
