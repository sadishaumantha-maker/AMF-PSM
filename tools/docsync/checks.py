"""The individual drift checks.

Each check is a pure function of ``(facts, claims)`` returning findings. Two conventions
matter:

* **Bidirectional by default.** Roughly half the drift found in this repository consisted of
  *omissions* -- a real docs file nobody documented, a real flag nobody listed. A check that
  only asks "is everything named here real?" passes on all of them, so most checks also ask
  "is everything real named here?".
* **No guessing.** Where a fact cannot be established (pytest missing, a section absent), the
  check yields nothing and the runner records it as skipped. A skipped check is visible; a
  guessed one is a lie.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from tools.docsync.links import find_dead_links
from tools.docsync.model import Finding, Severity

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable

    from tools.docsync.claims import Claims
    from tools.docsync.facts import RepoFacts

GUIDE = "CLAUDE.md"
"""The document whose claims are under test."""

_RENDERERS = frozenset({"report", "viz", "cli"})
"""Top layer of the declared one-way dependency order; nothing below may import these."""


def _fmt(values: Iterable[str]) -> str:
    """Render a set of names for a finding's detail line."""
    return ", ".join(f"`{v}`" for v in sorted(values)) or "(none)"


def check_test_count(facts: RepoFacts, claims: Claims) -> list[Finding]:
    """The stated test total must match what pytest actually collects."""
    if facts.test_count is None or claims.test_count is None:
        return []
    if facts.test_count == claims.test_count:
        return []
    return [
        Finding(
            check="docs.test-count",
            severity=Severity.HIGH,
            message=f"{GUIDE} states {claims.test_count} tests; pytest collects {facts.test_count}",
            detail="The stated total is the bar a change is told to clear, so a stale number "
            "misleads every contributor who checks their run against it.",
            location=GUIDE,
        )
    ]


def check_subcommands(facts: RepoFacts, claims: Claims) -> list[Finding]:
    """Documented subcommands and real subcommands must be the same set."""
    real = {s.name for s in facts.subcommands}
    documented = {c.name for c in claims.cli}
    findings: list[Finding] = []
    if missing := real - documented:
        findings.append(
            Finding(
                check="cli.subcommand-set",
                severity=Severity.HIGH,
                message="CLI subcommands exist that the guide does not document",
                detail=_fmt(missing),
                location=GUIDE,
            )
        )
    if phantom := documented - real:
        findings.append(
            Finding(
                check="cli.subcommand-set",
                severity=Severity.HIGH,
                message="The guide documents CLI subcommands that do not exist",
                detail=_fmt(phantom),
                location=GUIDE,
            )
        )
    if claims.subcommand_count is not None and claims.subcommand_count != len(real):
        findings.append(
            Finding(
                check="cli.subcommand-count",
                severity=Severity.MEDIUM,
                message=f"The guide says {claims.subcommand_count} subcommands; there are {len(real)}",
                location=GUIDE,
            )
        )
    return findings


def check_cli_flags(facts: RepoFacts, claims: Claims) -> list[Finding]:
    """Every real flag must be documented, and every documented flag must be real."""
    findings: list[Finding] = []
    for claim in claims.cli:
        subcommand = facts.subcommand(claim.name)
        if subcommand is None:
            continue
        real = set(subcommand.flag_names)
        if missing := real - claim.flags:
            findings.append(
                Finding(
                    check="cli.flags",
                    severity=Severity.MEDIUM,
                    message=f"`amf {claim.name}` accepts flags the guide does not show",
                    detail=_fmt(missing),
                    location=f"{GUIDE}:{claim.line}",
                )
            )
        if phantom := claim.flags - real:
            findings.append(
                Finding(
                    check="cli.flags",
                    severity=Severity.MEDIUM,
                    message=f"The guide shows flags `amf {claim.name}` does not accept",
                    detail=_fmt(phantom),
                    location=f"{GUIDE}:{claim.line}",
                )
            )
    return findings


def check_cli_docstring(facts: RepoFacts, _claims: Claims) -> list[Finding]:
    """``cli.py``'s own docstring must name every subcommand it builds."""
    real = {s.name for s in facts.subcommands}
    if not real or not facts.cli_docstring_commands:
        return []
    missing = real - set(facts.cli_docstring_commands)
    if not missing:
        return []
    return [
        Finding(
            check="cli.docstring-commands",
            severity=Severity.LOW,
            message="`cli.py`'s module docstring omits subcommands it defines",
            detail=_fmt(missing),
            location="src/amf/cli.py",
        )
    ]


