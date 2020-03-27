"""Constants for foldingathomecontrol."""
# Base component constants
DOMAIN = "foldingathomecontrol"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.1"
PLATFORMS = ["binary_sensor", "sensor"]
DATA_UPDATED = f"{DOMAIN}_data_updated"

# Icons
ICON = "mdi:state-machine"

# Device classes
BINARY_SENSOR_DEVICE_CLASS = "connectivity"

# Configuration
CONF_ADDRESS = "address"
CONF_PORT = "port"
CONF_PASSWORD = "password"
