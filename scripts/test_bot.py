#!/usr/bin/env python3
"""
Скрипт для тестирования Telegram бота
"""

import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')

def test_telegram_bot():
    """Тестирование Telegram бота"""
    if not TELEGRAM_TOKEN:
        print("❌ TELEGRAM_TOKEN не установлен")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getMe"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info['ok']:
                print(f"✅ Telegram бот работает:")
                print(f"   Имя: {bot_info['result']['first_name']}")
                print(f"   Username: @{bot_info['result']['username']}")
                print(f"   ID: {bot_info['result']['id']}")
                return True
            else:
                print(f"❌ Ошибка Telegram API: {bot_info}")
                return False
        else:
            print(f"❌ Ошибка HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")
        return False

def test_github_api():
    """Тестирование GitHub API"""
    if not GITHUB_TOKEN or not GITHUB_REPO:
        print("❌ GITHUB_TOKEN или GITHUB_REPO не установлены")
        return False
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Тестируем доступ к пользователю
    user_url = "https://api.github.com/user"
    try:
        response = requests.get(user_url, headers=headers)
        if response.status_code == 200:
            user_info = response.json()
            print(f"✅ GitHub API работает:")
            print(f"   Пользователь: {user_info['login']}")
            print(f"   Имя: {user_info.get('name', 'Не указано')}")
        else:
            print(f"❌ Ошибка GitHub API: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка соединения с GitHub: {e}")
        return False
    
    # Тестируем доступ к репозиторию
    repo_url = f"https://api.github.com/repos/{GITHUB_REPO}"
    try:
        response = requests.get(repo_url, headers=headers)
        if response.status_code == 200:
            repo_info = response.json()
            print(f"✅ Репозиторий доступен:")
            print(f"   Название: {repo_info['full_name']}")
            print(f"   URL: {repo_info['html_url']}")
            print(f"   Приватный: {repo_info['private']}")
            return True
        elif response.status_code == 404:
            print(f"⚠️ Репозиторий не найден: {GITHUB_REPO}")
            print("   Возможно, репозиторий еще не создан или нет доступа")
            return False
        else:
            print(f"❌ Ошибка доступа к репозиторию: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка соединения с репозиторием: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование системы Telegram Bot + GitHub")
    print("=" * 50)
    
    # Тестируем переменные окружения
    print("📋 Проверка переменных окружения:")
    print(f"   TELEGRAM_TOKEN: {'✅' if TELEGRAM_TOKEN else '❌'}")
    print(f"   GITHUB_TOKEN: {'✅' if GITHUB_TOKEN else '❌'}")
    print(f"   GITHUB_REPO: {'✅' if GITHUB_REPO else '❌'}")
    print()
    
    # Тестируем Telegram бота
    print("🤖 Тестирование Telegram бота:")
    telegram_ok = test_telegram_bot()
    print()
    
    # Тестируем GitHub API
    print("🔗 Тестирование GitHub API:")
    github_ok = test_github_api()
    print()
    
    # Итоговый результат
    print("=" * 50)
    if telegram_ok and github_ok:
        print("🎉 Все тесты пройдены! Система готова к работе.")
        print("\n📱 Следующие шаги:")
        print("1. Найдите вашего бота в Telegram")
        print("2. Отправьте команду /start")
        print("3. Попробуйте записать тренировку командой /log")
    else:
        print("❌ Некоторые тесты не пройдены.")
        if not telegram_ok:
            print("   - Проверьте TELEGRAM_TOKEN")
        if not github_ok:
            print("   - Проверьте GITHUB_TOKEN и GITHUB_REPO")
            print("   - Убедитесь, что репозиторий существует и доступен")

if __name__ == '__main__':
    main()