def check_modules(facts: RepoFacts, claims: Claims) -> list[Finding]:
    """The architecture table must list exactly the package's modules."""
    real = set(facts.modules)
    documented = set(claims.module_rows)
    findings: list[Finding] = []
    if missing := real - documented:
        findings.append(
            Finding(
                check="modules.table",
                severity=Severity.MEDIUM,
                message="Package modules are missing from the architecture table",
                detail=_fmt(missing),
                location=GUIDE,
            )
        )
    if phantom := documented - real:
        findings.append(
            Finding(
                check="modules.table",
                severity=Severity.MEDIUM,
                message="The architecture table lists modules that do not exist",
                detail=_fmt(phantom),
                location=GUIDE,
            )
        )
    return findings


def check_exceptions(facts: RepoFacts, claims: Claims) -> list[Finding]:
    """The documented exception hierarchy must match ``errors.py``."""
    real = set(facts.exceptions)
    documented = set(claims.exception_names)
    findings: list[Finding] = []
    if not documented:
        return findings
    if missing := real - documented:
        findings.append(
            Finding(
                check="errors.list",
                severity=Severity.MEDIUM,
                message="`errors.py` defines exceptions the guide does not list",
                detail=_fmt(missing),
                location=GUIDE,
            )
        )
    if phantom := documented - real:
        findings.append(
            Finding(
                check="errors.list",
                severity=Severity.MEDIUM,
                message="The guide lists exceptions `errors.py` does not define",
                detail=_fmt(phantom),
                location=GUIDE,
            )
        )
    stray = {name for name, base in facts.exceptions.items() if name != "AMFError" and base != "AMFError"}
    if stray:
        findings.append(
            Finding(
                check="errors.hierarchy",
                severity=Severity.HIGH,
                message="Exceptions do not derive from `AMFError`",
                detail=_fmt(stray),
                location="src/amf/errors.py",
            )
        )
    return findings


def check_version_sync(facts: RepoFacts, _claims: Claims) -> list[Finding]:
    """``__version__`` and the packaging version must agree."""
    if not facts.package_version or not facts.pyproject_version:
        return []
    if facts.package_version == facts.pyproject_version:
        return []
    return [
        Finding(
            check="version.sync",
            severity=Severity.HIGH,
            message=f"`__version__` is {facts.package_version} but pyproject says {facts.pyproject_version}",
            location="src/amf/__init__.py",
        )
    ]


def check_config_defaults(facts: RepoFacts, claims: Claims) -> list[Finding]:
    """Defaults stated in prose must match the dataclass field defaults."""
    findings: list[Finding] = []
    for name, stated in sorted(claims.config_defaults.items()):
        info = facts.dataclasses.get(name)
        if info is None:
            continue
        fields = info["fields"]
        for key, value in sorted(stated.items()):
            if key not in fields:
                findings.append(
                    Finding(
                        check="config.defaults",
                        severity=Severity.MEDIUM,
                        message=f"The guide documents `{name}.{key}`, which has no such field default",
                        location=GUIDE,
                    )
                )
            elif fields[key] != value:
                findings.append(
                    Finding(
                        check="config.defaults",
                        severity=Severity.HIGH,
                        message=f"`{name}.{key}` is {fields[key]!r} but the guide says {value!r}",
                        location=GUIDE,
                    )
                )
    return findings


def check_named_constants(facts: RepoFacts, claims: Claims) -> list[Finding]:
    """Constants quoted inline must match the source."""
    findings: list[Finding] = []
    for name, stated in sorted(claims.named_constants.items()):
        matches = {k: v for k, v in facts.constants.items() if k.rsplit(".", 1)[-1] == name}
        for key, actual in sorted(matches.items()):
            if actual != stated:
                findings.append(
                    Finding(
                        check="constants.named",
                        severity=Severity.HIGH,
                        message=f"`{name}` is {actual!r} but the guide says {stated!r}",
                        location=f"src/amf/{key.split('.')[0]}.py",
                    )
                )
    return findings


def check_docs_mentioned(facts: RepoFacts, claims: Claims) -> list[Finding]:
    """Every prose document must be accounted for in the guide.

    This is the inverse direction, and it is the one that catches a document being added
    without the guide's "what is authoritative" section being updated to place it.
    """
    orphans = [d for d in facts.doc_files if not claims.mentions(d)]
    if not orphans:
        return []
    return [
        Finding(
            check="docs.mentioned",
            severity=Severity.MEDIUM,
            message="Documents under `docs/` are not mentioned anywhere in the guide",
            detail=_fmt(orphans),
            location=GUIDE,
        )
    ]


