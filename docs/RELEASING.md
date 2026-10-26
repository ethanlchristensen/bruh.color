# Release process

Development uses Python 3.13 and uv 0.13.4. Install with
`python -m pip install uv==0.13.4`, then `uv sync --locked --python 3.13`.
The package supports Python >=3.10; the older interpreter is exercised by CI.

| Event | Checks | Publication |
| --- | --- | --- |
| PR into main / push to main | Lint, types, tests, README examples, archives and installed artifacts | None |
| Push matching `vMAJOR.MINOR.PATCH` | Validate tag/main ancestry; rerun CI on that exact commit | PyPI, then GitHub release |
| Dispatch Release with an existing tag | Same gates | Retry incomplete publication |

## Local preparation

```sh
uv run --locked python publish.py --check
uv run --locked python publish.py 0.0.66
uv run --locked python publish.py 0.0.66 --write
```

The first command checks the current version without bumping. The second only
previews. The third updates `[project].version` and `bruhcolor.__version__`,
refreshes uv.lock, then checks lint, types, tests, examples, freshly built wheel
and sdist contents and Twine metadata. VERSION is derived from __version__.
Use a new unpublished version; the example is not a claim about PyPI availability.
If a check fails after writing, changes remain reviewable. Fix them and retry
`--check`; do not bump again merely to rerun validation.

Commit/push/PR require `--write --commit`, then `--push`, then `--pr` explicitly.
Those flags require a clean feature branch and commit only both version files
and uv.lock. The helper never tags or publishes. Old archives in dist are never
used by the local check; CI starts with a fresh build/release directory.

Review and commit the intended changes including uv.lock, open a PR into main,
and wait for CI. After merging, wait for the main commit's checks. Then manually
tag that reviewed main commit and push the specific matching version tag. This
is the publication trigger. Never rewrite a published version or move its tag.

## GitHub and PyPI setup

Protect main with CI. Configure a `pypi` environment allowing version tags.
For Trusted Publishing, register the repository's actual owner/name, workflow
`release.yml`, and environment `pypi` in PyPI's bruhcolor publisher settings.
The checkout remote is FNBBDevs/bruhcolor; verify the current owner if transferring
the repository. Alternatively configure a project-scoped `PYPI_TOKEN` secret.
An existing token takes precedence; remove it to select OIDC/attestations.

Build/test jobs have read-only permissions. Only the publish job gets id-token
permission; it downloads verified artifacts and does not execute package code.
The GitHub release job gets contents write permission. Third-party Actions use
full commit SHAs aligned with bruhanimate's workflow pins. Refresh pins manually;
routine Dependabot version-update PRs are paused.

## Recovery and verification

For an interrupted release, rerun the workflow for the same existing tag. PyPI
skips already uploaded files; GitHub completes drafts and leaves published assets
intact. If uploaded contents are wrong, prepare a new version instead.

CI installs wheel and sdist separately and runs
`python -I scripts/check_installed.py` using the installed environment's Python,
not a syncing `uv run` command that could restore the editable checkout. Check
the publish and github-release jobs after tagging. Local/mock tests do not prove
GitHub environment permissions or PyPI credentials; those must be configured by
the maintainer. No account settings are changed by the helper.
