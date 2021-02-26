"""Constants for RCT Power."""
# Base component constants
NAME = "RCT Power"
DOMAIN = "rct_power"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.2.0"

ISSUE_URL = "https://github.com/weltenwort/rct-power/issues"

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

STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
