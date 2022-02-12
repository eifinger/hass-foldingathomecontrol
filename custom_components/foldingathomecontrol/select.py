"""Support for foldingathomecontrol select entities."""
from __future__ import annotations

from homeassistant.components.select import SelectEntity, SelectEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import EntityCategory
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.foldingathomecontrol.foldingathomecontrol_client import (
    FoldingAtHomeControlClient,
)
from custom_components.foldingathomecontrol.foldingathomecontrol_device import (
    FoldingAtHomeControlDevice,
)

from .const import CLIENT, DOMAIN
from .services import SERVICE_SET_POWER_LEVEL, async_set_power_level_service

SELECT_ENTITY_DESCRIPTIONS: tuple[SelectEntityDescription, ...] = (
    SelectEntityDescription(
        key=SERVICE_SET_POWER_LEVEL,
        name="Select Power Level",
        entity_category=EntityCategory.CONFIG,
    ),
)

DEFAULT_SELECT_OPTION = "Full"
SELECT_OPTIONS = ["Light", "Medium", "Full"]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the foldingathomecontrol selects."""

    client = hass.data[DOMAIN][entry.entry_id][CLIENT]
    selects: list = []
    for select_description in SELECT_ENTITY_DESCRIPTIONS:
        selects.append(FoldingAtHomeControlSelect(client, select_description))

    async_add_entities(selects, True)


class FoldingAtHomeControlSelect(FoldingAtHomeControlDevice, SelectEntity):
    """Representation of a foldingathomecontrol select."""

    def __init__(
        self,
        client: FoldingAtHomeControlClient,
        entity_description: SelectEntityDescription,
    ):
        super().__init__(client, entity_description)
        self._attr_options = SELECT_OPTIONS

    @property
    def current_option(self) -> str:
        """Return the selected entity option to represent the entity state."""
        if "power" in self._client.options_data:
            return str(self._client.options_data["power"])
        return DEFAULT_SELECT_OPTION

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        await async_set_power_level_service(self.hass, self._client.address, option)
