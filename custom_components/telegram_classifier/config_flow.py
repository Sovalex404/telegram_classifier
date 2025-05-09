from homeassistant import config_entries
from .const import DOMAIN, DEFAULT_IMPORTANT_SENDERS, DEFAULT_TRACKED_NAMES

class TelegramClassifierConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="Telegram Classifier", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Optional("important_senders", default=DEFAULT_IMPORTANT_SENDERS): str,
                vol.Optional("tracked_names", default=DEFAULT_TRACKED_NAMES): str,
            })
        )