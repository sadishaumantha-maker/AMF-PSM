"""Mutation corpus: one defect at a time, each caught by exactly the right check."""

from __future__ import annotations

import pytest
from tools.docsync.drift import scan
from tools.docsync.model import Severity


def checks_fired(root):
    return sorted({f.check for f in scan(root, with_test_count=False).findings})


def test_clean_repo_is_silent(mini_repo):
    """The baseline must produce no findings at all -- the anti-false-positive anchor."""
    report = scan(mini_repo, with_test_count=False)
    assert report.findings == (), [f.to_dict() for f in report.findings]


def test_clean_repo_reports_test_count_as_skipped_not_guessed(mini_repo):
    report = scan(mini_repo, with_test_count=False)
    assert "docs.test-count" in report.skipped


# --- each mutation below introduces exactly one defect ------------------------------


def test_undocumented_flag_is_caught(mini_repo, guide_editor):
    guide_editor("amf alpha  source [--depth 3] [--format text|json]", "amf alpha  source [--format text|json]")
    assert checks_fired(mini_repo) == ["cli.flags"]


def test_phantom_flag_is_caught(mini_repo, guide_editor):
    guide_editor("[--depth 3] [--format text|json]", "[--depth 3] [--format text|json] [--nonesuch]")
    assert checks_fired(mini_repo) == ["cli.flags"]


def test_undocumented_subcommand_is_caught(mini_repo):
    cli = mini_repo / "src/amf/cli.py"
    cli.write_text(
        cli.read_text().replace(
            '    b = sub.add_parser("beta")',
            '    g = sub.add_parser("gamma")\n    _add_format(g)\n\n    b = sub.add_parser("beta")',
        ),
        encoding="utf-8",
    )
    fired = checks_fired(mini_repo)
    assert "cli.subcommand-set" in fired
    assert "cli.subcommand-count" in fired


def test_stale_subcommand_count_is_caught(mini_repo, guide_editor):
    guide_editor("offers two subcommands", "offers three subcommands")
    assert checks_fired(mini_repo) == ["cli.subcommand-count"]


def test_new_module_missing_from_table_is_caught(mini_repo):
    (mini_repo / "src/amf/extra.py").write_text('"""Extra."""\n', encoding="utf-8")
    assert checks_fired(mini_repo) == ["modules.table"]


def test_table_row_for_absent_module_is_caught(mini_repo, guide_editor):
    guide_editor("| `engine.py` | The engine. |", "| `engine.py` | The engine. |\n| `ghost.py` | Nothing. |")
    assert checks_fired(mini_repo) == ["modules.table"]


def test_undocumented_exception_is_caught(mini_repo):
    errors = mini_repo / "src/amf/errors.py"
    errors.write_text(errors.read_text() + '\n\nclass LateError(AMFError):\n    """Late."""\n', encoding="utf-8")
    assert checks_fired(mini_repo) == ["errors.list"]


def test_exception_outside_the_hierarchy_is_caught(mini_repo, guide_editor):
    errors = mini_repo / "src/amf/errors.py"
    errors.write_text(errors.read_text() + '\n\nclass RogueError(ValueError):\n    """Rogue."""\n', encoding="utf-8")
    guide_editor("`AMFError`, `InvalidSystemError`.", "`AMFError`, `InvalidSystemError`, `RogueError`.")
    assert checks_fired(mini_repo) == ["errors.hierarchy"]


def test_version_skew_is_caught(mini_repo):
    pyproject = mini_repo / "pyproject.toml"
    pyproject.write_text(pyproject.read_text().replace('version = "0.1.0"', 'version = "0.2.0"'), encoding="utf-8")
    assert checks_fired(mini_repo) == ["version.sync"]


def test_unmentioned_doc_is_caught(mini_repo):
    (mini_repo / "docs/orphan.md").write_text("# Orphan\n", encoding="utf-8")
    assert checks_fired(mini_repo) == ["docs.mentioned"]


def test_unmentioned_example_is_caught(mini_repo):
    (mini_repo / "examples/lonely.py").write_text("print('x')\n", encoding="utf-8")
    assert checks_fired(mini_repo) == ["examples.mentioned"]


def test_layout_path_that_does_not_exist_is_caught(mini_repo, guide_editor):
    guide_editor("docs/               prose", "docs/               prose\nnowhere/            missing")
    assert checks_fired(mini_repo) == ["layout.paths-exist"]


