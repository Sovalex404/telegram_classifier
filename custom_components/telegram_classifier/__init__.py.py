"""
Custom component for Telegram message classification.
"""
from __future__ import annotations

import logging
from typing import Any

import spacy
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN,
    DEFAULT_MODEL,
    CONF_IMPORTANT_SENDERS,
    CONF_TRACKED_NAMES,
    DEFAULT_IMPORTANT_SENDERS,
    DEFAULT_TRACKED_NAMES
)

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the component from YAML (legacy)."""
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a config entry."""
    # Initialize NLP model
    try:
        nlp = spacy.load(DEFAULT_MODEL)
        _LOGGER.info("Successfully loaded spaCy model: %s", DEFAULT_MODEL)
    except Exception as e:
        _LOGGER.error("Failed to load spaCy model: %s", str(e))
        return False

    # Get configuration
    config = {
        CONF_IMPORTANT_SENDERS: entry.data.get(CONF_IMPORTANT_SENDERS, DEFAULT_IMPORTANT_SENDERS),
        CONF_TRACKED_NAMES: entry.data.get(CONF_TRACKED_NAMES, DEFAULT_TRACKED_NAMES)
    }

    # Store in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "nlp": nlp,
        "config": config
    }

    # Register service
    async def async_classify_message(call: ServiceCall) -> dict[str, Any]:
        """Classify Telegram message."""
        message = call.data.get("message", "")
        from_id = call.data.get("from_id", {})

        # Get stored components
        data = hass.data[DOMAIN][entry.entry_id]
        nlp = data["nlp"]
        config = data["config"]

        # Classify message
        result = classify_message(nlp, message, from_id, config)
        return result

    hass.services.async_register(DOMAIN, "classify", async_classify_message)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Remove service
    hass.services.async_remove(DOMAIN, "classify")
    
    # Clean up
    hass.data[DOMAIN].pop(entry.entry_id)
    if not hass.data[DOMAIN]:
        hass.data.pop(DOMAIN)
    
    return True

def classify_message(
    nlp: spacy.language.Language,
    message: str,
    from_id: dict[str, Any],
    config: dict[str, Any]
) -> dict[str, Any]:
    """Classify message using NLP and rules."""
    # Determine sender type
    sender_type = "other"
    user_id = from_id.get("user_id")
    channel_id = from_id.get("channel_id")

    if user_id in config[CONF_IMPORTANT_SENDERS].get("teachers", []):
        sender_type = "teacher"
    elif channel_id in config[CONF_IMPORTANT_SENDERS].get("channels", []):
        sender_type = "important"

    # Process message
    doc = nlp(message)
    result = {
        "type": "normal",
        "category": "other",
        "tags": [],
        "sender_type": sender_type
    }

    # Apply classification rules
    if sender_type in ["teacher", "important"]:
        result["type"] = "important"

        if any(token.text.lower() in ["домашнее задание", "контрольная", "дз"] for token in doc):
            result["category"] = "homework"
        elif any(token.text.lower() in ["праздник", "экскурсия", "мероприятие"] for token in doc):
            result["category"] = "event"

    # Check for mentions
    if any(name.lower() in message.lower() for name in config[CONF_TRACKED_NAMES]):
        result["category"] = "mention"

    # Extract tags
    for token in doc:
        if token.text.lower() in ["математика", "физика", "литература"]:
            result["tags"].append(token.text.lower())
        elif token.like_num and "руб" in doc.text.lower():
            result["tags"].append(f"{token.text} руб")

    return result