# Author: Ethan Christensen <github: https://github.com/ethanlchristensen>

"""
256 Color formatting for bruhshell purposes
Format and logic behind some of the code follows
with that of termcolor, the ANSII Color formater
that suported around 8 colors total
"""

import os
from collections.abc import Sequence


VERSION = (0, 0, 65)

class bruhcolorwrapper(Sequence):
    """
    This class serves as a mean to wrap over the
    color coded text. Wrapping it allows us to
    get the length of a color coded text ignoring
    the escape sequences. It also allows us to create
    out own format methods so we can properly us the
    f-string in python with a bruhcolored text
    """

    def __init__(self, text: str, colored: str):
        self.text = text
        self.colored = colored
        super().__init__()

    def __len__(self):
        return len(self.text)

    def __str__(self):
        return self.colored

    def __format__(self, fmt: str):
        if fmt != "":
            if fmt[0] in ["<", ">", "^"]:
                spacing = int(fmt[1:])
                if fmt[0] == "<":  # left aligned
                    word_size = len(self.text)
                    return self.colored + (" " * (spacing - word_size))
                elif fmt[0] == ">":  # right aligned
                    word_size = len(self.text)
                    return (" " * (spacing - word_size)) + self.colored
                elif fmt[0] == "^":  # center aligned
                    word_size = len(self.text)
                    left_size = (spacing - word_size) // 2
                    right_size = (spacing - word_size) // 2
                    # If the spacing is odd, add the extra space to the right side
                    if (spacing - word_size) % 2 != 0:
                        right_size += 1
                    return (" " * left_size) + self.colored + (" " * right_size)
                    pass
            else:  # default left aligned
                spacing = int(fmt)
                word_size = len(self.text)
                return self.colored + (" " * (spacing - word_size))
        return self.colored

    def __add__(self, addition: any):
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
        else:
            print(
                f"ERROR: when trying to add, [{addition}] must be a string or bruhcolorwrapper"
            )

    def __mul__(self, val: int):
        tmp = self.copy()
        tmp.text *= val
        tmp.colored *= val
        return tmp

    def __getitem__(self, i: int):
        return self.text[i]

    def __contains__(self, value: any):
        return str(value) in self.text

    def copy(self):
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


def bruhcolored(
    text: str,
    color: int | str = None,
    on_color: int | str = None,
    attrs: list[str] = None,
):
    """
    desc:    Generates the properly escape sequenced string for the
             user inputeed text
    args:
             text     -> text to be escape sequenced
             color    -> the color code to color the text
             on_color -> the color to set the background
             attrs    -> list of other attributes to apply to the text
    returns: wrapper-object for the colored string
    """
    if not color and not on_color and not attrs:
        return bruhcolorwrapper(text=text, colored=text)

    color = str(color) if color else None
    on_color = str(on_color) if on_color else None
    color_mode = None
    on_color_mode = None

    if color in COLORS_256:
        color_mode = 256
    else:
        color_mode = 8

    if on_color in COLORS_256:
        on_color_mode = 256
    else:
        on_color_mode = 8

    text, orig_text = str(text), str(text)

    if os.getenv("ANSI_COLORS_DISABLED") is None:
        if color_mode == 256:
            if color is not None:
                if str(color) in COLORS_256:
                    text = COLORS_256[str(color)] + text
        else:
            if color is not None:
                if str(color) in COLORS_8:
                    text = COLORS_8[str(color)] + text
        if on_color_mode == 256:
            if on_color is not None:
                if str(on_color) in HIGHLIGHTS_256:
                    text = "\u001b[" + HIGHLIGHTS_256[str(on_color)] + text
        else:
            if on_color is not None:
                if str(on_color) in HIGHLIGHTS_8:
                    text = HIGHLIGHTS_8[str(on_color)] + text
        if color_mode == 256:
            if attrs is not None:
                for attr in attrs:
                    if attr in ATTRIBUTES:
                        text = "\u001b[" + str(ATTRIBUTES[attr]) + "m" + text
        else:
            if attrs is not None:
                for attr in attrs:
                    if attr in ATTRIBUTES:
                        text = "\033[" + str(ATTRIBUTES[attr]) + "m" + text

    return bruhcolorwrapper(orig_text, text + RESET_256)


def colors(support: str = "limited", on_color: int | str = "black"):
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


def color_codes(support: str = "limited"):
    if support == "full":
        print(list(range(256)))
    else:
        print(list(COLORS_8.keys()))


def valid_effects():
    print(list(ATTRIBUTES.keys()))
