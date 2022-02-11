"""Support for foldingathomecontrol button entities."""
from __future__ import annotations

from typing import List

from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.foldingathomecontrol.foldingathomecontrol_client import (
    FoldingAtHomeControlClient,
)
from custom_components.foldingathomecontrol.foldingathomecontrol_device import (
    FoldingAtHomeControlDevice,
)

from .const import CLIENT, DOMAIN, UNSUB_DISPATCHERS
from .services import (
    SERVICE_PAUSE,
    SERVICE_UNPAUSE,
    async_pause_service,
    async_unpause_service,
)

BUTTON_ENTITY_DESCRIPTIONS: tuple[ButtonEntityDescription, ...] = (
    ButtonEntityDescription(
        key=SERVICE_UNPAUSE,
        name="Unpause",
        icon="mdi:play",
        entity_category=EntityCategory.CONFIG,
    ),
    ButtonEntityDescription(
        key=SERVICE_PAUSE,
        name="Pause",
        icon="mdi:pause",
        entity_category=EntityCategory.CONFIG,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the foldingathomecontrol buttons."""

    @callback
    def async_add_buttons(
        new_slots: List[str],
    ) -> None:
        """Add buttons callback."""

        client = hass.data[DOMAIN][entry.entry_id][CLIENT]
        buttons: list = []
        for slot in new_slots:
            for button_description in BUTTON_ENTITY_DESCRIPTIONS:
                buttons.append(
                    FoldingAtHomeControlButton(client, slot, button_description)
                )

        async_add_entities(buttons, True)

    unsub_dispatcher = async_dispatcher_connect(
        hass,
        hass.data[DOMAIN][entry.entry_id][CLIENT].sensor_added_identifer,
        async_add_buttons,
    )
    hass.data[DOMAIN][entry.entry_id][UNSUB_DISPATCHERS].append(unsub_dispatcher)
    if len(hass.data[DOMAIN][entry.entry_id][CLIENT].slot_data) > 0:
        async_add_buttons(hass.data[DOMAIN][entry.entry_id][CLIENT].slot_data.keys())


class FoldingAtHomeControlButton(FoldingAtHomeControlDevice, ButtonEntity):
    """Representation of a foldingathomecontrol button."""

    def __init__(
        self,
        client: FoldingAtHomeControlClient,
        slot_id: str,
        entity_description: ButtonEntityDescription,
    ):
        super().__init__(client, slot_id)
        self.entity_description = entity_description
        self._attr_name = f"{self.entity_description.name} {self._device_identifier}"
        self._attr_unique_id = self._attr_name

    async def async_press(self) -> None:
        """Handle the button press."""
        if self.entity_description.key == SERVICE_PAUSE:
            await async_pause_service(self.hass, self._client.address, self._slot_id)
        if self.entity_description.key == SERVICE_UNPAUSE:
            await async_unpause_service(self.hass, self._client.address, self._slot_id)
