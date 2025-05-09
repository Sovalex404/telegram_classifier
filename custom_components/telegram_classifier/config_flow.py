"""Config flow for Telegram Classifier."""
from typing import Any, Dict, Optional
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from .const import (
    DOMAIN,
    CONF_IMPORTANT_SENDERS,
    CONF_TRACKED_NAMES,
    DEFAULT_IMPORTANT_SENDERS,
    DEFAULT_TRACKED_NAMES
)

class TelegramClassifierConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Telegram Classifier."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="Telegram Classifier",
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Optional(
                    CONF_IMPORTANT_SENDERS,
                    default=DEFAULT_IMPORTANT_SENDERS
                ): str,
                vol.Optional(
                    CONF_TRACKED_NAMES,
                    default=",".join(DEFAULT_TRACKED_NAMES)
                ): str,
            }),
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry
    ) -> config_entries.OptionsFlow:
        """Create the options flow."""
        return TelegramClassifierOptionsFlow(config_entry)

class TelegramClassifierOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow updates."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: Optional[Dict[str, Any]] = None
    ) -> FlowResult:
        """Manage the options."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    CONF_IMPORTANT_SENDERS,
                    default=self.config_entry.options.get(
                        CONF_IMPORTANT_SENDERS,
                        DEFAULT_IMPORTANT_SENDERS
                    )
                ): str,
                vol.Optional(
                    CONF_TRACKED_NAMES,
                    default=",".join(
                        self.config_entry.options.get(
                            CONF_TRACKED_NAMES,
                            DEFAULT_TRACKED_NAMES
                        )
                    )
                ): str,
            }),
            errors=errors
        )
