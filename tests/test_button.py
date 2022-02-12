"""Tests for the buttons."""

from unittest.mock import AsyncMock

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.foldingathomecontrol.const import DOMAIN
from tests.const import MOCK_CONFIG, SLOTS_DATA, UNITS_DATA


async def test_buttons(hass, foldingathomecontroller):
    """Test button presses."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)

    await hass.async_block_till_done()

    callback, mock = foldingathomecontroller
    callback("units", UNITS_DATA)
    callback("slots", SLOTS_DATA)
    await hass.async_block_till_done()

    function_mock = AsyncMock()
    mock.return_value.unpause_all_slots_async = function_mock
    await hass.services.async_call(
        "button",
        "press",
        {"entity_id": "button.localhost_unpause"},
        blocking=True,
    )
    await hass.async_block_till_done()
    function_mock.assert_awaited_once()

    function_mock = AsyncMock()
    mock.return_value.pause_all_slots_async = function_mock
    await hass.services.async_call(
        "button",
        "press",
        {"entity_id": "button.localhost_pause"},
        blocking=True,
    )
    await hass.async_block_till_done()
    function_mock.assert_called_once()

    function_mock = AsyncMock()
    mock.return_value.unpause_slot_async = function_mock
    await hass.services.async_call(
        "button",
        "press",
        {"entity_id": "button.localhost_00_unpause"},
        blocking=True,
    )
    await hass.async_block_till_done()
    function_mock.assert_awaited_once()

    function_mock = AsyncMock()
    mock.return_value.pause_slot_async = function_mock
    await hass.services.async_call(
        "button",
        "press",
        {"entity_id": "button.localhost_00_pause"},
        blocking=True,
    )
    await hass.async_block_till_done()
    function_mock.assert_called_once()
