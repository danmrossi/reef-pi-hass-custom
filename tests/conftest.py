"""Fixtures for testing."""

import pytest


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Auto-enable custom integrations for all tests."""
    yield
