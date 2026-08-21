"""Edge cases for the offline dead-relative-link scanner."""

from __future__ import annotations

import pytest
from tools.docsync.links import find_dead_links


def write(root, relative, text):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.mark.parametrize(
    "link",
    [
        "[x](https://example.com/gone.md)",
        "[x](http://example.com/gone.md)",
        "[x](mailto:someone@example.com)",
        "[x](#a-heading-in-this-file)",
    ],
)
def test_external_and_anchor_targets_are_ignored(tmp_path, link):
    write(tmp_path, "a.md", f"# A\n\n{link}\n")
    assert find_dead_links(tmp_path) == []


def test_existing_relative_target_is_accepted(tmp_path):
    write(tmp_path, "a.md", "[b](b.md)\n")
    write(tmp_path, "b.md", "# B\n")
    assert find_dead_links(tmp_path) == []


def test_fragment_is_stripped_before_the_existence_test(tmp_path):
    write(tmp_path, "a.md", "[b](b.md#section)\n")
    write(tmp_path, "b.md", "# B\n")
    assert find_dead_links(tmp_path) == []


def test_parent_relative_target_resolves_from_the_files_own_directory(tmp_path):
    write(tmp_path, "top.md", "# Top\n")
    write(tmp_path, "nested/a.md", "[top](../top.md)\n")
    assert find_dead_links(tmp_path) == []


def test_sibling_relative_target_does_not_resolve_from_the_repo_root(tmp_path):
    """The trap that broke `.github/RULESET-POLICY.md`: `./X.md` is relative to the file."""
    write(tmp_path, "top.md", "# Top\n")
    write(tmp_path, "nested/a.md", "[top](top.md)\n")
    dead = find_dead_links(tmp_path)
    assert [(d.source, d.target) for d in dead] == [("nested/a.md", "top.md")]


def test_missing_target_is_reported_with_its_line(tmp_path):
    write(tmp_path, "a.md", "# A\n\nintro\n\n[gone](gone.md)\n")
    dead = find_dead_links(tmp_path)
    assert len(dead) == 1
    assert dead[0].line == 5


def test_results_are_ordered_canonically(tmp_path):
    write(tmp_path, "z.md", "[q](q.md)\n")
    write(tmp_path, "a.md", "[y](y.md)\n[x](x.md)\n")
    dead = find_dead_links(tmp_path)
    assert [(d.source, d.line) for d in dead] == [("a.md", 1), ("a.md", 2), ("z.md", 1)]


def test_repeated_scans_are_identical(tmp_path):
    write(tmp_path, "a.md", "[gone](gone.md)\n")
    assert find_dead_links(tmp_path) == find_dead_links(tmp_path)


def test_vendored_directories_are_skipped(tmp_path):
    write(tmp_path, "node_modules/pkg/readme.md", "[gone](gone.md)\n")
    assert find_dead_links(tmp_path) == []


def test_unreadable_file_is_skipped_rather_than_crashing(tmp_path):
    write(tmp_path, "a.md", "[gone](gone.md)\n")
    (tmp_path / "b.md").mkdir()  # a directory named like a Markdown file
    assert len(find_dead_links(tmp_path)) == 1


def test_mentions_path_requires_a_boundary(tmp_path):
    from tools.docsync.claims import Claims

    claims = Claims(text="see tests/tools/ and also those tools everywhere")
    assert claims.mentions_path("tests/tools/")
    assert not claims.mentions_path("tools/")
    assert claims.mentions("tools/")  # the loose test is satisfied -- which is the bug
