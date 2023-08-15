"""Support for foldingathomecontrol button entities."""
from __future__ import annotations


from homeassistant.components.button import ButtonEntity, ButtonEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.foldingathomecontrol.foldingathomecontrol_device import (
    FoldingAtHomeControlDevice,
    FoldingAtHomeControlSlotDevice,
)

from .const import CLIENT, DOMAIN, UNSUB_DISPATCHERS
from .services import SERVICE_PAUSE, SERVICE_UNPAUSE, async_pause, async_unpause

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

    client = hass.data[DOMAIN][entry.entry_id][CLIENT]
    # Add buttons for address
    buttons: list = []
    for button_description in BUTTON_ENTITY_DESCRIPTIONS:
        buttons.append(FoldingAtHomeControlButton(client, button_description))
    async_add_entities(buttons, True)

    @callback
    def async_add_buttons(
        new_slots: list[str],
    ) -> None:
        """Add slot buttons callback."""

        buttons: list = []
        for slot in new_slots:
            for button_description in BUTTON_ENTITY_DESCRIPTIONS:
                buttons.append(
                    FoldingAtHomeControlSlotButton(client, button_description, slot)
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


class FoldingAtHomeControlSlotButton(FoldingAtHomeControlSlotDevice, ButtonEntity):
    """Representation of a foldingathomecontrol button."""

    async def async_press(self) -> None:
        """Handle the button press."""
        if self.entity_description.key == SERVICE_PAUSE:
            await async_pause(self.hass, self._client.address, self._slot_id)
        if self.entity_description.key == SERVICE_UNPAUSE:
            await async_unpause(self.hass, self._client.address, self._slot_id)


class FoldingAtHomeControlButton(FoldingAtHomeControlDevice, ButtonEntity):
    """Representation of a foldingathomecontrol button."""

    async def async_press(self) -> None:
        """Handle the button press."""
        if self.entity_description.key == SERVICE_PAUSE:
            await async_pause(self.hass, self._client.address, None)
        if self.entity_description.key == SERVICE_UNPAUSE:
            await async_unpause(self.hass, self._client.address, None)
