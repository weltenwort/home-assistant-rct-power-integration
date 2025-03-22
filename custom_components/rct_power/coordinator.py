from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import LOGGER
from .lib.api import ApiResponseValue, RctPowerApiClient, RctPowerData, ValidApiResponse
from .lib.const import DOMAIN


class RctPowerDataUpdateCoordinator(DataUpdateCoordinator[RctPowerData]):
    """Class to manage fetching data from the rct power inverter API."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        *,
        name_suffix: str,
        client: RctPowerApiClient,
        object_ids: list[int],
        update_interval: timedelta | None = None,
    ) -> None:
        self.client = client
        self.object_ids = object_ids
        super().__init__(
            hass=hass,
            config_entry=entry,
            logger=LOGGER,
            name=f"{DOMAIN} {entry.unique_id} {name_suffix}",
            update_interval=update_interval,
        )

    def get_latest_response(self, object_id: int):
        if self.data is not None:  # pyright: ignore [reportUnnecessaryComparison]
            return self.data.get(object_id)
        return None

    def get_valid_value_or(self, object_id: int, default_value: ApiResponseValue):
        latest_response = self.get_latest_response(object_id)

        if isinstance(latest_response, ValidApiResponse):
            return latest_response.value
        return default_value

    def has_valid_value(self, object_id: int):
        return isinstance(self.get_latest_response(object_id), ValidApiResponse)

    async def _async_update_data(self):
        return await self.client.async_get_data(object_ids=self.object_ids)