def test_stale_codeql_directive_count_is_caught(mini_repo):
    codeql = mini_repo / ".github/workflows/codeql.yml"
    codeql.write_text("# yamllint disable-line rule:line-length\n" + codeql.read_text(), encoding="utf-8")
    assert checks_fired(mini_repo) == ["ci.codeql-directives"]


def test_unmentioned_workflow_is_caught(mini_repo):
    (mini_repo / ".github/workflows/extra.yml").write_text("name: Extra\n", encoding="utf-8")
    assert checks_fired(mini_repo) == ["ci.workflow-set"]


def test_forbidden_publish_workflow_is_caught(mini_repo, guide_editor):
    (mini_repo / ".github/workflows/publish.yml").write_text("name: Publish\n", encoding="utf-8")
    guide_editor("`ci.yml` and `codeql.yml`.", "`ci.yml`, `codeql.yml` and `publish.yml`.")
    fired = checks_fired(mini_repo)
    assert fired == ["ci.forbidden-workflow"]


def test_layering_violation_is_caught(mini_repo):
    engine = mini_repo / "src/amf/engine.py"
    engine.write_text(
        engine.read_text().replace(
            "from amf.errors import AMFError",
            "from amf.cli import _build_parser\nfrom amf.errors import AMFError",
        ),
        encoding="utf-8",
    )
    assert "imports.layering" in checks_fired(mini_repo)


def test_dead_relative_link_is_caught(mini_repo):
    (mini_repo / "docs/guide.md").write_text("# Guide\n\nSee [gone](gone.md).\n", encoding="utf-8")
    report = scan(mini_repo, with_test_count=False)
    assert [f.check for f in report.findings] == ["links.dead"]
    assert report.findings[0].severity is Severity.HIGH
    assert report.findings[0].location == "docs/guide.md:3"


def test_cli_docstring_that_omits_a_subcommand_is_caught(mini_repo):
    cli = mini_repo / "src/amf/cli.py"
    cli.write_text(
        cli.read_text().replace("Exposes ``alpha`` and ``beta`` subcommands.", "Exposes ``alpha``."),
        encoding="utf-8",
    )
    assert checks_fired(mini_repo) == ["cli.docstring-commands"]


@pytest.mark.parametrize("stated", ["0.5", "0.9"])
def test_config_default_mismatch_is_caught(mini_repo, guide_editor, stated):
    engine = mini_repo / "src/amf/engine.py"
    engine.write_text(
        '"""Engine."""\n\nfrom dataclasses import dataclass\n\nfrom amf.errors import AMFError\n\n'
        '__all__ = ["AMFError"]\n\n\n@dataclass(frozen=True, slots=True)\nclass DemoConfig:\n'
        '    """Config."""\n\n    ratio: float = 0.25\n',
        encoding="utf-8",
    )
    guide_editor("## CI", f"`DemoConfig` defaults: `ratio={stated}`.\n\n## CI")
    findings = scan(mini_repo, with_test_count=False).findings
    assert [f.check for f in findings] == ["config.defaults"]
    assert "0.25" in findings[0].message


def test_undocumented_top_level_directory_is_caught(mini_repo):
    (mini_repo / "newdir").mkdir()
    (mini_repo / "newdir" / "thing.py").write_text("x = 1\n", encoding="utf-8")
    assert checks_fired(mini_repo) == ["layout.top-level-mentioned"]


def test_a_different_directorys_name_does_not_satisfy_the_mention(mini_repo, guide_editor):
    """Regression: `tests/tools/` must not count as documenting a top-level `tools/`."""
    (mini_repo / "tools").mkdir()
    (mini_repo / "tools" / "thing.py").write_text("x = 1\n", encoding="utf-8")
    guide_editor("docs/               prose", "docs/               prose\ndeeply/tools/       unrelated")
    fired = checks_fired(mini_repo)
    assert "layout.top-level-mentioned" in fired


def test_prose_containing_the_bare_word_does_not_satisfy_the_mention(mini_repo, guide_editor):
    """Regression: prose like "do not add those tools" must not document a `tools/` directory."""
    (mini_repo / "tools").mkdir()
    (mini_repo / "tools" / "thing.py").write_text("x = 1\n", encoding="utf-8")
    guide_editor("## Docs", "Do not add those tools or files.\n\n## Docs")
    assert "layout.top-level-mentioned" in checks_fired(mini_repo)


def test_properly_documented_directory_passes(mini_repo, guide_editor):
    (mini_repo / "tools").mkdir()
    (mini_repo / "tools" / "thing.py").write_text("x = 1\n", encoding="utf-8")
    guide_editor("docs/               prose", "docs/               prose\ntools/              helpers")
    assert checks_fired(mini_repo) == []
