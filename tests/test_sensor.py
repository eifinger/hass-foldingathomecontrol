"""Tests for the foldingathomecontrol sensor platform."""
import asyncio
from asyncio.streams import StreamReader
from unittest.mock import AsyncMock, patch

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
def stream_reader_writer(hass):
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
        b'[{"id": "00", "status": "READY", "description": "cpu: 3", "options": {"idle": "false"}, "reason": "", "idle": False}]\n'
    )
    reader.feed_data(b"---\n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_data(b"> \n")
    reader.feed_eof()
    stream_writer = AsyncMock()
    return (reader, stream_writer)


async def test_sensor(hass, stream_reader_writer):
    """Test that sensor works."""
    with patch("asyncio.open_connection", return_value=stream_reader_writer,), patch(
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
        await asyncio.sleep(1)
        assert len(hass.states.async_all()) > 0
