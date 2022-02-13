"""Client for handling the connection to a FoldingAtHomeControl instance."""

from __future__ import annotations

import asyncio
import datetime
from typing import Any, Dict, List, Optional, Tuple

from FoldingAtHomeControl import FoldingAtHomeController, PyOnMessageTypes
from homeassistant.const import EVENT_HOMEASSISTANT_STOP
from homeassistant.core import Event, HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_send
from homeassistant.util.dt import as_utc

from .const import (
    _LOGGER,
    CONF_ADDRESS,
    CONF_PASSWORD,
    CONF_PORT,
    CONF_READ_TIMEOUT,
    CONF_UPDATE_RATE,
    DATA_UPDATED,
    DEFAULT_READ_TIMEOUT,
    DEFAULT_UPDATE_RATE,
    SENSOR_ADDED,
    SENSOR_REMOVED,
)
from .timeparse import timeparse  # type: ignore


class FoldingAtHomeControlClient:
    """This class handles communication and stores the data."""

    def __init__(self, hass: HomeAssistant, config_entry) -> None:
        """Initialize the class."""
        self.hass = hass
        self.config_entry = config_entry
        self.slot_data: Dict[str, Dict[str, str | None]] = {}
        self.slots: List[str] = []
        self.options_data: Dict[str, str | None] = {}
        self._available = False
        self.add_options()
        self.client = FoldingAtHomeController(
            config_entry.data[CONF_ADDRESS],
            config_entry.data[CONF_PORT],
            config_entry.data.get(CONF_PASSWORD),
            update_rate=config_entry.options[CONF_UPDATE_RATE],
            read_timeout=config_entry.options[CONF_READ_TIMEOUT],
        )
        self._remove_callback = self.client.register_callback(
            self.data_received_callback
        )

        self.client.on_disconnect(self.on_disconnect_callback)
        self._tasks = self._start_background_tasks()

    def _start_background_tasks(self) -> List[asyncio.Task[None]]:
        """Start all background tasks."""

        tasks = []

        @callback
        def cancel_tasks(event: Event) -> None:  # noqa
            for task in self._tasks:
                task.cancel()

        tasks.append(asyncio.ensure_future(self.client.start()))
        tasks.append(asyncio.ensure_future(self._request_slot_info()))
        self.hass.bus.async_listen(EVENT_HOMEASSISTANT_STOP, cancel_tasks)
        return tasks

    async def _request_slot_info(self) -> None:
        """Send a slot-info command."""
        while True:
            if self.client.is_connected:
                await self.client.send_command_async("slot-info")
            await asyncio.sleep(self.client.update_rate)

    def add_options(self) -> None:
        """Add options for FoldingAtHomeControl integration."""
        if not self.config_entry.options:
            options = {
                CONF_UPDATE_RATE: DEFAULT_UPDATE_RATE,
                CONF_READ_TIMEOUT: DEFAULT_READ_TIMEOUT,
            }
            self.hass.config_entries.async_update_entry(
                self.config_entry, options=options
            )
        else:
            options = dict(self.config_entry.options)
            if CONF_UPDATE_RATE not in self.config_entry.options:
                options[CONF_UPDATE_RATE] = DEFAULT_UPDATE_RATE
            if CONF_READ_TIMEOUT not in self.config_entry.options:
                options[CONF_READ_TIMEOUT] = DEFAULT_READ_TIMEOUT
            self.hass.config_entries.async_update_entry(
                self.config_entry, options=options
            )

    async def async_set_update_rate(self, update_rate: int) -> None:
        """Set update_rate."""
        if self.client is not None:
            await self.client.set_subscription_update_rate_async(update_rate)

    def set_read_timeout(self, read_timeout: int) -> None:
        """Set the Read Timeout."""
        if self.client is not None:
            self.client.set_read_timeout(read_timeout)

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
                (
                    "Got disconnected from %s:%s. Trying to reconnect. "
                    "If this happens a lot try increasing the Read Timeout "
                    "in the Integration Options"
                ),
                self.config_entry.data[CONF_ADDRESS],
                self.config_entry.data[CONF_PORT],
            )
            async_dispatcher_send(self.hass, self.data_update_identifer)

    async def async_remove(self) -> None:
        """Remove the callback and stops the client."""
        if self._remove_callback is not None:
            self._remove_callback()
        if self._tasks:
            for task in self._tasks:
                try:
                    task.cancel()
                    await task
                except asyncio.CancelledError:
                    pass

    def handle_error_received(self, error: Any) -> None:
        """Handle received error message."""
        _LOGGER.warning("%s received error: %s", self.address, error)

    def handle_unit_data_received(self, data: Any) -> None:
        """Handle unit data received."""
        _LOGGER.debug("Unit data received %s", data)
        slots_in_data_handled = []
        for unit in data:
            if unit["slot"] not in slots_in_data_handled or unit["state"] == "Running":
                #  For more than one unit for a slot take the one which is running
                slots_in_data_handled.append(unit["slot"])
                self.slot_data.setdefault(unit["id"], {})
                self.slot_data[unit["slot"]]["Error"] = unit.get("error")
                self.slot_data[unit["slot"]]["Project"] = unit.get("project")
                percent_done = unit.get("percentdone")
                if percent_done is not None:
                    percent_done = percent_done.split("%")[0]
                self.slot_data[unit["slot"]]["Percentdone"] = percent_done
                self.slot_data[unit["slot"]]["Estimated Time Finished"] = str(
                    convert_eta_to_timestamp(unit.get("eta"))
                )
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
                tpf = unit.get("tpf")
                if tpf is not None:
                    tpf = timeparse(
                        tpf
                    )  # Convert to seconds e.g. "22 mins 47 secs" to 1367
                self.slot_data[unit["slot"]]["Time per Frame"] = str(tpf)
                self.slot_data[unit["slot"]]["Basecredit"] = unit.get("basecredit")

    def handle_options_data_received(self, data: Any) -> None:
        """Handle options data received."""
        _LOGGER.debug("Options data received %s", data)
        self.options_data["power"] = data.get("power")
        self.options_data["team"] = data.get("team")
        self.options_data["user"] = data.get("user")

    def handle_slots_data_received(self, slots_data: Any) -> None:
        """Handle received slots data."""
        _LOGGER.debug("Slots data received: %s", slots_data)
        self.update_slots_data(slots_data)
        added, removed = self.calculate_slot_changes(slots_data)
        if len(added) > 0:
            _LOGGER.debug("Slots added: %s", added)
            self.slots.extend(added)
            async_dispatcher_send(self.hass, self.sensor_added_identifer, added)
        if len(removed) > 0:
            _LOGGER.debug("Slots removed: %s", removed)
            async_dispatcher_send(self.hass, self.sensor_removed_identifer, removed)
            for slot in removed:
                # Remove old data
                del self.slot_data[slot]
                self.slots.remove(slot)

    def calculate_slot_changes(self, slots: dict) -> Tuple[List[Any], List[str]]:
        """Get added and removed slots."""
        added = [slot["id"] for slot in slots if slot["id"] not in self.slots]
        removed = [
            slot
            for slot in self.slots
            if slot not in list(map(lambda x: x["id"], slots))  # type: ignore
        ]
        return added, removed

    def update_slots_data(self, data: Any) -> None:
        """Store received slots data."""
        for slot in data:
            self.slot_data.setdefault(slot["id"], {})
            self.slot_data[slot["id"]]["Status"] = slot.get("status")
            self.slot_data[slot["id"]]["Description"] = slot.get("description")
            self.slot_data[slot["id"]]["Reason"] = slot.get("reason")
            self.slot_data[slot["id"]]["Idle"] = slot.get("idle")

    @property
    def available(self) -> bool:
        """Is the Folding@Home client available."""
        return bool(self._available)

    @property
    def address(self) -> str:
        """The address the Folding@Home client is connected to."""
        return str(self.config_entry.data[CONF_ADDRESS])

    @property
    def port(self) -> str:
        """The port the Folding@Home client is connected to."""
        return str(self.config_entry.data[CONF_PORT])

    @property
    def data_update_identifer(self) -> str:
        """The unique data_update itentifier for this connection."""
        return f"{DATA_UPDATED}_{self.address}"

    @property
    def sensor_added_identifer(self) -> str:
        """The unique sensor_added itentifier for this connection."""
        return f"{SENSOR_ADDED}_{self.address}"

    @property
    def sensor_removed_identifer(self) -> str:
        """The unique sensor_removed itentifier for this connection."""
        return f"{SENSOR_REMOVED}_{self.address}"


def convert_eta_to_timestamp(eta: Optional[str]) -> Optional[datetime.datetime]:
    """Convert relative eta to a timestamp."""
    if eta is None:
        return None
    seconds_from_now = timeparse(eta)
    if seconds_from_now is None:
        return None
    return as_utc(  # type: ignore
        datetime.datetime.now() + datetime.timedelta(seconds=seconds_from_now)
    )
