"""Sensor platform for RCT Power."""
from typing import Callable, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity

from .lib.const import DOMAIN
from .lib.context import RctPowerContext
from .lib.entities import (
    battery_sensor_entity_descriptions,
    fault_sensor_entity_descriptions,
    inverter_sensor_entity_descriptions,
)
from .lib.entity import (
    RctPowerBatterySensorEntity,
    RctPowerInverterFaultSensorEntity,
    RctPowerInverterSensorEntity,
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable[[List[Entity]], None],
):
    """Setup sensor platform."""
    context = hass.data[DOMAIN][entry.entry_id]  # type: ignore

    if not isinstance(context, RctPowerContext):
        return False

    battery_sensor_entities = [
        RctPowerBatterySensorEntity(
            coordinators=list(context.update_coordinators.values()),
            config_entry=entry,
            entity_description=entity_description,
        )
        for entity_description in battery_sensor_entity_descriptions
    ]

    inverter_sensor_entities = [
        RctPowerInverterSensorEntity(
            coordinators=list(context.update_coordinators.values()),
            config_entry=entry,
            entity_description=entity_description,
        )
        for entity_description in inverter_sensor_entity_descriptions
    ]

    inverter_fault_sensor_entities = [
        RctPowerInverterFaultSensorEntity(
            coordinators=list(context.update_coordinators.values()),
            config_entry=entry,
            entity_description=entity_description,
        )
        for entity_description in fault_sensor_entity_descriptions
    ]

    async_add_entities(
        [
            *battery_sensor_entities,
            *inverter_sensor_entities,
            *inverter_fault_sensor_entities,
        ]
    )
