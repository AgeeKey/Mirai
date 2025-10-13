#!/usr/bin/env python3
"""
МИРАЙ САМА РЕШАЕТ ЧТО ЕЙ НУЖНО
Автономный анализ возможностей и планирование улучшений
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

sys.path.insert(0, "/root/mirai/mirai-agent")
os.environ["PATH"] = f"{os.path.expanduser('~')}/.cargo/bin:" + os.environ["PATH"]

from core.autonomous_agent import AutonomousAgent


def main():
    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        # Если есть аргументы - используем их как вопрос
        user_question = " ".join(sys.argv[1:])

        print("=" * 80)
        print("🤖 МИРАЙ: ОТВЕТ НА ВОПРОС")
        print("=" * 80)
        print(f"\n❓ Вопрос: {user_question}\n")

        agent = AutonomousAgent()

        print("🤔 МИРАЙ думает...\n")
        response = agent.think(user_question, max_iterations=3)

        print("\n" + "=" * 80)
        print("💬 ОТВЕТ МИРАЙ:")
        print("=" * 80)
        print(response)
        print("\n" + "=" * 80)
        return

    # Если аргументов нет - используем стандартный режим анализа
    print("=" * 80)
    print("🤖 МИРАЙ: САМОАНАЛИЗ И ПЛАНИРОВАНИЕ")
    print("=" * 80)

    agent = AutonomousAgent()

    # Проверка возможностей
    print("\n📊 Текущие возможности МИРАЙ:")
    print("-" * 80)

    if agent.has_advanced_features:
        print("✅ Расширенные функции: Активны")
        print(f"✅ Языки программирования: 8 (Python, JS, TS, C, C++, Go, Rust, Bash)")
        print(f"✅ Базы данных: 4 (SQLite, PostgreSQL, Redis, MongoDB)")
        print(f"✅ ML библиотеки: PyTorch, scikit-learn, pandas")
        print(f"✅ Инструментов: 8")
    else:
        print("⚠️ Расширенные функции: Не загружены")

    print("\n" + "=" * 80)
    print("🧠 МИРАЙ, ЧТО ТЫ ХОЧЕШЬ? ЧТО ТЕБЕ НУЖНО ДЛЯ РАБОТЫ?")
    print("=" * 80)

    # МИРАЙ сама анализирует что ей нужно
    prompt = """
Ты МИРАЙ - автономный AI агент.

Проанализируй свои возможности и ответь на вопросы:

1. ЧТО ТЕБЕ НУЖНО ДЛЯ РАБОТЫ?
   - GitHub API (для работы с репозиториями)?
   - MongoDB (или PostgreSQL достаточно)?
   - AWS/GCP SDK (для облачных сервисов)?
   - Что-то ещё?

2. КАКИЕ ЗАДАЧИ ТЫ МОЖЕШЬ РЕШАТЬ ПРЯМО СЕЙЧАС?
   - Разработка (какие языки и фреймворки)
   - Анализ данных (какие инструменты)
   - Автоматизация (какие сценарии)
   - Другое

3. ЧТО БЫ ТЫ ХОТЕЛА УМЕТЬ ДОПОЛНИТЕЛЬНО?
   - Какие инструменты добавить
   - Какие интеграции настроить
   - Какие возможности расширить

4. ТВОЯ РЕКОМЕНДАЦИЯ:
   - Что КРИТИЧНО для работы
   - Что ЖЕЛАТЕЛЬНО
   - Что ОПЦИОНАЛЬНО

Будь конкретной и практичной. Думай как инженер.

Твой анализ:
"""

    print("\n🤔 МИРАЙ думает...\n")

    # МИРАЙ отвечает
    response = agent.think(prompt, max_iterations=3)

    print("\n" + "=" * 80)
    print("💬 ОТВЕТ МИРАЙ:")
    print("=" * 80)
    print(response)
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
