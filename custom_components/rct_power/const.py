from __future__ import annotations

import logging
from enum import IntEnum, StrEnum
from typing import Final

LOGGER = logging.getLogger(__package__)

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
