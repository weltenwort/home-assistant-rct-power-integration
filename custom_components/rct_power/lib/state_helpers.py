from typing import Optional, Union

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.typing import StateType

from .api import ApiResponseValue
from .const import FREQUENCY_STATE_DECIMAL_DIGITS, NUMERIC_STATE_DECIMAL_DIGITS


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
        get_api_response_value_as_state(entity, value)
        for value in values
        if isinstance(value, (int, float))
    )


def get_first_api_response_value_as_binary_state(
    entity: BinarySensorEntity,
    values: list[Optional[ApiResponseValue]],
) -> Union[None, bool]:
    if len(values) <= 0:
        return None

    return get_api_response_value_as_binary_state(entity=entity, value=values[0])


def get_api_response_value_as_binary_state(
    entity: BinarySensorEntity,
    value: Optional[ApiResponseValue],
) -> Union[None, bool]:
    if value is None:
        return None
    return bool(value)


def get_battery_calibration_status(
    entity: BinarySensorEntity,
    values: list[Optional[ApiResponseValue]],
) -> Union[None, bool]:
    if len(values) <= 0:
        return None
    value = values[0]

    if isinstance(value, int):
        return value & 1032 != 0
    return None


def get_battery_balancing_status(
    entity: BinarySensorEntity,
    values: list[Optional[ApiResponseValue]],
) -> Union[None, bool]:
    if len(values) <= 0:
        return None
    value = values[0]

    if isinstance(value, int):
        return value & 2048 != 0
    return None
