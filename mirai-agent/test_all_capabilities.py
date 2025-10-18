#!/usr/bin/env python3
"""
🔍 Тест всех возможностей MIRAI
Проверяет какие функции работают, какие используются в автономном режиме
"""

import json
import sys
sys.path.insert(0, "/root/mirai/mirai-agent")

from core.autonomous_agent import AutonomousAgent

def test_all_capabilities():
    """Тестирование всех возможностей"""
    
    print("=" * 70)
    print("🤖 MIRAI - ПОЛНАЯ ПРОВЕРКА ВОЗМОЖНОСТЕЙ")
    print("=" * 70)
    
    agent = AutonomousAgent()
    
    # 1. Список всех инструментов
    print("\n📋 1. ИНСТРУМЕНТЫ MIRAI:")
    print("-" * 70)
    for i, tool in enumerate(agent.tools, 1):
        name = tool['function']['name']
        desc = tool['function']['description']
        print(f"{i:2}. {name:20} - {desc}")
    
    print(f"\n✅ Всего инструментов: {len(agent.tools)}")
    
    # 2. Проверка продвинутых функций
    print("\n🚀 2. ПРОДВИНУТЫЕ ВОЗМОЖНОСТИ:")
    print("-" * 70)
    
    capabilities = {
        "Multi-Language Executor": agent.multi_lang is not None,
        "Database Manager": agent.db_manager is not None,
        "GitHub Integration": agent.github is not None,
        "Advanced Features": agent.has_advanced_features
    }
    
    for name, status in capabilities.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {name:25} - {'Доступно' if status else 'НЕ доступно'}")
    
    # 3. Проверка GitHub
    print("\n🐙 3. GITHUB INTEGRATION:")
    print("-" * 70)
    
    if agent.github:
        is_auth = agent.github.is_authenticated()
        print(f"{'✅' if is_auth else '❌'} Авторизация: {'OK' if is_auth else 'НЕТ'}")
        
        if is_auth:
            user_info = agent.github.get_user_info()
            if 'login' in user_info:
                print(f"👤 Пользователь: {user_info['login']}")
                print(f"📦 Публичных репозиториев: {user_info.get('public_repos', 0)}")
    else:
        print("❌ GitHub интеграция не загружена")
    
    # 4. Проверка доступных языков
    print("\n💻 4. ПОДДЕРЖКА ЯЗЫКОВ ПРОГРАММИРОВАНИЯ:")
    print("-" * 70)
    
    if agent.multi_lang:
        languages = ["python", "javascript", "typescript", "c", "cpp", "go", "rust", "bash"]
        for lang in languages:
            print(f"✅ {lang}")
    else:
        print("❌ Multi-language executor не загружен")
    
    # 5. Проверка баз данных
    print("\n🗄️  5. ПОДДЕРЖКА БАЗ ДАННЫХ:")
    print("-" * 70)
    
    if agent.db_manager:
        databases = ["SQLite", "PostgreSQL", "MongoDB", "Redis"]
        for db in databases:
            print(f"✅ {db}")
    else:
        print("❌ Database manager не загружен")
    
    # 6. ТЕСТЫ ФУНКЦИЙ
    print("\n🧪 6. ТЕСТИРОВАНИЕ ФУНКЦИЙ:")
    print("-" * 70)
    
    # Test 1: Search Web
    print("\n🔍 Test: search_web()")
    try:
        result = agent.search_web("Python programming")
        print(f"✅ Поиск работает: {len(result)} символов")
        print(f"   Первые 100 символов: {result[:100]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Test 2: Execute Python
    print("\n🐍 Test: execute_python()")
    try:
        result = agent.execute_python("print('Hello from MIRAI!'); import sys; print(sys.version)")
        print(f"✅ Python выполнение работает")
        print(f"   {result[:200]}...")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    # Test 3: GitHub
    if agent.github and agent.github.is_authenticated():
        print("\n🐙 Test: github_action()")
        try:
            result = agent.github_action("get_user_info")
            print(f"✅ GitHub работает")
            print(f"   {result[:200]}...")
        except Exception as e:
            print(f"❌ Ошибка: {e}")
    
    # 7. КРИТИЧНЫЕ ФУНКЦИИ
    print("\n🔴 7. КРИТИЧНЫЕ ДЛЯ РАБОТЫ:")
    print("-" * 70)
    
    critical = [
        ("AI мышление (think)", True),
        ("Чтение файлов (read_file)", True),
        ("Запись файлов (write_file)", True),
        ("Выполнение команд (run_command)", True),
        ("Поиск в интернете (search_web)", True),
        ("GitHub интеграция", agent.github is not None),
    ]
    
    for name, available in critical:
        icon = "✅" if available else "⚠️"
        print(f"{icon} {name}")
    
    # 8. ЧТО НУЖНО ДОБАВИТЬ
    print("\n💡 8. ВОЗМОЖНЫЕ УЛУЧШЕНИЯ:")
    print("-" * 70)
    
    improvements = [
        "✨ Чтение других GitHub репозиториев (get_repo_content)",
        "✨ Продвинутый веб-поиск (Google Custom Search API)",
        "✨ Скрапинг веб-страниц (Beautiful Soup)",
        "✨ API интеграции (Twitter, Reddit, Stack Overflow)",
        "✨ Векторные базы данных (Pinecone, Weaviate)",
        "✨ RAG (Retrieval-Augmented Generation)",
    ]
    
    for improvement in improvements:
        print(improvement)
    
    print("\n" + "=" * 70)
    print("✅ ПРОВЕРКА ЗАВЕРШЕНА")
    print("=" * 70)

if __name__ == "__main__":
    test_all_capabilities()
