from __future__ import annotations

from datetime import datetime, timedelta
from heapq import heappop, heappush
from logging import Logger

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .api import (
    ApiResponse,
    ApiResponseValue,
    ObjectId,
    RctPowerApiClient,
    RctPowerData,
    RctPowerPersistentApiClient,
    ValidApiResponse,
)


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

    def get_valid_value_or(self, object_id: int, default_value: ApiResponseValue):
        latest_response = self.get_latest_response(object_id)

        if isinstance(latest_response, ValidApiResponse):
            return latest_response.value
        else:
            return default_value

    def has_valid_value(self, object_id: int):
        return isinstance(self.get_latest_response(object_id), ValidApiResponse)

    async def _async_update_data(self):
        return await self.client.async_get_data(object_ids=self.object_ids)


class ListenerSubscription(NamedTuple):
    """A subscription to a data update coordinator."""

    object_id: ObjectId
    listener: Callable[[ObjectId, ApiResponseValue], None]
    maximum_passive_age: timedelta


class QueuedRequest(NamedTuple):
    """A request that has been queued for fetching from the inverter at a future
    point in time."""

    timestamp: datetime
    object_id: ObjectId


class RctPowerCooperativeDataUpdateCoordinator:
    """Class to manage fetching data from the rct power inverter API more efficiently.

    This data update coordinator is designed to be as non-intrusive as possible
    in regard to the inverter's network traffic. It will continuously listen for
    updates from the inverter and only request object ids from the inverter when
    they haven't been passively observed in the meantime.
    """

    def __init__(
        self,
        hass: HomeAssistant,
        name: str,
        logger: Logger,
        config_entry: ConfigEntry,
        client: RctPowerPersistentApiClient,
        # update_interval: Optional[timedelta] = None,
    ) -> None:
        self.client = client
        self.config_entry = config_entry
        self.hass = hass
        self.logger = logger
        self.name = name
        # self.update_interval = update_interval

        self.latest_responses_by_object_id: dict[ObjectId, ApiResponse] = {}
        self._subscriptions_by_object_id: dict[
            ObjectId, list[ListenerSubscription]
        ] = {}
        self._next_requests_heap: list[QueuedRequest] = []

        self.config_entry.async_on_unload(self.async_shutdown)

    async def async_shutdown(self) -> None:
        await self.client.async_shutdown()

    async def async_request_updates(self) -> None:
        if not self._next_requests_heap:
            # no requests have been queued, so don't do anything
            return

        now = dt_util.utcnow()

        while self._next_requests_heap[0].timestamp <= now:
            next_request = heappop(self._next_requests_heap)

            previous_response = self.latest_responses_by_object_id.get(
                next_request.object_id
            )
            soonest_subscription = self.get_soonest_subscription(next_request.object_id)

            if soonest_subscription is None:
                # no subscriptions for this object id, so don't do anything
                continue

            if (
                previous_response is None
                or previous_response.time + soonest_subscription.maximum_passive_age
                > now
            ):
                await self.client.async_request_object_data([next_request.object_id])

            # schedule the next request for this object id
            heappush(
                self._next_requests_heap,
                QueuedRequest(
                    timestamp=now + soonest_subscription.maximum_passive_age,
                    object_id=next_request.object_id,
                ),
            )

    def get_soonest_subscription(
        self, object_id: ObjectId
    ) -> Optional[ListenerSubscription]:
        subscriptions = self._subscriptions_by_object_id.get(object_id)

        if subscriptions:
            return min(subscriptions, default=None, key=lambda s: s.maximum_passive_age)
