from __future__ import annotations

from dataclasses import dataclass

from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN
from .schema_helpers import get_schema_for_dataclass


@dataclass
class RctPowerConfigEntryData:
    hostname: str
    port: int = 8899
    entity_prefix: str = "RCT Power Storage"

    @classmethod
    def from_config_entry(cls, config_entry: ConfigEntry):
        if config_entry.domain != DOMAIN:
            raise TypeError(
                "Failed to configure the integration: Mismatching config entry domain."
            )

        return cls(**config_entry.data)

    @classmethod
    def from_user_input(cls, user_input: object):
        valid_user_input = get_schema_for_dataclass(cls)(user_input)

        return cls(**valid_user_input)

    @classmethod
    def get_schema(cls):
        return get_schema_for_dataclass(cls)


def get_title(config_data: RctPowerConfigEntryData):
    return f"RCT Power Inverter at {config_data.hostname}:{config_data.port}"


@dataclass
class RctPowerConfigEntryOptions:
    frequent_scan_interval: int = 30
    infrequent_scan_interval: int = 60 * 3
    static_scan_interval: int = 60 * 60

    @classmethod
    def from_config_entry(cls, config_entry: ConfigEntry):
        if config_entry.domain != DOMAIN:
            raise TypeError(
                "Failed to configure the integration: Mismatching config entry domain."
            )

        return cls(**config_entry.options)

    @classmethod
    def from_user_input(cls, user_input):
        valid_user_input = get_schema_for_dataclass(cls)(user_input)

        return cls(**valid_user_input)

    @classmethod
    def get_schema(cls):
        return get_schema_for_dataclass(cls)


#     @property
#     def object_ids(self):
#         return [
#             entity_descriptor.object_info.object_id
#             for entity_descriptor in self.enabled_entity_descriptors
#         ]

#     @property
#     def enabled_entity_descriptors(self):
#         return known_entities


# from .entities import known_entities
