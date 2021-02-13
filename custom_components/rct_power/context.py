from dataclasses import dataclass

from .update_coordinator import RctPowerDataUpdateCoordinator


@dataclass
class RctPowerContext:
    coordinator: RctPowerDataUpdateCoordinator
