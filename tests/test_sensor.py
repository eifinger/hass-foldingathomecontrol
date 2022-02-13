"""Tests for the foldingathomecontrol sensor platform."""

from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.foldingathomecontrol.const import DOMAIN
from tests.const import (
    MOCK_CONFIG,
    OPTIONS_DATA,
    SLOTS_DATA,
    TWO_SLOTS_DATA,
    TWO_UNITS_DATA,
    UNITS_DATA,
)


async def test_sensor(hass, foldingathomecontroller):
    """Test that sensor works."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)

    await hass.async_block_till_done()

    callback, _, _ = foldingathomecontroller
    callback("units", UNITS_DATA)
    callback("slots", SLOTS_DATA)
    await hass.async_block_till_done()
    assert hass.states.get("sensor.localhost_00_status").state == "READY"
    assert (
        hass.states.get("sensor.localhost_00_status").attributes["icon"]
        == "mdi:state-machine"
    )
    assert hass.states.get("sensor.localhost_00_reason").state == ""
    assert (
        hass.states.get("sensor.localhost_00_reason").attributes["icon"]
        == "mdi:state-machine"
    )
    assert hass.states.get("sensor.localhost_00_idle").state == "False"
    assert (
        hass.states.get("sensor.localhost_00_idle").attributes["icon"]
        == "mdi:state-machine"
    )
    assert hass.states.get("sensor.localhost_00_error").state == "NO_ERROR"
    assert (
        hass.states.get("sensor.localhost_00_error").attributes["icon"] == "mdi:alert"
    )
    assert hass.states.get("sensor.localhost_00_project").state == "11777"
    assert (
        hass.states.get("sensor.localhost_00_project").attributes["icon"]
        == "mdi:state-machine"
    )
    assert hass.states.get("sensor.localhost_00_percentdone").state == "72.51"
    assert (
        hass.states.get("sensor.localhost_00_percentdone").attributes["icon"]
        == "mdi:percent"
    )
    assert (
        hass.states.get("sensor.localhost_00_estimated_time_finished").attributes[
            "icon"
        ]
        == "mdi:calendar-clock"
    )
    assert hass.states.get("sensor.localhost_00_points_per_day").state == "359072"
    assert (
        hass.states.get("sensor.localhost_00_points_per_day").attributes["icon"]
        == "mdi:state-machine"
    )
    assert hass.states.get("sensor.localhost_00_creditestimate").state == "58183"
    assert (
        hass.states.get("sensor.localhost_00_creditestimate").attributes["icon"]
        == "mdi:state-machine"
    )
    assert hass.states.get("sensor.localhost_00_waiting_on").state == ""
    assert (
        hass.states.get("sensor.localhost_00_waiting_on").attributes["icon"]
        == "mdi:state-machine"
    )
    assert hass.states.get("sensor.localhost_00_next_attempt").state == "0.00 secs"
    assert (
        hass.states.get("sensor.localhost_00_next_attempt").attributes["icon"]
        == "mdi:history"
    )
    assert hass.states.get("sensor.localhost_00_total_frames").state == "100"
    assert (
        hass.states.get("sensor.localhost_00_total_frames").attributes["icon"]
        == "mdi:state-machine"
    )
    assert hass.states.get("sensor.localhost_00_frames_done").state == "72"
    assert (
        hass.states.get("sensor.localhost_00_frames_done").attributes["icon"]
        == "mdi:state-machine"
    )
    assert (
        hass.states.get("sensor.localhost_00_assigned").state
        == "2020-03-28T08: 33: 55Z"
    )
    assert (
        hass.states.get("sensor.localhost_00_assigned").attributes["icon"]
        == "mdi:calendar-clock"
    )
    assert (
        hass.states.get("sensor.localhost_00_timeout").state == "2020-03-29T08: 33: 55Z"
    )
    assert (
        hass.states.get("sensor.localhost_00_timeout").attributes["icon"]
        == "mdi:calendar-clock"
    )
    assert (
        hass.states.get("sensor.localhost_00_deadline").state
        == "2020-04-05T13: 21: 54Z"
    )
    assert (
        hass.states.get("sensor.localhost_00_deadline").attributes["icon"]
        == "mdi:calendar-clock"
    )
    assert hass.states.get("sensor.localhost_00_work_server").state == "40.114.52.201"
    assert (
        hass.states.get("sensor.localhost_00_work_server").attributes["icon"]
        == "mdi:server-network"
    )
    assert (
        hass.states.get("sensor.localhost_00_collection_server").state == "13.82.98.119"
    )
    assert (
        hass.states.get("sensor.localhost_00_collection_server").attributes["icon"]
        == "mdi:server-network"
    )
    assert hass.states.get("sensor.localhost_00_attempts").state == "0"
    assert (
        hass.states.get("sensor.localhost_00_attempts").attributes["icon"]
        == "mdi:cached"
    )
    assert hass.states.get("sensor.localhost_00_time_per_frame").state == "140"
    assert (
        hass.states.get("sensor.localhost_00_time_per_frame").attributes["icon"]
        == "mdi:speedometer"
    )
    assert hass.states.get("sensor.localhost_00_basecredit").state == "9405"
    assert (
        hass.states.get("sensor.localhost_00_basecredit").attributes["icon"]
        == "mdi:state-machine"
    )


async def test_sensor_slots_before_units(hass, foldingathomecontroller):
    """Test that sensor works when slot info is received before unit info."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)

    await hass.async_block_till_done()

    callback, _, _ = foldingathomecontroller
    callback("units", UNITS_DATA)
    callback("slots", SLOTS_DATA)
    await hass.async_block_till_done()
    assert hass.states.get("sensor.localhost_00_status").state == "READY"
    assert (
        hass.states.get("sensor.localhost_00_status").attributes["icon"]
        == "mdi:state-machine"
    )


async def test_sensor_attributes(hass, foldingathomecontroller):
    """Test that sensor attributes show the options."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)

    await hass.async_block_till_done()

    callback, _, _ = foldingathomecontroller
    callback("slots", SLOTS_DATA)
    callback("units", UNITS_DATA)
    callback("options", OPTIONS_DATA)
    await hass.async_block_till_done()
    assert hass.states.get("sensor.localhost_00_status").attributes["power"] == "Light"
    assert hass.states.get("sensor.localhost_00_status").attributes["team"] == "247478"
    assert (
        hass.states.get("sensor.localhost_00_status").attributes["user"] == "Anonymous"
    )
    assert (
        hass.states.get("sensor.localhost_00_status").attributes["description"]
        == "cpu: 3"
    )


async def test_sensor_removed(hass, foldingathomecontroller):
    """Test that sensors get removed."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    callback, _, _ = foldingathomecontroller
    callback("slots", TWO_SLOTS_DATA)
    callback("units", TWO_UNITS_DATA)
    await hass.async_block_till_done()
    assert len(hass.states.async_all()) == 49

    callback("slots", SLOTS_DATA)
    callback("units", UNITS_DATA)
    await hass.async_block_till_done()
    assert len(hass.states.async_all()) == 49


async def test_disconnect(hass, foldingathomecontroller):
    """Test that disconnect is handled."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    callback, disconnect, _ = foldingathomecontroller
    callback("slots", TWO_SLOTS_DATA)
    callback("units", TWO_UNITS_DATA)
    await hass.async_block_till_done()

    disconnect()
    await hass.async_block_till_done()
    assert hass.states.get("sensor.localhost_00_status").state == "unavailable"
