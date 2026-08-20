# Contributing to AMF-PSM

Thank you for contributing to the AMF (Original Framework) v1.0 project! This document outlines our development workflow, branch protection rules, and contribution guidelines.

## Branch Protection Rules

We use GitHub rulesets to maintain code quality and ensure a stable codebase. Here's what you need to know:

### Main Branch (`main`)
- **Status**: Fully protected
- **Requirements**:
  - ✅ All status checks must pass (CI/build, tests, linting)
  - ✅ Pull request review required (2 approvals minimum)
  - ✅ Code owner approval required
  - ✅ Commits must be signed
  - ✅ Branch must be up to date before merging
  - ✅ Stale review dismissal enabled
  - ❌ Force pushes blocked
  - ❌ Deletions blocked

**Who can bypass**: Repository admins only

### Development Branches (`develop`, `dev`)
- **Status**: Protected
- **Requirements**:
  - ✅ Status checks must pass
  - ✅ Pull request review required (1 approval)
  - ✅ Stale review dismissal enabled
  - ❌ Force pushes blocked

**Who can bypass**: Repository admins, CI/CD automation

### Release Branches (`release/*`)
- **Status**: Strictly protected
- **Requirements**:
  - ✅ Status checks must pass
  - ✅ Pull request review required (2 approvals)
  - ✅ Commits must be signed
  - ❌ Force pushes blocked
  - ❌ Deletions blocked

**Who can bypass**: Repository admins only

## Workflow

### 1. Creating a Feature Branch
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b bugfix/issue-description
# or
git checkout -b docs/documentation-update
```

**Branch naming conventions**:
- `feature/` — New features
- `bugfix/` or `fix/` — Bug fixes
- `docs/` — Documentation updates
- `refactor/` — Code refactoring
- `test/` — Test additions or improvements
- `chore/` — Maintenance tasks

### 2. Committing Your Changes
```bash
# Sign your commits (required for main branch)
git commit -S -m "feat: description of your change"
```

**Commit message format** (follows Conventional Commits):
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style changes (formatting, missing semicolons, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance or dependency updates

### 3. Submitting a Pull Request
1. Push your branch to GitHub
2. Open a pull request against the target branch (usually `develop` or `main`)
3. Fill in the PR template with:
   - Clear description of changes
   - Linked issues (if applicable)
   - Testing performed
   - Screenshots/videos (if relevant)
4. Request reviewers (at least 1 for develop, 2 for main)
5. Ensure all CI checks pass
6. Address review comments
7. Wait for approvals and merge

### 4. Merging Strategy
- **Squash merge** for feature branches → keeps history clean
- **Rebase merge** for hotfixes → maintains linear history
- **Create merge commit** for major releases → preserves branch context

## Code Quality Standards

### Python Code
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where applicable
- Minimum test coverage: 80%
- Run linting before committing: `pylint`, `black`, `flake8`

### Testing
- Write unit tests for all new features
- Update tests when fixing bugs
- Ensure all tests pass locally before pushing

### Documentation
- Update README.md if changing functionality
- Add docstrings to all functions and classes
- Include examples in documentation for complex features

## Development Setup

```bash
# Clone the repository
git clone https://github.com/sadishaumantha-maker/AMF-PSM.git
cd AMF-PSM

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
black .
pylint src/
flake8 src/
```

## Code Review Process

### For Reviewers
- Provide constructive feedback
- Approve only when:
  - Code quality standards are met
  - Tests pass and coverage is sufficient
  - Documentation is complete
  - No security vulnerabilities introduced

### For Authors
- Respond to all review comments
- Push additional commits to address feedback (don't force push)
- Re-request review after changes
- Ask for clarification if feedback is unclear

## Release Process

1. Create a release branch: `release/v1.x.x`
2. Update version numbers and CHANGELOG
3. Create a PR to `main` with 2 approvals
4. Merge to `main` and tag the commit
5. Backport critical fixes to `develop`

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Create an Issue with the bug report template
- **Security**: Email security concerns privately to maintainers
- **Documentation**: Suggest improvements in issues or discussions

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Respect others' time and expertise
- Report inappropriate behavior to maintainers

---

**Last Updated**: August 2026  
**Maintained by**: sadishaumantha-maker
