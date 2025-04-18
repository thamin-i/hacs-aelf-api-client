"""None sensor definition."""

import logging
import typing as t
from datetime import datetime, timedelta

from aelf_api_client import AELFClient
from aelf_api_client.schemas.enums import EntityEnum, ZoneEnum
from aelf_api_client.schemas.responses.none import NoneResponseModel

from .abstract import AbstractSensor

_LOGGER = logging.getLogger(__name__)


class NoneSensor(AbstractSensor):
    """None sensor."""

    loaded_data: t.Dict[str, t.Any] | None

    def __init__(
        self,
        zone: ZoneEnum,
        update_interval: timedelta,
        entity: EntityEnum = EntityEnum.NONE,
    ) -> None:
        super().__init__(zone, update_interval, entity)

    async def refresh(self, now: datetime = datetime.now()) -> None:  # pylint: disable=unused-argument
        """Fetch none from AELF API.

        Args:
            now (datetime): The current time.
        """
        client: AELFClient = AELFClient()
        today: datetime = datetime.now()

        _LOGGER.info("Fetching none for %s [zone: %s]...", today, self.zone)

        none_response: NoneResponseModel = await client.request(
            entity=self.entity, zone=self.zone, date=today
        )

        _LOGGER.info(
            "Fetched none for %s [zone: %s]",
            today,
            self.zone,
        )

        self.loaded_data = none_response.none.model_dump()
