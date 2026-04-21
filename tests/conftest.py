"""Shared pytest fixtures for Caffeine Tracker tests."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

from homeassistant.core import HomeAssistant
import pytest
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.caffeine_tracker.const import (
    CONF_HALF_LIFE_HOURS,
    CONF_PERSON_NAME,
    CONF_SLEEP_SAFE_MG,
    DOMAIN,
)


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Enable custom integrations for all tests in this package."""
    return enable_custom_integrations


@pytest.fixture
def mock_config_entry() -> MockConfigEntry:
    return MockConfigEntry(
        domain=DOMAIN,
        title="Erik",
        data={
            CONF_PERSON_NAME: "Erik",
            CONF_HALF_LIFE_HOURS: 5.0,
            CONF_SLEEP_SAFE_MG: 50.0,
        },
        options={},
        entry_id="test_entry_erik",
    )


@pytest.fixture
def mock_storage():
    """Patch Store so tests don't touch the filesystem."""
    with patch(
        "custom_components.caffeine_tracker.coordinator.Store"
    ) as mock_store_cls:
        store_instance = AsyncMock()
        store_instance.async_load.return_value = None
        store_instance.async_save.return_value = None
        mock_store_cls.return_value = store_instance
        yield store_instance
