"""Masses sensor definition."""

import logging
import typing as t
from datetime import datetime, timedelta

from aelf_api_client import AELFClient
from aelf_api_client.schemas.enums import EntityEnum, ZoneEnum
from aelf_api_client.schemas.responses.masses import MassesResponseModel

from .abstract import AbstractSensor

_LOGGER = logging.getLogger(__name__)


class MassesSensor(AbstractSensor):
    """Masses sensor."""

    loaded_data: t.List[t.Dict[str, t.Any]] | None

    def __init__(
        self,
        zone: ZoneEnum,
        update_interval: timedelta,
        entity: EntityEnum = EntityEnum.MASS,
    ) -> None:
        super().__init__(zone, update_interval, entity)

    async def refresh(self, now: datetime = datetime.now()) -> None:  # pylint: disable=unused-argument
        """Fetch masses from AELF API.

        Args:
            now (datetime): The current time.
        """
        client: AELFClient = AELFClient()
        today: datetime = datetime.now()

        _LOGGER.info("Fetching masses for %s [zone: %s]...", today, self.zone)

        masses_response: MassesResponseModel = await client.request(
            entity=self.entity, zone=self.zone, date=today
        )

        _LOGGER.info(
            "Fetched %s masses for %s [zone: %s]",
            len(masses_response.messes),
            today,
            self.zone,
        )

        self.loaded_data = [mass.model_dump() for mass in masses_response.messes]
