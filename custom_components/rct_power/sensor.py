"""Sensor platform for RCT Power."""
from typing import Callable, List

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from rctclient.registry import REGISTRY
from rctclient.types import DataType, ObjectGroup

from .lib.api import INVERTER_SN_OID
from .lib.const import DEFAULT_NAME, DOMAIN, ICON, SENSOR
from .lib.context import RctPowerContext
from .lib.entity import (
    AttributesEntityDescriptor,
    RctPowerBatteryEntity,
    RctPowerInverterEntity,
)


SENSOR_DATA_TYPES = [
    DataType.UINT8,
    DataType.INT8,
    DataType.UINT16,
    DataType.INT16,
    DataType.UINT32,
    DataType.INT32,
    DataType.ENUM,
    DataType.FLOAT,
    DataType.STRING,
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: Callable[[List[Entity]], None],
):
    """Setup sensor platform."""
    context = hass.data[DOMAIN][entry.entry_id]

    if not isinstance(context, RctPowerContext):
        return False

    async_add_entities(
        [
            entity_descriptor.entity_class(
                coordinators=list(context.update_coordinators.values()),
                config_entry=entry,
                entity_descriptor=entity_descriptor,
            )
            for entity_descriptor in context.entity_descriptors
            if isinstance(entity_descriptor, AttributesEntityDescriptor)
            or all(
                info.response_data_type in SENSOR_DATA_TYPES
                for info in entity_descriptor.object_infos
            )
        ]
    )
