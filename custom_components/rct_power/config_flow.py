"""Adds config flow for RCT Power."""

from dataclasses import asdict
from logging import Logger, getLogger

from homeassistant import config_entries
from homeassistant.core import callback
from voluptuous.error import MultipleInvalid

from .lib.api import RctPowerApiClient
from .lib.const import DOMAIN
from .lib.entry import RctPowerConfigEntryData, RctPowerConfigEntryOptions, get_title


_LOGGER: Logger = getLogger(__package__)


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

                if unique_id is not None:
                    await self.async_set_unique_id(unique_id)

                    return self.async_create_entry(
                        title=get_title(valid_user_input),
                        data=asdict(valid_user_input),
                    )
                else:
                    errors["base"] = "connect"

            except MultipleInvalid as exc:
                errors.update({err.path: err.msg for err in exc.errors})

        return self.async_show_form(
            step_id="user",
            data_schema=RctPowerConfigEntryData.get_schema(),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        return RctPowerOptionsFlowHandler(config_entry)


class RctPowerOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for rct_power."""

    def __init__(self, config_entry):
        """Initialize HACS options flow."""
        self.config_entry = config_entry
        self.options = dict(config_entry.options)

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user(user_input=user_input)

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        errors = {}

        if user_input is not None:
            try:
                valid_user_input = RctPowerConfigEntryOptions.from_user_input(
                    user_input
                )

                self.options.update(asdict(valid_user_input))
                return self.async_create_entry(
                    title=get_title(
                        RctPowerConfigEntryData.from_config_entry(self.config_entry)
                    ),
                    data=self.options,
                )
            except MultipleInvalid as exc:
                errors.update({err.path: err.msg for err in exc.errors})

        return self.async_show_form(
            step_id="user",
            data_schema=RctPowerConfigEntryOptions.get_schema(),
            errors=errors,
        )
