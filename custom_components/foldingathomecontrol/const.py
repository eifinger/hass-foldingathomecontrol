"""Constants for foldingathomecontrol."""
import logging

from homeassistant.const import Platform

# Base component constants
CLIENT = "client"
DOMAIN = "foldingathomecontrol"
DEFAULT_UPDATE_RATE = 5
DEFAULT_READ_TIMEOUT = 15
PLATFORMS = [Platform.SENSOR, Platform.BUTTON, Platform.SELECT]

# Logger
_LOGGER = logging.getLogger(__package__)

# Dispatchers
UNSUB_DISPATCHERS = "unsub_dispatchers"
DATA_UPDATED = f"{DOMAIN}_data_updated"
SENSOR_ADDED = f"{DOMAIN}_sensor_added"
SENSOR_REMOVED = f"{DOMAIN}_sensor_removed"

# Configuration
CONF_ADDRESS = "address"
CONF_PORT = "port"
CONF_PASSWORD = "password"  # nosec
CONF_UPDATE_RATE = "update_rate"
CONF_READ_TIMEOUT = "read_timeout"

# Startup message
NAME = "FoldingAtHomeControl"
ISSUE_URL = "https://github.com/eifinger/hass-foldingathomecontrol/issues"
VERSION = "2.4.2"
STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
