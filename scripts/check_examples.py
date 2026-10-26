"""Execute standalone Python README examples; never run shell/release commands."""

import contextlib
import io
import re
from pathlib import Path


def main():
    readme = Path(__file__).resolve().parents[1] / "README.md"
    blocks = re.findall(
        r"```python\n(.*?)```", readme.read_text(encoding="utf-8"), re.S
    )
    for index, block in enumerate(blocks):
        with contextlib.redirect_stdout(io.StringIO()):
            exec(compile(block, f"README example {index + 1}", "exec"), {})
    print(f"Verified {len(blocks)} README examples")


if __name__ == "__main__":
    main()
