"""Tests for the foldingathomecontrol sensor platform."""
from asyncio.streams import StreamReader
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from homeassistant.const import EVENT_HOMEASSISTANT_START
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.foldingathomecontrol.const import (
    CONF_ADDRESS,
    CONF_PASSWORD,
    CONF_PORT,
    DOMAIN,
)


@pytest.fixture
def stream_reader_writer():
    """Create a StreamReader and fill it with connection messages."""
    reader = StreamReader()
    reader.feed_data(
        b"\x1b[H\x1b[2JWelcome to the Folding@home Client command server.\n"
    )
    reader.feed_data(b"OK\n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"PyON 1 units\n")
    reader.feed_data(
        b"""[{
        "id": "00",
        "state": "RUNNING",
        "error": "NO_ERROR",
        "project": 11777,
        "run": 0,
        "clone": 17250,
        "gen": 0,
        "core": "0x22",
        "unit": "0x00000003287234c95e774a8488c5d4ea",
        "percentdone": "72.51%",
        "eta": "1 hours 04 mins",
        "ppd": "359072",
        "creditestimate": "58183",
        "waitingon": "",
        "nextattempt": "0.00 secs",
        "timeremaining": "8.08 days",
        "totalframes": 100,
        "framesdone": 72,
        "assigned": "2020-03-28T08: 33: 55Z",
        "timeout": "2020-03-29T08: 33: 55Z",
        "deadline": "2020-04-05T13: 21: 54Z",
        "ws": "40.114.52.201",
        "cs": "13.82.98.119",
        "attempts": 0,
        "slot": "00",
        "tpf": "2 mins 20 secs",
        "basecredit": "9405"
    }
    ]\n"""
    )
    reader.feed_data(b"---\n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"PyON 1 slots\n")
    reader.feed_data(
        b'[{"id": "00", "status": "READY", "description": "cpu: 3", "options": {"idle": "false"}, "reason": "", "idle": False}]\n'  # noqa: line-too-long
    )
    reader.feed_data(b"---\n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    stream_writer = AsyncMock()
    stream_writer.close = MagicMock()
    return (reader, stream_writer)


@pytest.fixture
def stream_reader_writer_slots_before_units():
    """Create a StreamReader and fill it with connection messages."""
    reader = StreamReader()
    reader.feed_data(
        b"\x1b[H\x1b[2JWelcome to the Folding@home Client command server.\n"
    )
    reader.feed_data(b"OK\n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"PyON 1 slots\n")
    reader.feed_data(
        b'[{"id": "00", "status": "READY", "description": "cpu: 3", "options": {"idle": "false"}, "reason": "", "idle": False}]\n'  # noqa: line-too-long
    )
    reader.feed_data(b"---\n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"PyON 1 units\n")
    reader.feed_data(
        b"""[{
        "id": "00",
        "state": "RUNNING",
        "error": "NO_ERROR",
        "project": 11777,
        "run": 0,
        "clone": 17250,
        "gen": 0,
        "core": "0x22",
        "unit": "0x00000003287234c95e774a8488c5d4ea",
        "percentdone": "72.51%",
        "eta": "1 hours 04 mins",
        "ppd": "359072",
        "creditestimate": "58183",
        "waitingon": "",
        "nextattempt": "0.00 secs",
        "timeremaining": "8.08 days",
        "totalframes": 100,
        "framesdone": 72,
        "assigned": "2020-03-28T08: 33: 55Z",
        "timeout": "2020-03-29T08: 33: 55Z",
        "deadline": "2020-04-05T13: 21: 54Z",
        "ws": "40.114.52.201",
        "cs": "13.82.98.119",
        "attempts": 0,
        "slot": "00",
        "tpf": "2 mins 20 secs",
        "basecredit": "9405"
    }
    ]\n"""
    )
    reader.feed_data(b"---\n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    stream_writer = AsyncMock()
    stream_writer.close = MagicMock()
    return (reader, stream_writer)


async def test_sensor(hass, stream_reader_writer):
    """Test that sensor works."""
    with patch("asyncio.StreamWriter.close", return_value=None), patch(
        "asyncio.open_connection",
        return_value=stream_reader_writer,
    ), patch(
        "FoldingAtHomeControl.serialconnection.SerialConnection.send_async",
        return_value=AsyncMock(),
    ):
        entry = MockConfigEntry(
            domain=DOMAIN,
            data={
                CONF_ADDRESS: "localhost",
                CONF_PORT: 36330,
                CONF_PASSWORD: "CONF_UNIT_SYSTEM_IMPERIAL",
            },
        )
        entry.add_to_hass(hass)
        await hass.config_entries.async_setup(entry.entry_id)

        await hass.async_block_till_done()

        hass.bus.async_fire(EVENT_HOMEASSISTANT_START)
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
            hass.states.get("sensor.localhost_00_error").attributes["icon"]
            == "mdi:alert"
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
            hass.states.get("sensor.localhost_00_timeout").state
            == "2020-03-29T08: 33: 55Z"
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
        assert (
            hass.states.get("sensor.localhost_00_work_server").state == "40.114.52.201"
        )
        assert (
            hass.states.get("sensor.localhost_00_work_server").attributes["icon"]
            == "mdi:server-network"
        )
        assert (
            hass.states.get("sensor.localhost_00_collection_server").state
            == "13.82.98.119"
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


async def test_sensor_slots_before_units(hass, stream_reader_writer_slots_before_units):
    """Test that sensor works when slot info is received before unit info."""
    with patch("asyncio.StreamWriter.close", return_value=None), patch(
        "asyncio.open_connection",
        return_value=stream_reader_writer_slots_before_units,
    ), patch(
        "FoldingAtHomeControl.serialconnection.SerialConnection.send_async",
        return_value=AsyncMock(),
    ):
        entry = MockConfigEntry(
            domain=DOMAIN,
            data={
                CONF_ADDRESS: "localhost",
                CONF_PORT: 36330,
                CONF_PASSWORD: "CONF_UNIT_SYSTEM_IMPERIAL",
            },
        )
        entry.add_to_hass(hass)
        await hass.config_entries.async_setup(entry.entry_id)

        await hass.async_block_till_done()

        hass.bus.async_fire(EVENT_HOMEASSISTANT_START)
        await hass.async_block_till_done()
        assert hass.states.get("sensor.localhost_00_status").state == "READY"
        assert (
            hass.states.get("sensor.localhost_00_status").attributes["icon"]
            == "mdi:state-machine"
        )
