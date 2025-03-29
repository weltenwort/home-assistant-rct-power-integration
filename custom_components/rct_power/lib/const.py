"""Constants for RCT Power."""

from __future__ import annotations

# Base component constants
from enum import KEEP, Enum, IntFlag, auto

NAME = "RCT Power"
DOMAIN = "rct_power"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.14.1"

# Inverter
INVERTER_MODEL = "RCT Power Storage"

# Battery
BATTERY_MODEL = "RCT Power Battery"

# Icons
ICON = "mdi:solar-power"

# Platforms
BINARY_SENSOR = "binary_sensor"
SENSOR = "sensor"
PLATFORMS = [SENSOR]

# Configuration and options
CONF_ENABLED = "enabled"
CONF_HOSTNAME = "hostname"
CONF_PORT = "port"
CONF_SCAN_INTERVAL = "scan_interval"

# Defaults
DEFAULT_NAME = DOMAIN

NUMERIC_STATE_DECIMAL_DIGITS = 1
FREQUENCY_STATE_DECIMAL_DIGITS = 3


class EntityUpdatePriority(Enum):
    FREQUENT = auto()
    INFREQUENT = auto()
    STATIC = auto()


class BatteryStatusFlag(IntFlag, boundary=KEEP):
    normal = 0
    charging = 2**3
    discharging = 2**10
    balancing = 2**11

    calibrating = charging | discharging
