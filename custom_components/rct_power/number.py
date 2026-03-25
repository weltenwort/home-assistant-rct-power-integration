"""Number platform for RCT Power — write support."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.const import PERCENTAGE, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import RctConfigEntry
from .lib.api import RctPowerApiClient
from .lib.device_info_helpers import get_battery_device_info, get_inverter_device_info
from .lib.entity import RctPowerEntity


@dataclass(frozen=True, kw_only=True)
class RctPowerNumberDescription(NumberEntityDescription):
    object_name: str
    multiplier: float = 1.0
    get_device_info: Callable = lambda e: None


NUMBER_DESCRIPTIONS: list[RctPowerNumberDescription] = [
    RctPowerNumberDescription(
        key="power_mng.soc_max",
        object_name="power_mng.soc_max",
        name="Battery Maximum State of Charge",
        native_min_value=10,
        native_max_value=100,
        native_step=1,
        native_unit_of_measurement=PERCENTAGE,
        device_class=NumberDeviceClass.BATTERY,
        mode=NumberMode.SLIDER,
        multiplier=0.01,
        get_device_info=get_battery_device_info,
    ),
    RctPowerNumberDescription(
        key="power_mng.soc_min",
        object_name="power_mng.soc_min",
        name="Battery Minimum State of Charge",
        native_min_value=5,
        native_max_value=50,
        native_step=1,
        native_unit_of_measurement=PERCENTAGE,
        device_class=NumberDeviceClass.BATTERY,
        mode=NumberMode.SLIDER,
        multiplier=0.01,
        get_device_info=get_battery_device_info,
    ),
    RctPowerNumberDescription(
        key="power_mng.battery_power_extern",
        object_name="power_mng.battery_power_extern",
        name="Battery External Power Target",
        native_min_value=-6000,
        native_max_value=6000,
        native_step=100,
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=NumberDeviceClass.POWER,
        mode=NumberMode.SLIDER,
        entity_category=EntityCategory.CONFIG,
        get_device_info=get_battery_device_info,
    ),
    RctPowerNumberDescription(
        key="p_rec_lim[1]",
        object_name="p_rec_lim[1]",
        name="Maximum Grid Feed Power",
        native_min_value=0,
        native_max_value=6000,
        native_step=100,
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=NumberDeviceClass.POWER,
        mode=NumberMode.SLIDER,
        entity_category=EntityCategory.CONFIG,
        get_device_info=get_inverter_device_info,
    ),
]


class RctPowerNumberEntity(NumberEntity):
    """Writable number entity for RCT Power inverter."""

    _attr_has_entity_name = True

    def __init__(
        self,
        client: RctPowerApiClient,
        config_entry: RctConfigEntry,
        description: RctPowerNumberDescription,
    ) -> None:
        self._client = client
        self._config_entry = config_entry
        self.entity_description = description
        self._attr_unique_id = f"{config_entry.entry_id}-write-{description.key}"
        self._attr_device_info = description.get_device_info(self)
        self._attr_native_value = None

    async def async_set_native_value(self, value: float) -> None:
        write_value = value * self.entity_description.multiplier
        await self._client.async_write_object(
            self.entity_description.object_name, write_value
        )
        self._attr_native_value = value
        self.async_write_ha_state()


async def async_setup_entry(
    hass: HomeAssistant,
    entry: RctConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up number platform."""
    from .const import CONF_WRITE_SUPPORT
    from .lib.api import RctPowerApiClient

    if not entry.options.get(CONF_WRITE_SUPPORT, False):
        return

    client: RctPowerApiClient = entry.runtime_data.client  # type: ignore[assignment]

    async_add_entities(
        [
            RctPowerNumberEntity(
                client=client,
                config_entry=entry,
                description=description,
            )
            for description in NUMBER_DESCRIPTIONS
        ]
    )
