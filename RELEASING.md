# Releasing `amf` — private distribution only

`amf` is proprietary, all-rights-reserved software (see `LICENSE.txt`). It is
**never** published to a public package index. Uploading it to PyPI would invite
precisely the installation, redistribution, and use that its licence forbids.

This document is the release procedure. It is deliberately manual: there is no
publish workflow in `.github/workflows/`, and none should be added.

## What enforces this

| Mechanism | Where | What it stops |
|-----------|-------|---------------|
| `Private :: Do Not Upload` classifier | `pyproject.toml` | PyPI **rejects** the upload outright, so a stray `twine upload` fails instead of publishing. |
| `tests/unit/test_packaging.py` | test suite, run in CI | Fails if the classifier is dropped from the source config or from the built distribution, or if a public-index URL is added. |
| No publish workflow | `.github/workflows/` | Nothing can publish automatically on a tag or release. |

Note that the classifier is checked **in the built wheel**, not just in
`pyproject.toml` — PyPI reads the metadata from the distribution, so that is
where the guard has to hold.

## Distribution channels

Because the repository itself is public, **a GitHub Release asset is not a
private channel** — anything attached to a release, and any GitHub Actions
artifact, is downloadable by anyone. Do not use either to distribute builds.

Private distribution means one of:

- Sending the built wheel directly to a named, authorised recipient who has
  written permission from the author, or
- Hosting it on an access-controlled private index, or
- Having the recipient build from source under the terms of `LICENSE.txt`.

Whichever is used, the recipient's permission comes from the author in writing;
the licence grants nothing by default.

## Procedure

1. **Confirm the version.** `pyproject.toml`'s `version` and
   `src/amf/__init__.py`'s `__version__` must agree — `test_packaging.py`
   asserts this. `CITATION.cff`'s `version` tracks the *framework* release (1.0),
   not the package, and is intentionally different.

2. **Record the change.** Move the relevant `## [Unreleased]` entries in
   `CHANGELOG.md` under the new version heading.

3. **Run the full gate.**

   ```sh
   ruff check . && ruff format --check .
   mypy
   pytest
   sha256sum --check --strict SHA256SUMS
   ```

4. **Build.**

   ```sh
   python -m pip install build
   python -m build            # writes dist/amf-<version>-py3-none-any.whl and .tar.gz
   ```

5. **Verify the guard survived the build.** This is the step that matters:

   ```sh
   python - <<'EOF'
   import glob, zipfile
   whl = glob.glob("dist/*.whl")[0]
   meta = next(p for p in zipfile.Path(whl).iterdir() if p.name.endswith(".dist-info"))
   assert "Private :: Do Not Upload" in (meta / "METADATA").read_text(), (
       "private classifier missing from wheel"
   )
   print("ok:", whl)
   EOF
   ```

6. **Tag the commit** (annotated, so the release point is recorded in the repo
   even though the artifact is not):

   ```sh
   git tag -a v<version> -m "amf v<version>"
   git push origin v<version>
   ```

7. **Deliver the wheel privately** to the authorised recipient, per
   *Distribution channels* above. Do not attach it to a GitHub Release.

## Installing a private build

The recipient installs the wheel directly:

```sh
python -m pip install amf-<version>-py3-none-any.whl
```

Or, with source access, from a checkout:

```sh
python -m pip install .
```

## Versioning

The package version is independent of the AMF framework version. Because the
package's scores, thresholds, and weights are illustrative rather than
validated, treat any change to them as **user-visible** and record it in
`CHANGELOG.md`, even when the Python API is unchanged: a caller's numbers move
even though their code does not.
