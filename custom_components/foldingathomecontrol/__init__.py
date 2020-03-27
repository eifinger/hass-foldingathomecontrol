"""
Component to integrate with PyFoldingAtHomeControl.
"""
import logging
from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from FoldingAtHomeControl import (
    FoldingAtHomeControlConnectionFailed,
    FoldingAtHomeController,
    PyOnMessageTypes,
)
from homeassistant.config_entries import SOURCE_IMPORT
from homeassistant.core import Config, HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_send

from .const import CONF_ADDRESS, CONF_PASSWORD, CONF_PORT, DATA_UPDATED, DOMAIN

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Optional(CONF_ADDRESS, default="localhost"): cv.string,
                vol.Optional(CONF_PORT, default=36330): cv.port,
                vol.Optional(CONF_PASSWORD): cv.string,
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Configure PyFoldingAtHomeControl using config flow only."""
    if DOMAIN in config:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": SOURCE_IMPORT}, data=config[DOMAIN]
            )
        )

    return True


async def async_setup_entry(hass, config_entry):
    """Set up PyFoldingAtHomeControl from config entry."""
    data = FoldingAtHomeControlData(hass, config_entry)
    hass.data.setdefault(DOMAIN, {})[config_entry.entry_id] = data
    if not await data.async_setup():
        return False

    return True


async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
    hass.data[DOMAIN].pop(config_entry.entry_id)
    return True


class FoldingAtHomeControlData:
    """This class handles communication and stores the data."""

    def __init__(self, hass: HomeAssistant, config_entry) -> None:
        """Initialize the class."""
        self.hass = hass
        self.config_entry = config_entry
        self.data = {}
        self.client = None
        self._remove_callback = None
        self._task = None

    @callback
    def callback(self, message_type: str, data: Any) -> None:
        """Called when data is received from the Folding@Home client."""
        if len(self.data[PyOnMessageTypes.SLOTS.value]) != len(self.data[message_type]):
            _LOGGER.debug("Length has changed create/remove sensors.")
        self.data[message_type] = data
        async_dispatcher_send(self.hass, DATA_UPDATED)

    async def async_setup(self) -> bool:
        """Set up the Folding@Home client."""
        address = self.config_entry.data[CONF_ADDRESS]
        port = self.config_entry.data[CONF_PORT]
        password = self.config_entry.data.get(CONF_PASSWORD)
        self.client = FoldingAtHomeController(address, port, password)
        try:
            await self.client.try_connect_async(timeout=5)
        except FoldingAtHomeControlConnectionFailed:
            return False

        self._remove_callback = self.client.register_callback(self.callback)
        self._task = self.hass.async_create_task(self.client.run())
        self.hass.async_create_task(
            self.hass.config_entries.async_forward_entry_setup(
                self.config_entry, "sensor"
            )
        )
        return True

    async def async_remove(self) -> None:
        """Remove the callback and stops the client."""
        if self._remove_callback is not None:
            self._remove_callback()
        if self._task is not None:
            self._task.cancel()

    @property
    def available(self):
        """Is the Client available."""
        if self.client:
            return self.client.is_connected
        return False
