from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from functools import cached_property
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityDescription
from homeassistant.helpers.typing import UNDEFINED, StateType, UndefinedType
from rctclient.registry import REGISTRY, ObjectInfo

from .api import (
    ApiResponse,
    ApiResponseValue,
    ValidApiResponse,
    get_valid_response_value_or,
)
from .const import ICON, EntityUpdatePriority
from .device_class_helpers import guess_device_class_from_unit
from .entry import RctPowerConfigEntryData
from .multi_coordinator_entity import MultiCoordinatorEntity
from .state_helpers import (
    get_api_response_values_as_bitfield,
    get_first_api_response_value_as_state,
)
from .update_coordinator import RctPowerDataUpdateCoordinator


class RctPowerEntity(MultiCoordinatorEntity):
    entity_description: RctPowerEntityDescription
    object_infos: list[ObjectInfo]

    def __init__(
        self,
        coordinators: list[RctPowerDataUpdateCoordinator],
        config_entry: ConfigEntry,
        entity_description: RctPowerEntityDescription,
    ):
        super().__init__(coordinators)
        self.config_entry = config_entry
        self.entity_description = (  # pyright: ignore [reportIncompatibleVariableOverride]
            entity_description
        )
        self.object_infos = resolve_object_infos(self.entity_description)

    def get_api_response_by_id(
        self, object_id: int, default: ApiResponse | None = None
    ):
        for coordinator in self.coordinators:
            latest_response = coordinator.get_latest_response(object_id)

            if latest_response is not None:
                return latest_response

        return default

    def get_api_response_by_name(
        self, object_name: str, default: ApiResponse | None = None
    ):
        return self.get_api_response_by_id(
            REGISTRY.get_by_name(object_name).object_id, default
        )

    def get_valid_api_response_value_by_id(
        self, object_id: int, default: ApiResponseValue | None = None
    ):
        return get_valid_response_value_or(
            self.get_api_response_by_id(object_id, None), default
        )

    def get_valid_api_response_value_by_name(
        self, object_name: str, default: ApiResponseValue | None = None
    ):
        return get_valid_response_value_or(
            self.get_api_response_by_name(object_name, None), default
        )

    @property
    def config_entry_data(self):
        return RctPowerConfigEntryData.from_config_entry(self.config_entry)

    @cached_property
    def unique_id(self) -> str | None:
        """Return a unique ID to use for this entity."""
        # this allows for keeping the entity identity stable for existing
        # sensors when the algorithm below changes
        if uid := self.entity_description.unique_id:
            return f"{self.config_entry.entry_id}-{uid}"

        object_ids = [str(object_info.object_id) for object_info in self.object_infos]
        return "-".join([self.config_entry.entry_id, *object_ids])

    @property
    def name(self) -> str | UndefinedType | None:
        """Return the name of the entity."""
        entity_name = (
            self.entity_description.name
            if self.entity_description.name != UNDEFINED
            else slugify_entity_name(self.object_infos[0].name)
        )

        return f"{self.config_entry_data.entity_prefix} {entity_name}"

    @property
    def available(self) -> bool:
        return all(
            isinstance(
                self.get_api_response_by_id(object_info.object_id), ValidApiResponse
            )
            for object_info in self.object_infos
        )

    @cached_property
    def unit_of_measurement(self):
        if unit_of_measurement := super().unit_of_measurement:
            return unit_of_measurement

        return self.object_infos[0].unit

    @cached_property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        return {}

    @property
    def device_info(self):
        return self.entity_description.get_device_info(self)


class RctPowerSensorEntity(SensorEntity, RctPowerEntity):
    entity_description: RctPowerSensorEntityDescription  # pyright: ignore [reportIncompatibleVariableOverride]

    def get_valid_api_responses(self):
        return [
            self.get_valid_api_response_value_by_id(object_info.object_id, None)
            for object_info in self.object_infos
        ]

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        if device_class := super().device_class:
            return device_class

        if self.native_unit_of_measurement:
            return guess_device_class_from_unit(self.native_unit_of_measurement)

        return None

    @property
    def native_value(self) -> StateType | date | datetime | Decimal:
        return self.entity_description.get_native_value(
            self, self.get_valid_api_responses()
        )

    @cached_property
    def native_unit_of_measurement(self):
        if native_unit_of_measurement := super().native_unit_of_measurement:
            return native_unit_of_measurement

        return self.object_infos[0].unit


class RctPowerBitfieldSensorEntity(RctPowerSensorEntity):
    @cached_property
    def native_unit_of_measurement(self) -> str | None:
        return None

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        if device_class := super().device_class:
            return device_class

        if self.options:
            return SensorDeviceClass.ENUM

        return None

    @property
    def extra_state_attributes(self):
        return {
            **(super().extra_state_attributes),
            "bitfield": get_api_response_values_as_bitfield(
                self, self.get_valid_api_responses()
            ),
        }


@dataclass(frozen=True, kw_only=True)
class RctPowerEntityDescription(EntityDescription):
    icon: str | None = ICON
    object_names: list[str] | None = None
    # to allow for stable entity identities even if the object ids change
    unique_id: str | None = None
    update_priority: EntityUpdatePriority = EntityUpdatePriority.FREQUENT
    get_device_info: Callable[[RctPowerEntity], DeviceInfo | None] = lambda e: None


@dataclass(frozen=True, kw_only=True)
class RctPowerSensorEntityDescription(
    RctPowerEntityDescription, SensorEntityDescription
):
    get_native_value: Callable[
        [RctPowerSensorEntity, list[ApiResponseValue | None]], StateType
    ] = get_first_api_response_value_as_state


