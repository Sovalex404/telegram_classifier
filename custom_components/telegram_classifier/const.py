"""Constants for Telegram Classifier."""
from typing import Final, Dict, List

DOMAIN: Final[str] = "telegram_classifier"

# Configuration keys
CONF_IMPORTANT_SENDERS: Final[str] = "important_senders"
CONF_TRACKED_NAMES: Final[str] = "tracked_names"
CONF_MODEL_PATH: Final[str] = "model_path"

# Default values
DEFAULT_MODEL: Final[str] = "ru_core_news_sm"
DEFAULT_IMPORTANT_SENDERS: Final[Dict[str, List[int]]] = {
    "teachers": [123456789],
    "channels": [-10012345678]
}
DEFAULT_TRACKED_NAMES: Final[List[str]] = ["Коля Иванов"]

# Service attributes
ATTR_MESSAGE: Final[str] = "message"
ATTR_FROM_ID: Final[str] = "from_id"
ATTR_RESULT: Final[str] = "result"

# Classification types
TYPE_IMPORTANT: Final[str] = "important"
TYPE_NORMAL: Final[str] = "normal"
TYPE_NOISE: Final[str] = "noise"

# Categories
CATEGORY_HOMEWORK: Final[str] = "homework"
CATEGORY_EVENT: Final[str] = "event"
CATEGORY_MENTION: Final[str] = "mention"
CATEGORY_OTHER: Final[str] = "other"
