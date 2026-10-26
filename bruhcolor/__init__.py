"""Terminal formatting; importing opens no resources and writes no output."""

__version__ = "0.0.66"

from bruhcolor.bruhcolor import (
    ATTRIBUTES,
    COLORS_8,
    COLORS_256,
    HIGHLIGHTS_8,
    HIGHLIGHTS_256,
    RESET_8,
    RESET_256,
    VALID_COLORS_8_NAMES,
    VALID_HIGHLIGHTS_8_NAMES,
    VERSION,
    bruhcolored,
    bruhcolorwrapper,
    color_codes,
    colors,
    valid_effects,
)

__all__ = [
    "__version__",
    "ATTRIBUTES",
    "COLORS_8",
    "VALID_COLORS_8_NAMES",
    "COLORS_256",
    "HIGHLIGHTS_8",
    "VALID_HIGHLIGHTS_8_NAMES",
    "HIGHLIGHTS_256",
    "RESET_8",
    "RESET_256",
    "bruhcolored",
    "bruhcolorwrapper",
    "colors",
    "color_codes",
    "VERSION",
    "valid_effects",
]
