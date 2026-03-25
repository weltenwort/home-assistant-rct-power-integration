"""Select platform for RCT Power — charging strategy."""

from __future__ import annotations

from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import RctConfigEntry
from .lib.api import RctPowerApiClient, ValidApiResponse

# power_mng.soc_strategy values (index = integer written to inverter)
SOC_STRATEGY_OPTIONS: list[str] = [
    "SOC Target",
    "Constant",
    "External",
    "Average Voltage",
    "Internal",
    "Schedule",
]


class RctPowerSocStrategyEntity(SelectEntity):
    """Select entity for the battery charging strategy."""

    _attr_has_entity_name = True
    _attr_name = "Battery Charging Strategy"
    _attr_options = SOC_STRATEGY_OPTIONS
    _attr_entity_category = EntityCategory.CONFIG

    def __init__(
        self,
        client: RctPowerApiClient,
        config_entry: RctConfigEntry,
        device_info: DeviceInfo,
        current_option: str | None = None,
    ) -> None:
        self._client = client
        self._config_entry = config_entry
        self._attr_unique_id = f"{config_entry.entry_id}-write-power_mng.soc_strategy"
        self._attr_device_info = device_info
        self._attr_current_option = current_option

    async def async_select_option(self, option: str) -> None:
        value = SOC_STRATEGY_OPTIONS.index(option)
        await self._client.async_write_object("power_mng.soc_strategy", value)
        self._attr_current_option = option
        self.async_write_ha_state()


async def async_setup_entry(
    hass: HomeAssistant,
    entry: RctConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up select platform."""
    from rctclient.registry import REGISTRY

    from .const import (
        CONF_WRITE_SUPPORT,
        DOMAIN,
        INVERTER_MODEL,
        NAME,
        EntityUpdatePriority,
    )

    if not entry.options.get(CONF_WRITE_SUPPORT, False):
        return

    client: RctPowerApiClient = entry.runtime_data.client  # type: ignore[assignment]
    static_coordinator = entry.runtime_data.update_coordinators[
        EntityUpdatePriority.STATIC
    ]
    frequent_coordinator = entry.runtime_data.update_coordinators[
        EntityUpdatePriority.FREQUENT
    ]

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

    inverter_device_info = DeviceInfo(
        identifiers={(DOMAIN, "STORAGE", inverter_sn), (DOMAIN, inverter_sn)},  # type: ignore
        name=inverter_name,
        sw_version=inverter_sw,
        model=INVERTER_MODEL,
        manufacturer=NAME,
    )

    # Pre-populate current strategy from coordinator
    current_option: str | None = None
    try:
        oid = REGISTRY.get_by_name("power_mng.soc_strategy").object_id
        for coord in (static_coordinator, frequent_coordinator):
            resp = coord.get_latest_response(oid)
            if isinstance(resp, ValidApiResponse) and isinstance(resp.value, int):
                if 0 <= resp.value < len(SOC_STRATEGY_OPTIONS):
                    current_option = SOC_STRATEGY_OPTIONS[resp.value]
                break
    except Exception:
        pass

    async_add_entities(
        [
            RctPowerSocStrategyEntity(
                client=client,
                config_entry=entry,
                device_info=inverter_device_info,
                current_option=current_option,
            )
        ]
    )
