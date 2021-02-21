from dataclasses import dataclass
from typing import Callable

from .update_coordinator import RctPowerDataUpdateCoordinator


@dataclass
class RctPowerContext:
    coordinator: RctPowerDataUpdateCoordinator
    clean_up: Callable
