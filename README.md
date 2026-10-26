# bruhcolor

Named and 256-color terminal text formatting for Python. No runtime dependencies.
The companion formatter used by [bruhanimate](https://github.com/ethanlchristensen/bruh.animate).

Requires Python 3.10 or newer. Development uses Python 3.13 and uv 0.13.4.

```sh
python -m pip install bruhcolor
```

```python
from bruhcolor import bruhcolored

message = bruhcolored("Hello world!", color="red", on_color=194, attrs=["bold"])
print(message)
print(message.colored)  # ANSI string
print(message.text)     # original text
assert len(message) == 12
```

Foreground/background accept named colors or integers/numeric strings from 0
through 255, including zero (black). Named colors include black, red, green,
yellow, blue, magenta, cyan, light_grey, dark_grey, light_red, light_green,
light_yellow, light_blue, light_magenta, light_cyan and white; grey aliases black.
Attributes: bold, dark, italic, underline, blink, reverse, concealed, crossed-out.
Unknown colors/attributes are ignored for compatibility.

```python
from bruhcolor import bruhcolored, colors, color_codes, valid_effects

label = bruhcolored("Ready", color=46)
print(f"{label:>12}")
assert label[:2] == "Re"
assert (label + "!").text == "Ready!"
assert (label * 2).text == "ReadyReady"
color_codes()
valid_effects()
colors(support="full")
```

Alignment supports a width and optional `<`, `>` or `^`; length/indexing count
Python characters, not terminal display cells. Slices return plain strings.
Set `ANSI_COLORS_DISABLED` (any value) to disable all generated escape sequences.
Imports and formatting do not print or open a terminal; only discovery helpers print.

## Development

```sh
python -m pip install uv==0.13.4
uv sync --locked --python 3.13
uv run --locked ruff check .
uv run --locked mypy
uv run --locked pytest
uv run --locked python scripts/check_examples.py
uv run --locked python publish.py --check
```

`uv.lock` pins repository/CI environments. `poetry-core` is only the build backend;
the Poetry CLI is not used. The former `poetry.lock` is superseded by `uv.lock`.
The package keeps no runtime dependencies. CI covers Python 3.13 on Linux,
Windows and macOS, plus the minimum Python 3.10 on Linux.

## Releases

Develop on a feature/dev branch, merge reviewed changes into main, then explicitly
push a matching `vMAJOR.MINOR.PATCH` tag when ready to publish. Main pushes run
checks; they do not publish. See [the release guide](docs/RELEASING.md).

`publish.py` previews by default. `--check` validates the current version;
`--write` bumps source versions and refreshes the lockfile. Git writes require
additional explicit flags. The helper never creates a release tag or uploads.
Legacy ignored `publish.ps1`/`push_version.py` are not part of this workflow.

## Formatting corrections

The current working version fixes integer zero being treated as an absent color,
removes the duplicate escape prefix from indexed backgrounds, and emits no reset
when colors are disabled. Unsupported wrapper addition raises TypeError instead
of printing and returning None. Metadata now declares Python >=3.10, matching
the union annotations already used by the package. These corrections are covered
by regression tests; the existing version number has not been bumped or published.

## License

MIT. See [LICENSE](LICENSE) and retained upstream attribution in [COPYING.txt](COPYING.txt).

## RGB colors, color control, and formatting

`bruhcolored` accepts palette indexes/names, `#RRGGBB`, and `(r, g, b)` tuples.
RGB channels must be integers from 0 through 255. Invalid explicit hex/RGB values
raise `ValueError`; unknown legacy color names retain their existing behavior.

```python
from bruhcolor import bruhcolored

color = bruhcolored('hello', color='#66ccff', on_color=(12, 20, 30), enabled=True)
assert '38;2;102;204;255' in str(color)
assert format(bruhcolored('hello', enabled=False), '*^9.3s') == '***hel***'
```

Use `enabled=False` for plain output or `enabled=True` to explicitly enable color.
With `enabled=None` (the default), a present `ANSI_COLORS_DISABLED` or nonempty
`NO_COLOR` disables styling. There is no terminal probing or automatic RGB
fallback. Formatting supports Python string fill/alignment, width, precision and
optional `s`; precision preserves color spans and resets styling before padding.
Widths and precision count Python characters, not terminal display cells. Wide
and combining characters therefore need application-level display-width handling.
These additions are available starting with bruhcolor 0.0.67.
