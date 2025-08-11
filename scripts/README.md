# 🤖 Telegram Bot для GitHub Issues

## 🎯 Описание
Telegram бот для автоматической записи тренировок в GitHub Issues. Бот позволяет легко записывать данные о тренировках через Telegram и автоматически сохранять их в GitHub Issues с соответствующими метками.

## 🚀 Быстрый старт

### 1. Создание Telegram бота

1. **Откройте Telegram** и найдите @BotFather
2. **Отправьте команду** `/newbot`
3. **Следуйте инструкциям:**
   - Введите имя бота (например: "Training Log Bot")
   - Введите username бота (например: "training_log_bot")
4. **Сохраните токен** - он понадобится для настройки

### 2. Создание GitHub Personal Access Token

1. **Перейдите на GitHub** → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. **Нажмите "Generate new token"** → "Generate new token (classic)"
3. **Настройте токен:**
   - Note: "Training Bot Token"
   - Expiration: Выберите срок действия
   - Scopes: Отметьте `repo` (полный доступ к репозиториям)
4. **Скопируйте токен** - он понадобится для настройки

### 3. Настройка переменных окружения

Создайте файл `.env` в папке `scripts/`:

```bash
# Telegram Bot Token (получите у @BotFather)
TELEGRAM_TOKEN=your_telegram_bot_token_here

# GitHub Personal Access Token
GITHUB_TOKEN=your_github_token_here

# GitHub Repository (формат: username/repository)
GITHUB_REPO=your_username/your_repository_name
```

### 4. Установка зависимостей

```bash
cd scripts/
pip install -r requirements.txt
```

### 5. Запуск бота

```bash
python telegram-training-bot.py
```

## 📱 Использование бота

### Доступные команды

- `/start` - Приветствие и основная информация
- `/help` - Подробная справка
- `/log` - Начать запись новой тренировки
- `/status` - Проверить статус бота

### Процесс записи тренировки

1. **Отправьте `/log`** боту
2. **Выберите тип тренировки:**
   - 🏋️‍♂️ WOD
   - 💪 Силовая
   - 🏃‍♂️ Кардио
   - 🎯 Смешанная
3. **Введите данные по запросу:**
   - Название тренировки
   - Время выполнения
   - Количество раундов/повторений
   - Использованные веса
   - Заметки
4. **Подтвердите сохранение**

### Формат сохраняемых данных

Каждая тренировка сохраняется как GitHub Issue со следующей структурой:

```markdown
# 🏋️‍♂️ Training Log Entry

## 📅 Основная информация
- **Дата:** 2024-12-15
- **Время тренировки:** 10:30
- **Тип тренировки:** wod
- **Название:** Cindy

## 📊 Результаты
- **Время выполнения:** 20:00
- **Раунды/Повторения:** 12
- **Веса:** Не указано

## 📝 Заметки
Хорошая тренировка, улучшил технику pull-ups

---
*Записано через Telegram Bot*
```

### Метки (Labels)

Каждая запись автоматически получает метки:
- `training-log` - общая метка для всех записей
- `crossfit` - указывает на тип тренировок
- `[тип тренировки]` - wod, strength, cardio, mixed

## 🔧 Настройка и кастомизация

### Изменение структуры данных

Для изменения формата сохраняемых данных отредактируйте метод `save_to_github()` в файле `telegram-training-bot.py`.

### Добавление новых полей

1. Добавьте новый метод `ask_new_field()` в класс `TrainingBot`
2. Обновите `handle_text_input()` для обработки нового поля
3. Добавьте поле в `confirm_training()` и `save_to_github()`

### Изменение меток

Отредактируйте список `labels` в методе `save_to_github()`:

```python
labels = ['training-log', 'crossfit', training_data['training_type'], 'your-custom-label']
```

## 🛠️ Развертывание

### Локальный запуск

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск бота
python telegram-training-bot.py
```

### Развертывание на сервере

1. **Загрузите файлы на сервер**
2. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Настройте переменные окружения**
4. **Запустите бота:**
   ```bash
   nohup python telegram-training-bot.py &
   ```

### Использование systemd (Linux)

Создайте файл `/etc/systemd/system/training-bot.service`:

```ini
[Unit]
Description=Training Log Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/your/bot
Environment=PATH=/path/to/your/venv/bin
ExecStart=/path/to/your/venv/bin/python telegram-training-bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Затем:
```bash
sudo systemctl enable training-bot
sudo systemctl start training-bot
```

## 🔍 Отладка и логирование

### Включение логирования

Добавьте в начало `main()`:

```python
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
```

### Проверка статуса

Используйте команду `/status` в боте для проверки:
- Соединения с GitHub
- Информации о репозитории
- Количества открытых issues

## 🚨 Безопасность

### Рекомендации по безопасности

1. **Храните токены в безопасном месте**
2. **Не публикуйте токены в коде**
3. **Используйте переменные окружения**
4. **Регулярно обновляйте токены**
5. **Ограничивайте права токенов**

### Ограничение доступа

Для ограничения доступа к боту:
1. Создайте список разрешенных пользователей
2. Добавьте проверку в обработчики команд
3. Используйте Telegram Bot API для получения информации о пользователе

## 📊 Интеграция с существующей системой

### Автоматическая обработка Issues

Создайте GitHub Action для автоматической обработки новых issues:

```yaml
# .github/workflows/process-training-logs.yml
name: Process Training Logs
on:
  issues:
    types: [opened]

jobs:
  process-training:
    runs-on: ubuntu-latest
    if: contains(github.event.issue.labels.*.name, 'training-log')
    steps:
      - uses: actions/checkout@v3
      - name: Process training data
        run: |
          # Ваша логика обработки
          echo "Processing training log..."
```

### Экспорт данных

Для экспорта данных из Issues в другие форматы используйте GitHub API или создайте скрипт для обработки.

## 🤝 Поддержка

### Полезные ссылки

- [Telegram Bot API Documentation](https://core.telegram.org/bots/api)
- [GitHub REST API Documentation](https://docs.github.com/en/rest)
- [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)

### Сообщество

- [Telegram Bot Developers](https://t.me/botfather)
- [GitHub Community](https://github.com/orgs/community/discussions)

## 📝 Лицензия

Этот проект распространяется под лицензией MIT. См. файл LICENSE для подробностей.


