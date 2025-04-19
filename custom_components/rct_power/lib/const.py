"""Constants for RCT Power."""

from __future__ import annotations

from enum import KEEP, IntFlag
from typing import Final

# Defaults
NUMERIC_STATE_DECIMAL_DIGITS: Final = 1
FREQUENCY_STATE_DECIMAL_DIGITS: Final = 3


class BatteryStatusFlag(IntFlag, boundary=KEEP):
    normal = 0
    charging = 2**3
    discharging = 2**10
    balancing = 2**11

    calibrating = charging | discharging
