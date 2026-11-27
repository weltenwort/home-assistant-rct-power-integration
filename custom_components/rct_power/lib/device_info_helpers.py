from __future__ import annotations

from homeassistant.helpers import device_registry as dr
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
        via_device_id=_get_inverter_device_id(entity),
    )


def _get_inverter_device_id(entity: RctPowerEntity) -> str | None:
    """Return the device registry id of the inverter the battery belongs to."""
    inverter_sn = entity.get_valid_api_response_value_by_name("inverter_sn", None)
    if inverter_sn is None:
        # Don't link to a device registered under the serial number "None"
        return None

    identifier = (DOMAIN, str(inverter_sn))
    device_registry = dr.async_get(entity.hass)

    if hasattr(device_registry, "async_get_device_by_identifier"):
        device = device_registry.async_get_device_by_identifier(
            identifier, entity.config_entry.entry_id
        )
    else:  # HA < 2026.9
        device = device_registry.async_get_device(identifiers={identifier})

    return device.id if device else None
