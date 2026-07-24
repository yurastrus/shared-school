# SPDX-License-Identifier: AGPL-3.0-only
"""Приклади: додавання та віднімання — a randomised +/− worksheet.

Python port of ``arithmetic_worksheet.R``. Problems live in table cells (no
running numbering, which distracts a child) with a name/date header on top.
Negative results are allowed by default, consistent with the −20..20 number
line. A fresh random set is produced on each call unless ``seed`` is given.
"""
import random

from .base import new_page, MINUS
from .schema import Field
from ..i18n import gen_labels

FIELDS = (
    Field("operand_min", "int", 0, {"uk": "Нижня межа чисел", "en": "Lower bound"}, min=-1000, max=1000),
    Field("operand_max", "int", 20, {"uk": "Верхня межа чисел", "en": "Upper bound"}, min=-1000, max=1000),
    Field("n_problems", "int", 30, {"uk": "Кількість прикладів", "en": "Number of problems"}, min=1, max=90),
    Field("n_cols", "int", 3, {"uk": "Стовпців", "en": "Columns"}, min=1, max=5),
    Field("allow_add", "bool", True, {"uk": "Додавання (+)", "en": "Addition (+)"}),
    Field("allow_sub", "bool", True, {"uk": "Віднімання (−)", "en": "Subtraction (−)"}),
    Field("allow_negative_results", "bool", True,
          {"uk": "Дозволити від'ємні результати", "en": "Allow negative results"}),
    Field("include_answers", "bool", False,
          {"uk": "Додати сторінку відповідей", "en": "Include answer key"}),
)


def _make_problem(rng, ops, lo, hi, allow_negative):
    op = rng.choice(ops)
    a = rng.randint(lo, hi)
    b = rng.randint(lo, hi)
    if op == "-" and not allow_negative and a < b:
        a, b = b, a  # keep the result ≥ 0
    result = a + b if op == "+" else a - b
    op_sym = "+" if op == "+" else MINUS
    a_txt = f"({MINUS}{abs(a)})" if a < 0 else str(a)
    b_txt = f"({MINUS}{abs(b)})" if b < 0 else str(b)
    return {"text": f"{a_txt} {op_sym} {b_txt} =", "answer": result}


def build(operand_min=0, operand_max=20, n_problems=30, n_cols=3,
          allow_add=True, allow_sub=True, allow_negative_results=True,
          include_answers=False, seed=None, lang="uk", **_):
    rng = random.Random(seed)  # seed=None → fresh set each call
    lbl = gen_labels("arithmetic", lang)

    operand_min, operand_max = int(operand_min), int(operand_max)
    if operand_max < operand_min:                # keep the range well-formed
        operand_min, operand_max = operand_max, operand_min
    n_problems = max(1, int(n_problems))
    n_cols = max(1, int(n_cols))

    ops = []
    if allow_add:
        ops.append("+")
    if allow_sub:
        ops.append("-")
    if not ops:
        ops = ["+"]  # neither ticked → fall back to addition (never 500)

    problems = [
        _make_problem(rng, ops, operand_min, operand_max, allow_negative_results)
        for _ in range(n_problems)
    ]

    figures = [_draw_sheet(problems, n_cols, lbl, lang, show_answers=False)]
    if include_answers:
        figures.append(_draw_sheet(problems, n_cols, lbl, lang, show_answers=True))
    return figures


def _draw_sheet(problems, n_cols, lbl, lang, show_answers):
    fig, ax = new_page(landscape=False, lang=lang)

    ttl = f"{lbl['sheet_title']}  —  {lbl['answers']}" if show_answers else lbl["sheet_title"]
    ax.text(0.5, 0.975, ttl, ha="center", va="center", fontsize=17, fontweight="bold")

    ax.text(0.06, 0.930, f"{lbl['name']} ______________________", ha="left", va="center", fontsize=12)
    ax.text(0.70, 0.930, f"{lbl['date']} ____________", ha="left", va="center", fontsize=12)
    ax.plot([0.05, 0.95], [0.905, 0.905], color="black", lw=1.5)

    x_left, x_right = 0.05, 0.95
    y_top, y_bot = 0.875, 0.03
    n = len(problems)
    n_rows = -(-n // n_cols)  # ceil
    cell_w = (x_right - x_left) / n_cols
    cell_h = (y_top - y_bot) / n_rows

    for r in range(n_rows + 1):
        yy = y_top - r * cell_h
        ax.plot([x_left, x_right], [yy, yy], color="0.4", lw=1.2)
    for c in range(n_cols + 1):
        xx = x_left + c * cell_w
        ax.plot([xx, xx], [y_bot, y_top], color="0.4", lw=1.2)

    for i, prob in enumerate(problems):
        r = i // n_cols
        c = i % n_cols
        cx = x_left + (c + 0.5) * cell_w
        cy = y_top - (r + 0.5) * cell_h
        if show_answers:
            ax.text(cx, cy, f"{prob['text']} {prob['answer']}",
                    ha="center", va="center", fontsize=13, fontweight="bold")
        else:
            ax.text(cx - 0.10 * cell_w, cy, prob["text"],
                    ha="center", va="center", fontsize=13)
            ax.plot([cx + 0.18 * cell_w, cx + 0.44 * cell_w],
                    [cy - 0.22 * cell_h, cy - 0.22 * cell_h], color="black", lw=1)

    return fig
