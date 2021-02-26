from dataclasses import dataclass
from typing import Callable, Dict, List

from .update_coordinator import RctPowerDataUpdateCoordinator


@dataclass
class RctPowerContext:
    update_coordinators: Dict["EntityUpdatePriority", RctPowerDataUpdateCoordinator]
    entity_descriptors: List["EntityDescriptor"]
    clean_up: Callable


from .entity import EntityDescriptor, EntityUpdatePriority  # noqa: E402
