from __future__ import annotations

from homeassistant.helpers.device_registry import DeviceInfo

from ..const import BATTERY_MODEL, DOMAIN, INVERTER_MODEL, NAME
from .entity import RctPowerEntity


def get_inverter_device_info(entity: RctPowerEntity) -> DeviceInfo:
    inverter_sn = str(entity.get_valid_api_response_value_by_name("inverter_sn", None))

    return DeviceInfo(
        identifiers={
            (
                DOMAIN,
                "STORAGE",
                inverter_sn,
            ),
            (
                DOMAIN,
                inverter_sn,
            ),
        },  # type: ignore
        name=str(
            entity.get_valid_api_response_value_by_name("android_description", ""),
        ),
        sw_version=str(entity.get_valid_api_response_value_by_name("svnversion", "")),
        model=INVERTER_MODEL,
        manufacturer=NAME,
    )


def get_battery_device_info(entity: RctPowerEntity) -> DeviceInfo:
    bms_sn = str(entity.get_valid_api_response_value_by_name("battery.bms_sn", None))

    return DeviceInfo(
        identifiers={
            (
                DOMAIN,
                "BATTERY",
                bms_sn,
            ),
            (
                DOMAIN,
                bms_sn,
            ),
        },  # type: ignore
        name=f"Battery at {entity.get_valid_api_response_value_by_name('android_description', '')}",
        sw_version=str(
            entity.get_valid_api_response_value_by_name(
                "battery.bms_software_version", ""
            )
        ),
        model=BATTERY_MODEL,
        manufacturer=NAME,
        via_device=(
            DOMAIN,
            str(entity.get_valid_api_response_value_by_name("inverter_sn", None)),
        ),
    )
