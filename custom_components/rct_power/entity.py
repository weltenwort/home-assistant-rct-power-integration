from dataclasses import dataclass, field, fields
from enum import Enum
from typing import List, Optional, Type

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from rctclient.registry import ObjectInfo, REGISTRY
from rctclient.types import DataType

from .const import BATTERY_MODEL, DOMAIN, ICON, INVERTER_MODEL, NAME, VERSION
from .entry import RctPowerConfigEntryData
from .update_coordinator import RctPowerDataUpdateCoordinator


class RctPowerEntity(CoordinatorEntity):
    def __init__(
        self,
        coordinator: RctPowerDataUpdateCoordinator,
        config_entry: ConfigEntry,
        entity_descriptor: "EntityDescriptor",
    ):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.entity_descriptor = entity_descriptor

    def get_object_data_by_name(self, object_name: str):
        return self.coordinator.data.get(REGISTRY.get_by_name(object_name).object_id)

    @property
    def object_infos(self):
        return self.entity_descriptor.object_infos

    @property
    def config_entry_data(self):
        return RctPowerConfigEntryData.from_config_entry(self.config_entry)

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}-{self.object_infos[0].object_id}"

    @property
    def name(self):
        """Return the name of the entity."""
        entity_name = (
            self.entity_descriptor.entity_name
            if self.entity_descriptor != None
            and self.entity_descriptor.entity_name != None
            else slugify_entity_name(self.object_infos[0].name)
        )
        return f"{self.config_entry_data.entity_prefix} {entity_name}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get(self.object_infos[0].object_id)

    @property
    def unit_of_measurement(self):
        return self.object_infos[0].unit

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self.entity_descriptor.icon


class RctPowerInverterEntity(RctPowerEntity):
    @property
    def device_info(self):
        return {
            "identifiers": {
                (DOMAIN, "STORAGE", self.get_object_data_by_name("inverter_sn"))
            },
            "name": str(self.get_object_data_by_name("android_description")),
            "sw_version": str(self.get_object_data_by_name("svnversion")),
            "model": INVERTER_MODEL,
            "manufacturer": NAME,
        }

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return None


# class RctPowerInverterFaultEntity(RctPowerInverterEntity):
#     @property
#     def state(self):
#         fault_bitmask = super().state


class RctPowerBatteryEntity(RctPowerEntity):
    @property
    def device_info(self):
        return {
            "identifiers": {
                (DOMAIN, "BATTERY", self.get_object_data_by_name("battery.bms_sn"))
            },
            "name": f"Battery at {self.get_object_data_by_name('android_description')}",
            "sw_version": str(
                self.get_object_data_by_name("battery.bms_software_version")
            ),
            "model": BATTERY_MODEL,
            "manufacturer": NAME,
            "via_device": (DOMAIN, self.get_object_data_by_name("inverter_sn")),
        }

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return None


class RctPowerPowerSensorEntity(RctPowerEntity):
    pass


class RctPowerAttributesEntity(RctPowerEntity):
    @property
    def state(self):
        return f"{len(self.device_state_attributes.keys())} attributes"

    @property
    def unit_of_measurement(self):
        return None

    @property
    def device_state_attributes(self):
        return {
            object_info.name: self.get_object_data_by_name(object_info.name)
            for object_info in self.entity_descriptor.object_infos
        }


class EntityGroup(Enum):
    BATTERY = "Battery"
    INVERTER = "Inverter"
    OTHERS = "Others"


@dataclass
class EntityDescriptor:
    object_names: List[str]
    entity_group: EntityGroup = EntityGroup.OTHERS
    entity_name: Optional[str] = None
    icon: Optional[str] = ICON
    object_infos: List[ObjectInfo] = field(init=False)
    entity_class: Type[RctPowerEntity] = RctPowerEntity

    def __post_init__(self):
        self.object_infos = [
            REGISTRY.get_by_name(object_name) for object_name in self.object_names
        ]


@dataclass
class BatteryEntityDescriptor(EntityDescriptor):
    entity_group: EntityGroup = EntityGroup.BATTERY
    entity_class: Type[RctPowerEntity] = RctPowerBatteryEntity


@dataclass
class PowerSensorEntityDescriptor(EntityDescriptor):
    entity_group: EntityGroup = EntityGroup.BATTERY
    entity_class: Type[RctPowerEntity] = RctPowerPowerSensorEntity


@dataclass
class InverterEntityDescriptor(EntityDescriptor):
    entity_group: EntityGroup = EntityGroup.INVERTER
    entity_class: Type[RctPowerEntity] = RctPowerInverterEntity


@dataclass
class AttributesEntityDescriptor(EntityDescriptor):
    entity_class: Type[RctPowerEntity] = RctPowerAttributesEntity


# @dataclass
# class FaultEntityDescriptor(EntityDescriptor):
#     def __post_init__(self):
#         self.object_info = REGISTRY.get_by_name(self.object_name)


def slugify_entity_name(name: str):
    return name.replace(".", "_").replace("[", "_").replace("]", "_").replace("?", "_")
