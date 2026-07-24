# SPDX-License-Identifier: AGPL-3.0-only
"""Числові шкали — several identical number lines stacked to fill an A4 sheet.

Python port of the original ``number_line.R`` (base R graphics → matplotlib).
"""
from .base import new_page
from .schema import Field

FIELDS = (
    Field("min_val", "int", -20, {"uk": "Нижня межа", "en": "Lower bound"}, min=-1000, max=1000),
    Field("max_val", "int", 20, {"uk": "Верхня межа", "en": "Upper bound"}, min=-1000, max=1000),
    Field("step", "int", 1, {"uk": "Крок поділок", "en": "Tick step"}, min=1, max=100),
    Field("n_lines", "int", 7, {"uk": "Шкал на аркуші", "en": "Lines per sheet"}, min=1, max=15),
)


def build(min_val=-20, max_val=20, step=1, n_lines=7, lang="uk", **_):
    """Return a one-page list of Figures (landscape A4)."""
    # Guards: keep the range valid and the tick count sane regardless of input.
    min_val, max_val, step, n_lines = int(min_val), int(max_val), int(step), int(n_lines)
    if max_val <= min_val:
        max_val = min_val + 1
    step = max(1, step)
    n_lines = max(1, n_lines)
    span = max_val - min_val
    if span // step > 400:                       # avoid an unreadable/huge line
        step = -(-span // 400)                   # ceil division

    fig, ax = new_page(landscape=True, lang=lang)

    pad = max(1, step) * 2  # room for the arrowheads past the outermost numbers
    ax.set_xlim(min_val - pad, max_val + pad)
    ax.set_ylim(0, n_lines)

    ticks = range(min_val, max_val + 1, step)

    for i in range(1, n_lines + 1):
        yc = n_lines - i + 0.5  # centre of the i-th line, top → bottom
        _draw_one_line(ax, ticks, yc, pad)

    return [fig]


def _draw_one_line(ax, ticks, yc, pad):
    x0 = min(ticks)
    x1 = max(ticks)
    # main axis with an arrowhead on each end
    ax.annotate(
        "", xy=(x1 + pad, yc), xytext=(x0 - pad, yc),
        arrowprops=dict(arrowstyle="<->", lw=2.6, color="black"),
    )

    for t in ticks:
        is_zero = t == 0
        big = t % 5 == 0
        hlen = 0.16 if big else 0.09          # tick half-length (y units)
        lw = 3.0 if is_zero else (2.0 if big else 1.0)
        ax.plot([t, t], [yc - hlen, yc + hlen], color="black", lw=lw)

        size = 9 if (big or is_zero) else 7
        weight = "bold" if is_zero else "normal"
        ax.text(t, yc - 0.34, str(t), color="black",
                ha="center", va="center", fontsize=size, fontweight=weight)
