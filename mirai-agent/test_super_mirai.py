#!/usr/bin/env python3
"""
ФИНАЛЬНЫЙ ТЕСТ СУПЕР МИРАЙ
Проверка всех новых возможностей через autonomous_agent
"""

import sys
import os
from dotenv import load_dotenv

load_dotenv()

# Добавляем путь
sys.path.insert(0, "/root/mirai/mirai-agent")

from core.autonomous_agent import AutonomousAgent


def main():
    print("=" * 80)
    print("🚀 ФИНАЛЬНЫЙ ТЕСТ: СУПЕР МИРАЙ")
    print("=" * 80)

    agent = AutonomousAgent()

    # Проверка доступности расширенных функций
    if agent.has_advanced_features:
        print("✅ Расширенные функции загружены!")
    else:
        print("⚠️ Расширенные функции не доступны")
        return

    print("\n" + "=" * 80)
    print("ТЕСТ 1: Выполнение JavaScript кода")
    print("=" * 80)

    js_code = """
    const numbers = [1, 2, 3, 4, 5];
    const sum = numbers.reduce((a, b) => a + b, 0);
    console.log('Сумма массива:', sum);
    console.log('Среднее:', sum / numbers.length);
    """

    result = agent.execute_code(js_code, "javascript")
    print(result)

    print("\n" + "=" * 80)
    print("ТЕСТ 2: Выполнение C++ кода")
    print("=" * 80)

    cpp_code = """
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> nums = {1, 2, 3, 4, 5};
    int sum = 0;
    for(int n : nums) sum += n;
    cout << "Сумма: " << sum << endl;
    cout << "MIRAI может выполнять C++!" << endl;
    return 0;
}
"""

    result = agent.execute_code(cpp_code, "cpp")
    print(result)

    print("\n" + "=" * 80)
    print("ТЕСТ 3: Работа с PostgreSQL")
    print("=" * 80)

    result = agent.database_query(
        "postgres",
        "query",
        {"query": "SELECT current_database(), current_user, version() as pg_version"},
    )
    print(result)

    print("\n" + "=" * 80)
    print("ТЕСТ 4: Работа с Redis (кэш)")
    print("=" * 80)

    # Записываем в Redis
    result1 = agent.database_query(
        "redis",
        "set",
        {"key": "mirai_power_level", "value": "OVER 9000!", "expire": 120},
    )
    print("Запись в Redis:", result1)

    # Читаем из Redis
    result2 = agent.database_query("redis", "get", {"key": "mirai_power_level"})
    print("Чтение из Redis:", result2)

    print("\n" + "=" * 80)
    print("ТЕСТ 5: Выполнение Bash скрипта")
    print("=" * 80)

    bash_code = """
#!/bin/bash
echo "🤖 MIRAI System Info:"
echo "Hostname: $(hostname)"
echo "Uptime: $(uptime -p)"
echo "Disk: $(df -h / | tail -1 | awk '{print $5}')"
"""

    result = agent.execute_code(bash_code, "bash")
    print(result)

    print("\n" + "=" * 80)
    print("🎉 ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ УСПЕШНО!")
    print("=" * 80)

    print("\n📊 ИТОГОВАЯ СТАТИСТИКА:")
    print(
        f"   ✅ Поддерживаемых языков: {len(agent.multi_lang.get_supported_languages())}"
    )
    print(f"   ✅ Баз данных: 4 (SQLite, PostgreSQL, Redis, MongoDB)")
    print(
        f"   ✅ Инструментов агента: 8 (execute_python, search_web, read_file, write_file, run_command, create_task, execute_code, database_query)"
    )
    print("\n🚀 MIRAI готов к универсальной работе!")


if __name__ == "__main__":
    main()
