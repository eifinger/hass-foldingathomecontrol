"""Sensor platform for PyFoldingAtHomeControl."""
from typing import List

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.const import PERCENTAGE, TIME_SECONDS
from homeassistant.core import callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect

from .const import CLIENT, DOMAIN, UNSUB_DISPATCHERS
from .foldingathomecontrol_device import FoldingAtHomeControlSlotDevice

ICON = "mdi:state-machine"

SENSOR_ENTITY_DESCRIPTIONS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="Status",
        name="Status",
        icon=ICON,
    ),
    SensorEntityDescription(
        key="Reason",
        name="Reason",
        icon=ICON,
    ),
    SensorEntityDescription(
        key="Idle",
        name="Idle",
        icon=ICON,
    ),
    SensorEntityDescription(
        key="Error",
        name="Error",
        icon="mdi:alert",
    ),
    SensorEntityDescription(
        key="Project",
        name="Project",
        icon=ICON,
    ),
    SensorEntityDescription(
        key="Percentdone",
        name="Percentdone",
        native_unit_of_measurement=PERCENTAGE,
        icon="mdi:percent",
    ),
    SensorEntityDescription(
        key="Estimated Time Finished",
        name="Estimated Time Finished",
        icon="mdi:calendar-clock",
    ),
    SensorEntityDescription(
        key="Points Per Day",
        name="Points Per Day",
        native_unit_of_measurement="points",
        icon=ICON,
    ),
    SensorEntityDescription(
        key="Creditestimate",
        name="Creditestimate",
        native_unit_of_measurement="credits",
        icon=ICON,
    ),
    SensorEntityDescription(
        key="Waiting On",
        name="Waiting On",
        icon=ICON,
    ),
    SensorEntityDescription(
        key="Next Attempt",
        name="Next Attempt",
        icon="mdi:history",
    ),
    SensorEntityDescription(
        key="Total Frames",
        name="Total Frames",
        native_unit_of_measurement="frames",
        icon=ICON,
    ),
    SensorEntityDescription(
        key="Frames Done",
        name="Frames Done",
        native_unit_of_measurement="frames",
        icon=ICON,
    ),
    SensorEntityDescription(
        key="Assigned",
        name="Assigned",
        icon="mdi:calendar-clock",
    ),
    SensorEntityDescription(
        key="Timeout",
        name="Timeout",
        icon="mdi:calendar-clock",
    ),
    SensorEntityDescription(
        key="Deadline",
        name="Deadline",
        icon="mdi:calendar-clock",
    ),
    SensorEntityDescription(
        key="Work Server",
        name="Work Server",
        icon="mdi:server-network",
    ),
    SensorEntityDescription(
        key="Collection Server",
        name="Collection Server",
        icon="mdi:server-network",
    ),
    SensorEntityDescription(
        key="Attempts",
        name="Attempts",
        native_unit_of_measurement="attempts",
        icon="mdi:cached",
    ),
    SensorEntityDescription(
        key="Time per Frame",
        name="Time per Frame",
        native_unit_of_measurement=TIME_SECONDS,
        icon="mdi:speedometer",
    ),
    SensorEntityDescription(
        key="Basecredit",
        name="Basecredit",
        native_unit_of_measurement="credits",
        icon=ICON,
    ),
)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the PyFoldingAtHomeControl sensors."""

    @callback
    def async_add_sensors(new_slots: List[str]) -> None:
        """add sensors callback."""

        client = hass.data[DOMAIN][config_entry.entry_id][CLIENT]
        dev: list = []
        for slot in new_slots:
            for entity_description in SENSOR_ENTITY_DESCRIPTIONS:
                dev.append(
                    FoldingAtHomeControlSensor(
                        client,
                        entity_description,
                        slot,
                    )
                )

        async_add_entities(dev, True)

    unsub_dispatcher = async_dispatcher_connect(
        hass,
        hass.data[DOMAIN][config_entry.entry_id][CLIENT].sensor_added_identifer,
        async_add_sensors,
    )
    hass.data[DOMAIN][config_entry.entry_id][UNSUB_DISPATCHERS].append(unsub_dispatcher)
    if len(hass.data[DOMAIN][config_entry.entry_id][CLIENT].slot_data) > 0:
        async_add_sensors(
            hass.data[DOMAIN][config_entry.entry_id][CLIENT].slot_data.keys()
        )


class FoldingAtHomeControlSensor(FoldingAtHomeControlSlotDevice, SensorEntity):
    """Implementation of a FoldingAtHomeControl sensor."""

    @property
    def native_value(self):
        """Return the state of the resources if it has been received yet."""
        if self._slot_id in self._client.slot_data:
            if self.entity_description.key in self._client.slot_data[self._slot_id]:
                return self._client.slot_data[self._slot_id][
                    self.entity_description.key
                ]

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        if self._slot_id in self._client.slot_data:
            attr = self._client.options_data.copy()
            attr["description"] = self._client.slot_data[self._slot_id]["Description"]
            return attr
