"""Validate source versions and the exact distributions selected for publishing."""

from __future__ import annotations

import argparse
import ast
import os
import re
import sys
import tarfile

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib
import zipfile
from email.parser import Parser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")
REQUIRED = {"__init__.py", "bruhcolor.py", "py.typed"}


def parse_version(value: str) -> tuple[int, int, int]:
    """Accept canonical stable MAJOR.MINOR.PATCH versions, rejecting suffixes."""
    if not VERSION.fullmatch(value):
        raise ValueError(f"Expected MAJOR.MINOR.PATCH without leading zeros: {value!r}")
    major, minor, patch = map(int, value.split("."))
    return major, minor, patch


def source_version(root: Path = ROOT) -> str:
    """Read TOML/AST without importing the package or optional device backends."""
    project = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
    version = project["project"]["version"]
    parse_version(version)
    tree = ast.parse((root / "bruhcolor/__init__.py").read_text(encoding="utf-8"))
    values = [
        ast.literal_eval(node.value)
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "__version__"
            for target in node.targets
        )
    ]
    if values != [version]:
        raise ValueError("pyproject.toml and bruhcolor.__version__ must agree exactly")
    return version


def _metadata(text: str, version: str) -> None:
    metadata = Parser().parsestr(text)
    if metadata["Name"] != "bruhcolor" or metadata["Version"] != version:
        raise ValueError(
            "Distribution metadata does not match the source package/version"
        )


def check_dist(directory: Path, version: str) -> None:
    """Require one wheel and sdist with matching metadata, public modules and types.

    Reject stale distributions and private development files. Inspect archives
    without extracting them, so validation cannot write archive-supplied paths.
    """
    parse_version(version)
    wheel_name = f"bruhcolor-{version}-py3-none-any.whl"
    sdist_name = f"bruhcolor-{version}.tar.gz"
    if {path.name for path in directory.iterdir() if path.is_file()} != {
        wheel_name,
        sdist_name,
    }:
        raise ValueError(
            "Publish directory must contain exactly this version's wheel and sdist"
        )
    with zipfile.ZipFile(directory / wheel_name) as archive:
        names = set(archive.namelist())
        _metadata(
            archive.read(f"bruhcolor-{version}.dist-info/METADATA").decode(), version
        )
        if not {f"bruhcolor/{name}" for name in REQUIRED} <= names:
            raise ValueError("Wheel is missing a public module or the py.typed marker")
        _check_names(names)
    with tarfile.open(directory / sdist_name) as archive:
        names = set(archive.getnames())
        prefix = f"bruhcolor-{version}/"
        member = archive.extractfile(prefix + "PKG-INFO")
        if member is None:
            raise ValueError("Source distribution has no package metadata")
        _metadata(member.read().decode(), version)
        if not {prefix + f"bruhcolor/{name}" for name in REQUIRED} <= names:
            raise ValueError(
                "Source distribution is missing a public module or type marker"
            )
        _check_names(names)


def _check_names(names: set[str]) -> None:
    for name in names:
        parts = set(name.split("/"))
        if parts & {
            ".git",
            ".env",
            ".codegraph",
            ".venv",
            "api.txt",
            "publish.ps1",
            "push_version.py",
        }:
            raise ValueError(
                f"Unexpected private distribution path: {name}"
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tag", help="Require a matching vMAJOR.MINOR.PATCH release tag"
    )
    parser.add_argument(
        "--dist", type=Path, help="Validate the selected distribution directory"
    )
    parser.add_argument(
        "--github-output",
        action="store_true",
        help="Append validated version to GITHUB_OUTPUT",
    )
    args = parser.parse_args(argv)
    version = source_version()
    if args.tag is not None and args.tag != f"v{version}":
        raise ValueError(f"Release tag must be v{version}, got {args.tag!r}")
    if args.dist is not None:
        check_dist(args.dist, version)
    if args.github_output:
        with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as output:
            output.write(f"version={version}\n")
    print(f"Verified bruhcolor {version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
