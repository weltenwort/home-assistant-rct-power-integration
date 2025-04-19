"""Adds config flow for RCT Power."""

from __future__ import annotations

from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry, ConfigFlowResult
from homeassistant.const import CONF_PORT
from homeassistant.core import callback

from .const import (
    CONF_ENTITY_PREFIX,
    CONF_HOSTNAME,
    DEFAULT_ENTITY_PREFIX,
    DEFAULT_PORT,
    DOMAIN,
    ConfScanInterval,
    ScanIntervalDefault,
)
from .lib.api import RctPowerApiClient


class RctPowerFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for rct_power."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle a flow initialized by the user."""
        errors: dict[str, str] = {}

        if user_input is not None:
            client = RctPowerApiClient(
                hostname=user_input[CONF_HOSTNAME],
                port=user_input[CONF_PORT],
            )
            serial_number = await client.get_serial_number()

            if serial_number is not None:
                await self.async_set_unique_id(serial_number)

                return self.async_create_entry(
                    title=self.get_title(user_input),
                    data=user_input,
                )
            else:
                errors["base"] = "connect"

        return self.async_show_form(
            step_id="user",
            data_schema=CONFIG_FLOW_SCHEMA,
            errors=errors,
        )

    @staticmethod
    def get_title(user_input: dict[str, Any]) -> str:
        return (
            f"RCT Power Inverter at {user_input[CONF_HOSTNAME]}:{user_input[CONF_PORT]}"
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> RctPowerOptionsFlowHandler:
        return RctPowerOptionsFlowHandler()


class RctPowerOptionsFlowHandler(config_entries.OptionsFlow):
    """Config flow options handler for rct_power."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the options."""
        return await self.async_step_user(user_input=user_input)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(
                OPTIONS_SCHEMA, self.config_entry.options
            ),
        )


CONFIG_FLOW_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOSTNAME): str,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Optional(CONF_ENTITY_PREFIX, default=DEFAULT_ENTITY_PREFIX): str,
    }
)


OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Optional(
            ConfScanInterval.FREQUENT.value, default=ScanIntervalDefault.FREQUENT
        ): cv.positive_int,
        vol.Optional(
            ConfScanInterval.INFREQUENT.value, default=ScanIntervalDefault.INFREQUENT
        ): cv.positive_int,
        vol.Optional(
            ConfScanInterval.STATIC.value, default=ScanIntervalDefault.STATIC
        ): cv.positive_int,
    }
)
