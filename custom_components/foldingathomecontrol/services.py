"""FoldingAtHomeControl services."""
import voluptuous as vol
from FoldingAtHomeControl import PowerLevel
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv

from .const import _LOGGER, CLIENT, CONF_ADDRESS, DOMAIN

DOMAIN_SERVICES = f"{DOMAIN}_services"

SERVICE_ADDRESS = "address"
SERVICE_SLOT = "slot"
SERVICE_POWER_LEVEL = "power_level"

SERVICE_REQUEST_WORK_SERVER_ASSIGNMENT = "request_work_server_assignment"
SERVICE_REQUEST_WORK_SERVER_ASSIGNMENT_SCHEMA = vol.Schema(
    {vol.Required(SERVICE_ADDRESS): cv.string}
)

SERVICE_PAUSE = "pause"
SERVICE_UNPAUSE = "unpause"
SERVICE_SLOT_SCHEMA = vol.Schema(
    {
        vol.Required(SERVICE_ADDRESS): cv.string,
        vol.Optional(SERVICE_SLOT, default=None): vol.Any(cv.string, None),
    }
)

SERVICE_SHUTDOWN = "shutdown"
SERVICE_REQUEST_WORK_SERVER_ASSIGNMENT = "request_work_server_assignment"
SERVICE_SCHEMA = vol.Schema({vol.Required(SERVICE_ADDRESS): cv.string})

SERVICE_SET_POWER_LEVEL = "set_power_level"
SERVICE_SET_POWER_LEVEL_SCHEMA = vol.Schema(
    {
        vol.Required(SERVICE_ADDRESS): cv.string,
        vol.Required(SERVICE_POWER_LEVEL): cv.enum(PowerLevel),
    }
)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Set up services for FoldingAtHomeControl integration."""
    if hass.data.get(DOMAIN_SERVICES, False):
        return None

    hass.data[DOMAIN_SERVICES] = True

    async def async_call_folding_at_home_control_service(service_call) -> None:
        """Call correct FoldingAtHomeControl service."""
        service = service_call.service
        service_data = service_call.data

        if service == SERVICE_SET_POWER_LEVEL:
            await async_set_power_level_service(
                hass, service_data[SERVICE_ADDRESS], service_data[SERVICE_POWER_LEVEL]
            )
        if service == SERVICE_REQUEST_WORK_SERVER_ASSIGNMENT:
            await async_request_assignment_service(hass, service_data[SERVICE_ADDRESS])
        if service == SERVICE_PAUSE:
            await async_pause_service(
                hass, service_data[SERVICE_ADDRESS], service_data.get(SERVICE_SLOT)
            )
        if service == SERVICE_UNPAUSE:
            await async_unpause_service(
                hass, service_data[SERVICE_ADDRESS], service_data.get(SERVICE_SLOT)
            )
        if service == SERVICE_SHUTDOWN:
            await async_shutdown_service(hass, service_data[SERVICE_ADDRESS])

    hass.services.async_register(
        DOMAIN,
        SERVICE_SET_POWER_LEVEL,
        async_call_folding_at_home_control_service,
        schema=SERVICE_SET_POWER_LEVEL_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_PAUSE,
        async_call_folding_at_home_control_service,
        schema=SERVICE_SLOT_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_UNPAUSE,
        async_call_folding_at_home_control_service,
        schema=SERVICE_SLOT_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_REQUEST_WORK_SERVER_ASSIGNMENT,
        async_call_folding_at_home_control_service,
        schema=SERVICE_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN,
        SERVICE_SHUTDOWN,
        async_call_folding_at_home_control_service,
        schema=SERVICE_SCHEMA,
    )
    return None


async def async_unload_services(hass: HomeAssistant) -> None:
    """Unload deCONZ services."""
    if not hass.data.get(DOMAIN_SERVICES):
        return None

    hass.data[DOMAIN_SERVICES] = False

    hass.services.async_remove(DOMAIN, SERVICE_PAUSE)
    hass.services.async_remove(DOMAIN, SERVICE_UNPAUSE)
    hass.services.async_remove(DOMAIN, SERVICE_SHUTDOWN)
    hass.services.async_remove(DOMAIN, SERVICE_REQUEST_WORK_SERVER_ASSIGNMENT)
    hass.services.async_remove(DOMAIN, SERVICE_SET_POWER_LEVEL)
    return None


async def async_pause_service(hass: HomeAssistant, address: str, slot: str) -> None:
    """Let the client pause one or all slots."""

    for config_entry in hass.data[DOMAIN]:
        if (
            hass.data[DOMAIN][config_entry][CLIENT].config_entry.data[CONF_ADDRESS]
            == address
        ):
            if slot is not None:
                await hass.data[DOMAIN][config_entry][CLIENT].client.pause_slot_async(
                    slot
                )
                return
            await hass.data[DOMAIN][config_entry][CLIENT].client.pause_all_slots_async()
            return None
    _LOGGER.warning("Could not find a registered integration with address: %s", address)
    return None


async def async_unpause_service(hass: HomeAssistant, address: str, slot: str) -> None:
    """Let the client unpause one or all slots."""

    for config_entry in hass.data[DOMAIN]:
        if (
            hass.data[DOMAIN][config_entry][CLIENT].config_entry.data[CONF_ADDRESS]
            == address
        ):
            if slot is not None:
                await hass.data[DOMAIN][config_entry][CLIENT].client.unpause_slot_async(
                    slot
                )
                return
            await hass.data[DOMAIN][config_entry][
                CLIENT
            ].client.unpause_all_slots_async()
            return None
    _LOGGER.warning("Could not find a registered integration with address: %s", address)
    return None


async def async_shutdown_service(hass: HomeAssistant, address: str) -> None:
    """Let the client shutdown."""

    for config_entry in hass.data[DOMAIN]:
        if (
            hass.data[DOMAIN][config_entry][CLIENT].config_entry.data[CONF_ADDRESS]
            == address
        ):
            await hass.data[DOMAIN][config_entry][CLIENT].client.shutdown()
            return None
    _LOGGER.warning("Could not find a registered integration with address: %s", address)
    return None


async def async_request_assignment_service(hass: HomeAssistant, address: str) -> None:
    """Let the client request a new work server assignment."""

    for config_entry in hass.data[DOMAIN]:
        if (
            hass.data[DOMAIN][config_entry][CLIENT].config_entry.data[CONF_ADDRESS]
            == address
        ):
            await hass.data[DOMAIN][config_entry][
                CLIENT
            ].client.request_work_server_assignment()
            return None
    _LOGGER.warning("Could not find a registered integration with address: %s", address)
    return None


async def async_set_power_level_service(
    hass: HomeAssistant, address: str, power_level: str
) -> None:
    """Let the client set the power level."""

    for config_entry in hass.data[DOMAIN]:
        if (
            hass.data[DOMAIN][config_entry][CLIENT].config_entry.data[CONF_ADDRESS]
            == address
        ):
            await hass.data[DOMAIN][config_entry][CLIENT].client.set_power_level_async(
                PowerLevel(power_level)
            )
            return None
    _LOGGER.warning("Could not find a registered integration with address: %s", address)
    return None
