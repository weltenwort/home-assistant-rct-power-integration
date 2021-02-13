"""RctPowerEntity class"""
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from rctclient.registry import REGISTRY

from .const import ATTRIBUTION, DOMAIN, NAME, VERSION


class RctPowerEntity(CoordinatorEntity):
    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        config_entry: ConfigEntry,
        object_id: int,
    ):
        super().__init__(coordinator)
        self.config_entry = config_entry
        self.object_id = object_id
        self.object_info = REGISTRY.get_by_id(self.object_id)

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.config_entry.entry_id

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.unique_id)},
            "name": NAME,
            "model": VERSION,
            "manufacturer": NAME,
        }

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "id": str(self.coordinator.data.get("id")),
            "integration": DOMAIN,
        }

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return None
