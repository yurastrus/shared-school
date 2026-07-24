# SPDX-License-Identifier: AGPL-3.0-only
"""Lightweight UK/EN i18n for the school module.

Ukrainian is the source language: template/UI strings are written in Ukrainian
and this table maps them to English. `_()` (injected in __init__) returns the
source for `uk`, the mapped value for `en`, and falls back to the host app's
flask-babel catalogue for shared strings (e.g. the site nav) it doesn't know.

Generated worksheets are localised separately — each generator takes a ``lang``
argument and pulls its labels from ``GEN`` below.
"""

# UI / template strings: Ukrainian source → English.
EN = {
    "Навчальні матеріали": "Learning materials",
    "До розділів": "Back to sections",
    "Друковані заготовки для дітей — A4, чорно-білий друк. Виберіть тему, а на її сторінці завантажте PDF (для друку) або PNG.":
        "Printable worksheets for children — A4, black-and-white. Choose a topic, then download it as PDF (for printing) or PNG on its page.",
    "Завантажити PDF": "Download PDF",
    "Завантажити PNG": "Download PNG",
}


def ui(text, lang):
    """Translate a UI string; unknown strings return None so the caller can
    fall back to the host flask-babel catalogue."""
    if lang == "en":
        return EN.get(text)
    return text


# Per-generator localised labels, keyed by generator ``key`` then language.
GEN = {
    "number-line": {
        "uk": {"title": "Числові шкали",
               "desc": "Числова пряма −20…+20, кілька шт. на аркуш."},
        "en": {"title": "Number lines",
               "desc": "Number line −20…+20, several per sheet."},
    },
    "arithmetic": {
        "uk": {"title": "Приклади (додавання-віднімання)",
               "desc": "Випадкові приклади на + та − у комірках.",
               "sheet_title": "Приклади: додавання та віднімання",
               "name": "Ім'я:", "date": "Дата:", "answers": "ВІДПОВІДІ"},
        "en": {"title": "Arithmetic (addition & subtraction)",
               "desc": "Random + and − problems in a grid of cells.",
               "sheet_title": "Problems: addition & subtraction",
               "name": "Name:", "date": "Date:", "answers": "ANSWERS"},
    },
    "pythagoras": {
        "uk": {"title": "Таблиця Піфагора",
               "desc": "Таблиця множення: заповнена та «сліпа».",
               "sheet_title": "Таблиця множення (Піфагора)",
               "filled": "заповнена", "blank": "заповни сам(а)"},
        "en": {"title": "Multiplication table",
               "desc": "Times table: filled and blank versions.",
               "sheet_title": "Multiplication table",
               "filled": "filled in", "blank": "fill it in yourself"},
    },
}


def gen_labels(key, lang):
    """Localised label bundle for a generator; defaults to Ukrainian."""
    langs = GEN[key]
    return langs.get(lang, langs["uk"])
