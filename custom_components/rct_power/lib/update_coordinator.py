from __future__ import annotations

from datetime import timedelta
from logging import Logger

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import ApiResponseValue, RctPowerApiClient, RctPowerData, ValidApiResponse


class RctPowerDataUpdateCoordinator(DataUpdateCoordinator[RctPowerData]):
    """Class to manage fetching data from the rct power inverter API."""

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        logger: Logger,
        client: RctPowerApiClient,
        object_ids: list[int],
        update_interval: timedelta | None = None,
    ) -> None:
        self.client = client
        self.object_ids = object_ids

        super().__init__(
            hass=hass, logger=logger, name=name, update_interval=update_interval
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
