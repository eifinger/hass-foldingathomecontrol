"""Global fixtures for foldingathomecontrol integration."""

import logging
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from FoldingAtHomeControl import (
    FoldingAtHomeControlAuthenticationFailed,
    FoldingAtHomeControlAuthenticationRequired,
    FoldingAtHomeControlConnectionFailed,
)

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


@pytest.fixture(name="simplecontroller")
def simplecontroller_fixture():
    """Mock the serialconnection."""
    with patch(
        "custom_components.foldingathomecontrol.foldingathomecontrol_client.FoldingAtHomeController"  # noqa: E501
    ) as mock:

        mock.return_value.start = AsyncMock()
        yield mock


@pytest.fixture(name="foldingathomecontroller")
def foldingathomecontroller_fixture():
    """Mock the serialconnection."""
    with patch(
        "custom_components.foldingathomecontrol.foldingathomecontrol_client.FoldingAtHomeController"  # noqa: E501
    ) as mock:

        mock.return_value.start = AsyncMock()
        register_callback_mock = MagicMock()
        mock.return_value.register_callback = register_callback_mock

        def receive_data(message_type, data):
            """Mock received data on the serialconnection."""
            callback = register_callback_mock.call_args[0][0]

            callback(message_type, data)

        yield receive_data, mock


@pytest.fixture(name="bypass_login")
def bypass_login_fixture():
    """Mock the serialconnection."""
    with patch(
        "custom_components.foldingathomecontrol.config_flow.FoldingAtHomeController"
    ) as mock, patch(
        "custom_components.foldingathomecontrol.foldingathomecontrol_client.FoldingAtHomeController"  # noqa: E501
    ) as mock2:

        mock2.return_value.start = AsyncMock()
        mock.return_value.try_connect_async = AsyncMock()
        mock.return_value.cleanup_async = AsyncMock()
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
