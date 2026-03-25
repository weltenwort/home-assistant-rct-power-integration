"""Number platform for RCT Power — write support."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity,
    NumberEntityDescription,
    NumberMode,
)
from homeassistant.const import PERCENTAGE, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import RctConfigEntry
from .lib.api import RctPowerApiClient, ValidApiResponse


@dataclass(frozen=True, kw_only=True)
class RctPowerNumberDescription(NumberEntityDescription):
    object_name: str
    multiplier: float = 1.0
    device_type: str = "inverter"  # "inverter" or "battery"


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
        device_type="battery",
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
        device_type="battery",
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
        device_type="battery",
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
        device_type="inverter",
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
        device_info: DeviceInfo,
        native_max_value_override: float | None = None,
    ) -> None:
        self._client = client
        self._config_entry = config_entry
        self.entity_description = description
        self._attr_unique_id = f"{config_entry.entry_id}-write-{description.key}"
        self._attr_device_info = device_info
        self._attr_native_value = None
        if native_max_value_override is not None:
            self._attr_native_max_value = native_max_value_override

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
    from rctclient.registry import REGISTRY

    from .const import (
        BATTERY_MODEL,
        CONF_WRITE_SUPPORT,
        DOMAIN,
        INVERTER_MODEL,
        NAME,
        EntityUpdatePriority,
    )

    if not entry.options.get(CONF_WRITE_SUPPORT, False):
        return

    client: RctPowerApiClient = entry.runtime_data.client  # type: ignore[assignment]
    static_coordinator = entry.runtime_data.update_coordinators[EntityUpdatePriority.STATIC]
    frequent_coordinator = entry.runtime_data.update_coordinators[EntityUpdatePriority.FREQUENT]

    def _get_value(obj_name: str, default=None):
        try:
            oid = REGISTRY.get_by_name(obj_name).object_id
            for coord in (static_coordinator, frequent_coordinator):
                resp = coord.get_latest_response(oid)
                if isinstance(resp, ValidApiResponse):
                    return resp.value
        except Exception:
            pass
        return default

    inverter_sn = str(_get_value("inverter_sn", "unknown"))
    inverter_name = str(_get_value("android_description", "RCT Power"))
    inverter_sw = str(_get_value("svnversion", ""))
    bms_sn = str(_get_value("battery.bms_sn", "unknown"))
    bms_sw = str(_get_value("battery.bms_software_version", ""))

    inverter_device_info = DeviceInfo(
        identifiers={(DOMAIN, "STORAGE", inverter_sn), (DOMAIN, inverter_sn)},  # type: ignore
        name=inverter_name,
        sw_version=inverter_sw,
        model=INVERTER_MODEL,
        manufacturer=NAME,
    )
    battery_device_info = DeviceInfo(
        identifiers={(DOMAIN, "BATTERY", bms_sn), (DOMAIN, bms_sn)},  # type: ignore
        name=f"Battery at {inverter_name}",
        sw_version=bms_sw,
        model=BATTERY_MODEL,
        manufacturer=NAME,
        via_device=(DOMAIN, inverter_sn),
    )

    # Read max grid feed power from inverter (buf_v_control.power_reduction_max_solar_grid)
    # This is already polled as a STATIC entity — read from coordinator data.
    grid_feed_max: float = 6000.0
    try:
        obj_info = REGISTRY.get_by_name("buf_v_control.power_reduction_max_solar_grid")
        response = static_coordinator.get_latest_response(obj_info.object_id)
        if isinstance(response, ValidApiResponse) and isinstance(response.value, (int, float)):
            grid_feed_max = float(response.value)
    except Exception:
        pass  # Fall back to 6000W default

    entities = []
    for description in NUMBER_DESCRIPTIONS:
        device_info = battery_device_info if description.device_type == "battery" else inverter_device_info
        override = grid_feed_max if description.key == "p_rec_lim[1]" else None
        entities.append(
            RctPowerNumberEntity(
                client=client,
                config_entry=entry,
                description=description,
                device_info=device_info,
                native_max_value_override=override,
            )
        )

    async_add_entities(entities)

