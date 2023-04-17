"""
Custom integration to integrate RCT Power with Home Assistant.

For more details about this integration, please refer to
https://github.com/weltenwort/home-assistant-rct-power-integration
"""
import asyncio
from datetime import timedelta
import logging
from typing import Any, Callable, cast

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import Config
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .lib.api import RctPowerApiClient
from .lib.const import (
    DOMAIN,
    PLATFORMS,
    STARTUP_MESSAGE,
)
from .lib.context import RctPowerContext
from .lib.domain_data import get_domain_data
from .lib.entities import all_entity_descriptions
from .lib.entity import EntityUpdatePriority
from .lib.entry import RctPowerConfigEntryData, RctPowerConfigEntryOptions
from .lib.update_coordinator import RctPowerDataUpdateCoordinator

SCAN_INTERVAL = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__package__)


async def async_setup(hass: HomeAssistant, config: Config):
    """Set up this integration using YAML is not supported."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up this integration using UI."""
    if len(domain_data := get_domain_data(hass)) == 0:
        _LOGGER.info(STARTUP_MESSAGE)

    config_entry_data = RctPowerConfigEntryData.from_config_entry(entry)
    config_entry_options = RctPowerConfigEntryOptions.from_config_entry(entry)

    client = RctPowerApiClient(
        hostname=config_entry_data.hostname, port=config_entry_data.port
    )

    frequently_updated_object_ids = list(
        {
            object_info.object_id
            for entity_description in all_entity_descriptions
            if entity_description.update_priority == EntityUpdatePriority.FREQUENT
            for object_info in entity_description.object_infos
        }
    )
    frequent_update_coordinator = RctPowerDataUpdateCoordinator(
        hass=hass,
        logger=_LOGGER,
        name=f"{DOMAIN} {entry.unique_id} frequent",
        update_interval=timedelta(seconds=config_entry_options.frequent_scan_interval),
        object_ids=frequently_updated_object_ids,
        client=client,
    )

    infrequently_updated_object_ids = list(
        {
            object_info.object_id
            for entity_description in all_entity_descriptions
            if entity_description.update_priority == EntityUpdatePriority.INFREQUENT
            for object_info in entity_description.object_infos
        }
    )
    infrequent_update_coordinator = RctPowerDataUpdateCoordinator(
        hass=hass,
        logger=_LOGGER,
        name=f"{DOMAIN} {entry.unique_id} infrequent",
        update_interval=timedelta(
            seconds=config_entry_options.infrequent_scan_interval
        ),
        object_ids=infrequently_updated_object_ids,
        client=client,
    )

    static_object_ids = list(
        {
            object_info.object_id
            for entity_description in all_entity_descriptions
            if entity_description.update_priority == EntityUpdatePriority.STATIC
            for object_info in entity_description.object_infos
        }
    )
    static_update_coordinator = RctPowerDataUpdateCoordinator(
        hass=hass,
        logger=_LOGGER,
        name=f"{DOMAIN} {entry.unique_id} static",
        update_interval=timedelta(seconds=config_entry_options.static_scan_interval),
        object_ids=static_object_ids,
        client=client,
    )

    await frequent_update_coordinator.async_refresh()
    await infrequent_update_coordinator.async_refresh()
    await static_update_coordinator.async_refresh()

    if not (
        frequent_update_coordinator.last_update_success
        and infrequent_update_coordinator.last_update_success
        and static_update_coordinator.last_update_success
    ):
        raise ConfigEntryNotReady

    remove_update_listener = entry.add_update_listener(async_reload_entry)

    for platform in PLATFORMS:
        hass.async_add_job(  # type: ignore
            cast(
                Callable[[Any, Any], Any],
                hass.config_entries.async_forward_entry_setup(entry, platform),
            )
        )

    domain_data[entry.entry_id] = RctPowerContext(
        update_coordinators={
            EntityUpdatePriority.FREQUENT: frequent_update_coordinator,
            EntityUpdatePriority.INFREQUENT: infrequent_update_coordinator,
            EntityUpdatePriority.STATIC: static_update_coordinator,
        },
        clean_up=remove_update_listener,
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""
    if (context := RctPowerContext.get_from_domain_data(hass, entry)) is None:
        return False

    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )

    if unloaded:
        context.clean_up()
        context.remove_from_domain_data(hass, entry)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
