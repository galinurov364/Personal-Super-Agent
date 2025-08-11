# 🚀 Инструкции по настройке Telegram Bot + GitHub Issues

## 📋 Что нужно сделать

### 1. 🎯 Создание Telegram бота

1. **Откройте Telegram** и найдите @BotFather
2. **Отправьте команду** `/newbot`
3. **Следуйте инструкциям:**
   - Введите имя бота: `Training Log Bot`
   - Введите username: `your_training_log_bot` (должен заканчиваться на 'bot')
4. **Сохраните токен** - он выглядит как `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### 2. 🔑 Создание GitHub Personal Access Token

1. **Перейдите на GitHub** → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. **Нажмите "Generate new token"** → "Generate new token (classic)"
3. **Настройте токен:**
   - **Note:** `Training Bot Token`
   - **Expiration:** Выберите срок (рекомендую 90 дней)
   - **Scopes:** Отметьте `repo` (полный доступ к репозиториям)
4. **Скопируйте токен** - он выглядит как `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### 3. 📁 Настройка переменных окружения

Создайте файл `.env` в папке `scripts/`:

```bash
# Telegram Bot Token (получите у @BotFather)
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# GitHub Personal Access Token
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# GitHub Repository (замените на ваш репозиторий)
GITHUB_REPO=your_username/Personal-Super-Agent
```

### 4. 🐍 Установка Python зависимостей

```bash
cd scripts/
pip install -r requirements.txt
```

### 5. 🚀 Запуск бота

```bash
python telegram-training-bot.py
```

## 📱 Тестирование бота

### 1. Найдите вашего бота в Telegram
- Поищите по username, который вы создали
- Или используйте ссылку: `https://t.me/your_training_log_bot`

### 2. Отправьте команды для тестирования:
- `/start` - должно появиться приветствие
- `/help` - должна появиться справка
- `/status` - должна показаться информация о GitHub репозитории

### 3. Попробуйте записать тренировку:
- Отправьте `/log`
- Выберите тип тренировки
- Заполните данные
- Подтвердите сохранение

## 🔧 Настройка GitHub Actions

### 1. Включите GitHub Actions
- Перейдите в ваш репозиторий на GitHub
- Перейдите в Settings → Actions → General
- Включите "Allow all actions and reusable workflows"

### 2. Проверьте права для Actions
- Перейдите в Settings → Actions → General
- Убедитесь, что "Workflow permissions" установлены в "Read and write permissions"

## 📊 Проверка работы

### 1. После записи тренировки через бота:
- Перейдите в ваш репозиторий на GitHub
- Откройте вкладку "Issues"
- Должна появиться новая issue с данными о тренировке

### 2. Проверьте GitHub Actions:
- Перейдите в вкладку "Actions"
- Должен запуститься workflow "Process Training Logs"
- Проверьте, что он завершился успешно

### 3. Проверьте обновление файлов:
- Откройте файл `Docs/Health/Fitness/CrossFit/workout-log.md`
- Должна появиться новая запись о тренировке

## 🛠️ Устранение неполадок

### Проблема: "Ошибка: Не все переменные окружения установлены"
**Решение:**
- Проверьте, что файл `.env` создан в папке `scripts/`
- Убедитесь, что все переменные заполнены правильно
- Проверьте, что нет лишних пробелов в значениях

### Проблема: "Ошибка соединения с GitHub"
**Решение:**
- Проверьте правильность GitHub токена
- Убедитесь, что токен имеет права `repo`
- Проверьте правильность названия репозитория в `GITHUB_REPO`

### Проблема: "Ошибка при сохранении: 401"
**Решение:**
- GitHub токен недействителен или истек
- Создайте новый токен и обновите `.env` файл

### Проблема: "Ошибка при сохранении: 404"
**Решение:**
- Проверьте правильность названия репозитория
- Убедитесь, что репозиторий существует и доступен

### Проблема: Бот не отвечает
**Решение:**
- Проверьте, что бот запущен (`python telegram-training-bot.py`)
- Убедитесь, что токен Telegram бота правильный
- Проверьте логи на наличие ошибок

## 🔒 Безопасность

### Рекомендации:
1. **Не публикуйте токены** в публичных репозиториях
2. **Добавьте `.env` в `.gitignore`**
3. **Регулярно обновляйте токены**
4. **Используйте минимальные необходимые права** для токенов

### Добавьте в `.gitignore`:
```
scripts/.env
*.pyc
__pycache__/
```

## 📈 Дальнейшее развитие

### Возможные улучшения:
1. **Добавление новых полей** (настроение, энергия, фото)
2. **Интеграция с другими сервисами** (Strava, MyFitnessPal)
3. **Аналитика и отчеты** (графики прогресса)
4. **Уведомления** (напоминания о тренировках)
5. **Экспорт данных** (CSV, PDF отчеты)

### Полезные команды для разработки:
```bash
# Запуск с логированием
python -u telegram-training-bot.py

# Тестирование GitHub API
curl -H "Authorization: token YOUR_TOKEN" https://api.github.com/user

# Проверка переменных окружения
python -c "import os; print(os.getenv('TELEGRAM_TOKEN'))"
```

## 🆘 Поддержка

### Если что-то не работает:
1. Проверьте логи бота
2. Проверьте статус GitHub Actions
3. Убедитесь, что все токены действительны
4. Проверьте права доступа к репозиторию

### Полезные ссылки:
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [GitHub REST API](https://docs.github.com/en/rest)
- [GitHub Actions](https://docs.github.com/en/actions)

---

**Удачи с настройкой! 🚀**
