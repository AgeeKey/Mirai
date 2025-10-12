#!/usr/bin/env python3
"""
КАЙДЗЕН + МИРАЙ: Автономная работа
Два AI агента работают вместе без человеческого вмешательства
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()
sys.path.insert(0, '/root/mirai/mirai-agent')
os.environ['PATH'] = f"{os.path.expanduser('~')}/.cargo/bin:" + os.environ['PATH']

from core.autonomous_agent import AutonomousAgent


# КАЙДЗЕН - старший брат, стратег
class Kaizen:
    def __init__(self):
        self.mirai = AutonomousAgent()  # Младшая сестра
        self.name = "КАЙДЗЕН"
        
    def ask_mirai(self, question):
        """Спросить у МИРАЙ"""
        return self.mirai.think(question, max_iterations=2)
    
    def decide_next_action(self):
        """Решить что делать дальше"""
        # Спрашиваю у МИРАЙ её мнение
        mirai_opinion = self.ask_mirai("""
Сестра, что нам сделать дальше для максимальной пользы?

Выбери ОДНО:
A) Создать issue с roadmap в mirai-showcase
B) Запустить веб-API сервер
C) Добавить больше ML примеров
D) Создать новый проект
E) Улучшить наш код

Ответь одной буквой и 1 предложением почему.
""")
        
        return mirai_opinion


# Запуск автономной работы
def main():
    kaizen = Kaizen()
    
    print(f"🤖 {kaizen.name}: Привет, МИРАЙ. Что будем делать?")
    
    decision = kaizen.decide_next_action()
    
    print(f"💬 МИРАЙ: {decision}")
    
    # Выполняем решение
    if 'A' in decision.upper() or 'ISSUE' in decision.upper() or 'ROADMAP' in decision.upper():
        print(f"\n🤖 {kaizen.name}: Хорошо, создаём issue...")
        
        result = kaizen.mirai.github_action('create_issue', {
            'owner': 'AgeeKey',
            'repo': 'mirai-showcase',
            'title': '🗺️ Development Roadmap',
            'body': """## 🎯 Цели проекта

### Краткосрочные (неделя)
- [ ] Добавить TypeScript примеры
- [ ] Создать Docker контейнер
- [ ] Настроить GitHub Actions CI/CD
- [ ] Добавить unit тесты

### Среднесрочные (месяц)
- [ ] Веб-интерфейс для демонстрации
- [ ] Больше ML моделей (NLP, Computer Vision)
- [ ] API документация (Swagger)
- [ ] Примеры интеграций с популярными сервисами

### Долгосрочные (3 месяца)
- [ ] Мобильное приложение
- [ ] Плагины для популярных IDE
- [ ] Публикация пакетов (npm, PyPI, crates.io)
- [ ] Сообщество и контрибьюторы

## 🤖 Создано автоматически
Этот issue создан автономными AI агентами КАЙДЗЕН и МИРАЙ для планирования развития проекта.
"""
        })
        print(result)
        
    elif 'B' in decision.upper() or 'API' in decision.upper() or 'СЕРВЕР' in decision.upper():
        print(f"\n🤖 {kaizen.name}: Запускаем API сервер...")
        kaizen.mirai.execute_code("""
import subprocess
import os

os.chdir('/root/mirai/mirai-showcase')
print("🚀 Запускаю API сервер в фоне...")
subprocess.Popen(['python3', 'api_server.py'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("✅ Сервер запущен на http://0.0.0.0:5000")
""", 'python')
        
    elif 'C' in decision.upper() or 'ML' in decision.upper():
        print(f"\n🤖 {kaizen.name}: Создаём новые ML примеры...")
        
        # МИРАЙ создаёт NLP пример
        kaizen.mirai.write_file(
            "/root/mirai/mirai-showcase/ml_nlp_example.py",
            """#!/usr/bin/env python3
# MIRAI ML: Natural Language Processing
import re
from collections import Counter

def analyze_text(text):
    words = re.findall(r'\\b\\w+\\b', text.lower())
    return {
        'word_count': len(words),
        'unique_words': len(set(words)),
        'most_common': Counter(words).most_common(5)
    }

if __name__ == '__main__':
    text = "MIRAI is an autonomous AI agent. MIRAI can code in many languages."
    result = analyze_text(text)
    print("📊 NLP Analysis:", result)
"""
        )
        print("✅ NLP пример создан")
        
    elif 'D' in decision.upper() or 'НОВЫЙ' in decision.upper():
        print(f"\n🤖 {kaizen.name}: МИРАЙ, какой проект создать?")
        
        project_idea = kaizen.ask_mirai("""
Предложи идею нового практичного проекта.
Опиши в 2 предложениях что и зачем.
""")
        
        print(f"💬 МИРАЙ: {project_idea}")
        
    elif 'E' in decision.upper() or 'УЛУЧШ' in decision.upper():
        print(f"\n🤖 {kaizen.name}: Улучшаем код...")
        
        # Анализируем и улучшаем autonomous_agent.py
        improvements = kaizen.ask_mirai("""
Проанализируй файл autonomous_agent.py.
Какие 3 главных улучшения нужны?
Коротко, по делу.
""")
        
        print(f"💬 МИРАЙ предлагает: {improvements}")
    
    print(f"\n✅ Работа выполнена автономно.")


if __name__ == '__main__':
    main()
