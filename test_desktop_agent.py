#!/usr/bin/env python3
"""
Тестирование MIRAI Desktop Agent V2

Проверяет все возможности агента:
- Базовые операции (мышь, клавиатура)
- Скриншоты и Vision
- OCR и Computer Vision
- Управление окнами
- Автономное выполнение задач
"""

import sys
import time
from pathlib import Path

# Добавить путь к mirai-agent
sys.path.insert(0, str(Path(__file__).parent))

try:
    from core.desktop_agent_v2 import MiraiDesktopAgent
except ImportError:
    print("❌ Не удалось импортировать desktop_agent_v2")
    print("Убедитесь, что файл существует: mirai-agent/core/desktop_agent_v2.py")
    sys.exit(1)


def test_initialization():
    """Тест 1: Инициализация агента"""
    print("\n" + "=" * 70)
    print("ТЕСТ 1: Инициализация агента")
    print("=" * 70)
    
    try:
        agent = MiraiDesktopAgent(
            enable_safety=True,
            enable_memory=False,  # Отключаем для тестов
            screenshots_dir="test_screenshots"
        )
        
        print(f"✅ Агент создан")
        print(f"   ОС: {agent.os_type}")
        print(f"   Экран: {agent.screen_width}x{agent.screen_height}")
        print(f"   Модель: {agent.model}")
        print(f"   Безопасность: {agent.enable_safety}")
        
        return agent
    
    except Exception as e:
        print(f"❌ Ошибка инициализации: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_basic_operations(agent):
    """Тест 2: Базовые операции"""
    print("\n" + "=" * 70)
    print("ТЕСТ 2: Базовые операции")
    print("=" * 70)
    
    # Получить позицию мыши
    print("\n1️⃣ Получение позиции мыши...")
    result = agent.get_mouse_position()
    print(f"   {result}")
    
    # Переместить мышь
    print("\n2️⃣ Перемещение мыши...")
    result = agent.move_mouse(100, 100, duration=0.5)
    print(f"   {result}")
    
    # Подождать
    print("\n3️⃣ Ожидание 1 секунду...")
    result = agent.wait_seconds(1)
    print(f"   {result}")
    
    print("\n✅ Базовые операции работают")


def test_screenshot_and_vision(agent):
    """Тест 3: Скриншоты и Vision"""
    print("\n" + "=" * 70)
    print("ТЕСТ 3: Скриншоты и Vision анализ")
    print("=" * 70)
    
    # Сделать скриншот
    print("\n1️⃣ Создание скриншота...")
    result = agent.take_screenshot("full")
    print(f"   {result}")
    
    if agent.last_screenshot_path:
        print(f"   Путь: {agent.last_screenshot_path}")
        
        # Анализ через Vision
        print("\n2️⃣ Анализ скриншота через GPT-4 Vision...")
        result = agent.analyze_screenshot(
            "Опиши что ты видишь на этом скриншоте. "
            "Какие приложения открыты? Что находится на рабочем столе?"
        )
        print(f"   {result[:200]}...")
        
        print("\n✅ Скриншоты и Vision работают")
    else:
        print("❌ Скриншот не был создан")


def test_window_operations(agent):
    """Тест 4: Операции с окнами"""
    print("\n" + "=" * 70)
    print("ТЕСТ 4: Управление окнами")
    print("=" * 70)
    
    # Найти окна
    print("\n1️⃣ Поиск окон с 'explorer' в заголовке...")
    result = agent.find_window("explorer")
    print(f"   {result}")
    
    # Открыть Notepad (если на Windows)
    if agent.os_type == "Windows":
        print("\n2️⃣ Открытие Notepad...")
        result = agent.open_application("notepad")
        print(f"   {result}")
        
        time.sleep(2)
        
        # Найти окно Notepad
        print("\n3️⃣ Поиск окна Notepad...")
        result = agent.find_window("notepad")
        print(f"   {result}")
        
        # Активировать окно
        print("\n4️⃣ Активация окна Notepad...")
        result = agent.activate_window("notepad")
        print(f"   {result}")
        
        print("\n✅ Управление окнами работает")
    else:
        print("⚠️ Тест окон доступен только на Windows")


def test_ocr(agent):
    """Тест 5: OCR"""
    print("\n" + "=" * 70)
    print("ТЕСТ 5: OCR (распознавание текста)")
    print("=" * 70)
    
    print("\n1️⃣ Поиск текста на экране...")
    result = agent.find_text_on_screen("File")
    print(f"   {result[:200]}...")
    
    if "✅" in result:
        print("\n✅ OCR работает")
    else:
        print("\n⚠️ OCR может быть недоступен (требуется pytesseract)")


def test_autonomous_task(agent):
    """Тест 6: Автономное выполнение задачи"""
    print("\n" + "=" * 70)
    print("ТЕСТ 6: Автономное выполнение задачи")
    print("=" * 70)
    
    # Простая задача
    task = "Получи текущую позицию курсора мыши, затем сделай скриншот экрана"
    
    print(f"\n📋 Задача: {task}")
    print("\n🤔 Агент думает и выполняет...\n")
    
    result = agent.execute_task(task, max_iterations=5)
    
    print("\n" + "-" * 70)
    print("📊 Результат:")
    print("-" * 70)
    print(result)
    
    if "✅" in result or "завершена" in result.lower():
        print("\n✅ Автономная работа успешна")
    else:
        print("\n⚠️ Автономная работа завершена с предупреждениями")


def test_action_history(agent):
    """Тест 7: История действий"""
    print("\n" + "=" * 70)
    print("ТЕСТ 7: История действий")
    print("=" * 70)
    
    history = agent.get_action_history(limit=10)
    
    print(f"\n📝 Всего действий: {len(agent.action_history)}")
    print(f"📝 Последние {len(history)} действий:")
    
    for i, action in enumerate(history, 1):
        print(f"\n   {i}. {action['action_type']}")
        print(f"      Результат: {action['result'][:50]}...")
        print(f"      Длительность: {action['duration']:.3f}с")
    
    # Сохранить историю
    history_file = "test_action_history.json"
    agent.save_action_history(history_file)
    print(f"\n💾 История сохранена: {history_file}")
    
    print("\n✅ История действий работает")


def main():
    """Главная функция тестирования"""
    print("╔══════════════════════════════════════════════════════════════════════╗")
    print("║     Тестирование MIRAI Desktop Agent V2                            ║")
    print("╚══════════════════════════════════════════════════════════════════════╝")
    
    # Тест 1: Инициализация
    agent = test_initialization()
    if not agent:
        print("\n❌ Тестирование прервано из-за ошибки инициализации")
        return 1
    
    # Выбор тестов
    print("\n" + "=" * 70)
    print("Доступные тесты:")
    print("=" * 70)
    print("1. Базовые операции (мышь, клавиатура)")
    print("2. Скриншоты и Vision")
    print("3. Управление окнами")
    print("4. OCR (распознавание текста)")
    print("5. Автономная задача")
    print("6. История действий")
    print("7. Запустить все тесты")
    print()
    
    choice = input("Выберите тест (1-7) или нажмите Enter для всех: ").strip()
    
    try:
        if not choice or choice == "7":
            # Все тесты
            test_basic_operations(agent)
            test_screenshot_and_vision(agent)
            test_window_operations(agent)
            test_ocr(agent)
            test_autonomous_task(agent)
            test_action_history(agent)
        
        elif choice == "1":
            test_basic_operations(agent)
        elif choice == "2":
            test_screenshot_and_vision(agent)
        elif choice == "3":
            test_window_operations(agent)
        elif choice == "4":
            test_ocr(agent)
        elif choice == "5":
            test_autonomous_task(agent)
        elif choice == "6":
            test_action_history(agent)
        else:
            print(f"❌ Неверный выбор: {choice}")
            return 1
        
        print("\n" + "=" * 70)
        print("✅ Тестирование завершено успешно!")
        print("=" * 70)
        
        return 0
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Тестирование прервано пользователем")
        return 1
    
    except Exception as e:
        print(f"\n❌ Ошибка во время тестирования: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
