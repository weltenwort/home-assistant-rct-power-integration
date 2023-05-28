from typing import Literal, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.typing import StateType

from .api import ApiResponseValue
from .const import (
    FREQUENCY_STATE_DECIMAL_DIGITS,
    NUMERIC_STATE_DECIMAL_DIGITS,
    BatteryStatusFlag,
)


def get_first_api_response_value_as_state(
    entity: SensorEntity,
    values: list[Optional[ApiResponseValue]],
) -> StateType:
    if len(values) <= 0:
        return None

    return get_api_response_value_as_state(entity=entity, value=values[0])


def get_api_response_value_as_state(
    entity: SensorEntity,
    value: Optional[ApiResponseValue],
) -> StateType:
    if isinstance(value, bytes):
        return value.hex()

    if isinstance(value, tuple):
        return None

    if isinstance(value, (int, float)) and entity.native_unit_of_measurement == "%":
        return round(value * 100, NUMERIC_STATE_DECIMAL_DIGITS)

    if isinstance(value, (int, float)) and entity.native_unit_of_measurement == "Hz":
        return round(value, FREQUENCY_STATE_DECIMAL_DIGITS)

    if isinstance(value, (int, float)):
        return round(value, NUMERIC_STATE_DECIMAL_DIGITS)

    return value


def get_first_api_reponse_value_as_absolute_state(
    entity: SensorEntity,
    values: list[Optional[ApiResponseValue]],
) -> StateType:
    value = get_first_api_response_value_as_state(entity=entity, values=values)

    if isinstance(value, (int, float)):
        return abs(value)

    return value


def sum_api_response_values_as_state(
    entity: SensorEntity,
    values: list[Optional[ApiResponseValue]],
) -> StateType:
    return sum(
        (
            float(state_value)
            for value in values
            if isinstance(
                state_value := get_api_response_value_as_state(entity, value),
                (int, float),
            )
        ),
        0.0,
    )


#
# Battery status
#

BatteryStatus = Literal["normal", "calibrating", "balancing"]


def get_api_response_value_as_battery_status(
    entity: SensorEntity,
    value: Optional[ApiResponseValue],
) -> BatteryStatus | None:
    if not isinstance(value, int):
        return None

    match BatteryStatusFlag(value):
        case BatteryStatusFlag.calibrating:
            return "calibrating"
        case BatteryStatusFlag.balancing:
            return "balancing"
        case _:
            return "normal"

    return None


def get_first_api_response_value_as_battery_status(
    entity: SensorEntity,
    values: list[Optional[ApiResponseValue]],
) -> BatteryStatus | None:
    match values:
        case [firstValue, *_] if firstValue is not None:
            return get_api_response_value_as_battery_status(entity, firstValue)
        case _:
            return None
