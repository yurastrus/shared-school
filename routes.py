# SPDX-License-Identifier: AGPL-3.0-only
import os
import random

from flask import render_template, request, abort, Response, send_from_directory

from . import school_bp
from . import generators as gen


def _lang(lang_code):
    return "en" if lang_code == "en" else "uk"


def _params_from_request(generator):
    """Coerce editable params from the query; add a seed for randomised
    generators (honour an explicit ?seed=, else pick a fresh one so each
    "Generate" reshuffles while preview and downloads stay consistent)."""
    submitted = "submitted" in request.args
    p = gen.coerce_params(generator, request.args, submitted)
    if generator.randomized:
        s = request.args.get("seed", "")
        p["seed"] = int(s) if s.lstrip("-").isdigit() else random.randrange(1, 10**9)
    return p


def _fields_view(generator, params, lang):
    """Shape FIELDS + current values into template-friendly dicts."""
    view = []
    for f in generator.fields:
        item = {"key": f.key, "kind": f.kind,
                "label": f.label.get(lang, f.label["uk"]),
                "value": params[f.key], "min": f.min, "max": f.max}
        if f.kind == "select":
            item["options"] = [
                {"value": str(v), "label": lab.get(lang, lab["uk"]),
                 "selected": str(v) == str(params[f.key])}
                for v, lab in f.options
            ]
        view.append(item)
    return view


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


# --- WORKSHEET PAGE (settings form + preview + download buttons) ---
@school_bp.route("/w/<key>")
def worksheet(lang_code, key):
    generator = gen.get(key)
    if generator is None:
        abort(404)
    lang = _lang(lang_code)
    params = _params_from_request(generator)
    item = {"key": generator.key, "icon": generator.icon,
            "title": generator.title(lang), "desc": generator.desc(lang)}
    return render_template(
        "school/worksheet.html",
        gen=item,
        fields=_fields_view(generator, params, lang),
        params=params,  # used to build preview/download URLs (incl. seed)
    )


# --- DOWNLOADS ---
def _download(lang_code, key, kind):
    generator = gen.get(key)
    if generator is None:
        abort(404)
    lang = _lang(lang_code)
    params = _params_from_request(generator)
    fname = f"{generator.filename}_{lang}_A4.{kind}"
    if kind == "pdf":
        data = gen.render_pdf(generator, lang=lang, **params)
        mimetype = "application/pdf"
    else:
        data = gen.render_png(generator, lang=lang, **params)
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
    params = _params_from_request(generator)
    return Response(
        gen.render_png(generator, lang=_lang(lang_code), **params),
        mimetype="image/png",
    )
