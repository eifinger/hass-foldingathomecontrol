"""Global fixtures for foldingathomecontrol integration."""

import logging
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from FoldingAtHomeControl import (
    FoldingAtHomeControlAuthenticationFailed,
    FoldingAtHomeControlAuthenticationRequired,
    FoldingAtHomeControlConnectionFailed,
)

from tests.const import UNITS_DATA

_LOGGER: logging.Logger = logging.getLogger(__package__)

pytest_plugins = "pytest_homeassistant_custom_component"  # pylint: disable=invalid-name


# This fixture enables loading custom integrations in all tests.
# Remove to enable selective use of this fixture
@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):  # noqa: F841
    """Enable custom integration loading."""
    yield


# This fixture is used to prevent HomeAssistant from attempting
# to create and dismiss persistent notifications.
# These calls would fail without this fixture since the persistent_notification
# integration is never loaded during a test.
@pytest.fixture(name="skip_notifications", autouse=True)
def skip_notifications_fixture():
    """Skip notification calls."""
    with patch("homeassistant.components.persistent_notification.async_create"), patch(
        "homeassistant.components.persistent_notification.async_dismiss"
    ):
        yield


@pytest.fixture(name="no_slots_controller")
def no_slots_controller_fixture():
    """Send only unit data."""
    with patch(
        "custom_components.foldingathomecontrol.foldingathomecontrol_client.FoldingAtHomeController"  # noqa: E501
    ) as mock:

        def register_callback(callback):
            """Immediately send unit data when the client is created."""

            callback("units", UNITS_DATA)

        mock.return_value.start = AsyncMock()
        mock.return_value.send_command_async = AsyncMock()
        mock.return_value.register_callback = register_callback

        yield mock


@pytest.fixture(name="foldingathomecontroller")
def foldingathomecontroller_fixture():
    """Mock the serialconnection."""
    with patch(
        "custom_components.foldingathomecontrol.foldingathomecontrol_client.FoldingAtHomeController"  # noqa: E501
    ) as mock:

        mock.return_value.start = AsyncMock()
        mock.return_value.update_rate = 5
        mock.return_value.send_command_async = AsyncMock()
        register_callback_mock = MagicMock()
        mock.return_value.register_callback = register_callback_mock

        def receive_data(message_type, data):
            """Mock received data on the serialconnection."""
            callback = register_callback_mock.call_args[0][0]

            callback(message_type, data)

        register_on_disconnect_callback_mock = MagicMock()
        mock.return_value.on_disconnect = register_on_disconnect_callback_mock

        def disconnect():
            """Call the disconnect callback."""
            callback = register_on_disconnect_callback_mock.call_args[0][0]

            callback()

        yield receive_data, disconnect, mock


@pytest.fixture(name="bypass_login")
def bypass_login_fixture():
    """Mock the serialconnection."""
    with patch(
        "custom_components.foldingathomecontrol.config_flow.FoldingAtHomeController"
    ) as config_flow_mock, patch(
        "custom_components.foldingathomecontrol.foldingathomecontrol_client.FoldingAtHomeController"  # noqa: E501
    ) as client_mock:

        client_mock.return_value.start = AsyncMock()
        client_mock.return_value.update_rate = 5
        client_mock.return_value.send_command_async = AsyncMock()
        config_flow_mock.return_value.try_connect_async = AsyncMock()
        config_flow_mock.return_value.cleanup_async = AsyncMock()
        yield


@pytest.fixture(name="auth_failed_on_login")
def auth_failed_on_login_fixture():
    """Mock the serialconnection."""
    with patch(
        "custom_components.foldingathomecontrol.config_flow.FoldingAtHomeController"
    ) as mock:

        mock.return_value.try_connect_async = AsyncMock(
            side_effect=FoldingAtHomeControlAuthenticationFailed
        )
        yield


@pytest.fixture(name="auth_required_on_login")
def auth_required_on_login_fixture():
    """Mock the serialconnection."""
    with patch(
        "custom_components.foldingathomecontrol.config_flow.FoldingAtHomeController"
    ) as mock:

        mock.return_value.try_connect_async = AsyncMock(
            side_effect=FoldingAtHomeControlAuthenticationRequired
        )
        yield


@pytest.fixture(name="connection_failed_on_login")
def connection_failed_on_login_fixture():
    """Mock the serialconnection."""
    with patch(
        "custom_components.foldingathomecontrol.config_flow.FoldingAtHomeController"
    ) as mock:

        mock.return_value.try_connect_async = AsyncMock(
            side_effect=FoldingAtHomeControlConnectionFailed
        )
        yield


@pytest.fixture(name="connection_failed")
def connection_failed_fixture():
    """Mock the serialconnection."""
    with patch(
        "custom_components.foldingathomecontrol.foldingathomecontrol_client.FoldingAtHomeController",  # noqa: E501
        side_effect=FoldingAtHomeControlConnectionFailed,
    ):
        yield
