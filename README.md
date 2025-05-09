![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)
# Telegram Classifier
Классификация Telegram-сообщений по отправителям, ключевым словам и упоминаниям.
Используется только совместно с teleram_client

# Важно
Находится в стадии разработки и тестирования, поэтому не рекомендуется для установки никому.
## Установка
1. Установите через [HACS](указав кастомный репозиторий).
2. Перезагрузите Home Assistant.

## Настройка
Добавьте в `configuration.yaml`:
```yaml
telegram_classifier:
  important_senders:
    teachers: [123456789, 987654321]
    channels: [-100123456789]
  tracked_names: ["Коля Иванов"]
```
