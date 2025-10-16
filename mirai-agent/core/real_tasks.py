#!/usr/bin/env python3
"""
🎯 РЕАЛЬНЫЕ Задачи для MIRAI
Замена "TODO" на конкретные действия с измеримым результатом
"""

import subprocess
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from collections import Counter
import re


class RealTaskExecutor:
    """Выполняет реальные задачи вместо TODO"""
    
    def __init__(self, base_dir: str = "/root/mirai"):
        self.base_dir = Path(base_dir)
        self.reports_dir = self.base_dir / "reports"
        self.metrics_dir = self.base_dir / "metrics"
        self.knowledge_dir = self.base_dir / "knowledge_base"
        
        # Создаём директории
        self.reports_dir.mkdir(exist_ok=True)
        self.metrics_dir.mkdir(exist_ok=True)
        self.knowledge_dir.mkdir(exist_ok=True)
    
    def task1_analyze_logs_and_report(self) -> Dict:
        """
        ЗАДАЧА 1: Анализ Логов и Создание Отчёта
        
        Измеримый результат: Файл reports/daily_analysis_YYYY-MM-DD.md создан
        """
        print("🔍 Начинаю анализ логов...")
        
        # Читаем логи за последние 24 часа
        logs = self._read_journalctl_logs(since="24 hours ago")
        
        # Анализируем
        analysis = self._analyze_logs(logs)
        
        # Создаём отчёт
        report_date = datetime.now().strftime("%Y-%m-%d")
        report_content = self._generate_report(analysis, report_date)
        
        # Сохраняем отчёт
        report_file = self.reports_dir / f"daily_analysis_{report_date}.md"
        report_file.write_text(report_content, encoding='utf-8')
        
        # Сохраняем JSON со статистикой
        stats_file = self.reports_dir / f"daily_stats_{report_date}.json"
        stats_file.write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding='utf-8')
        
        result = {
            "task": "analyze_logs_and_report",
            "status": "COMPLETED",
            "timestamp": datetime.now().isoformat(),
            "report_file": str(report_file),
            "stats_file": str(stats_file),
            "summary": {
                "total_lines": analysis['total_lines'],
                "errors": analysis['error_count'],
                "warnings": analysis['warning_count'],
                "autonomous_cycles": analysis['autonomous_cycles']
            }
        }
        
        print(f"✅ Отчёт создан: {report_file}")
        print(f"✅ Статистика: {stats_file}")
        
        return result
    
    def _read_journalctl_logs(self, since: str = "24 hours ago") -> List[str]:
        """Читает логи из journalctl"""
        try:
            cmd = ["sudo", "journalctl", "-u", "mirai", "--since", since, "--no-pager"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return result.stdout.split('\n')
            else:
                print(f"⚠️ Ошибка чтения логов: {result.stderr}")
                return []
        except Exception as e:
            print(f"❌ Не удалось прочитать логи: {e}")
            return []
    
    def _analyze_logs(self, logs: List[str]) -> Dict:
        """Анализирует логи и извлекает статистику"""
        
        analysis = {
            "total_lines": len(logs),
            "error_count": 0,
            "warning_count": 0,
            "info_count": 0,
            "autonomous_cycles": 0,
            "todo_count": 0,
            "errors": [],
            "warnings": [],
            "top_messages": [],
            "cycle_numbers": [],
            "timestamp_first": None,
            "timestamp_last": None
        }
        
        # Паттерны для поиска
        error_pattern = re.compile(r'(ERROR|error|ошибка|failed|failure)', re.IGNORECASE)
        warning_pattern = re.compile(r'(WARNING|warning|предупреждение)', re.IGNORECASE)
        cycle_pattern = re.compile(r'АВТОНОМНЫЙ ЦИКЛ #(\d+)')
        todo_pattern = re.compile(r'TODO:', re.IGNORECASE)
        
        message_counter = Counter()
        
        for line in logs:
            if not line.strip():
                continue
            
            # Считаем ошибки
            if error_pattern.search(line):
                analysis['error_count'] += 1
                # Сохраняем первые 10 уникальных ошибок
                if len(analysis['errors']) < 10:
                    error_msg = line.split(':', 3)[-1].strip()[:200]
                    if error_msg and error_msg not in analysis['errors']:
                        analysis['errors'].append(error_msg)
            
            # Считаем предупреждения
            if warning_pattern.search(line):
                analysis['warning_count'] += 1
                if len(analysis['warnings']) < 10:
                    warn_msg = line.split(':', 3)[-1].strip()[:200]
                    if warn_msg and warn_msg not in analysis['warnings']:
                        analysis['warnings'].append(warn_msg)
            
            # Считаем циклы
            cycle_match = cycle_pattern.search(line)
            if cycle_match:
                analysis['autonomous_cycles'] += 1
                cycle_num = int(cycle_match.group(1))
                analysis['cycle_numbers'].append(cycle_num)
            
            # Считаем TODO
            if todo_pattern.search(line):
                analysis['todo_count'] += 1
            
            # Считаем частые сообщения
            if any(keyword in line for keyword in ['🤖', '🌸', '✅', '❌', 'КАЙДЗЕН', 'MIRAI']):
                msg = line.split(':', 3)[-1].strip()[:100]
                if msg:
                    message_counter[msg] += 1
            
            # INFO сообщения
            if 'INFO' in line or 'info' in line:
                analysis['info_count'] += 1
        
        # Топ сообщений
        analysis['top_messages'] = [
            {"message": msg, "count": count} 
            for msg, count in message_counter.most_common(10)
        ]
        
        # Временные метки
        if logs:
            for line in logs:
                if line.strip():
                    analysis['timestamp_first'] = line.split()[0:3]
                    break
            for line in reversed(logs):
                if line.strip():
                    analysis['timestamp_last'] = line.split()[0:3]
                    break
        
        return analysis
    
    def _generate_report(self, analysis: Dict, date: str) -> str:
        """Генерирует Markdown отчёт"""
        
        report = f"""# 📊 Ежедневный Анализ Логов MIRAI

**Дата:** {date}
**Период:** Последние 24 часа
**Сгенерировано:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 📈 Общая Статистика

- **Всего строк логов:** {analysis['total_lines']:,}
- **Ошибки:** {analysis['error_count']:,}
- **Предупреждения:** {analysis['warning_count']:,}
- **Инфо сообщения:** {analysis['info_count']:,}
- **Автономных циклов:** {analysis['autonomous_cycles']:,}
- **TODO записей:** {analysis['todo_count']:,}

---

## 🔴 Топ Ошибок

"""
        
        if analysis['errors']:
            for i, error in enumerate(analysis['errors'], 1):
                report += f"{i}. `{error}`\n"
        else:
            report += "*Ошибок не найдено* ✅\n"
        
        report += "\n---\n\n## ⚠️ Топ Предупреждений\n\n"
        
        if analysis['warnings']:
            for i, warning in enumerate(analysis['warnings'], 1):
                report += f"{i}. `{warning}`\n"
        else:
            report += "*Предупреждений не найдено* ✅\n"
        
        report += "\n---\n\n## 💬 Топ Сообщений (Частота)\n\n"
        
        for item in analysis['top_messages'][:5]:
            report += f"- `{item['message']}` - **{item['count']}** раз\n"
        
        report += "\n---\n\n## 🔄 Автономные Циклы\n\n"
        
        if analysis['cycle_numbers']:
            report += f"- **Минимальный цикл:** #{min(analysis['cycle_numbers'])}\n"
            report += f"- **Максимальный цикл:** #{max(analysis['cycle_numbers'])}\n"
            report += f"- **Всего выполнено:** {len(analysis['cycle_numbers'])} циклов\n"
        else:
            report += "*Циклы не найдены*\n"
        
        report += "\n---\n\n## 🚨 TODO Проблема\n\n"
        
        if analysis['todo_count'] > 0:
            report += f"⚠️ **ВНИМАНИЕ:** Найдено {analysis['todo_count']} записей TODO!\n\n"
            report += "Это значит что MIRAI логирует намерения, но не выполняет их.\n"
            report += "**Требуется:** Заменить TODO на реальную имплементацию.\n"
        else:
            report += "✅ TODO записей не найдено - MIRAI работает корректно!\n"
        
        report += "\n---\n\n## 📊 Оценка Здоровья\n\n"
        
        # Вычисляем оценку здоровья
        health_score = 100
        
        if analysis['error_count'] > 10:
            health_score -= 30
        elif analysis['error_count'] > 5:
            health_score -= 15
        
        if analysis['todo_count'] > 10:
            health_score -= 20
        elif analysis['todo_count'] > 5:
            health_score -= 10
        
        if analysis['warning_count'] > 20:
            health_score -= 10
        
        if analysis['autonomous_cycles'] == 0:
            health_score -= 40
        
        if health_score >= 90:
            grade = "🟢 ОТЛИЧНО"
        elif health_score >= 70:
            grade = "🟡 ХОРОШО"
        elif health_score >= 50:
            grade = "🟠 УДОВЛЕТВОРИТЕЛЬНО"
        else:
            grade = "🔴 ТРЕБУЕТ ВНИМАНИЯ"
        
        report += f"**Оценка:** {health_score}/100 - {grade}\n\n"
        
        report += "---\n\n*Отчёт сгенерирован автоматически MIRAI Real Task Executor*\n"
        
        return report


def main():
    """Запуск задачи 1 для тестирования"""
    executor = RealTaskExecutor()
    result = executor.task1_analyze_logs_and_report()
    
    print("\n" + "="*60)
    print("📊 РЕЗУЛЬТАТ ВЫПОЛНЕНИЯ ЗАДАЧИ")
    print("="*60)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
