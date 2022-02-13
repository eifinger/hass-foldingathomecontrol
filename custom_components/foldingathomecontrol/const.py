"""Constants for foldingathomecontrol."""
import logging

from homeassistant.const import Platform

# Base component constants
CLIENT = "client"
UNSUB_DISPATCHERS = "unsub_dispatchers"
DOMAIN = "foldingathomecontrol"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "2.3.1"
PLATFORMS = ["sensor"]
DATA_UPDATED = f"{DOMAIN}_data_updated"
SENSOR_ADDED = f"{DOMAIN}_sensor_added"
SENSOR_REMOVED = f"{DOMAIN}_sensor_removed"
DEFAULT_UPDATE_RATE = 5
DEFAULT_READ_TIMEOUT = 15
PLATFORMS = [Platform.SENSOR, Platform.BUTTON, Platform.SELECT]

# Logger
_LOGGER = logging.getLogger(__package__)

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Configuration
CONF_ADDRESS = "address"
CONF_PORT = "port"
CONF_PASSWORD = "password"  # nosec
CONF_UPDATE_RATE = "update_rate"
CONF_READ_TIMEOUT = "read_timeout"
