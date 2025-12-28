"""
Custom integration to integrate RCT Power with Home Assistant.

For more details about this integration, please refer to
https://github.com/weltenwort/home-assistant-rct-power-integration
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.util.hass_dict import HassEntryKey

from .const import (
    CONF_HOSTNAME,
    DOMAIN,
    PLATFORMS,
    ConfScanInterval,
    EntityUpdatePriority,
    ScanIntervalDefault,
)
from .coordinator import RctPowerDataUpdateCoordinator
from .lib.api import RctPowerApiClient
from .lib.entities import all_entity_descriptions
from .lib.entity import resolve_object_infos
from .models import RctConfEntryData, RctConfEntryOptions

RCT_DATA_KEY: HassEntryKey[RctData] = HassEntryKey(DOMAIN)

type RctConfigEntry = ConfigEntry[RctData]


@dataclass
class RctData:
    update_coordinators: dict[EntityUpdatePriority, RctPowerDataUpdateCoordinator]


def object_ids_for_update_priority(update_priority: EntityUpdatePriority) -> list[int]:
    """Collect all object_ids for an update_priority."""
    return list(
        {
            object_info.object_id
            for entity_description in all_entity_descriptions
            if entity_description.update_priority == update_priority
            for object_info in resolve_object_infos(entity_description)
        }
    )


async def async_setup_entry(hass: HomeAssistant, entry: RctConfigEntry) -> bool:
    """Set up this integration using UI."""
    data = cast(RctConfEntryData, entry.data)
    options = cast(RctConfEntryOptions, entry.options)

    client = RctPowerApiClient(
        hostname=data[CONF_HOSTNAME],
        port=data[CONF_PORT],
    )

    frequent_update_coordinator = RctPowerDataUpdateCoordinator(
        hass=hass,
        entry=entry,
        client=client,
        name_suffix="frequent",
        object_ids=object_ids_for_update_priority(EntityUpdatePriority.FREQUENT),
        update_interval=options.get(
            ConfScanInterval.FREQUENT, ScanIntervalDefault.FREQUENT
        ),
    )

    infrequent_update_coordinator = RctPowerDataUpdateCoordinator(
        hass=hass,
        entry=entry,
        client=client,
        name_suffix="infrequent",
        object_ids=object_ids_for_update_priority(EntityUpdatePriority.INFREQUENT),
        update_interval=options.get(
            ConfScanInterval.INFREQUENT, ScanIntervalDefault.INFREQUENT
        ),
    )

    static_update_coordinator = RctPowerDataUpdateCoordinator(
        hass=hass,
        entry=entry,
        client=client,
        name_suffix="static",
        object_ids=object_ids_for_update_priority(EntityUpdatePriority.STATIC),
        update_interval=options.get(
            ConfScanInterval.STATIC, ScanIntervalDefault.STATIC
        ),
    )

    await frequent_update_coordinator.async_config_entry_first_refresh()
    await infrequent_update_coordinator.async_config_entry_first_refresh()
    await static_update_coordinator.async_config_entry_first_refresh()

    entry.runtime_data = RctData(
        {
            EntityUpdatePriority.FREQUENT: frequent_update_coordinator,
            EntityUpdatePriority.INFREQUENT: infrequent_update_coordinator,
            EntityUpdatePriority.STATIC: static_update_coordinator,
        }
    )

    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: RctConfigEntry) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: RctConfigEntry) -> None:
    """Reload config entry."""
    await hass.config_entries.async_reload(entry.entry_id)
