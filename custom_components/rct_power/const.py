from __future__ import annotations

import logging
from enum import Enum, IntEnum, StrEnum
from typing import Final

from homeassistant.const import Platform

LOGGER = logging.getLogger(__package__)

DOMAIN: Final = "rct_power"
ICON: Final = "mdi:solar-power"
PLATFORMS: Final = [Platform.SENSOR]

NAME: Final = "RCT Power"
INVERTER_MODEL: Final = "RCT Power Storage"
BATTERY_MODEL: Final = "RCT Power Battery"


class EntityUpdatePriority(Enum):
    FREQUENT = 1
    INFREQUENT = 2
    STATIC = 3


# Configuration, options, defaults
CONF_ENTITY_PREFIX: Final = "entity_prefix"
CONF_HOSTNAME: Final = "hostname"

DEFAULT_ENTITY_PREFIX: Final = "RCT Power Storage"
DEFAULT_PORT: Final = 8899


class ConfScanInterval(StrEnum):
    FREQUENT = "frequent_scan_interval"
    INFREQUENT = "infrequent_scan_interval"
    STATIC = "static_scan_interval"


class ScanIntervalDefault(IntEnum):
    FREQUENT = 30
    INFREQUENT = 60 * 3
    STATIC = 60 * 60
