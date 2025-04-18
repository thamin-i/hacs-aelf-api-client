"""Sensor for the Aelf API Client integration."""

import logging
import typing as t
from datetime import timedelta

from aelf_api_client.schemas.enums import ZoneEnum
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.event import async_track_time_interval

from .const import CONF_UPDATE_INTERVAL, CONF_ZONE, DOMAIN
from .sensors import (
    ComplinesSensor,
    LaudsSensor,
    MassesSensor,
    NoneSensor,
    ReadingsSensor,
    SextSensor,
    TerceSensor,
    VespersSensor,
)
from .sensors.abstract import AbstractSensor

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: t.Callable[[t.List[Entity]], None],
) -> None:
    """Set up the AELF API Client sensor platform.

    Args:
        hass (HomeAssistant): Home Assistant instance.
        config_entry (ConfigEntry): The config entry to set up.
        async_add_entities (t.Callable[[t.List[Entity]], None]): Function to add entities to the platform.  # pylint: disable=line-too-long
    """
    entry_id: str = config_entry.entry_id
    zone: ZoneEnum = ZoneEnum(config_entry.data[CONF_ZONE])
    update_interval: timedelta = timedelta(
        hours=config_entry.data[CONF_UPDATE_INTERVAL]
    )

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry_id] = {}

    sensors_classes: t.List[t.Type[AbstractSensor]] = [
        ComplinesSensor,
        LaudsSensor,
        MassesSensor,
        NoneSensor,
        ReadingsSensor,
        SextSensor,
        TerceSensor,
        VespersSensor,
    ]
    sensors: t.List[AbstractSensor] = [
        sensor_class(
            zone=zone,
            update_interval=update_interval,
        )
        for sensor_class in sensors_classes
    ]

    for sensor in sensors:
        await sensor.refresh()
        async_track_time_interval(hass, sensor.refresh, update_interval)

    async_add_entities(t.cast(t.List[Entity], sensors))
