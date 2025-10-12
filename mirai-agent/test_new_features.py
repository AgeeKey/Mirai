#!/usr/bin/env python3
"""
Тест новых возможностей MIRAI
- Многоязыковое выполнение кода
- Работа с базами данных
"""

import asyncio
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, '/root/mirai/mirai-agent')

from core.multi_language_executor import MultiLanguageExecutor
from core.database_manager import DatabaseManager


async def test_languages():
    """Тест выполнения кода на разных языках"""
    print("=" * 70)
    print("🚀 ТЕСТ МНОГОЯЗЫКОВОГО ВЫПОЛНЕНИЯ КОДА")
    print("=" * 70)
    
    executor = MultiLanguageExecutor()
    
    tests = [
        {
            'name': 'Python',
            'code': 'print("Hello from Python!")\nprint(2 + 2)',
            'language': 'python'
        },
        {
            'name': 'JavaScript (Node.js)',
            'code': 'console.log("Hello from JavaScript!");\nconsole.log(2 + 2);',
            'language': 'javascript'
        },
        {
            'name': 'C++',
            'code': '''#include <iostream>
using namespace std;
int main() {
    cout << "Hello from C++!" << endl;
    cout << 2 + 2 << endl;
    return 0;
}''',
            'language': 'cpp'
        },
        {
            'name': 'Bash',
            'code': '''echo "Hello from Bash!"
expr 2 + 2''',
            'language': 'bash'
        },
    ]
    
    for test in tests:
        print(f"\n{'='*70}")
        print(f"📝 Тестируем: {test['name']}")
        print(f"{'='*70}")
        
        result = await executor.execute_code(test['code'], test['language'])
        
        if result['success']:
            print(f"✅ Успех! ({result['execution_time']}s)")
            print(f"Вывод:\n{result['output']}")
        else:
            print(f"❌ Ошибка:")
            print(result['error'])
    
    print(f"\n{'='*70}")
    print(f"✅ Поддерживаемые языки: {', '.join(executor.get_supported_languages())}")
    print(f"{'='*70}")


async def test_databases():
    """Тест работы с базами данных"""
    print("\n\n" + "=" * 70)
    print("🗄️ ТЕСТ РАБОТЫ С БАЗАМИ ДАННЫХ")
    print("=" * 70)
    
    db = DatabaseManager()
    
    # Тест SQLite
    print("\n📦 SQLite:")
    result = await db.sqlite_query("SELECT datetime('now') as current_time, 'MIRAI' as agent")
    print(f"   Результат: {result}")
    
    # Тест Redis
    print("\n🔴 Redis:")
    await db.redis_set('mirai_test', 'Hello from MIRAI!', expire=60)
    value = await db.redis_get('mirai_test')
    print(f"   Установлено: 'mirai_test' = 'Hello from MIRAI!'")
    print(f"   Получено: {value}")
    
    # Тест PostgreSQL
    print("\n🐘 PostgreSQL:")
    result = await db.postgres_query("SELECT version()")
    if 'error' not in result[0]:
        print(f"   ✅ Подключено! Версия: {result[0].get('version', 'unknown')[:50]}...")
    else:
        print(f"   ⚠️ {result[0]['error']}")
    
    # Тест MongoDB
    print("\n🍃 MongoDB:")
    result = await db.mongodb_insert('test', {'message': 'Hello from MIRAI!', 'timestamp': 'now'})
    if 'error' not in result:
        print(f"   ✅ Документ вставлен: ID={result.get('inserted_id')}")
        
        # Найдем его обратно
        docs = await db.mongodb_find('test', {'message': 'Hello from MIRAI!'}, limit=1)
        if docs and 'error' not in docs[0]:
            print(f"   ✅ Документ найден: {docs[0]}")
        else:
            print(f"   ⚠️ Документ не найден")
    else:
        print(f"   ⚠️ {result['error']}")
    
    # Общая информация
    print(f"\n{'='*70}")
    print("📊 СТАТУС ВСЕХ БАЗ ДАННЫХ:")
    print(f"{'='*70}")
    info = await db.get_database_info()
    for db_name, status in info.items():
        status_icon = "✅" if status['status'] == 'connected' else "❌"
        print(f"{status_icon} {db_name.upper()}: {status['status']} - {status['details']}")
    print(f"{'='*70}")


async def main():
    """Главная функция"""
    try:
        # Тест языков программирования
        await test_languages()
        
        # Тест баз данных
        await test_databases()
        
        print("\n\n" + "=" * 70)
        print("🎉 ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ Ошибка при выполнении тестов: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    asyncio.run(main())
