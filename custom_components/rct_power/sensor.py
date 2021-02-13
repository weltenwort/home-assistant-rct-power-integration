"""Sensor platform for RCT Power."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from rctclient.registry import REGISTRY

from .const import DEFAULT_NAME, DOMAIN, ICON, SENSOR
from .context import RctPowerContext
from .entity import RctPowerEntity


INVERTER_SN_OID = 0x7924ABD9


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    context = hass.data[DOMAIN][entry.entry_id]

    if not isinstance(context, RctPowerContext):
        return False

    enabled_object_ids = [INVERTER_SN_OID]

    async_add_devices(
        [
            RctPowerSensor(
                coordinator=context.coordinator, config_entry=entry, object_id=object_id
            )
            for object_id in enabled_object_ids
        ]
    )


class RctPowerSensor(RctPowerEntity):
    """rct_power Sensor class."""

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{DOMAIN}_{SENSOR}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.coordinator.data.get("body")

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return ICON

    @property
    def device_class(self):
        """Return the device class of the sensor."""
        return None
