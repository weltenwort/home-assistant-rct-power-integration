"""Adds config flow for RCT Power."""
from dataclasses import asdict
from voluptuous.error import MultipleInvalid
from custom_components.rct_power.entry import RctPowerConfigEntryData
from typing import TypedDict
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import RctPowerApiClient

# from .const import CONF_PASSWORD
# from .const import CONF_USERNAME
from .const import DOMAIN
from .const import PLATFORMS


class RctPowerFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for rct_power."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            try:
                valid_user_input = RctPowerConfigEntryData.from_user_input(user_input)

                unique_id = await RctPowerApiClient(
                    valid_user_input.hostname, valid_user_input.port
                ).get_serial_number()

                if unique_id != None:
                    await self.async_set_unique_id(unique_id)

                    return self.async_create_entry(
                        title=f"Inverter at {valid_user_input.hostname}:{valid_user_input.port}",
                        data=asdict(valid_user_input),
                    )
                else:
                    errors[
                        "base"
                    ] = f"Faild to connect to {valid_user_input.hostname}:{valid_user_input.port}."

            except MultipleInvalid as exc:
                errors["base"] = str(exc)

        return await self._show_config_form(user_input, errors)

    async def _show_config_form(
        self, user_input, errors
    ):  # pylint: disable=unused-argument
        """Show the configuration form to edit location data."""
        return self.async_show_form(
            step_id="user",
            data_schema=RctPowerConfigEntryData.get_schema(),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return RctPowerOptionsFlowHandler(config_entry)


class RctPowerOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for rct_power."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):  # pylint: disable=unused-argument
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            self.options.update(user_input)
            return await self._update_options()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(x, default=self.options.get(x, True)): bool
                    for x in sorted(PLATFORMS)
                }
            ),
        )

    async def _update_options(self):
        """Update config entry options."""
        return self.async_create_entry(
            title=self.config_entry.data.get(CONF_USERNAME), data=self.options
        )
