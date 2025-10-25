#!/usr/bin/env python3
"""
🎯 ДЕМОНСТРАЦИЯ: Реальная автоматизация браузера в MIRAI
========================================================

Этот скрипт демонстрирует НОВЫЕ возможности MIRAI:
1. ✅ Реальный поиск и анализ веб-страниц (WebScraperAgent)
2. ✅ Автоматизация браузера через Selenium (опционально)
3. ✅ Умное извлечение поисковых запросов

Автор: MIRAI Team
Дата: 2025-10-25
"""

import asyncio
import sys
from pathlib import Path

# Добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent / "core"))

from web_scraper_agent import WebScraperAgent


async def demo_query_extraction():
    """Демонстрация умного извлечения запросов"""
    print("\n" + "="*70)
    print("📝 ДЕМОНСТРАЦИЯ 1: Умное извлечение поисковых запросов")
    print("="*70)
    
    agent = WebScraperAgent()
    
    # ПРИМЕЧАНИЕ: Опечатки в запросах НАМЕРЕННЫЕ!
    # Демонстрируем что система исправляет их автоматически
    test_queries = [
        "открый браузер и поищи иформатцию прос бинанс и расскажми мне что это за платформа",  # Много опечаток
        "найди информацию про Python программирование и объясни",
        "поищи что такое криптовалюта",
        "загугли React JS и расскажи мне что это",
    ]
    
    print("\n🔍 Тестовые запросы (с намеренными опечатками):\n")
    for query in test_queries:
        clean_query = agent.extract_search_query(query)
        print(f"📥 Исходный запрос:")
        print(f"   \"{query}\"")
        print(f"✨ Извлечённый запрос:")
        print(f"   \"{clean_query}\"")
        print()
    
    agent.close()
    print("✅ Демонстрация 1 завершена")


async def demo_web_scraping():
    """Демонстрация реального поиска и парсинга"""
    print("\n" + "="*70)
    print("🌐 ДЕМОНСТРАЦИЯ 2: Реальный поиск в Google и парсинг сайтов")
    print("="*70)
    
    agent = WebScraperAgent()
    
    # Простой поиск без AI анализа (для демонстрации)
    query = "Python programming language"
    print(f"\n🔍 Ищем: {query}")
    print("⏳ Выполняется поиск...")
    
    result = await agent.search_and_analyze(
        query,
        num_results=2,  # Загружаем только 2 сайта для скорости
        analyze=False   # Отключаем AI анализ для демонстрации
    )
    
    if result['success']:
        print(f"\n✅ Поиск выполнен успешно!")
        print(f"📊 Статистика:")
        print(f"   • Найдено результатов: {result['summary']['total_results']}")
        print(f"   • Загружено сайтов: {result['summary']['scraped_pages']}")
        
        print(f"\n📋 Найденные результаты (топ-5):")
        for i, res in enumerate(result['search_results'][:5], 1):
            print(f"\n{i}. {res['title']}")
            print(f"   🔗 {res['url']}")
            if res.get('snippet'):
                snippet = res['snippet'][:100] + "..." if len(res['snippet']) > 100 else res['snippet']
                print(f"   📝 {snippet}")
        
        if result['scraped_content']:
            print(f"\n📄 Загруженный контент:")
            for i, content in enumerate(result['scraped_content'], 1):
                print(f"\n{i}. {content['title']}")
                print(f"   📊 Извлечено символов: {len(content['content'])}")
                preview = content['content'][:200].replace('\n', ' ')
                print(f"   📝 Превью: {preview}...")
    else:
        print(f"❌ Ошибка: {result.get('error')}")
    
    agent.close()
    print("\n✅ Демонстрация 2 завершена")


