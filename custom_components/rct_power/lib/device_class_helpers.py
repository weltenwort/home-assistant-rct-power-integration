from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import (
    UnitOfApparentPower,
    UnitOfElectricCurrent,
    UnitOfElectricPotential,
    UnitOfEnergy,
    UnitOfPower,
    UnitOfTemperature,
)


def guess_device_class_from_unit(unit: str) -> SensorDeviceClass | None:
    if unit in [
        UnitOfTemperature.CELSIUS,
        UnitOfTemperature.FAHRENHEIT,
        UnitOfTemperature.KELVIN,
    ]:
        return SensorDeviceClass.TEMPERATURE
    elif unit in [
        UnitOfElectricPotential.VOLT,
        UnitOfElectricPotential.MILLIVOLT,
    ]:
        return SensorDeviceClass.VOLTAGE
    elif unit in [
        UnitOfElectricCurrent.AMPERE,
        UnitOfElectricCurrent.MILLIAMPERE,
    ]:
        return SensorDeviceClass.CURRENT
    elif unit in [
        UnitOfPower.WATT,
        UnitOfPower.KILO_WATT,
        UnitOfApparentPower.VOLT_AMPERE,
    ]:
        return SensorDeviceClass.POWER
    elif unit in [UnitOfEnergy.KILO_WATT_HOUR, UnitOfEnergy.WATT_HOUR]:
        return SensorDeviceClass.ENERGY

    return None