@dataclass(frozen=True, kw_only=True)
class RctPowerBitfieldSensorEntityDescription(
    RctPowerEntityDescription, SensorEntityDescription
):
    get_native_value: Callable[
        [RctPowerSensorEntity, list[ApiResponseValue | None]], StateType
    ] = get_api_response_values_as_bitfield


def slugify_entity_name(name: str):
    return name.replace(".", "_").replace("[", "_").replace("]", "_").replace("?", "_")


def resolve_object_infos(entity_description: RctPowerEntityDescription):
    object_names = entity_description.object_names or [entity_description.key]
    return [REGISTRY.get_by_name(object_name) for object_name in object_names]


known_faults = [
    "TRAP occurred",
    "RTC can't be configured",
    "RTC 1Hz signal timeout",
    "Hardware Stop by 3.3V fault",
    "Hardware Stop by PWM Logic",
    "Hardware Stop by Uzk overvoltage",
    "Uzk+ is over limit",
    "Uzk- is over limit",
    "Throttle Phase L1 overcurrent",
    "Throttle Phase L2 overcurrent",
    "Throttle Phase L3 overcurrent",
    "Buffer capacitor voltage",
    "Quartz fault",
    "Grid under_voltage phase 1",
    "Grid under_voltage phase 2",
    "Grid under_voltage phase 3",
    "Battery overcurrent",
    "Relays Test failed",
    "Board Over Temperature",
    "Core Over Temperature",
    "Sink 1 Over Temperature",
    "Sink 2 Over Temperature",
    "Error by I2C communication with Power Board",
    "Power Board Error",
    "PWM output ports defect",
    "Insulation is too small or not plausible",
    "I DC Component Max (1 A)",
    "I DC Component Max Slow (47 mA)",
    "One of the DSD channels possibly defect (too big current offset)",
    "Error by RS485 communication with Relays BoxIGBT L1 BH defect",
    "Phase to phase over voltage",
    "IGBT L1 BH defect",
    "IGBT L1 BL defect",
    "IGBT L2 BH defect",
    "IGBT L2 BL defect",
    "IGBT L3 BH defect",
    "IGBT L3 BL defect",
    "Long Term over voltage phase 1",
    "Long Term over voltage phase 2",
    "Long Term over voltage phase 3",
    "Over voltage phase 1, level 1",
    "Over voltage phase 1, level 2",
    "Over voltage phase 2, level 1",
    "Over voltage phase 2, level 2",
    "Over voltage phase 3, level 1",
    "Over voltage phase 3, level 2",
    "Over frequency, level 1",
    "Over frequency, level 2",
    "Under voltage phase 1, level 1",
    "Under voltage phase 1, level 2",
    "Under voltage phase 2, level 1",
    "Under voltage phase 2, level 2",
    "Under voltage phase 3, level 1",
    "Under voltage phase 3, level 2",
    "Under frequency, level 1",
    "Under frequency, level 2",
    "CPU Exception NMI",
    "CPU Exception HardFault",
    "CPU Exception MemManage",
    "CPU Exception BusFault",
    "CPU Exception UsageFault",
    "RTC Power on reset",
    "RTC Oscillation stops",
    "RTC Supply voltage drop",
    "Jump of RCD current DC + AC > 30mA was noticed",
    "Jump of RCD current DC > 60mA was noticed",
    "Jump of RCD current AC > 150mA was noticed",
    "RCD current > 300mA was noticed",
    "incorrect 5V was noticed",
    "incorrect -9V was noticed",
    "incorrect 9V was noticed",
    "incorrect 3V3 was noticed",
    "failure of RDC calibration was noticed",
    "failure of I2C was noticed",
    "afi frequency generator failure",
    "sink temperature too high",
    "Uzk is over limit",
    "Usg A is over limit",
    "Usg B is over limit",
    "Switching On Conditions Umin phase 1",
    "Switching On Conditions Umax phase 1",
    "Switching On Conditions Fmin phase 1",
    "Switching On Conditions Fmax phase 1",
    "Switching On Conditions Umin phase 2",
    "Switching On Conditions Umax phase 2",
    "Battery current sensor defect",
    "Battery booster damaged",
    "Switching On Conditions Umin phase 3",
    "Switching On Conditions Umax phase 3",
    "Voltage surge or average offset is too big on AC-terminals (phase failure detected)",
    "Inverter is disconnected from the household grid",
    "Difference of the measured +9V between DSP and PIC is too big",
    "1.5V error",
    "2.5V error",
    "1.5V measurement difference",
    "2.5V measurement difference",
    "The battery voltage is outside of the expected range",
    "Unable to start the main PIC software",
    "PIC bootloader detected unexpectedly",
    "Phase position error (not 120° as expected)",
    "Battery overvoltage",
    "Throttle current is unstable",
    "Difference between internal and external measured grid voltage is too big in phase",
    "Difference between internal and external measured grid voltage is too big in phase",
    "Difference between internal and external measured grid voltage is too big in phase",
    "External emergency turn off signal is active",
    "Battery is empty, not more energy for standby",
    "CAN communication timeout with battery",
    "Timing problem",
    "Battery IGBT's Heat Sink Over Temperature",
    "Battery heat sink temperature too high",
    "Internal Relays Box error",
    "Relays Box PE off error",
    "Relays Box PE on error",
    "Internal battery error",
    "Parameter changed",
    "3 attempts of island building are failed",
    "Phase to phase under voltage",
    "System reset detected",
    "Update detected",
    "FRT over-voltage",
    "FRT under-voltage",
    "IGBT L1 free wheeling diode defect",
    "IGBT L2 free wheeling diode defect",
    "IGBT L3 free wheeling diode defect",
    "1 phase mode is activated but not allowed for this device class (e.g. 10K)",
    "Island detected",
]
