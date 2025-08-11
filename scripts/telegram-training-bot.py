#!/usr/bin/env python3
"""
Telegram Bot для отправки данных о тренировках в GitHub Issues
"""

import os
import json
import requests
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Конфигурация
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')  # format: "username/repository"
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

class TrainingBot:
    def __init__(self):
        self.github_headers = {
            'Authorization': f'token {GITHUB_TOKEN}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.github_api_url = f'https://api.github.com/repos/{GITHUB_REPO}/issues'
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        welcome_text = """
🏋️‍♂️ Добро пожаловать в Training Log Bot!

Этот бот поможет вам записывать тренировки прямо в GitHub Issues.

📝 Доступные команды:
/start - Показать это сообщение
/help - Показать справку
/log - Записать новую тренировку
/status - Показать статус бота

🎯 Как использовать:
1. Отправьте /log для начала записи тренировки
2. Следуйте инструкциям бота
3. Ваша тренировка будет сохранена в GitHub Issues
        """
        await update.message.reply_text(welcome_text)
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = """
📚 Справка по использованию бота:

🔹 /log - Начать запись новой тренировки
   Бот задаст вам вопросы о тренировке и сохранит данные

🔹 Формат данных о тренировке:
   - Дата и время
   - Тип тренировки (WOD, Силовая, Кардио)
   - Название WOD (если применимо)
   - Время выполнения
   - Количество раундов/повторений
   - Веса (если применимо)
   - Заметки и ощущения

🔹 Пример использования:
   1. /log
   2. Выберите тип тренировки
   3. Введите данные
   4. Подтвердите сохранение

🔹 Данные сохраняются в GitHub Issues с метками:
   - training-log
   - crossfit
   - [тип тренировки]
        """
        await update.message.reply_text(help_text)
    
    async def log_training(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начать процесс записи тренировки"""
        keyboard = [
            [InlineKeyboardButton("🏋️‍♂️ WOD", callback_data="type_wod")],
            [InlineKeyboardButton("💪 Силовая", callback_data="type_strength")],
            [InlineKeyboardButton("🏃‍♂️ Кардио", callback_data="type_cardio")],
            [InlineKeyboardButton("🎯 Смешанная", callback_data="type_mixed")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "Выберите тип тренировки:",
            reply_markup=reply_markup
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий на кнопки"""
        query = update.callback_query
        await query.answer()
        
        if query.data.startswith("type_"):
            training_type = query.data.replace("type_", "")
            context.user_data['training_type'] = training_type
            
            # Сохраняем тип тренировки и переходим к следующему шагу
            await self.ask_training_name(query, context)
        
        elif query.data == "confirm_save":
            await self.save_to_github(update, context)
        
        elif query.data == "confirm_cancel":
            await self.cancel_training(update, context)
    
    async def ask_training_name(self, query, context):
        """Спросить название тренировки"""
        training_type = context.user_data['training_type']
        
        if training_type == 'wod':
            await query.edit_message_text(
                "Введите название WOD (например: Cindy, Fran, Murph):\n"
                "Или отправьте 'skip' чтобы пропустить"
            )
        else:
            await query.edit_message_text(
                "Введите название тренировки (например: Back Squat 5x5):\n"
                "Или отправьте 'skip' чтобы пропустить"
            )
        
        context.user_data['awaiting'] = 'training_name'
    
    async def handle_text_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        if 'awaiting' not in context.user_data:
            await update.message.reply_text(
                "Используйте /log для начала записи тренировки"
            )
            return
        
        awaiting = context.user_data['awaiting']
        text = update.message.text
        
        if awaiting == 'training_name':
            if text.lower() == 'skip':
                context.user_data['training_name'] = 'Не указано'
            else:
                context.user_data['training_name'] = text
            
            await self.ask_duration(update, context)
        
        elif awaiting == 'duration':
            if text.lower() == 'skip':
                context.user_data['duration'] = 'Не указано'
            else:
                context.user_data['duration'] = text
            
            await self.ask_rounds(update, context)
        
        elif awaiting == 'rounds':
            if text.lower() == 'skip':
                context.user_data['rounds'] = 'Не указано'
            else:
                context.user_data['rounds'] = text
            
            await self.ask_weights(update, context)
        
        elif awaiting == 'weights':
            if text.lower() == 'skip':
                context.user_data['weights'] = 'Не указано'
            else:
                context.user_data['weights'] = text
            
            await self.ask_notes(update, context)
        
        elif awaiting == 'notes':
            if text.lower() == 'skip':
                context.user_data['notes'] = 'Нет заметок'
            else:
                context.user_data['notes'] = text
            
            await self.confirm_training(update, context)
    
    async def ask_duration(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Спросить время выполнения"""
        await update.message.reply_text(
            "Введите время выполнения (например: 15:30, 20:00):\n"
            "Или отправьте 'skip' чтобы пропустить"
        )
        context.user_data['awaiting'] = 'duration'
    
    async def ask_rounds(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Спросить количество раундов/повторений"""
        await update.message.reply_text(
            "Введите количество раундов или повторений:\n"
            "Или отправьте 'skip' чтобы пропустить"
        )
        context.user_data['awaiting'] = 'rounds'
    
    async def ask_weights(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Спросить веса"""
        await update.message.reply_text(
            "Введите использованные веса (например: 100кг, 95/65 lbs):\n"
            "Или отправьте 'skip' чтобы пропустить"
        )
        context.user_data['awaiting'] = 'weights'
    
    async def ask_notes(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Спросить заметки"""
        await update.message.reply_text(
            "Введите заметки о тренировке (ощущения, улучшения, проблемы):\n"
            "Или отправьте 'skip' чтобы пропустить"
        )
        context.user_data['awaiting'] = 'notes'
    
    async def confirm_training(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать подтверждение тренировки"""
        training_data = context.user_data
        
        summary = f"""
📋 Подтвердите данные тренировки:

🏋️‍♂️ Тип: {training_data['training_type']}
📝 Название: {training_data['training_name']}
⏱️ Время: {training_data['duration']}
🔄 Раунды: {training_data['rounds']}
🏋️ Веса: {training_data['weights']}
📝 Заметки: {training_data['notes']}

Все верно?
        """
        
        keyboard = [
            [InlineKeyboardButton("✅ Сохранить", callback_data="confirm_save")],
            [InlineKeyboardButton("❌ Отменить", callback_data="confirm_cancel")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(summary, reply_markup=reply_markup)
    
    async def save_to_github(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Сохранить тренировку в GitHub Issues"""
        query = update.callback_query
        training_data = context.user_data
        
        # Создаем заголовок issue
        current_date = datetime.now().strftime("%Y-%m-%d")
        title = f"Training Log - {current_date} - {training_data['training_name']}"
        
        # Создаем тело issue
        body = f"""
# 🏋️‍♂️ Training Log Entry

## 📅 Основная информация
- **Дата:** {current_date}
- **Время тренировки:** {datetime.now().strftime("%H:%M")}
- **Тип тренировки:** {training_data['training_type']}
- **Название:** {training_data['training_name']}

## 📊 Результаты
- **Время выполнения:** {training_data['duration']}
- **Раунды/Повторения:** {training_data['rounds']}
- **Веса:** {training_data['weights']}

## 📝 Заметки
{training_data['notes']}

---
*Записано через Telegram Bot*
        """
        
        # Подготавливаем метки
        labels = ['training-log', 'crossfit', training_data['training_type']]
        
        # Данные для GitHub API
        issue_data = {
            'title': title,
            'body': body,
            'labels': labels
        }
        
        try:
            response = requests.post(
                self.github_api_url,
                headers=self.github_headers,
                json=issue_data
            )
            
            if response.status_code == 201:
                issue_url = response.json()['html_url']
                await query.edit_message_text(
                    f"✅ Тренировка успешно сохранена!\n\n"
                    f"🔗 Ссылка: {issue_url}\n\n"
                    f"Используйте /log для записи следующей тренировки"
                )
            else:
                await query.edit_message_text(
                    f"❌ Ошибка при сохранении: {response.status_code}\n"
                    f"Попробуйте позже или обратитесь к администратору"
                )
                
        except Exception as e:
            await query.edit_message_text(
                f"❌ Ошибка соединения: {str(e)}\n"
                f"Проверьте настройки бота"
            )
        
        # Очищаем данные пользователя
        context.user_data.clear()
    
    async def cancel_training(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отменить запись тренировки"""
        query = update.callback_query
        context.user_data.clear()
        
        await query.edit_message_text(
            "❌ Запись тренировки отменена.\n\n"
            "Используйте /log для начала новой записи"
        )
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать статус бота"""
        try:
            response = requests.get(
                f'https://api.github.com/repos/{GITHUB_REPO}',
                headers=self.github_headers
            )
            
            if response.status_code == 200:
                repo_info = response.json()
                status_text = f"""
🤖 Статус бота:

✅ GitHub соединение: Работает
📁 Репозиторий: {repo_info['full_name']}
🔗 URL: {repo_info['html_url']}
📊 Issues: {repo_info['open_issues_count']}

Используйте /log для записи тренировки
                """
            else:
                status_text = f"❌ Ошибка соединения с GitHub: {response.status_code}"
                
        except Exception as e:
            status_text = f"❌ Ошибка: {str(e)}"
        
        await update.message.reply_text(status_text)

def main():
    """Основная функция"""
    if not all([GITHUB_TOKEN, GITHUB_REPO, TELEGRAM_TOKEN]):
        print("❌ Ошибка: Не все переменные окружения установлены")
        print("Убедитесь, что установлены: GITHUB_TOKEN, GITHUB_REPO, TELEGRAM_TOKEN")
        return
    
    # Создаем экземпляр бота
    bot = TrainingBot()
    
    # Создаем приложение
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help))
    application.add_handler(CommandHandler("log", bot.log_training))
    application.add_handler(CommandHandler("status", bot.status))
    application.add_handler(CallbackQueryHandler(bot.button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, bot.handle_text_input))
    
    # Запускаем бота
    print("🤖 Training Bot запущен...")
    application.run_polling()

if __name__ == '__main__':
    main()
