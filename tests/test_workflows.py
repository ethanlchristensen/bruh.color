from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def workflow(name):
    return yaml.load(
        (ROOT / ".github/workflows" / name).read_text(), Loader=yaml.BaseLoader
    )


def test_release_checks_exact_main_commit_and_only_publishes_verified_artifact():
    release = workflow("release.yml")
    assert release["permissions"] == {"contents": "read"}
    verify = release["jobs"]["verify"]["steps"]
    assert any(
        "git merge-base --is-ancestor HEAD origin/main" in step.get("run", "")
        for step in verify
    )
    assert (
        release["jobs"]["checks"]["with"]["ref"] == "${{ needs.verify.outputs.commit }}"
    )
    publish = release["jobs"]["publish"]
    assert publish["needs"] == ["verify", "checks"]
    assert publish["permissions"]["id-token"] == "write"
    assert not any(
        "checkout@" in step.get("uses", "") or "run" in step
        for step in publish["steps"]
    )
    assert publish["steps"][0]["with"]["name"] == "python-dist"


def test_ci_checks_minimum_python_and_installed_artifacts_without_editable_sync():
    ci = workflow("test.yml")
    assert ci["permissions"] == {"contents": "read"}
    tests = ci["jobs"]["tests"]
    assert {"os": "ubuntu-latest", "python": "3.10"} in tests["strategy"]["matrix"][
        "include"
    ]
    assert any(
        "--python ${{ matrix.python }}" in step.get("run", "")
        for step in tests["steps"]
    )
    package = "\n".join(step.get("run", "") for step in ci["jobs"]["package"]["steps"])
    assert package.count(".venv/bin/python -I scripts/check_installed.py") == 2
    assert "--no-sources" in package
    assert "twine check --strict" in package


def test_external_actions_are_pinned_and_build_jobs_are_read_only():
    for name in ("test.yml", "release.yml"):
        for job in workflow(name)["jobs"].values():
            for step in job.get("steps", []):
                if "uses" in step:
                    pin = step["uses"].split("@")[1]
                    assert len(pin) == 40 and all(c in "0123456789abcdef" for c in pin)
    assert "permissions" not in workflow("test.yml")["jobs"]["package"]
