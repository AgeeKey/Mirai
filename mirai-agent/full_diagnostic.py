#!/usr/bin/env python3
"""
🔍 ПОЛНАЯ ДИАГНОСТИКА MIRAI
===========================

Проверяет ВСЕ системы и выдаёт детальный отчёт о реальной работе
"""

import os
import sys
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
import subprocess

print("🔍 ПОЛНАЯ ДИАГНОСТИКА MIRAI")
print("=" * 70)
print()

# === 1. СТАТУС СЛУЖБЫ ===
print("1️⃣ СТАТУС СЛУЖБЫ MIRAI:")
result = subprocess.run(['systemctl', 'is-active', 'mirai'], capture_output=True, text=True)
status = result.stdout.strip()
if status == 'active':
    print(f"   ✅ Служба работает: {status}")
else:
    print(f"   ❌ Служба НЕ работает: {status}")

# Uptime
result = subprocess.run(['systemctl', 'show', 'mirai', '--property=ActiveEnterTimestamp'], capture_output=True, text=True)
if result.returncode == 0:
    timestamp = result.stdout.split('=')[1].strip()
    print(f"   ⏰ Работает с: {timestamp}")

# Memory
result = subprocess.run(['systemctl', 'show', 'mirai', '--property=MemoryCurrent'], capture_output=True, text=True)
if result.returncode == 0:
    memory_bytes = int(result.stdout.split('=')[1].strip())
    memory_mb = memory_bytes / 1024 / 1024
    print(f"   💾 Память: {memory_mb:.1f} MB")

print()

# === 2. БАЗЫ ДАННЫХ ===
print("2️⃣ БАЗЫ ДАННЫХ:")

data_dir = Path("/root/mirai/mirai-agent/data")

# mirai_memory.db
db_path = data_dir / "mirai_memory.db"
if db_path.exists():
    size = db_path.stat().st_size / 1024
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sessions")
    sessions = cursor.fetchone()[0]
    conn.close()
    print(f"   ✅ mirai_memory.db: {size:.1f} KB, {sessions} сессий")
else:
    print(f"   ❌ mirai_memory.db: НЕ НАЙДЕНА")

# long_term_memory.db
db_path = data_dir / "long_term_memory.db"
if db_path.exists():
    size = db_path.stat().st_size / 1024
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT COUNT(*) FROM goals WHERE status = 'active'")
        goals = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM achievements")
        achievements = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM decisions")
        decisions = cursor.fetchone()[0]
        print(f"   ✅ long_term_memory.db: {size:.1f} KB")
        print(f"      • Целей: {goals}")
        print(f"      • Достижений: {achievements}")
        print(f"      • Решений: {decisions}")
    except sqlite3.OperationalError as e:
        print(f"   ⚠️ long_term_memory.db: {size:.1f} KB (структура устарела)")
        print(f"      Ошибка: {e}")
    
    conn.close()
else:
    print(f"   ❌ long_term_memory.db: НЕ НАЙДЕНА")

# personality.db
db_path = data_dir / "personality.db"
if db_path.exists():
    size = db_path.stat().st_size / 1024
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("SELECT overall_level, total_xp FROM overall_progress WHERE id = 1")
    row = cursor.fetchone()
    if row:
        level, xp = row
        print(f"   ✅ personality.db: {size:.1f} KB")
        print(f"      • Уровень MIRAI: {level}")
        print(f"      • Общий XP: {xp:.0f}")
        
        cursor.execute("SELECT COUNT(*) FROM skills")
        skills = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM titles")
        titles = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM traits")
        traits = cursor.fetchone()[0]
        
        print(f"      • Навыков: {skills}")
        print(f"      • Титулов: {titles}")
        print(f"      • Черт: {traits}")
    
    conn.close()
else:
    print(f"   ❌ personality.db: НЕ НАЙДЕНА")

print()

# === 3. ЛОГИ И ОШИБКИ ===
print("3️⃣ АНАЛИЗ ЛОГОВ (последние 24 часа):")

# Подсчёт ошибок
result = subprocess.run(
    ['journalctl', '-u', 'mirai', '--since', '24 hours ago', '--no-pager'],
    capture_output=True, text=True
)
logs = result.stdout

error_count = logs.count('[ERROR]')
warning_count = logs.count('[WARNING]')
info_count = logs.count('[INFO]')

print(f"   📊 Всего строк: {len(logs.splitlines())}")
print(f"   ❌ Ошибок (ERROR): {error_count}")
print(f"   ⚠️  Предупреждений (WARNING): {warning_count}")
print(f"   ℹ️  Информации (INFO): {info_count}")

# Ищем частые ошибки
print("\n   🔍 Критические ошибки:")
errors = []
for line in logs.splitlines():
    if '[ERROR]' in line or 'Traceback' in line or 'Exception' in line:
        errors.append(line)

if errors:
    # Показываем уникальные ошибки
    unique_errors = {}
    for error in errors:
        # Извлекаем суть ошибки
        if 'ERROR]' in error:
            msg = error.split('[ERROR]')[1].strip()[:80]
            unique_errors[msg] = unique_errors.get(msg, 0) + 1
    
    for msg, count in sorted(unique_errors.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"      [{count}x] {msg}")
else:
    print(f"      ✅ Нет критических ошибок!")

print()

# === 4. ПРОВЕРКА МОДУЛЕЙ ===
print("4️⃣ ПРОВЕРКА МОДУЛЕЙ:")

modules = [
    ('core.long_term_memory', 'LongTermMemory'),
    ('core.self_awareness', 'SelfAwareness'),
    ('core.auto_planner', 'AutoPlanner'),
    ('core.self_modification', 'SelfModification'),
    ('core.personality_system', 'PersonalitySystem'),
    ('core.github_integration', 'GitHubIntegration'),
]

