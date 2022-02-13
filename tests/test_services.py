"""Tests for the services."""

from unittest.mock import AsyncMock

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.foldingathomecontrol.const import DOMAIN
from custom_components.foldingathomecontrol.services import (
    SERVICE_ADDRESS,
    SERVICE_COMMAND,
    SERVICE_PAUSE,
    SERVICE_POWER_LEVEL,
    SERVICE_REQUEST_WORK_SERVER_ASSIGNMENT,
    SERVICE_SEND_COMMAND,
    SERVICE_SET_POWER_LEVEL,
    SERVICE_SHUTDOWN,
    SERVICE_SLOT,
    SERVICE_UNPAUSE,
)
from tests.const import MOCK_CONFIG


async def test_services(hass, foldingathomecontroller):
    """Test service calls."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    _, mock = foldingathomecontroller

    function_mock = AsyncMock()
    mock.return_value.send_command_async = function_mock
    await hass.services.async_call(
        DOMAIN,
        SERVICE_SEND_COMMAND,
        {SERVICE_ADDRESS: "localhost", SERVICE_COMMAND: "slot-info"},
        blocking=True,
    )
    await hass.async_block_till_done()
    function_mock.assert_called_once()

    function_mock = AsyncMock()
    mock.return_value.set_power_level_async = function_mock
    await hass.services.async_call(
        DOMAIN,
        SERVICE_SET_POWER_LEVEL,
        {SERVICE_ADDRESS: "localhost", SERVICE_POWER_LEVEL: "FULL"},
        blocking=True,
    )
    await hass.async_block_till_done()
    function_mock.assert_called_once()

    function_mock = AsyncMock()
    mock.return_value.request_work_server_assignment = function_mock
    await hass.services.async_call(
        DOMAIN,
        SERVICE_REQUEST_WORK_SERVER_ASSIGNMENT,
        {SERVICE_ADDRESS: "localhost"},
        blocking=True,
    )
    await hass.async_block_till_done()
    function_mock.assert_called_once()

    function_mock = AsyncMock()
    mock.return_value.shutdown = function_mock
    await hass.services.async_call(
        DOMAIN,
        SERVICE_SHUTDOWN,
        {SERVICE_ADDRESS: "localhost"},
        blocking=True,
    )
    await hass.async_block_till_done()
    function_mock.assert_called_once()

    function_mock = AsyncMock()
    mock.return_value.unpause_all_slots_async = function_mock
    await hass.services.async_call(
        DOMAIN,
        SERVICE_UNPAUSE,
        {SERVICE_ADDRESS: "localhost"},
        blocking=True,
    )
    await hass.async_block_till_done()
    function_mock.assert_called_once()

    function_mock = AsyncMock()
    mock.return_value.unpause_slot_async = function_mock
    await hass.services.async_call(
        DOMAIN,
        SERVICE_UNPAUSE,
        {SERVICE_ADDRESS: "localhost", SERVICE_SLOT: "01"},
        blocking=True,
    )
    await hass.async_block_till_done()
    function_mock.assert_called_once()

    function_mock = AsyncMock()
    mock.return_value.pause_all_slots_async = function_mock
    await hass.services.async_call(
        DOMAIN,
        SERVICE_PAUSE,
        {SERVICE_ADDRESS: "localhost"},
        blocking=True,
    )
    await hass.async_block_till_done()
    function_mock.assert_called_once()

    function_mock = AsyncMock()
    mock.return_value.pause_slot_async = function_mock
    await hass.services.async_call(
        DOMAIN,
        SERVICE_PAUSE,
        {SERVICE_ADDRESS: "localhost", SERVICE_SLOT: "01"},
        blocking=True,
    )
    await hass.async_block_till_done()
    function_mock.assert_called_once()


async def test_address_not_found(hass, foldingathomecontroller):
    """Test service call for wrong address."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)
    await hass.async_block_till_done()

    _, mock = foldingathomecontroller

    function_mock = AsyncMock()
    mock.return_value.send_command_async = function_mock
    await hass.services.async_call(
        DOMAIN,
        SERVICE_SEND_COMMAND,
        {SERVICE_ADDRESS: "false", SERVICE_COMMAND: "slot-info"},
        blocking=True,
    )
    await hass.async_block_till_done()
    function_mock.assert_not_called()
