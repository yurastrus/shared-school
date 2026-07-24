# SPDX-License-Identifier: AGPL-3.0-only
"""Declarative description of a generator's user-editable parameters.

Each generator lists ``FIELDS`` (a tuple of ``Field``). The registry coerces
incoming query args against them (with clamping/validation), the routes render
a settings form from them, and the values are passed straight to ``build()``.
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Field:
    key: str                      # matches the build() kwarg + form input name
    kind: str                     # 'int' | 'bool' | 'select'
    default: object
    label: dict                   # {'uk': ..., 'en': ...}
    min: Optional[int] = None     # int only — clamp bound (also a hard safety cap)
    max: Optional[int] = None
    # select only: tuple of (value, {'uk','en'}) pairs
    options: tuple = field(default_factory=tuple)


_TRUTHY = {"1", "true", "on", "yes"}


def coerce(fields, args, submitted):
    """Return {key: value} coerced/clamped from a request-args mapping.

    ``submitted`` marks that the settings form was posted (a hidden marker),
    so an absent checkbox reads as False rather than falling back to default.
    """
    out = {}
    for f in fields:
        if f.kind == "int":
            raw = args.get(f.key)
            try:
                v = int(raw)
            except (TypeError, ValueError):
                v = f.default
            if f.min is not None:
                v = max(f.min, v)
            if f.max is not None:
                v = min(f.max, v)
            out[f.key] = v
        elif f.kind == "bool":
            if f.key in args:
                out[f.key] = args.get(f.key, "").strip().lower() in _TRUTHY
            else:
                out[f.key] = False if submitted else f.default
        elif f.kind == "select":
            raw = args.get(f.key)
            valid = {str(v) for v, _ in f.options}
            out[f.key] = raw if raw in valid else str(f.default)
    return out
