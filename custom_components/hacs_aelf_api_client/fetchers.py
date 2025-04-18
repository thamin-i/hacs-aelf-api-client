"""Data fetchers definition."""

import logging
from datetime import datetime

from aelf_api_client import AELFClient
from aelf_api_client.schemas.enums import EntityEnum, ZoneEnum
from aelf_api_client.schemas.responses.masses import MassesResponseModel
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def fetch_masses(hass: HomeAssistant, entry_id: str, zone: ZoneEnum) -> None:  # pylint: disable=unused-argument
    """Fetch masses from AELF API.

    Args:
        hass (HomeAssistant): Home Assistant instance.
        entry_id (str): Config entry ID.
        zone (ZoneEnum): Zone for which to fetch masses.
    """
    client: AELFClient = AELFClient()
    today: datetime = datetime.now()

    _LOGGER.info("Fetching masses for %s [zone: %s]...", today, zone)

    masses_response: MassesResponseModel = await client.request(
        entity=EntityEnum.MASS, zone=zone, date=today
    )

    _LOGGER.info(
        "Fetched %s masses for %s [zone: %s]",
        len(masses_response.messes),
        today,
        zone,
    )

    hass.data[DOMAIN][entry_id]["masses"] = [
        mass.model_dump() for mass in masses_response.messes
    ]
