"""
Component to integrate with PyFoldingAtHomeControl.
"""

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.core import Config, HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import (
    CLIENT,
    CONF_ADDRESS,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_READ_TIMEOUT,
    CONF_UPDATE_RATE,
    DOMAIN,
    UNSUB_DISPATCHERS,
)
from .foldingathomecontrol_client import FoldingAtHomeControlClient
from .services import async_setup_services, async_unload_services

FOLDINGATHOMECONTROL_SCHEMA = vol.Schema(
    {
        vol.Optional(CONF_ADDRESS, default="localhost"): cv.string,
        vol.Optional(CONF_PORT, default=36330): cv.port,
        vol.Optional(CONF_PASSWORD): cv.string,
    }
)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.All(cv.ensure_list, [FOLDINGATHOMECONTROL_SCHEMA])},
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass: HomeAssistant, config: Config) -> bool:
    """Configure PyFoldingAtHomeControl using config flow only."""
    if DOMAIN in config:
        for entry in config[DOMAIN]:
            hass.async_create_task(
                hass.config_entries.flow.async_init(
                    DOMAIN, context={"source": SOURCE_IMPORT}, data=entry
                )
            )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up PyFoldingAtHomeControl from config entry."""
    try:
        client = FoldingAtHomeControlClient(hass, entry)
        hass.data.setdefault(DOMAIN, {})[entry.entry_id] = {}
        hass.data.setdefault(DOMAIN, {})[entry.entry_id][CLIENT] = client
        hass.data.setdefault(DOMAIN, {})[entry.entry_id][UNSUB_DISPATCHERS] = []

        await async_setup_services(hass)
        entry.add_update_listener(async_options_updated)

        return True
    except Exception as err:
        ex = ConfigEntryNotReady()
        ex.__cause__ = err
        raise ex from err


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, "sensor")
    await hass.data[DOMAIN][entry.entry_id][CLIENT].async_remove()
    for unsub_dispatcher in hass.data[DOMAIN][entry.entry_id][UNSUB_DISPATCHERS]:
        unsub_dispatcher()
    hass.data[DOMAIN].pop(entry.entry_id)
    # If there is no instance of this integration registered anymore
    if not hass.data[DOMAIN]:
        await async_unload_services(hass)
    return True


async def async_options_updated(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Triggered by config entry options updates."""
    await hass.data[DOMAIN][entry.entry_id][CLIENT].async_set_update_rate(
        entry.options[CONF_UPDATE_RATE]
    )
    hass.data[DOMAIN][entry.entry_id][CLIENT].set_read_timeout(
        entry.options[CONF_READ_TIMEOUT]
    )


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
