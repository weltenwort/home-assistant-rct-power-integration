from dataclasses import Field, MISSING, fields
from typing import Any, List, Optional

from voluptuous import Optional as OptionalField, Required as RequiredField, Schema


def get_key_for_field(field: Field[Any]):
    if field.default == MISSING:
        return RequiredField(field.name)

    return OptionalField(field.name, default=field.default)


def get_schema_for_field(field: Field[Any]):
    return field.metadata.get("schema_type", field.type)


def get_schema_for_dataclass(cls: type, allow_fields: Optional[List[str]] = None):
    return Schema(
        {
            get_key_for_field(field): get_schema_for_field(field)
            for field in fields(cls)
            if allow_fields is None or field.name in allow_fields
        }
    )