sys.path.insert(0, '/root/mirai/mirai-agent')

for module_name, class_name in modules:
    try:
        module = __import__(module_name, fromlist=[class_name])
        cls = getattr(module, class_name)
        print(f"   ✅ {class_name}: импорт OK")
    except Exception as e:
        print(f"   ❌ {class_name}: ОШИБКА - {e}")

print()

# === 5. ПРОВЕРКА МЕТОДОВ ===
print("5️⃣ ПРОВЕРКА КРИТИЧЕСКИХ МЕТОДОВ:")

try:
    from core.personality_system import PersonalitySystem
    personality = PersonalitySystem()
    
    # Проверяем auto_develop_personality
    print("   🧪 Тест PersonalitySystem.auto_develop_personality()...")
    try:
        from core.long_term_memory import LongTermMemory
        ltm = LongTermMemory()
        
        # Проверяем наличие метода
        if hasattr(ltm, 'get_recent_achievements'):
            print("      ✅ LongTermMemory.get_recent_achievements() существует")
        else:
            print("      ❌ LongTermMemory.get_recent_achievements() НЕ СУЩЕСТВУЕТ!")
            print("         КРИТИЧЕСКАЯ ПРОБЛЕМА: метод не реализован!")
            
    except Exception as e:
        print(f"      ❌ Ошибка при проверке: {e}")
        
except Exception as e:
    print(f"   ❌ Не удалось импортировать PersonalitySystem: {e}")

print()

# === 6. ПРОВЕРКА ИНТЕГРАЦИИ ===
print("6️⃣ ПРОВЕРКА ИНТЕГРАЦИИ В autonomous_service.py:")

service_path = Path("/root/mirai/mirai-agent/autonomous_service.py")
if service_path.exists():
    content = service_path.read_text()
    
    checks = [
        ("Long-Term Memory", "from core.long_term_memory import LongTermMemory"),
        ("Self-Awareness", "from core.self_awareness import SelfAwareness"),
        ("Auto-Planner", "from core.auto_planner import AutoPlanner"),
        ("Self-Modification", "from core.self_modification import SelfModification"),
        ("Personality System", "from core.personality_system import PersonalitySystem"),
    ]
    
    for name, import_line in checks:
        if import_line in content:
            print(f"   ✅ {name}: интегрирована")
        else:
            print(f"   ❌ {name}: НЕ интегрирована!")
    
    # Проверяем вызовы
    print("\n   🔄 Проверка вызовов:")
    if "self.personality.auto_develop_personality()" in content:
        print("      ✅ auto_develop_personality() вызывается")
    else:
        print("      ⚠️ auto_develop_personality() НЕ вызывается")
    
    if "self.ltm.record_achievement" in content:
        print("      ✅ record_achievement() вызывается")
    else:
        print("      ⚠️ record_achievement() НЕ вызывается")
        
else:
    print("   ❌ autonomous_service.py не найден!")

print()

# === 7. РЕАЛЬНАЯ АКТИВНОСТЬ ===
print("7️⃣ РЕАЛЬНАЯ АКТИВНОСТЬ MIRAI:")

metrics_path = Path("/root/mirai/metrics/latest.json")
if metrics_path.exists():
    with open(metrics_path) as f:
        metrics = json.load(f)
    
    print(f"   📊 Циклов за час: {metrics.get('cycles_last_hour', 0)}")
    print(f"   📝 Строк логов за час: {metrics.get('log_lines_last_hour', 0)}")
    print(f"   ❌ Ошибок за час: {metrics.get('errors_last_hour', 0)}")
    print(f"   ⚠️  Предупреждений за час: {metrics.get('warnings_last_hour', 0)}")
else:
    print("   ⚠️ Метрики не найдены")

print()

# === 8. ВЫВОД ===
print("=" * 70)
print("🎯 ИТОГОВЫЙ ВЫВОД:")
print()

issues = []

# Проверяем критические проблемы
if error_count > 0:
    issues.append(f"❌ КРИТИЧНО: {error_count} ошибок за 24 часа")

# Проверяем LongTermMemory
try:
    from core.long_term_memory import LongTermMemory
    ltm = LongTermMemory()
    if not hasattr(ltm, 'get_recent_achievements'):
        issues.append("❌ КРИТИЧНО: LongTermMemory.get_recent_achievements() не существует")
except:
    issues.append("❌ КРИТИЧНО: Не удалось импортировать LongTermMemory")

# Проверяем активность Personality
if db_path.exists():
    conn = sqlite3.connect(data_dir / "personality.db")
    cursor = conn.cursor()
    cursor.execute("SELECT total_xp FROM overall_progress WHERE id = 1")
    xp = cursor.fetchone()[0]
    conn.close()
    
    if xp < 100:
        issues.append(f"⚠️ ПРОБЛЕМА: Personality System почти не используется (XP: {xp:.0f})")

if issues:
    print("🔴 НАЙДЕНЫ ПРОБЛЕМЫ:")
    for issue in issues:
        print(f"   {issue}")
    print()
    print("📋 РЕКОМЕНДАЦИИ:")
    print("   1. Реализовать недостающие методы в LongTermMemory")
    print("   2. Убедиться что auto_develop_personality() вызывается")
    print("   3. Проверить логику записи достижений")
    print("   4. Перезапустить службу после исправлений")
else:
    print("✅ ВСЁ РАБОТАЕТ ОТЛИЧНО!")
    print("   MIRAI функционирует как задумано")

print()
print("=" * 70)
