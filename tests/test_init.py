"""Test weenect setup process."""
import pytest
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.foldingathomecontrol import (
    async_reload_entry,
    async_setup_entry,
    async_unload_entry,
)
from custom_components.foldingathomecontrol.const import CLIENT, DOMAIN
from custom_components.foldingathomecontrol.foldingathomecontrol_client import (
    FoldingAtHomeControlClient,
)

from .const import MOCK_CONFIG


# We can pass fixtures as defined in conftest.py to tell pytest to use the fixture
# for a given test. We can also leverage fixtures and mocks that are available in
# Home Assistant using the pytest_homeassistant_custom_component plugin.
# Assertions allow you to verify that the return value of whatever is on the left
# side of the assertion matches with the right side.
@pytest.mark.usefixtures("bypass_login")
async def test_setup_unload_and_reload_entry(hass):
    """Test entry setup and unload."""
    # Create a mock entry so we don't have to go through config flow
    config_entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    config_entry.add_to_hass(hass)
    await hass.config_entries.async_setup(config_entry.entry_id)

    await hass.async_block_till_done()
    assert DOMAIN in hass.data and config_entry.entry_id in hass.data[DOMAIN]
    assert isinstance(hass.data[DOMAIN][config_entry.entry_id][CLIENT], FoldingAtHomeControlClient)

    # Reload the entry and assert that the data from above is still there
    await async_reload_entry(hass, config_entry)
    assert DOMAIN in hass.data and config_entry.entry_id in hass.data[DOMAIN]
    assert isinstance(hass.data[DOMAIN][config_entry.entry_id][CLIENT], FoldingAtHomeControlClient)

    # Unload the entry and verify that the data has been removed
    assert await async_unload_entry(hass, config_entry)
    assert config_entry.entry_id not in hass.data[DOMAIN]


@pytest.mark.usefixtures("connection_failed")
async def test_setup_entry_exception(hass):
    """Test ConfigEntryNotReady when API raises an exception during entry setup."""
    config_entry = MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test")

    # In this case we are testing the condition where async_setup_entry raises
    # ConfigEntryNotReady using the `connection_failed` fixture which simulates
    # an error.
    with pytest.raises(ConfigEntryNotReady):
        assert await async_setup_entry(hass, config_entry)


@pytest.mark.usefixtures("bypass_login")
async def test_import(hass):
    """Test import from configuration.yaml."""
    config = {DOMAIN: MOCK_CONFIG}
    assert await async_setup_component(hass, DOMAIN, config)
    await hass.async_block_till_done()

    assert len(hass.states.async_all()) == 3


async def test_error_received(hass, foldingathomecontroller, caplog):
    """Test that error is logged."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)

    await hass.async_block_till_done()

    callback, _, _ = foldingathomecontroller
    callback("error", "Something happened!")
    await hass.async_block_till_done()
    assert "localhost received error: Something happened!" in caplog.text
