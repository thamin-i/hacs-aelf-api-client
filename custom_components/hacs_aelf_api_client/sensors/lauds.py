"""Lauds sensor definition."""

import logging
import typing as t
from datetime import datetime, timedelta

from aelf_api_client import AELFClient
from aelf_api_client.schemas.enums import EntityEnum, ZoneEnum
from aelf_api_client.schemas.responses.lauds import LaudsResponseModel

from .abstract import AbstractSensor

_LOGGER = logging.getLogger(__name__)


class LaudsSensor(AbstractSensor):
    """Lauds sensor."""

    loaded_data: t.Dict[str, t.Any] | None

    def __init__(
        self,
        zone: ZoneEnum,
        update_interval: timedelta,
        entity: EntityEnum = EntityEnum.LAUDS,
    ) -> None:
        super().__init__(zone, update_interval, entity)

    async def refresh(self, now: datetime = datetime.now()) -> None:  # pylint: disable=unused-argument
        """Fetch lauds from AELF API.

        Args:
            now (datetime): The current time.
        """
        client: AELFClient = AELFClient()
        today: datetime = datetime.now()

        _LOGGER.info("Fetching lauds for %s [zone: %s]...", today, self.zone)

        lauds_response: LaudsResponseModel = await client.request(
            entity=self.entity, zone=self.zone, date=today
        )

        _LOGGER.info(
            "Fetched lauds for %s [zone: %s]",
            today,
            self.zone,
        )

        self.loaded_data = lauds_response.laudes.model_dump()
