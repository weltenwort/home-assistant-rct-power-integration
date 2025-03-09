from __future__ import annotations

from asyncio.tasks import gather

from homeassistant.core import callback
from homeassistant.helpers.entity import Entity

from .update_coordinator import RctPowerDataUpdateCoordinator


class MultiCoordinatorEntity(Entity):
    """A class for entities using multiple DataUpdateCoordinators."""

    _attr_should_poll = False

    def __init__(self, coordinators: list[RctPowerDataUpdateCoordinator]) -> None:
        self.coordinators = coordinators

    @property
    def available(self) -> bool:
        return any(coordinator.last_update_success for coordinator in self.coordinators)

    async def async_added_to_hass(self) -> None:
        await super().async_added_to_hass()

        for coordinator in self.coordinators:
            self.async_on_remove(
                coordinator.async_add_listener(self._handle_coordinator_update)
            )

    @callback
    def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()

    async def async_update(self) -> None:
        # Ignore manual update requests if the entity is disabled
        if not self.enabled:
            return

        await gather(
            *[coordinator.async_request_refresh() for coordinator in self.coordinators]
        )
