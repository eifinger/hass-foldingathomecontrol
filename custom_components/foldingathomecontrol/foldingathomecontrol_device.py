"""Base class for FoldingAtHomeControl devices."""
from collections.abc import Callable

from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity import DeviceInfo, Entity, EntityDescription

from .const import DOMAIN
from .foldingathomecontrol_client import FoldingAtHomeControlClient


class FoldingAtHomeControlDevice(Entity):
    """Common base for FoldingAtHomeControl entities for an address."""

    def __init__(
        self, client: FoldingAtHomeControlClient, entity_description: EntityDescription
    ) -> None:
        self._client: FoldingAtHomeControlClient = client
        self.listeners: list[Callable[[], None]] = []
        self.entity_description = entity_description
        self._attr_name = f"{client.address} {self.entity_description.name}"
        self._attr_unique_id = self._attr_name
        self._attr_should_poll = False
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, client.address)},
            name=client.address,
            manufacturer="FoldingAtHomeControl",
        )

    @property
    def available(self) -> bool:
        """Return True if device is available."""
        return self._client.available

    async def async_added_to_hass(self) -> None:
        """Subscribe to device events."""
        self.listeners.append(
            async_dispatcher_connect(
                self.hass,
                self._client.data_update_identifer,
                self.async_write_ha_state,
            )
        )

    async def async_will_remove_from_hass(self) -> None:
        """Disconnect device object when removed."""
        for unsub_dispatcher in self.listeners:
            unsub_dispatcher()


class FoldingAtHomeControlSlotDevice(FoldingAtHomeControlDevice):
    """FoldingAtHomeControl entities for a specific slot."""

    def __init__(
        self,
        client: FoldingAtHomeControlClient,
        entity_description: EntityDescription,
        slot_id: str,
    ) -> None:
        """Set up device and add update callback to get data."""
        super().__init__(client, entity_description)
        self._attr_name = f"{client.address}_{slot_id} {self.entity_description.name}"
        self._attr_unique_id = self._attr_name
        self._slot_id: str = slot_id
        description = client.slot_data[slot_id]["Description"]
        device_description = description.split(":")[0].upper()  # type: ignore
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{client.address}_{slot_id}")},
            name=f"{client.address} {device_description}: {slot_id}",
            manufacturer="FoldingAtHomeControl",
            via_device=(DOMAIN, self._client.address),
        )

    async def async_added_to_hass(self) -> None:
        """Subscribe to device events."""
        self.listeners.append(
            async_dispatcher_connect(
                self.hass,
                self._client.data_update_identifer,
                self.async_write_ha_state,
            )
        )
        self.listeners.append(
            async_dispatcher_connect(
                self.hass, self._client.sensor_removed_identifer, self.async_remove_self
            )
        )

    async def async_remove_self(self, removed_slots: list) -> None:
        """Schedule removal of this entity.

        Called by sensor_removed_identifer scheduled by async_added_to_hass.
        """
        if self._slot_id not in removed_slots:
            return
        await self.async_remove()
