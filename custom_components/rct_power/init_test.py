"""Test RCT Power setup process."""

from __future__ import annotations

import pytest
from homeassistant.const import CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.rct_power import RctData, async_setup_entry
from custom_components.rct_power.const import (
    CONF_ENTITY_PREFIX,
    CONF_HOSTNAME,
    DEFAULT_ENTITY_PREFIX,
    DEFAULT_PORT,
    DOMAIN,
)


# We can pass fixtures as defined in conftest.py to tell pytest to use the fixture
# for a given test. We can also leverage fixtures and mocks that are available in
# Home Assistant using the pytest_homeassistant_custom_component plugin.
# Assertions allow you to verify that the return value of whatever is on the left
# side of the assertion matches with the right side.
@pytest.mark.usefixtures("bypass_get_data")
async def test_setup_unload_and_reload_entry(hass: HomeAssistant) -> None:
    """Test entry setup and unload."""
    # Create a mock entry so we don't have to go through config flow
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOSTNAME: "localhost",
            CONF_PORT: DEFAULT_PORT,
            CONF_ENTITY_PREFIX: DEFAULT_ENTITY_PREFIX,
        },
        entry_id="test",
    )

    config_entry.add_to_hass(hass)
    # Set up the entry and assert that the values set during setup are where we expect
    # them to be. Because we have patched the RctPowerDataUpdateCoordinator.async_get_data
    # call, no code from custom_components/rct_power/api.py actually runs.
    assert await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()
    assert isinstance(config_entry.runtime_data, RctData)

    # Reload the entry and assert that the data from above is still there
    assert await hass.config_entries.async_reload(config_entry.entry_id)
    await hass.async_block_till_done()
    assert isinstance(config_entry.runtime_data, RctData)


@pytest.mark.usefixtures("error_on_get_data")
async def test_setup_entry_exception(hass: HomeAssistant) -> None:
    """Test ConfigEntryNotReady when API raises an exception during entry setup."""
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            CONF_HOSTNAME: "localhost",
            CONF_PORT: DEFAULT_PORT,
            CONF_ENTITY_PREFIX: DEFAULT_ENTITY_PREFIX,
        },
        entry_id="test",
    )

    # In this case we are testing the condition where async_setup_entry raises
    # ConfigEntryNotReady using the `error_on_get_data` fixture which simulates
    # an error.
    with pytest.raises(ConfigEntryNotReady):
        assert await async_setup_entry(hass, config_entry)
