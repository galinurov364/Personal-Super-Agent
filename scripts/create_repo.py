#!/usr/bin/env python3
"""
Скрипт для создания репозитория через GitHub API
"""

import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def create_repository():
    """Создать репозиторий на GitHub"""
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'name': 'Personal-Super-Agent',
        'description': 'Personal workspace for health tracking, learning, and AI projects',
        'private': False,  # Публичный репозиторий
        'auto_init': False,  # Не создавать README (у нас уже есть файлы)
        'gitignore_template': 'Python',  # Добавить .gitignore для Python
        'license_template': 'mit'  # MIT лицензия
    }
    
    url = 'https://api.github.com/user/repos'
    
    try:
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 201:
            repo_info = response.json()
            print(f"✅ Репозиторий создан успешно!")
            print(f"   Название: {repo_info['full_name']}")
            print(f"   URL: {repo_info['html_url']}")
            print(f"   SSH: {repo_info['ssh_url']}")
            print(f"   HTTPS: {repo_info['clone_url']}")
            return repo_info
        elif response.status_code == 422:
            print("⚠️ Репозиторий уже существует")
            # Попробуем получить информацию о существующем репозитории
            return get_existing_repo()
        else:
            print(f"❌ Ошибка создания репозитория: {response.status_code}")
            print(f"   Ответ: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")
        return None

def get_existing_repo():
    """Получить информацию о существующем репозитории"""
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = 'https://api.github.com/repos/galinurov364/Personal-Super-Agent'
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            repo_info = response.json()
            print(f"✅ Репозиторий найден:")
            print(f"   Название: {repo_info['full_name']}")
            print(f"   URL: {repo_info['html_url']}")
            return repo_info
        else:
            print(f"❌ Ошибка получения репозитория: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Ошибка соединения: {e}")
        return None

def main():
    """Основная функция"""
    if not GITHUB_TOKEN:
        print("❌ GITHUB_TOKEN не установлен")
        return
    
    print("🏗️ Создание репозитория Personal-Super-Agent...")
    print("=" * 50)
    
    repo_info = create_repository()
    
    if repo_info:
        print("\n" + "=" * 50)
        print("🎉 Репозиторий готов!")
        print(f"📋 Следующие шаги:")
        print(f"1. Загрузить код: git push -u origin main")
        print(f"2. Создать метки: python3 create_labels.py")
        print(f"3. Включить GitHub Actions в настройках")
    else:
        print("\n❌ Не удалось создать репозиторий")

if __name__ == '__main__':
    main()