def check_examples_mentioned(facts: RepoFacts, claims: Claims) -> list[Finding]:
    """Every runnable example must be described in the guide."""
    orphans = [e for e in facts.examples if not claims.mentions(e)]
    if not orphans:
        return []
    return [
        Finding(
            check="examples.mentioned",
            severity=Severity.LOW,
            message="Example scripts are not mentioned in the guide",
            detail=_fmt(orphans),
            location=GUIDE,
        )
    ]


def check_layout(facts: RepoFacts, claims: Claims) -> list[Finding]:
    """Layout-block paths must exist, and real top-level entries must be mentioned."""
    findings: list[Finding] = []
    ghosts = [p for p in claims.layout_paths if not (facts.root / p).exists()]
    if ghosts:
        findings.append(
            Finding(
                check="layout.paths-exist",
                severity=Severity.MEDIUM,
                message="The repository layout block lists paths that do not exist",
                detail=_fmt(ghosts),
                location=GUIDE,
            )
        )
    unmentioned = []
    for name in facts.top_level:
        if name.startswith(".") or name == GUIDE:
            continue
        # A directory is referenced as a path (`tools/`); matching the bare word would let
        # ordinary prose such as "those tools" mask a genuinely undocumented directory.
        needle = f"{name}/" if (facts.root / name).is_dir() else name
        if not claims.mentions_path(needle):
            unmentioned.append(name)
    if unmentioned:
        findings.append(
            Finding(
                check="layout.top-level-mentioned",
                severity=Severity.LOW,
                message="Top-level entries are not mentioned anywhere in the guide",
                detail=_fmt(unmentioned),
                location=GUIDE,
            )
        )
    return findings


def check_ci(facts: RepoFacts, claims: Claims) -> list[Finding]:
    """Workflow inventory and the stated yamllint-directive count must hold."""
    findings: list[Finding] = []
    if claims.codeql_directives is not None and claims.codeql_directives != facts.codeql_disable_directives:
        findings.append(
            Finding(
                check="ci.codeql-directives",
                severity=Severity.MEDIUM,
                message=(
                    f"The guide says `codeql.yml` carries {claims.codeql_directives} "
                    f"yamllint disable-line directives; it carries {facts.codeql_disable_directives}"
                ),
                location=GUIDE,
            )
        )
    for workflow in facts.workflows:
        if not claims.mentions(workflow):
            findings.append(
                Finding(
                    check="ci.workflow-set",
                    severity=Severity.MEDIUM,
                    message=f"Workflow `{workflow}` is not mentioned in the guide",
                    location=GUIDE,
                )
            )
    banned = [w for w in facts.workflows if "conda" in w or "publish" in w or "release" in w]
    if banned:
        findings.append(
            Finding(
                check="ci.forbidden-workflow",
                severity=Severity.HIGH,
                message="A workflow the guide forbids has been added",
                detail=_fmt(banned),
                location=".github/workflows",
            )
        )
    return findings


def check_layering(facts: RepoFacts, _claims: Claims) -> list[Finding]:
    """No module below the rendering layer may import `report`, `viz` or `cli`."""
    findings: list[Finding] = []
    for name, module in sorted(facts.modules.items()):
        if name in _RENDERERS:
            continue
        if violations := module.imports & _RENDERERS:
            findings.append(
                Finding(
                    check="imports.layering",
                    severity=Severity.HIGH,
                    message=f"`{name}` imports from the rendering layer, breaking the one-way dependency order",
                    detail=_fmt(violations),
                    location=f"src/amf/{name}.py",
                )
            )
    return findings


def check_dead_links(facts: RepoFacts, _claims: Claims) -> list[Finding]:
    """No Markdown file may link to a relative target that does not exist."""
    return [
        Finding(
            check="links.dead",
            severity=Severity.HIGH,
            message=f"Dead relative link to `{dead.target}`",
            detail="CI's Markdown link check fails the `Validate metadata` job on this.",
            location=f"{dead.source}:{dead.line}",
        )
        for dead in find_dead_links(facts.root)
    ]


CHECKS: tuple[Callable[[RepoFacts, Claims], list[Finding]], ...] = (
    check_dead_links,
    check_test_count,
    check_subcommands,
    check_cli_flags,
    check_cli_docstring,
    check_modules,
    check_exceptions,
    check_version_sync,
    check_config_defaults,
    check_named_constants,
    check_docs_mentioned,
    check_examples_mentioned,
    check_layout,
    check_ci,
    check_layering,
)
"""Every check, in a fixed order. Findings are re-sorted canonically before output."""
