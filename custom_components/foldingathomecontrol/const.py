"""Constants for foldingathomecontrol."""
import logging
from homeassistant.const import UNIT_PERCENTAGE

# Base component constants
DOMAIN = "foldingathomecontrol"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.1.0"
PLATFORMS = ["binary_sensor", "sensor"]
DATA_UPDATED = f"{DOMAIN}_data_updated"
SENSOR_ADDED = f"{DOMAIN}_sensor_added"
SENSOR_REMOVED = f"{DOMAIN}_sensor_removed"

# Logger
_LOGGER = logging.getLogger(__package__)

# Icons
ICON = "mdi:state-machine"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Configuration
CONF_ADDRESS = "address"
CONF_PORT = "port"
CONF_PASSWORD = "password"

# Sensor types

SENSOR_TYPES = [
    {"name": "Status", "unit_of_measurement": None, "icon": ICON},
    {"name": "Reason", "unit_of_measurement": None, "icon": ICON},
    {"name": "Idle", "unit_of_measurement": None, "icon": ICON},
    {"name": "Error", "unit_of_measurement": None, "icon": ICON},
    {"name": "Project", "unit_of_measurement": None, "icon": ICON},
    {"name": "Percentdone", "unit_of_measurement": UNIT_PERCENTAGE, "icon": ICON},
    {"name": "Estimated Time Finished", "unit_of_measurement": None, "icon": ICON},
    {"name": "Points Per Day", "unit_of_measurement": None, "icon": ICON},
    {"name": "Creditestimate", "unit_of_measurement": None, "icon": ICON},
    {"name": "Waiting On", "unit_of_measurement": None, "icon": ICON},
    {"name": "Next Attempt", "unit_of_measurement": None, "icon": ICON},
    {"name": "Total Frames", "unit_of_measurement": None, "icon": ICON},
    {"name": "Frames Done", "unit_of_measurement": None, "icon": ICON},
    {"name": "Assigned", "unit_of_measurement": None, "icon": ICON},
    {"name": "Timeout", "unit_of_measurement": None, "icon": ICON},
    {"name": "Deadline", "unit_of_measurement": None, "icon": ICON},
    {"name": "Work Server", "unit_of_measurement": None, "icon": ICON},
    {"name": "Collection Server", "unit_of_measurement": None, "icon": ICON},
    {"name": "Attempts", "unit_of_measurement": None, "icon": ICON},
    {"name": "Time per Frame", "unit_of_measurement": None, "icon": ICON},
    {"name": "Basecredit", "unit_of_measurement": None, "icon": ICON},
]
