name: Pull Request Template
description: Standard PR template for AMF-PSM contributions
title: "[TYPE] Brief description of change"
labels: ["needs-review"]
assignees: []
---

## 📝 Description

<!-- Provide a clear description of what this PR does. -->

**What problem does this solve?**
<!-- Explain the motivation or issue being addressed -->

**What changes are made?**
<!-- List the main changes/files modified -->

---

## 🔗 Related Issues

<!-- Link to related issues using #ISSUE_NUMBER -->
Closes #
Related to #

---

## 🧪 Testing

<!-- Describe how you tested your changes -->

- [ ] Unit tests added/updated
- [ ] Integration tests passed
- [ ] Manual testing completed
- [ ] No regressions detected

**Test coverage**: ___% (minimum 80%)

**Steps to reproduce/test**:
```bash
# Add steps to test your changes
```

---

## 📸 Screenshots / Videos

<!-- If applicable, add screenshots or screen recordings demonstrating the changes -->

---

## ✅ Checklist

- [ ] Code follows [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- [ ] Self-review completed
- [ ] Comments added for complex logic
- [ ] Documentation updated
- [ ] No breaking changes
- [ ] All tests pass locally
- [ ] Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
- [ ] Branch is up to date with `main`/`develop`
- [ ] Code owner review requested (if applicable)

---

## 🔐 Security Considerations

- [ ] No hardcoded secrets/credentials
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] No authentication bypass
- [ ] Dependencies are from trusted sources

---

## 📊 Type of Change

<!-- Mark the relevant option with an "x" -->

- [ ] 🐛 Bug fix (non-breaking change that fixes an issue)
- [ ] ✨ New feature (non-breaking change that adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to change)
- [ ] 📚 Documentation update
- [ ] 🔧 Configuration change
- [ ] ♻️ Refactoring (no behavior change)
- [ ] ⚡ Performance improvement
- [ ] 🧪 Test addition/improvement

---

## 🎯 Priority

<!-- Select the priority level -->

- [ ] 🔴 Critical (production hotfix, security issue)
- [ ] 🟠 High (urgent feature, blocking issue)
- [ ] 🟡 Medium (normal priority feature/fix)
- [ ] 🟢 Low (nice-to-have, documentation)

---

## 📝 Additional Notes

<!-- Any additional context for reviewers -->

---

## 👥 Reviewers: Please Check

- [ ] Code quality and style
- [ ] Logic and correctness
- [ ] Test coverage
- [ ] Documentation completeness
- [ ] No security issues
- [ ] Performance impact acceptable
- [ ] Follows branch protection rules

---

**Remember**: Keep PRs focused and reviewable. If this PR is large (>400 lines), consider splitting it into smaller PRs.