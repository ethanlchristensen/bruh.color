# Author: Ethan Christensen <github: https://github.com/ethanlchristensen>

"""
256 Color formatting for bruhshell purposes
Format and logic behind some of the code follows
with that of termcolor, the ANSII Color formater
that suported around 8 colors total
"""

from __future__ import annotations

import os
import re
from collections.abc import Sequence
from typing import overload

from . import __version__

VERSION = tuple(map(int, __version__.split(".")))


class bruhcolorwrapper(Sequence[str]):
    """
    This class serves as a mean to wrap over the
    color coded text. Wrapping it allows us to
    get the length of a color coded text ignoring
    the escape sequences. It also allows us to create
    out own format methods so we can properly us the
    f-string in python with a bruhcolored text
    """

    def __init__(self, text: str, colored: str) -> None:
        self.text = text
        self.colored = colored
        super().__init__()

    def __len__(self) -> int:
        return len(self.text)

    def __str__(self) -> str:
        return self.colored

    def __format__(self, fmt: str) -> str:
        """Python string alignment, fill, width, precision and optional s type.

        Width/precision count Python characters, not terminal display cells.
        Precision preserves SGR spans and resets styling before padding.
        """
        format(self.text, fmt)  # Let Python reject unsupported string formats.
        match = re.fullmatch(
            r"(?:(.)([<^>])|([<^>]))?(0?)([0-9]*)(?:\.([0-9]+))?s?", fmt, re.DOTALL
        )
        if match is None:
            raise ValueError(f"Unsupported string format: {fmt!r}")
        fill, explicit_align, align, zero, width, precision = match.groups()
        fill = fill or ("0" if zero else " ")
        align = explicit_align or align or "<"
        count = (
            min(len(self.text), int(precision))
            if precision is not None
            else len(self.text)
        )
        styled = (
            _truncate(self.colored, count) if count < len(self.text) else self.colored
        )
        padding = max(0, int(width or 0) - count)
        left = padding if align == ">" else padding // 2 if align == "^" else 0
        return fill * left + styled + fill * (padding - left)

    def __add__(self, addition: str | bruhcolorwrapper) -> bruhcolorwrapper:
        if isinstance(addition, str):
            tmp = self.copy()
            tmp.text += str(addition)
            tmp.colored += str(addition)
            return tmp
        elif isinstance(addition, bruhcolorwrapper):
            tmp = self.copy()
            tmp.text += addition.text
            tmp.colored += addition.colored
            return tmp
        return NotImplemented

    def __mul__(self, val: int) -> bruhcolorwrapper:
        tmp = self.copy()
        tmp.text *= val
        tmp.colored *= val
        return tmp

    @overload
    def __getitem__(self, i: int) -> str: ...

    @overload
    def __getitem__(self, i: slice) -> str: ...

    def __getitem__(self, i: int | slice) -> str:
        return self.text[i]

    def __contains__(self, value: object) -> bool:
        return str(value) in self.text

    def copy(self) -> bruhcolorwrapper:
        text = self.text
        colored = self.colored
        return bruhcolorwrapper(text=text, colored=colored)


__AVAILABLE_COMMANDS__ = ["bruhcolored", "colors", "color_codes", "valid_effects"]

# GENERATE THE 256 COLORS -> [38;5;#m for color
COLORS_256 = {}
for i in range(16):
    for j in range(16):
        code = str(i * 16 + j)
        COLORS_256[code] = "\033[38;5;" + code + "m"

# GENERATE THE 17 COLORS
COLORS_8 = {
    "black": "\033[30m",
    "grey": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "light_grey": "\033[37m",
    "dark_grey": "\033[90m",
    "light_red": "\033[91m",
    "light_green": "\033[92m",
    "light_yellow": "\033[93m",
    "light_blue": "\033[94m",
    "light_magenta": "\033[95m",
    "light_cyan": "\033[96m",
    "white": "\033[97m",
}

VALID_COLORS_8_NAMES = list(COLORS_8.keys())

# GENERATE THE 17 BACKGROUND COLORS
HIGHLIGHTS_8 = {
    "black": "\033[40m",
    "grey": "\033[40m",
    "red": "\033[41m",
    "green": "\033[42m",
    "yellow": "\033[43m",
    "blue": "\033[44m",
    "magenta": "\033[45m",
    "cyan": "\033[46m",
    "light_grey": "\033[47m",
    "dark_grey": "\033[100m",
    "light_red": "\033[101m",
    "light_green": "\033[102m",
    "light_yellow": "\033[103m",
    "light_blue": "\033[104m",
    "light_magenta": "\033[105m",
    "light_cyan": "\033[106m",
    "white": "\033[107m",
}

