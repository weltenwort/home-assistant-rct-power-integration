"""Sensor platform for RCT Power."""

from __future__ import annotations

from collections.abc import Callable

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from . import RctConfigEntry
from .lib.entities import (
    battery_sensor_entity_descriptions,
    bitfield_sensor_entity_descriptions,
    inverter_sensor_entity_descriptions,
)
from .lib.entity import RctPowerBitfieldSensorEntity, RctPowerSensorEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: RctConfigEntry,
    async_add_entities: Callable[[list[Entity]], None],
) -> None:
    """Setup sensor platform."""
    data = entry.runtime_data

    battery_sensor_entities = [
        RctPowerSensorEntity(
            coordinators=list(data.update_coordinators.values()),
            config_entry=entry,
            entity_description=entity_description,
        )
        for entity_description in battery_sensor_entity_descriptions
    ]

    inverter_sensor_entities = [
        RctPowerSensorEntity(
            coordinators=list(data.update_coordinators.values()),
            config_entry=entry,
            entity_description=entity_description,
        )
        for entity_description in inverter_sensor_entity_descriptions
    ]

    bitfield_sensor_entities = [
        RctPowerBitfieldSensorEntity(
            coordinators=list(data.update_coordinators.values()),
            config_entry=entry,
            entity_description=entity_description,
        )
        for entity_description in bitfield_sensor_entity_descriptions
    ]

    async_add_entities(
        [
            *battery_sensor_entities,
            *inverter_sensor_entities,
            *bitfield_sensor_entities,
        ]
    )
