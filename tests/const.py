"""Constants for foldingathomecontrol tests."""
from __future__ import annotations

from typing import Dict

from custom_components.foldingathomecontrol.const import (
    CONF_ADDRESS,
    CONF_PASSWORD,
    CONF_PORT,
)

# Mock config data to be used across multiple tests
MOCK_CONFIG: Dict[str, str | int] = {
    CONF_ADDRESS: "localhost",
    CONF_PORT: 36330,
    CONF_PASSWORD: "password",
}

SLOTS_DATA = [
    {
        "id": "00",
        "status": "READY",
        "description": "cpu: 3",
        "options": {"idle": "false"},
        "reason": "",
        "idle": False,
    }
]

OPTIONS_DATA = {
    "allow": "0/0",
    "command-address": "0.0.0.0",
    "command-allow-no-pass": "0/0",
    "command-port": "36330",
    "http-addresses": "0.0.0.0:7396",
    "power": "Light",
    "smp": "true",
    "team": "247478",
    "user": "Anonymous",
    "web-allow": "0/0",
}

UNITS_DATA = [
    {
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
        "basecredit": "9405",
    }
]
