"""
Custom integration to integrate RCT Power with Home Assistant.

For more details about this integration, please refer to
https://github.com/weltenwort/rct-power
"""
import asyncio
from datetime import timedelta
import logging
from typing import Callable, cast

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
from .lib.entities import known_entities
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
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})
        _LOGGER.info(STARTUP_MESSAGE)

    config_entry_data = RctPowerConfigEntryData.from_config_entry(entry)
    config_entry_options = RctPowerConfigEntryOptions.from_config_entry(entry)

    client = RctPowerApiClient(
        hostname=config_entry_data.hostname, port=config_entry_data.port
    )

    frequent_update_coordinator = RctPowerDataUpdateCoordinator(
        hass=hass,
        logger=_LOGGER,
        name=f"{DOMAIN} {entry.unique_id} frequent",
        update_interval=timedelta(seconds=config_entry_options.frequent_scan_interval),
        entity_descriptors=[
            entity_descriptor
            for entity_descriptor in known_entities
            if entity_descriptor.update_priority == EntityUpdatePriority.FREQUENT
        ],
        client=client,
    )

    infrequent_update_coordinator = RctPowerDataUpdateCoordinator(
        hass=hass,
        logger=_LOGGER,
        name=f"{DOMAIN} {entry.unique_id} infrequent",
        update_interval=timedelta(
            seconds=config_entry_options.infrequent_scan_interval
        ),
        entity_descriptors=[
            entity_descriptor
            for entity_descriptor in known_entities
            if entity_descriptor.update_priority == EntityUpdatePriority.INFREQUENT
        ],
        client=client,
    )

    static_update_coordinator = RctPowerDataUpdateCoordinator(
        hass=hass,
        logger=_LOGGER,
        name=f"{DOMAIN} {entry.unique_id} static",
        update_interval=timedelta(seconds=config_entry_options.static_scan_interval),
        entity_descriptors=[
            entity_descriptor
            for entity_descriptor in known_entities
            if entity_descriptor.update_priority == EntityUpdatePriority.STATIC
        ],
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
        hass.async_add_job(
            cast(
                Callable, hass.config_entries.async_forward_entry_setup(entry, platform)
            )
        )

    hass.data[DOMAIN][entry.entry_id] = RctPowerContext(
        update_coordinators={
            EntityUpdatePriority.FREQUENT: frequent_update_coordinator,
            EntityUpdatePriority.INFREQUENT: infrequent_update_coordinator,
            EntityUpdatePriority.STATIC: static_update_coordinator,
        },
        entity_descriptors=known_entities,
        clean_up=remove_update_listener,
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Handle removal of an entry."""

    context = hass.data[DOMAIN][entry.entry_id]

    if not isinstance(context, RctPowerContext):
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
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
