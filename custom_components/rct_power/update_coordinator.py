from datetime import timedelta
from logging import Logger
from typing import Optional

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.helpers.update_coordinator import UpdateFailed

from .api import RctPowerApiClient, RctPowerData
from .const import DOMAIN


class RctPowerDataUpdateCoordinator(DataUpdateCoordinator[RctPowerData]):
    """Class to manage fetching data from the rct power inverter API."""

    def __init__(
        self,
        hass: HomeAssistant,
        logger: Logger,
        client: RctPowerApiClient,
        update_interval: Optional[timedelta] = None,
    ) -> None:
        self.client = client

        super().__init__(
            hass=hass, logger=logger, name=DOMAIN, update_interval=update_interval
        )

    async def _async_update_data(self):
        try:
            return await self.client.async_get_data()
        except Exception as exception:
            raise UpdateFailed() from exception
