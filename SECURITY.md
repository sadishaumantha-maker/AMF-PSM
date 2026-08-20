# Security Policy

## Reporting Security Vulnerabilities

**DO NOT** create a public GitHub issue for security vulnerabilities. Instead:

1. **Email**: security@example.com (or privately contact maintainer)
2. **Include**:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)
3. **Response time**: We aim to respond within 48 hours

## Responsible Disclosure

- Allow 90 days for a fix before public disclosure
- Credit reporter in security advisory (unless requested otherwise)
- Work with us to coordinate timing of public announcement

---

## Security Best Practices in This Repository

### Commits
- All commits must be signed with GPG
- Verify commit signatures: `git log --show-signature`

### Dependencies
- Regularly updated via automated scanning
- No known vulnerabilities allowed
- Pin versions in production environments

### Code Review
- Security review for all code changes
- Special review for authentication/authorization code
- Dependency updates require approval

### Environment Variables
- Never commit `.env` files
- Use GitHub Secrets for sensitive data
- Rotate credentials regularly

---

## Supported Versions

| Version | Status | Security Updates |
|---------|--------|------------------|
| 1.x | Current | Yes |
| 0.x | Legacy | Limited |

---

## Security Features

- ✅ Signed commits required on main branch
- ✅ Branch protection with code review
- ✅ Automated dependency scanning (Dependabot)
- ✅ Required status checks before merge
- ✅ Protected secrets in GitHub

---

## Contact

For security concerns, reach out to maintainers privately.