# SPDX-License-Identifier: AGPL-3.0-only
"""School (навчальні матеріали) blueprint package.

Printable worksheet generators for children — a card hub start page grouped by
subject (currently «Математика»); each card opens a page with two buttons that
download the worksheet as PDF (for printing) or PNG (for preview). Designed as a
git submodule of the host site, mirroring the camera_traps / pam modules.
"""
from flask import Blueprint

# Blueprint name doubles as the templates folder name.
school_bp = Blueprint("school", __name__, template_folder="templates")


@school_bp.context_processor
def _inject_translation():
    """UK/EN `_` for school templates: Ukrainian source strings pass through for
    `uk`, are mapped to English for `en` (see i18n.EN), and fall back to the host
    app's flask-babel catalogue for shared strings (e.g. the site nav) — since a
    blueprint context processor overrides flask-babel's `_` on this module's
    pages. Mirrors how the camera_traps submodule injects its own `_`."""
    from flask import g
    from flask_babel import gettext as _babel_gettext
    from . import i18n

    def _translate(s):
        lang = getattr(g, "lang_code", "uk") or "uk"
        hit = i18n.ui(s, lang)
        if hit is not None:
            return hit
        # unknown to this module → defer to the host catalogue (nav, etc.)
        return _babel_gettext(s)

    return {"_": _translate, "gettext": _translate}


from . import routes  # noqa: E402,F401
