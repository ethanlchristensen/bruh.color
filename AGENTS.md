# Contributing to bruhcolor

Use Python 3.13 and uv 0.13.4 for development. Consumers support Python >=3.10.
Keep the package dependency-free. Imports/constructors/formatting must not print,
open terminals, start threads or run commands. Discovery helpers print explicitly.
Preserve named/indexed colors, wrapper plain-text length/slicing, and the
ANSI_COLORS_DISABLED override. Read the tests before changing formatting.

Run `uv sync --locked --python 3.13`, `uv run --locked ruff check .`,
`uv run --locked mypy`, `uv run --locked pytest`, and
`uv run --locked python scripts/check_examples.py`. Full release validation is
`uv run --locked python publish.py --check`. Keep uv.lock; refresh it for dependency
or package-version changes. Poetry CLI is not required.

Read docs/RELEASING.md before changing release behavior. Version metadata and
__version__ agree; VERSION is derived. Publication requires a matching main-branch
tag and exact-commit gates. Keep Actions pinned to full SHAs. Never print tokens.
Do not commit, push, tag or publish without user authorization. Preserve unrelated
work and upstream attribution. Keep .env, local indexes and build outputs ignored.
