import asyncio
from unittest.mock import patch

import pytest
import respx
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.reef_pi import DOMAIN

from . import async_api_mock


@pytest.fixture
async def async_api_mock_instance():
    with respx.mock() as mock:
        async_api_mock.mock_all(mock)
        yield mock


@pytest.mark.asyncio
async def test_ph_calibration_buttons(hass, async_api_mock_instance):
    entry = MockConfigEntry(
        domain=DOMAIN,
        data={
            "host": async_api_mock.REEF_MOCK_URL,
            "username": async_api_mock.REEF_MOCK_USER,
            "password": async_api_mock.REEF_MOCK_PASSWORD,
            "verify": False,
        },
    )

    entry.add_to_hass(hass)
    await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()

    route = async_api_mock_instance.post(
        f"{async_api_mock.REEF_MOCK_URL}/api/phprobes/6/calibratepoint"
    ).respond(200, json={})

    with patch("custom_components.reef_pi.__init__.PH_CALIBRATION_DELAY", 0), patch(
        "asyncio.sleep",
        return_value=asyncio.Future(),
    ) as sleep_mock:
        sleep_mock.return_value.set_result(None)
        await hass.services.async_call(
            "button",
            "press",
            {"entity_id": "button.reef_pi_calibrate_ph_freshwater"},
            blocking=True,
        )

    assert route.call_count == 2