async def demo_selenium_automation():
    """Демонстрация автоматизации через Selenium (опционально)"""
    print("\n" + "="*70)
    print("🤖 ДЕМОНСТРАЦИЯ 3: Автоматизация браузера через Selenium")
    print("="*70)
    
    try:
        from selenium_browser_agent import SeleniumBrowserAgent, SELENIUM_AVAILABLE
        
        if not SELENIUM_AVAILABLE:
            print("\n⚠️ Selenium не установлен.")
            print("📦 Для использования установите: pip install selenium")
            print("💡 WebScraperAgent работает и без Selenium!")
            return
        
        print("\n🚀 Запуск браузера...")
        print("⚠️ ВНИМАНИЕ: Браузер откроется на 10 секунд, затем закроется")
        
        agent = SeleniumBrowserAgent(headless=False)
        await agent.initialize()
        
        print("✅ Браузер запущен!")
        
        # Выполняем поиск
        query = "Python"
        print(f"\n🔍 Поиск в Google: {query}")
        result = await agent.search_google(query)
        
        if result['success']:
            print(f"✅ Найдено результатов: {result['count']}")
            print(f"\n📋 Топ-3 результата:")
            for i, res in enumerate(result['results'][:3], 1):
                print(f"\n{i}. {res['title']}")
                print(f"   {res['url']}")
        
        # Скриншот
        print("\n📸 Создаём скриншот страницы поиска...")
        screenshot = await agent.take_screenshot("demo_search.png")
        if screenshot:
            print(f"✅ Скриншот сохранён: {screenshot}")
        
        # Ждём немного чтобы пользователь увидел
        print("\n⏳ Браузер останется открытым 10 секунд...")
        await asyncio.sleep(10)
        
        # Закрываем
        await agent.close()
        print("✅ Браузер закрыт")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
    
    print("\n✅ Демонстрация 3 завершена")


async def main():
    """Главная функция"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*15 + "🎯 ДЕМОНСТРАЦИЯ НОВЫХ ВОЗМОЖНОСТЕЙ MIRAI" + " "*14 + "║")
    print("╚" + "="*68 + "╝")
    
    print("\n🌐 Демонстрируем РЕАЛЬНУЮ автоматизацию браузера:")
    print("   ✅ Поиск в Google")
    print("   ✅ Чтение веб-страниц")
    print("   ✅ Извлечение данных")
    print("   ✅ AI анализ (опционально)")
    print("   ✅ Selenium автоматизация (опционально)")
    
    # Запускаем демонстрации
    await demo_query_extraction()
    await demo_web_scraping()
    
    # Спрашиваем про Selenium
    print("\n" + "="*70)
    response = input("\n❓ Хотите запустить демонстрацию Selenium? (браузер откроется) [y/N]: ")
    if response.lower() in ['y', 'yes', 'да', 'д']:
        await demo_selenium_automation()
    else:
        print("⏭️ Пропускаем Selenium демонстрацию")
    
    print("\n" + "="*70)
    print("🎉 ВСЕ ДЕМОНСТРАЦИИ ЗАВЕРШЕНЫ!")
    print("="*70)
    
    print("\n📝 Что было продемонстрировано:")
    print("   ✅ Умное извлечение поисковых запросов из команд")
    print("   ✅ Реальный поиск в Google с парсингом HTML")
    print("   ✅ Загрузка и чтение веб-страниц")
    print("   ✅ Извлечение чистого текста из HTML")
    if response.lower() in ['y', 'yes', 'да', 'д']:
        print("   ✅ Автоматизация браузера через Selenium")
        print("   ✅ Создание скриншотов")
    
    print("\n💡 Теперь MIRAI - это НАСТОЯЩИЙ AI агент, который:")
    print("   • НЕ просто открывает браузер")
    print("   • РЕАЛЬНО читает и анализирует веб-страницы")
    print("   • Извлекает информацию из интернета")
    print("   • Может отвечать на вопросы о найденной информации")
    
    print("\n🚀 Готово к использованию в unified_mirai.py!")
    print("   Инструмент: search_and_analyze_web")
    print("   Инструмент: automate_browser (если Selenium установлен)")
    print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Прервано пользователем")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
