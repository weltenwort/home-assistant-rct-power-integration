from dataclasses import Field, MISSING, dataclass, fields
from typing import ClassVar

from homeassistant.config_entries import ConfigEntry
from voluptuous import Required, Schema

from .const import DOMAIN


def get_key_for_field(field: Field):
    if field.default == MISSING:
        return Required(field.name)

    return field.name


def get_schema_for_field(field: Field):
    return field.metadata.get("schema_type", field.type)


def get_schema_for_dataclass(cls):
    return Schema(
        {get_key_for_field(field): get_schema_for_field(field) for field in fields(cls)}
    )


@dataclass
class RctPowerConfigEntryData:
    hostname: str
    port: int
    enabled: bool = True
    scan_interval: int = 30

    @classmethod
    def from_config_entry(cls, config_entry: ConfigEntry):
        if config_entry.domain != DOMAIN:
            raise TypeError(
                "Failed to configure the integration: Mismatching config entry domain."
            )

        return cls(**config_entry.data)

    @classmethod
    def from_user_input(cls, user_input):
        valid_user_input = get_schema_for_dataclass(cls)(user_input)

        return cls(**valid_user_input)

    @classmethod
    def get_schema(cls):
        return get_schema_for_dataclass(cls)

    def get_title(self):
        return f"Inverter at {self.hostname}:{self.port}"
