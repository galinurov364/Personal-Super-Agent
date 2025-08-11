#!/usr/bin/env python3
"""
Скрипт для создания меток в GitHub репозитории
"""

import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_REPO = os.getenv('GITHUB_REPO')

def create_label(name, color, description):
    """Создать метку в GitHub репозитории"""
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    data = {
        'name': name,
        'color': color,
        'description': description
    }
    
    url = f'https://api.github.com/repos/{GITHUB_REPO}/labels'
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        print(f"✅ Создана метка: {name}")
        return True
    elif response.status_code == 422:
        print(f"⚠️ Метка уже существует: {name}")
        return True
    else:
        print(f"❌ Ошибка создания метки {name}: {response.status_code}")
        return False

def main():
    """Основная функция"""
    if not GITHUB_TOKEN or not GITHUB_REPO:
        print("❌ Ошибка: Не установлены переменные окружения")
        return
    
    # Список меток для создания
    labels = [
        {
            'name': 'training-log',
            'color': '0e8a16',
            'description': 'Записи о тренировках'
        },
        {
            'name': 'crossfit',
            'color': '1d76db',
            'description': 'Кроссфит тренировки'
        },
        {
            'name': 'wod',
            'color': 'fbca04',
            'description': 'Workout of the Day'
        },
        {
            'name': 'strength',
            'color': 'd93f0b',
            'description': 'Силовые тренировки'
        },
        {
            'name': 'cardio',
            'color': '84b6eb',
            'description': 'Кардио тренировки'
        },
        {
            'name': 'mixed',
            'color': '5319e7',
            'description': 'Смешанные тренировки'
        },
        {
            'name': 'pr',
            'color': 'fef2c0',
            'description': 'Личные рекорды'
        },
        {
            'name': 'progress',
            'color': 'c2e0c6',
            'description': 'Прогресс в тренировках'
        }
    ]
    
    print(f"🏷️ Создание меток для репозитория: {GITHUB_REPO}")
    print("=" * 50)
    
    success_count = 0
    for label in labels:
        if create_label(label['name'], label['color'], label['description']):
            success_count += 1
    
    print("=" * 50)
    print(f"✅ Создано меток: {success_count}/{len(labels)}")

if __name__ == '__main__':
    main()
