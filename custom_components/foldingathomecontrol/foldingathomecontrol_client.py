"""Client for handling the conncection to a FoldingAtHomeControl instance."""

import asyncio
import itertools
import datetime
from typing import Any, Tuple

from homeassistant.core import HomeAssistant, callback

from homeassistant.util.dt import as_utc

from homeassistant.helpers.dispatcher import async_dispatcher_send

from FoldingAtHomeControl import (
    FoldingAtHomeControlConnectionFailed,
    FoldingAtHomeController,
    PyOnMessageTypes,
)

from .timeparse import timeparse

from .const import (
    CONF_ADDRESS,
    CONF_PASSWORD,
    CONF_PORT,
    DATA_UPDATED,
    DOMAIN,
    SENSOR_ADDED,
    SENSOR_REMOVED,
    _LOGGER,
)


class FoldingAtHomeControlClient:
    """This class handles communication and stores the data."""

    def __init__(self, hass: HomeAssistant, config_entry) -> None:
        """Initialize the class."""
        self.hass = hass
        self.config_entry = config_entry
        self._address = self.config_entry.data[CONF_ADDRESS]
        self._port = self.config_entry.data[CONF_PORT]
        self.slot_data = {}
        self.options_data = {}
        self.client = None
        self._remove_callback = None
        self._task = None
        self._available = False

    @callback
    def data_received_callback(self, message_type: str, data: Any) -> None:
        """Called when data is received from the Folding@Home client."""
        self._available = True
        if message_type == PyOnMessageTypes.SLOTS.value:
            self.handle_slots_data_received(data)
        if message_type == PyOnMessageTypes.UNITS.value:
            self.handle_unit_data_received(data)
        if message_type == PyOnMessageTypes.OPTIONS.value:
            self.handle_options_data_received(data)
        if message_type == PyOnMessageTypes.ERROR.value:
            self.handle_error_received(data)
        async_dispatcher_send(self.hass, self.data_update_identifer)

    @callback
    def on_disconnect_callback(self) -> None:
        """Called when data is received from the Folding@Home client."""
        if self._available:
            self._available = False
            _LOGGER.error(
                "Disconnected from %s:%s. Trying to reconnect.",
                self.config_entry.data[CONF_ADDRESS],
                self.config_entry.data[CONF_PORT],
            )
            async_dispatcher_send(self.hass, self.data_update_identifer)

    async def async_setup(self) -> bool:
        """Set up the Folding@Home client."""
        address = self.config_entry.data[CONF_ADDRESS]
        port = self.config_entry.data[CONF_PORT]
        password = self.config_entry.data.get(CONF_PASSWORD)
        self.client = FoldingAtHomeController(address, port, password)
        self._remove_callback = self.client.register_callback(
            self.data_received_callback
        )

        self.hass.async_create_task(
            self.hass.config_entries.async_forward_entry_setup(
                self.config_entry, "sensor"
            )
        )

        self.client.on_disconnect(self.on_disconnect_callback)
        self._task = asyncio.ensure_future(self.client.start())

        return True

    async def async_remove(self) -> None:
        """Remove the callback and stops the client."""
        if self._remove_callback is not None:
            self._remove_callback()
        if self._task is not None:
            try:
                self._task.cancel()
                await self._task
            except asyncio.CancelledError:
                pass

    async def async_update_device_registry(self) -> None:
        """Update device registry."""
        device_registry = await self.hass.helpers.device_registry.async_get_registry()
        device_registry.async_get_or_create(
            config_entry_id=self.config_entry.entry_id,
            manufacturer="FoldingAtHomeControl",
            identifiers={(DOMAIN, self.address)},
        )

    def handle_error_received(self, error: Any) -> None:
        """Handle received error message."""
        _LOGGER.warning("%s received error: %s", self.address, error)

    def handle_unit_data_received(self, data: Any) -> None:
        """Handle unit data received."""
        slots_in_data_handled = []
        for unit in data:
            if unit["slot"] not in slots_in_data_handled or unit["state"] == "Running":
                #  If there is more than one unit for a slot take the one which is running
                slots_in_data_handled.append(unit["slot"])
                self.slot_data[unit["slot"]]["Error"] = unit.get("error")
                self.slot_data[unit["slot"]]["Project"] = unit.get("project")
                self.slot_data[unit["slot"]]["Percentdone"] = unit.get("percentdone")
                self.slot_data[unit["slot"]][
                    "Estimated Time Finished"
                ] = convert_eta_to_timestamp(unit.get("eta"))
                self.slot_data[unit["slot"]]["Points Per Day"] = unit.get("ppd")
                self.slot_data[unit["slot"]]["Creditestimate"] = unit.get(
                    "creditestimate"
                )
                self.slot_data[unit["slot"]]["Waiting On"] = unit.get("waitingon")
                self.slot_data[unit["slot"]]["Next Attempt"] = unit.get("nextattempt")
                self.slot_data[unit["slot"]]["Total Frames"] = unit.get("totalframes")
                self.slot_data[unit["slot"]]["Frames Done"] = unit.get("framesdone")
                self.slot_data[unit["slot"]]["Assigned"] = unit.get("assigned")
                self.slot_data[unit["slot"]]["Timeout"] = unit.get("timeout")
                self.slot_data[unit["slot"]]["Deadline"] = unit.get("deadline")
                self.slot_data[unit["slot"]]["Work Server"] = unit.get("ws")
                self.slot_data[unit["slot"]]["Collection Server"] = unit.get("cs")
                self.slot_data[unit["slot"]]["Attempts"] = unit.get("attempts")
                self.slot_data[unit["slot"]]["Time per Frame"] = unit.get("tpf")
                self.slot_data[unit["slot"]]["Basecredit"] = unit.get("basecredit")

    def handle_options_data_received(self, data: Any) -> None:
        """Handle options data received."""
        self.options_data["power"] = data.get("power")
        self.options_data["team"] = data.get("team")
        self.options_data["user"] = data.get("user")

    def handle_slots_data_received(self, data: Any) -> None:
        """Handle received slots data."""
        self.update_slots_data(data)
        if len(self.slot_data) > 0:
            added, removed = self.calculate_slot_changes(data)
            async_dispatcher_send(self.hass, self.sensor_added_identifer, added)
            async_dispatcher_send(self.hass, self.sensor_removed_identifer, removed)
        else:
            async_dispatcher_send(
                self.hass, self.sensor_added_identifer, [slot["id"] for slot in data]
            )

    def calculate_slot_changes(self, slots: dict) -> Tuple[dict, dict]:
        """Get added and removed slots."""
        added = list(
            itertools.filterfalse(
                lambda slot: (slot["id"] != entry for entry in self.slot_data), slots,
            )
        )
        removed = list(
            itertools.filterfalse(
                lambda entry: (entry != slot["id"] for slot in slots), self.slot_data,
            )
        )
        return added, removed

    def update_slots_data(self, data: Any) -> None:
        """Store received slots data."""
        for slot in data:
            self.slot_data[slot["id"]]["Status"] = slot.get("status")
            self.slot_data[slot["id"]]["Description"] = slot.get("description")
            self.slot_data[slot["id"]]["Reason"] = slot.get("reason")
            self.slot_data[slot["id"]]["Idle"] = slot.get("idle")

    @property
    def available(self):
        """Is the Folding@Home client available."""
        return self._available

    @property
    def address(self):
        """The address the Folding@Home client is connected to."""
        return self._address

    @property
    def port(self):
        """The port the Folding@Home client is connected to."""
        return self._port

    @property
    def data_update_identifer(self) -> None:
        """The unique data_update itentifier for this connection."""
        return f"{DATA_UPDATED}_{self.address}"

    @property
    def sensor_added_identifer(self) -> None:
        """The unique sensor_added itentifier for this connection."""
        return f"{SENSOR_ADDED}_{self.address}"

    @property
    def sensor_removed_identifer(self) -> None:
        """The unique sensor_removed itentifier for this connection."""
        return f"{SENSOR_REMOVED}_{self.address}"


def convert_eta_to_timestamp(eta: Optional[str]) -> Optional[str]:
    """Convert relative eta to a timestamp."""
    if eta is None:
        return
    seconds_from_now = timeparse(eta)
    return as_utc(
        datetime.datetime.now() + datetime.timedelta(seconds=seconds_from_now)
    )
