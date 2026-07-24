# shared-school — навчальні матеріали для дітей / kids' learning worksheets

> **EN:** A Flask-blueprint module of **printable worksheets for children**,
> fully **bilingual (Ukrainian / English)** — both the UI and the generated
> sheets follow the page language (`/uk/…` vs `/en/…`). Start page = a card hub
> grouped by subject (currently **Mathematics**); each card opens a page with
> **Download PDF** / **Download PNG** buttons. A4, black-and-white, print-ready.
> Built as a git submodule of the host site, like `camera_traps` / `pam`.
> Python/matplotlib port of the original R generators. Public repository.

Flask-blueprint модуль із **друкованими заготовками для дітей** (worksheets).
Стартова сторінка — хаб карток, згрупованих за предметом (наразі
**Математика**). Кожна картка відкриває сторінку з двома кнопками:
**завантажити PDF** (для друку) та **завантажити PNG** (для перегляду).

Проєктувався як git-**субмодуль** основного сайту, за тим самим шаблоном, що й
модулі `camera_traps` (shared-ct) та `pam` (shared-pam): монтується в
`app/school` і реєструється з префіксом `/<lang_code>/school`.

Це Python-порт R-генераторів із теки
`G:\My Drive\7 - Навчальні матеріали\01 - Для дітей` (base R graphics →
matplotlib). Дизайн-правила збережено: **A4, чорно-білий друк**, елементи
розрізняються товщиною/довжиною ліній і жирністю шрифту, аркуш заповнюється
ефективно.

## Структура

```
school/
├── __init__.py            # Blueprint `school_bp` (+ i18n-шим `_`)
├── routes.py              # overview (хаб) · worksheet · .pdf / .png / preview
├── generators/            # рушій генерації
│   ├── __init__.py        # РЕЄСТР генераторів (GENERATORS, GROUPS)
│   ├── base.py            # A4-константи, matplotlib-налаштування, PDF/PNG
│   ├── number_line.py     # Числові шкали  (−20…20, кілька на аркуш)
│   ├── arithmetic.py      # Приклади +/− у комірках
│   └── pythagoras.py      # Таблиця Піфагора (заповнена + «сліпа»)
├── templates/             # school_base · overview · worksheet
└── static/css/school.css
```

## Маршрути

| URL | Опис |
|---|---|
| `/<lang>/school/` | стартова сторінка (картки) |
| `/<lang>/school/w/<key>` | сторінка теми (прев'ю + 2 кнопки) |
| `/<lang>/school/w/<key>.pdf` | завантажити PDF (A4, усі сторінки) |
| `/<lang>/school/w/<key>.png` | завантажити PNG (перша сторінка, 300 dpi) |
| `/<lang>/school/w/<key>/preview.png` | inline-прев'ю для сторінки теми |

`<key>` ∈ `number-line`, `arithmetic`, `pythagoras`.

## Додати новий генератор

1. Створити модуль `generators/<name>.py` з функцією
   `build(**params) -> list[matplotlib.figure.Figure]` (одна Figure = одна
   сторінка). Використовувати хелпери з `generators/base.py`.
2. Додати один запис `Generator(...)` у `_ALL` в `generators/__init__.py`.
3. Усе інше (картка на хабі, сторінка теми, ендпоінти PDF/PNG) підхопиться
   автоматично з реєстру.

## Залежності

`Flask`, `matplotlib`, `pillow` — усі вже присутні в основному застосунку.
DejaVu Sans (бандл matplotlib) покриває кирилицю та потрібні мат. гліфи;
у PDF вбудовуються реальні TrueType-контури (`pdf.fonttype = 42`).

## Ліцензія

AGPL-3.0-only (див. `LICENSE`).