VALID_HIGHLIGHTS_8_NAMES = list(HIGHLIGHTS_8.keys())

# GENERATE THE 256 BACKGROUND COLORS -> [48;5;#m for backgrounf
HIGHLIGHTS_256 = {}
for i in range(16):
    for j in range(16):
        code = str(i * 16 + j)
        HIGHLIGHTS_256[code] = "\033[48;5;" + code + "m"

# Possible attributes
ATTRIBUTES = {
    "bold": 1,
    "dark": 2,
    "italic": 3,
    "underline": 4,
    "blink": 5,
    "reverse": 7,
    "concealed": 8,
    "crossed-out": 9,
}

# Reset token to restore orginal formatting
RESET_256 = "\u001b[0m"
RESET_8 = "\033[0m"


_SGR = re.compile(r"\x1b\[[0-9;:]*m")
Color = int | str | tuple[int, int, int]


def _truncate(styled: str, count: int) -> str:
    if count == 0:
        return ""
    position = visible = 0
    while position < len(styled) and visible < count:
        match = _SGR.match(styled, position)
        if match:
            position = match.end()
        else:
            position += 1
            visible += 1
    result = styled[:position]
    return result + (RESET_256 if "\x1b[" in result else "")


def _color_escape(value: Color, *, background: bool = False) -> str:
    channel = 48 if background else 38
    if isinstance(value, str) and value.startswith("#"):
        if not re.fullmatch(r"#[0-9a-fA-F]{6}", value):
            raise ValueError("Hex colors must be #RRGGBB")
        value = (int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16))
    if isinstance(value, tuple):
        if len(value) != 3 or any(
            type(part) is not int or not 0 <= part <= 255 for part in value
        ):
            raise ValueError("RGB colors require three integer channels in 0..255")
        return f"\x1b[{channel};2;{value[0]};{value[1]};{value[2]}m"
    palette, names = (
        (HIGHLIGHTS_256, HIGHLIGHTS_8) if background else (COLORS_256, COLORS_8)
    )
    return palette.get(str(value), names.get(str(value), ""))


def bruhcolored(
    text: object,
    color: Color | None = None,
    on_color: Color | None = None,
    attrs: Sequence[str] | None = None,
    *,
    enabled: bool | None = None,
) -> bruhcolorwrapper:
    """Format text with named/indexed, #RRGGBB or (r, g, b) colors.

    Index zero is black. Unknown colors/attributes are ignored for compatibility.
    enabled overrides environment policy. Otherwise ANSI_COLORS_DISABLED (when
    present) or nonempty NO_COLOR disables styling. No terminal probing occurs. The
    wrapper's length/indexing refer to plain Python characters, not display cells.
    This function does not inspect a terminal, print, or open external resources.
    """
    original = str(text)
    if enabled is not None and type(enabled) is not bool:
        raise TypeError("enabled must be bool or None")
    if enabled is False or (
        enabled is None
        and ("ANSI_COLORS_DISABLED" in os.environ or bool(os.getenv("NO_COLOR")))
    ):
        return bruhcolorwrapper(original, original)
    if color is None and on_color is None and not attrs:
        return bruhcolorwrapper(original, original)
    styled = original
    if color is not None:
        styled = _color_escape(color) + styled
    if on_color is not None:
        styled = _color_escape(on_color, background=True) + styled
    for attr in attrs or ():
        if attr in ATTRIBUTES:
            styled = f"\x1b[{ATTRIBUTES[attr]}m" + styled
    return bruhcolorwrapper(original, styled + RESET_256)


def colors(support: str = "limited", on_color: int | str = "black") -> None:
    """
    desc:    prints out all of the colors supported
    args:    None
    returns: None
    """
    if support == "full":
        for i in range(0, len(COLORS_256), 16):
            for j in range(i, i + 16):
                c = bruhcolored(
                    (" " * (4 - len(str(j)))) + (str(j)), color=j, on_color=on_color
                )
                print(f"{c}", end="")
            print()
    else:
        for i, color in enumerate(list(COLORS_8)):
            c = bruhcolored(f"{color:^20s}", color=color, on_color=on_color)
            if i != 0 and i % 2 == 0:
                print()
                print(c, end="")
            else:
                print(c, end="")
        print()


def color_codes(support: str = "limited") -> None:
    if support == "full":
        print(list(range(256)))
    else:
        print(list(COLORS_8.keys()))


def valid_effects() -> None:
    print(list(ATTRIBUTES.keys()))
