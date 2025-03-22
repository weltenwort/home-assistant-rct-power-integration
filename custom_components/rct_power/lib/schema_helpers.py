from __future__ import annotations

from dataclasses import MISSING, Field, fields
from typing import Any

import voluptuous as vol


def get_key_for_field(field: Field[Any]):
    if field.default == MISSING:
        return vol.Required(field.name)

    return vol.Optional(field.name, default=field.default)


def get_schema_for_field(field: Field[Any]):
    return field.metadata.get("schema_type", field.type)


def get_schema_for_dataclass(cls: type, allow_fields: list[str] | None = None):
    return vol.Schema(
        {
            get_key_for_field(field): get_schema_for_field(field)
            for field in fields(cls)
            if allow_fields is None or field.name in allow_fields
        }
    )
