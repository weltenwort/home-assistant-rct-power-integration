"""Sensor platform for RCT Power."""

from __future__ import annotations

from collections.abc import Callable

from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from rctclient.registry import REGISTRY

from . import RctConfigEntry
from .lib.entities import (
    GRID_VOLTAGE_SMARTMETER_OBJECT_NAMES,
    battery_sensor_entity_descriptions,
    bitfield_sensor_entity_descriptions,
    get_grid_voltage_sensor_entity_descriptions,
    inverter_sensor_entity_descriptions,
)
from .lib.entity import RctPowerBitfieldSensorEntity, RctPowerSensorEntity


def _has_smartmeter_voltage(entry: RctConfigEntry, object_name: str) -> bool:
    """Return whether the smart meter reports a non-zero voltage."""
    object_id = REGISTRY.get_by_name(object_name).object_id

    return any(
        isinstance(value := coordinator.get_valid_value_or(object_id, 0), (int, float))
        and value != 0
        for coordinator in entry.runtime_data.update_coordinators.values()
    )


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
        if entity_description.key not in GRID_VOLTAGE_SMARTMETER_OBJECT_NAMES
    ]

    grid_voltage_sensor_entities = [
        RctPowerSensorEntity(
            coordinators=list(data.update_coordinators.values()),
            config_entry=entry,
            entity_description=entity_description,
        )
        for entity_description in get_grid_voltage_sensor_entity_descriptions(
            [
                _has_smartmeter_voltage(entry, object_name)
                for object_name in GRID_VOLTAGE_SMARTMETER_OBJECT_NAMES
            ]
        )
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
            *grid_voltage_sensor_entities,
            *bitfield_sensor_entities,
        ]
    )
