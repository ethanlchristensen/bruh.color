import importlib
from unittest.mock import Mock

import pytest

from bruhcolor import (
    VERSION,
    __version__,
    bruhcolored,
    bruhcolorwrapper,
    color_codes,
    colors,
    valid_effects,
)


@pytest.fixture(autouse=True)
def color_environment(monkeypatch):
    monkeypatch.delenv("ANSI_COLORS_DISABLED", raising=False)


@pytest.mark.parametrize("index", range(256))
def test_every_palette_index_for_foreground_and_background(index):
    assert str(bruhcolored("x", color=index)) == f"\x1b[38;5;{index}mx\x1b[0m"
    assert str(bruhcolored("x", on_color=index)) == f"\x1b[48;5;{index}mx\x1b[0m"
    assert str(bruhcolored("x", color=str(index))) == str(bruhcolored("x", color=index))


def test_named_colors_attributes_and_combination():
    assert (
        str(bruhcolored("x", "red", "blue", ["bold", "underline"]))
        == "\x1b[4m\x1b[1m\x1b[44m\x1b[31mx\x1b[0m"
    )
    assert str(bruhcolored("x", "not-a-color", attrs=["unknown"])) == "x\x1b[0m"
    assert str(bruhcolored(123)) == "123"


def test_disabled_output_contains_no_escapes(monkeypatch):
    monkeypatch.setenv("ANSI_COLORS_DISABLED", "")
    assert str(bruhcolored("x", 0, 194, ["bold"])) == "x"


def test_wrapper_sequence_and_operations_do_not_mutate_original(capsys):
    value = bruhcolored("hi", "red")
    assert len(value) == 2 and value[0] == "h" and value[:] == "hi"
    assert "hi" in value and "z" not in value
    assert (value + "!").text == "hi!"
    assert (value + value).text == "hihi"
    assert (value * 3).text == "hihihi"
    assert value.text == "hi" and value.copy() is not value
    with pytest.raises(TypeError):
        value + 3
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    "spec,expected",
    [
        ("5", "hi   "),
        ("<5", "hi   "),
        (">5", "   hi"),
        ("^5", " hi  "),
        ("^1", "hi"),
        ("", "hi"),
    ],
)
def test_alignment_uses_plain_length(spec, expected):
    value = bruhcolorwrapper("hi", "hi")
    assert format(value, spec) == expected


def test_discovery_and_import_are_resource_free(monkeypatch, capsys):
    colors("full")
    colors()
    color_codes("full")
    color_codes()
    valid_effects()
    output = capsys.readouterr().out
    assert "255" in output and "red" in output and "bold" in output
    import os
    import threading

    monkeypatch.setattr(os, "system", Mock(side_effect=AssertionError("shell")))
    monkeypatch.setattr(
        threading.Thread, "start", Mock(side_effect=AssertionError("worker"))
    )
    import bruhcolor

    importlib.reload(bruhcolor)
    assert VERSION == tuple(map(int, __version__.split(".")))
    assert capsys.readouterr().out == ""
