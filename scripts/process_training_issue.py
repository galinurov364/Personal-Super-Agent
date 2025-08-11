#!/usr/bin/env python3
"""
Скрипт для обработки training log issues и обновления файлов
"""

import os
import sys
import re
import requests
from datetime import datetime

def get_issue_data(issue_number):
    """Получить данные issue из GitHub API"""
    token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPOSITORY')  # Автоматически устанавливается GitHub Actions
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    url = f'https://api.github.com/repos/{repo}/issues/{issue_number}'
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка получения issue: {response.status_code}")
        return None

def parse_training_data(issue_body):
    """Парсинг данных тренировки из тела issue"""
    data = {}
    
    # Извлекаем дату
    date_match = re.search(r'\*\*Дата:\*\* (\d{4}-\d{2}-\d{2})', issue_body)
    if date_match:
        data['date'] = date_match.group(1)
    
    # Извлекаем время тренировки
    time_match = re.search(r'\*\*Время тренировки:\*\* (\d{2}:\d{2})', issue_body)
    if time_match:
        data['time'] = time_match.group(1)
    
    # Извлекаем тип тренировки
    type_match = re.search(r'\*\*Тип тренировки:\*\* (\w+)', issue_body)
    if type_match:
        data['type'] = type_match.group(1)
    
    # Извлекаем название
    name_match = re.search(r'\*\*Название:\*\* (.+)', issue_body)
    if name_match:
        data['name'] = name_match.group(1)
    
    # Извлекаем время выполнения
    duration_match = re.search(r'\*\*Время выполнения:\*\* (.+)', issue_body)
    if duration_match:
        data['duration'] = duration_match.group(1)
    
    # Извлекаем раунды
    rounds_match = re.search(r'\*\*Раунды/Повторения:\*\* (.+)', issue_body)
    if rounds_match:
        data['rounds'] = rounds_match.group(1)
    
    # Извлекаем веса
    weights_match = re.search(r'\*\*Веса:\*\* (.+)', issue_body)
    if weights_match:
        data['weights'] = weights_match.group(1)
    
    # Извлекаем заметки
    notes_match = re.search(r'## 📝 Заметки\n(.+?)(?=\n---|\n$)', issue_body, re.DOTALL)
    if notes_match:
        data['notes'] = notes_match.group(1).strip()
    
    return data

def update_workout_log(training_data):
    """Обновить файл workout-log.md"""
    log_file = 'Docs/Health/Fitness/CrossFit/workout-log.md'
    
    # Создаем запись тренировки
    workout_entry = f"""
### 📅 {training_data['date']} - {get_day_of_week(training_data['date'])}
**Время:** {training_data['time']}  
**Тип:** {training_data['type']}  
**Настроение:** [1-10]  
**Энергия:** [1-10]  

#### 💪 Основная тренировка
**WOD:** {training_data['name']}

**Результаты:**
- **Время:** {training_data['duration']}
- **Раунды:** {training_data['rounds']}
- **Вес:** {training_data['weights']}
- **Интенсивность:** [1-10]

#### 📝 Заметки
{training_data['notes']}

#### ✅ Проверка диапазонов
**Проверено:** `python3 scripts/check_range.py [значения] [диапазоны]`

---
"""
    
    # Читаем существующий файл
    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Файл {log_file} не найден")
        return False
    
    # Находим место для вставки (после заголовка и перед шаблоном)
    lines = content.split('\n')
    insert_index = None
    
    for i, line in enumerate(lines):
        if line.startswith('## 🎯 Шаблон тренировки'):
            insert_index = i
            break
    
    if insert_index is None:
        # Если не нашли шаблон, вставляем после заголовка
        for i, line in enumerate(lines):
            if line.startswith('## 📅 Текущий месяц'):
                insert_index = i + 2
                break
    
    if insert_index is None:
        print("Не удалось найти место для вставки")
        return False
    
    # Вставляем новую запись
    lines.insert(insert_index, workout_entry)
    
    # Записываем обновленный файл
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"Обновлен файл {log_file}")
    return True

def update_personal_records(training_data):
    """Обновить файл personal-records.md если есть новые рекорды"""
    # Здесь можно добавить логику для обновления PR
    # Например, если время выполнения лучше предыдущего
    pass

def update_progress_tracking(training_data):
    """Обновить файл progress-tracking.md"""
    progress_file = 'Docs/Health/Fitness/CrossFit/progress-tracking.md'
    
    # Здесь можно добавить логику для обновления статистики
    # Например, подсчет количества тренировок в месяц
    pass

def get_day_of_week(date_str):
    """Получить день недели по дате"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
        return days[date_obj.weekday()]
    except:
        return ''

def main():
    """Основная функция"""
    if len(sys.argv) != 2:
        print("Использование: python process_training_issue.py <issue_number>")
        sys.exit(1)
    
    issue_number = sys.argv[1]
    
    # Получаем данные issue
    issue_data = get_issue_data(issue_number)
    if not issue_data:
        print(f"Не удалось получить данные issue #{issue_number}")
        sys.exit(1)
    
    # Парсим данные тренировки
    training_data = parse_training_data(issue_data['body'])
    if not training_data:
        print("Не удалось распарсить данные тренировки")
        sys.exit(1)
    
    print(f"Обрабатываем тренировку: {training_data['name']} от {training_data['date']}")
    
    # Обновляем файлы
    success = update_workout_log(training_data)
    
    if success:
        print("✅ Тренировка успешно обработана")
    else:
        print("❌ Ошибка при обработке тренировки")
        sys.exit(1)

if __name__ == '__main__':
    main()
