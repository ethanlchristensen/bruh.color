"""Run directly with the artifact environment's Python and -I."""

from importlib.metadata import version
from pathlib import Path


def main():
    import bruhcolor

    checkout = Path(__file__).resolve().parents[1] / "bruhcolor"
    installed = Path(bruhcolor.__file__).resolve()
    if installed.is_relative_to(checkout):
        raise RuntimeError("Imported checkout instead of installed distribution")
    assert version("bruhcolor") == bruhcolor.__version__
    assert bruhcolor.VERSION == tuple(map(int, bruhcolor.__version__.split(".")))
    assert (installed.parent / "py.typed").is_file()
    assert all(hasattr(bruhcolor, name) for name in bruhcolor.__all__)
    assert bruhcolor.bruhcolored("x", color=0).colored == "\x1b[38;5;0mx\x1b[0m"
    assert bruhcolor.bruhcolored("x", on_color=194).colored == "\x1b[48;5;194mx\x1b[0m"
    assert len(bruhcolor.bruhcolored("hello", color="red")) == 5
    print(f"Verified installed bruhcolor {bruhcolor.__version__}")


if __name__ == "__main__":
    main()
