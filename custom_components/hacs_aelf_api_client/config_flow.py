"""Config flow definition."""

import typing as t

import voluptuous as vol
from aelf_api_client.schemas.enums import ZoneEnum
from homeassistant import config_entries

from .const import CONF_UPDATE_INTERVAL, CONF_ZONE, DOMAIN


class AELFConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AELF API Client integration."""

    VERSION: int = 1

    async def async_step_user(
        self,
        user_input: t.Dict[str, t.Any] | None = None,
    ) -> config_entries.ConfigFlowResult:
        """Handle the user step of the config flow.

        Args:
            user_input (t.Dict[str, t.Any] | None, optional): The user input. Defaults to None.

        Returns:
            config_entries.ConfigFlowResult: The result of the config flow step.
        """
        if user_input is not None:
            return self.async_create_entry(
                title=f"Liturgical entities for {user_input[CONF_ZONE]}",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_ZONE,
                        description="AELF region/liturgical zone",
                    ): vol.In([zone.value for zone in ZoneEnum]),
                    vol.Required(
                        CONF_UPDATE_INTERVAL,
                        description="AELF update interval (in hours)",
                    ): vol.In([i + 1 for i in range(24)]),
                },
                extra=vol.PREVENT_EXTRA,
            ),
        )

    def is_matching(self, other_flow: config_entries.ConfigFlow) -> bool:
        """Prevent duplicates — called internally by HA when config flow runs.

        Args:
            other_flow (config_entries.ConfigFlow): The other flow.

        Returns:
            bool: True if the entry matches the current user input.
        """
        this_input: t.Any = self.context.get("user_input", {})
        other_input: t.Any = other_flow.context.get("user_input", {})

        return bool(this_input.get(CONF_ZONE) == other_input.get(CONF_ZONE))
