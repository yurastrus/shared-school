# SPDX-License-Identifier: AGPL-3.0-only
"""Shared drawing helpers for worksheet generators.

Common rules for every generator (ported from the original R scripts):
  * page is A4;
  * strictly black-and-white (a mono laser printer is the target) — elements are
    distinguished by line weight/length and font weight, never by colour;
  * templates fill the sheet efficiently (little empty space);
  * Cyrillic + the glyphs ▲ ▼ → ← ○ ÷ × − ≤ ≥ render fine in DejaVu Sans.
"""
import io

import matplotlib
matplotlib.use("Agg")  # headless: no display, safe inside a web worker
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import rcParams  # noqa: E402
from matplotlib.backends.backend_pdf import PdfPages  # noqa: E402

# A4 in inches (210 × 297 mm).
A4_W_IN = 210 / 25.4
A4_H_IN = 297 / 25.4

# DejaVu Sans is matplotlib's bundled default and covers Ukrainian + the maths
# glyphs the worksheets use. Embed real TrueType outlines in the PDF (type 42)
# so print shops don't substitute fonts.
rcParams["font.family"] = "DejaVu Sans"
rcParams["pdf.fonttype"] = 42
rcParams["ps.fonttype"] = 42

# Unicode minus — matches the "−" used in the R originals (nicer than ASCII "-").
MINUS = "−"


def new_page(landscape=False, full_bleed=True, lang="uk"):
    """Return (fig, ax) for one A4 page with a unit [0,1]×[0,1] coordinate box.

    full_bleed keeps a tiny margin so strokes at the very edge are not clipped.
    Every page gets a small attribution stamped in the bottom-right corner.
    """
    from ..i18n import credit

    w, h = (A4_H_IN, A4_W_IN) if landscape else (A4_W_IN, A4_H_IN)
    fig = plt.figure(figsize=(w, h))
    margin = 0.012 if full_bleed else 0.0
    ax = fig.add_axes([margin, margin, 1 - 2 * margin, 1 - 2 * margin])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()
    # Subtle corner credit (figure coords → independent of the axes' data range).
    fig.text(0.992, 0.006, credit(lang), ha="right", va="bottom",
             fontsize=6, color="0.5")
    return fig, ax


def figures_to_pdf(figures):
    """Render one or more Figures into a single multi-page PDF (bytes)."""
    buf = io.BytesIO()
    with PdfPages(buf) as pdf:
        for fig in figures:
            pdf.savefig(fig)
    for fig in figures:
        plt.close(fig)
    return buf.getvalue()


def figure_to_png(fig, dpi=300):
    """Render a single Figure to PNG bytes at print resolution (A4 @ 300 dpi)."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi)
    plt.close(fig)
    return buf.getvalue()
