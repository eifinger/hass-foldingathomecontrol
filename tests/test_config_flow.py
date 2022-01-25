"""Test foldingathomecontrol config flow."""
from unittest.mock import patch

import pytest
from homeassistant import config_entries, data_entry_flow
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.foldingathomecontrol.const import (
    CONF_READ_TIMEOUT,
    CONF_UPDATE_RATE,
    DOMAIN,
)

from .const import MOCK_CONFIG


# This fixture bypasses the actual setup of the integration
# since we only want to test the config flow. We test the
# actual functionality of the integration in other test modules.
@pytest.fixture(autouse=True)
def bypass_setup_fixture():
    """Prevent setup."""
    with patch(
        "custom_components.foldingathomecontrol.async_setup_entry",
        return_value=True,
    ):
        yield


# Here we simulate a successful config flow from the backend.
# Note that we use the `bypass_login` fixture here because
# we want the config flow validation to succeed during the test.
@pytest.mark.usefixtures("bypass_login")
async def test_successful_config_flow(hass):
    """Test a successful config flow."""
    # Initialize a config flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Check that the config flow shows the user form as the first step
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "user"

    # If a user were to enter `test_username` for username and `test_password`
    # for password, it would result in this function call
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_CONFIG
    )

    # Check that the config flow is complete and a new entry is created with
    # the input data
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["title"] == "localhost"
    assert result["data"] == MOCK_CONFIG
    assert result["result"]


# Here we simulate that an already configured entry is detected.
# Note that we use the `bypass_login` fixture here because
# we want the config flow validation to succeed during the test.
@pytest.mark.usefixtures("bypass_login")
async def test_already_configured(hass):
    """Test already configured result."""
    MockConfigEntry(domain=DOMAIN, data=MOCK_CONFIG, entry_id="test").add_to_hass(hass)

    result = await hass.config_entries.flow.async_init(
        DOMAIN, data=MOCK_CONFIG, context={"source": config_entries.SOURCE_USER}
    )
    assert result.get("type") == "abort"
    assert result.get("reason") == "already_configured"


# In this case, we want to simulate a failure during the config flow.
# We use the `auth_failed_on_login` mock instead of `bypass_login`
# to raise an Exception during
# validation of the input config.
@pytest.mark.usefixtures("auth_failed_on_login")
async def test_auth_failed_config_flow(hass):
    """Test a failed config flow due to credential validation failure."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_CONFIG
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {"base": "auth_failed"}


# In this case, we want to simulate a failure during the config flow.
# We use the `auth_required_on_login` mock instead of `bypass_login`
# to raise an Exception during
# validation of the input config.
@pytest.mark.usefixtures("auth_required_on_login")
async def test_auth_required_config_flow(hass):
    """Test a failed config flow due to credential validation failure."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_CONFIG
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {"base": "auth_required"}


# In this case, we want to simulate a failure during the config flow.
# We use the `connection_failed_on_login` mock instead of `bypass_login`
# to raise an Exception during
# validation of the input config.
@pytest.mark.usefixtures("connection_failed_on_login")
async def test_connection_failed_config_flow(hass):
    """Test a failed config flow due to credential validation failure."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "user"

    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_CONFIG
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {"base": "cannot_connect"}


# Here we simulate a successful import from configuration.yaml.
# Note that we use the `bypass_login` fixture here because
# we want the config flow validation to succeed during the test.
@pytest.mark.usefixtures("bypass_login")
async def test_import(hass):
    """Test a successful config flow."""
    # Initialize a config flow
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_IMPORT}
    )

    # Check that the config flow shows the user form as the first step
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "user"

    # If a user were to enter `test_username` for username and `test_password`
    # for password, it would result in this function call
    result = await hass.config_entries.flow.async_configure(
        result["flow_id"], user_input=MOCK_CONFIG
    )

    # Check that the config flow is complete and a new entry is created with
    # the input data
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["title"] == "localhost"
    assert result["data"] == MOCK_CONFIG
    assert result["result"]


@pytest.mark.usefixtures("bypass_login")
async def test_options_flow(hass):
    """Test the options flow."""
    entry = MockConfigEntry(
        domain=DOMAIN,
        data=MOCK_CONFIG,
    )
    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    result = await hass.config_entries.options.async_init(entry.entry_id)

    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "init"

    result = await hass.config_entries.options.async_configure(
        result["flow_id"],
        user_input={CONF_UPDATE_RATE: 10},
    )

    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert entry.options == {
        CONF_UPDATE_RATE: 10,
        CONF_READ_TIMEOUT: 15,
    }
