# SPDX-License-Identifier: AGPL-3.0-only
"""Registry of printable worksheet generators.

Each generator exposes ``build(lang=..., **params) -> list[Figure]`` (one Figure
per page) and a ``FIELDS`` tuple describing its user-editable parameters. Adding
a new worksheet = add a module next to this one and one ``Generator`` entry in
``_ALL`` — routes, start-page cards, the settings form and the download
endpoints are all driven off this table. Localised card titles / descriptions
live in ``i18n.GEN`` (keyed by the generator's ``key``).
"""
from dataclasses import dataclass, field
from typing import Callable

from . import number_line, arithmetic, pythagoras
from .base import figures_to_pdf, figure_to_png
from .schema import coerce as _coerce
from ..i18n import gen_labels


@dataclass(frozen=True)
class Generator:
    key: str                       # URL slug + filename stem + i18n key
    group: str                     # start-page section, e.g. "math"
    icon: str                      # emoji shown on the card
    build: Callable                # (lang=..., **params) -> list[Figure]
    filename: str                  # download base name (no extension)
    fields: tuple                  # schema.Field tuple (editable params)
    randomized: bool = False       # True → seed-driven; "Generate" reshuffles
    params: dict = field(default_factory=dict)  # extra fixed build params

    def title(self, lang):
        return gen_labels(self.key, lang)["title"]

    def desc(self, lang):
        return gen_labels(self.key, lang)["desc"]


# Ordered so the start page renders cards in a sensible sequence.
_ALL = [
    Generator(key="number-line", group="math", icon="📏",
              build=number_line.build, filename="number_line",
              fields=number_line.FIELDS),
    Generator(key="arithmetic", group="math", icon="➕",
              build=arithmetic.build, filename="arithmetic",
              fields=arithmetic.FIELDS, randomized=True),
    Generator(key="pythagoras", group="math", icon="✖️",
              build=pythagoras.build, filename="multiplication_table",
              fields=pythagoras.FIELDS),
]

GENERATORS = {g.key: g for g in _ALL}

# Section metadata for the start page (ordered); titles are bilingual.
GROUPS = [
    {"key": "math", "icon": "🔢", "title": {"uk": "Математика", "en": "Mathematics"}},
]


def list_by_group(group_key):
    return [g for g in _ALL if g.group == group_key]


def get(key):
    return GENERATORS.get(key)


def coerce_params(gen, args, submitted):
    """Validate/clamp request args against the generator's FIELDS."""
    return _coerce(gen.fields, args, submitted)


def render_pdf(gen, lang="uk", **params):
    p = {**gen.params, "lang": lang, **params}
    return figures_to_pdf(gen.build(**p))


def render_png(gen, lang="uk", **params):
    p = {**gen.params, "lang": lang, **params}
    figs = gen.build(**p)
    return figure_to_png(figs[0])  # PNG preview = first page only
