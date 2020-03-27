"""Sensor platform for PyFoldingAtHomeControl."""
from FoldingAtHomeControl import PyOnMessageTypes
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import Entity

from .const import CONF_ADDRESS, DATA_UPDATED, DOMAIN, ICON


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the PyFoldingAtHomeControl sensors."""

    @callback
    def async_add_sensors():
        """add sensors callback."""

        data = hass.data[DOMAIN][config_entry.entry_id].data
        name_prefix = config_entry.data[CONF_ADDRESS]
        dev = []
        for index, slot in enumerate(data[PyOnMessageTypes.SLOTS.value]):
            description = slot["description"]
            dev.append(
                FoldingAtHomeControlSensor(data, name_prefix, description, index)
            )

        async_add_entities(dev, True)

    async_dispatcher_connect(hass, DATA_UPDATED, async_add_sensors)


class FoldingAtHomeControlSensor(Entity):
    """Implementation of a FoldingAtHomeControl sensor."""

    def __init__(self, data, name_prefix: str, description: str, index: int) -> None:
        """Initialize the sensor."""
        self.data = data
        self._sensor_name = description
        self._name_prefix = name_prefix
        self._index = index
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"{self._name_prefix} {self._sensor_name}"

    @property
    def unique_id(self):
        """Set unique_id for sensor."""
        return self.name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return ICON

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return None

    @property
    def available(self):
        """Could the device be accessed during the last update call."""
        return self.data.available

    @property
    def state(self):
        """Return the state of the resources."""
        return self._state

    @property
    def should_poll(self):
        """Return the polling requirement for this sensor."""
        return False

    async def async_added_to_hass(self):
        """Handle entity which will be added."""
        async_dispatcher_connect(
            self.hass, DATA_UPDATED, self._schedule_immediate_update
        )

    @callback
    def _schedule_immediate_update(self):
        self.async_schedule_update_ha_state(True)

    async def async_update(self):
        """Update the sensor."""
        self._state = self.data[PyOnMessageTypes.SLOTS.value][self._index]["state"]
