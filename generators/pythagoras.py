# SPDX-License-Identifier: AGPL-3.0-only
"""Таблиця Піфагора — the multiplication table, filled and/or blank.

Python port of ``pythagoras_table.R``.
"""
from .base import new_page
from .schema import Field
from ..i18n import gen_labels

FIELDS = (
    Field("n_min", "int", 1, {"uk": "Від", "en": "From"}, min=1, max=20),
    Field("n_max", "int", 10, {"uk": "До", "en": "To"}, min=1, max=20),
    Field("mode", "select", "both", {"uk": "Версія", "en": "Version"},
          options=(("both", {"uk": "Обидві сторінки", "en": "Both pages"}),
                   ("blind", {"uk": "Сліпа (заповни сам)", "en": "Blank (fill in)"}),
                   ("full", {"uk": "Заповнена", "en": "Filled in"}))),
)


def build(n_min=1, n_max=10, mode="both", lang="uk", **_):
    """mode: "full" (filled), "blind" (blank), "both" (blank page then filled)."""
    n_min, n_max = int(n_min), int(n_max)
    if n_max < n_min:
        n_min, n_max = n_max, n_min
    factors = list(range(n_min, n_max + 1))
    lbl = gen_labels("pythagoras", lang)
    pages = {"full": [True], "blind": [False], "both": [False, True]}.get(mode, [False, True])
    return [_draw_table(factors, fill, lbl) for fill in pages]


def _draw_table(factors, fill, lbl):
    fig, ax = new_page(landscape=False)
    n = len(factors)

    ax.text(0.5, 0.965, lbl["sheet_title"], ha="center", va="center", fontsize=17, fontweight="bold")
    sub = lbl["filled"] if fill else lbl["blank"]
    ax.text(0.5, 0.925, sub, ha="center", va="center", fontsize=12, color="0.3")

    # square block of (N+1)×(N+1) cells including the header row/column
    side = 0.86
    x0 = 0.5 - side / 2
    y1 = 0.90
    cw = side / (n + 1)
    ch = side / (n + 1)
    y0 = y1 - side

    for k in range(n + 2):
        lw = 2 if k <= 1 else 1
        ax.plot([x0 + k * cw, x0 + k * cw], [y0, y1], color="0.3", lw=lw)
        ax.plot([x0, x0 + side], [y1 - k * ch, y1 - k * ch], color="0.3", lw=lw)

    def centre(col, row):
        return x0 + (col + 0.5) * cw, y1 - (row + 0.5) * ch

    cx, cy = centre(0, 0)
    ax.text(cx, cy, "×", ha="center", va="center", fontsize=15, fontweight="bold")

    for j, f in enumerate(factors, start=1):
        tx, ty = centre(j, 0)
        ax.text(tx, ty, str(f), ha="center", va="center", fontsize=12, fontweight="bold")
        lx, ly = centre(0, j)
        ax.text(lx, ly, str(f), ha="center", va="center", fontsize=12, fontweight="bold")

    if fill:
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                px, py = centre(j, i)
                ax.text(px, py, str(factors[i - 1] * factors[j - 1]),
                        ha="center", va="center", fontsize=11)

    return fig
