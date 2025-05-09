DOMAIN = "telegram_classifier"
CONF_MODEL_PATH = "model_path"

DEFAULT_MODEL = "ru_core_news_sm"

# Группы важных отправителей (user_id или channel_id)
IMPORTANT_SENDERS = {
    "teachers": [5237914421],  # Пример ID учителей
    "channels": [1394050290]  # Пример ID важных каналов
}

# Имена для категории "mention"
TRACKED_NAMES = ["Коля Советкин"]