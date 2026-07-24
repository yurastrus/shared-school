# SPDX-License-Identifier: AGPL-3.0-only
import os

from flask import render_template, abort, Response, send_from_directory

from . import school_bp
from . import generators as gen


def _lang(lang_code):
    return "en" if lang_code == "en" else "uk"


# --- MODULE STATIC FILES ---
@school_bp.route("/school-static/<path:filename>")
def serve_school_static(lang_code, filename):
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    return send_from_directory(static_dir, filename)


# --- MODULE START PAGE (card hub) ---
@school_bp.route("/")
def overview(lang_code):
    """Start page: subject groups with a card per worksheet generator."""
    lang = _lang(lang_code)
    groups = [
        {
            "title": grp["title"].get(lang, grp["title"]["uk"]),
            "icon": grp["icon"],
            "items": [
                {"key": g.key, "icon": g.icon,
                 "title": g.title(lang), "desc": g.desc(lang)}
                for g in gen.list_by_group(grp["key"])
            ],
        }
        for grp in gen.GROUPS
    ]
    return render_template("school/overview.html", groups=groups)


# --- WORKSHEET PAGE (preview + two download buttons) ---
@school_bp.route("/w/<key>")
def worksheet(lang_code, key):
    generator = gen.get(key)
    if generator is None:
        abort(404)
    lang = _lang(lang_code)
    item = {"key": generator.key, "icon": generator.icon,
            "title": generator.title(lang), "desc": generator.desc(lang)}
    return render_template("school/worksheet.html", gen=item)


# --- DOWNLOADS ---
def _download(lang_code, key, kind):
    generator = gen.get(key)
    if generator is None:
        abort(404)
    lang = _lang(lang_code)
    fname = f"{generator.filename}_{lang}_A4.{kind}"
    if kind == "pdf":
        data = gen.render_pdf(generator, lang=lang)
        mimetype = "application/pdf"
    else:
        data = gen.render_png(generator, lang=lang)
        mimetype = "image/png"
    return Response(
        data,
        mimetype=mimetype,
        headers={"Content-Disposition": f'attachment; filename="{fname}"'},
    )


@school_bp.route("/w/<key>.pdf")
def worksheet_pdf(lang_code, key):
    return _download(lang_code, key, "pdf")


@school_bp.route("/w/<key>.png")
def worksheet_png(lang_code, key):
    return _download(lang_code, key, "png")


@school_bp.route("/w/<key>/preview.png")
def worksheet_preview(lang_code, key):
    """Inline PNG for the on-page preview (no attachment header)."""
    generator = gen.get(key)
    if generator is None:
        abort(404)
    return Response(gen.render_png(generator, lang=_lang(lang_code)), mimetype="image/png")
