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
import voluptuous as vol

from .api import RctPowerApiClient, RctPowerData
from .const import CONF_HOSTNAME, CONF_PORT, CONF_SCAN_INTERVAL, DOMAIN
from .const import PLATFORMS
from .const import STARTUP_MESSAGE
from .context import RctPowerContext
from .update_coordinator import RctPowerDataUpdateCoordinator

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

    hostname = cast(str, vol.Schema(str)(entry.data.get(CONF_HOSTNAME)))
    port = cast(int, vol.Schema(int)(entry.data.get(CONF_PORT)))
    scan_interval = cast(int, vol.Schema(int)(entry.data.get(CONF_SCAN_INTERVAL)))

    client = RctPowerApiClient(hostname=hostname, port=port)

    coordinator = RctPowerDataUpdateCoordinator(
        hass=hass,
        logger=_LOGGER,
        update_interval=timedelta(seconds=scan_interval),
        client=client,
    )

    await coordinator.async_refresh()

    if not coordinator.last_update_success:
        raise ConfigEntryNotReady

    hass.data[DOMAIN][entry.entry_id] = RctPowerContext(coordinator=coordinator)

    for platform in PLATFORMS:
        hass.async_add_job(
            cast(
                Callable, hass.config_entries.async_forward_entry_setup(entry, platform)
            )
        )

    entry.add_update_listener(async_reload_entry)

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
        hass.data[DOMAIN].pop(entry.entry_id)

    return unloaded


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
