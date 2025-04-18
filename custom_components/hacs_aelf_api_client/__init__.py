"""Initialize the AELF API Client integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up the AELF API Client integration from a config entry.

    Args:
        hass (HomeAssistant): Home Assistant instance.
        entry (ConfigEntry): The config entry to set up.

    Returns:
        bool: True if the setup was successful, False otherwise.
    """
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = entry.data

    await hass.async_create_task(
        hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:  # pylint: disable=unused-argument
    """Unload a config entry.

    Args:
        hass (HomeAssistant): Home Assistant instance.
        entry (ConfigEntry): The config entry to unload.

    Returns:
        bool: True if the unload was successful, False otherwise.
    """
    if DOMAIN in hass.data:
        hass.data.pop(DOMAIN)

    return True
