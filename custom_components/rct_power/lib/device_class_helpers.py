from homeassistant.const import (
    ELECTRIC_CURRENT_AMPERE,
    ELECTRIC_CURRENT_MILLIAMPERE,
    ELECTRIC_POTENTIAL_MILLIVOLT,
    ELECTRIC_POTENTIAL_VOLT,
    ENERGY_KILO_WATT_HOUR,
    ENERGY_WATT_HOUR,
    POWER_KILO_WATT,
    POWER_VOLT_AMPERE,
    POWER_WATT,
    TEMP_CELSIUS,
    TEMP_FAHRENHEIT,
    TEMP_KELVIN,
)

from homeassistant.components.sensor import SensorDeviceClass


def guess_device_class_from_unit(unit: str):
    if unit in [TEMP_CELSIUS, TEMP_FAHRENHEIT, TEMP_KELVIN]:
        return SensorDeviceClass.TEMPERATURE
    elif unit in [
        ELECTRIC_POTENTIAL_VOLT,
        ELECTRIC_POTENTIAL_MILLIVOLT,
    ]:
        return SensorDeviceClass.VOLTAGE
    elif unit in [
        ELECTRIC_CURRENT_AMPERE,
        ELECTRIC_CURRENT_MILLIAMPERE,
    ]:
        return SensorDeviceClass.CURRENT
    elif unit in [
        POWER_WATT,
        POWER_KILO_WATT,
        POWER_VOLT_AMPERE,
    ]:
        return SensorDeviceClass.POWER
    elif unit in [ENERGY_KILO_WATT_HOUR, ENERGY_WATT_HOUR]:
        return SensorDeviceClass.ENERGY

    return None
