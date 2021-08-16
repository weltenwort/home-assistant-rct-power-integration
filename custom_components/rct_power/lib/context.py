from dataclasses import dataclass
from typing import Callable, Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import EntityUpdatePriority
from .domain_data import get_domain_data
from .update_coordinator import RctPowerDataUpdateCoordinator


@dataclass
class RctPowerContext:
    update_coordinators: Dict[EntityUpdatePriority, RctPowerDataUpdateCoordinator]
    clean_up: Callable[[], None]

    @classmethod
    def get_from_domain_data(cls, hass: HomeAssistant, config_entry: ConfigEntry):
        domain_data = get_domain_data(hass)

        if isinstance(context := domain_data[config_entry.entry_id], RctPowerContext):
            return context

        return None

    def put_to_domain_data(self, hass: HomeAssistant, config_entry: ConfigEntry):
        domain_data = get_domain_data(hass)

        domain_data[config_entry.entry_id] = self

    def remove_from_domain_data(self, hass: HomeAssistant, config_entry: ConfigEntry):
        domain_data = get_domain_data(hass)

        domain_data.pop(config_entry.entry_id)
