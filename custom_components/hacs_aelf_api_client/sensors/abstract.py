"""Abstract sensor definition."""

import logging
import typing as t
from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from aelf_api_client.schemas.enums import EntityEnum, ZoneEnum
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)


class AbstractSensor(Entity, ABC):
    """Abstract sensor."""

    entity: EntityEnum
    zone: ZoneEnum
    update_interval: timedelta
    loaded_data: t.Any

    def __init__(
        self,
        zone: ZoneEnum,
        update_interval: timedelta,
        entity: EntityEnum | None = None,
    ) -> None:
        """Initialize the sensor.

        Args:
            zone (ZoneEnum): The liturgical zone.
            update_interval (timedelta): The update interval for the sensor.
            entity (EntityEnum): The entity type.
        """
        if entity is None:
            raise ValueError("An entity must be provided.")
        self.entity = entity
        self.zone = zone
        self.update_interval = update_interval
        self.loaded_data = None

    @property
    def name(self) -> str:
        """Return the name of the sensor.

        Returns:
            str: The name of the sensor.
        """
        return f"{self.entity.value.capitalize()} for {self.zone.value} (updated every {self.update_interval.seconds / 3600} hours)"  # pylint:disable=line-too-long

    @property
    def unique_id(self) -> str:
        """Return a unique ID for the sensor.

        Returns:
            str: The unique ID of the sensor.
        """
        return f"aelf_{self.entity.value}_sensor_{self.zone.value}_{self.update_interval.seconds / 3600}"  # pylint:disable=line-too-long

    @property
    def state(self) -> str:
        """Return the state of the sensor.

        Returns:
            str: The state of the sensor.
        """
        if self.loaded_data is not None:
            return f"Loaded {self.entity.value}."
        return f"No {self.entity.value} loaded."

    @property
    def extra_state_attributes(self) -> t.Dict[str, t.Any]:
        """Return the extra state attributes of the sensor.

        Returns:
            t.Dict[str, t.Any]: The extra state attributes of the sensor.
        """
        return {f"{self.entity.value}": self.loaded_data}

    @abstractmethod
    async def refresh(self, now: datetime = datetime.now()) -> None:  # pylint: disable=unused-argument
        """Fetch entity from AELF API.

        Args:
            now (datetime): The current time.
        """
        raise NotImplementedError(
            f"Subclasses must implement the refresh method for {self.entity.value}."
        )
